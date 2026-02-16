# 🤝 Contributing Guide

Спасибо за интерес к проекту! Этот гайд поможет вам внести свой вклад.

---

## 🎯 Как помочь проекту

### 1. Найти баг и сообщить о нём
- Создайте Issue с подробным описанием
- Укажите шаги для воспроизведения
- Приложите логи/скриншоты

### 2. Исправить баг
- Форкните репозиторий
- Создайте ветку: `git checkout -b fix/bug-name`
- Исправьте и протестируйте
- Создайте Pull Request

### 3. Добавить новую фичу
- Откройте Issue с предложением
- Дождитесь обсуждения
- Создайте PR с реализацией

### 4. Улучшить документацию
- Исправьте опечатки
- Дополните примеры
- Переведите на другие языки

---

## 📝 Code Style

### Python

Следуйте PEP 8:
```python
# Хорошо ✅
async def get_user_streaks(user_id: int, status: str = 'active') -> List[Dict[str, Any]]:
    db = await get_db()
    # ...
    return results

# Плохо ❌
async def GetUserStreaks(userId,status='active'):
    db=await get_db()
    #...
    return results
```

### Типизация

Всегда используйте type hints:
```python
from typing import Optional, List, Dict, Any

async def create_user(
    user_id: int,
    username: Optional[str],
    nickname: str,
    avatar: str
) -> bool:
    # ...
```

### Документация

Добавляйте docstrings для сложных функций:
```python
async def process_referral(referrer_id: int, new_user_id: int, level: int = 1) -> int:
    """
    Обрабатывает реферальное вознаграждение.
    
    Args:
        referrer_id: ID реферера
        new_user_id: ID нового пользователя
        level: Уровень реферальной сети (1-3)
    
    Returns:
        Количество начисленных искр
    """
    # ...
```

---

## 🧪 Тестирование

Перед коммитом протестируйте:

```bash
# 1. Проверьте синтаксис
python -m py_compile main.py

# 2. Запустите бота
python main.py

# 3. Протестируйте основные флоу:
# - /start с регистрацией
# - Создание огонька
# - Продление серии
# - Покупка в магазине
```

---

## 🔀 Git Workflow

### Именование веток

- `feature/название` — новая фича
- `fix/название` — исправление бага
- `docs/название` — документация
- `refactor/название` — рефакторинг

Примеры:
```bash
git checkout -b feature/achievements-system
git checkout -b fix/streak-expiry-bug
git checkout -b docs/spanish-translation
```

### Коммиты

Используйте Conventional Commits:

```
feat: add achievements system
fix: correct streak expiry calculation
docs: add Spanish translations
refactor: optimize database queries
style: format code with black
test: add unit tests for pets module
```

### Pull Request

Шаблон PR:

```markdown
## Описание
Краткое описание изменений

## Тип изменения
- [ ] Новая фича
- [ ] Исправление бага
- [ ] Документация
- [ ] Рефакторинг

## Тестирование
- [ ] Протестировано локально
- [ ] Проверены edge cases
- [ ] Обновлена документация

## Скриншоты
(если применимо)
```

---

## 📂 Структура проекта

```
friendship-flames-bot/
├── config.py              # Конфигурация
├── main.py               # Точка входа
├── tasks.py              # Фоновые задачи
├── requirements.txt      # Зависимости
├── .env.example         # Пример .env
├── database/
│   ├── init_db.py       # Инициализация БД
│   └── crud.py          # CRUD операции
├── handlers/            # Обработчики команд
│   ├── start.py
│   ├── profile.py
│   ├── streaks.py
│   ├── pets.py
│   ├── shop.py
│   ├── referrals.py
│   ├── leaderboard.py
│   ├── quests.py
│   ├── gifts.py
│   ├── games.py
│   └── friends.py
├── keyboards/           # Клавиатуры
│   └── inline.py
├── middlewares/         # Middleware
│   ├── user_check.py
│   └── throttling.py
├── states/              # FSM состояния
│   └── fsm.py
└── utils/              # Утилиты
    ├── text.py         # Тексты и локализация
    └── time.py         # Работа со временем
```

