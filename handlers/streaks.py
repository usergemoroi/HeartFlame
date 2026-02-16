import asyncio
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from states.fsm import FlameStates
from keyboards.inline import (
    get_streaks_keyboard, get_streak_actions_keyboard, 
    get_flame_request_keyboard, get_back_to_menu_keyboard,
    get_revive_keyboard
)
from database.crud import (
    get_user_streaks, extend_streak, get_user_by_username,
    create_flame_request, get_pending_request, accept_flame_request,
    update_user_sparks, get_streak_by_users, kill_streak,
    revive_streak, create_pet, get_user
)
from utils.text import get_text, get_streak_color, format_time_left, escape_markdown
from utils.time import get_current_timestamp, get_time_until_expiry, can_extend_streak, get_revival_cost
from config import STREAK_MILESTONES
import random

router = Router()


@router.callback_query(F.data == "menu_streaks")
async def show_streaks(callback: CallbackQuery, user_data: dict):
    lang = user_data['language']
    user_id = user_data['user_id']
    
    streaks = await get_user_streaks(user_id)
    
    if not streaks:
        await callback.message.edit_text(
            get_text(lang, 'no_streaks'),
            reply_markup=get_streaks_keyboard(lang),
            parse_mode='MarkdownV2'
        )
        await callback.answer()
        return
    
    streaks_text = ""
    for streak in streaks:
        days = streak['days']
        color_emoji, color_name = get_streak_color(days)
        time_left = get_time_until_expiry(streak['streak_expiry'])
        
        streaks_text += get_text(
            lang,
            'streak_item',
            color=color_emoji,
            days=days,
            avatar=streak['friend_avatar'],
            nickname=escape_markdown(streak['friend_nickname']),
            time_left=format_time_left(time_left, lang)
        )
    
    full_text = get_text(lang, 'streaks_list', streaks=streaks_text)
    
    await callback.message.edit_text(
        full_text,
        reply_markup=get_streaks_keyboard(lang),
        parse_mode='MarkdownV2'
    )
    
    await callback.answer()


@router.callback_query(F.data == "streak_new")
async def new_streak(callback: CallbackQuery, state: FSMContext, user_data: dict):
    lang = user_data['language']
    
    await callback.message.edit_text(
        get_text(lang, 'light_flame'),
        reply_markup=get_back_to_menu_keyboard(lang),
        parse_mode='MarkdownV2'
    )
    
    await callback.message.answer(
        get_text(lang, 'search_friend'),
        parse_mode='MarkdownV2'
    )
    
    await state.set_state(FlameStates.searching_friend)
    await callback.answer()


@router.message(FlameStates.searching_friend)
async def process_friend_search(message: Message, state: FSMContext, user_data: dict):
    lang = user_data['language']
    username = message.text.strip().replace('@', '')
    
    friend = await get_user_by_username(username)
    
    if not friend or friend['user_id'] == user_data['user_id']:
        await message.answer(
            get_text(lang, 'friend_not_found'),
            parse_mode='MarkdownV2'
        )
        return
    
    existing_streak = await get_streak_by_users(user_data['user_id'], friend['user_id'])
    if existing_streak:
        await message.answer(
            "You already have a flame with this user!" if lang == 'en' else "У вас уже есть огонёк с этим пользователем!",
            parse_mode='MarkdownV2'
        )
        await state.clear()
        return
    
    await create_flame_request(user_data['user_id'], friend['user_id'])
    
    await message.answer(
        get_text(
            lang,
            'flame_request_sent',
            avatar=friend['avatar'],
            nickname=escape_markdown(friend['nickname'])
        ),
        parse_mode='MarkdownV2'
    )
    
    try:
        friend_lang = friend['language']
        await message.bot.send_message(
            friend['user_id'],
            get_text(
                friend_lang,
                'flame_request_received',
                avatar=user_data['avatar'],
                nickname=escape_markdown(user_data['nickname'])
            ),
            reply_markup=get_flame_request_keyboard(user_data['user_id'], friend_lang),
            parse_mode='MarkdownV2'
        )
    except:
        pass
    
    await state.clear()


@router.callback_query(F.data.startswith("flame_accept_"))
async def accept_flame(callback: CallbackQuery, user_data: dict):
    from_user_id = int(callback.data.split("_")[2])
    lang = user_data['language']
    
    request = await get_pending_request(from_user_id, user_data['user_id'])
    
    if not request:
        await callback.answer("Request no longer valid" if lang == 'en' else "Запрос больше недействителен", show_alert=True)
        return
    
    await accept_flame_request(from_user_id, user_data['user_id'])
    
    from_user = await get_user(from_user_id)
    
    await callback.message.edit_text(
        get_text(
            lang,
            'flame_started',
            avatar=from_user['avatar'],
            nickname=escape_markdown(from_user['nickname'])
        ),
        parse_mode='MarkdownV2'
    )
    
    try:
        from_lang = from_user['language']
        await callback.bot.send_message(
            from_user_id,
            get_text(
                from_lang,
                'flame_started',
                avatar=user_data['avatar'],
                nickname=escape_markdown(user_data['nickname'])
            ),
            parse_mode='MarkdownV2'
        )
    except:
        pass
    
    await callback.answer()


