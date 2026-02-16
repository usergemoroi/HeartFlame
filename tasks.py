import asyncio
from aiogram import Bot
from database.crud import get_db
from utils.text import get_text, get_streak_color, escape_markdown, format_time_left
from utils.time import get_current_timestamp, get_time_until_expiry, kill_streak
from config import settings
import structlog

logger = structlog.get_logger()


async def check_dying_streaks(bot: Bot):
    logger.info("Checking for dying streaks...")
    
    db = await get_db()
    now = get_current_timestamp()
    
    cursor = await db.execute("""
        SELECT s.*, 
               u1.user_id as user1_id, u1.language as user1_lang,
               u2.user_id as user2_id, u2.language as user2_lang,
               u1.nickname as user1_nick, u1.avatar as user1_avatar,
               u2.nickname as user2_nick, u2.avatar as user2_avatar
        FROM streaks s
        JOIN users u1 ON s.user1_id = u1.user_id
        JOIN users u2 ON s.user2_id = u2.user_id
        WHERE s.status = 'active' AND s.streak_expiry < ?
    """, (now + 14400,))
    
    rows = await cursor.fetchall()
    
    for row in rows:
        streak_id = row[0]
        expiry = row[5]
        days = row[3]
        
        time_left = get_time_until_expiry(expiry)
        
        if time_left <= 0:
            await kill_streak(streak_id)
            logger.info(f"Streak {streak_id} has died")
            
            from database.crud import update_pet
            if row[10]:
                await update_pet(row[10], mood='depressed')
            
            color_emoji, _ = get_streak_color(days)
            
            try:
                await bot.send_message(
                    row[11],
                    get_text(
                        row[12],
                        'flame_died',
                        days=days,
                        avatar=row[18],
                        nickname=escape_markdown(row[17])
                    ),
                    parse_mode='MarkdownV2'
                )
            except:
                pass
            
            try:
                await bot.send_message(
                    row[13],
                    get_text(
                        row[14],
                        'flame_died',
                        days=days,
                        avatar=row[16],
                        nickname=escape_markdown(row[15])
                    ),
                    parse_mode='MarkdownV2'
                )
            except:
                pass
            
            continue
        
        hours_left = time_left // 3600
        
        if hours_left in [4, 1] or (time_left <= 1800 and time_left >= 1500):
            color_emoji, _ = get_streak_color(days)
            
            try:
                await bot.send_message(
                    row[11],
                    get_text(
                        row[12],
                        'flame_dying',
                        color=color_emoji,
                        avatar=row[18],
                        nickname=escape_markdown(row[17]),
                        hours=hours_left if hours_left > 0 else 0.5
                    ),
                    parse_mode='MarkdownV2'
                )
            except:
                pass
            
            try:
                await bot.send_message(
                    row[13],
                    get_text(
                        row[14],
                        'flame_dying',
                        color=color_emoji,
                        avatar=row[16],
                        nickname=escape_markdown(row[15]),
                        hours=hours_left if hours_left > 0 else 0.5
                    ),
                    parse_mode='MarkdownV2'
                )
            except:
                pass
    
    await db.close()
    logger.info(f"Checked {len(rows)} active streaks")


async def restore_energy():
    logger.info("Restoring user energy...")
    
    db = await get_db()
    
    await db.execute("""
        UPDATE users 
        SET energy = MIN(100, energy + 1)
        WHERE energy < 100
    """)
    
    await db.commit()
    await db.close()
    
    logger.info("Energy restored")


async def reset_daily_quests():
    logger.info("Resetting daily quests...")
    
    db = await get_db()
    now = get_current_timestamp()
    
    await db.execute("""
        DELETE FROM quests 
        WHERE period = 'daily' AND created_at < ?
    """, (now - 86400,))
    
    await db.commit()
    await db.close()
    
    logger.info("Daily quests reset")


async def scheduled_tasks(bot: Bot):
    while True:
        try:
            await check_dying_streaks(bot)
        except Exception as e:
            logger.error(f"Error in check_dying_streaks: {e}")
        
        await asyncio.sleep(600)
        
        try:
            await restore_energy()
        except Exception as e:
            logger.error(f"Error in restore_energy: {e}")
        
        await asyncio.sleep(1800)


async def daily_tasks(bot: Bot):
    while True:
        await asyncio.sleep(86400)
        
        try:
            await reset_daily_quests()
        except Exception as e:
            logger.error(f"Error in reset_daily_quests: {e}")


async def start_background_tasks(bot: Bot):
    asyncio.create_task(scheduled_tasks(bot))
    asyncio.create_task(daily_tasks(bot))
    logger.info("Background tasks started")
