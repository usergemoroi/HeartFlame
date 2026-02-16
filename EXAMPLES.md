# 📚 Examples & Extensions

Примеры расширения функционала бота.

---

## 🎨 Пример 1: Добавление нового языка (Испанский)

### Шаг 1: Обновите `config.py`

```python
LANGUAGES = {
    'ru': '🇷🇺 Русский',
    'en': '🇺🇸 English',
    'es': '🇪🇸 Español',  # ← Новый язык
    'fr': '🇫🇷 Français',
    'de': '🇩🇪 Deutsch',
}
```

### Шаг 2: Добавьте тексты в `utils/text.py`

```python
TEXTS = {
    'en': { ... },
    'ru': { ... },
    'es': {
        'welcome_1': "✨ Bienvenido a *Friendship Flames 2\\.0* ✨",
        'welcome_2': "Donde las amistades nunca se desvanecen\\.\\.\\. ¡si las mantienes vivas\\! 🔥",
        'welcome_3': "¡Cada día con amigos es una chispa\\. No dejes que se apague\\! 💫",
        'choose_language': "🌍 Elige tu idioma:",
        'enter_nickname': "👤 Ingresa tu apodo \\(3\\-20 caracteres\\):",
        'nickname_taken': "😔 Este apodo ya está en uso\\. ¡Intenta otro\\!",
        'nickname_invalid': "❌ El apodo debe tener 3\\-20 caracteres, solo letras, números y guiones bajos\\.",
        # ... добавьте все остальные ключи
    }
}
```

### Шаг 3: Перезапустите бота

```bash
python main.py
```

Теперь при `/start` пользователи смогут выбрать испанский язык!

---

## 💎 Пример 2: Добавление Telegram Stars покупок

### Шаг 1: Создайте handler в `handlers/shop.py`

```python
from aiogram.types import LabeledPrice, PreCheckoutQuery, Message

@router.callback_query(F.data == "shop_stars_100")
async def buy_stars_100(callback: CallbackQuery):
    """Покупка пакета 100 звёзд"""
    prices = [LabeledPrice(label="100 ⭐ Stars", amount=100)]
    
    await callback.message.answer_invoice(
        title="Stars Package: 100 ⭐",
        description="Get 100 stars for premium features, revivals, and exclusive pets!",
        payload="stars_100",
        provider_token="",  # Пусто для Telegram Stars
        currency="XTR",
        prices=prices,
        photo_url="https://your-cdn.com/stars_package.jpg",
        photo_width=512,
        photo_height=512
    )
    await callback.answer()


@router.callback_query(F.data == "shop_stars_500")
async def buy_stars_500(callback: CallbackQuery):
    """Покупка пакета 500 звёзд (20% bonus)"""
    prices = [LabeledPrice(label="500 ⭐ Stars (+100 bonus)", amount=500)]
    
    await callback.message.answer_invoice(
        title="Stars Package: 600 ⭐",
        description="Get 500 stars + 100 BONUS stars! Best value!",
        payload="stars_500",
        provider_token="",
        currency="XTR",
        prices=prices,
        photo_url="https://your-cdn.com/stars_package_big.jpg",
        photo_width=512,
        photo_height=512
    )
    await callback.answer()


@router.pre_checkout_query()
async def process_pre_checkout(pre_checkout_query: PreCheckoutQuery):
    """Подтверждение перед оплатой"""
    await pre_checkout_query.answer(ok=True)


@router.message(F.successful_payment)
async def process_successful_payment(message: Message, user_data: dict):
    """Обработка успешной оплаты"""
    payload = message.successful_payment.invoice_payload
    
    stars_to_add = 0
    if payload == "stars_100":
        stars_to_add = 100
    elif payload == "stars_500":
        stars_to_add = 600  # 500 + 100 бонус
    
    from database.crud import update_user
    await update_user(
        message.from_user.id, 
        stars=user_data['stars'] + stars_to_add
    )
    
    lang = user_data['language']
    
    await message.answer(
        f"✅ *Payment Successful\\!*\n\n\\+{stars_to_add} ⭐ stars added to your account\\!\n\nThank you for your support\\! 🙏" if lang == 'en' 
        else f"✅ *Платёж успешен\\!*\n\n\\+{stars_to_add} ⭐ звёзд добавлено на счёт\\!\n\nСпасибо за поддержку\\! 🙏",
        parse_mode='MarkdownV2'
    )
```

### Шаг 2: Обновите клавиатуру магазина в `keyboards/inline.py`

