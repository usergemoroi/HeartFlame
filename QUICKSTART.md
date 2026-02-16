# ⚡ Quick Start Guide

Запустите бота за **5 минут**!

---

## 📋 Шаг 1: Создание бота в Telegram

1. Откройте Telegram и найдите [@BotFather](https://t.me/BotFather)
2. Отправьте команду: `/newbot`
3. Введите имя бота: `Friendship Flames`
4. Введите username бота: `friendship_flames_bot` (должен быть уникальным)
5. **Сохраните токен** — он понадобится на следующем шаге

Пример токена: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`

### Дополнительные настройки бота (опционально):

```
/setdescription - Краткое описание
Зажигайте огоньки дружбы каждый день! 🔥 Коллекционируйте питомцев и соревнуйтесь с друзьями!

/setabouttext - Подробное описание
Friendship Flames 2.0 — это социальная игра, где вы поддерживаете дружбу через ежедневные серии. Вылупляйте магических питомцев, выполняйте квесты и приглашайте друзей!

/setuserpic - Загрузите аватар (512x512px PNG)

/setcommands - Команды бота:
start - Запустить бота
menu - Главное меню
profile - Мой профиль
streaks - Мои огоньки
pets - Мои питомцы
friends - Список друзей
shop - Магазин
```

---

## 📦 Шаг 2: Установка

### На Linux/macOS:

```bash
# Клонируйте или скачайте проект
cd /path/to/friendship-flames-bot

# Создайте виртуальное окружение
python3.11 -m venv venv
source venv/bin/activate

# Установите зависимости
pip install -r requirements.txt
```

### На Windows:

```powershell
# Создайте виртуальное окружение
python -m venv venv
venv\Scripts\activate

# Установите зависимости
pip install -r requirements.txt
```

---

## 🔑 Шаг 3: Настройка

Создайте файл `.env` в корневой папке проекта:

```env
BOT_TOKEN=ВСТАВЬТЕ_ВАШ_ТОКЕН_СЮДА
ADMIN_IDS=ВАШ_TELEGRAM_ID
DATABASE_PATH=./friendship_flames.db
DEBUG=False
```

### Как узнать свой Telegram ID?

1. Напишите боту [@userinfobot](https://t.me/userinfobot)
2. Он отправит вам ваш ID (например: `123456789`)
3. Вставьте этот ID в поле `ADMIN_IDS` в `.env`

Если админов несколько, перечислите через запятую:
```env
ADMIN_IDS=123456789,987654321,555666777
```

---

## 🚀 Шаг 4: Запуск

```bash
python main.py
```

Вы должны увидеть:

```
2024-01-15T12:00:00 [info] Starting Friendship Flames Bot 2.0...
2024-01-15T12:00:00 [info] Initializing database...
2024-01-15T12:00:00 [info] Database initialized successfully
2024-01-15T12:00:00 [info] Background tasks initialized
2024-01-15T12:00:00 [info] Bot started successfully! Press Ctrl+C to stop.
```

✅ **Готово!** Бот запущен и готов к использованию.

---

## 🧪 Шаг 5: Первый тест

1. Откройте Telegram
2. Найдите вашего бота по username (например: `@friendship_flames_bot`)
3. Нажмите `/start`
4. Пройдите онбординг:
   - Выберите язык 🌍
   - Введите никнейм 👤
   - Выберите аватар 🎭
   - Пройдите туториал (3 шага)
5. Получите приветственный бонус: **+150🔥 искр + 🛡️ щит + 🥚 питомец**

---

## 👥 Шаг 6: Тест с другом (или вторым аккаунтом)

### Сценарий: зажигание огонька

**Аккаунт А:**
1. В меню выберите `🔥 Мои огоньки`
2. Нажмите `🔥 Зажечь новый огонёк`
3. Введите @username аккаунта Б

**Аккаунт Б:**
1. Получит уведомление: "🔥 Новый запрос на огонёк!"
2. Нажмите `✅ Принять`

**Результат:**
- Оба аккаунта получат: "✨ Огонёк зажжён! 🔥"
- Счётчик: `🟥 День 1`

### Тест продления:

**Через 8 часов** (можно подождать или изменить в коде cooldown):
1. Любой аккаунт: `🔥 Продлить`
2. Оба получат уведомление
3. Счётчик: `🟧 День 2` (цвет изменился!)

### Вылупление питомца:

**После 3 продлений:**
- `🎉 ПИТОМЕЦ ВЫЛУПИЛСЯ! 🥚→🐣`
- Случайный питомец (common/rare/epic/legendary/mythic)
- Можно кормить, гладить, играть

---

## 🔥 Продвинутые тесты

### Тест реферальной системы:

1. В меню: `💫 Рефералы`
2. Скопируйте реферальную ссылку
3. Отправьте другу (или откройте в другом Telegram-аккаунте)
4. Друг проходит регистрацию
5. Вы получаете: `🎉 Новый реферал! +50🔥 искр`

### Тест питомца:

1. `🐣 Мои питомцы` → выберите питомца
2. `🍖 Покормить` (–30🔥, +15-30 XP)
3. При накоплении XP → **Level Up!**
4. Каждый 5-й уровень → **эволюция редкости**

### Тест магазина:

1. `🛒 Магазин`
2. Купите `🛡️ Щит огонька` (100🔥)
3. Баланс искр уменьшится

### Тест квестов:

1. `📋 Квесты`
2. Смотрите ежедневные и недельные квесты
3. Выполняйте их для получения наград

---

## 🛠️ Troubleshooting

### ❌ Ошибка: "No module named 'aiogram'"

**Решение:**
```bash
# Убедитесь, что виртуальное окружение активировано
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Переустановите зависимости
pip install -r requirements.txt
```

### ❌ Ошибка: "Invalid token"

**Решение:**
1. Проверьте, что в `.env` правильно указан токен
2. Токен должен быть без пробелов и кавычек
3. Формат: `BOT_TOKEN=1234567890:ABCdef...`

### ❌ Бот не отвечает

**Решение:**
1. Убедитесь, что `python main.py` запущен
2. Проверьте логи в терминале на ошибки
3. Перезапустите бота: `Ctrl+C` → `python main.py`

### ❌ База данных заблокирована

**Решение:**
```bash
# Закройте все процессы, использующие БД
pkill -f main.py

# Удалите БД и пересоздайте
rm friendship_flames.db
python main.py
```

---

## 📊 Мониторинг

### Просмотр логов в реальном времени:

```bash
python main.py 2>&1 | tee bot.log
```

### Статистика базы данных:

```bash
sqlite3 friendship_flames.db

# В SQLite консоли:
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM streaks WHERE status = 'active';
SELECT COUNT(*) FROM pets;

# Топ-10 пользователей по искрам:
SELECT nickname, sparks FROM users ORDER BY sparks DESC LIMIT 10;

# Выход:
.exit
```

---

## 🎯 Следующие шаги

### 1. Настройте автозапуск (Linux/VPS):

```bash
# Создайте systemd service
sudo nano /etc/systemd/system/flames-bot.service
```

Вставьте:
```ini
[Unit]
Description=Friendship Flames Bot
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/path/to/flames-bot
Environment="PATH=/path/to/flames-bot/venv/bin"
ExecStart=/path/to/flames-bot/venv/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Активируйте:
```bash
sudo systemctl enable flames-bot
sudo systemctl start flames-bot
sudo systemctl status flames-bot
```

### 2. Добавьте мониторинг

Установите Sentry для отслеживания ошибок:

```bash
pip install sentry-sdk
```

В `main.py` добавьте:
```python
import sentry_sdk
sentry_sdk.init("YOUR_SENTRY_DSN")
```

### 3. Расширьте функционал

См. `README.md` → раздел "Точки роста и монетизация"

---

## 🎉 Готово!

Ваш бот запущен и готов масштабироваться!

**Поделитесь ссылкой с друзьями:**
```
https://t.me/ваш_бот_username?start=ref123456789
```

**Полезные ссылки:**
- 📖 Полная документация: `README.md`
- 🔧 Настройка конфига: `config.py`
- 💾 База данных: `database/`
- 🎨 Тексты и локализация: `utils/text.py`

---

**Вопросы?** Читайте `README.md` или проверьте Issues в репозитории!

🔥 **Удачного запуска!** 🚀