@router.callback_query(F.data.startswith("flame_reject_"))
async def reject_flame(callback: CallbackQuery, user_data: dict):
    lang = user_data['language']
    
    await callback.message.edit_text(
        "Request declined" if lang == 'en' else "Запрос отклонён",
        parse_mode=None
    )
    
    await callback.answer()


@router.callback_query(F.data.startswith("streak_extend_"))
async def extend_streak_action(callback: CallbackQuery, user_data: dict):
    streak_id = int(callback.data.split("_")[2])
    lang = user_data['language']
    
    streaks = await get_user_streaks(user_data['user_id'])
    streak = next((s for s in streaks if s['streak_id'] == streak_id), None)
    
    if not streak:
        await callback.answer("Streak not found" if lang == 'en' else "Огонёк не найден", show_alert=True)
        return
    
    if not can_extend_streak(streak['last_update'], cooldown_hours=8):
        await callback.answer(
            "Too soon! Wait 8 hours between extensions" if lang == 'en' else "Слишком рано! Подожди 8 часов между продлениями",
            show_alert=True
        )
        return
    
    result = await extend_streak(streak_id)
    new_days = result['new_days']
    
    base_sparks = 20 + (new_days // 10) * 5
    sparks_reward = random.randint(base_sparks, base_sparks + 20)
    
    await update_user_sparks(user_data['user_id'], sparks_reward)
    
    color_emoji, color_name = get_streak_color(new_days)
    
    milestone_text = ""
    if new_days in STREAK_MILESTONES:
        milestone_text = f"🎉 *MILESTONE\\!* {new_days} days\\! \\+{sparks_reward * 2} bonus 🔥"
        await update_user_sparks(user_data['user_id'], sparks_reward * 2)
        
        if new_days == 3 and not streak.get('pet_id'):
            pet_data = await create_pet(streak_id, user_data['user_id'])
            
            await callback.message.answer(
                get_text(
                    lang,
                    'pet_hatched',
                    pet=pet_data['pet_emoji'],
                    pet_name=escape_markdown(pet_data['pet_name'])
                ),
                parse_mode='MarkdownV2'
            )
    
    await callback.message.edit_text(
        get_text(
            lang,
            'flame_extended',
            color=color_emoji,
            days=new_days,
            avatar=streak['friend_avatar'],
            nickname=escape_markdown(streak['friend_nickname']),
            sparks=sparks_reward,
            milestone=milestone_text
        ),
        parse_mode='MarkdownV2'
    )
    
    friend_data = await get_user(streak['friend_id'])
    if friend_data:
        try:
            friend_lang = friend_data['language']
            await callback.bot.send_message(
                streak['friend_id'],
                get_text(
                    friend_lang,
                    'flame_extended',
                    color=color_emoji,
                    days=new_days,
                    avatar=user_data['avatar'],
                    nickname=escape_markdown(user_data['nickname']),
                    sparks=sparks_reward,
                    milestone=milestone_text
                ),
                parse_mode='MarkdownV2'
            )
        except:
            pass
    
    await callback.answer()


@router.callback_query(F.data.startswith("revive_confirm_"))
async def revive_streak_action(callback: CallbackQuery, user_data: dict):
    streak_id = int(callback.data.split("_")[2])
    lang = user_data['language']
    
    streaks = await get_user_streaks(user_data['user_id'], status='dead')
    streak = next((s for s in streaks if s['streak_id'] == streak_id), None)
    
    if not streak:
        await callback.answer("Streak not found" if lang == 'en' else "Огонёк не найден", show_alert=True)
        return
    
    now = get_current_timestamp()
    hours_passed = (now - streak['died_at']) / 3600
    
    if hours_passed > 168:
        await callback.answer(
            "Too late to revive!" if lang == 'en' else "Слишком поздно для воскрешения!",
            show_alert=True
        )
        return
    
    cost = get_revival_cost(int(hours_passed))
    
    if user_data['stars'] < cost:
        await callback.answer(
            f"Need {cost} ⭐ stars!" if lang == 'en' else f"Нужно {cost} ⭐ звёзд!",
            show_alert=True
        )
        return
    
    success = await revive_streak(streak_id)
    
    if not success:
        await callback.answer(
            get_text(lang, 'revive_no_lives'),
            show_alert=True
        )
        return
    
    await update_user_sparks(user_data['user_id'], -cost)
    
    await callback.message.edit_text(
        get_text(
            lang,
            'revive_success',
            avatar=streak['friend_avatar'],
            nickname=escape_markdown(streak['friend_nickname']),
            lives=streak['lives_left'] - 1
        ),
        parse_mode='MarkdownV2'
    )
    
    await callback.answer()
