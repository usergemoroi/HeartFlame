from datetime import datetime, timedelta


def format_time_left(expiry: datetime) -> str:
    delta = expiry - datetime.now()
    
    if delta.total_seconds() < 0:
        return "🔴 Погас"
    
    hours = int(delta.total_seconds() // 3600)
    minutes = int((delta.total_seconds() % 3600) // 60)
    
    if hours > 0:
        return f"{hours}ч {minutes}м"
    else:
        return f"{minutes}м"


def format_duration(seconds: int) -> str:
    if seconds < 60:
        return f"{seconds}с"
    
    minutes = seconds // 60
    hours = minutes // 60
    
    if hours > 0:
        remaining_minutes = minutes % 60
        return f"{hours}ч {remaining_minutes}м"
    else:
        return f"{minutes}м"
