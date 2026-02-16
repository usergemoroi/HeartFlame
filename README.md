# 🔥 Огоньки Дружбы 2.0 - Friendship Flames Bot

**Production-ready Telegram бот с геймификацией, стриками, питомцами и вирусной реферальной системой**

## 🎯 Описание

"Огоньки Дружбы" - это эмоциональный микс Snapchat Streaks + Duolingo + Tamagotchi + мощная реферальная система.

### Ключевые механики:

- 🔥 **Система огоньков (Streaks)** - поддерживай дружбу каждый день
- 🐾 **Серийчики-питомцы** - растут вместе с твоими стриками
- 👥 **Гипервирусная реферальная система** - многоуровневые награды
- 🎁 **Подарки друзьям** - усиливайте огоньки вместе
- ⚔️ **Квесты и достижения** - ежедневные задания
- 🏆 **Глобальный лидерборд** - соревнуйся с лучшими
- 💎 **Двойная экономика** - искры (free) и звёзды (premium)
- 🌍 **Мультиязычность** - русский, английский, испанский, китайский

## 🛠 Технологический стек

- **Python 3.11+**
- **aiogram 3.10** - асинхронный фреймворк для Telegram Bot API
- **aiosqlite** - асинхронная работа с SQLite
- **pydantic v2** - валидация данных и настройки
- **structlog** - структурированное логирование
- **FSM** - конечные автоматы для сложных флоу

## 📁 Структура проекта

```
├── config/              # Конфигурация и константы
│   ├── settings.py      # Настройки из .env
│   └── constants.py     # Игровые константы, енумы
├── database/            # Работа с БД
│   ├── init_db.py       # Миграции и инициализация
│   └── queries.py       # CRUD операции
├── handlers/            # Обработчики команд
│   ├── start.py         # Онбординг
│   ├── profile.py       # Профиль пользователя
│   ├── streaks.py       # Огоньки
│   ├── pets.py          # Питомцы
│   ├── shop.py          # Магазин
│   ├── referrals.py     # Реферальная система
│   ├── quests.py        # Квесты
│   └── leaderboard.py   # Топы
├── keyboards/           # Клавиатуры
│   └── inline.py        # Inline кнопки
├── states/              # FSM состояния
│   └── fsm.py           # Определения состояний
├── middlewares/         # Middleware
│   ├── throttling.py    # Антифлуд
│   └── user_check.py    # Проверка пользователя
├── utils/               # Утилиты
│   ├── time_utils.py    # Форматирование времени
│   ├── text_utils.py    # Работа с текстом
│   └── pet_utils.py     # Логика питомцев
├── locales/             # Переводы
│   └── translations.py  # Мультиязычность
├── main.py              # Точка входа
├── requirements.txt     # Зависимости
└── README.md            # Документация
```

## 🚀 Установка и запуск

### 1. Клонирование и установка зависимостей

```bash
# Создай виртуальное окружение
python3.11 -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate

# Установи зависимости
pip install -r requirements.txt
```

### 2. Создание бота в Telegram

