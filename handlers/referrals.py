from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from database import Database
from keyboards.inline import get_referrals_keyboard, get_back_keyboard
from locales import get_text
from utils.text_utils import generate_referral_link
from config.constants import REFERRAL_REWARDS
import structlog

logger = structlog.get_logger()
router = Router()
db = Database()


@router.callback_query(F.data == "menu_referrals")
@router.message(Command("referrals"))
async def show_referrals(event):
    if isinstance(event, CallbackQuery):
        user_id = event.from_user.id
        message = event.message
        is_callback = True
        bot_username = (await event.bot.me()).username
    else:
        user_id = event.from_user.id
        message = event
        is_callback = False
        bot_username = (await event.bot.me()).username
    
    user = await db.get_user(user_id)
    referral_count = await db.get_referral_count(user_id)
    
    rewards_earned = 0
    async with await db.get_connection() as conn:
        cursor = await conn.execute(
            "SELECT SUM(reward_value) as total FROM referral_rewards WHERE user_id = ? AND reward_type = 'sparks'",
            (user_id,)
        )
        row = await cursor.fetchone()
        if row and row['total']:
            rewards_earned = row['total']
    
    rewards_text = ""
    for milestone, reward in sorted(REFERRAL_REWARDS.items()):
        status = "✅" if referral_count >= milestone else "🔒"
        rewards_text += f"{status} {milestone} друзей → {reward} 🔥\n"
    
    link = generate_referral_link(bot_username, user_id)
    
    text = get_text(
        "referrals",
        user_id,
        link=link,
        count=referral_count,
        earned=rewards_earned,
        rewards=rewards_text
    )
    
    keyboard = get_referrals_keyboard(bot_username, user_id)
    
    if is_callback:
        await message.edit_text(text, reply_markup=keyboard, parse_mode="MarkdownV2")
        await event.answer()
    else:
        await message.answer(text, reply_markup=keyboard, parse_mode="MarkdownV2")


@router.callback_query(F.data == "ref_copy")
async def copy_referral_link(callback: CallbackQuery):
    await callback.answer("📋 Скопируй ссылку из сообщения выше!", show_alert=True)
