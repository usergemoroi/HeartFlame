# 📚 API Documentation - Internal Structure

Документация внутренней структуры для разработчиков.

## 🗄️ Database API

### Database Class

```python
from database import Database

db = Database()
```

#### User Methods

```python
# Создать пользователя
await db.create_user(
    user_id=123456789,
    username="john_doe",
    avatar="🐱",
    language=Language.RU,
    referrer_id=987654321  # опционально
)

# Получить пользователя
user = await db.get_user(123456789)
# Returns: Dict[str, Any] или None

# Получить по username
user = await db.get_user_by_username("john_doe")

# Обновить пользователя
await db.update_user(
    123456789,
    sparks=500,
    stars=10,
    level=5
)

# Добавить искры
await db.add_sparks(user_id=123456789, amount=100)

# Обновить энергию (auto regen)
new_energy = await db.update_energy(user_id=123456789)
```

#### Streak Methods

```python
# Создать запрос на стрик
request_id = await db.create_streak_request(
    from_user_id=123,
    to_user_id=456
)

# Получить pending запрос
request = await db.get_pending_request(123, 456)

# Обновить статус запроса
await db.update_request_status(request_id, 'accepted')

# Создать стрик
streak_id = await db.create_streak(user1_id=123, user2_id=456)

# Получить стрик между пользователями
streak = await db.get_streak(123, 456)

# Получить все стрики пользователя
streaks = await db.get_user_streaks(user_id=123)

# Продлить стрик
success, new_days = await db.extend_streak(streak_id=1, user_id=123)

# Деактивировать стрик
await db.expire_streak(streak_id=1)
```

#### Pet Methods

```python
# Создать питомца
pet_id = await db.create_pet(
    user_id=123,
    name="Пушистик",
    emoji="🐣",
    rarity=PetRarity.COMMON,
    streak_id=1  # опционально
)

# Получить питомцев пользователя
pets = await db.get_user_pets(user_id=123)

# Получить конкретного питомца
pet = await db.get_pet(pet_id=1)

# Обновить питомца
await db.update_pet(
    pet_id=1,
    exp=150,
    level=3,
    mood=PetMood.HAPPY.value
)
```

#### Achievement Methods

```python
# Добавить достижение
achievement_id = await db.add_achievement(
    user_id=123,
    type_=AchievementType.STREAK,
    name="Серия 30 дней",
    description="Поддержал огонёк 30 дней!",
    emoji="🌸"
)

# Получить достижения
achievements = await db.get_user_achievements(user_id=123)
```

#### Quest Methods

```python
# Создать квест
quest_id = await db.create_quest(
    user_id=123,
    type_=QuestType.DAILY,
    name="Продли 3 огонька",
    description="Поддержи 3 дружбы сегодня",
    target=3,
    reward_sparks=50,
    reward_stars=0,
    expires_at=datetime.now() + timedelta(days=1)
)

# Получить квесты
active_quests = await db.get_user_quests(user_id=123, completed=False)
completed_quests = await db.get_user_quests(user_id=123, completed=True)

# Обновить прогресс
is_completed = await db.update_quest_progress(quest_id=1, progress=2)
```

#### Inventory & Gifts Methods

```python
# Добавить в инвентарь
await db.add_inventory_item(
    user_id=123,
    item_type="shield",
    item_id="basic",
    quantity=1
)

# Получить инвентарь
inventory = await db.get_inventory(user_id=123)

# Удалить из инвентаря
success = await db.remove_inventory_item(
    user_id=123,
    item_type="shield",
    item_id="basic",
    quantity=1
)

# Отправить подарок
gift_id = await db.send_gift(
    from_user_id=123,
    to_user_id=456,
    gift_type="cake",
    message="С днём рождения!"
)

# Получить подарки
unopened_gifts = await db.get_user_gifts(user_id=123, opened=False)

# Открыть подарок
await db.open_gift(gift_id=1)
```

#### Leaderboard & Referrals

```python
# Получить топ игроков
leaders = await db.get_leaderboard(
    order_by="best_streak",  # или "total_referrals", "sparks", "level"
    limit=100
)

# Количество рефералов
count = await db.get_referral_count(user_id=123)

# Добавить запись о награде за реферала
await db.add_referral_reward(
    user_id=123,
    level=1,
    referral_count=5,
    reward_type="sparks",
    reward_value=350
)

# Получить историю наград
rewards = await db.get_referral_rewards(user_id=123)
```

## 🎮 Game Logic API

### Pet Utils

```python
from utils.pet_utils import (
    calculate_pet_exp_for_level,
    get_pet_state_emoji,
    get_mood_emoji,
    check_pet_evolution
)

# Рассчитать нужный опыт для уровня
exp_needed = calculate_pet_exp_for_level(level=5)
# Returns: 1118

# Получить эмодзи состояния
emoji = get_pet_state_emoji(PetState.BABY)
# Returns: "🐣"

# Проверить эволюцию
new_state = check_pet_evolution(level=10, current_state=PetState.BABY)
# Returns: PetState.TEEN
```

