from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession

from database.engine import session_maker
from database.methods import (
    orm_change_banner_image,
    orm_get_banner,
    orm_get_info_pages,
)
from filters.is_admin import IsAdmin
from handlers.handlers_methods import get_media_banner
from handlers.material_handlers import AddMaterial
from handlers.note_handlers import AddNotes
from handlers.record_handlers import AddRecord
from keyboards.other_kb import (
    ADMIN_MENU_KB, ADD_OR_CHANGE_RECORD_ADMIN, MATERIAL_ADMIN, NOTE_ADMIN,
    SELECTION_AFTER_ADDING_BANNER
)
from middlewares.db import DataBaseSession


admin_router = Router()

admin_router.message.filter(IsAdmin())

admin_router.message.middleware(DataBaseSession(session_pool=session_maker))
admin_router.callback_query.middleware(
    DataBaseSession(session_pool=session_maker)
)


@admin_router.message(StateFilter("*"), Command("admin"))
@admin_router.message(
    StateFilter("*"), F.text.casefold() == "назад в меню администратора"
)
@admin_router.message(
    StateFilter("*"), F.text.casefold() == "меню администратора"
)
async def admin_features(
    message: Message, state: FSMContext, session: AsyncSession
) -> None:
    """Вызов меню администратора"""
    await state.clear()
    banner = await orm_get_banner(session, page="admin")
    if not banner.image:
        await message.answer(
            "<b>Необходимо добавить баннер</b>", reply_markup=ADMIN_MENU_KB
        )
    await message.answer_photo(
        banner.image, caption=banner.description, reply_markup=ADMIN_MENU_KB
    )


@admin_router.callback_query(StateFilter(None), F.data == "admin_menu")
async def admin_features_callback(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
) -> None:
    """Вызов меню администратора через callback"""
    await state.clear()
    await callback.answer()
    media = await get_media_banner(session, menu_name="admin")
    if not media:
        await callback.message.answer("Добавте баннер")
    try:
        await callback.message.edit_media(
            media=media,
            reply_markup=ADMIN_MENU_KB
        )
    except Exception as e:
        print(e)
        await callback.message.answer_photo(
            media.media,
            media.caption,
            reply_markup=ADMIN_MENU_KB
        )


@admin_router.callback_query(StateFilter(None), F.data == "calendar_record")
async def admin_records(
    callback: CallbackQuery, session: AsyncSession
) -> None:
    """Вызов меню записей для администратора"""
    await callback.answer()
    media = await get_media_banner(session, menu_name="calendar_entries")
    if not media:
        await callback.message.answer(
            "<b>Необходимо добавить баннер</b>", reply_markup=ADMIN_MENU_KB
        )
    await callback.message.edit_media(
        media=media,
        reply_markup=ADD_OR_CHANGE_RECORD_ADMIN
    )


@admin_router.callback_query(
        StateFilter(None), F.data == "admin_choise_material"
    )
async def admin_record_menu_choise(
    callback: CallbackQuery, session: AsyncSession
) -> None:
    """Вызов меню материалов для администратора"""
    await callback.answer()
    media = await get_media_banner(session, menu_name="material_entries")
    if not media:
        await callback.message.answer(
            "<b>Необходимо добавить баннер</b>", reply_markup=ADMIN_MENU_KB
        )
    await callback.message.edit_media(
        media=media,
        reply_markup=MATERIAL_ADMIN
    )


@admin_router.callback_query(
        StateFilter(None), F.data == "admin_note"
    )
async def admin_record_menu(
    callback: CallbackQuery, session: AsyncSession
) -> None:
    """Вызов меню материалов для администратора"""
    await callback.answer()
    media = await get_media_banner(session, menu_name="information")
    if not media:
        await callback.message.answer(
            "<b>Необходимо добавить баннер</b>", reply_markup=ADMIN_MENU_KB
        )
    await callback.message.edit_media(
        media=media,
        reply_markup=NOTE_ADMIN
    )


@admin_router.message(StateFilter("*"), F.text.casefold() == "отмена")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """Отмена действия во время заполнения FSM"""
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
    await message.answer("Действия отменены", reply_markup=ADMIN_MENU_KB)


# Микро FSM для загрузки/изменения баннеров
class AddBanner(StatesGroup):
    image = State()


@admin_router.callback_query(
        StateFilter(None),
        or_f(F.data == 'add_banner', F.data == 'add_change_banner')
    )
async def add_image2(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
) -> None:
    """
    Отправляем перечень информационных страниц бота и становимся в состояние
    отправки photo
    """
    await callback.answer()
    pages_names = [page.name for page in await orm_get_info_pages(session)]
    await callback.message.answer(
        f"Отправьте фото баннера.\nВ описании укажите для"
        f" какой страницы:\n{', '.join(pages_names)}"
    )
    await state.set_state(AddBanner.image)


@admin_router.message(AddBanner.image, F.photo)
async def add_banner(
    message: Message, state: FSMContext, session: AsyncSession
) -> None:
    """
    Добавляем/изменяем изображение в таблице (данные баннера заполнены в БД)
    """
    image_id = message.photo[-1].file_id
    for_page = message.caption.strip()
    print(for_page)
    pages_names = [page.name for page in await orm_get_info_pages(session)]
    if for_page not in pages_names:
        await message.answer(f"Введите нормальное название страницы, например:\
                         \n{', '.join(pages_names)}")
        return

    await state.update_data(image_id=image_id, for_page=for_page)
    await orm_change_banner_image(session, for_page, image_id,)
    await message.answer(
        "Баннер добавлен/изменен.",
        reply_markup=SELECTION_AFTER_ADDING_BANNER
    )
    await state.clear()


@admin_router.message(AddBanner.image)
async def add_banner2(message: Message) -> None:
    """Ловим некоррекный ввод"""
    await message.answer("Отправьте фото баннера или отмена")
