from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from database.crud import get_user
from utils.time import get_current_timestamp


class UserCheckMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        user = await get_user(user_id)
        
        data['user_data'] = user
        data['is_registered'] = user is not None
        
        if user:
            from database.crud import update_user
            now = get_current_timestamp()
            await update_user(user_id, last_action=now)
        
        return await handler(event, data)
