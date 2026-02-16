from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
import time


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, rate_limit: float = 0.5):
        self.rate_limit = rate_limit
        self.user_timestamps: Dict[int, float] = {}
    
    async def __call__(
        self,
        handler: Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        current_time = time.time()
        
        if user_id in self.user_timestamps:
            time_passed = current_time - self.user_timestamps[user_id]
            
            if time_passed < self.rate_limit:
                return
        
        self.user_timestamps[user_id] = current_time
        
        return await handler(event, data)
