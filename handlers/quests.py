from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from database import Database
from keyboards.inline import get_quests_keyboard, get_back_keyboard
from locales import get_text
import structlog

logger = structlog.get_logger()
router = Router()
db = Database()


@router.callback_query(F.data == "menu_quests")
@router.message(Command("quests"))
async def show_quests(event):
    if isinstance(event, CallbackQuery):
        user_id = event.from_user.id
        message = event.message
        is_callback = True
    else:
        user_id = event.from_user.id
        message = event
        is_callback = False
    
    quests = await db.get_user_quests(user_id, completed=False)
    
    if not quests:
        quests_text = "🎯 Сегодня нет активных квестов\n\nВозвращайся завтра за новыми заданиями!"
    else:
        quests_text = ""
        for quest in quests:
            progress_bar = "█" * (quest['progress'] * 10 // quest['target']) + "░" * (10 - quest['progress'] * 10 // quest['target'])
            quests_text += f"\n📌 **{quest['name']}**\n"
            quests_text += f"   {quest['description']}\n"
            quests_text += f"   {progress_bar} {quest['progress']}/{quest['target']}\n"
            quests_text += f"   🎁 {quest['reward_sparks']} 🔥"
            if quest['reward_stars'] > 0:
                quests_text += f" + {quest['reward_stars']} ⭐"
            quests_text += "\n"
    
    text = get_text("quests", user_id, quests_text=quests_text)
    keyboard = get_quests_keyboard()
    
    if is_callback:
        await message.edit_text(text, reply_markup=keyboard, parse_mode="MarkdownV2")
        await event.answer()
    else:
        await message.answer(text, reply_markup=keyboard, parse_mode="MarkdownV2")


@router.callback_query(F.data.startswith("quests_"))
async def show_quests_category(callback: CallbackQuery):
    user_id = callback.from_user.id
    category = callback.data.split("_")[1]
    
    await callback.answer(f"📋 {category.upper()} квесты скоро будут доступны!", show_alert=True)
