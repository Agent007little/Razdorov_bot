from aiogram import Router, types, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message

from States.States import FSMDefaultChoice
from database.database import save_user

from keyboards.all_bot_kb import share_phone_kb, gift_or_record_kb
from lexicon.lexicon import BOT_MAIN_COMMANDS

router = Router()


# Этот хэндлер будет срабатывать на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(BOT_MAIN_COMMANDS[message.text], reply_markup=await share_phone_kb())
    # Сделать добавление нового пользователя в БД при начале общения с ботом.
    await save_user(int(message.chat.id))


# Хендлер срабатывает, когда пользователь нажимает инлайн кнопку "Поделиться телефоном"
@router.message(F.contact, StateFilter(default_state))
async def get_contact(message: types.Message, state: FSMContext):
    contact = message.contact
    await message.answer(f"Спасибо, {contact.first_name}.\n"
                         f"Ваш номер {contact.phone_number} был получен",
                         reply_markup=await gift_or_record_kb())
    await state.set_state(FSMDefaultChoice.choice) # Переводим в состояние выбора подарка или консультации


# Команда help. Возвращает выбор подарок или запись на приём.
@router.message(Command(commands="help"))
async def process_start_command(message: Message, state: FSMContext):
    await message.answer(BOT_MAIN_COMMANDS["/help"], reply_markup=await gift_or_record_kb())
    await state.set_state(FSMDefaultChoice.choice) # Переводим в состояние выбора подарка или консультации


# Хэндлер срабатывает на неизвестные команды от пользователя
@router.message(StateFilter(default_state))
async def process_unknown_command(message: Message):
    await message.answer(BOT_MAIN_COMMANDS["unknown_command"])
