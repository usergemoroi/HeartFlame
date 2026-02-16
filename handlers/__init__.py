from aiogram import Router
from . import start, menu, profile, streaks, pets, shop, referrals, quests, leaderboard


def get_handlers_router() -> Router:
    router = Router()
    
    router.include_router(start.router)
    router.include_router(menu.router)
    router.include_router(profile.router)
    router.include_router(streaks.router)
    router.include_router(pets.router)
    router.include_router(shop.router)
    router.include_router(referrals.router)
    router.include_router(quests.router)
    router.include_router(leaderboard.router)
    
    return router
