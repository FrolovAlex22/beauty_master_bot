from aiogram import F, Router
from aiogram.types import ReplyKeyboardRemove
from aiogram.filters import StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession
from database.methods import (
    orm_add_note,
    orm_change_puplish_note,
    orm_get_notes,
    orm_get_note,
    orm_delete_note,
    orm_get_notes_is_published,
    orm_update_note
)

from database.engine import session_maker
from filters.is_admin import IsAdmin
from handlers.handlers_methods import get_media_banner
from keyboards.reply import get_keyboard
from keyboards.inline import get_callback_btns
from keyboards.other_kb import (
    ADMIN_MENU_KB, NOTE_ADD_EDIT_PHOTO_STATE, NOTE_ADMIN, NOTE_ADMIN_AFTER_ADD,
    NOTE_CHOISE_TYPE, NOTE_EDIT_CHOISE_TYPE, NOTE_IS_PUBLISHED,
    NOTE_LIST_CHOISE_TYPE
)
from lexicon.lexicon_ru import LEXICON_NOTES
from middlewares.db import DataBaseSession


note_router = Router()

note_router.message.filter(IsAdmin())


note_router.message.middleware(DataBaseSession(session_pool=session_maker))
note_router.callback_query.middleware(
    DataBaseSession(session_pool=session_maker)
)


class AddNotes(StatesGroup):
    note_type = State()
    title = State()
    description = State()
    photo = State()
    is_published = State()

    note_for_change = None

    texts_back = {
        "AddNotes:note_type": "Выберите тип заметки",
        "AddNotes:title": "Введите название заметки заново",
        "AddNotes:description": "Введите описание заметки заново",
        "AddNotes:photo": "Отправте изображение заметки заново",
    }

    texts_leave_as_is = {
        "AddNotes:note_type": "Введите тип заметки",
        "AddNotes:title": "Введите описание заметки",
        "AddNotes:description": "Отправте изображение заметки",
        "AddNotes:photo": "Запись обновлена",
    }


@note_router.message(
        AddNotes.photo, or_f(
            F.photo,
            F.text.casefold() == "пропустить",
            F.text.casefold() == "оставить как есть"
        )
    )
async def notes_add_image(message: Message, state: FSMContext) -> None:
    """Добавление изображения к заметке"""
    if message.photo:
        await state.update_data(photo=message.photo[-1].file_id)
    else:
        if message.text.casefold() == "пропустить":
            await state.update_data(photo=None)
        elif (
            message.text.casefold() == "оставить как есть"
            and AddNotes.note_for_change
        ):
            await state.update_data(photo=AddNotes.note_for_change.photo)
    await message.answer(
        text="<b>Изображение добавлено</b>\n",
        reply_markup=ReplyKeyboardRemove()
    )
    await message.answer(
        text="Опубликовать заметку?",
        reply_markup=NOTE_IS_PUBLISHED
    )
    await state.set_state(AddNotes.is_published)


@note_router.callback_query(StateFilter("*"), F.data == "note_step_back")
async def note_back_step_handler(
    callback: CallbackQuery, state: FSMContext
) -> None:
    """Возврат на шаг назад"""
    current_state = await state.get_state()

    if current_state == AddNotes.note_type:
        await callback.message.answer(
            "Предидущего шага нет, нужно выбрать тип заметки",
        )
        return

    previous = None
    for step in AddNotes.__all_states__:

        if step.state == current_state:
            await state.set_state(previous)
            if previous.state == AddNotes.note_type:
                keyboard = NOTE_CHOISE_TYPE
            else:
                keyboard = NOTE_EDIT_CHOISE_TYPE
            await callback.message.answer(
                "Ок, вы вернулись к прошлому шагу \n"
                f" {AddNotes.texts_back[previous.state]}",
                reply_markup=keyboard
            )
            return
        previous = step


@note_router.callback_query(StateFilter(None), F.data == "add_note")
async def notes_add(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
) -> None:
    """Добавление заметки"""
    await callback.answer()
    if callback.message.photo:
        await callback.bot.edit_message_caption(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            caption=LEXICON_NOTES["notes_add"],
            reply_markup=NOTE_CHOISE_TYPE
        )
    else:
        media = await get_media_banner(session, menu_name="information")
        await callback.message.answer_photo(
            media.media,
            media.caption,
            reply_markup=NOTE_CHOISE_TYPE
        )
    await state.set_state(AddNotes.note_type)


