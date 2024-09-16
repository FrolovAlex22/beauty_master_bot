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
from database.methods import orm_add_note, orm_get_notes, orm_get_note, orm_delete_note, orm_update_note

from database.engine import session_maker
from keyboards.reply import get_keyboard
from keyboards.inline import get_callback_btns
from keyboards.other_kb import  ADMIN_KB, NOTE_KB, CHANGE_NOTE_KB
from lexicon.lexicon_ru import LEXICON, LEXICON_NOTES
from middlewares.db import DataBaseSession


note_router = Router()


note_router.message.middleware(DataBaseSession(session_pool=session_maker))
note_router.callback_query.middleware(DataBaseSession(session_pool=session_maker))


class AddNotes(StatesGroup):
    title = State()
    description = State()
    photo = State()

    note_for_change = None

    texts = {
        "AddNotes:title": "Введите название заметки заново:",
        "AddNotes:description": "Введите описание заметки заново:",
        "AddNotes:photo": "Отправте изображение заметки заново:",
    }


@note_router.callback_query(StateFilter(None), F.data.startswith("change_note_"))
async def change_material_callback(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
):
    note_id = callback.data.split("_")[-1]

    note_for_change = await orm_get_note(session, int(note_id))

    AddNotes.note_for_change = note_for_change

    await callback.answer()
    await callback.message.answer(
        "Введите название заметки", reply_markup=CHANGE_NOTE_KB
    )
    await state.set_state(AddNotes.title)


@note_router.message(
        StateFilter("*"),
        F.text == "Вернуться к предыдущему шагу"
    )
async def back_step_handler_material(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()


    if current_state == AddNotes.title:
        await message.answer(
            'Предидущего шага нет, или введите название заметки или'
            ' напишите "отмена"'
        )
        return

    previous = None
    for step in AddNotes.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(
                "Ок, вы вернулись к прошлому шагу \n"
                f" {AddNotes.texts[previous.state]}"
            )
            return
        previous = step

################################################
@note_router.message(StateFilter(None), F.text == "Добавить новую заметку")
async def notes_add(message: Message, state: FSMContext):
    await message.answer(
        LEXICON["notes_add"],
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(AddNotes.title)


@note_router.message(AddNotes.title, F.text)
async def notes_add_title(message: Message, state: FSMContext):
    if message.text == "Оставить как есть" and AddNotes.note_for_change:
        await state.update_data(title=AddNotes.note_for_change.title)
        await message.answer(
            LEXICON_NOTES["notes_add_input_description"],
            reply_markup=CHANGE_NOTE_KB
        )
    else:
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
    if message.text == "Оставить как есть" and AddNotes.note_for_change:
        await state.update_data(
            description=AddNotes.note_for_change.description
        )
        await message.answer(
            LEXICON_NOTES["notes_add_input_image"],
            reply_markup=CHANGE_NOTE_KB
        )
    else:
        await state.update_data(description=message.text)
        await message.answer(
            LEXICON_NOTES["notes_add_input_image"],
            reply_markup=get_keyboard(
                "Пропустить",
                sizes=(1, )
                )
        )
    await state.set_state(AddNotes.photo)


@note_router.message(AddNotes.description)
async def notes_add_description_wrong(message: Message, state: FSMContext):
    await message.answer(LEXICON_NOTES["notes_add_description_wrong"])


@note_router.message(
        AddNotes.photo,
        or_f(
            F.photo,
            F.text.casefold() == "пропустить",
            F.text.casefold() == "оставить как есть")
        )
async def notes_add_image(
    message: Message,
    state: FSMContext,
    session: AsyncSession
):
    if message.text == "Оставить как есть" and AddNotes.note_for_change:
        await state.update_data(
            photo=AddNotes.note_for_change.photo
        )
    elif message.text == "Пропустить":
        await state.update_data(photo=None)
    else:
        await state.update_data(photo=message.photo[-1].file_id)
    data = await state.get_data()
    try:
        if AddNotes.note_for_change:
            await orm_update_note(
                session,
                AddNotes.note_for_change.id,
                data
            )
        else:
            await orm_add_note(session, data)
        if data['photo']:
            await message.answer_photo(
                data['photo'],
                caption=(
                    f"<b>Заметка добавлена в базу данных</b>\n"
                    f"Название: <b>{data['title']}\n</b>"
                    f"Описание: <b>{data['description']}\n</b>"
                ),
                reply_markup=NOTE_KB
            )
            await state.clear()
            return
        await message.answer(
            text=(
                f"<b>Заметка добавлена в базу данных</b>\n"
                f"Название: <b>{data['title']}\n</b>"
                f"Описание: <b>{data['description']}\n</b>"
                f"Изображение: <b>Отсутствует</b>"),
            reply_markup=NOTE_KB
        )
        await state.clear()
    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}", reply_markup=ADMIN_KB,)
        await state.clear()


@note_router.message(AddNotes.photo)
async def notes_add_image_wrong(message: Message, state: FSMContext):
    await message.answer(
        LEXICON_NOTES["notes_add_image_wrong"],
        reply_markup=get_keyboard(
            "Пропустить",
            "Оставить как есть",
            sizes=(1, )
            )
    )


@note_router.callback_query(F.data.startswith("delete_note_"))
async def note_delete_position(callback: CallbackQuery, session: AsyncSession):
    note_id = callback.data.split("_")[-1]
    await orm_delete_note(session, int(note_id))

    await callback.answer("Заметка удалена")
    await callback.message.answer("Заметка удалена из базы данных.")


@note_router.message(F.text == "Спиок заметок")
async def notes_list(message: Message, session: AsyncSession):
    for note in await orm_get_notes(session):
        if note.photo:
            await message.answer_photo(
                photo=note.photo,
                caption=(
                    f"Название: <b>{note.title}\n</b>"
                    f"Описание: <b>{note.description}\n</b>"
                ),
                reply_markup=get_callback_btns(
                    btns={
                        "Удалить": f"delete_note_{note.id}",
                        "Изменить": f"change_note_{note.id}",
                    }
                ),
            )
        else:
            await message.answer(
                text=(
                    f"Название: <b>{note.title}\n</b>"
                    f"Описание: <b>{note.description}\n</b>"
                ),
                reply_markup=get_callback_btns(
                    btns={
                        "Удалить": f"delete_note_{note.id}",
                        "Изменить": f"change_note_{note.id}",
                    }
                ),
            )
    await message.answer(
        "ОК, вот список заметок ⏫",
        reply_markup=get_keyboard("Спиок заметок", "Главное меню", sizes=(1, ))
    )
