from datetime import datetime
from aiogram import F, Router
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram.filters import Command, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from sqlalchemy.ext.asyncio import AsyncSession

from database.engine import session_maker
from database.methods import (
    orm_add_record,
    orm_change_banner_image,
    # orm_get_categories,
    # orm_add_product,
    # orm_delete_product,
    orm_get_info_pages,
    orm_get_record,
    orm_get_records,
    orm_update_record,
    # orm_get_product,
    # orm_get_products,
    # orm_update_product,
)
from keyboards.reply import get_keyboard

# from filters.chat_types import ChatTypeFilter, IsAdmin

from handlers.material_handlers import AddMaterial
from handlers.note_handlers import AddNotes
from keyboards.inline import get_callback_btns
from keyboards.my_calendar import CalendarMarkup
from keyboards.reply import get_keyboard
from keyboards.other_kb import ADMIN_KB, ADMIN_MENU_KB, CHANGE_RECORD_ADMIN, CHANGE_RECORD_AFTER_FILING, CHANGE_RECORD_KB, RECORD_KB
from lexicon.lexicon_ru import LEXICON, LEXICON_CALENDAR
from middlewares.db import DataBaseSession



admin_router = Router()
# admin_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())


admin_router.message.middleware(DataBaseSession(session_pool=session_maker))
admin_router.callback_query.middleware(DataBaseSession(session_pool=session_maker))