### Time Utils

```python
from utils.time_utils import format_time_left, format_duration
from datetime import datetime, timedelta

expiry = datetime.now() + timedelta(hours=2, minutes=30)
time_str = format_time_left(expiry)
# Returns: "2ч 30м"

duration_str = format_duration(3665)
# Returns: "1ч 1м"
```

### Text Utils

```python
from utils.text_utils import escape_markdown, generate_referral_link

# Экранировать Markdown V2
safe_text = escape_markdown("Привет! [Это ссылка]")
# Returns: "Привет\\! \\[Это ссылка\\]"

# Генерировать реферальную ссылку
link = generate_referral_link("bot_username", user_id=123)
# Returns: "https://t.me/bot_username?start=ref_123"
```

## 🌍 Localization API

```python
from locales import get_text, set_user_language
from config.constants import Language

# Установить язык пользователя
set_user_language(user_id=123, language=Language.EN)

# Получить переведённый текст
text = get_text("welcome_1", user_id=123)

# С параметрами
text = get_text(
    "profile",
    user_id=123,
    username="John",
    sparks=500,
    stars=10
)
```

## ⌨️ Keyboards API

```python
from keyboards.inline import (
    get_menu_keyboard,
    get_streaks_keyboard,
    get_pet_keyboard,
    get_shop_keyboard,
    get_pagination_keyboard
)

# Главное меню
keyboard = get_menu_keyboard(user_id=123)

# Меню огоньков
keyboard = get_streaks_keyboard(has_streaks=True)

# Меню питомца
keyboard = get_pet_keyboard(pet_id=1)

# Пагинация
keyboard = get_pagination_keyboard(
    current_page=0,
    total_pages=5,
    callback_prefix="top_page",
    back_callback="menu_main"
)
```

## 🎯 Constants

### Игровые константы

```python
from config.constants import (
    STREAK_COLORS,
    STREAK_MILESTONES,
    REFERRAL_REWARDS,
    SHOP_ITEMS,
    BASE_PETS,
    PET_EVOLUTION_THRESHOLDS
)

# Цвета стриков
color = STREAK_COLORS[30]  # "🌸"

# Милестоуны
milestones = STREAK_MILESTONES  # [7, 14, 30, 50, 100, ...]

# Награды за рефералов
reward = REFERRAL_REWARDS[5]  # 350 искр

# Предметы магазина
shield = SHOP_ITEMS["shield"]
# {
#     "name": "🛡️ Огненный Щит",
#     "price": 200,
#     "currency": "sparks",
#     "description": "..."
# }

# Базовые питомцы по редкости
common_pets = BASE_PETS["common"]  # ["🐣", "🐥", ...]

# Пороги эволюции
threshold = PET_EVOLUTION_THRESHOLDS[PetState.TEEN]  # 10 дней
```

### Энумы

```python
from config.constants import (
    Language,
    PetRarity,
    PetState,
    PetMood,
    QuestType,
    AchievementType
)

# Использование
language = Language.RU
rarity = PetRarity.LEGENDARY
state = PetState.ADULT
mood = PetMood.HAPPY
quest_type = QuestType.DAILY
achievement = AchievementType.STREAK
```

## 🔌 Extending the Bot

### Добавить новый handler

1. Создай файл в `handlers/`:

```python
# handlers/my_feature.py
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

router = Router()

@router.callback_query(F.data == "my_feature")
async def my_feature_handler(callback: CallbackQuery):
    await callback.message.answer("Моя новая фича!")
    await callback.answer()
```

2. Зарегистрируй в `handlers/__init__.py`:

```python
from . import my_feature

def get_handlers_router() -> Router:
    router = Router()
    # ...
    router.include_router(my_feature.router)
    return router
```

### Добавить новую таблицу БД

1. Обнови `database/init_db.py`:

```python
await db.execute("""
    CREATE TABLE IF NOT EXISTS my_table (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        data TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
""")
```

2. Добавь методы в `database/queries.py`:

```python
async def get_my_data(self, user_id: int) -> List[Dict]:
    async with await self.get_connection() as db:
        cursor = await db.execute(
            "SELECT * FROM my_table WHERE user_id = ?",
            (user_id,)
        )
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]
```

### Добавить middleware

```python
# middlewares/my_middleware.py
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

class MyMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        # Твоя логика здесь
        return await handler(event, data)
```

Зарегистрируй в `main.py`:

```python
from middlewares.my_middleware import MyMiddleware

dp.message.middleware(MyMiddleware())
```

## 📊 Monitoring & Logging

```python
import structlog

logger = structlog.get_logger()

# Логирование событий
logger.info("event_name", user_id=123, extra_data="value")
logger.warning("warning_event", reason="something wrong")
logger.error("error_occurred", error=str(e), user_id=123)

# Structured data автоматически форматируется
```

---

Для более детальной информации смотри исходный код модулей! 📖
