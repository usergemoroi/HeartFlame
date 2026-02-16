import asyncio
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from states.fsm import OnboardingStates
from keyboards.inline import (
    get_language_keyboard, get_avatar_keyboard, 
    get_tutorial_keyboard, get_main_menu_keyboard
)
from database.crud import create_user, get_user_by_nickname, update_user, process_referral
from utils.text import get_text, escape_markdown
from utils.time import get_current_timestamp
import re

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext, user_data: dict, is_registered: bool):
    user_id = message.from_user.id
    
    if is_registered:
        lang = user_data['language']
        await message.answer(
            get_text(lang, 'main_menu'),
            reply_markup=get_main_menu_keyboard(lang),
            parse_mode='MarkdownV2'
        )
        return
    
    args = message.text.split()
    referrer_id = None
    if len(args) > 1:
        try:
            referrer_id = int(args[1].replace('ref', ''))
        except:
            pass
    
    await state.update_data(referrer_id=referrer_id)
    
    await message.answer("✨", parse_mode=None)
    await asyncio.sleep(1)
    
    await message.answer(
        get_text('en', 'welcome_1'),
        parse_mode='MarkdownV2'
    )
    
    await asyncio.sleep(1.5)
    
    await message.answer(
        get_text('en', 'welcome_2'),
        parse_mode='MarkdownV2'
    )
    
    await asyncio.sleep(1.5)
    
    await message.answer(
        get_text('en', 'welcome_3'),
        parse_mode='MarkdownV2'
    )
    
    await asyncio.sleep(2)
    
    await message.answer(
        get_text('en', 'choose_language'),
        reply_markup=get_language_keyboard(),
        parse_mode='MarkdownV2'
    )
    
    await state.set_state(OnboardingStates.choosing_language)


@router.callback_query(F.data.startswith("lang_"), OnboardingStates.choosing_language)
async def process_language(callback: CallbackQuery, state: FSMContext):
    language = callback.data.split("_")[1]
    
    await state.update_data(language=language)
    
    await callback.message.edit_text(
        get_text(language, 'enter_nickname'),
        parse_mode='MarkdownV2'
    )
    
    await state.set_state(OnboardingStates.entering_nickname)
    await callback.answer()


@router.message(OnboardingStates.entering_nickname)
async def process_nickname(message: Message, state: FSMContext):
    nickname = message.text.strip()
    
    data = await state.get_data()
    language = data.get('language', 'en')
    
    if not re.match(r'^[a-zA-Z0-9_]{3,20}$', nickname):
        await message.answer(
            get_text(language, 'nickname_invalid'),
            parse_mode='MarkdownV2'
        )
        return
    
    existing = await get_user_by_nickname(nickname)
    if existing:
        await message.answer(
            get_text(language, 'nickname_taken'),
            parse_mode='MarkdownV2'
        )
        return
    
    await state.update_data(nickname=nickname)
    
    await message.answer(
        get_text(language, 'choose_avatar'),
        reply_markup=get_avatar_keyboard(),
        parse_mode='MarkdownV2'
    )
    
    await state.set_state(OnboardingStates.choosing_avatar)


@router.callback_query(F.data.startswith("avatar_"), OnboardingStates.choosing_avatar)
async def process_avatar(callback: CallbackQuery, state: FSMContext):
    avatar = callback.data.split("_")[1]
    
    data = await state.get_data()
    language = data.get('language', 'en')
    nickname = data['nickname']
    referrer_id = data.get('referrer_id')
    
    user_id = callback.from_user.id
    username = callback.from_user.username
    
    success = await create_user(
        user_id=user_id,
        username=username,
        nickname=nickname,
        avatar=avatar,
        language=language,
        referrer_id=referrer_id
    )
    
    if not success:
        await callback.answer("Error creating user. Please try again.", show_alert=True)
        return
    
    if referrer_id:
        reward = await process_referral(referrer_id, user_id)
        from database.crud import get_user
        referrer = await get_user(referrer_id)
        if referrer:
            try:
                from aiogram import Bot
                bot: Bot = callback.bot
                ref_lang = referrer['language']
                milestone = ""
                
                if referrer['total_referrals'] in [5, 10, 25, 50]:
                    milestone = f"🎉 Milestone: {referrer['total_referrals']} referrals!"
                
                await bot.send_message(
                    referrer_id,
                    get_text(
                        ref_lang, 
                        'new_referral',
                        avatar=avatar,
                        nickname=escape_markdown(nickname),
                        reward=reward,
                        milestone=milestone
                    ),
                    parse_mode='MarkdownV2'
                )
            except:
                pass
    
    await callback.message.edit_text(
        get_text(language, 'tutorial_1'),
        reply_markup=get_tutorial_keyboard(1, language),
        parse_mode='MarkdownV2'
    )
    
    await state.set_state(OnboardingStates.tutorial_step_1)
    await callback.answer()


@router.callback_query(F.data == "tutorial_2", OnboardingStates.tutorial_step_1)
async def tutorial_step_2(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    language = data.get('language', 'en')
    
    await callback.message.edit_text(
        get_text(language, 'tutorial_2'),
        reply_markup=get_tutorial_keyboard(2, language),
        parse_mode='MarkdownV2'
    )
    
    await state.set_state(OnboardingStates.tutorial_step_2)
    await callback.answer()


@router.callback_query(F.data == "tutorial_3", OnboardingStates.tutorial_step_2)
async def tutorial_step_3(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    language = data.get('language', 'en')
    
    await callback.message.edit_text(
        get_text(language, 'tutorial_3'),
        reply_markup=get_tutorial_keyboard(3, language),
        parse_mode='MarkdownV2'
    )
    
    await state.set_state(OnboardingStates.tutorial_step_3)
    await callback.answer()


@router.callback_query(F.data == "tutorial_complete")
async def tutorial_complete(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    language = data.get('language', 'en')
    user_id = callback.from_user.id
    
    await update_user(user_id, tutorial_completed=True)
    
    await callback.message.edit_text(
        get_text(language, 'bonus_received'),
        parse_mode='MarkdownV2'
    )
    
    await asyncio.sleep(2)
    
    await callback.message.answer(
        get_text(language, 'main_menu'),
        reply_markup=get_main_menu_keyboard(language),
        parse_mode='MarkdownV2'
    )
    
    await state.clear()
    await callback.answer()


@router.message(Command("menu"))
async def cmd_menu(message: Message, user_data: dict, is_registered: bool):
    if not is_registered:
        await message.answer("Please start the bot first with /start")
        return
    
    lang = user_data['language']
    await message.answer(
        get_text(lang, 'main_menu'),
        reply_markup=get_main_menu_keyboard(lang),
        parse_mode='MarkdownV2'
    )


@router.callback_query(F.data == "menu_main")
async def menu_main(callback: CallbackQuery, user_data: dict):
    lang = user_data['language']
    
    await callback.message.edit_text(
        get_text(lang, 'main_menu'),
        reply_markup=get_main_menu_keyboard(lang),
        parse_mode='MarkdownV2'
    )
    
    await callback.answer()
