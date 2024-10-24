from datetime import datetime
from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession
from database.methods import (
    orm_add_record, orm_get_records,
    orm_get_record, orm_delete_record,
    orm_update_record
)
from database.engine import session_maker
from filters.is_admin import IsAdmin
from keyboards.my_calendar import CalendarMarkup
from keyboards.inline import get_callback_btns
from keyboards.other_kb import (
    ADMIN_MENU_KB,
    RECORD_AFTER_FILING,
    CHANGE_RECORD_KB,
    RECORD_AFTER_LIST_RESORD
)
from lexicon.lexicon_ru import (
    LEXICON,
    LEXICON_CALENDAR,
)
from middlewares.db import DataBaseSession


record_router = Router()

record_router.message.filter(IsAdmin())

record_router.message.middleware(DataBaseSession(session_pool=session_maker))
record_router.callback_query.middleware(
    DataBaseSession(session_pool=session_maker)
)


class AddRecord(StatesGroup):
    """FSM для добавления/изменения записей"""
    date = State()
    name = State()
    phone_number = State()

    record_for_change = None

    texts = {
        "AddRecord:date": "Введите дату приема заново:",
        "AddRecord:name": "Введите имя заново:",
        "AddRecord:phone_number": "Введите номер телефона заново:",
    }


@record_router.message(
        StateFilter("*"),
        F.text == "Вернуться на шаг назад"
    )
async def back_step_handler(message: Message, state: FSMContext) -> None:
    """Возврат к предыдущему шагу во время зполнения FSM для засписей"""
    current_state = await state.get_state()

    if current_state == AddRecord.date:
        await message.answer(
            'Предидущего шага нет, или введите дату'
            ' напишите "отмена"'
        )
        return

    previous = None
    for step in AddRecord.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(
                "Ок, вы вернулись к прошлому шагу \n"
                f" {AddRecord.texts[previous.state]}"
            )
            return
        previous = step


@record_router.callback_query(
        StateFilter(None), F.data.startswith("add_record")
    )
async def calendar_add_reception(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
) -> None:
    """Начало добавления записей, вывод календаря"""
    await callback.message.delete()
    current_date = datetime.now()
    current_month = current_date.month
    current_year = current_date.year
    await callback.message.answer(
        text=LEXICON['record_client'],
        reply_markup=CalendarMarkup(current_month, current_year).build.kb
    )
    await state.set_state(AddRecord.date)


@record_router.callback_query(AddRecord.date)
async def calendar_add_date(
    callback: CallbackQuery, state: FSMContext
) -> None:
    """Ответ на нажатие кнопок календаря, вход в состояния ввода имени"""
    mes = callback.data
    if "date" in mes:
        str_date = callback.data.split()[1]
        date = datetime.strptime(str_date, '%d.%m.%Y')
        if date < datetime.now():
            await callback.message.answer("Дата должна быть в будущем")
            return
        await callback.message.answer(
            text=(
                f"Вы выбрали дату: {str_date}\n\n"
                "<b>Введите имя клиента</b>"
                )
            )
        await callback.bot.delete_message(
            callback.from_user.id, callback.message.message_id
        )
        await state.update_data(date=str_date)
        await state.set_state(AddRecord.name)
    elif "back" in mes or "next" in mes:
        await get_next_month(callback)


@record_router.message(AddRecord.date)
async def calendar_wrong_name_client(
    message: Message, state: FSMContext
) -> None:
    """Валидация вводимых данных в календаре"""
    await message.answer(LEXICON_CALENDAR["calendar_add_invalid_date"])


@record_router.message(AddRecord.name, F.text)
async def calendar_add_name_client(
    message: Message, state: FSMContext
) -> None:
    """Ввод имени, вход в состояние ввода номера телефона."""
    await message.delete()
    if len(message.text) >= 30:
        await message.answer(LEXICON_CALENDAR["calendar_add_long_name"])
        return
    if message.text == "Оставить как есть" and AddRecord.record_for_change:
        await state.update_data(name=AddRecord.record_for_change.name)
        await message.answer(
            LEXICON_CALENDAR["calendar_add_input_name"],
            reply_markup=CHANGE_RECORD_KB
        )
    else:
        await state.update_data(name=message.text)
        await message.answer(LEXICON_CALENDAR["calendar_add_input_name"])
    await state.set_state(AddRecord.phone_number)


