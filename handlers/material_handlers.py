from aiogram import F, Router
from aiogram.filters import StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from database.methods import (
    material_fix_quantity,
    orm_add_material,
    orm_get_category_by_name,
    orm_get_material_by_category_id,
    orm_get_material_by_title,
    orm_get_material,
    orm_delete_material,
    orm_get_materials_purchase,
    orm_update_material
)
from database.engine import session_maker
from filters.is_admin import IsAdmin
from handlers.handlers_methods import (
    MaterialCallBack, collection_of_materials_list, get_media_banner
)
from keyboards.inline import get_callback_btns
from keyboards.other_kb import (
    ADMIN_MENU_KB, CHOISE_CATEGORY_ADMIN, CHOISE_CATEGORY_FOR_CHANGE,
    MATERIAL_ADMIN_AFTER_ADD, MATERIAL_ADMIN_CHOISE_FOR_EDIT
)
from lexicon.lexicon_ru import LEXICON_MATERIAL

from middlewares.db import DataBaseSession


material_router = Router()

material_router.message.filter(IsAdmin())

material_router.message.middleware(
    DataBaseSession(session_pool=session_maker)
)
material_router.callback_query.middleware(
    DataBaseSession(session_pool=session_maker)
)


# FSM для добавления материала
class AddMaterial(StatesGroup):
    # Шаги состояний
    category_name = State()
    title = State()
    description = State()
    photo = State()
    packing = State()
    price = State()
    quantity = State()

    material_for_change = None

    texts_back = {
        "AddMaterial:category_name": "выберите категорию заново.",
        "AddMaterial:title": "Введите название заново.",
        "AddMaterial:description": "Введите описание заново.",
        "AddMaterial:photo": "Отправте изображение заново.",
        "AddMaterial:packing": "Укажите фасовку заново.",
        "AddMaterial:price": "Введите цену заново.",
        "AddMaterial:quantity": "Введите количество заново.",
    }

    texts_leave_as_is = {
        "AddMaterial:category_name": "Выберите категорию",
        "AddMaterial:title": "Введите описание материала",
        "AddMaterial:description": "Отправте изображение материала",
        "AddMaterial:photo": "Укажите фасовку материала",
        "AddMaterial:packing": "Введите цену материала",
        "AddMaterial:price": "Количество материала в наличие",
        "AddMaterial:quantity": "Данные о материале обновленны",
    }


@material_router.callback_query(
        StateFilter("*"), F.data == "material_step_back"
    )
async def note_back_step_handler(
    callback: CallbackQuery, state: FSMContext
) -> None:
    """Возврат на шаг назад"""
    current_state = await state.get_state()

    if current_state == AddMaterial.category_name:
        await callback.message.answer(
            "Предидущего шага нет, нужно выбрать категорию",
        )
        return

    previous = None
    for step in AddMaterial.__all_states__:

        if step.state == current_state:
            await state.set_state(previous)
            if previous.state == AddMaterial.category_name:
                keyboard = CHOISE_CATEGORY_ADMIN
            else:
                keyboard = MATERIAL_ADMIN_CHOISE_FOR_EDIT
            await callback.message.answer(
                "Ок, вы вернулись к прошлому шагу \n"
                f" {AddMaterial.texts_back[previous.state]}",
                reply_markup=keyboard
            )
            return
        previous = step


@material_router.callback_query(
        StateFilter("*"),
        F.data == "material_leave_as_is",
        )