@admin_router.message(StateFilter("*"), Command("admin"))
@admin_router.message(StateFilter("*"), F.text.casefold() == "назад в меню администратора")
@admin_router.message(StateFilter("*"), F.text.casefold() == "меню администратора")
async def admin_features(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("<b>Меню администратора</b>", reply_markup=ADMIN_MENU_KB)


@admin_router.message(F.text.casefold() == "добавить/изменить запись")
async def admin_features(message: Message):
    await message.answer(
        "Если нужно вернуться в меню администратора пропишите или нажмине\n"
        "/admin",
        reply_markup=ReplyKeyboardRemove()
    )
    await message.answer(
        "<b>Добавление. Изменение записи.</b>\nВыберите действие.",
        reply_markup=CHANGE_RECORD_ADMIN
    )



# Отмена действия во время заполнения FSM
@admin_router.message(StateFilter("*"), F.text.casefold() == "отмена")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return

    states = [
        AddRecord.record_for_change,
        AddMaterial.material_for_change,
        AddNotes.note_for_change
    ]

    for state in states:
        if state:
            state = None

    await state.clear()
    await message.answer("Действия отменены", reply_markup=ADMIN_KB)


################# Микро FSM для загрузки/изменения баннеров ###################

class AddBanner(StatesGroup):
    image = State()

# Отправляем перечень информационных страниц бота и становимся в состояние отправки photo
@admin_router.message(StateFilter(None), F.text == 'Добавить/Изменить баннер')
async def add_image2(message: Message, state: FSMContext, session: AsyncSession):
    pages_names = [page.name for page in await orm_get_info_pages(session)]
    await message.answer(f"Отправьте фото баннера.\nВ описании укажите для какой страницы:\
                         \n{', '.join(pages_names)}")
    await state.set_state(AddBanner.image)

# Добавляем/изменяем изображение в таблице (данные баннера заполнены в БД)
@admin_router.message(AddBanner.image, F.photo)
async def add_banner(message: Message, state: FSMContext, session: AsyncSession):
    image_id = message.photo[-1].file_id
    for_page = message.caption.strip()
    pages_names = [page.name for page in await orm_get_info_pages(session)]
    if for_page not in pages_names:
        await message.answer(f"Введите нормальное название страницы, например:\
                         \n{', '.join(pages_names)}")
        return
    await orm_change_banner_image(session, for_page, image_id,)
    await message.answer("Баннер добавлен/изменен.")
    await state.clear()

# ловим некоррекный ввод
@admin_router.message(AddBanner.image)
async def add_banner2(message: Message, state: FSMContext):
    await message.answer("Отправьте фото баннера или отмена")


################### FSM для добавления/изменения записей ######################

class AddRecord(StatesGroup):
    date = State()
    name = State()
    phone_number = State()

    record_for_change = None

    texts = {
        "AddRecord:date": "Введите дату приема заново:",
        "AddRecord:name": "Введите имя заново:",
        "AddRecord:phone_number": "Введите номер телефона заново:",
    }

# Возврат к предыдущему шагу во время зполнения FSM для засписей
@admin_router.message(
        StateFilter("*"),
        F.text == "Вернуться на шаг назад"
    )
async def back_step_handler(message: Message, state: FSMContext) -> None:
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

# Начало добавления записей, вывод календаря
@admin_router.callback_query(StateFilter(None), F.data.startswith("add_record"))
async def calendar_add_reception(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
) -> None:
# @admin_router.message(StateFilter(None), F.text == "Добавить запись")
# async def calendar_add_reception(message: Message, state: FSMContext) -> None:
    await callback.message.delete()
    print("YES")
    current_date = datetime.now()
    current_month = current_date.month
    current_year = current_date.year
    await callback.message.answer(
        text=LEXICON['record_client'],
        reply_markup=CalendarMarkup(current_month, current_year).build.kb
    )
    await state.set_state(AddRecord.date)

# Ответ на нажатие кнопок календаря, вход в состояния ввода имени.
@admin_router.callback_query(AddRecord.date)
async def calendar_add_date(
    callback: CallbackQuery, session: AsyncSession, state: FSMContext
) -> None:
    """Ответ на нажатие кнопок календаря."""
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

# Смена месяца на клавиатуре.
async def get_next_month(callback: CallbackQuery) -> None:
    """Смена месяца на клавиатуре."""
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

# Валидация вводимых данных в календаре
@admin_router.message(AddRecord.date)
async def calendar_wrong_name_client(message: Message, state: FSMContext):
    await message.answer(LEXICON_CALENDAR["calendar_add_invalid_date"])

# Ввод имени, вход в состояние ввода номера телефона.
@admin_router.message(AddRecord.name, F.text)
async def calendar_add_name_client(message: Message, state: FSMContext):
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

# Валидация вводимых имени
@admin_router.message(AddRecord.name)
async def calendar_wrong_name_client(message: Message, state: FSMContext):
    await message.answer(LEXICON_CALENDAR["calendar_wrong_name_client"])

# Ввод номера телефона, завершение добавления записи.
@admin_router.message(AddRecord.phone_number, F.text)
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
                f"<b>Номер клиента:</b> {data["phone_number"]}\n"
                f"<b>Дата приема клиента:</b> {data["date"]}"
            ),
            reply_markup=CHANGE_RECORD_AFTER_FILING
        )
        await state.clear()
    except Exception as e:
        await message.answer(
            f"Произошла ошибка: {e}", reply_markup=ADMIN_MENU_KB,
        )
        await state.clear()

# Валидация вводимого номера
@admin_router.message(AddRecord.phone_number)
async def calendar_wrong_phone_number_client(
    message: Message,
    state: FSMContext
):
    await message.answer(LEXICON_CALENDAR["calendar_wrong_phone_number_client"])


# Изменяем запись
@admin_router.callback_query(StateFilter(None), F.data.startswith("change_record_"))
async def change_record_callback(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
) -> None:
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

# Список записей для изменения
@admin_router.callback_query(F.data.startswith("list_from_change_record"))
async def calendar_reception_list(callback: CallbackQuery, session: AsyncSession) -> None:
    for record in await orm_get_records(session):
        await callback.message.answer(
            text=(
                f"<b>Имя клиента:</b> {record.name}\n\n"
                f"<b>Номер клиента:</b> {record.phone_number}\n"
                f"<b>Дата приема клиента:</b> {record.date.strftime("%d/%m/%Y")}"
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
        reply_markup=get_keyboard("меню администратора", "Главное меню", sizes=(2, ))
    )