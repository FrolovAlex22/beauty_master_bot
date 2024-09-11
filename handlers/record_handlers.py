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
from keyboards.other_kb import CHANGE_KB, ADMIN_KB, RECORD_KB
from lexicon.lexicon_ru import (
    LEXICON,
    LEXICON_CALENDAR,
    LEXICON_MATERIAL,
    LEXICON_NOTES
)
# from database.database import library_of_articles, products_in_sale

router = Router()


CHANGE_KB = get_keyboard(
        "Оставить как есть",
        "Вернуться на шаг назад",
        sizes=(1, ),
)

class AddRecord(StatesGroup):
    # Шаги состояний
    name = State()
    phone_number = State()
    # date = State
    record_for_change = None




@router.callback_query(StateFilter(None), F.data.startswith("change_record_"))
async def change_record_callback(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
):
    record_id = callback.data.split("_")[-1]

    record_for_change = await orm_get_record(session, int(record_id))

    AddRecord.record_for_change = record_for_change

    await callback.answer()
    await callback.message.answer(
        "Введите название товара", reply_markup=CHANGE_KB
    )
    await state.set_state(AddRecord.name)


# @router.message(StateFilter("*"), F.text.casefold() == "назад")
# async def back_step_handler(message: Message, state: FSMContext) -> None:
#     current_state = await state.get_state()


#     if current_state == AddRecord.name:
#         await message.answer(
#             'Предидущего шага нет, или введите название товара или напишите "отмена"'
#         )
#         return

#     previous = None
#     for step in AddRecord.__all_states__:
#         if step.state == current_state:
#             await state.set_state(previous)
#             await message.answer(
#                 f"Ок, вы вернулись к прошлому шагу \n {AddRecord.texts[previous.state]}"
#             )
#             return
#         previous = step


@router.message(StateFilter("*"), F.text.casefold() == "отмена")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    if AddRecord.record_for_change:
        AddRecord.record_for_change = None

    await state.clear()
    await message.answer("Действия отменены", reply_markup=ADMIN_KB)


@router.message(StateFilter(None), F.text == "Добавить запись")
async def calendar_add_reception(message: Message, state: FSMContext):
    await message.answer(text=LEXICON['record_client'], reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(AddRecord.name)


@router.message(AddRecord.name, or_f(F.text))
async def calendar_add_name_client(message: Message, state: FSMContext):
    if len(message.text) >= 30:
        await message.answer(LEXICON_CALENDAR["calendar_add_long_name"])
        return
    if message.text == "Оставить как есть" and AddRecord.record_for_change:
        await state.update_data(description=AddRecord.record_for_change.name)
    await state.update_data(name=message.text)
    if AddRecord.record_for_change:
        await message.answer(
            LEXICON_CALENDAR["calendar_add_input_name"],
            reply_markup=CHANGE_KB
        )
        await state.set_state(AddRecord.phone_number)
        return
    await message.answer(LEXICON_CALENDAR["calendar_add_input_name"])
    await state.set_state(AddRecord.phone_number)


@router.message(AddRecord.name)
async def calendar_wrong_name_client(message: Message, state: FSMContext):
    await message.answer(LEXICON_CALENDAR["calendar_wrong_name_client"])


@router.message(AddRecord.phone_number, F.text)
async def calendar_add_phone_number_client(
    message: Message,
    state: FSMContext,
    session: AsyncSession
):
    answer = message.text
    number = answer.replace("+", "").replace(" ", "")
    if message.text == "Оставить как есть" and AddRecord.record_for_change:
        await state.update_data(
            phone_number=AddRecord.record_for_change.phone_number
        )
    else:
        if number.isnumeric() and len(number) == 11:
            await state.update_data(phone_number=int(number))
        else:
            await message.answer(
                LEXICON_CALENDAR["calendar_add_phone_number_invalid_len_phone"]
            )
            return
    data = await state.get_data()

    try:
        if AddRecord.record_for_change:
            await orm_update_record(session, AddRecord.record_for_change.id, data)
        else:
            await orm_add_record(session, data)
        await message.answer(
            text=(
                f"Запись клиента добавлена\n"
                f"<b>Имя клиента:</b> {data["name"]}\n"
                f"<b>Номер клиента:</b> {data["phone_number"]}"
            ),
            reply_markup=RECORD_KB
        )
        await state.clear()
    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}", reply_markup=ADMIN_KB,)
        await state.clear()



@router.message(AddRecord.phone_number)
async def calendar_wrong_phone_number_client(
    message: Message,
    state: FSMContext
):
    await message.answer(LEXICON_CALENDAR["calendar_wrong_phone_number_client"])


@router.message(F.text == "Мои записи")
async def calendar_reception_list(message: Message, session: AsyncSession):
    for record in await orm_get_records(session):
        await message.answer(
            text=(
                f"Имя клиента: {record.name}\n\n"
                f"Номер клиента: {record.phone_number}"
            ),
            reply_markup=get_callback_btns(
                btns={
                    "Удалить": f"delete_record_{record.id}",
                    "Изменить": f"change_record_{record.id}",
                }
            ),
        )
    await message.answer(
        "ОК, вот список записей ⏫",
        reply_markup=get_keyboard("Мои записи", "Главное меню", sizes=(1, ))
    )


@router.callback_query(F.data.startswith("delete_record_"))
async def delete_record_callback(callback: CallbackQuery, session: AsyncSession):
    record_id = callback.data.split("_")[-1]
    await orm_delete_record(session, int(record_id))

    await callback.answer("Запись удалена!")
    await callback.message.answer("Запись удалена!")