@note_router.callback_query(
    AddNotes.note_type, or_f(
        F.data == "note material_info", F.data == "note good_to_know"
    )
)
async def notes_add_type_choise_callback(
    callback: CallbackQuery, state: FSMContext
) -> None:
    """Выбор типа заметки"""
    note_type = callback.data.split(" ")[-1]
    await state.update_data(note_type=note_type)
    if AddNotes.note_for_change:
        keyboard = NOTE_EDIT_CHOISE_TYPE
    else:
        keyboard = None
    await callback.message.delete()
    await callback.message.answer(
        LEXICON_NOTES["notes_add_title"],
        reply_markup=keyboard
    )

    await state.set_state(AddNotes.title)


@note_router.callback_query(
        StateFilter(None), F.data.startswith("change_note_")
    )
async def change_note_callback(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
) -> None:
    """Изменение заметки"""
    note_id = callback.data.split("_")[-1]

    note_for_change = await orm_get_note(session, int(note_id))

    AddNotes.note_for_change = note_for_change

    await callback.answer()

    media = await get_media_banner(session, menu_name="information")
    await callback.message.answer_photo(
        media.media,
        LEXICON_NOTES["notes_add"],
        reply_markup=NOTE_CHOISE_TYPE
    )
    await state.set_state(AddNotes.note_type)


@note_router.callback_query(F.data.startswith("unpublish_note_"))
async def unpublish_note_handler(
    callback: CallbackQuery, session: AsyncSession
) -> None:
    """Изменение заметки"""
    note_id = callback.data.split("_")[-1]
    note_for_change = await orm_get_note(session, int(note_id))

    await orm_change_puplish_note(
        session, int(note_id), note_for_change.is_published
    )

    await callback.answer(
        text=f"Публикация: <b>{note_for_change.title}</b>, снята с записи"
    )


@note_router.message(AddNotes.title, F.text)
async def notes_add_title(message: Message, state: FSMContext) -> None:
    """Обработчик названия заметки"""
    await message.delete()
    await state.update_data(title=message.text)
    if AddNotes.note_for_change:
        keyboard = get_callback_btns(
            btns={"Оставить как есть": "note_leave_as_is", },
            sizes=(2,),
        )
    else:
        keyboard = None
    await message.answer(
        LEXICON_NOTES["notes_add_input_description"], reply_markup=keyboard
    )
    await state.set_state(AddNotes.description)


@note_router.message(AddNotes.title)
async def notes_add_title_wrong(message: Message) -> None:
    """Обработчик ошибки при добавлении названия"""
    await message.answer(
        LEXICON_NOTES["notes_add_title_wrong"]
    )


@note_router.message(AddNotes.description, F.text)
async def notes_add_description(message: Message, state: FSMContext) -> None:
    await message.delete()
    await state.update_data(description=message.text)
    if not AddNotes.note_for_change:
        await message.answer(
            LEXICON_NOTES["notes_add_input_image"],
            reply_markup=get_keyboard("Пропустить", sizes=(2, ))
        )
    else:
        await message.answer(
            LEXICON_NOTES["notes_add_input_image"],
            reply_markup=NOTE_ADD_EDIT_PHOTO_STATE
        )
    await state.set_state(AddNotes.photo)


@note_router.message(AddNotes.description)
async def notes_add_description_wrong(message: Message) -> None:
    """Обработчик ошибки при добавлении описания"""
    await message.answer(LEXICON_NOTES["notes_add_description_wrong"])


@note_router.message(AddNotes.photo)
async def notes_add_image_wrong(message: Message) -> None:
    """Обработчик ошибки при добавлении изображения"""
    await message.delete()
    await message.answer(LEXICON_NOTES["notes_add_image_wrong"])


@note_router.callback_query(F.data.startswith("delete_note_"))
async def note_delete_position(
    callback: CallbackQuery, session: AsyncSession
) -> None:
    """Удаляем заметку"""
    note_id = callback.data.split("_")[-1]
    await orm_delete_note(session, int(note_id))

    await callback.answer("Заметка удалена")
    await callback.message.answer("Заметка удалена из базы данных.")


@note_router.callback_query(
        AddNotes.is_published,
        or_f(F.data == "publish_yes", F.data == "publish_no")
    )
