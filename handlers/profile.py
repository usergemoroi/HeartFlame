from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.inline import get_back_to_menu_keyboard
from database.crud import get_user_pets
from utils.text import get_text, escape_markdown
from utils.time import format_date

router = Router()


@router.callback_query(F.data == "menu_profile")
async def show_profile(callback: CallbackQuery, user_data: dict):
    lang = user_data['language']
    
    pets = await get_user_pets(user_data['user_id'])
    max_pet_level = max([p['level'] for p in pets], default=0)
    
    language_name = {
        'en': '🇺🇸 English',
        'ru': '🇷🇺 Русский',
        'es': '🇪🇸 Español',
        'fr': '🇫🇷 Français',
        'de': '🇩🇪 Deutsch',
    }.get(lang, lang)
    
    profile_text = get_text(
        lang,
        'profile',
        avatar=user_data['avatar'],
        nickname=escape_markdown(user_data['nickname']),
        user_id=user_data['user_id'],
        language=language_name,
        sparks=user_data['sparks'],
        stars=user_data['stars'],
        energy=user_data['energy'],
        active_streaks=user_data['active_streaks'],
        max_streak=user_data['max_streak'],
        pets_count=len(pets),
        max_pet_level=max_pet_level,
        referrals=user_data['total_referrals'],
        friends_count=user_data['active_streaks'],
        joined_date=format_date(user_data['created_at'], lang)
    )
    
    await callback.message.edit_text(
        profile_text,
        reply_markup=get_back_to_menu_keyboard(lang),
        parse_mode='MarkdownV2'
    )
    
    await callback.answer()
