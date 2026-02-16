from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.inline import get_pet_actions_keyboard, get_back_to_menu_keyboard
from database.crud import get_user_pets, get_pet, feed_pet, update_pet, update_user_sparks
from utils.text import get_text, escape_markdown
from utils.time import get_current_timestamp
import random
import json

router = Router()


@router.callback_query(F.data == "menu_pets")
async def show_pets(callback: CallbackQuery, user_data: dict):
    lang = user_data['language']
    user_id = user_data['user_id']
    
    pets = await get_user_pets(user_id)
    
    if not pets:
        text = "🐣 You have no pets yet\\!\n\nLight flames with friends for 3 days to hatch one\\!" if lang == 'en' else "🐣 У тебя пока нет питомцев\\!\n\nДержи огоньки с друзьями 3 дня, чтобы вылупился питомец\\!"
        
        await callback.message.edit_text(
            text,
            reply_markup=get_back_to_menu_keyboard(lang),
            parse_mode='MarkdownV2'
        )
        await callback.answer()
        return
    
    pet = pets[0]
    
    xp_needed = 100 * (pet['level'] ** 1.5)
    
    mood_emojis = {
        'happy': '😊',
        'neutral': '😐',
        'sad': '😢',
        'depressed': '😭'
    }
    
    items_list = json.loads(pet.get('items', '[]'))
    items_display = ' '.join(items_list[:10]) if items_list else "None" if lang == 'en' else "Нет"
    
    now = get_current_timestamp()
    age_days = (now - pet['created_at']) // 86400
    
    pet_text = get_text(
        lang,
        'pet_profile',
        pet=pet['pet_emoji'],
        pet_name=escape_markdown(pet['pet_name']),
        level=pet['level'],
        rarity=pet['rarity'].upper(),
        mood=mood_emojis.get(pet['mood'], '😊'),
        xp=pet['xp'],
        max_xp=int(xp_needed),
        age=age_days,
        items=items_display
    )
    
    await callback.message.edit_text(
        pet_text,
        reply_markup=get_pet_actions_keyboard(pet['pet_id'], lang),
        parse_mode='MarkdownV2'
    )
    
    await callback.answer()


@router.callback_query(F.data.startswith("pet_feed_"))
async def feed_pet_action(callback: CallbackQuery, user_data: dict):
    pet_id = int(callback.data.split("_")[2])
    lang = user_data['language']
    
    if user_data['sparks'] < 30:
        await callback.answer(
            "Not enough sparks! Need 30 🔥" if lang == 'en' else "Недостаточно искр! Нужно 30 🔥",
            show_alert=True
        )
        return
    
    pet = await get_pet(pet_id)
    
    if not pet:
        await callback.answer("Pet not found" if lang == 'en' else "Питомец не найден", show_alert=True)
        return
    
    xp_gain = random.randint(15, 30)
    
    await feed_pet(pet_id, xp_gain)
    await update_user_sparks(user_data['user_id'], -30)
    
    new_xp = pet['xp'] + xp_gain
    xp_needed = 100 * (pet['level'] ** 1.5)
    
    if new_xp >= xp_needed:
        new_level = pet['level'] + 1
        await update_pet(pet_id, level=new_level, xp=0, mood='happy')
        
        from config import PET_TYPES
        
        if new_level % 5 == 0 and pet['rarity'] != 'mythic':
            rarity_upgrade = {
                'common': 'rare',
                'rare': 'epic',
                'epic': 'legendary',
                'legendary': 'mythic'
            }
            new_rarity = rarity_upgrade.get(pet['rarity'], pet['rarity'])
            new_emoji = random.choice(PET_TYPES[new_rarity])
            
            await update_pet(pet_id, rarity=new_rarity, pet_emoji=new_emoji)
            
            await callback.message.answer(
                get_text(
                    lang,
                    'pet_evolved',
                    old_pet=pet['pet_emoji'],
                    new_pet=new_emoji,
                    pet_name=escape_markdown(pet['pet_name']),
                    level=new_level
                ),
                parse_mode='MarkdownV2'
            )
        else:
            await callback.message.answer(
                f"🎉 *Level Up\\!* {pet['pet_emoji']} is now level {new_level}\\!",
                parse_mode='MarkdownV2'
            )
    else:
        await update_pet(pet_id, mood='happy')
    
    await callback.message.edit_text(
        get_text(
            lang,
            'pet_feed',
            pet_name=escape_markdown(pet['pet_name']),
            xp=xp_gain,
            pet=pet['pet_emoji']
        ),
        parse_mode='MarkdownV2'
    )
    
    await callback.answer()