async def material_leave_as_is(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
) -> None:
    """Возвратна шаг назад при заполнении FSM Note"""
    current_state = await state.get_state()

    if current_state == AddMaterial.quantity:
        keyboard = MATERIAL_ADMIN_AFTER_ADD
    else:
        keyboard = MATERIAL_ADMIN_CHOISE_FOR_EDIT

    if current_state == AddMaterial.material_for_change:
        await state.update_data(
            category_name=AddMaterial.material_for_change.category_name
        )
        await state.set_state(AddMaterial.title)

    elif current_state == AddMaterial.title:
        await state.update_data(title=AddMaterial.material_for_change.title)
        await state.set_state(AddMaterial.description)

    elif current_state == AddMaterial.description:
        await state.update_data(
            description=AddMaterial.material_for_change.description
        )
        await state.set_state(AddMaterial.photo)

    elif current_state == AddMaterial.photo:
        await state.update_data(photo=AddMaterial.material_for_change.photo)
        await state.set_state(AddMaterial.packing)

    elif current_state == AddMaterial.packing:
        await state.update_data(
            packing=AddMaterial.material_for_change.packing)
        await state.set_state(AddMaterial.price)

    elif current_state == AddMaterial.price:
        await state.update_data(
            price=AddMaterial.material_for_change.price
        )
        await state.set_state(AddMaterial.quantity)

    elif current_state == AddMaterial.quantity:
        await state.update_data(
            quantity=AddMaterial.material_for_change.quantity
        )

        data = await state.get_data()
        await orm_update_material(
                session, AddMaterial.material_for_change.id, data
            )
        await callback.message.answer_photo(
            data["photo"],
            caption=(
                f"<b>Материал изменен в базе данных</b>\n"
                f"Название: <b>{data["title"]}\n</b>"
                f"Описание: <b>{data["description"]}\n</b>"
                f"Фасовка: <b>{data["packing"]}\n</b>"
                f"Цена: <b>{data["price"]}\n</b>"
                f"Количество: <b>{data["quantity"]}\n</b>"
                f"Категория: <b>{data["category_name"]}\n</b>"
            ),
            reply_markup=keyboard
        )
        await state.clear()

    if current_state != AddMaterial.quantity:
        await callback.message.answer(
            "Оставили как есть.\n"
            f"{AddMaterial.texts_leave_as_is[current_state]}",
            reply_markup=keyboard
        )


@material_router.callback_query(
        StateFilter(None), F.data == "admin_material_list"
    )
async def admin_material_category(
    callback: CallbackQuery, session: AsyncSession
) -> None:
    """Выбор категории материалов для администратора"""
    await callback.answer()
    media = await get_media_banner(session, menu_name="material_entries")
    if not media:
        await callback.message.answer(
            "<b>Необходимо добавить баннер</b>", reply_markup=ADMIN_MENU_KB
        )
    if callback.message.photo:
        await callback.message.edit_media(
            media=media,
            reply_markup=CHOISE_CATEGORY_FOR_CHANGE
        )
    else:
        await callback.message.answer_photo(
            media.media,
            media.caption,
            reply_markup=CHOISE_CATEGORY_FOR_CHANGE
        )


@material_router.callback_query(
        F.data.startswith("change_material_"),
    )
async def change_material_callback(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
) -> None:
    """Выбор категории для изменения материала"""
    material_id = callback.data.split("_")[-1]

    material_for_change = await orm_get_material(session, int(material_id))

    AddMaterial.material_for_change = material_for_change

    await callback.answer()
    if callback.message.photo:
        await callback.bot.edit_message_caption(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            caption="Выерите категорию материала",
            reply_markup=CHOISE_CATEGORY_ADMIN
        )
    else:
        media = await get_media_banner(session, menu_name="material_entries")
        await callback.message.answer_photo(
            media.media,
            media.caption,
            reply_markup=CHOISE_CATEGORY_ADMIN
        )
    await state.set_state(AddMaterial.category_name)


@material_router.callback_query(
        StateFilter(None),
        F.data == "add_material"
    )
async def material_add_position(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
) -> None:
    """Выбор категории для добавления материала"""
    if callback.message.photo:
        await callback.bot.edit_message_caption(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            caption="Выерите категорию материала",
            reply_markup=CHOISE_CATEGORY_ADMIN
        )
    else:
        await callback.answer()
        media = await get_media_banner(session, menu_name="material_entries")
        await callback.message.answer_photo(
            media.media,
            media.caption,
            reply_markup=CHOISE_CATEGORY_ADMIN
        )
    await state.set_state(AddMaterial.category_name)


@material_router.callback_query(
        AddMaterial.category_name,
        or_f(
            F.data == "admin ceratin_botox",
            F.data == "admin cold_recovery",
            F.data == "admin home_care",
        )
    )
