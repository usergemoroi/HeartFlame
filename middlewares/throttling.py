from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from datetime import datetime, timedelta
from config import settings


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self):
        self.rate_limit = settings.RATE_LIMIT_REQUESTS
        self.period = settings.RATE_LIMIT_PERIOD
        self.user_timestamps: Dict[int, list] = {}
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        if isinstance(event, (Message, CallbackQuery)):
            user_id = event.from_user.id
            now = datetime.now()
            
            if user_id not in self.user_timestamps:
                self.user_timestamps[user_id] = []
            
            self.user_timestamps[user_id] = [
                ts for ts in self.user_timestamps[user_id]
                if now - ts < timedelta(seconds=self.period)
            ]
            
            if len(self.user_timestamps[user_id]) >= self.rate_limit:
                if isinstance(event, Message):
                    await event.answer("⏳ Слишком много запросов. Подожди немного...")
                elif isinstance(event, CallbackQuery):
                    await event.answer("⏳ Подожди немного...", show_alert=True)
                return
            
            self.user_timestamps[user_id].append(now)
        
        return await handler(event, data)
