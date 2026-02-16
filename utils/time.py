from datetime import datetime, timedelta
from typing import Optional


def get_current_timestamp() -> int:
    return int(datetime.now().timestamp())


def get_timestamp_from_datetime(dt: datetime) -> int:
    return int(dt.timestamp())


def get_datetime_from_timestamp(ts: int) -> datetime:
    return datetime.fromtimestamp(ts)


def get_streak_expiry(last_update: int) -> int:
    last_dt = get_datetime_from_timestamp(last_update)
    expiry_dt = last_dt + timedelta(days=1)
    return get_timestamp_from_datetime(expiry_dt)


def get_time_until_expiry(expiry: int) -> int:
    now = get_current_timestamp()
    return max(0, expiry - now)


def can_extend_streak(last_update: int, cooldown_hours: int = 8) -> bool:
    now = get_current_timestamp()
    time_since_last = now - last_update
    return time_since_last >= (cooldown_hours * 3600)


def get_revival_cost(hours_passed: int) -> int:
    if hours_passed <= 72:
        return 120
    elif hours_passed <= 168:
        return 350
    return 999999


def format_date(timestamp: int, lang: str = 'en') -> str:
    dt = get_datetime_from_timestamp(timestamp)
    if lang == 'ru':
        return dt.strftime('%d.%m.%Y')
    return dt.strftime('%Y-%m-%d')
