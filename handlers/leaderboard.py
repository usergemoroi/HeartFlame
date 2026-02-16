from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from database import Database
from keyboards.inline import get_leaderboard_keyboard, get_back_keyboard
from locales import get_text
from utils.text_utils import escape_markdown
import structlog

logger = structlog.get_logger()
router = Router()
db = Database()


@router.callback_query(F.data == "menu_top")
@router.message(Command("top"))
async def show_leaderboard(event):
    if isinstance(event, CallbackQuery):
        user_id = event.from_user.id
        message = event.message
        is_callback = True
    else:
        user_id = event.from_user.id
        message = event
        is_callback = False
    
    leaders = await db.get_leaderboard(order_by="best_streak", limit=20)
    
    leaderboard_text = ""
    for idx, leader in enumerate(leaders, 1):
        medal = ""
        if idx == 1:
            medal = "🥇"
        elif idx == 2:
            medal = "🥈"
        elif idx == 3:
            medal = "🥉"
        else:
            medal = f"{idx}\\."
        
        premium = "⭐" if leader.get('is_premium') else ""
        username = escape_markdown(leader['username'])
        
        leaderboard_text += f"{medal} {leader['avatar']} **{username}** {premium}\n"
        leaderboard_text += f"   🔥 {leader['best_streak']} дней\n\n"
    
    text = get_text("leaderboard", user_id, list=leaderboard_text)
    keyboard = get_leaderboard_keyboard()
    
    if is_callback:
        await message.edit_text(text, reply_markup=keyboard, parse_mode="MarkdownV2")
        await event.answer()
    else:
        await message.answer(text, reply_markup=keyboard, parse_mode="MarkdownV2")


@router.callback_query(F.data.startswith("top_"))
async def show_leaderboard_category(callback: CallbackQuery):
    user_id = callback.from_user.id
    category = callback.data.split("_")[1]
    
    order_map = {
        "streaks": "best_streak",
        "referrals": "total_referrals",
        "sparks": "sparks",
        "level": "level"
    }
    
    order_by = order_map.get(category, "best_streak")
    leaders = await db.get_leaderboard(order_by=order_by, limit=20)
    
    leaderboard_text = ""
    for idx, leader in enumerate(leaders, 1):
        medal = ""
        if idx == 1:
            medal = "🥇"
        elif idx == 2:
            medal = "🥈"
        elif idx == 3:
            medal = "🥉"
        else:
            medal = f"{idx}\\."
        
        premium = "⭐" if leader.get('is_premium') else ""
        username = escape_markdown(leader['username'])
        
        leaderboard_text += f"{medal} {leader['avatar']} **{username}** {premium}\n"
        
        if category == "streaks":
            leaderboard_text += f"   🔥 {leader['best_streak']} дней\n\n"
        elif category == "referrals":
            leaderboard_text += f"   👥 {leader['total_referrals']} друзей\n\n"
        elif category == "sparks":
            leaderboard_text += f"   💎 {leader['sparks']} искр\n\n"
        elif category == "level":
            leaderboard_text += f"   ⭐ Уровень {leader['level']}\n\n"
    
    text = get_text("leaderboard", user_id, list=leaderboard_text)
    keyboard = get_leaderboard_keyboard()
    
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="MarkdownV2")
    await callback.answer()