1. Найди [@BotFather](https://t.me/BotFather) в Telegram
2. Отправь `/newbot`
3. Следуй инструкциям и получи токен
4. **Важно**: включи inline mode командой `/setinline`

### 3. Настройка окружения

Создай файл `.env` в корне проекта:

```bash
cp .env.example .env
```

Отредактируй `.env`:

```env
BOT_TOKEN=1234567890:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
ADMIN_IDS=123456789,987654321
DATABASE_PATH=data/bot.db
LOG_LEVEL=INFO
RATE_LIMIT_REQUESTS=30
RATE_LIMIT_PERIOD=60
```

### 4. Запуск бота

```bash
python main.py
```

Бот автоматически создаст базу данных и все необходимые таблицы.

## 📱 Основные команды

- `/start` - Запуск бота и онбординг
- `/menu` - Главное меню
- `/profile` - Твой профиль
- `/streaks` - Твои огоньки
- `/pet` - Твой питомец
- `/shop` - Магазин
- `/referrals` - Реферальная система
- `/quests` - Квесты
- `/top` - Лидерборд

## 🎮 Геймплей

### Онбординг (3-5 минут)

1. **Выбор языка** - 4 языка на выбор
2. **Ввод никнейма** - уникальный ник с валидацией
3. **Выбор аватара** - 12 милых эмодзи
4. **Туториал** - интерактивное обучение в 3 шага
5. **Стартовый бонус**:
   - 150 искр 🔥
   - 1 Щит огонька 🛡️
   - Яйцо серийчика 🥚

### Система огоньков

1. **Зажигание**:
   - Найди друга по @username
   - Отправь запрос
   - Друг должен принять
   
2. **Поддержание**:
   - Оба должны продлевать раз в 24 часа
   - Награда за продление: 20-40+ искр
   - Цвет огонька меняется с ростом серии

3. **Милестоуны** (7, 14, 30, 50, 100, 200, 365, 500, 1000+ дней):
   - Крупные награды искрами
   - Редкие питомцы
   - Уникальные достижения
   - Коллекционные предметы

4. **Спасение**:
   - 0-72 часа: 120 ⭐
   - 72-168 часов: 350 ⭐
   - После 7 дней: только новая серия

### Питомцы (Серийчики)

1. **Вылупление**: После 3 дней активной серии
2. **Эволюция**: 
   - 🥚 Яйцо (0 дней)
   - 🐣 Малыш (3 дня)
   - 🐥 Подросток (10 дней)
   - 🦜 Взрослый (30 дней)
   - 🦅 Старейшина (100 дней)
   - ✨🔥 Мифический (365 дней)

3. **Взаимодействие**:
   - 🍖 Покормить (30 искр → exp)
   - 🤗 Погладить (бесплатно → настроение)
   - 🎮 Играть (20 энергии → искры + exp)
   - 💃 Потанцевать (бесплатно → exp + эмоция)

4. **Настроения**: счастливый, нейтральный, голодный, грустный, депрессия

### Реферальная система

**Многоуровневая система наград:**

| Рефералов | Награда |
|-----------|---------|
| 1 | 50 🔥 |
| 2 | 80 🔥 |
| 3 | 120 🔥 |
| 4 | 200 🔥 |
| 5 | 350 🔥 |
| 10 | 600 🔥 + бонус |
| 25 | 1200 🔥 + уникальный титул |
| 50 | 2500 🔥 + VIP статус |
| 100 | 5000 🔥 + легендарная аура |

**Бонусы:**
- Telegram Premium рефералы дают ×2 награду
- Первые 3 реферала - мгновенный буст серийчику
- Достижения за каждый милестоун

### Экономика

**Искры 🔥** (Free currency):
- Ежедневка: +10-50
- Продление стрика: +20-40
- Рефералы: +50-1500
- Мини-игры: +5-15
- Квесты: +50-200

**Звёзды ⭐** (Premium currency):
- Достижения за милестоуны
- Редкие события
- Покупка (Telegram Stars)
- Топ лидерборда

### Магазин

**Бусты:**
- 🛡️ Огненный Щит (200 🔥) - защита на 7 дней
- 🛡️✨ Вечный Щит (1500 🔥) - защита на 30 дней
- ⚡ Буст ×2 (300 🔥) - двойные искры на 24 часа
- ⚡ Энергия (50 🔥) - +50 энергии

**Питомцы:**
- 🥚✨ Редкое яйцо (800 🔥)
- 🥚🌟 Эпическое яйцо (250 ⭐)

**Спасение:**
- 💫 Воскрешение 0-72ч (120 ⭐)
- 💫 Воскрешение 72-168ч (350 ⭐)

**Подарки:**
- 🎂 Тортик (100 🔥) - +50 искр другу
- 💐 Букет (150 🔥) - +настроение питомцу
- 🚀 Ракета (200 🔥) - +100 exp питомцу
- 👑 Корона (500 🔥) - VIP на 3 дня
- 🔥💎 Вечный Огонь (1000 🔥) - защита на 7 дней

## 🔧 Разработка и расширение

### Добавление новых языков

Отредактируй `locales/translations.py`:

```python
Language.FR: {
    "welcome_1": "✨ **Bonjour\\!** ...",
    # ...
}
```

### Добавление новых питомцев

Отредактируй `config/constants.py`:

```python
BASE_PETS = {
    "legendary": ["🔥🦅", "⚡🦉", "🌟🐉", "🌈🦄", "🎨🦋"],
    # ...
}
```

### Добавление новых квестов

Создай квесты при старте бота или по расписанию:

```python
await db.create_quest(
    user_id=user_id,
    type_=QuestType.DAILY,
    name="Зажги 3 огонька",
    description="Найди трёх друзей и зажги с ними огоньки",
    target=3,
    reward_sparks=100,
    expires_at=datetime.now() + timedelta(days=1)
)
```

### Добавление Telegram Stars платежей

```python
from aiogram.types import LabeledPrice

# В handler для покупки
@router.callback_query(F.data == "buy_stars")
async def send_invoice(callback: CallbackQuery):
    prices = [LabeledPrice(label="100 звёзд", amount=100)]
    
    await callback.bot.send_invoice(
        chat_id=callback.from_user.id,
        title="Покупка звёзд",
        description="100 звёзд для игры",
        payload="stars_100",
        provider_token="",  # Оставь пустым для Telegram Stars
        currency="XTR",
        prices=prices
    )

# Обработчик успешного платежа
@router.pre_checkout_query()
async def process_pre_checkout(pre_checkout_query):
    await pre_checkout_query.answer(ok=True)

@router.message(F.successful_payment)
async def process_successful_payment(message: Message):
    await db.add_stars(message.from_user.id, 100)
    await message.answer("✅ 100 звёзд зачислено!")
```

## 📊 Мониторинг и логирование

Бот использует `structlog` для структурированного логирования:

```python
logger.info("event_name", user_id=123, extra_data="value")
```

Для production рекомендуется:
- **Sentry** - отслеживание ошибок
- **Prometheus** - метрики
- **Grafana** - визуализация

## 🧪 Тестирование

### Локальное тестирование

1. Создай несколько тестовых аккаунтов в Telegram
2. Запусти бота
3. Протестируй флоу:
   - Онбординг
   - Создание стрика между двумя аккаунтами
   - Продление стрика
   - Реферальную систему

### Тестирование рефералов

```bash
# Аккаунт 1
/start ref_123456789

# Аккаунт 2 (123456789)
/referrals  # Проверь, что появился реферал
```

## 🚀 Деплой

### Docker

Создай `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

Создай `docker-compose.yml`:

```yaml
version: '3.8'

services:
  bot:
    build: .
    env_file:
      - .env
    volumes:
      - ./data:/app/data
    restart: unless-stopped
```

Запусти:

```bash
docker-compose up -d
```

### VPS (Ubuntu/Debian)

```bash
# Установка зависимостей
sudo apt update
sudo apt install python3.11 python3.11-venv git

# Клонирование
git clone <repo_url>
cd friendship-flames-bot

# Виртуальное окружение
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Настройка .env
nano .env

# Systemd service
sudo nano /etc/systemd/system/flames-bot.service
```

Содержимое service файла:

```ini
[Unit]
Description=Friendship Flames Bot
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/home/youruser/friendship-flames-bot
Environment="PATH=/home/youruser/friendship-flames-bot/venv/bin"
ExecStart=/home/youruser/friendship-flames-bot/venv/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Запуск:

```bash
sudo systemctl daemon-reload
sudo systemctl enable flames-bot
sudo systemctl start flames-bot
sudo systemctl status flames-bot
```

## 💰 Монетизация

### 1. Telegram Stars

- Покупка звёзд (премиум валюта)
- VIP подписки (×2 искры, приоритет в топе)
- Эксклюзивные питомцы
- Ускоренное восстановление энергии

### 2. Реклама

- Баннеры в меню (ненавязчиво)
- Рекламные квесты (бонус за просмотр)
- Спонсорские события

### 3. Партнёрства

- Коллаборации с другими ботами
- Кросс-промо
- Брендированные питомцы

### 4. Premium подписка

```python
PREMIUM_FEATURES = {
    "double_sparks": True,
    "exclusive_pets": True,
    "no_ads": True,
    "priority_support": True,
    "custom_emoji": True,
    "leaderboard_badge": "⭐",
}
```

## 📈 Точки роста

### Краткосрочные (1-2 недели)

- [ ] Ежедневные/еженедельные квесты с автогенерацией
- [ ] Кастомизация питомцев (50+ предметов)
- [ ] Мини-игра "Поймай искры" (кликер)
- [ ] Push-уведомления за 4ч/1ч/30мин до гашения
- [ ] Генерация красивых story-картинок для шеринга

### Среднесрочные (1 месяц)

- [ ] Сезонные события (Новый год, 14 февраля, Хэллоуин)
- [ ] Глобальный огонь (monthly event)
- [ ] Коллекционные карточки/NFT
- [ ] Гильдии/Команды (групповые стрики)
- [ ] Турниры и PvP элементы

### Долгосрочные (3+ месяца)

- [ ] Web-интерфейс (Telegram Mini Apps)
- [ ] Интеграция с TON (крипто-награды)
- [ ] Marketplace для обмена питомцами
- [ ] Кросс-платформенность (веб, мобильное приложение)
- [ ] AI-генерация уникальных питомцев

## 🐛 Известные ограничения

1. **Нет автоматических уведомлений** - нужен отдельный процесс-планировщик
2. **In-memory FSM** - при перезапуске теряется состояние (используй Redis для production)
3. **SQLite** - для масштабирования нужна PostgreSQL
4. **Анти-чит базовый** - нужна более сложная система

## 🤝 Вклад и поддержка

Если хочешь улучшить бота:

1. Fork проекта
2. Создай feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit изменений (`git commit -m 'Add some AmazingFeature'`)
4. Push в branch (`git push origin feature/AmazingFeature`)
5. Открой Pull Request

## 📄 Лицензия

MIT License - свободно используй в коммерческих и некоммерческих проектах.

## 🌟 Авторы и благодарности

Создано с ❤️ и 🔥 для сообщества Telegram

**Retention target**: 60%+ на D7  
**K-factor target**: 1.2+  
**Emotional impact**: 9/10 🥺🔥

---

**Готов к запуску!** 🚀 Создай своё сообщество огоньков!
