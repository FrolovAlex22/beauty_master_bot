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
from keyboards.other_kb import CHANGE_KB, ADMIN_KB, RECORD_KB
from lexicon.lexicon_ru import (
    LEXICON,
    LEXICON_CALENDAR,
    LEXICON_MATERIAL,
    LEXICON_NOTES
)
from middlewares.db import DataBaseSession


note_router = Router()


note_router.message.middleware(DataBaseSession(session_pool=session_maker))
note_router.callback_query.middleware(DataBaseSession(session_pool=session_maker))


class AddNotes(StatesGroup):
    title = State()
    description = State()
    image = State()


@note_router.message(StateFilter(None), F.text == "Добавить новую заметку")
async def notes_add(message: Message, state: FSMContext):
    await message.answer(
        LEXICON["notes_add"],
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(AddNotes.title)


@note_router.message(AddNotes.title, F.text)
async def notes_add_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer(LEXICON_NOTES["notes_add_input_description"])
    await state.set_state(AddNotes.description)


@note_router.message(AddNotes.title)
async def notes_add_title_wrong(message: Message, state: FSMContext):
    await message.answer(
        LEXICON_NOTES["notes_add_title_wrong"]
    )


@note_router.message(AddNotes.description, F.text)
async def notes_add_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer(
        LEXICON_NOTES["notes_add_input_image"],
        reply_markup=get_keyboard(
            "пропустить",
            sizes=(1, )
            )
    )
    await state.set_state(AddNotes.image)


@note_router.message(AddNotes.description)
async def notes_add_description_wrong(message: Message, state: FSMContext):
    await message.answer(LEXICON_NOTES["notes_add_description_wrong"])


@note_router.message(AddNotes.image, or_f(F.photo, F.text == "пропустить"))
async def notes_add_image(message: Message, state: FSMContext):
    if message.text == "пропустить":
        await state.update_data(image=None)
    else:
        await state.update_data(image=message.photo[-1].file_id)
    data = await state.get_data()
    if data['image']:
        await message.answer_photo(
            data['image'],
            caption=(
                f"<b>Заметка добавлена в базу данных</b>\n"
                f"Название: <b>{data['title']}\n</b>"
                f"Описание: <b>{data['description']}\n</b>"
            ),
            reply_markup=ADMIN_KB
        )
        await state.clear()
        return
    await message.answer(
        text=(
            f"<b>Заметка добавлена в базу данных</b>\n"
            f"Название: <b>{data['title']}\n</b>"
            f"Описание: <b>{data['description']}\n</b>"
            f"Изображение: <b>Отсутствует</b>"),
        reply_markup=ADMIN_KB
    )
    await state.clear()


@note_router.message(AddNotes.image)
async def notes_add_image_wrong(message: Message, state: FSMContext):
    await message.answer(
        LEXICON_NOTES["notes_add_image_wrong"],
        reply_markup=get_keyboard(
            "пропустить",
            sizes=(1, )
            )
    )


@note_router.message(F.text == "Удалить заметку")
async def material_add_position(message: Message):
    await message.answer(text=LEXICON['pass'], reply_markup=ADMIN_KB)


@note_router.message(F.text == "Посмотреть список заметок")
async def material_add_position(message: Message):
    await message.answer(text=LEXICON['pass'], reply_markup=ADMIN_KB)
