from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.inline import get_leaderboard_keyboard, get_back_to_menu_keyboard
from database.crud import get_leaderboard, get_user_rank
from utils.text import get_text, escape_markdown

router = Router()


@router.callback_query(F.data == "menu_leaderboard")
async def show_leaderboard(callback: CallbackQuery, user_data: dict):
    lang = user_data['language']
    
    await show_leaderboard_stat(callback, user_data, 'streak')


@router.callback_query(F.data.startswith("lb_"))
async def show_leaderboard_stat(callback: CallbackQuery, user_data: dict, stat: str = None):
    if stat is None:
        stat = callback.data.split("_")[1]
    
    lang = user_data['language']
    
    leaders = await get_leaderboard(stat, limit=10)
    user_rank = await get_user_rank(user_data['user_id'], stat)
    
    medals = ['🥇', '🥈', '🥉', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
    
    stat_names = {
        'streak': 'Max Streak' if lang == 'en' else 'Макс. серия',
        'sparks': 'Total Sparks' if lang == 'en' else 'Всего искр',
        'referrals': 'Referrals' if lang == 'en' else 'Рефералов'
    }
    
    leaders_text = ""
    for i, leader in enumerate(leaders):
        medal = medals[i] if i < len(medals) else f"{i+1}\\."
        leaders_text += get_text(
            lang,
            'leader_item',
            medal=medal,
            nickname=escape_markdown(leader['nickname']),
            avatar=leader['avatar'],
            stat=stat_names[stat],
            value=leader['value']
        )
    
    your_pos_text = f"\n\n📍 Your position: *#{user_rank}*" if lang == 'en' else f"\n\n📍 Твоя позиция: *#{user_rank}*"
    
    full_text = get_text(
        lang,
        'leaderboard',
        leaders=leaders_text,
        your_position=your_pos_text
    )
    
    await callback.message.edit_text(
        full_text,
        reply_markup=get_leaderboard_keyboard(lang),
        parse_mode='MarkdownV2'
    )
    
    await callback.answer()
