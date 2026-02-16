from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.inline import get_shop_keyboard, get_back_to_menu_keyboard
from database.crud import update_user_sparks, update_user
from utils.text import get_text

router = Router()


@router.callback_query(F.data == "menu_shop")
async def show_shop(callback: CallbackQuery, user_data: dict):
    lang = user_data['language']
    
    await callback.message.edit_text(
        get_text(lang, 'shop', items=""),
        reply_markup=get_shop_keyboard(lang),
        parse_mode='MarkdownV2'
    )
    
    await callback.answer()


@router.callback_query(F.data == "shop_buy_shield")
async def buy_shield(callback: CallbackQuery, user_data: dict):
    lang = user_data['language']
    cost = 100
    
    if user_data['sparks'] < cost:
        await callback.answer(
            get_text(lang, 'insufficient_funds', currency='🔥', required=cost, current=user_data['sparks']),
            show_alert=True
        )
        return
    
    await update_user_sparks(user_data['user_id'], -cost)
    await update_user(user_data['user_id'], has_shield=True)
    
    await callback.answer(
        get_text(lang, 'purchase_success', emoji='🛡️', name='Flame Shield'),
        show_alert=True
    )


@router.callback_query(F.data == "shop_buy_boost")
async def buy_boost(callback: CallbackQuery, user_data: dict):
    lang = user_data['language']
    cost = 150
    
    if user_data['sparks'] < cost:
        await callback.answer(
            get_text(lang, 'insufficient_funds', currency='🔥', required=cost, current=user_data['sparks']),
            show_alert=True
        )
        return
    
    await update_user_sparks(user_data['user_id'], -cost)
    
    from utils.time import get_current_timestamp
    now = get_current_timestamp()
    
    from database.crud import get_db
    db = await get_db()
    await db.execute("""
        INSERT INTO shop_items (user_id, item_type, item_data, purchased_at, expires_at)
        VALUES (?, 'boost', 'x2_sparks', ?, ?)
    """, (user_data['user_id'], now, now + 86400))
    await db.commit()
    await db.close()
    
    await callback.answer(
        get_text(lang, 'purchase_success', emoji='💫', name='x2 Sparks Boost'),
        show_alert=True
    )


@router.callback_query(F.data.startswith("shop_buy_"))
async def buy_item(callback: CallbackQuery, user_data: dict):
    lang = user_data['language']
    
    await callback.answer(
        "Coming soon! 🛒" if lang == 'en' else "Скоро! 🛒",
        show_alert=True
    )


@router.callback_query(F.data == "shop_skins")
async def show_skins(callback: CallbackQuery, user_data: dict):
    lang = user_data['language']
    
    await callback.answer(
        "Pet skins coming soon! 🎨" if lang == 'en' else "Скины питомцев скоро! 🎨",
        show_alert=True
    )
