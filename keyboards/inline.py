from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import List, Optional
from config.constants import Language, STARTER_AVATARS


def get_language_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    builder.button(text="🇷🇺 Русский", callback_data=f"lang_{Language.RU.value}")
    builder.button(text="🇬🇧 English", callback_data=f"lang_{Language.EN.value}")
    builder.button(text="🇪🇸 Español", callback_data=f"lang_{Language.ES.value}")
    builder.button(text="🇨🇳 中文", callback_data=f"lang_{Language.ZH.value}")
    
    builder.adjust(2)
    return builder.as_markup()


def get_avatar_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    for i, avatar in enumerate(STARTER_AVATARS):
        builder.button(text=avatar, callback_data=f"avatar_{i}")
    
    builder.adjust(4)
    return builder.as_markup()


def get_menu_keyboard(user_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    builder.button(text="👤 Профиль", callback_data="menu_profile")
    builder.button(text="🔥 Огоньки", callback_data="menu_streaks")
    builder.button(text="👥 Друзья", callback_data="menu_friends")
    builder.button(text="🐾 Питомец", callback_data="menu_pet")
    builder.button(text="🛒 Магазин", callback_data="menu_shop")
    builder.button(text="⚔️ Квесты", callback_data="menu_quests")
    builder.button(text="🏆 Топ", callback_data="menu_top")
    builder.button(text="🎁 Рефералы", callback_data="menu_referrals")
    
    builder.adjust(2)
    return builder.as_markup()


def get_profile_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    builder.button(text="🔄 Обновить", callback_data="profile_refresh")
    builder.button(text="◀️ Назад", callback_data="menu_main")
    
    builder.adjust(2)
    return builder.as_markup()


def get_streaks_keyboard(has_streaks: bool = False) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    builder.button(text="➕ Зажечь огонёк", callback_data="streak_new")
    
    if has_streaks:
        builder.button(text="⚡ Продлить все", callback_data="streak_extend_all")
    
    builder.button(text="💡 Кого зажечь?", callback_data="streak_suggest")
    builder.button(text="◀️ Назад", callback_data="menu_main")
    
    builder.adjust(2)
    return builder.as_markup()


def get_streak_actions_keyboard(streak_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    builder.button(text="⚡ Продлить", callback_data=f"streak_extend_{streak_id}")
    builder.button(text="🎁 Подарок", callback_data=f"streak_gift_{streak_id}")
    builder.button(text="◀️ Назад", callback_data="menu_streaks")
    
    builder.adjust(2)
    return builder.as_markup()


def get_streak_request_keyboard(request_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    builder.button(text="✅ Принять", callback_data=f"streak_accept_{request_id}")
    builder.button(text="❌ Отклонить", callback_data=f"streak_reject_{request_id}")
    
    builder.adjust(2)
    return builder.as_markup()


def get_pet_keyboard(pet_id: Optional[int] = None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    if pet_id:
        builder.button(text="🍖 Покормить", callback_data=f"pet_feed_{pet_id}")
        builder.button(text="🤗 Погладить", callback_data=f"pet_pet_{pet_id}")
        builder.button(text="🎮 Играть", callback_data=f"pet_play_{pet_id}")
        builder.button(text="💃 Потанцевать", callback_data=f"pet_dance_{pet_id}")
        builder.button(text="✨ Кастомизация", callback_data=f"pet_customize_{pet_id}")
    
    builder.button(text="◀️ Назад", callback_data="menu_main")
    
    builder.adjust(2)
    return builder.as_markup()


def get_shop_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    builder.button(text="⚡ Бусты", callback_data="shop_boosts")
    builder.button(text="🥚 Питомцы", callback_data="shop_pets")
    builder.button(text="✨ Кастомизация", callback_data="shop_custom")
    builder.button(text="🎁 Подарки", callback_data="shop_gifts")
    builder.button(text="◀️ Назад", callback_data="menu_main")
    
    builder.adjust(2)
    return builder.as_markup()


def get_shop_items_keyboard(category: str) -> InlineKeyboardMarkup:
    from config.constants import SHOP_ITEMS
    
    builder = InlineKeyboardBuilder()
    
    items = {k: v for k, v in SHOP_ITEMS.items() if category in k or category == "boosts"}
    
    for item_id, item in items.items():
        price_str = f"{item['price']} {'🔥' if item['currency'] == 'sparks' else '⭐'}"
        builder.button(
            text=f"{item['name']} - {price_str}",
            callback_data=f"buy_{item_id}"
        )
    
    builder.button(text="◀️ Назад", callback_data="menu_shop")
    builder.adjust(1)
    return builder.as_markup()


def get_referrals_keyboard(bot_username: str, user_id: int) -> InlineKeyboardMarkup:
    from utils.text_utils import generate_referral_link
    
    builder = InlineKeyboardBuilder()
    
    link = generate_referral_link(bot_username, user_id)
    builder.button(text="📤 Поделиться ссылкой", url=f"https://t.me/share/url?url={link}")
    builder.button(text="📋 Скопировать", callback_data="ref_copy")
    builder.button(text="◀️ Назад", callback_data="menu_main")
    
    builder.adjust(1)
    return builder.as_markup()


def get_quests_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    builder.button(text="📅 Ежедневные", callback_data="quests_daily")
    builder.button(text="📆 Еженедельные", callback_data="quests_weekly")
    builder.button(text="🎭 Сезонные", callback_data="quests_seasonal")
    builder.button(text="◀️ Назад", callback_data="menu_main")
    
    builder.adjust(2)
    return builder.as_markup()


def get_leaderboard_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    builder.button(text="🔥 По стрикам", callback_data="top_streaks")
    builder.button(text="👥 По рефералам", callback_data="top_referrals")
    builder.button(text="💎 По искрам", callback_data="top_sparks")
    builder.button(text="⭐ По уровню", callback_data="top_level")
    builder.button(text="◀️ Назад", callback_data="menu_main")
    
    builder.adjust(2)
    return builder.as_markup()


def get_back_keyboard(callback_data: str = "menu_main") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="◀️ Назад", callback_data=callback_data)
    return builder.as_markup()


def get_pagination_keyboard(
    current_page: int,
    total_pages: int,
    callback_prefix: str,
    back_callback: str = "menu_main"
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    if current_page > 0:
        builder.button(text="◀️", callback_data=f"{callback_prefix}_{current_page - 1}")
    
    builder.button(text=f"{current_page + 1}/{total_pages}", callback_data="noop")
    
    if current_page < total_pages - 1:
        builder.button(text="▶️", callback_data=f"{callback_prefix}_{current_page + 1}")
    
    builder.button(text="◀️ Назад", callback_data=back_callback)
    
    builder.adjust(3, 1)
    return builder.as_markup()
