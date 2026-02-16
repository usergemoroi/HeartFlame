from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from database import Database
from states import OnboardingStates
from keyboards.inline import get_language_keyboard, get_avatar_keyboard, get_menu_keyboard
from locales import get_text, set_user_language
from config.constants import Language, STARTER_AVATARS, ONBOARDING_SPARKS, ONBOARDING_SHIELDS
import asyncio
import structlog
import random

logger = structlog.get_logger()
router = Router()
db = Database()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user = await db.get_user(user_id)
    
    args = message.text.split()[1] if len(message.text.split()) > 1 else None
    referrer_id = None
    
    if args and args.startswith("ref_"):
        try:
            referrer_id = int(args.split("_")[1])
        except (ValueError, IndexError):
            pass
    
    if user:
        await message.answer(
            get_text("menu", user_id),
            reply_markup=get_menu_keyboard(user_id),
            parse_mode="MarkdownV2"
        )
        await state.clear()
        return
    
    await state.update_data(referrer_id=referrer_id)
    
    msg1 = await message.answer(get_text("welcome_1", user_id), parse_mode="MarkdownV2")
    await asyncio.sleep(1.5)
    
    msg2 = await message.answer(get_text("welcome_2", user_id), parse_mode="MarkdownV2")
    await asyncio.sleep(1.5)
    
    await message.answer(get_text("welcome_3", user_id), parse_mode="MarkdownV2")
    await asyncio.sleep(2)
    
    await message.answer(
        get_text("choose_language", user_id),
        reply_markup=get_language_keyboard()
    )
    await state.set_state(OnboardingStates.choosing_language)


@router.callback_query(OnboardingStates.choosing_language, F.data.startswith("lang_"))
async def process_language(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    lang_code = callback.data.split("_")[1]
    
    try:
        language = Language(lang_code)
    except ValueError:
        language = Language.RU
    
    set_user_language(user_id, language)
    await state.update_data(language=language)
    
    await callback.message.edit_text(get_text("language_set", user_id))
    await asyncio.sleep(1)
    
    await callback.message.answer(get_text("ask_username", user_id))
    await state.set_state(OnboardingStates.entering_username)
    await callback.answer()


@router.message(OnboardingStates.entering_username)
async def process_username(message: Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.text.strip()
    
    if len(username) < 2 or len(username) > 30:
        await message.answer("❌ Ник должен быть от 2 до 30 символов. Попробуй ещё раз:")
        return
    
    existing = await db.get_user_by_username(username)
    if existing:
        await message.answer(get_text("username_taken", user_id))
        return
    
    await state.update_data(username=username)
    
    await message.answer(
        get_text("username_set", user_id, username),
        reply_markup=get_avatar_keyboard(),
        parse_mode="MarkdownV2"
    )
    await state.set_state(OnboardingStates.choosing_avatar)


@router.callback_query(OnboardingStates.choosing_avatar, F.data.startswith("avatar_"))
async def process_avatar(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    avatar_idx = int(callback.data.split("_")[1])
    
    if avatar_idx < 0 or avatar_idx >= len(STARTER_AVATARS):
        await callback.answer("❌ Неверный выбор", show_alert=True)
        return
    
    avatar = STARTER_AVATARS[avatar_idx]
    
    data = await state.get_data()
    username = data.get("username")
    language = data.get("language", Language.RU)
    referrer_id = data.get("referrer_id")
    
    success = await db.create_user(user_id, username, avatar, language, referrer_id)
    
    if not success:
        await callback.answer("❌ Ошибка создания пользователя", show_alert=True)
        return
    
    await db.add_sparks(user_id, ONBOARDING_SPARKS)
    await db.add_inventory_item(user_id, "shield", "basic", ONBOARDING_SHIELDS)
    
    base_pet_emoji = random.choice(["🥚"])
    await db.create_pet(user_id, "Серийчик", base_pet_emoji, "common")
    
    if referrer_id:
        await process_referral_reward(referrer_id, user_id)
    
    await callback.message.edit_text(get_text("avatar_chosen", user_id, avatar=avatar))
    await asyncio.sleep(1)
    
    await show_tutorial(callback.message, user_id, state)
    await callback.answer()


async def show_tutorial(message: Message, user_id: int, state: FSMContext):
    await message.answer(get_text("tutorial_1", user_id), parse_mode="MarkdownV2")
    await asyncio.sleep(3)
    
    await message.answer(get_text("tutorial_2", user_id), parse_mode="MarkdownV2")
    await asyncio.sleep(3)
    
    await message.answer(get_text("tutorial_3", user_id), parse_mode="MarkdownV2")
    await asyncio.sleep(2)
    
    await message.answer(
        get_text("onboarding_complete", user_id),
        reply_markup=get_menu_keyboard(user_id),
        parse_mode="MarkdownV2"
    )
    await state.clear()


async def process_referral_reward(referrer_id: int, new_user_id: int):
    referrer = await db.get_user(referrer_id)
    if not referrer:
        return
    
    referral_count = await db.get_referral_count(referrer_id)
    
    base_reward = 50
    if referral_count <= 5:
        rewards_map = {1: 50, 2: 80, 3: 120, 4: 200, 5: 350}
        base_reward = rewards_map.get(referral_count, 600)
    elif referral_count <= 10:
        base_reward = 600
    elif referral_count <= 25:
        base_reward = 800
    elif referral_count <= 50:
        base_reward = 1200
    else:
        base_reward = 1500
    
    new_user = await db.get_user(new_user_id)
    if new_user and new_user.get('is_premium'):
        base_reward *= 2
    
    await db.add_sparks(referrer_id, base_reward)
    await db.update_user(referrer_id, total_referrals=referral_count)
    
    await db.add_referral_reward(
        referrer_id,
        level=1,
        referral_count=referral_count,
        reward_type="sparks",
        reward_value=base_reward
    )
    
    logger.info(
        "referral_reward_given",
        referrer_id=referrer_id,
        new_user_id=new_user_id,
        reward=base_reward,
        count=referral_count
    )


@router.message(Command("menu"))
async def cmd_menu(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user = await db.get_user(user_id)
    
    if not user:
        await cmd_start(message, state)
        return
    
    await message.answer(
        get_text("menu", user_id),
        reply_markup=get_menu_keyboard(user_id),
        parse_mode="MarkdownV2"
    )
    await state.clear()


@router.callback_query(F.data == "menu_main")
async def show_menu(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    
    await callback.message.edit_text(
        get_text("menu", user_id),
        reply_markup=get_menu_keyboard(user_id),
        parse_mode="MarkdownV2"
    )
    await state.clear()
    await callback.answer()
