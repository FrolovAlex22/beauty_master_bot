from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import CallbackQuery, Message, FSInputFile
# from filters.filters import IsDigitCallbackData
# from keyboards.inlines_kb import create_calendar_keyboard, create_product_keyboard
from keyboards.main_kb import start_no_kb
from keyboards.choise_kb import calendar_choise_ketboard
from lexicon.lexicon_ru import LEXICON, LEXICON_BUTTONS
# from database.database import library_of_articles, products_in_sale

router = Router()

class Registration(StatesGroup):
    choosing_name = State()
    choosing_password = State()


@router.message(Command(commands='registration'))
async def process_help_command(message: Message):
    await message.answer(LEXICON[message.text])