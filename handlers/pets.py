from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from database import Database
from keyboards.inline import get_pet_keyboard, get_back_keyboard
from locales import get_text
from utils.pet_utils import (
    calculate_pet_exp_for_level,
    get_pet_state_emoji,
    get_mood_emoji,
    check_pet_evolution
)
from config.constants import PetState, PetMood
import random
import structlog

logger = structlog.get_logger()
router = Router()
db = Database()


@router.callback_query(F.data == "menu_pet")
@router.message(Command("pet"))
async def show_pet(event):
    if isinstance(event, CallbackQuery):
        user_id = event.from_user.id
        message = event.message
        is_callback = True
    else:
        user_id = event.from_user.id
        message = event
        is_callback = False
    
    pets = await db.get_user_pets(user_id)
    
    if not pets:
        text = get_text("no_pet", user_id)
        keyboard = get_pet_keyboard(None)
    else:
        pet = pets[0]
        
        state_emoji = get_pet_state_emoji(PetState(pet['state']))
        mood_emoji = get_mood_emoji(PetMood(pet['mood']))
        
        next_level_exp = calculate_pet_exp_for_level(pet['level'] + 1)
        
        status_text = ""
        if pet['mood'] == PetMood.HAPPY.value:
            status_text = "Питомец счастлив! 😊"
        elif pet['mood'] == PetMood.HUNGRY.value:
            status_text = "Питомец хочет кушать... 😋"
        elif pet['mood'] == PetMood.SAD.value:
            status_text = "Питомец грустит 😢"
        elif pet['mood'] == PetMood.DEPRESSED.value:
            status_text = "Питомец в депрессии... 😭"
        
        text = get_text(
            "pet_status",
            user_id,
            emoji=pet['emoji'],
            name=pet['name'],
            state=pet['state'],
            mood=mood_emoji,
            level=pet['level'],
            exp=pet['exp'],
            next_exp=next_level_exp,
            lives=pet['lives'],
            status_text=status_text
        )
        keyboard = get_pet_keyboard(pet['id'])
    
    if is_callback:
        await message.edit_text(text, reply_markup=keyboard, parse_mode="MarkdownV2")
        await event.answer()
    else:
        await message.answer(text, reply_markup=keyboard, parse_mode="MarkdownV2")


@router.callback_query(F.data.startswith("pet_feed_"))
async def feed_pet(callback: CallbackQuery):
    user_id = callback.from_user.id
    pet_id = int(callback.data.split("_")[2])
    
    user = await db.get_user(user_id)
    pet = await db.get_pet(pet_id)
    
    if not pet or pet['user_id'] != user_id:
        await callback.answer("❌ Питомец не найден", show_alert=True)
        return
    
    feed_cost = 30
    
    if user['sparks'] < feed_cost:
        await callback.answer(get_text("not_enough_sparks", user_id), show_alert=True)
        return
    
    await db.add_sparks(user_id, -feed_cost)
    
    exp_gain = random.randint(15, 30)
    new_exp = pet['exp'] + exp_gain
    new_level = pet['level']
    
    next_level_exp = calculate_pet_exp_for_level(new_level + 1)
    
    while new_exp >= next_level_exp:
        new_exp -= next_level_exp
        new_level += 1
        next_level_exp = calculate_pet_exp_for_level(new_level + 1)
    
    current_state = PetState(pet['state'])
    new_state = check_pet_evolution(new_level, current_state)
    
    await db.update_pet(
        pet_id,
        exp=new_exp,
        level=new_level,
        state=new_state.value,
        mood=PetMood.HAPPY.value
    )
    
    if new_state != current_state:
        await callback.message.answer(
            get_text(
                "pet_evolved",
                user_id,
                old=get_pet_state_emoji(current_state),
                new=get_pet_state_emoji(new_state)
            ),
            parse_mode="MarkdownV2"
        )
    
    await callback.answer(
        get_text("feed_success", user_id, exp=exp_gain),
        show_alert=True
    )
    
    await show_pet(callback)


@router.callback_query(F.data.startswith("pet_pet_"))
async def pet_pet(callback: CallbackQuery):
    user_id = callback.from_user.id
    pet_id = int(callback.data.split("_")[2])
    
    pet = await db.get_pet(pet_id)
    
    if not pet or pet['user_id'] != user_id:
        await callback.answer("❌ Питомец не найден", show_alert=True)
        return
    
    current_mood = PetMood(pet['mood'])
    
    if current_mood == PetMood.DEPRESSED:
        new_mood = PetMood.SAD
    elif current_mood == PetMood.SAD:
        new_mood = PetMood.NEUTRAL
    elif current_mood == PetMood.NEUTRAL or current_mood == PetMood.HUNGRY:
        new_mood = PetMood.HAPPY
    else:
        new_mood = current_mood
    
    await db.update_pet(pet_id, mood=new_mood.value)
    
    await callback.answer(get_text("pet_success", user_id), show_alert=True)
    await show_pet(callback)


@router.callback_query(F.data.startswith("pet_play_"))
async def play_with_pet(callback: CallbackQuery):
    user_id = callback.from_user.id
    pet_id = int(callback.data.split("_")[2])
    
    user = await db.get_user(user_id)
    pet = await db.get_pet(pet_id)
    
    if not pet or pet['user_id'] != user_id:
        await callback.answer("❌ Питомец не найден", show_alert=True)
        return
    
    energy_cost = 20
    
    if user['energy'] < energy_cost:
        await callback.answer("⚡ Недостаточно энергии!", show_alert=True)
        return
    
    await db.update_user(user_id, energy=user['energy'] - energy_cost)
    
    sparks_earned = random.randint(5, 15)
    await db.add_sparks(user_id, sparks_earned)
    
    exp_gain = random.randint(10, 20)
    new_exp = pet['exp'] + exp_gain
    
    await db.update_pet(pet_id, exp=new_exp, mood=PetMood.HAPPY.value)
    
    await callback.answer(
        f"🎮 Отличная игра! +{sparks_earned} 🔥 и +{exp_gain} опыта!",
        show_alert=True
    )
    
    await show_pet(callback)


@router.callback_query(F.data.startswith("pet_dance_"))
async def dance_with_pet(callback: CallbackQuery):
    user_id = callback.from_user.id
    pet_id = int(callback.data.split("_")[2])
    
    pet = await db.get_pet(pet_id)
    
    if not pet or pet['user_id'] != user_id:
        await callback.answer("❌ Питомец не найден", show_alert=True)
        return
    
    animations = [
        "💃🕺 Танцуем вместе!",
        "🎵 Зажигательный танец!",
        "✨ Магический танец!",
        "🌟 Космический танец!",
    ]
    
    animation = random.choice(animations)
    
    exp_gain = random.randint(5, 10)
    await db.update_pet(pet_id, exp=pet['exp'] + exp_gain)
    
    await callback.answer(f"{animation} +{exp_gain} опыта!", show_alert=True)
    await show_pet(callback)


@router.callback_query(F.data.startswith("pet_customize_"))
async def customize_pet(callback: CallbackQuery):
    user_id = callback.from_user.id
    
    await callback.answer("✨ Кастомизация скоро будет доступна!", show_alert=True)
