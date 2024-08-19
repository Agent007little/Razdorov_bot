import os

from aiogram import Router, F, types
from aiogram.types import CallbackQuery

from keyboards.all_bot_kb import gifts_choice_kb
from lexicon.lexicon import BOT_MAIN_COMMANDS

router = Router()


# Хэндлер выводит список подарков пользователя в виде инлайн клавиатуры.
@router.callback_query(F.data == "gifts")
async def gifts_choice(callback: CallbackQuery):
    await callback.message.answer(BOT_MAIN_COMMANDS["get_gifts"], reply_markup=await gifts_choice_kb())
    await callback.answer()


# Хендлер возвращает подарок, если пользователь нажал на любую кнопку. Файл example.docx
@router.callback_query(F.data.in_({"gift_1", "gift_2", "gift_3", "gift_4", "gift_5", "gift_6"}))
async def send_gift(callback: CallbackQuery):
    # Получаем путь к директории, где находится текущий исполняемый файл
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Переходим на уровень выше
    parent_dir = os.path.dirname(current_dir)
    # Указываем имя файла
    file_name = "example.docx"
    # Формируем полный путь к файлу
    file_path = os.path.join(parent_dir, file_name)
    # Возвращаем файл
    await callback.message.answer_document(document=types.FSInputFile(path=file_path))
    await callback.answer()
