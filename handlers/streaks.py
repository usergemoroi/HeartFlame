from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from database import Database
from states import StreakStates
from keyboards.inline import (
    get_streaks_keyboard,
    get_streak_actions_keyboard,
    get_streak_request_keyboard,
    get_back_keyboard
)
from locales import get_text
from utils.time_utils import format_time_left
from config.constants import STREAK_COLORS, EXTEND_SPARK_REWARD, STREAK_MILESTONES
from datetime import datetime, timedelta
import structlog

logger = structlog.get_logger()
router = Router()
db = Database()


def get_streak_color(days: int) -> str:
    for threshold in sorted(STREAK_COLORS.keys(), reverse=True):
        if days >= threshold:
            return STREAK_COLORS[threshold]
    return "🔴"


@router.callback_query(F.data == "menu_streaks")
@router.message(Command("streaks"))
async def show_streaks(event, state: FSMContext = None):
    if isinstance(event, CallbackQuery):
        user_id = event.from_user.id
        message = event.message
        is_callback = True
    else:
        user_id = event.from_user.id
        message = event
        is_callback = False
    
    streaks = await db.get_user_streaks(user_id)
    
    if not streaks:
        text = get_text("no_streaks", user_id)
        keyboard = get_streaks_keyboard(has_streaks=False)
    else:
        streaks_text = ""
        for streak in streaks:
            friend_id = streak['user2_id'] if streak['user1_id'] == user_id else streak['user1_id']
            friend_name = streak['user2_name'] if streak['user1_id'] == user_id else streak['user1_name']
            
            color = get_streak_color(streak['days'])
            expiry = datetime.fromisoformat(streak['expiry'])
            time_left = format_time_left(expiry)
            
            streaks_text += get_text(
                "streak_item",
                user_id,
                color=color,
                friend_name=friend_name,
                days=streak['days'],
                time_left=time_left
            )
        
        text = get_text("streaks_list", user_id, count=len(streaks), streaks_text=streaks_text)
        keyboard = get_streaks_keyboard(has_streaks=True)
    
    if is_callback:
        await message.edit_text(text, reply_markup=keyboard, parse_mode="MarkdownV2")
        await event.answer()
    else:
        await message.answer(text, reply_markup=keyboard, parse_mode="MarkdownV2")
    
    if state:
        await state.clear()