async def material_add_category(
    callback: CallbackQuery, state: FSMContext
) -> None:
    """Выбор категории для материала"""
    name = callback.data.split(" ")[1]
    await state.update_data(category_name=name)
    if AddMaterial.material_for_change:
        keyboard = MATERIAL_ADMIN_CHOISE_FOR_EDIT
    else:
        keyboard = None
    if callback.message.photo:
        await callback.bot.edit_message_caption(

            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            caption=LEXICON_MATERIAL["material_add"],
            reply_markup=keyboard
        )
    else:
        await callback.message.answer(
            LEXICON_MATERIAL["material_add"],
            reply_markup=keyboard
        )
    await state.set_state(AddMaterial.title)


@material_router.message(AddMaterial.title, F.text)
async def material_add_position_title(
    message: Message, state: FSMContext
) -> None:
    """При корректном вводе названия"""
    await message.delete()
    if len(message.text) >= 50:
        await message.answer(
            caption=LEXICON_MATERIAL["material_add_long_name"],
        )
        return
    if AddMaterial.material_for_change:
        keyboard = MATERIAL_ADMIN_CHOISE_FOR_EDIT
    else:
        keyboard = None
    await state.update_data(title=message.text)
    await message.answer(
        LEXICON_MATERIAL["material_add_input_description"],
        reply_markup=keyboard
    )
    await state.set_state(AddMaterial.description)


@material_router.message(AddMaterial.title)
async def material_add_title_wrong(message: Message) -> None:
    """При некорректном вводе названия"""
    await message.bot.edit_message_caption(

        chat_id=message.chat.id,
        message_id=message.message_id,
        caption=LEXICON_MATERIAL["material_add_title_wrong"],
    )


@material_router.message(AddMaterial.description, F.text)
async def material_add_position_description(
    message: Message, state: FSMContext
) -> None:
    """При корректном вводе описания"""
    if AddMaterial.material_for_change:
        keyboard = MATERIAL_ADMIN_CHOISE_FOR_EDIT
    else:
        keyboard = None
    await state.update_data(description=message.text)
    await message.delete()
    await message.answer(
        LEXICON_MATERIAL["material_add_input_photo"],
        reply_markup=keyboard
    )
    await state.set_state(AddMaterial.photo)


@material_router.message(AddMaterial.description)
async def material_add_description_wrong(message: Message) -> None:
    """При некорректном вводе описания"""
    await message.answer(
        LEXICON_MATERIAL["material_add_description_wrong"],
    )


@material_router.message(AddMaterial.photo, F.photo)
async def material_add_position_photo(
    message: Message, state: FSMContext
) -> None:
    """При корректном вводе фото"""
    if AddMaterial.material_for_change:
        keyboard = MATERIAL_ADMIN_CHOISE_FOR_EDIT
    else:
        keyboard = None
    await message.delete()
    await state.update_data(photo=message.photo[-1].file_id)
    await message.answer(
        LEXICON_MATERIAL["material_add_input_packing"],
        reply_markup=keyboard
        )
    await state.set_state(AddMaterial.packing)


@material_router.message(AddMaterial.photo)
async def material_add_photo_wrong(
    message: Message, state: FSMContext
) -> None:
    """При некорректном вводе фото"""
    await state.update_data(photo=message.photo[-1].file_id)
    await message.answer(LEXICON_MATERIAL["material_add_photo_wrong"])


@material_router.message(AddMaterial.packing, F.text)
async def material_add_position_packing(
    message: Message, state: FSMContext
) -> None:
    """При корректном вводе упаковки"""
    if AddMaterial.material_for_change:
        keyboard = MATERIAL_ADMIN_CHOISE_FOR_EDIT
    else:
        keyboard = None
    await message.delete()
    answer = message.text.replace(",", ".")
    if float(answer):
        await state.update_data(packing=float(answer))
        await message.answer(
            LEXICON_MATERIAL["material_add_input_price"],
            reply_markup=keyboard
        )
    else:
        await message.answer(LEXICON_MATERIAL["material_add_packing_wrong"])
        return
    await state.set_state(AddMaterial.price)


