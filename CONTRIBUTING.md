# 🤝 Contributing to Friendship Flames Bot

Спасибо за интерес к улучшению проекта! Вот гайд по внесению изменений.

## 📋 Содержание

- [Code of Conduct](#code-of-conduct)
- [Как начать](#как-начать)
- [Структура проекта](#структура-проекта)
- [Стиль кода](#стиль-кода)
- [Тестирование](#тестирование)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

- Будь уважителен к другим контрибьюторам
- Конструктивная критика приветствуется
- Никакого токсичного поведения

## Как начать

1. **Fork репозиторий**
2. **Клонируй свой fork**:
   ```bash
   git clone https://github.com/your-username/friendship-flames-bot.git
   cd friendship-flames-bot
   ```

3. **Создай ветку для фичи**:
   ```bash
   git checkout -b feature/amazing-feature
   ```

4. **Установи зависимости**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # если есть
   ```

5. **Создай .env** и добавь свой токен

## Структура проекта

```
├── config/         # Конфигурация
├── database/       # БД
├── handlers/       # Обработчики команд
├── keyboards/      # Клавиатуры
├── states/         # FSM состояния
├── middlewares/    # Middleware
├── utils/          # Утилиты
├── locales/        # Переводы
└── tests/          # Тесты (TODO)
```

## Стиль кода

### Python Style Guide

Мы следуем [PEP 8](https://pep8.org/) с некоторыми дополнениями:

- **Максимальная длина строки**: 100 символов
- **Отступы**: 4 пробела
- **Импорты**: группируй и сортируй (stdlib → third-party → local)
- **Type hints**: используй везде где возможно

### Пример хорошего кода:

```python
from typing import Optional, Dict, Any
from datetime import datetime

async def get_user_streak(
    user_id: int,
    friend_id: int
) -> Optional[Dict[str, Any]]:
    """
    Получить информацию о стрике между пользователями.
    
    Args:
        user_id: ID первого пользователя
        friend_id: ID второго пользователя
    
    Returns:
        Словарь с данными стрика или None
    """
    streak = await db.get_streak(user_id, friend_id)
    return streak
```

### Naming Conventions

- **Функции/переменные**: `snake_case`
- **Классы**: `PascalCase`
- **Константы**: `UPPER_SNAKE_CASE`
- **Private методы**: `_leading_underscore`

### Docstrings

Используй Google style docstrings:

```python
def function(arg1: int, arg2: str) -> bool:
    """
    Краткое описание функции.
    
    Более детальное описание если нужно.
    
    Args:
        arg1: Описание первого аргумента
        arg2: Описание второго аргумента
    
    Returns:
        Описание возвращаемого значения
    
    Raises:
        ValueError: Когда возникает ошибка
    """
    pass
```

## Тестирование

(TODO: добавить когда будут тесты)

```bash
# Запуск тестов
pytest

# С coverage
pytest --cov=. --cov-report=html
```

## Pull Request Process

### 1. Перед созданием PR

- [ ] Код соответствует style guide
- [ ] Добавлены docstrings
- [ ] Обновлена документация если нужно
- [ ] Протестировано локально
- [ ] Коммиты имеют понятные сообщения

### 2. Сообщения коммитов

Используй [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: добавил систему гильдий
fix: исправил баг с продлением стрика
docs: обновил README
style: форматирование кода
refactor: рефакторинг handlers
test: добавил тесты для pets
chore: обновил зависимости
```

### 3. Создание PR

1. Push в свой fork:
   ```bash
   git push origin feature/amazing-feature
   ```

2. Создай PR на GitHub

3. Заполни template:
   ```markdown
   ## Описание
   Краткое описание изменений
   
   ## Тип изменений
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation
   
   ## Как протестировать
   1. Шаги для воспроизведения
   2. ...
   
   ## Чеклист
   - [ ] Код следует style guide
   - [ ] Добавлена документация
   - [ ] Протестировано локально
   ```

4. Дождись ревью

### 4. Ревью процесс

- Один из мейнтейнеров проверит твой код
- Могут попросить внести изменения
- После аппрува PR будет смержен

## Что можно улучшать

### 🔥 High Priority

- [ ] Тесты (unit + integration)
- [ ] Кастомизация питомцев
- [ ] Мини-игры
- [ ] Push-уведомления
- [ ] Генерация story-картинок

### 🌟 Nice to Have

- [ ] Web-интерфейс (Telegram Mini Apps)
- [ ] Больше языков
- [ ] Анимации
- [ ] Голосовые реакции
- [ ] Marketplace

### 🐛 Known Issues

- [ ] FSM хранится в памяти (нужен Redis)
- [ ] SQLite не масштабируется (нужна PostgreSQL)
- [ ] Базовый анти-чит

## Вопросы?

- Создай [Issue](https://github.com/your-repo/issues)
- Спроси в [Discussions](https://github.com/your-repo/discussions)
- Напиши мейнтейнерам

---

Спасибо за вклад! 🔥💫
