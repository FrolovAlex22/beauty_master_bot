from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.reply import get_keyboard
from keyboards.other_kb import ADMIN_KB, CHECK_KB, RECORD_KB, MATERIAL_KB, NOTE_KB
from lexicon.lexicon_ru import LEXICON

router = Router()


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


@router.message(Command(commands="records"))
@router.message(F.text == "Календарь записей")
async def calendar_menu(message: Message):
    await message.answer(
            text=LEXICON["select_action"],
            reply_markup=RECORD_KB
        )


@router.message(Command(commands="materials"))
@router.message(F.text == "Мои материалы")
async def material_menu(message: Message):
    await message.answer(
        text=LEXICON['select_action'],
        reply_markup=MATERIAL_KB
    )


@router.message(Command(commands="notes"))
@router.message(F.text == "Заметки для соц. сетей")
async def calendar_menu(message: Message):
    await message.answer(
        text=LEXICON['select_action'],
        reply_markup=NOTE_KB
        )


@router.message(Command(commands="check"))
@router.message(F.text == "Мастера города")
async def calendar_menu(message: Message):
    await message.answer(text=LEXICON['check_list'], reply_markup=CHECK_KB)