@material_router.message(AddMaterial.packing)
async def material_add_packing_wrong(message: Message) -> None:
    """При некорректном вводе упаковки"""
    await message.delete()
    await message.bot.answer(LEXICON_MATERIAL["material_add_packing_wrong"])


@material_router.message(AddMaterial.price, F.text)
async def material_add_position_price(
    message: Message, state: FSMContext
) -> None:
    """При корректном вводе цены"""
    if AddMaterial.material_for_change:
        keyboard = MATERIAL_ADMIN_CHOISE_FOR_EDIT
    else:
        keyboard = None
    await message.delete()
    if message.text.isdigit():
        await state.update_data(price=int(message.text))
    else:
        await message.answer(
            LEXICON_MATERIAL["material_add_price_wrong"],
            reply_markup=keyboard
        )
        return
    await message.answer(LEXICON_MATERIAL["material_add_input_quantity"])
    await state.set_state(AddMaterial.quantity)


@material_router.message(AddMaterial.price)
async def material_add_price_wrong(message: Message) -> None:
    """При некорректном вводе цены"""
    await message.answer(LEXICON_MATERIAL["material_add_price_wrong"])


@material_router.message(AddMaterial.quantity, F.text)
async def material_add_position_quantity(
    message: Message,
    state: FSMContext,
    session: AsyncSession
) -> None:
    """Добавление нового материала в БД"""
    if message.text.isdigit():
        await state.update_data(quantity=int(message.text))
    else:
        await message.answer(LEXICON_MATERIAL["material_add_quantity_wrong"])
        return
    data = await state.get_data()
    category_name = data["category_name"]
    category_id = await orm_get_category_by_name(session, category_name)
    data["category_name"] = int(category_id.id)
    vidation_obj = await orm_get_material_by_title(
        session, data["title"], data["packing"]
    )

    if vidation_obj:
        await message.answer(
            LEXICON_MATERIAL["material_add_title_exists"],
            reply_markup=MATERIAL_ADMIN_AFTER_ADD
            )
        await state.clear()
        return
    try:
        if AddMaterial.material_for_change:
            if (
                vidation_obj and
                (vidation_obj.id != AddMaterial.material_for_change.id)
            ):
                await message.answer(
                    LEXICON_MATERIAL["material_add_title_exists"],
                    reply_markup=MATERIAL_ADMIN_AFTER_ADD
                    )
                await state.clear()
                return
            await orm_update_material(
                session,
                AddMaterial.material_for_change.id,
                data
            )
            await state.clear()
        else:
            if vidation_obj:
                await message.answer(
                    LEXICON_MATERIAL["material_add_title_exists"],
                    reply_markup=MATERIAL_ADMIN_AFTER_ADD
                    )
                await state.clear()
                return
            await orm_add_material(session, data)
        await message.answer_photo(
            photo=data["photo"],
            caption=(
                f"<b>Материал добавлен в базу данных</b>\n"
                f"Название: <b>{data["title"]}\n</b>"
                f"Описание: <b>{data["description"]}\n</b>"
                f"Фасовка: <b>{data["packing"]}\n</b>"
                f"Цена: <b>{data["price"]}\n</b>"
                f"Количество: <b>{data["quantity"]}\n</b>"
                f"Категория: <b>{category_name}\n</b>"
            ),
            reply_markup=MATERIAL_ADMIN_AFTER_ADD
        )
        await state.clear()
    except Exception as e:
        await message.answer(
            f"Произошла ошибка: {e}", reply_markup=MATERIAL_ADMIN_AFTER_ADD,
        )
        await state.clear()


@material_router.message(AddMaterial.quantity)
async def material_add_quantity_wrong(message: Message) -> None:
    """При некорректном вводе количества"""
    await message.answer(LEXICON_MATERIAL["material_add_quantity_wrong"])


@material_router.callback_query(F.data.startswith("delete_material_"))
async def material_delete(
    callback: CallbackQuery, session: AsyncSession
) -> None:
    """Удаляем материал"""
    record_id = callback.data.split("_")[-1]
    await orm_delete_material(session, int(record_id))

    await callback.answer("Материал удален")
    await callback.message.answer("Материал удален из базы данных.")


