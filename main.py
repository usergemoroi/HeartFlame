import asyncio
import sys
import structlog
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import settings
from database.init_db import init_database
from middlewares.user_check import UserCheckMiddleware
from middlewares.throttling import ThrottlingMiddleware

from handlers import (
    start,
    profile,
    streaks,
    pets,
    shop,
    referrals,
    leaderboard,
    quests,
    gifts,
    games,
    friends
)

logger = structlog.get_logger()


async def on_startup(bot: Bot):
    logger.info("Initializing database...")
    await init_database()
    logger.info("Database initialized successfully")
    
    from tasks import start_background_tasks
    await start_background_tasks(bot)
    logger.info("Background tasks initialized")


async def on_shutdown():
    logger.info("Bot shutting down...")


async def main():
    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer()
        ]
    )
    
    logger.info("Starting Friendship Flames Bot 2.0...")
    
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2)
    )
    
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    
    dp.message.middleware(ThrottlingMiddleware(rate_limit=0.5))
    dp.callback_query.middleware(ThrottlingMiddleware(rate_limit=0.3))
    
    dp.message.middleware(UserCheckMiddleware())
    dp.callback_query.middleware(UserCheckMiddleware())
    
    dp.include_router(start.router)
    dp.include_router(profile.router)
    dp.include_router(streaks.router)
    dp.include_router(pets.router)
    dp.include_router(shop.router)
    dp.include_router(referrals.router)
    dp.include_router(leaderboard.router)
    dp.include_router(quests.router)
    dp.include_router(gifts.router)
    dp.include_router(games.router)
    dp.include_router(friends.router)
    
    dp.startup.register(lambda: on_startup(bot))
    dp.shutdown.register(on_shutdown)
    
    try:
        logger.info("Bot started successfully! Press Ctrl+C to stop.")
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Critical error: {e}")
        raise
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        sys.exit(0)
