import asyncio
import logging

from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

from config_data.config import Config, load_config
from database.engine import create_db, drop_db
from handlers import other_handlers, user_handlers #form_handlers,
from keyboards.main_menu import set_main_menu

# Инициализируем логгер
logger = logging.getLogger(__name__)

config: Config = load_config()

bot = Bot(
    token=config.tg_bot.token,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()


async def on_startup(bot):

    run_param = True
    if run_param:
        await drop_db()

    await create_db()


async def on_shutdown(bot):
    print('бот лег')

# Функция конфигурирования и запуска бота
async def main():

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    await set_main_menu(bot)

    # Регистрируем роутеры в диспетчере
    dp.include_router(user_handlers.router)
    # dp.include_router(form_handlers.router)
    dp.include_router(other_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
    logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
            '[%(asctime)s] - %(name)s - %(message)s'
        )

    logger.info('Starting bot')