```python
def get_shop_keyboard(lang: str = 'en') -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    if lang == 'ru':
        items = [
            ("💎 100 ⭐ Звёзд (100 XTR)", "shop_stars_100"),
            ("💎 600 ⭐ Звёзд (500 XTR)", "shop_stars_500"),
            ("🛡️ Щит огонька (100🔥)", "shop_buy_shield"),
            # ...
        ]
    else:
        items = [
            ("💎 100 ⭐ Stars (100 XTR)", "shop_stars_100"),
            ("💎 600 ⭐ Stars (500 XTR)", "shop_stars_500"),
            ("🛡️ Flame Shield (100🔥)", "shop_buy_shield"),
            # ...
        ]
    
    # ...
```

---

## 🐉 Пример 3: Добавление нового типа питомца

### Шаг 1: Обновите `config.py`

```python
PET_TYPES = {
    'common': ['🐣', '🐥', '🐤', '🐦', '🦆', '🕊️', '🦜', '🦩'],
    'rare': ['🦋', '🐛', '🐝', '🦗', '🐞'],
    'epic': ['🦚', '🦅', '🦉', '🦇'],
    'legendary': ['🐉', '🦖', '🦕', '🔥'],
    'mythic': ['✨', '🌟', '💫', '⭐'],
    'cosmic': ['🌌', '☄️', '🪐', '🌠', '👽', '🛸'],  # ← Новая редкость
}
```

### Шаг 2: Обновите логику создания питомца в `database/crud.py`

```python
async def create_pet(streak_id: int, owner_id: int) -> Dict[str, Any]:
    db = await get_db()
    now = get_current_timestamp()
    
    # Новая логика с космическими питомцами (0.1% шанс)
    rarity_roll = random.random()
    if rarity_roll < 0.001:
        rarity = 'cosmic'  # ← 0.1% шанс
    elif rarity_roll < 0.01:
        rarity = 'mythic'
    elif rarity_roll < 0.05:
        rarity = 'legendary'
    # ... остальное без изменений
```

### Шаг 3: Добавьте специальные способности

В `handlers/pets.py`:

```python
@router.callback_query(F.data.startswith("pet_special_"))
async def use_special_ability(callback: CallbackQuery, user_data: dict):
    pet_id = int(callback.data.split("_")[2])
    pet = await get_pet(pet_id)
    
    if pet['rarity'] == 'cosmic':
        # Космические питомцы дают x3 искры за 1 час
        await callback.answer("Cosmic power activated! x3 sparks for 1 hour! 🌌", show_alert=True)
        # Логика активации буста...
    elif pet['rarity'] == 'mythic':
        # Мифические питомцы защищают от погасания огонька на 24ч
        await callback.answer("Mythic shield activated! Flame protected for 24h! ✨", show_alert=True)
    # ...
```

---

## 🎮 Пример 4: Создание новой мини-игры "Memory Match"

### Шаг 1: Создайте handler в `handlers/games.py`

```python
@router.callback_query(F.data == "game_memory")
async def start_memory_game(callback: CallbackQuery, user_data: dict, state: FSMContext):
    lang = user_data['language']
    
    if user_data['energy'] < 15:
        await callback.answer("Not enough energy! Need 15 ⚡", show_alert=True)
        return
    
    # Генерируем пары эмодзи
    emojis = ['🔥', '⭐', '🐣', '💎', '🎁', '👑']
    game_field = emojis * 2  # 12 карт (6 пар)
    random.shuffle(game_field)
    
    await state.update_data(
        game_field=game_field,
        opened_cards=[],
        matched_pairs=0,
        moves=0
    )
    
    # Показываем поле (все карты закрыты)
    keyboard = InlineKeyboardBuilder()
    for i in range(12):
        keyboard.button(text="❓", callback_data=f"memory_card_{i}")
    keyboard.adjust(4)
    
    await callback.message.edit_text(
        "🎮 *Memory Match\\!*\n\nFind all pairs\\!\nMoves: 0",
        reply_markup=keyboard.as_markup(),
        parse_mode='MarkdownV2'
    )
    
    await state.set_state(MiniGameStates.playing)
    await callback.answer()


@router.callback_query(F.data.startswith("memory_card_"))
async def memory_card_click(callback: CallbackQuery, state: FSMContext):
    card_index = int(callback.data.split("_")[2])
    data = await state.get_data()
    
    game_field = data['game_field']
    opened_cards = data['opened_cards']
    matched_pairs = data['matched_pairs']
    moves = data['moves']
    
    # Логика игры...
    # Если открыты 2 карты и они совпадают → matched_pairs += 1
    # Если все пары найдены → награда
    
    if matched_pairs == 6:
        reward = 50
        await update_user_sparks(callback.from_user.id, reward)
        await callback.message.edit_text(
            f"🎉 *You won\\!*\n\n\\+{reward} 🔥 sparks\\!\nMoves: {moves}",
            parse_mode='MarkdownV2'
        )
        await state.clear()
```

