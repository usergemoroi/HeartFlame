from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.inline import get_gifts_keyboard, get_back_to_menu_keyboard
from database.crud import get_user_streaks, send_gift, update_user_sparks, get_user
from utils.text import get_text, escape_markdown
from config import GIFT_ITEMS

router = Router()


@router.callback_query(F.data == "menu_gifts")
async def show_gifts_menu(callback: CallbackQuery, user_data: dict):
    lang = user_data['language']
    
    text = "🎁 *Gifts Menu*\n\nChoose a friend to send a gift:" if lang == 'en' else "🎁 *Меню подарков*\n\nВыбери друга для отправки подарка:"
    
    streaks = await get_user_streaks(user_data['user_id'])
    
    if not streaks:
        await callback.message.edit_text(
            "No friends yet! Light flames first 🔥" if lang == 'en' else "Пока нет друзей! Сначала зажги огоньки 🔥",
            reply_markup=get_back_to_menu_keyboard(lang),
            parse_mode='MarkdownV2'
        )
        await callback.answer()
        return
    
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    builder = InlineKeyboardBuilder()
    
    for streak in streaks[:10]:
        builder.button(
            text=f"{streak['friend_avatar']} {streak['friend_nickname']}",
            callback_data=f"gift_choose_{streak['friend_id']}"
        )
    
    back_text = "🏠 Main Menu" if lang == 'en' else "🏠 Главное меню"
    builder.button(text=back_text, callback_data="menu_main")
    
    builder.adjust(2)
    
    await callback.message.edit_text(
        text,
        reply_markup=builder.as_markup(),
        parse_mode='MarkdownV2'
    )
    
    await callback.answer()


@router.callback_query(F.data.startswith("gift_choose_"))
async def choose_gift_for_friend(callback: CallbackQuery, user_data: dict):
    friend_id = int(callback.data.split("_")[2])
    lang = user_data['language']
    
    friend = await get_user(friend_id)
    
    if not friend:
        await callback.answer("Friend not found" if lang == 'en' else "Друг не найден", show_alert=True)
        return
    
    text = f"🎁 Choose a gift for {friend['avatar']} *{escape_markdown(friend['nickname'])}*:" if lang == 'en' else f"🎁 Выбери подарок для {friend['avatar']} *{escape_markdown(friend['nickname'])}*:"
    
    await callback.message.edit_text(
        text,
        reply_markup=get_gifts_keyboard(friend_id, lang),
        parse_mode='MarkdownV2'
    )
    
    await callback.answer()


@router.callback_query(F.data.startswith("gift_send_"))
async def send_gift_action(callback: CallbackQuery, user_data: dict):
    parts = callback.data.split("_")
    friend_id = int(parts[2])
    gift_type = parts[3]
    
    lang = user_data['language']
    
    gift_data = GIFT_ITEMS.get(gift_type)
    
    if not gift_data:
        await callback.answer("Invalid gift" if lang == 'en' else "Неверный подарок", show_alert=True)
        return
    
    cost = gift_data['sparks']
    
    if user_data['sparks'] < cost:
        await callback.answer(
            f"Not enough sparks! Need {cost} 🔥" if lang == 'en' else f"Недостаточно искр! Нужно {cost} 🔥",
            show_alert=True
        )
        return
    
    await update_user_sparks(user_data['user_id'], -cost)
    await send_gift(user_data['user_id'], friend_id, gift_type, str(gift_data))
    
    friend = await get_user(friend_id)
    
    if gift_type == 'cake':
        await update_user_sparks(friend_id, 50)
        effect = "+50 🔥 sparks" if lang == 'en' else "+50 🔥 искр"
    elif gift_type == 'bouquet':
        await update_user_sparks(friend_id, 40)
        effect = "+40 🔥 sparks" if lang == 'en' else "+40 🔥 искр"
    else:
        effect = gift_data['description']
    
    await callback.message.edit_text(
        get_text(
            lang,
            'gift_sent',
            emoji=gift_data['emoji'],
            name=gift_data['name'],
            avatar=friend['avatar'],
            nickname=escape_markdown(friend['nickname']),
            effect=effect
        ),
        parse_mode='MarkdownV2'
    )
    
    try:
        friend_lang = friend['language']
        await callback.bot.send_message(
            friend_id,
            get_text(
                friend_lang,
                'gift_received',
                emoji=gift_data['emoji'],
                name=gift_data['name'],
                avatar=user_data['avatar'],
                nickname=escape_markdown(user_data['nickname']),
                effect=effect
            ),
            parse_mode='MarkdownV2'
        )
    except:
        pass
    
    await callback.answer()


@router.callback_query(F.data.startswith("streak_gift_"))
async def gift_from_streak(callback: CallbackQuery, user_data: dict):
    streak_id = int(callback.data.split("_")[2])
    lang = user_data['language']
    
    streaks = await get_user_streaks(user_data['user_id'])
    streak = next((s for s in streaks if s['streak_id'] == streak_id), None)
    
    if not streak:
        await callback.answer("Streak not found" if lang == 'en' else "Огонёк не найден", show_alert=True)
        return
    
    await choose_gift_for_friend(callback, user_data)
