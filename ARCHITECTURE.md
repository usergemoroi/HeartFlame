# 🏗️ Architecture Overview

Архитектура проекта "Огоньки Дружбы 2.0"

---

## 📊 Общая структура

```
┌─────────────────────────────────────────────────┐
│              Telegram Bot API                   │
└────────────────┬────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────┐
│              aiogram 3.x                        │
│  ┌──────────────────────────────────────────┐  │
│  │        Dispatcher & Routers              │  │
│  └──────────────────────────────────────────┘  │
└────────────────┬────────────────────────────────┘
                 │
    ┌────────────┼────────────┐
    │            │            │
┌───▼──┐    ┌───▼──┐    ┌───▼──┐
│Middle│    │ FSM  │    │Hand- │
│wares │    │      │    │lers  │
└───┬──┘    └──────┘    └───┬──┘
    │                       │
    └───────────┬───────────┘
                │
        ┌───────▼────────┐
        │   Business     │
        │     Logic      │
        │   (CRUD)       │
        └───────┬────────┘
                │
        ┌───────▼────────┐
        │   Database     │
        │   (SQLite)     │
        └────────────────┘
```

---

## 🎯 Компоненты

### 1. Entry Point (main.py)

**Ответственность:**
- Инициализация бота и диспетчера
- Регистрация middleware
- Подключение роутеров
- Запуск фоновых задач
- Lifecycle management (startup/shutdown)

**Основные функции:**
```python
async def main()                # Точка входа
async def on_startup(bot)       # Инициализация при запуске
async def on_shutdown()         # Очистка при остановке
```

---

### 2. Configuration (config.py)

**Ответственность:**
- Загрузка настроек из .env
- Константы (языки, награды, типы питомцев)
- Настройки по умолчанию

**Основные компоненты:**
```python
Settings                # Pydantic настройки из .env
LANGUAGES              # Поддерживаемые языки
STARTER_AVATARS        # Стартовые аватары
PET_TYPES              # Типы и редкость питомцев
GIFT_ITEMS             # Подарки и их эффекты
STREAK_COLORS          # Цвета огоньков по дням
REFERRAL_REWARDS       # Награды за рефералов
STREAK_MILESTONES      # Важные дни серий
```

---

### 3. Handlers (handlers/)

**Архитектура:** Router-based (aiogram 3.x)

Каждый handler отвечает за свою функциональную область:

#### start.py — Онбординг
```python
cmd_start()                  # /start команда
process_language()           # Выбор языка
process_nickname()           # Ввод никнейма
process_avatar()             # Выбор аватара
tutorial_step_X()            # Шаги туториала
tutorial_complete()          # Завершение обучения
```

#### streaks.py — Огоньки дружбы
```python
show_streaks()               # Список огоньков
new_streak()                 # Начать новый
process_friend_search()      # Поиск друга
accept_flame()               # Принять запрос
extend_streak_action()       # Продлить серию
revive_streak_action()       # Воскресить огонёк
```

#### pets.py — Питомцы
```python
show_pets()                  # Список питомцев
feed_pet_action()            # Покормить
pet_pet_action()             # Погладить
pet_play_action()            # Поиграть
```

#### profile.py — Профиль
```python
show_profile()               # Показать профиль пользователя
```

#### shop.py — Магазин
```python
show_shop()                  # Каталог товаров
buy_shield()                 # Купить щит
buy_boost()                  # Купить буст
```

#### referrals.py — Рефералы
```python
show_referrals()             # Статистика рефералов
```

#### leaderboard.py — Лидерборд
```python
show_leaderboard()           # Показать топ
show_leaderboard_stat()      # Конкретная категория
```

#### quests.py — Квесты
```python
show_quests()                # Список квестов
generate_daily_quests()      # Генерация ежедневных
generate_weekly_quests()     # Генерация недельных
```

#### gifts.py — Подарки
```python
show_gifts_menu()            # Меню подарков
choose_gift_for_friend()     # Выбор подарка
send_gift_action()           # Отправка
```

#### games.py — Мини-игры
```python
show_games()                 # Список игр
start_spark_catcher()        # Игра "Ловец искр"
```

#### friends.py — Друзья
```python
show_friends()               # Список друзей
```

---

### 4. Database Layer (database/)

**Архитектура:** Асинхронный SQLite через aiosqlite

