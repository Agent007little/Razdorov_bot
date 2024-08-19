from aiogram.types import InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import BOT_INLINE_TEXT, BOT_GIFTS_TEXT


# Функция, генерирующая инлайн кнопку, поделиться телефоном.
async def share_phone_kb():
    first_button = [[KeyboardButton(text=BOT_INLINE_TEXT["share_phone"], request_contact=True)], ]
    keyboard = ReplyKeyboardMarkup(keyboard=first_button, resize_keyboard=True)
    return keyboard


# Основной выбор Подарки или Запись.
async def gift_or_record_kb():
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(InlineKeyboardButton(text=BOT_INLINE_TEXT["gift"], callback_data="gifts"),
                   InlineKeyboardButton(text=BOT_INLINE_TEXT["record"], callback_data="record"),
                   width=2)
    return kb_builder.as_markup()


# Клавиатура со списком подарков
async def gifts_choice_kb():
    kb_builder = InlineKeyboardBuilder()
    for key, value in BOT_GIFTS_TEXT.items():
        kb_builder.row(InlineKeyboardButton(text=value, callback_data=f"gift_{key}"))

    return kb_builder.as_markup()
