import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )
    
    BOT_TOKEN: str
    ADMIN_IDS: str = ""
    DATABASE_PATH: str = "./friendship_flames.db"
    DEBUG: bool = False
    
    @property
    def admin_ids_list(self) -> List[int]:
        if not self.ADMIN_IDS:
            return []
        return [int(x.strip()) for x in self.ADMIN_IDS.split(',') if x.strip()]


settings = Settings()

LANGUAGES = {
    'ru': '🇷🇺 Русский',
    'en': '🇺🇸 English',
    'es': '🇪🇸 Español',
    'fr': '🇫🇷 Français',
    'de': '🇩🇪 Deutsch',
}

STARTER_AVATARS = [
    "🐱", "🐶", "🦊", "🐻", "🐼",
    "🐨", "🐯", "🦁", "🐮", "🐷",
    "🐸", "🦄"
]

PET_TYPES = {
    'common': ['🐣', '🐥', '🐤', '🐦', '🦆', '🕊️', '🦜', '🦩'],
    'rare': ['🦋', '🐛', '🐝', '🦗', '🐞'],
    'epic': ['🦚', '🦅', '🦉', '🦇'],
    'legendary': ['🐉', '🦖', '🦕', '🔥'],
    'mythic': ['✨', '🌟', '💫', '⭐']
}

PET_ITEMS = [
    "🎩", "👑", "🎓", "🧢", "👒",
    "🕶️", "👓", "🥽", "🎭", "💍",
    "⚡", "❄️", "🔥", "💧", "🌈",
    "🦋", "🌸", "🌺", "🍀", "🌟",
    "💎", "👾", "🎪", "🎨", "🎭",
    "🎀", "🎗️", "🏆", "🎯", "🎲",
    "🔮", "💝", "💖", "💗", "💓",
    "🌀", "💫", "✨", "⭐", "🌙",
    "☀️", "🌤️", "⛅", "🌈", "🌠",
    "🎊", "🎉", "🎁", "🎈", "🎆"
]

GIFT_ITEMS = {
    'cake': {'emoji': '🎂', 'name': 'Birthday Cake', 'sparks': 50, 'description': '+50 sparks gift'},
    'bouquet': {'emoji': '💐', 'name': 'Flower Bouquet', 'sparks': 40, 'description': '+40 sparks gift'},
    'rocket': {'emoji': '🚀', 'name': 'Rocket Boost', 'sparks': 100, 'description': 'x2 sparks for 24h'},
    'crown': {'emoji': '👑', 'name': 'Royal Crown', 'sparks': 150, 'description': 'VIP badge for 7 days'},
    'double_day': {'emoji': '⏰', 'name': 'Double Day', 'sparks': 80, 'description': 'Counts as 2 days'},
    'extra_life': {'emoji': '❤️', 'name': 'Extra Life', 'sparks': 120, 'description': '+1 life to pet'},
    'eternal_flame': {'emoji': '🔥', 'name': 'Eternal Flame', 'sparks': 300, 'description': '30 days protection'},
}

STREAK_COLORS = [
    (1, 2, '🟥', 'Red Ember'),
    (3, 6, '🟧', 'Orange Glow'),
    (7, 14, '🟨', 'Yellow Flame'),
    (15, 29, '💜', 'Purple Blaze'),
    (30, 59, '🌸', 'Pink Blossom'),
    (60, 99, '🌟', 'Starlight'),
    (100, 364, '🌈', 'Rainbow Fire'),
    (365, 10000, '✨🔥', 'Eternal Radiance'),
]

REFERRAL_REWARDS = [
    (1, 50), (2, 80), (3, 120), (4, 200),
    (5, 350), (10, 600), (15, 1000), (25, 2000),
    (50, 5000), (100, 15000)
]

STREAK_MILESTONES = [
    7, 14, 30, 50, 100, 200, 365, 500, 1000, 2000
]
