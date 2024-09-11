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


material_router = Router()


material_router.message.middleware(DataBaseSession(session_pool=session_maker))
material_router.callback_query.middleware(DataBaseSession(session_pool=session_maker))


class AddMaterial(StatesGroup):
    # Шаги состояний
    title = State()
    description = State()
    photo = State()
    packing = State()
    price = State()
    quantity = State()

    material_for_change = None


@material_router.message(
        StateFilter(None),
        F.text == "Добавить новую позицию в базу данных"
    )
async def material_add_position(message: Message, state: FSMContext):
    await message.answer(
        LEXICON["material_add"],
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(AddMaterial.title)


@material_router.message(AddMaterial.title, F.text)
async def material_add_position_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer(LEXICON_MATERIAL["material_add_input_description"])
    await state.set_state(AddMaterial.description)


@material_router.message(AddMaterial.title)
async def material_add_title_wrong(message: Message, state: FSMContext):
    await message.answer(LEXICON_MATERIAL["material_add_title_wrong"])


@material_router.message(AddMaterial.description, F.text)
async def material_add_position_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer(LEXICON_MATERIAL["material_add_input_photo"])
    await state.set_state(AddMaterial.photo)


@material_router.message(AddMaterial.description)
async def material_add_description_wrong(message: Message, state: FSMContext):
    await message.answer(LEXICON_MATERIAL["material_add_description_wrong"])


@material_router.message(AddMaterial.photo, F.photo)
async def material_add_position_photo(message: Message, state: FSMContext):
    await state.update_data(photo=message.photo[-1].file_id)
    await message.answer(
        LEXICON_MATERIAL["material_add_input_packing"]
    )
    await state.set_state(AddMaterial.packing)


@material_router.message(AddMaterial.photo)
async def material_add_description_wrong(message: Message, state: FSMContext):
    await message.answer(LEXICON_MATERIAL["material_add_photo_wrong"])


@material_router.message(AddMaterial.packing, F.text)
async def material_add_position_packing(message: Message, state: FSMContext):
    answer = message.text
    if answer.replace(",", "").replace(".", "").isdigit():
        await state.update_data(packing=message.text)
    else:
        await message.answer(LEXICON_MATERIAL["material_add_packing_wrong"])
        return
    await message.answer(LEXICON_MATERIAL["material_add_input_price"])
    await state.set_state(AddMaterial.price)


@material_router.message(AddMaterial.packing)
async def material_add_packing_wrong(message: Message, state: FSMContext):
    await message.answer(LEXICON_MATERIAL["material_add_packing_wrong"])


@material_router.message(AddMaterial.price, F.text)
async def material_add_position_price(message: Message, state: FSMContext):
    answer = message.text
    if answer.isdigit():
        await state.update_data(price=message.text)
    else:
        await message.answer(LEXICON_MATERIAL["material_add_price_wrong"])
        return
    await message.answer(LEXICON_MATERIAL["material_add_input_quantity"])
    await state.set_state(AddMaterial.quantity)


@material_router.message(AddMaterial.price)
async def material_add_price_wrong(message: Message, state: FSMContext):
    await message.answer(LEXICON_MATERIAL["material_add_price_wrong"])


@material_router.message(AddMaterial.quantity, F.text)
async def material_add_position_price(message: Message, state: FSMContext):
    answer = message.text
    await state.set_state(AddMaterial.quantity)
    if answer.isdigit():
        await state.update_data(quantity=message.text)
    else:
        await message.answer(LEXICON_MATERIAL["material_add_price_wrong"])
        return
    data = await state.get_data()
    await message.answer_photo(
        photo=data["photo"],
        caption=(
            f"<b>Материал добавлен в базу данных</b>\n"
            f"Название: <b>{data["title"]}\n</b>"
            f"Описание: <b>{data["description"]}\n</b>"
            f"Фасовка: <b>{data["packing"]}\n</b>"
            f"Цена: <b>{data["price"]}\n</b>"
            f"Количество: <b>{data["quantity"]}\n</b>"
        ),
        reply_markup=ADMIN_KB
    )
    await state.clear()


@material_router.message(AddMaterial.quantity)
async def material_add_price_wrong(message: Message, state: FSMContext):
    await message.answer(LEXICON_MATERIAL["material_add_price_wrong"])


@material_router.message(F.text == "Удалить позицию")
async def material_add_position(message: Message):
    await message.answer(text=LEXICON['pass'], reply_markup=ADMIN_KB)


@material_router.message(F.text == "Спиок материалов")
async def material_add_position(message: Message):
    await message.answer(text=LEXICON['pass'], reply_markup=ADMIN_KB
    )


@material_router.message(F.text == "Список для покупки")
async def material_add_position(message: Message):
    await message.answer(text=LEXICON['pass'], reply_markup=ADMIN_KB)