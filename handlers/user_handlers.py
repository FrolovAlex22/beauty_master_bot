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

@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(LEXICON[message.text], reply_markup=start_no_kb)

@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(LEXICON[message.text])

@router.message(Command(commands='calendar'))
@router.message(F.text == LEXICON_BUTTONS['calendar_button'])
async def calendar_menu(message: Message):
    await message.answer(
            text=LEXICON['select_action'],
            reply_markup=calendar_choise_ketboard
        )


@router.message(F.text == LEXICON['add_or_delete_reception'])
async def add_or_delete_reception(message: Message):
    await message.answer(text=LEXICON['pass'], reply_markup=start_no_kb)


@router.message(F.text == LEXICON['add_reception'])
async def calendar_add_reception(message: Message):
    await message.answer(text=LEXICON['pass'], reply_markup=start_no_kb)


@router.message(F.text == LEXICON['delete_reception'])
async def calendar_add_reception(message: Message):
    await message.answer(text=LEXICON['pass'], reply_markup=start_no_kb)


@router.message(F.text == LEXICON['reception_list'])
async def calendar_reception_list(message: Message):
    await message.answer(text=LEXICON['pass'], reply_markup=start_no_kb)


@router.message(Command(commands='material'))
@router.message(F.text == LEXICON_BUTTONS['material_button'])
async def material_menu(message: Message):
    await message.answer(text=LEXICON['pass'], reply_markup=start_no_kb)


@router.message(F.text == LEXICON['add_or_delete_position'])
async def material_add_position(message: Message):
    await message.answer(text=LEXICON['pass'], reply_markup=start_no_kb)


@router.message(Command(commands='notes'))
@router.message(F.text == LEXICON_BUTTONS['notes_button'])
async def calendar_menu(message: Message):
    await message.answer(text=LEXICON['pass'], reply_markup=start_no_kb)


@router.message(Command(commands='check'))
@router.message(F.text == LEXICON_BUTTONS['check_masters_button'])
async def calendar_menu(message: Message):
    await message.answer(text=LEXICON['pass'], reply_markup=start_no_kb)