@router.callback_query(F.data == "streak_new")
async def start_new_streak(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    
    await callback.message.answer(
        get_text("search_friend", user_id),
        reply_markup=get_back_keyboard("menu_streaks")
    )
    await state.set_state(StreakStates.searching_friend)
    await callback.answer()


@router.message(StreakStates.searching_friend)
async def process_friend_search(message: Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.text.strip().lstrip("@")
    
    if not username:
        await message.answer("❌ Неверный формат. Введи @username:")
        return
    
    friend = await db.get_user_by_username(username)
    
    if not friend:
        await message.answer(get_text("user_not_found", user_id))
        return
    
    if friend['user_id'] == user_id:
        await message.answer(get_text("cant_streak_yourself", user_id))
        return
    
    existing_streak = await db.get_streak(user_id, friend['user_id'])
    if existing_streak:
        await message.answer(get_text("streak_already_exists", user_id))
        return
    
    existing_request = await db.get_pending_request(user_id, friend['user_id'])
    if existing_request:
        await message.answer("⏳ Запрос уже отправлен. Жди ответа!")
        return
    
    reverse_request = await db.get_pending_request(friend['user_id'], user_id)
    if reverse_request:
        await db.update_request_status(reverse_request['id'], 'accepted')
        streak_id = await db.create_streak(user_id, friend['user_id'])
        
        await message.answer(
            get_text("streak_accepted", user_id, name=friend['username']),
            parse_mode="MarkdownV2"
        )
        
        try:
            from main import bot
            await bot.send_message(
                friend['user_id'],
                get_text("streak_accepted", friend['user_id'], name=message.from_user.username or "друг"),
                parse_mode="MarkdownV2"
            )
        except Exception as e:
            logger.error("failed_to_notify_friend", error=str(e))
        
        await state.clear()
        return
    
    request_id = await db.create_streak_request(user_id, friend['user_id'])
    
    await message.answer(
        get_text("streak_request_sent", user_id, name=friend['username']),
        parse_mode="MarkdownV2"
    )
    
    user = await db.get_user(user_id)
    try:
        from main import bot
        await bot.send_message(
            friend['user_id'],
            get_text("streak_request", friend['user_id'], from_name=user['username']),
            reply_markup=get_streak_request_keyboard(request_id),
            parse_mode="MarkdownV2"
        )
    except Exception as e:
        logger.error("failed_to_send_request", error=str(e))
    
    await state.clear()


@router.callback_query(F.data.startswith("streak_accept_"))
async def accept_streak_request(callback: CallbackQuery):
    user_id = callback.from_user.id
    request_id = int(callback.data.split("_")[2])
    
    async with await db.get_connection() as conn:
        cursor = await conn.execute(
            "SELECT * FROM streak_requests WHERE id = ? AND status = 'pending'",
            (request_id,)
        )
        request = await cursor.fetchone()
    
    if not request:
        await callback.answer("❌ Запрос не найден", show_alert=True)
        return
    
    if request['to_user_id'] != user_id:
        await callback.answer("❌ Это не твой запрос", show_alert=True)
        return
    
    from_user = await db.get_user(request['from_user_id'])
    
    await db.update_request_status(request_id, 'accepted')
    streak_id = await db.create_streak(request['from_user_id'], user_id)
    
    await callback.message.edit_text(
        get_text("streak_accepted", user_id, name=from_user['username']),
        parse_mode="MarkdownV2"
    )
    
    try:
        from main import bot
        await bot.send_message(
            request['from_user_id'],
            get_text("streak_accepted", request['from_user_id'], name=callback.from_user.username or "друг"),
            parse_mode="MarkdownV2"
        )
    except Exception as e:
        logger.error("failed_to_notify_requester", error=str(e))
    
    await callback.answer("✅ Огонёк зажжён!")


@router.callback_query(F.data.startswith("streak_reject_"))
async def reject_streak_request(callback: CallbackQuery):
    user_id = callback.from_user.id
    request_id = int(callback.data.split("_")[2])
    
    async with await db.get_connection() as conn:
        cursor = await conn.execute(
            "SELECT * FROM streak_requests WHERE id = ? AND status = 'pending'",
            (request_id,)
        )
        request = await cursor.fetchone()
    
    if not request:
        await callback.answer("❌ Запрос не найден", show_alert=True)
        return
    
    if request['to_user_id'] != user_id:
        await callback.answer("❌ Это не твой запрос", show_alert=True)
        return
    
    from_user = await db.get_user(request['from_user_id'])
    
    await db.update_request_status(request_id, 'rejected')
    
    await callback.message.edit_text(
        get_text("streak_rejected", user_id, name=from_user['username']),
        parse_mode="MarkdownV2"
    )
    
    try:
        from main import bot
        await bot.send_message(
            request['from_user_id'],
            get_text("streak_rejected", request['from_user_id'], name=callback.from_user.username or "друг"),
            parse_mode="MarkdownV2"
        )
    except Exception as e:
        logger.error("failed_to_notify_requester", error=str(e))
    
    await callback.answer("❌ Отклонено")


@router.callback_query(F.data.startswith("streak_extend_"))
async def extend_streak(callback: CallbackQuery):
    user_id = callback.from_user.id
    
    if callback.data == "streak_extend_all":
        await extend_all_streaks(callback)
        return
    
    streak_id = int(callback.data.split("_")[2])
    
    success, new_days = await db.extend_streak(streak_id, user_id)
    
    if not success:
        cooldown_time = "8 часов"
        await callback.answer(
            get_text("extend_cooldown", user_id, time=cooldown_time),
            show_alert=True
        )
        return
    
    reward = EXTEND_SPARK_REWARD + (new_days // 10) * 5
    await db.add_sparks(user_id, reward)
    
    if new_days in STREAK_MILESTONES:
        streak = await db.get_connection()
        async with streak as conn:
            cursor = await conn.execute("SELECT * FROM streaks WHERE id = ?", (streak_id,))
            streak_data = await cursor.fetchone()
        
        friend_id = streak_data['user2_id'] if streak_data['user1_id'] == user_id else streak_data['user1_id']
        friend = await db.get_user(friend_id)
        
        milestone_rewards = f"• {reward * 2} искр 🔥\n• Достижение 🏆"
        
        await callback.message.answer(
            get_text(
                "streak_milestone",
                user_id,
                friend_name=friend['username'],
                days=new_days,
                rewards=milestone_rewards
            ),
            parse_mode="MarkdownV2"
        )
        
        await db.add_sparks(user_id, reward)
        await db.add_achievement(
            user_id,
            type_="streak",
            name=f"Серия {new_days} дней",
            description=f"Поддержал огонёк {new_days} дней!",
            emoji=get_streak_color(new_days)
        )
    
    user = await db.get_user(user_id)
    if new_days > user['best_streak']:
        await db.update_user(user_id, best_streak=new_days)
    
    await callback.answer(
        get_text("extend_success", user_id, sparks=reward),
        show_alert=True
    )
    
    await show_streaks(callback)


@router.callback_query(F.data == "streak_extend_all")
async def extend_all_streaks(callback: CallbackQuery):
    user_id = callback.from_user.id
    streaks = await db.get_user_streaks(user_id)
    
    extended_count = 0
    total_reward = 0
    
    for streak in streaks:
        success, new_days = await db.extend_streak(streak['id'], user_id)
        if success:
            extended_count += 1
            reward = EXTEND_SPARK_REWARD + (new_days // 10) * 5
            total_reward += reward
    
    if extended_count == 0:
        await callback.answer("⏳ Все огоньки уже продлены недавно", show_alert=True)
        return
    
    await db.add_sparks(user_id, total_reward)
    
    await callback.answer(
        get_text("extend_all_success", user_id, sparks=total_reward, count=extended_count),
        show_alert=True
    )
    
    await show_streaks(callback)


@router.callback_query(F.data == "streak_suggest")
async def suggest_friends(callback: CallbackQuery):
    user_id = callback.from_user.id
    
    await callback.answer("💡 Функция в разработке!", show_alert=True)