@router.callback_query(F.data.startswith("pet_pet_"))
async def pet_pet_action(callback: CallbackQuery, user_data: dict):
    pet_id = int(callback.data.split("_")[2])
    lang = user_data['language']
    
    pet = await get_pet(pet_id)
    
    if not pet:
        await callback.answer("Pet not found" if lang == 'en' else "Питомец не найден", show_alert=True)
        return
    
    mood_upgrade = {
        'depressed': 'sad',
        'sad': 'neutral',
        'neutral': 'happy',
        'happy': 'happy'
    }
    
    new_mood = mood_upgrade.get(pet['mood'], 'happy')
    await update_pet(pet_id, mood=new_mood)
    
    await callback.message.edit_text(
        get_text(
            lang,
            'pet_pet',
            pet_name=escape_markdown(pet['pet_name']),
            pet=pet['pet_emoji']
        ),
        parse_mode='MarkdownV2'
    )
    
    await callback.answer()


@router.callback_query(F.data.startswith("pet_play_"))
async def pet_play_action(callback: CallbackQuery, user_data: dict):
    lang = user_data['language']
    
    await callback.answer(
        "Mini-game coming soon! 🎮" if lang == 'en' else "Мини-игра скоро! 🎮",
        show_alert=True
    )


@router.callback_query(F.data.startswith("pet_customize_"))
async def pet_customize_action(callback: CallbackQuery, user_data: dict):
    lang = user_data['language']
    
    await callback.answer(
        "Customization coming soon! 🎨" if lang == 'en' else "Кастомизация скоро! 🎨",
        show_alert=True
    )


@router.callback_query(F.data.startswith("streak_pet_"))
async def show_streak_pet(callback: CallbackQuery, user_data: dict):
    streak_id = int(callback.data.split("_")[2])
    lang = user_data['language']
    
    from database.crud import get_user_streaks
    streaks = await get_user_streaks(user_data['user_id'])
    streak = next((s for s in streaks if s['streak_id'] == streak_id), None)
    
    if not streak or not streak.get('pet_id'):
        await callback.answer(
            "No pet yet! Reach 3 days to hatch one" if lang == 'en' else "Питомца пока нет! Достигни 3 дней, чтобы он вылупился",
            show_alert=True
        )
        return
    
    pet = await get_pet(streak['pet_id'])
    
    if not pet:
        await callback.answer("Pet not found" if lang == 'en' else "Питомец не найден", show_alert=True)
        return
    
    xp_needed = 100 * (pet['level'] ** 1.5)
    
    mood_emojis = {
        'happy': '😊',
        'neutral': '😐',
        'sad': '😢',
        'depressed': '😭'
    }
    
    items_list = json.loads(pet.get('items', '[]'))
    items_display = ' '.join(items_list[:10]) if items_list else "None" if lang == 'en' else "Нет"
    
    now = get_current_timestamp()
    age_days = (now - pet['created_at']) // 86400
    
    pet_text = get_text(
        lang,
        'pet_profile',
        pet=pet['pet_emoji'],
        pet_name=escape_markdown(pet['pet_name']),
        level=pet['level'],
        rarity=pet['rarity'].upper(),
        mood=mood_emojis.get(pet['mood'], '😊'),
        xp=pet['xp'],
        max_xp=int(xp_needed),
        age=age_days,
        items=items_display
    )
    
    await callback.message.answer(
        pet_text,
        reply_markup=get_pet_actions_keyboard(pet['pet_id'], lang),
        parse_mode='MarkdownV2'
    )
    
    await callback.answer()