@record_router.message(AddRecord.name)
async def calendar_wrong_name(message: Message, state: FSMContext) -> None:
    """Валидация вводимых имени"""
    await message.delete()
    await message.answer(LEXICON_CALENDAR["calendar_wrong_name_client"])


@record_router.message(AddRecord.phone_number, F.text)
async def calendar_add_phone_number_client(
    message: Message,
    state: FSMContext,
    session: AsyncSession
) -> None:
    """Ввод номера телефона, завершение добавления записи."""
    await message.delete()
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
            await orm_update_record(
                session, AddRecord.record_for_change.id, data
            )
        else:
            await orm_add_record(session, data)
        await message.answer(
            text=(
                f"Запись клиента добавлена\n"
                f"<b>Имя клиента:</b> {data["name"]}\n"
                f"<b>Номер клиента:</b> {data["phone_number"]}\n"
                f"<b>Дата приема клиента:</b> {data["date"]}"
            ),
            reply_markup=RECORD_AFTER_FILING
        )
        await state.clear()
    except Exception as e:
        await message.answer(
            f"Произошла ошибка: {e}", reply_markup=ADMIN_MENU_KB,
        )
        await state.clear()


@record_router.message(AddRecord.phone_number)
async def calendar_wrong_phone_number_client(
    message: Message,
    state: FSMContext
) -> None:
    """Валидация вводимого номера"""
    await message.answer(
        LEXICON_CALENDAR["calendar_wrong_phone_number_client"]
    )
# КОНЕЦ FSM


@record_router.callback_query(F.data.startswith("list_from_change_record"))
async def calendar_reception_list(
    callback: CallbackQuery, session: AsyncSession
) -> None:
    """Список записей для изменения"""
    callback.answer()
    for record in await orm_get_records(session):
        await callback.message.answer(
            text=(
                f"<b>Имя клиента:</b> {record.name}\n\n"
                f"<b>Номер клиента:</b> {record.phone_number}\n"
                f"<b>Дата приема:</b> {record.date.strftime("%d/%m/%Y")}"
            ),
            reply_markup=get_callback_btns(
                btns={
                    "Удалить": f"delete_record_{record.id}",
                    "Изменить": f"change_record_{record.id}",
                }
            ),
        )
    await callback.message.answer(
        "ОК, вот список записей ⏫",
        reply_markup=RECORD_AFTER_LIST_RESORD
    )


@record_router.callback_query(
        StateFilter(None), F.data.startswith("change_record_")
    )
async def change_record_callback(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
) -> None:
    """Изменяем запись"""
    record_id = callback.data.split("_")[-1]

    record_for_change = await orm_get_record(session, int(record_id))

    AddRecord.record_for_change = record_for_change

    current_date = datetime.now()
    current_month = current_date.month
    current_year = current_date.year

    await callback.answer()
    await callback.message.answer(
        "Введите дату приема",
        reply_markup=CalendarMarkup(current_month, current_year).build.kb
        )
    await state.set_state(AddRecord.date)


@record_router.callback_query(F.data.startswith("delete_record_"))
async def delete_record_cb(
    callback: CallbackQuery, session: AsyncSession
) -> None:
    """Удаляем запись"""
    record_id = callback.data.split("_")[-1]
    await orm_delete_record(session, int(record_id))

    await callback.answer("Запись удалена!")
    await callback.message.answer("Запись удалена!")


async def get_next_month(callback: CallbackQuery) -> None:
    """Смена месяца на клавиатуре"""
    month, year = map(int, callback.data.split()[1].split("."))
    calendar = CalendarMarkup(month, year)
    if "next" in callback.data:
        await callback.message.edit_reply_markup(
            reply_markup=calendar.next_month().kb
        )
    elif "back" in callback.data:
        await callback.message.edit_reply_markup(
            reply_markup=calendar.previous_month().kb
        )