#### init_db.py
```python
init_database()              # Создание схемы БД
get_db()                     # Фабрика подключений
```

**Схема базы данных:**

```sql
users
├── user_id (PK)
├── username
├── nickname (UNIQUE)
├── avatar
├── language
├── sparks, stars, energy
├── referrer_id (FK)
├── total_referrals
├── max_streak
└── created_at, last_action

streaks
├── streak_id (PK)
├── user1_id, user2_id (FK)
├── days
├── status (active/dead)
├── lives_left
├── last_update, streak_expiry
└── pet_id (FK)

pets
├── pet_id (PK)
├── owner_id (FK)
├── streak_id (FK)
├── pet_emoji, pet_name
├── level, xp
├── rarity, mood
└── items (JSON)

flame_requests
├── request_id (PK)
├── from_user_id, to_user_id (FK)
├── status
└── created_at

gifts, quests, shop_items, achievements, notifications
```

#### crud.py

**CRUD операции:**
```python
# Users
create_user()
get_user()
get_user_by_username()
update_user()
update_user_sparks()

# Streaks
create_flame_request()
accept_flame_request()
get_user_streaks()
extend_streak()
kill_streak()
revive_streak()

# Pets
create_pet()
get_pet()
feed_pet()
update_pet()

# Quests
create_quest()
get_user_quests()
update_quest_progress()

# Leaderboard
get_leaderboard()
get_user_rank()

# Referrals
process_referral()

# Gifts
send_gift()
get_user_gifts()
```

---

### 5. Keyboards (keyboards/)

**Ответственность:** Генерация inline-клавиатур

#### inline.py
```python
get_language_keyboard()      # Выбор языка
get_avatar_keyboard()        # Выбор аватара
get_main_menu_keyboard()     # Главное меню
get_streaks_keyboard()       # Действия с огоньками
get_pet_actions_keyboard()   # Действия с питомцем
get_shop_keyboard()          # Магазин
get_gifts_keyboard()         # Подарки
get_leaderboard_keyboard()   # Лидерборд
get_games_keyboard()         # Игры
```

**Паттерн callback_data:**
```
menu_<action>              # Навигация по меню
streak_<action>_<id>       # Действия с огоньками
pet_<action>_<id>          # Действия с питомцами
shop_buy_<item>            # Покупки
gift_send_<friend>_<type>  # Подарки
```

---

### 6. Middlewares (middlewares/)

**Выполняются ДО обработчиков**

#### user_check.py
```python
UserCheckMiddleware
├── Проверяет регистрацию пользователя
├── Загружает данные пользователя в context
└── Обновляет last_action
```

#### throttling.py
```python
ThrottlingMiddleware
├── Защита от флуда
├── Rate limiting (0.5s для message, 0.3s для callback)
└── Хранит timestamps в памяти
```

**Порядок выполнения:**
```
Message → ThrottlingMiddleware → UserCheckMiddleware → Handler
```

---

### 7. FSM States (states/)

**Finite State Machine для сложных флоу**

#### fsm.py
```python
OnboardingStates           # Регистрация
├── choosing_language
├── entering_nickname
├── choosing_avatar
└── tutorial_step_1/2/3

FlameStates               # Огоньки
├── searching_friend
└── confirming_request

PetStates                 # Питомцы
├── viewing_pet
├── feeding_pet
└── customizing_pet

ShopStates                # Магазин
├── browsing
└── confirming_purchase

GiftStates                # Подарки
├── choosing_friend
├── choosing_gift
└── confirming_gift

MiniGameStates            # Игры
├── spark_catcher
└── playing
```

---

### 8. Utils (utils/)

**Вспомогательные функции**

#### text.py
```python
TEXTS                      # Мультиязычные тексты
get_text()                 # Получить текст по ключу
get_streak_color()         # Определить цвет огонька
format_time_left()         # Форматировать время
escape_markdown()          # Экранирование для MarkdownV2
```

#### time.py
```python
get_current_timestamp()    # Текущее время (UNIX)
get_streak_expiry()        # Время истечения серии
get_time_until_expiry()    # Осталось времени
can_extend_streak()        # Проверка кулдауна
get_revival_cost()         # Стоимость воскрешения
```

---

### 9. Background Tasks (tasks.py)

**Фоновые периодические задачи**

