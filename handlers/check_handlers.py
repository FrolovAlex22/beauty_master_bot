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

from database.engine import session_maker
from keyboards.reply import get_keyboard
from keyboards.inline import get_callback_btns
from keyboards.other_kb import ADMIN_KB, RECORD_KB
from lexicon.lexicon_ru import (
    LEXICON,
    LEXICON_CALENDAR,
    LEXICON_MATERIAL,
    LEXICON_NOTES
)
from middlewares.db import DataBaseSession


check_router = Router()


check_router.message.middleware(DataBaseSession(session_pool=session_maker))
check_router.callback_query.middleware(DataBaseSession(session_pool=session_maker))


@check_router.message(F.text == "Реконструкция волос")
async def material_add_position(message: Message):
    await message.answer(text=LEXICON['pass'], reply_markup=ADMIN_KB)


@check_router.message(F.text == "Маникюр")
async def material_add_position(message: Message):
    await message.answer(text=LEXICON['pass'], reply_markup=ADMIN_KB)


@check_router.message(F.text == "Ресницы")
async def material_add_position(message: Message):
    await message.answer(text=LEXICON['pass'], reply_markup=ADMIN_KB)