### Шаг 2: Добавьте кнопку в меню игр

В `keyboards/inline.py`:

```python
def get_games_keyboard(lang: str = 'en') -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    if lang == 'ru':
        builder.button(text="✨ Ловец искр", callback_data="game_sparks")
        builder.button(text="🧠 Мемори", callback_data="game_memory")  # ← Новая игра
        # ...
```

---

## 🏆 Пример 5: Добавление системы достижений

### Шаг 1: Создайте новый handler `handlers/achievements.py`

```python
from aiogram import Router, F
from aiogram.types import CallbackQuery
from database.crud import get_db
from utils.text import escape_markdown

router = Router()


ACHIEVEMENTS = {
    'first_flame': {
        'emoji': '🔥',
        'name_en': 'First Spark',
        'name_ru': 'Первая искра',
        'description_en': 'Light your first flame',
        'description_ru': 'Зажги первый огонёк',
        'reward_sparks': 50,
        'reward_stars': 1
    },
    'week_streak': {
        'emoji': '🌟',
        'name_en': 'Week Warrior',
        'name_ru': 'Недельный воин',
        'description_en': 'Maintain a 7-day streak',
        'description_ru': 'Держи серию 7 дней',
        'reward_sparks': 200,
        'reward_stars': 5
    },
    'month_streak': {
        'emoji': '🏆',
        'name_en': 'Monthly Master',
        'name_ru': 'Месячный мастер',
        'description_en': 'Maintain a 30-day streak',
        'description_ru': 'Держи серию 30 дней',
        'reward_sparks': 1000,
        'reward_stars': 25
    },
    'referral_king': {
        'emoji': '👑',
        'name_en': 'Referral King',
        'name_ru': 'Король рефералов',
        'description_en': 'Invite 50 friends',
        'description_ru': 'Пригласи 50 друзей',
        'reward_sparks': 5000,
        'reward_stars': 100
    }
}


async def check_and_grant_achievement(user_id: int, achievement_id: str):
    """Проверяет и выдает достижение"""
    db = await get_db()
    
    # Проверяем, есть ли уже это достижение
    cursor = await db.execute("""
        SELECT * FROM achievements 
        WHERE user_id = ? AND achievement_type = ?
    """, (user_id, achievement_id))
    
    existing = await cursor.fetchone()
    
    if existing:
        await db.close()
        return False
    
    # Выдаем достижение
    from utils.time import get_current_timestamp
    now = get_current_timestamp()
    
    achievement = ACHIEVEMENTS[achievement_id]
    
    await db.execute("""
        INSERT INTO achievements (user_id, achievement_type, achievement_name, unlocked_at)
        VALUES (?, ?, ?, ?)
    """, (user_id, achievement_id, achievement['name_en'], now))
    
    # Начисляем награду
    from database.crud import update_user_sparks
    await update_user_sparks(user_id, achievement['reward_sparks'])
    
    await db.commit()
    await db.close()
    
    return True


@router.callback_query(F.data == "menu_achievements")
async def show_achievements(callback: CallbackQuery, user_data: dict):
    lang = user_data['language']
    
    db = await get_db()
    cursor = await db.execute("""
        SELECT achievement_type FROM achievements WHERE user_id = ?
    """, (user_data['user_id'],))
    
    unlocked = [row[0] for row in await cursor.fetchall()]
    await db.close()
    
    text = "🏆 *Achievements*\n\n" if lang == 'en' else "🏆 *Достижения*\n\n"
    
    for ach_id, ach_data in ACHIEVEMENTS.items():
        status = "✅" if ach_id in unlocked else "🔒"
        name = ach_data[f'name_{lang}'] if f'name_{lang}' in ach_data else ach_data['name_en']
        desc = ach_data[f'description_{lang}'] if f'description_{lang}' in ach_data else ach_data['description_en']
        
        text += f"{status} {ach_data['emoji']} *{escape_markdown(name)}*\n"
        text += f"   {escape_markdown(desc)}\n"
        text += f"   Reward: {ach_data['reward_sparks']}🔥 {ach_data['reward_stars']}⭐\n\n"
    
    from keyboards.inline import get_back_to_menu_keyboard
    
    await callback.message.edit_text(
        text,
        reply_markup=get_back_to_menu_keyboard(lang),
        parse_mode='MarkdownV2'
    )
    
    await callback.answer()
```

