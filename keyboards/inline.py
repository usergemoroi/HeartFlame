from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import LANGUAGES, STARTER_AVATARS, GIFT_ITEMS
from typing import List, Dict, Any


def get_language_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    for code, name in LANGUAGES.items():
        builder.button(text=name, callback_data=f"lang_{code}")
    
    builder.adjust(2)
    return builder.as_markup()


def get_avatar_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    for avatar in STARTER_AVATARS:
        builder.button(text=avatar, callback_data=f"avatar_{avatar}")
    
    builder.adjust(4)
    return builder.as_markup()


def get_tutorial_keyboard(step: int, lang: str = 'en') -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    if step < 3:
        next_text = "Next ➡️" if lang == 'en' else "Далее ➡️"
        builder.button(text=next_text, callback_data=f"tutorial_{step + 1}")
    else:
        start_text = "🔥 Let's Go!" if lang == 'en' else "🔥 Поехали!"
        builder.button(text=start_text, callback_data="tutorial_complete")
    
    return builder.as_markup()


def get_main_menu_keyboard(lang: str = 'en') -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    buttons = {
        'en': [
            ("👤 Profile", "menu_profile"),
            ("🔥 My Flames", "menu_streaks"),
            ("🐣 My Pets", "menu_pets"),
            ("👥 Friends", "menu_friends"),
            ("🛒 Shop", "menu_shop"),
            ("🎁 Gifts", "menu_gifts"),
            ("📋 Quests", "menu_quests"),
            ("🏆 Leaderboard", "menu_leaderboard"),
            ("💫 Referrals", "menu_referrals"),
            ("🎮 Mini-Games", "menu_games"),
        ],
        'ru': [
            ("👤 Профиль", "menu_profile"),
            ("🔥 Мои огоньки", "menu_streaks"),
            ("🐣 Мои питомцы", "menu_pets"),
            ("👥 Друзья", "menu_friends"),
            ("🛒 Магазин", "menu_shop"),
            ("🎁 Подарки", "menu_gifts"),
            ("📋 Квесты", "menu_quests"),
            ("🏆 Лидерборд", "menu_leaderboard"),
            ("💫 Рефералы", "menu_referrals"),
            ("🎮 Мини-игры", "menu_games"),
        ]
    }
    
    for text, callback in buttons.get(lang, buttons['en']):
        builder.button(text=text, callback_data=callback)
    
    builder.adjust(2)
    return builder.as_markup()


def get_back_to_menu_keyboard(lang: str = 'en') -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    back_text = "🏠 Main Menu" if lang == 'en' else "🏠 Главное меню"
    builder.button(text=back_text, callback_data="menu_main")
    
    return builder.as_markup()


def get_streaks_keyboard(lang: str = 'en') -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    if lang == 'ru':
        builder.button(text="🔥 Зажечь новый огонёк", callback_data="streak_new")
        builder.button(text="🔄 Обновить", callback_data="menu_streaks")
        builder.button(text="🏠 Главное меню", callback_data="menu_main")
    else:
        builder.button(text="🔥 Light New Flame", callback_data="streak_new")
        builder.button(text="🔄 Refresh", callback_data="menu_streaks")
        builder.button(text="🏠 Main Menu", callback_data="menu_main")
    
    builder.adjust(1)
    return builder.as_markup()


def get_streak_actions_keyboard(streak_id: int, lang: str = 'en') -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    if lang == 'ru':
        builder.button(text="🔥 Продлить", callback_data=f"streak_extend_{streak_id}")
        builder.button(text="🐣 Питомец", callback_data=f"streak_pet_{streak_id}")
        builder.button(text="🎁 Подарить", callback_data=f"streak_gift_{streak_id}")
        builder.button(text="◀️ Назад", callback_data="menu_streaks")
    else:
        builder.button(text="🔥 Extend", callback_data=f"streak_extend_{streak_id}")
        builder.button(text="🐣 Pet", callback_data=f"streak_pet_{streak_id}")
        builder.button(text="🎁 Gift", callback_data=f"streak_gift_{streak_id}")
        builder.button(text="◀️ Back", callback_data="menu_streaks")
    
    builder.adjust(2)
    return builder.as_markup()


def get_flame_request_keyboard(request_id: int, lang: str = 'en') -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    if lang == 'ru':
        builder.button(text="✅ Принять", callback_data=f"flame_accept_{request_id}")
        builder.button(text="❌ Отклонить", callback_data=f"flame_reject_{request_id}")
    else:
        builder.button(text="✅ Accept", callback_data=f"flame_accept_{request_id}")
        builder.button(text="❌ Decline", callback_data=f"flame_reject_{request_id}")
    
    builder.adjust(2)
    return builder.as_markup()


