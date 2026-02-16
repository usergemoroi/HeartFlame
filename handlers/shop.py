from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from database import Database
from keyboards.inline import get_shop_keyboard, get_shop_items_keyboard, get_back_keyboard
from locales import get_text
from config.constants import SHOP_ITEMS
import structlog

logger = structlog.get_logger()
router = Router()
db = Database()


@router.callback_query(F.data == "menu_shop")
@router.message(Command("shop"))
async def show_shop(event):
    if isinstance(event, CallbackQuery):
        user_id = event.from_user.id
        message = event.message
        is_callback = True
    else:
        user_id = event.from_user.id
        message = event
        is_callback = False
    
    user = await db.get_user(user_id)
    
    text = get_text("shop", user_id, sparks=user['sparks'], stars=user['stars'])
    keyboard = get_shop_keyboard()
    
    if is_callback:
        await message.edit_text(text, reply_markup=keyboard, parse_mode="MarkdownV2")
        await event.answer()
    else:
        await message.answer(text, reply_markup=keyboard, parse_mode="MarkdownV2")


@router.callback_query(F.data.startswith("shop_"))
async def show_shop_category(callback: CallbackQuery):
    user_id = callback.from_user.id
    category = callback.data.split("_")[1]
    
    if category == "boosts":
        keyboard = get_shop_items_keyboard("boosts")
    elif category == "pets":
        keyboard = get_shop_items_keyboard("egg")
    elif category == "custom":
        await callback.answer("✨ Скоро будет доступно!", show_alert=True)
        return
    elif category == "gifts":
        keyboard = get_shop_items_keyboard("gifts")
    else:
        await callback.answer("❌ Неизвестная категория", show_alert=True)
        return
    
    await callback.message.edit_text(
        "🛒 **Выбери товар:**",
        reply_markup=keyboard,
        parse_mode="MarkdownV2"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("buy_"))
async def buy_item(callback: CallbackQuery):
    user_id = callback.from_user.id
    item_id = callback.data.replace("buy_", "")
    
    if item_id not in SHOP_ITEMS:
        await callback.answer("❌ Товар не найден", show_alert=True)
        return
    
    item = SHOP_ITEMS[item_id]
    user = await db.get_user(user_id)
    
    if item['currency'] == 'sparks':
        if user['sparks'] < item['price']:
            await callback.answer(get_text("not_enough_sparks", user_id), show_alert=True)
            return
        await db.add_sparks(user_id, -item['price'])
    else:
        if user['stars'] < item['price']:
            await callback.answer("😢 Недостаточно звёзд!", show_alert=True)
            return
        await db.add_stars(user_id, -item['price'])
    
    await db.add_inventory_item(user_id, "item", item_id, 1)
    
    await callback.answer(
        get_text("item_bought", user_id, item=item['name']),
        show_alert=True
    )
    
    logger.info("item_purchased", user_id=user_id, item_id=item_id, price=item['price'])


@router.callback_query(F.data == "menu_friends")
async def show_friends(callback: CallbackQuery):
    user_id = callback.from_user.id
    
    await callback.answer("👥 Список друзей скоро будет доступен!", show_alert=True)
