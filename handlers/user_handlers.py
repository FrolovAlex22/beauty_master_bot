from aiogram import F, Router
from aiogram.types import ReplyKeyboardRemove
from aiogram.filters import Command, CommandStart, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import CallbackQuery, Message, FSInputFile
from sqlalchemy.ext.asyncio import AsyncSession
# from filters.filters import IsDigitCallbackData
# from keyboards.inlines_kb import create_calendar_keyboard, create_product_keyboard
# from keyboards.choise_kb import calendar_choise_ketboard
from database.methods import orm_add_record, orm_get_records, orm_get_record, orm_delete_record, orm_update_record
from keyboards.reply import get_keyboard
from keyboards.inline import get_callback_btns
from lexicon.lexicon_ru import (
    LEXICON,
    LEXICON_CALENDAR,
    LEXICON_MATERIAL,
    LEXICON_NOTES
)
# from database.database import library_of_articles, products_in_sale

router = Router()


ADMIN_KB = get_keyboard(
        "Календарь записей",
        "Мои материалы",
        "Заметки для соц. сетей",
        "Мастера города",
        placeholder="Выберите действие",
        sizes=(1, ),
)

CHANGE_KB = get_keyboard(
        "Оставить как есть",
        "Вернуться на шаг назад",
        sizes=(1, ),
)


RECORD_KB = get_keyboard(
    "Добавить запись",
    "Мои записи",
    "Главное меню",
    sizes=(1, )
)

@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(f"Hello, {message.from_user.full_name}!")
    await message.answer(
        text=LEXICON[message.text], reply_markup=ADMIN_KB
    )


@router.message(Command(commands="help"))
async def process_help_command(message: Message):
    await message.answer(LEXICON[message.text])


@router.message(Command(commands="main_menu"))
@router.message(F.text == "Главное меню")
async def process_main_menu_command(message: Message, state: FSMContext):
    if state:
        await state.clear()
    await message.answer(
        LEXICON["/main_menu"],
        reply_markup=ADMIN_KB
    )

@router.message(Command(commands="calendar"))
@router.message(F.text == "Календарь записей")
async def calendar_menu(message: Message):
    await message.answer(
            text=LEXICON["select_action"],
            reply_markup=RECORD_KB
        )


@router.message(Command(commands="material"))
@router.message(F.text == "Мои материалы")
async def material_menu(message: Message):
    await message.answer(
        text=LEXICON['select_action'],
        reply_markup=get_keyboard(
            "Добавить новую позицию в базу данных",
            "Спиок материалов",
            "Список для покупки",
            "Главное меню",
            placeholder="Выберите действие",
            sizes=(1, )
        )
    )



@router.message(Command(commands="notes"))
@router.message(F.text == "Заметки для соц. сетей")
async def calendar_menu(message: Message):
    await message.answer(
        text=LEXICON['select_action'],
        reply_markup=get_keyboard(
            "Добавить новую заметку",
            "Посмотреть список заметок",
            "Главное меню",
            sizes=(1, )
            )
        )


@router.message(Command(commands="check"))
@router.message(F.text == "Мастера города")
async def calendar_menu(message: Message):
    await message.answer(text=LEXICON['pass'], reply_markup=get_keyboard(
        "Реконструкция волос",
        "Маникюр",
        "Ресницы",
        sizes=(1, )
        )
    )