@material_router.callback_query(F.data == "list_for_buy_material")
async def material_buy_list(
    callback: CallbackQuery, session: AsyncSession
) -> None:
    """Получить список материалов для покупки"""
    await callback.answer()
    materials = await orm_get_materials_purchase(session)
    material_list = await collection_of_materials_list(materials)
    await callback.message.answer(
        f"Вот список для покпуки:\n\n{material_list}",
        reply_markup=MATERIAL_ADMIN_AFTER_ADD
    )


@material_router.callback_query(
        StateFilter(None), F.data.startswith("list_material_chacnge")
    )
async def choise_material_list_for_change_callback(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
) -> None:
    """Получить список материалов для изменения"""
    await callback.answer()
    category = await orm_get_category_by_name(
        session, callback.data.split(" ")[-1]
    )
    for material in await orm_get_material_by_category_id(
        session, int(category.id)
    ):
        await callback.message.answer(
            text=(
                f"<b>Название:</b> {material.title}\n\n"
                f"<b>Описание:</b> {material.description}\n"
                f"<b>Фасовка:</b> {material.packing}\n"
                f"<b>Цена:</b> {material.price}\n"
                f"<b>Количество:</b> {material.quantity}\n"
            ),
            reply_markup=get_callback_btns(
                btns={
                    "Убавить -1": MaterialCallBack(
                        action="minus_material",
                        material_id=material.id,
                        title=material.title,
                        description=material.description,
                        price=material.price,
                        quantity_material=material.quantity,
                        packing=material.packing
                    ).pack(),
                    "Прибавить +1": MaterialCallBack(
                        action="plus_material",
                        material_id=material.id,
                        title=material.title,
                        description=material.description,
                        price=material.price,
                        quantity_material=material.quantity,
                        packing=material.packing
                    ).pack(),
                    "Удалить": f"delete_material_{material.id}",
                    "Изменить": f"change_material_{material.id}",
                }
            ),
        )
    await callback.message.answer(
        f"ОК, вот список материалов категории {callback.data.split(" ")[-1]}⏫",
        reply_markup=MATERIAL_ADMIN_AFTER_ADD
    )


@material_router.callback_query(
        MaterialCallBack.filter(F.action == "plus_material")
    )
@material_router.callback_query(
        MaterialCallBack.filter(F.action == "minus_material")
    )
async def change_in_material_quantity(
    callback: CallbackQuery,
    callback_data: MaterialCallBack,
    session: AsyncSession
) -> None:
    """Изменение количества материала"""
    await callback.answer()
    if callback_data.action == "minus_material":
        if callback_data.quantity_material == 1:
            await callback.answer(text="Минимальное количество 1")
            return

    if callback_data.action == "plus_material":
        new_quantity = callback_data.quantity_material + 1
    else:
        new_quantity = callback_data.quantity_material - 1

    try:
        await material_fix_quantity(
            session,
            callback_data.material_id,
            new_quantity=new_quantity
        )
    except Exception as ex:
        await callback.answer("Произошла ошибка")
        print(ex)
        return

    await callback.message.edit_text(
        text=(
            f"<b>Название:</b> {callback_data.title}\n\n"
            f"<b>Описание:</b> {callback_data.description}\n"
            f"<b>Цена:</b> {callback_data.price}\n"
            f"<b>Количество:</b> {new_quantity}\n"
        ),
        reply_markup=get_callback_btns(
            btns={
                "Убавить -1": MaterialCallBack(
                    action="minus_material",
                    material_id=callback_data.material_id,
                    title=callback_data.title,
                    description=callback_data.description,
                    price=callback_data.price,
                    quantity_material=new_quantity,
                    packing=callback_data.packing
                ).pack(),
                "Прибавить +1": MaterialCallBack(
                    action="plus_material",
                    material_id=callback_data.material_id,
                    title=callback_data.title,
                    description=callback_data.description,
                    price=callback_data.price,
                    quantity_material=new_quantity,
                    packing=callback_data.packing
                ).pack(),
                "Удалить": f"delete_material_{callback_data.material_id}",
                "Изменить": f"change_material_{callback_data.material_id}",
            }
        ),
    )