### Где что добавлять

- **Новый язык**: `utils/text.py` + `config.py`
- **Новая команда**: создайте handler в `handlers/`
- **Новая механика**: handler + CRUD в `database/crud.py`
- **Новая валюта/ресурс**: `config.py` + миграция БД
- **Фоновая задача**: `tasks.py`

---

## 🗃️ База данных

### Миграции

При изменении структуры БД:

1. **Создайте backup**:
```bash
cp friendship_flames.db friendship_flames.db.backup
```

2. **Напишите миграцию**:
```python
# migrations/001_add_achievements.py
async def migrate():
    db = await get_db()
    
    await db.execute("""
        CREATE TABLE IF NOT EXISTS achievements (
            achievement_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            achievement_type TEXT NOT NULL,
            unlocked_at INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)
    
    await db.commit()
    await db.close()
```

3. **Примените**:
```python
# В main.py
from migrations import migrate_001
await migrate_001.migrate()
```

---

## 🐛 Debugging

### Логирование

Добавляйте логи для отладки:

```python
import structlog

logger = structlog.get_logger()

async def complex_function():
    logger.info("Starting complex operation", user_id=123)
    
    try:
        # Ваш код
        logger.debug("Intermediate step completed", data=some_data)
    except Exception as e:
        logger.error("Error occurred", error=str(e), user_id=123)
        raise
    
    logger.info("Operation completed successfully")
```

### SQLite консоль

Отладка БД:

```bash
sqlite3 friendship_flames.db

# Просмотр структуры
.schema users

# Выборка данных
SELECT * FROM users LIMIT 5;

# Проверка активных серий
SELECT s.streak_id, s.days, u1.nickname, u2.nickname 
FROM streaks s
JOIN users u1 ON s.user1_id = u1.user_id
JOIN users u2 ON s.user2_id = u2.user_id
WHERE s.status = 'active';
```

---

## 🌐 Локализация

### Добавление нового языка

1. **config.py**:
```python
LANGUAGES = {
    # ...
    'pt': '🇵🇹 Português',
}
```

2. **utils/text.py**:
```python
TEXTS = {
    # ...
    'pt': {
        'welcome_1': "✨ Bem-vindo...",
        # ... все ключи из 'en'
    }
}
```

3. **Протестируйте**:
```bash
python main.py
# Выберите новый язык при регистрации
```

---

## 📊 Performance

### Оптимизация запросов

❌ **Плохо** (N+1 запросов):
```python
for streak in streaks:
    friend = await get_user(streak['friend_id'])
    # ...
```

✅ **Хорошо** (1 запрос с JOIN):
```python
cursor = await db.execute("""
    SELECT s.*, u.nickname, u.avatar
    FROM streaks s
    JOIN users u ON s.friend_id = u.user_id
""")
```

### Индексация

При большом количестве пользователей:

```sql
CREATE INDEX idx_users_referrer ON users(referrer_id);
CREATE INDEX idx_streaks_expiry ON streaks(streak_expiry);
CREATE INDEX idx_quests_user_status ON quests(user_id, status);
```

---

## 🚀 Деплой

### Подготовка к production

1. **Оптимизируйте БД**:
```bash
sqlite3 friendship_flames.db "VACUUM;"
```

2. **Включите логирование**:
```python
# В config.py
DEBUG = False
```

3. **Настройте systemd** (см. README.md)

4. **Мониторинг**:
- Sentry для ошибок
- Prometheus для метрик
- Grafana для визуализации

---

## ✅ Checklist перед PR

- [ ] Код следует PEP 8
- [ ] Добавлены type hints
- [ ] Протестировано локально
- [ ] Нет print() — только logger
- [ ] Обновлена документация
- [ ] Коммиты следуют Conventional Commits
- [ ] Нет секретов в коде (токены, пароли)
- [ ] Backward compatible (если возможно)

---

## 📞 Контакты

Вопросы по разработке:
- Telegram: @your_username
- Email: dev@yourproject.com

---

Спасибо за вклад в проект! 🙏
