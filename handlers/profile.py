from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from database import Database
from keyboards.inline import get_profile_keyboard
from locales import get_text
from config.constants import ENERGY_MAX
import structlog

logger = structlog.get_logger()
router = Router()
db = Database()


@router.callback_query(F.data == "menu_profile")
async def show_profile(callback: CallbackQuery):
    user_id = callback.from_user.id
    user = await db.get_user(user_id)
    
    if not user:
        await callback.answer("❌ Пользователь не найден", show_alert=True)
        return
    
    await db.update_energy(user_id)
    user = await db.get_user(user_id)
    
    streaks = await db.get_user_streaks(user_id)
    achievements = await db.get_user_achievements(user_id)
    
    achievements_text = ""
    if achievements:
        achievements_text = "\n".join([
            f"{a['emoji']} {a['name']}" for a in achievements[:5]
        ])
    else:
        achievements_text = get_text("no_achievements", user_id)
    
    profile_text = get_text(
        "profile",
        user_id,
        avatar=user['avatar'],
        username=user['username'],
        user_id=user_id,
        sparks=user['sparks'],
        stars=user['stars'],
        energy=user['energy'],
        max_energy=ENERGY_MAX,
        active_streaks=len(streaks),
        best_streak=user['best_streak'],
        level=user['level'],
        referrals=user['total_referrals'],
        achievements=achievements_text
    )
    
    await callback.message.edit_text(
        profile_text,
        reply_markup=get_profile_keyboard(),
        parse_mode="MarkdownV2"
    )
    await callback.answer()


@router.callback_query(F.data == "profile_refresh")
async def refresh_profile(callback: CallbackQuery):
    await show_profile(callback)
    # callback.answer уже вызван в show_profile


@router.message(Command("profile"))
async def cmd_profile(message: Message):
    user_id = message.from_user.id
    user = await db.get_user(user_id)
    
    if not user:
        await message.answer("❌ Профиль не найден. Используй /start")
        return
    
    await db.update_energy(user_id)
    user = await db.get_user(user_id)
    
    streaks = await db.get_user_streaks(user_id)
    achievements = await db.get_user_achievements(user_id)
    
    achievements_text = ""
    if achievements:
        achievements_text = "\n".join([
            f"{a['emoji']} {a['name']}" for a in achievements[:5]
        ])
    else:
        achievements_text = get_text("no_achievements", user_id)
    
    profile_text = get_text(
        "profile",
        user_id,
        avatar=user['avatar'],
        username=user['username'],
        user_id=user_id,
        sparks=user['sparks'],
        stars=user['stars'],
        energy=user['energy'],
        max_energy=ENERGY_MAX,
        active_streaks=len(streaks),
        best_streak=user['best_streak'],
        level=user['level'],
        referrals=user['total_referrals'],
        achievements=achievements_text
    )
    
    await message.answer(
        profile_text,
        reply_markup=get_profile_keyboard(),
        parse_mode="MarkdownV2"
    )