### Шаг 2: Интегрируйте проверку достижений

В `handlers/streaks.py` после создания первого огонька:

```python
# После accept_flame_request()
from handlers.achievements import check_and_grant_achievement

granted = await check_and_grant_achievement(user_data['user_id'], 'first_flame')
if granted:
    await callback.message.answer("🎉 Achievement Unlocked: First Spark! +50🔥")
```

### Шаг 3: Добавьте в меню

В `keyboards/inline.py`:

```python
builder.button(text="🏆 Achievements" if lang == 'en' else "🏆 Достижения", 
               callback_data="menu_achievements")
```

В `main.py`:

```python
from handlers import achievements
dp.include_router(achievements.router)
```

---

## 📊 Пример 6: Аналитика и метрики

### Создайте `analytics.py`:

```python
from database.crud import get_db
from datetime import datetime, timedelta


async def get_daily_stats():
    """Ежедневная статистика"""
    db = await get_db()
    
    # DAU (Daily Active Users)
    yesterday = int((datetime.now() - timedelta(days=1)).timestamp())
    cursor = await db.execute("""
        SELECT COUNT(DISTINCT user_id) FROM users WHERE last_action > ?
    """, (yesterday,))
    dau = (await cursor.fetchone())[0]
    
    # Новые пользователи за сутки
    cursor = await db.execute("""
        SELECT COUNT(*) FROM users WHERE created_at > ?
    """, (yesterday,))
    new_users = (await cursor.fetchone())[0]
    
    # Активные огоньки
    cursor = await db.execute("""
        SELECT COUNT(*) FROM streaks WHERE status = 'active'
    """, ())
    active_streaks = (await cursor.fetchone())[0]
    
    # Погасших огоньков за сутки
    cursor = await db.execute("""
        SELECT COUNT(*) FROM streaks WHERE status = 'dead' AND died_at > ?
    """, (yesterday,))
    dead_streaks = (await cursor.fetchone())[0]
    
    await db.close()
    
    return {
        'dau': dau,
        'new_users': new_users,
        'active_streaks': active_streaks,
        'dead_streaks': dead_streaks,
        'retention_rate': (dau / max(1, new_users)) * 100 if new_users > 0 else 0
    }


async def send_daily_report(bot, admin_ids: list):
    """Отправка отчета админам"""
    stats = await get_daily_stats()
    
    report = f"""
📊 **Daily Report** {datetime.now().strftime('%Y-%m-%d')}

👥 DAU: {stats['dau']}
🆕 New Users: {stats['new_users']}
🔥 Active Streaks: {stats['active_streaks']}
💔 Dead Streaks: {stats['dead_streaks']}
📈 Retention: {stats['retention_rate']:.1f}%
"""
    
    for admin_id in admin_ids:
        try:
            await bot.send_message(admin_id, report, parse_mode='Markdown')
        except:
            pass
```

В `tasks.py` добавьте:

```python
async def daily_analytics_task(bot: Bot):
    """Ежедневная аналитика в 9:00"""
    while True:
        now = datetime.now()
        target = now.replace(hour=9, minute=0, second=0)
        
        if now > target:
            target += timedelta(days=1)
        
        sleep_seconds = (target - now).total_seconds()
        await asyncio.sleep(sleep_seconds)
        
        from analytics import send_daily_report
        from config import settings
        await send_daily_report(bot, settings.admin_ids_list)
```

---

## 🚀 Готовые интеграции

### Sentry (мониторинг ошибок):

```bash
pip install sentry-sdk
```

В `main.py`:

```python
import sentry_sdk

sentry_sdk.init(
    dsn="YOUR_SENTRY_DSN",
    traces_sample_rate=1.0
)
```

### Redis (кэширование):

```bash
pip install redis aioredis
```

Создайте `cache.py`:

```python
import aioredis
from config import settings

redis = None

async def init_redis():
    global redis
    redis = await aioredis.create_redis_pool('redis://localhost')

async def get_cached_user(user_id: int):
    if redis:
        data = await redis.get(f'user:{user_id}')
        if data:
            return json.loads(data)
    return None

async def cache_user(user_id: int, user_data: dict):
    if redis:
        await redis.setex(f'user:{user_id}', 300, json.dumps(user_data))
```

---

Это лишь малая часть возможностей! Экспериментируйте и создавайте уникальные фичи! 🚀
