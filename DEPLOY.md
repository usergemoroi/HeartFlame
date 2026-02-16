# 🚀 Deployment Guide

Гайд по деплою бота на production-сервер.

---

## 🖥️ Варианты деплоя

### 1. VPS/Dedicated Server (рекомендуется)
- ✅ Полный контроль
- ✅ Низкая стоимость (~$5-10/месяц)
- ✅ Легко масштабируется

### 2. Docker на VPS
- ✅ Изолированная среда
- ✅ Легко обновлять
- ✅ Портабельность

### 3. Cloud Platform (AWS, Google Cloud, Azure)
- ✅ Автоматическое масштабирование
- ✅ Высокая доступность
- ❌ Дороже

### 4. Managed Bot Hosting
- ✅ Простая настройка
- ❌ Ограничения
- ❌ Дорого

---

## 🐧 Linux VPS Deployment (Ubuntu 22.04)

### Шаг 1: Подготовка сервера

```bash
# Обновите систему
sudo apt update && sudo apt upgrade -y

# Установите необходимые пакеты
sudo apt install -y python3.11 python3.11-venv python3-pip git sqlite3

# Создайте пользователя для бота
sudo adduser botuser
sudo usermod -aG sudo botuser
su - botuser
```

### Шаг 2: Клонирование проекта

```bash
cd ~
git clone https://github.com/yourusername/friendship-flames-bot.git
cd friendship-flames-bot

# Или загрузите через scp
# scp -r /local/path/friendship-flames-bot user@server:/home/botuser/
```

### Шаг 3: Настройка окружения

```bash
# Создайте виртуальное окружение
python3.11 -m venv venv
source venv/bin/activate

# Установите зависимости
pip install -r requirements.txt

# Создайте .env файл
nano .env
```

Вставьте:
```env
BOT_TOKEN=YOUR_BOT_TOKEN_HERE
ADMIN_IDS=YOUR_TELEGRAM_ID
DATABASE_PATH=/home/botuser/friendship-flames-bot/data/friendship_flames.db
DEBUG=False
```

```bash
# Создайте директорию для БД
mkdir -p data
```

### Шаг 4: Тестовый запуск

```bash
python main.py
```

Если всё работает, нажмите `Ctrl+C` и переходите к следующему шагу.

### Шаг 5: Настройка systemd service

```bash
sudo nano /etc/systemd/system/friendship-flames.service
```

Вставьте:
```ini
[Unit]
Description=Friendship Flames Bot
After=network.target

[Service]
Type=simple
User=botuser
WorkingDirectory=/home/botuser/friendship-flames-bot
Environment="PATH=/home/botuser/friendship-flames-bot/venv/bin"
ExecStart=/home/botuser/friendship-flames-bot/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Перезагрузите systemd
sudo systemctl daemon-reload

# Включите автозапуск
sudo systemctl enable friendship-flames

# Запустите бота
sudo systemctl start friendship-flames

# Проверьте статус
sudo systemctl status friendship-flames
```

### Шаг 6: Настройка логирования

```bash
# Просмотр логов в реальном времени
sudo journalctl -u friendship-flames -f

# Последние 100 строк
sudo journalctl -u friendship-flames -n 100

# Логи за сегодня
sudo journalctl -u friendship-flames --since today
```

### Шаг 7: Backup базы данных

Создайте скрипт backup:

```bash
nano ~/backup-bot.sh
```

Вставьте:
```bash
#!/bin/bash
BACKUP_DIR="/home/botuser/backups"
DB_PATH="/home/botuser/friendship-flames-bot/data/friendship_flames.db"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

cp $DB_PATH $BACKUP_DIR/flames_$DATE.db
sqlite3 $DB_PATH "VACUUM;"

# Удалить бэкапы старше 30 дней
find $BACKUP_DIR -name "flames_*.db" -mtime +30 -delete

echo "Backup completed: $BACKUP_DIR/flames_$DATE.db"
```

```bash
chmod +x ~/backup-bot.sh

# Добавьте в crontab для ежедневного бэкапа в 3:00
crontab -e
```

Добавьте строку:
```
0 3 * * * /home/botuser/backup-bot.sh >> /home/botuser/backup.log 2>&1
```

---

## 🐳 Docker Deployment

### Шаг 1: Установка Docker

```bash
# Установите Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Установите Docker Compose
sudo apt install docker-compose

# Добавьте пользователя в группу docker
sudo usermod -aG docker $USER
newgrp docker
```

### Шаг 2: Настройка проекта

```bash
cd /path/to/friendship-flames-bot

# Создайте .env
nano .env
```

Вставьте конфигурацию (см. выше).

### Шаг 3: Запуск

```bash
# Соберите образ и запустите
docker-compose up -d

# Проверьте логи
docker-compose logs -f

# Остановить
docker-compose down

# Перезапустить
docker-compose restart
```

### Шаг 4: Обновление

```bash
# Остановите контейнер
docker-compose down

# Обновите код
git pull

# Пересоберите и запустите
docker-compose up -d --build
```

---

## ☁️ AWS Deployment (EC2)

### Шаг 1: Создание EC2 инстанса

1. Войдите в AWS Console
2. EC2 → Launch Instance
3. Выберите Ubuntu 22.04 LTS
4. Тип: t2.micro (Free Tier) или t2.small
5. Security Group:
   - SSH (22) - ваш IP
   - HTTPS (443) - если нужен webhook
6. Создайте ключ или используйте существующий

### Шаг 2: Подключение

```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```

### Шаг 3: Настройка

