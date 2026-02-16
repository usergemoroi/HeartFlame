import asyncio
import sys
from pathlib import Path

import structlog
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import settings
from database import init_database, Database
from handlers import get_handlers_router
from middlewares import ThrottlingMiddleware, UserCheckMiddleware

structlog.configure(
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.dev.ConsoleRenderer()
    ]
)

logger = structlog.get_logger()

bot: Bot = None


async def on_startup():
    logger.info("bot_starting")
    await init_database()
    logger.info("database_initialized")


async def on_shutdown():
    logger.info("bot_shutting_down")


async def main():
    global bot
    
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2)
    )
    
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    
    db = Database()
    
    dp.message.middleware(ThrottlingMiddleware())
    dp.callback_query.middleware(ThrottlingMiddleware())
    
    dp.message.middleware(UserCheckMiddleware(db))
    dp.callback_query.middleware(UserCheckMiddleware(db))
    
    handlers_router = get_handlers_router()
    dp.include_router(handlers_router)
    
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    logger.info("bot_started", bot_username=(await bot.me()).username)
    
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("bot_stopped")
