# ⚡ Quick Start Guide - Огоньки Дружбы 2.0

Запусти бота за **5 минут**!

## 📋 Prerequisites

- Python 3.11+
- Telegram Bot Token
- 5 минут времени

## 🚀 Установка за 5 шагов

### Шаг 1: Получи Bot Token

1. Открой Telegram
2. Найди [@BotFather](https://t.me/BotFather)
3. Отправь `/newbot`
4. Следуй инструкциям
5. Скопируй токен (выглядит так: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

### Шаг 2: Клонируй репозиторий

```bash
git clone <your-repo-url>
cd friendship-flames-bot
```

### Шаг 3: Установи зависимости

```bash
# Создай виртуальное окружение
python3.11 -m venv venv

# Активируй его
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows

# Установи пакеты
pip install -r requirements.txt
```

### Шаг 4: Настрой бота

Используй автоматический скрипт:

```bash
./setup.sh
```

Или вручную создай `.env`:

```bash
cp .env.example .env
nano .env  # или любой редактор
```

Вставь свой токен:

```env
BOT_TOKEN=твой_токен_здесь
ADMIN_IDS=твой_telegram_id
DATABASE_PATH=data/bot.db
LOG_LEVEL=INFO
RATE_LIMIT_REQUESTS=30
RATE_LIMIT_PERIOD=60
```

### Шаг 5: Запусти!

```bash
python main.py
```

Увидишь:

```
INFO bot_starting
INFO database_initialized path=data/bot.db
INFO bot_started bot_username=YourBotName
```

## ✅ Проверь работу

1. Открой свой бот в Telegram
2. Отправь `/start`
3. Пройди онбординг
4. Готово! 🎉

## 🧪 Тестирование функций

### Тест реферальной системы

1. Создай второй тестовый аккаунт
2. В первом аккаунте: `/referrals`
3. Скопируй ссылку
4. Открой во втором аккаунте
5. Проверь что в первом аккаунте начислились искры

### Тест огоньков

1. Нужны 2 аккаунта с usernames
2. Аккаунт 1: Огоньки → Зажечь → @username_аккаунта2
3. Аккаунт 2: принять запрос
4. Оба аккаунта: продлить огонёк

### Тест питомца

1. Зажги огонёк
2. Жди 3 дня (или измени в БД для теста)
3. Питомец → Покормить/Погладить/Играть

## 🔧 Troubleshooting

### Ошибка: "No module named 'aiogram'"

```bash
# Убедись что виртуальное окружение активировано
source venv/bin/activate
pip install -r requirements.txt
```

### Ошибка: "BOT_TOKEN not found"

Проверь что файл `.env` создан и содержит токен.

### База данных не создаётся

Проверь права на запись:

```bash
mkdir -p data
chmod 755 data
```

### Бот не отвечает

1. Проверь токен
2. Проверь интернет
3. Посмотри логи на ошибки
4. Убедись что бот не запущен в другом месте

## 📊 Что дальше?

### Запусти scheduler (опционально)

Для автоматических напоминаний:

```bash
# В отдельном терминале
python scheduler.py
```

### Деплой на сервер

См. подробную инструкцию в [README.md](README.md#деплой)

### Кастомизация

1. Измени языки в `locales/translations.py`
2. Добавь питомцев в `config/constants.py`
3. Настрой награды в `config/constants.py`

## 🎮 Основные команды

| Команда | Описание |
|---------|----------|
| `/start` | Начать / онбординг |
| `/menu` | Главное меню |
| `/profile` | Твой профиль |
| `/streaks` | Управление огоньками |
| `/pet` | Твой питомец |
| `/shop` | Магазин |
| `/referrals` | Реферальная система |
| `/top` | Лидерборд |

## 💡 Pro Tips

### Для разработки

```bash
# Включи debug логи
LOG_LEVEL=DEBUG python main.py
```

### Для production

```bash
# Используй systemd (Linux)
sudo cp flames-bot.service.example /etc/systemd/system/flames-bot.service
# Отредактируй пути
sudo systemctl enable flames-bot
sudo systemctl start flames-bot
```

### Для Docker

```bash
docker-compose up -d
docker-compose logs -f  # смотри логи
```

## 🆘 Нужна помощь?

- 📖 Полная документация: [README.md](README.md)
- 🐛 Найдена ошибка: [GitHub Issues](https://github.com/your-repo/issues)
- 💬 Вопросы: [Discussions](https://github.com/your-repo/discussions)

---

**Готово!** Теперь у тебя работающий бот! 🔥

Следующие шаги:
- [ ] Добавь друзей в бота
- [ ] Зажги первый огонёк
- [ ] Пригласи людей по реферальной ссылке
- [ ] Следи за топом игроков

Удачи! 🚀💫
