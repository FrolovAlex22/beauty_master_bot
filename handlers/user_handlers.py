from datetime import datetime
import os
from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, ContentType, ReplyKeyboardRemove, Contact
from sqlalchemy.ext.asyncio import AsyncSession

from database.engine import session_maker
from database.methods import orm_get_banner, orm_get_records
from handlers.handlers_methods import client_reception_in_the_list
from handlers.record_handlers import get_next_month
from keyboards.my_calendar import CalendarMarkup
from keyboards.reply import get_keyboard
from keyboards.other_kb import ADMIN_KB, CHECK_KB, RECORD_KB, MATERIAL_KB, NOTE_KB, USER_MENU_KB, USER_RECORD_KB, USER_SENDING_CONTACT_KB
from lexicon.lexicon_ru import LEXICON, LEXICON_MATERIAL
from middlewares.db import DataBaseSession

user_router = Router()

user_router.message.middleware(DataBaseSession(session_pool=session_maker))
user_router.callback_query.middleware(DataBaseSession(session_pool=session_maker))



ADMIN_IDS = os.getenv("ADMIN_IDS")


# FSM для заявки пользователя на запись
class UserRecord(StatesGroup):
    # Шаги состояний
    date = State()
    contact = State()


@user_router.message(CommandStart())
async def process_start_command(
    message: Message, state: FSMContext, session: AsyncSession
) -> None:
    if state:
        await state.clear()
    await message.answer(f"Hello, {message.from_user.full_name}!")
    await message.answer(text=LEXICON[message.text])

    banner = await orm_get_banner(session, page="main")
    if  not banner.image:
        await message.answer(
            "<b>В данный момент ведется обновление бота. "
            "Приношу свои извененения</b>"
        )
    await message.answer_photo(
        banner.image, caption=banner.description, reply_markup=USER_MENU_KB
    )


@user_router.message(Command(commands="help"))
async def process_help_command(message: Message):
    await message.answer(LEXICON[message.text])


@user_router.callback_query(F.data =="main_menu")
async def process_main_menu_command(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
) -> None:

    await callback.answer()
    if state:
        await state.clear()
    banner = await orm_get_banner(session, page="main")
    if  not banner.image:
        await callback.message.answer(
            "<b>В данный момент ведется обновление бота. "
            "Приношу свои извененения</b>"
        )
    await callback.message.answer_photo(
        banner.image, caption=banner.description, reply_markup=USER_MENU_KB
    )


@user_router.callback_query(F.data == "user_record")
async def user_records(callback: CallbackQuery, session: AsyncSession):
    banner = await orm_get_banner(session, page="calendar_entries")
    media = InputMediaPhoto(
        media=banner.image, caption=LEXICON_MATERIAL['user_action_selection']
    )

    await callback.bot.edit_message_media(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        media=media,
        reply_markup=USER_RECORD_KB
    )


@user_router.callback_query(F.data == "user_record_list")
async def user_records_list(callback: CallbackQuery, session: AsyncSession):
    records = await orm_get_records(session)
    text = await client_reception_in_the_list(records)

    await callback.message.edit_caption(
        caption=text,
        reply_markup=USER_MENU_KB
    )


@user_router.callback_query(F.data == "user_record_bid")
async def user_records_bid(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    current_date = datetime.now()
    current_month = current_date.month
    current_year = current_date.year
    await callback.message.edit_caption(
        caption=LEXICON_MATERIAL['user_check_date'],
        reply_markup=CalendarMarkup(current_month, current_year).build.kb
    )
    await state.set_state(UserRecord.date)


@user_router.callback_query(UserRecord.date)
async def user_records_bid_get_date(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
)-> None:
    """Ответ на нажатие кнопок календаря, вход в состояния ввода телефона"""
    mes = callback.data
    if "date" in mes:
        str_date = callback.data.split()[1]
        date = datetime.strptime(str_date, '%d.%m.%Y')

        if date < datetime.now():
            await callback.message.answer("Дата должна быть в будущем")
            return
        await state.update_data(date=str_date)
        await state.set_state(UserRecord.contact)
        await callback.bot.delete_message(
            callback.from_user.id, callback.message.message_id
        )
        await callback.message.answer(
            text=(
                f"Вы выбрали дату: {str_date}\n\n"
                "Нажмите на кнопку ниже, чтобы отправить контакт"
            ),
            reply_markup=USER_SENDING_CONTACT_KB
        )
    elif "back" in mes or "next" in mes:
        await get_next_month(callback)


@user_router.message(UserRecord.contact, F.contact)
async def get_contact(
    message: Message, state: FSMContext, session: AsyncSession
)-> None:
    """Получение номера телефона"""
    # contact = message.contact
    data = await state.get_data()
    await message.answer(
        f"Спасибо, {message.contact.first_name}.\n"
        f"Ваш номер {message.contact.phone_number} был получен\n"
        f"Ваша заявка на дату: {data['date']} отправлена мастеру",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()
    banner = await orm_get_banner(session, page="main")
    if  not banner.image:
        await message.answer(
            "<b>В данный момент ведется обновление бота. "
            "Приношу свои извененения</b>"
        )
    await message.bot.send_message(
        chat_id=ADMIN_IDS,
        text= f"Поступила заявка от: {message.contact.first_name}.\n"
        f"Номер для связи: {message.contact.phone_number}\n"
        f"Заявка на дату: {data['date']}\n"
    )
    await message.answer_photo(
        banner.image, caption=banner.description, reply_markup=USER_MENU_KB
    )