def get_pet_actions_keyboard(pet_id: int, lang: str = 'en') -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    if lang == 'ru':
        builder.button(text="🍖 Покормить", callback_data=f"pet_feed_{pet_id}")
        builder.button(text="🤗 Погладить", callback_data=f"pet_pet_{pet_id}")
        builder.button(text="🎮 Поиграть", callback_data=f"pet_play_{pet_id}")
        builder.button(text="🎨 Кастомизация", callback_data=f"pet_customize_{pet_id}")
        builder.button(text="◀️ Назад", callback_data="menu_pets")
    else:
        builder.button(text="🍖 Feed", callback_data=f"pet_feed_{pet_id}")
        builder.button(text="🤗 Pet", callback_data=f"pet_pet_{pet_id}")
        builder.button(text="🎮 Play", callback_data=f"pet_play_{pet_id}")
        builder.button(text="🎨 Customize", callback_data=f"pet_customize_{pet_id}")
        builder.button(text="◀️ Back", callback_data="menu_pets")
    
    builder.adjust(2)
    return builder.as_markup()


def get_shop_keyboard(lang: str = 'en') -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    if lang == 'ru':
        items = [
            ("🛡️ Щит огонька (100🔥)", "shop_buy_shield"),
            ("💫 x2 искры (24ч) (150🔥)", "shop_buy_boost"),
            ("❤️ Доп. жизнь (120⭐)", "shop_buy_life"),
            ("🔥 Воскрешение (300⭐)", "shop_buy_revive"),
            ("🎨 Скины питомцев", "shop_skins"),
            ("🏠 Главное меню", "menu_main"),
        ]
    else:
        items = [
            ("🛡️ Flame Shield (100🔥)", "shop_buy_shield"),
            ("💫 x2 sparks (24h) (150🔥)", "shop_buy_boost"),
            ("❤️ Extra Life (120⭐)", "shop_buy_life"),
            ("🔥 Revival (300⭐)", "shop_buy_revive"),
            ("🎨 Pet Skins", "shop_skins"),
            ("🏠 Main Menu", "menu_main"),
        ]
    
    for text, callback in items:
        builder.button(text=text, callback_data=callback)
    
    builder.adjust(1)
    return builder.as_markup()


def get_gifts_keyboard(friend_id: int, lang: str = 'en') -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    for gift_type, data in GIFT_ITEMS.items():
        text = f"{data['emoji']} {data['name']} ({data['sparks']}🔥)"
        builder.button(text=text, callback_data=f"gift_send_{friend_id}_{gift_type}")
    
    back_text = "◀️ Back" if lang == 'en' else "◀️ Назад"
    builder.button(text=back_text, callback_data="menu_gifts")
    
    builder.adjust(2)
    return builder.as_markup()


def get_quests_keyboard(lang: str = 'en') -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    if lang == 'ru':
        builder.button(text="🔄 Обновить", callback_data="menu_quests")
        builder.button(text="🏠 Главное меню", callback_data="menu_main")
    else:
        builder.button(text="🔄 Refresh", callback_data="menu_quests")
        builder.button(text="🏠 Main Menu", callback_data="menu_main")
    
    builder.adjust(1)
    return builder.as_markup()


def get_leaderboard_keyboard(lang: str = 'en') -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    if lang == 'ru':
        builder.button(text="🔥 По сериям", callback_data="lb_streak")
        builder.button(text="💰 По искрам", callback_data="lb_sparks")
        builder.button(text="👥 По рефералам", callback_data="lb_referrals")
        builder.button(text="🏠 Главное меню", callback_data="menu_main")
    else:
        builder.button(text="🔥 By Streaks", callback_data="lb_streak")
        builder.button(text="💰 By Sparks", callback_data="lb_sparks")
        builder.button(text="👥 By Referrals", callback_data="lb_referrals")
        builder.button(text="🏠 Main Menu", callback_data="menu_main")
    
    builder.adjust(3)
    return builder.as_markup()


def get_games_keyboard(lang: str = 'en') -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    if lang == 'ru':
        builder.button(text="✨ Ловец искр", callback_data="game_sparks")
        builder.button(text="🎯 Скоро...", callback_data="game_soon")
        builder.button(text="🏠 Главное меню", callback_data="menu_main")
    else:
        builder.button(text="✨ Spark Catcher", callback_data="game_sparks")
        builder.button(text="🎯 Coming Soon...", callback_data="game_soon")
        builder.button(text="🏠 Main Menu", callback_data="menu_main")
    
    builder.adjust(1)
    return builder.as_markup()


def get_revive_keyboard(streak_id: int, lang: str = 'en') -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    if lang == 'ru':
        builder.button(text="✨ Воскресить", callback_data=f"revive_confirm_{streak_id}")
        builder.button(text="❌ Отмена", callback_data="menu_streaks")
    else:
        builder.button(text="✨ Revive", callback_data=f"revive_confirm_{streak_id}")
        builder.button(text="❌ Cancel", callback_data="menu_streaks")
    
    builder.adjust(2)
    return builder.as_markup()


def get_pagination_keyboard(
    items: List[Dict[str, Any]], 
    page: int, 
    callback_prefix: str,
    items_per_page: int = 5
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    total_pages = (len(items) + items_per_page - 1) // items_per_page
    
    if page > 1:
        builder.button(text="◀️", callback_data=f"{callback_prefix}_page_{page - 1}")
    
    builder.button(text=f"{page}/{total_pages}", callback_data="noop")
    
    if page < total_pages:
        builder.button(text="▶️", callback_data=f"{callback_prefix}_page_{page + 1}")
    
    return builder.as_markup()
