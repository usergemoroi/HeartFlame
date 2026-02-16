from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.inline import get_back_to_menu_keyboard
from database.crud import get_user_streaks
from utils.text import escape_markdown

router = Router()


@router.callback_query(F.data == "menu_friends")
async def show_friends(callback: CallbackQuery, user_data: dict):
    lang = user_data['language']
    
    streaks = await get_user_streaks(user_data['user_id'])
    
    if not streaks:
        text = "👥 *Friends*\n\nNo friends yet\\! Light flames to make friends 🔥" if lang == 'en' else "👥 *Друзья*\n\nПока нет друзей\\! Зажги огоньки, чтобы найти друзей 🔥"
    else:
        friends_list = ""
        for i, streak in enumerate(streaks, 1):
            friends_list += f"{i}\\. {streak['friend_avatar']} *{escape_markdown(streak['friend_nickname'])}* \\- {streak['days']} days 🔥\n"
        
        text = f"👥 *Friends* \\({len(streaks)}\\)\n\n{friends_list}" if lang == 'en' else f"👥 *Друзья* \\({len(streaks)}\\)\n\n{friends_list}"
    
    await callback.message.edit_text(
        text,
        reply_markup=get_back_to_menu_keyboard(lang),
        parse_mode='MarkdownV2'
    )
    
    await callback.answer()