Следуйте инструкциям из раздела "Linux VPS Deployment".

### Шаг 4: Настройка Elastic IP (опционально)

1. EC2 → Elastic IPs → Allocate
2. Associate с вашим инстансом
3. Теперь IP не изменится при перезапуске

---

## 🔧 Advanced: Webhook Mode

### Зачем нужен webhook?

- ✅ Мгновенная доставка сообщений (без polling delay)
- ✅ Меньше нагрузка на сервер
- ✅ Рекомендуется для >1000 пользователей

### Требования

- Доменное имя (например: bot.yourdomain.com)
- SSL сертификат (Let's Encrypt)
- Nginx

### Шаг 1: Домен и SSL

```bash
# Установите certbot
sudo apt install certbot python3-certbot-nginx

# Получите SSL сертификат
sudo certbot --nginx -d bot.yourdomain.com
```

### Шаг 2: Настройка Nginx

```bash
sudo nano /etc/nginx/sites-available/bot
```

Вставьте:
```nginx
server {
    listen 443 ssl;
    server_name bot.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/bot.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/bot.yourdomain.com/privkey.pem;

    location /webhook {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/bot /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Шаг 3: Изменение кода бота

В `main.py` замените polling на webhook:

```python
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"https://bot.yourdomain.com{WEBHOOK_PATH}"

async def on_startup(bot: Bot):
    await init_database()
    await bot.set_webhook(WEBHOOK_URL)
    from tasks import start_background_tasks
    await start_background_tasks(bot)

async def main():
    # ... (инициализация как раньше)
    
    # Вместо polling:
    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot
    )
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)
    
    await on_startup(bot)
    
    web.run_app(app, host="127.0.0.1", port=8080)
```

---

## 📊 Monitoring & Alerting

### 1. Simple Status Check

Создайте скрипт проверки:

```bash
nano ~/check-bot.sh
```

```bash
#!/bin/bash
if ! systemctl is-active --quiet friendship-flames; then
    echo "Bot is down! Restarting..."
    sudo systemctl restart friendship-flames
    
    # Отправить уведомление в Telegram
    curl -s -X POST "https://api.telegram.org/bot$BOT_TOKEN/sendMessage" \
         -d chat_id="YOUR_ADMIN_ID" \
         -d text="⚠️ Bot was down and restarted at $(date)"
fi
```

```bash
chmod +x ~/check-bot.sh

# Добавьте в crontab (проверка каждые 5 минут)
crontab -e
```

Добавьте:
```
*/5 * * * * /home/botuser/check-bot.sh
```

### 2. Prometheus + Grafana (Advanced)

#### Установка Prometheus

```bash
sudo apt install prometheus
```

В коде бота добавьте метрики:

```python
from prometheus_client import Counter, start_http_server

messages_counter = Counter('bot_messages_total', 'Total messages processed')

@router.message()
async def process_message(message: Message):
    messages_counter.inc()
    # ...

# В main():
start_http_server(9090)
```

#### Установка Grafana

```bash
sudo apt install grafana
sudo systemctl enable grafana-server
sudo systemctl start grafana-server
```

Откройте http://your-server:3000 (admin/admin).

---

## 🔒 Security Best Practices

### 1. Файрвол (UFW)

```bash
sudo ufw allow ssh
sudo ufw allow 443/tcp  # HTTPS для webhook
sudo ufw enable
```

### 2. Fail2Ban (защита от брутфорса SSH)

```bash
sudo apt install fail2ban
sudo systemctl enable fail2ban
```

### 3. Регулярные обновления

```bash
sudo apt update && sudo apt upgrade -y
sudo reboot
```

### 4. Ограничение прав

```bash
# Бот должен работать от непривилегированного пользователя
# Файлы должны быть readable только владельцем
chmod 600 .env
chmod 700 data/
```

---

## 📈 Performance Tuning

### SQLite оптимизация

В `database/init_db.py` добавьте:

```python
async def init_database():
    db = await aiosqlite.connect(settings.DATABASE_PATH)
    
    # Оптимизация для производительности
    await db.execute("PRAGMA journal_mode=WAL")
    await db.execute("PRAGMA synchronous=NORMAL")
    await db.execute("PRAGMA cache_size=10000")
    await db.execute("PRAGMA temp_store=MEMORY")
    
    # ... остальное
```

### Переход на PostgreSQL (>50k пользователей)

```bash
sudo apt install postgresql postgresql-contrib

pip install asyncpg
```

Измените `database/init_db.py`:

```python
import asyncpg

async def get_db():
    return await asyncpg.connect(
        host='localhost',
        database='flames_db',
        user='flames_user',
        password='your_password'
    )
```

---

## 🆘 Troubleshooting

### Бот не запускается

```bash
# Проверьте логи
sudo journalctl -u friendship-flames -n 100

# Проверьте синтаксис
python3 -m py_compile main.py

# Проверьте токен
grep BOT_TOKEN .env
```

### База данных заблокирована

```bash
# Найдите процессы, использующие БД
lsof data/friendship_flames.db

# Убейте процессы
pkill -f main.py

# Перезапустите
sudo systemctl restart friendship-flames
```

### Бот отвечает медленно

- Проверьте нагрузку: `htop`
- Увеличьте RAM или CPU
- Переходите на PostgreSQL
- Добавьте Redis для кэширования

---

## 📞 Support

Проблемы с деплоем?
- 📖 Читайте логи: `journalctl -u friendship-flames -f`
- 🐛 GitHub Issues
- 💬 Telegram: @yourusername

---

**Удачного деплоя! 🚀**
