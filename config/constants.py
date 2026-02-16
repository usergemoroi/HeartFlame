from enum import Enum
from typing import Dict, List


class Language(str, Enum):
    RU = "ru"
    EN = "en"
    ES = "es"
    ZH = "zh"


class PetRarity(str, Enum):
    COMMON = "common"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"
    MYTHIC = "mythic"


class PetState(str, Enum):
    EGG = "egg"
    BABY = "baby"
    TEEN = "teen"
    ADULT = "adult"
    ELDER = "elder"
    MYTHIC = "mythic"


class PetMood(str, Enum):
    HAPPY = "happy"
    NEUTRAL = "neutral"
    HUNGRY = "hungry"
    SAD = "sad"
    DEPRESSED = "depressed"


class QuestType(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    SEASONAL = "seasonal"
    REFERRAL = "referral"


class AchievementType(str, Enum):
    STREAK = "streak"
    REFERRAL = "referral"
    PET = "pet"
    SOCIAL = "social"
    COLLECTION = "collection"


STREAK_COLORS: Dict[int, str] = {
    1: "🟥",
    3: "🟧",
    7: "🟨",
    15: "💜",
    30: "🌸",
    60: "🌟",
    100: "🌈",
    365: "✨🔥",
}


STREAK_MILESTONES: List[int] = [
    7, 14, 30, 50, 100, 200, 365, 500, 1000, 2000
]


REFERRAL_REWARDS: Dict[int, int] = {
    1: 50,
    2: 80,
    3: 120,
    4: 200,
    5: 350,
    10: 600,
    25: 1200,
    50: 2500,
    100: 5000,
}


STARTER_AVATARS = [
    "🐱", "🐶", "🐼", "🦊", "🐨", "🐸",
    "🦄", "🐲", "🦋", "🌺", "⭐", "🌈"
]


BASE_PETS = {
    "common": ["🐣", "🐥", "🐤", "🐝", "🐛", "🦗", "🐌", "🪲"],
    "rare": ["🦜", "🦚", "🦢", "🦩", "🦆", "🐧"],
    "epic": ["🦅", "🦉", "🐉", "🦖", "🦕"],
    "legendary": ["🔥🦅", "⚡🦉", "🌟🐉", "🌈🦄"],
    "mythic": ["✨👑🔥", "💎🌌🦋", "🪐🌠🐲"]
}


PET_EVOLUTION_THRESHOLDS = {
    PetState.EGG: 0,
    PetState.BABY: 3,
    PetState.TEEN: 10,
    PetState.ADULT: 30,
    PetState.ELDER: 100,
    PetState.MYTHIC: 365,
}


SHOP_ITEMS = {
    "shield": {"name": "🛡️ Огненный Щит", "price": 200, "currency": "sparks", "description": "Защита от гашения на 7 дней"},
    "eternal_shield": {"name": "🛡️✨ Вечный Щит", "price": 1500, "currency": "sparks", "description": "Защита на 30 дней"},
    "revive": {"name": "💫 Воскрешение", "price": 120, "currency": "stars", "description": "Восстанови погасший огонёк (до 72ч)"},
    "boost_2x": {"name": "⚡ Буст ×2", "price": 300, "currency": "sparks", "description": "Двойные искры на 24 часа"},
    "pet_life": {"name": "❤️ Жизнь питомца", "price": 500, "currency": "sparks", "description": "+1 жизнь серийчику"},
    "energy": {"name": "⚡ Энергия", "price": 50, "currency": "sparks", "description": "+50 энергии для игр"},
    "rare_egg": {"name": "🥚✨ Редкое яйцо", "price": 800, "currency": "sparks", "description": "Гарантированный редкий питомец"},
    "epic_egg": {"name": "🥚🌟 Эпическое яйцо", "price": 250, "currency": "stars", "description": "Гарантированный эпический питомец"},
}


GIFTS = {
    "cake": {"emoji": "🎂", "name": "Тортик", "price": 100, "effect": "+50 искр другу"},
    "bouquet": {"emoji": "💐", "name": "Букет", "price": 150, "effect": "+настроение питомцу"},
    "rocket": {"emoji": "🚀", "name": "Ракета", "price": 200, "effect": "+100 опыта питомцу"},
    "crown": {"emoji": "👑", "name": "Корона", "price": 500, "effect": "VIP статус на 3 дня"},
    "double_day": {"emoji": "✨", "name": "Двойной День", "price": 300, "effect": "×2 прогресс стрика"},
    "eternal_flame": {"emoji": "🔥💎", "name": "Вечный Огонь", "price": 1000, "effect": "Защита огонька на 7 дней"},
}


CUSTOMIZATION_ITEMS = {
    "glasses": ["🕶️", "👓", "🥽", "🤓"],
    "hats": ["🎩", "👒", "🎓", "👑", "🧢", "⛑️", "🪖"],
    "wings": ["🦋", "🕊️", "🦅", "👼", "🧚"],
    "auras": ["✨", "💫", "⭐", "🌟", "💥", "🔥", "⚡", "🌈"],
    "backgrounds": ["🌅", "🌃", "🌌", "🌠", "🌈", "🔥", "💎", "🌸"],
}


DAILY_STREAK_BONUS_BASE = 10
EXTEND_SPARK_REWARD = 20
ONBOARDING_SPARKS = 150
ONBOARDING_SHIELDS = 1


REVIVE_PRICES = {
    "0-72h": 120,
    "72-168h": 350,
}


ENERGY_MAX = 100
ENERGY_REGEN_PER_MIN = 1
MINIGAME_ENERGY_COST = 20


LEADERBOARD_PAGE_SIZE = 10
FRIENDS_PAGE_SIZE = 8