```python
check_dying_streaks()      # Каждые 10 мин
├── Проверяет истекающие серии
├── Отправляет напоминания (4ч, 1ч, 30мин)
└── Убивает просроченные серии

restore_energy()           # Каждые 30 мин
└── Восстанавливает 1 энергию пользователям

reset_daily_quests()       # Раз в день
└── Очищает старые квесты

start_background_tasks()   # Запуск всех задач
```

---

## 🔄 Типичный флоу запроса

### Пример: Продление огонька

```
1. User нажимает "🔥 Продлить"
   │
2. ThrottlingMiddleware
   ├── Проверяет rate limit
   └── Пропускает дальше
   │
3. UserCheckMiddleware
   ├── Загружает user_data из БД
   └── Добавляет в context
   │
4. Handler: extend_streak_action()
   ├── Проверяет кулдаун (8 часов)
   ├── CRUD: extend_streak(streak_id)
   │   ├── UPDATE streaks SET days = days + 1
   │   ├── UPDATE users SET max_streak
   │   └── COMMIT
   ├── Рассчитывает награду (20-40🔥)
   ├── CRUD: update_user_sparks()
   ├── Проверяет милестоны (7, 14, 30...)
   │   └── Если 3 дня → create_pet()
   ├── Отправляет уведомление другу
   └── Редактирует сообщение с результатом
```

---

## 🔒 Безопасность

### Анти-чит механизмы

1. **Кулдауны**
   - Продление серии: 8-12 часов
   - Мини-игры: зависит от энергии
   - Запросы на огоньки: нет лимита, но дубликаты блокируются

2. **Валидация**
   - Проверка существования пользователей
   - Уникальность nickname
   - Проверка балансов перед покупками

3. **Rate Limiting**
   - Middleware уровень: 0.3-0.5s между действиями
   - Защита от флуда

4. **Проверка времени**
   - Серверное время для всех операций
   - Защита от манипуляций с временем клиента

---

## 📈 Масштабирование

### Текущая архитектура (до 10k пользователей)

```
Single Server
├── Python Process (main.py)
├── SQLite Database
└── Polling Mode
```

### Средний масштаб (10k-100k пользователей)

```
Server
├── Python Process
├── PostgreSQL Database
├── Redis (кэш + rate limiting)
└── Webhook Mode
```

### Крупный масштаб (100k+ пользователей)

```
Load Balancer
├── Bot Instance 1 ──┐
├── Bot Instance 2 ──┼─→ PostgreSQL Cluster
└── Bot Instance N ──┘       (Primary + Replicas)
        │
        ├─→ Redis Cluster (кэш, sessions, queues)
        │
        └─→ Celery Workers (фоновые задачи)
```

**Необходимые изменения:**
1. Замена SQLite на PostgreSQL
2. Добавление Redis для кэша и distributed locks
3. Webhook mode вместо polling
4. Вынос фоновых задач в Celery
5. CDN для статических ресурсов (изображения питомцев)

---

## 🧪 Тестирование

### Unit Tests (пример)

```python
import pytest
from database.crud import create_user, get_user

@pytest.mark.asyncio
async def test_create_user():
    success = await create_user(
        user_id=123456,
        username="testuser",
        nickname="test",
        avatar="🐱",
        language="en"
    )
    assert success == True
    
    user = await get_user(123456)
    assert user['nickname'] == 'test'
```

### Integration Tests

```python
@pytest.mark.asyncio
async def test_streak_flow():
    # Создать двух пользователей
    await create_user(1, None, "user1", "🐱", "en")
    await create_user(2, None, "user2", "🐶", "en")
    
    # Создать запрос на огонёк
    await create_flame_request(1, 2)
    
    # Принять запрос
    await accept_flame_request(1, 2)
    
    # Проверить, что серия создана
    streaks = await get_user_streaks(1)
    assert len(streaks) == 1
    assert streaks[0]['days'] == 1
```

---

## 📚 Полезные ссылки

- **aiogram docs**: https://docs.aiogram.dev/
- **SQLite docs**: https://www.sqlite.org/docs.html
- **Telegram Bot API**: https://core.telegram.org/bots/api

---

Эта архитектура обеспечивает:
✅ Модульность
✅ Масштабируемость
✅ Читаемость
✅ Тестируемость
✅ Безопасность
