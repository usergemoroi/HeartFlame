"""
Background scheduler для отправки напоминаний и выполнения фоновых задач
Запускай отдельным процессом: python scheduler.py
"""

import asyncio
from datetime import datetime, timedelta
from database import Database
from config import settings
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import structlog

logger = structlog.get_logger()

db = Database()


async def check_expiring_streaks(bot: Bot):
    """Проверка истекающих стриков и отправка напоминаний"""
    try:
        async with await db.get_connection() as conn:
            now = datetime.now()
            
            four_hours = now + timedelta(hours=4)
            one_hour = now + timedelta(hours=1)
            thirty_min = now + timedelta(minutes=30)
            
            cursor = await conn.execute(
                """
                SELECT s.*, u1.username as user1_name, u2.username as user2_name,
                       u1.user_id as u1_id, u2.user_id as u2_id
                FROM streaks s
                JOIN users u1 ON s.user1_id = u1.user_id
                JOIN users u2 ON s.user2_id = u2.user_id
                WHERE s.is_active = 1 
                AND s.expiry BETWEEN ? AND ?
                """,
                (now, four_hours)
            )
            
            streaks = await cursor.fetchall()
            
            for streak in streaks:
                expiry = datetime.fromisoformat(streak['expiry'])
                time_left = (expiry - now).total_seconds() / 3600
                
                last_extend_u1 = datetime.fromisoformat(streak['last_extend_user1']) if streak['last_extend_user1'] else None
                last_extend_u2 = datetime.fromisoformat(streak['last_extend_user2']) if streak['last_extend_user2'] else None
                
                message = ""
                if time_left <= 0.5:
                    message = f"🚨 **СРОЧНО!** Огонёк с **{streak['user2_name']}** погаснет через 30 минут! 😱"
                elif time_left <= 1:
                    message = f"⚠️ Огонёк с **{streak['user2_name']}** погаснет через час! 🔥"
                elif time_left <= 4:
                    message = f"⏰ Напоминание: огонёк с **{streak['user2_name']}** скоро погаснет"
                
                if message:
                    if not last_extend_u1 or (now - last_extend_u1).total_seconds() > 16 * 3600:
                        try:
                            await bot.send_message(
                                streak['u1_id'],
                                message,
                                parse_mode=ParseMode.MARKDOWN_V2
                            )
                        except Exception as e:
                            logger.error("failed_to_send_reminder", user_id=streak['u1_id'], error=str(e))
                    
                    if not last_extend_u2 or (now - last_extend_u2).total_seconds() > 16 * 3600:
                        try:
                            await bot.send_message(
                                streak['u2_id'],
                                message.replace(streak['user2_name'], streak['user1_name']),
                                parse_mode=ParseMode.MARKDOWN_V2
                            )
                        except Exception as e:
                            logger.error("failed_to_send_reminder", user_id=streak['u2_id'], error=str(e))
            
            logger.info("checked_expiring_streaks", count=len(streaks))
    
    except Exception as e:
        logger.error("check_expiring_streaks_error", error=str(e))


async def expire_old_streaks():
    """Деактивация истекших стриков"""
    try:
        async with await db.get_connection() as conn:
            now = datetime.now()
            
            cursor = await conn.execute(
                """
                SELECT * FROM streaks
                WHERE is_active = 1 AND expiry < ?
                """,
                (now,)
            )
            
            expired = await cursor.fetchall()
            
            for streak in expired:
                await db.expire_streak(streak['id'])
                logger.info("streak_expired", streak_id=streak['id'], days=streak['days'])
            
            if expired:
                logger.info("expired_streaks", count=len(expired))
    
    except Exception as e:
        logger.error("expire_old_streaks_error", error=str(e))


async def generate_daily_quests():
    """Генерация ежедневных квестов для всех пользователей"""
    try:
        async with await db.get_connection() as conn:
            cursor = await conn.execute("SELECT user_id FROM users WHERE is_banned = 0")
            users = await cursor.fetchall()
            
            quests_templates = [
                {
                    "name": "Продли 3 огонька",
                    "description": "Поддержи дружбу с тремя друзьями сегодня",
                    "target": 3,
                    "reward_sparks": 50
                },
                {
                    "name": "Покорми питомца 5 раз",
                    "description": "Твой серийчик голоден!",
                    "target": 5,
                    "reward_sparks": 40
                },
                {
                    "name": "Зажги новый огонёк",
                    "description": "Найди нового друга и зажги с ним огонёк",
                    "target": 1,
                    "reward_sparks": 100
                }
            ]
            
            import random
            
            for user in users:
                existing = await db.get_user_quests(user['user_id'], completed=False)
                
                if len(existing) < 3:
                    quest = random.choice(quests_templates)
                    
                    await db.create_quest(
                        user_id=user['user_id'],
                        type_="daily",
                        name=quest['name'],
                        description=quest['description'],
                        target=quest['target'],
                        reward_sparks=quest['reward_sparks'],
                        expires_at=datetime.now() + timedelta(days=1)
                    )
            
            logger.info("generated_daily_quests", users_count=len(users))
    
    except Exception as e:
        logger.error("generate_daily_quests_error", error=str(e))


async def scheduler_loop():
    """Основной цикл планировщика"""
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2)
    )
    
    logger.info("scheduler_started")
    
    last_quest_generation = None
    
    while True:
        try:
            await check_expiring_streaks(bot)
            
            await expire_old_streaks()
            
            now = datetime.now()
            if last_quest_generation is None or (now - last_quest_generation).days >= 1:
                if now.hour == 0:
                    await generate_daily_quests()
                    last_quest_generation = now
            
            await asyncio.sleep(300)
        
        except Exception as e:
            logger.error("scheduler_loop_error", error=str(e))
            await asyncio.sleep(60)


if __name__ == "__main__":
    try:
        asyncio.run(scheduler_loop())
    except (KeyboardInterrupt, SystemExit):
        logger.info("scheduler_stopped")
