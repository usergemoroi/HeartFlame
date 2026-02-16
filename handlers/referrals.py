from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.inline import get_back_to_menu_keyboard
from utils.text import get_text, escape_markdown

router = Router()


@router.callback_query(F.data == "menu_referrals")
async def show_referrals(callback: CallbackQuery, user_data: dict):
    lang = user_data['language']
    user_id = user_data['user_id']
    
    bot_username = (await callback.bot.me()).username
    ref_link = f"https://t\\.me/{bot_username}?start=ref{user_id}"
    
    from database.crud import get_db
    db = await get_db()
    
    cursor = await db.execute("""
        SELECT COUNT(*) FROM users WHERE referrer_id = ?
    """, (user_id,))
    level1 = (await cursor.fetchone())[0]
    
    cursor = await db.execute("""
        SELECT COUNT(*) FROM users 
        WHERE referrer_id IN (SELECT user_id FROM users WHERE referrer_id = ?)
    """, (user_id,))
    level2 = (await cursor.fetchone())[0]
    
    cursor = await db.execute("""
        SELECT COUNT(*) FROM users 
        WHERE referrer_id IN (
            SELECT user_id FROM users 
            WHERE referrer_id IN (SELECT user_id FROM users WHERE referrer_id = ?)
        )
    """, (user_id,))
    level3 = (await cursor.fetchone())[0]
    
    await db.close()
    
    total_earned = user_data.get('total_sparks_earned', 0)
    
    ref_text = get_text(
        lang,
        'referral_info',
        link=ref_link,
        ref1=level1,
        ref2=level2,
        ref3=level3,
        total=total_earned
    )
    
    await callback.message.edit_text(
        ref_text,
        reply_markup=get_back_to_menu_keyboard(lang),
        parse_mode='MarkdownV2'
    )
    
    await callback.answer()
