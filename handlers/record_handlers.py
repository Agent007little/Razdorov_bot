import aiohttp
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiohttp import ClientConnectorError

from database.database import get_phone_from_db, save_record_in_db

from config_data.logger_config import setup_logger

from lexicon.lexicon import BOT_RECORD_TEXT

logger = setup_logger(__name__)

router = Router()


# Хэндлер выводит список подарков пользователя в виде инлайн клавиатуры.
@router.callback_query(F.data == "record")
async def record_check(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    phone = await get_phone_from_db(chat_id)  # Получаем номер телефона из БД

    json_data = {"chatId": chat_id, "phone": phone}

    # запрос на сервер
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post('https://example/api/endpoint', json=json_data) as response:
                response_data = await response.json()

                # Успешный запрос
                if response_data.get("Consultation"):
                    # сохраняем в бд, что клиент записался на консультацию
                    await save_record_in_db(chat_id)

                    await callback.message.answer(BOT_RECORD_TEXT["Consultation_True"])

                # Ошибка запроса
                else:
                    # Логируем ошибку
                    error_message = response_data.get("Error", "Неизвестная ошибка")
                    user = callback.from_user.full_name
                    logger.warning(f"Ошибка записи на консультацию User: {user} - Error: {error_message}")

                    await callback.message.answer(BOT_RECORD_TEXT["Consultation_False"])
        except ClientConnectorError as e:
            print(f"Error: {e} Нет подключения к серверу")
    await callback.answer()
