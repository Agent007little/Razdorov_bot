import asyncio

from aiogram import Bot, Dispatcher

from database.database import init_db

from config_data.logger_config import setup_logger
from handlers import commands_handlers, gifts_handlers, record_handlers

from config_data.config import Config, load_config

# Инициализируем логгер
logger = setup_logger(__name__)


async def main():
    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')

    # Загружаем конфиг в переменную config
    config: Config = load_config()

    # Инициализируем бот, диспетчер
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher()

    # Инициализация базы данных.
    init_db(force=True)

    # Регистриуем роутеры в диспетчере
    dp.include_router(commands_handlers.router)
    dp.include_router(gifts_handlers.router)
    dp.include_router(record_handlers.router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
