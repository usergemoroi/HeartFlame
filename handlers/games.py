import asyncio
import random
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.inline import get_games_keyboard, get_back_to_menu_keyboard
from database.crud import update_user_sparks, update_user
from utils.text import get_text
from states.fsm import MiniGameStates

router = Router()


@router.callback_query(F.data == "menu_games")
async def show_games(callback: CallbackQuery, user_data: dict):
    lang = user_data['language']
    
    text = "🎮 *Mini\\-Games*\n\nChoose a game to play\\!" if lang == 'en' else "🎮 *Мини\\-игры*\n\nВыбери игру\\!"
    
    await callback.message.edit_text(
        text,
        reply_markup=get_games_keyboard(lang),
        parse_mode='MarkdownV2'
    )
    
    await callback.answer()


@router.callback_query(F.data == "game_sparks")
async def start_spark_catcher(callback: CallbackQuery, user_data: dict, state: FSMContext):
    lang = user_data['language']
    
    if user_data['energy'] < 10:
        await callback.answer(
            "Not enough energy! Need 10 ⚡" if lang == 'en' else "Недостаточно энергии! Нужно 10 ⚡",
            show_alert=True
        )
        return
    
    await update_user(user_data['user_id'], energy=user_data['energy'] - 10)
    
    await callback.message.edit_text(
        get_text(lang, 'minigame_sparks'),
        parse_mode='MarkdownV2'
    )
    
    await callback.answer()
    
    await asyncio.sleep(1)
    
    sparks_caught = 0
    
    for i in range(5):
        sparks = random.randint(1, 3)
        sparks_caught += sparks
        
        spark_text = "✨ " * sparks + "\n\nClick them fast! ⚡"
        
        await callback.message.answer(spark_text)
        await asyncio.sleep(2)
    
    await update_user_sparks(user_data['user_id'], sparks_caught)
    
    new_energy = max(0, user_data['energy'] - 10)
    
    await callback.message.answer(
        get_text(
            lang,
            'minigame_result',
            sparks=sparks_caught,
            energy=new_energy
        ),
        parse_mode='MarkdownV2'
    )


@router.callback_query(F.data == "game_soon")
async def game_soon(callback: CallbackQuery, user_data: dict):
    lang = user_data['language']
    
    await callback.answer(
        "More games coming soon! 🎮" if lang == 'en' else "Больше игр скоро! 🎮",
        show_alert=True
    )
