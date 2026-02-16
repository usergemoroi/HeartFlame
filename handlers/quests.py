from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.inline import get_quests_keyboard
from database.crud import get_user_quests, create_quest, update_user_sparks
from utils.text import get_text, escape_markdown
from utils.time import get_current_timestamp
import random

router = Router()


@router.callback_query(F.data == "menu_quests")
async def show_quests(callback: CallbackQuery, user_data: dict):
    lang = user_data['language']
    user_id = user_data['user_id']
    
    daily_quests = await get_user_quests(user_id, status='active')
    daily_quests = [q for q in daily_quests if q['period'] == 'daily']
    
    weekly_quests = await get_user_quests(user_id, status='active')
    weekly_quests = [q for q in weekly_quests if q['period'] == 'weekly']
    
    if not daily_quests:
        await generate_daily_quests(user_id, lang)
        daily_quests = await get_user_quests(user_id, status='active')
        daily_quests = [q for q in daily_quests if q['period'] == 'daily']
    
    if not weekly_quests:
        await generate_weekly_quests(user_id, lang)
        weekly_quests = await get_user_quests(user_id, status='active')
        weekly_quests = [q for q in weekly_quests if q['period'] == 'weekly']
    
    daily_text = ""
    for quest in daily_quests[:3]:
        status = "✅" if quest['quest_progress'] >= quest['quest_goal'] else "⏳"
        progress = f"{quest['quest_progress']}/{quest['quest_goal']}"
        
        daily_text += get_text(
            lang,
            'quest_item',
            status=status,
            emoji='🔥',
            name=escape_markdown(quest['quest_name']),
            description=f"Progress: {progress}",
            reward=f"+{quest['reward_sparks']} 🔥",
            progress=progress
        )
    
    weekly_text = ""
    for quest in weekly_quests[:2]:
        status = "✅" if quest['quest_progress'] >= quest['quest_goal'] else "⏳"
        progress = f"{quest['quest_progress']}/{quest['quest_goal']}"
        
        weekly_text += get_text(
            lang,
            'quest_item',
            status=status,
            emoji='📅',
            name=escape_markdown(quest['quest_name']),
            description=f"Progress: {progress}",
            reward=f"+{quest['reward_sparks']} 🔥",
            progress=progress
        )
    
    full_text = get_text(
        lang,
        'quests',
        daily=daily_text or ("No daily quests" if lang == 'en' else "Нет ежедневных квестов"),
        weekly=weekly_text or ("No weekly quests" if lang == 'en' else "Нет недельных квестов")
    )
    
    await callback.message.edit_text(
        full_text,
        reply_markup=get_quests_keyboard(lang),
        parse_mode='MarkdownV2'
    )
    
    await callback.answer()


async def generate_daily_quests(user_id: int, lang: str):
    quests = [
        ("Light 1 new flame", "Зажги 1 новый огонёк", 1, 50),
        ("Extend 2 streaks", "Продли 2 огонька", 2, 80),
        ("Feed your pet 3 times", "Покорми питомца 3 раза", 3, 100),
        ("Send 2 gifts", "Отправь 2 подарка", 2, 70),
        ("Invite 1 friend", "Пригласи 1 друга", 1, 120),
    ]
    
    selected = random.sample(quests, 3)
    
    for quest_en, quest_ru, goal, reward in selected:
        quest_name = quest_ru if lang == 'ru' else quest_en
        await create_quest(
            user_id=user_id,
            quest_type='daily',
            quest_name=quest_name,
            goal=goal,
            reward_sparks=reward,
            period='daily'
        )


async def generate_weekly_quests(user_id: int, lang: str):
    quests = [
        ("Maintain 3 streaks for 7 days", "Держи 3 огонька 7 дней", 3, 500),
        ("Reach 30-day streak", "Достигни 30-дневной серии", 1, 1000),
        ("Invite 5 friends", "Пригласи 5 друзей", 5, 800),
        ("Evolve pet to level 5", "Прокачай питомца до 5 уровня", 1, 600),
    ]
    
    selected = random.sample(quests, 2)
    
    for quest_en, quest_ru, goal, reward in selected:
        quest_name = quest_ru if lang == 'ru' else quest_en
        await create_quest(
            user_id=user_id,
            quest_type='weekly',
            quest_name=quest_name,
            goal=goal,
            reward_sparks=reward,
            period='weekly'
        )