async def notes_add_publish(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
) -> None:
    """Выбор возможности публикации заметки"""
    await callback.answer()
    if callback.data == "publish_yes":
        await state.update_data(is_published=True)
    else:
        await state.update_data(is_published=False)
    data = await state.get_data()
    try:
        if AddNotes.note_for_change:
            await orm_update_note(session, AddNotes.note_for_change.id, data)
        else:
            await orm_add_note(session, data)
        await callback.message.answer(
            text=(
                f"<b>Заметка добавлена в базу данных</b>\n"
                f"Название: <b>{data['title']}\n</b>"
                f"Категория заметки: <b>{data['note_type']}\n</b>"
                f"Описание: <b>{data['description']}\n</b>"
                f"Изображение: <b>Отсутствует</b>\n"
                f"Опубликованно?: <b>{data['is_published']}</b>"
            ),
            reply_markup=NOTE_ADMIN_AFTER_ADD
        )
        await state.clear()
    except Exception as e:
        await callback.message.answer(
            f"Произошла ошибка: {e}", reply_markup=ADMIN_MENU_KB,
        )
        await state.clear()


@note_router.callback_query(F.data == "admin_list_note")
async def notes_list_choise_type(
    callback: CallbackQuery, session: AsyncSession
) -> None:
    """Список заметок для администратора"""
    await callback.answer()
    if callback.message.photo:
        await callback.bot.edit_message_caption(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            caption=LEXICON_NOTES["notes_add"],
            reply_markup=NOTE_LIST_CHOISE_TYPE
        )
    else:
        media = await get_media_banner(session, menu_name="information")
        await callback.message.answer_photo(
            media.media,
            media.caption,
            reply_markup=NOTE_LIST_CHOISE_TYPE
        )


@note_router.callback_query(
        or_f(
            F.data == "note_list material_info",
            F.data == "note_list good_to_know"
        )
    )
async def notes_list(callback: CallbackQuery, session: AsyncSession) -> None:
    """Список заметок, в зависимости от категории для администратора"""
    await callback.answer()
    note_type = callback.data.split(" ")[-1]
    for note in await orm_get_notes(session, note_type):
        if note.photo:
            await callback.message.answer_photo(
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
            await callback.message.answer(
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
    await callback.message.answer(
        "ОК, вот список заметок ⏫",
        reply_markup=NOTE_ADMIN_AFTER_ADD
    )


@note_router.callback_query(F.data == "admin_published_entries",)
async def notes_list_published(
    callback: CallbackQuery, session: AsyncSession
) -> None:
    """Список опубликованных записей"""
    await callback.answer()
    for note in await orm_get_notes_is_published(session):
        if note.photo:
            await callback.message.answer_photo(
                photo=note.photo,
                caption=(
                    f"Название: <b>{note.title}\n</b>"
                    f"Описание: <b>{note.description}\n</b>"
                ),
                reply_markup=get_callback_btns(
                    btns={"Снять с публикации": f"unpublish_note_{note.id}"},
                ),
            )
        else:
            await callback.message.answer(
                text=(
                    f"Название: <b>{note.title}\n</b>"
                    f"Описание: <b>{note.description}\n</b>"
                ),
                reply_markup=get_callback_btns(
                    btns={"Снять с публикации": f"unpublish_note_{note.id}"}
                ),
            )
    await callback.message.answer(
        "ОК, вот список заметок ⏫",
        reply_markup=NOTE_ADMIN
    )


@note_router.callback_query(
        StateFilter("*"),
        F.data == "note_leave_as_is",
        )
async def note_step_back_handler(
    callback: CallbackQuery, state: FSMContext
) -> None:
    """Возвратна шаг назад при заполнении FSM Note"""
    current_state = await state.get_state()

    if current_state == AddNotes.note_type:
        keyboard = NOTE_CHOISE_TYPE
    elif current_state == AddNotes.description:
        keyboard = NOTE_ADD_EDIT_PHOTO_STATE
    else:
        keyboard = NOTE_EDIT_CHOISE_TYPE

    await callback.message.answer(
        "Оставили как есть.\n"
        f" {AddNotes.texts_leave_as_is[current_state]}",
        reply_markup=keyboard
    )

    if current_state == AddNotes.note_type:
        await state.update_data(note_type=AddNotes.note_for_change.note_type)
        await state.set_state(AddNotes.title)
    elif current_state == AddNotes.title:
        await state.update_data(title=AddNotes.note_for_change.title)
        await state.set_state(AddNotes.description)
    elif current_state == AddNotes.description:
        await state.update_data(
            description=AddNotes.note_for_change.description
        )
        await state.set_state(AddNotes.photo)
    elif current_state == AddNotes.photo:
        await state.update_data(photo=AddNotes.note_for_change.photo)
