from aiogram import F, Router
from aiogram.types import ReplyKeyboardRemove
from aiogram.filters import StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession
from database.methods import orm_add_material, orm_get_materials, orm_get_material, orm_delete_material, orm_update_material

from database.engine import session_maker
from keyboards.reply import get_keyboard
from keyboards.inline import get_callback_btns
from keyboards.other_kb import CHANGE_MATERIAL_KB, ADMIN_KB, MATERIAL_KB
from lexicon.lexicon_ru import LEXICON, LEXICON_MATERIAL

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

    texts = {
        "AddMaterial:title": "Введите название заново:",
        "AddMaterial:description": "Введите описание заново:",
        "AddMaterial:photo": "Отправте изображение заново:",
        "AddMaterial:packing": "Укажите фасовку заново:",
        "AddMaterial:price": "Введите цену заново:",
        "AddMaterial:quantity": "Введите количество заново:",
    }


@material_router.callback_query(StateFilter(None), F.data.startswith("change_material_"))
async def change_material_callback(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
):
    material_id = callback.data.split("_")[-1]

    material_for_change = await orm_get_material(session, int(material_id))

    AddMaterial.material_for_change = material_for_change

    await callback.answer()
    await callback.message.answer(
        "Введите название товара", reply_markup=CHANGE_MATERIAL_KB
    )
    await state.set_state(AddMaterial.title)


@material_router.message(
        StateFilter("*"),
        F.text == "Вернуться на шаг"
    )
async def back_step_handler_material(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()


    if current_state == AddMaterial.title:
        await message.answer(
            'Предидущего шага нет, или введите название продукта или'
            ' напишите "отмена"'
        )
        return

    previous = None
    for step in AddMaterial.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(
                "Ок, вы вернулись к прошлому шагу \n"
                f" {AddMaterial.texts[previous.state]}"
            )
            return
        previous = step

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


@material_router.message(
        StateFilter(None),
        F.text == "Добавить материал в базу данных"
    )
async def material_add_position(message: Message, state: FSMContext):
    await message.answer(
        LEXICON["material_add"],
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(AddMaterial.title)


@material_router.message(AddMaterial.title, F.text)
async def material_add_position_title(message: Message, state: FSMContext):
    if len(message.text) >= 50:
        await message.answer(LEXICON_MATERIAL["material_add_long_name"])
        return
    if message.text == "Оставить как есть" and AddMaterial.material_for_change:
        await state.update_data(title=AddMaterial.material_for_change.title)
        await message.answer(
            LEXICON_MATERIAL["material_add_input_description"],
            reply_markup=CHANGE_MATERIAL_KB
        )
    else:
        await state.update_data(title=message.text)
        await message.answer(LEXICON_MATERIAL["material_add_input_description"])
    await state.set_state(AddMaterial.description)


@material_router.message(AddMaterial.title)
async def material_add_title_wrong(message: Message, state: FSMContext):
    await message.answer(LEXICON_MATERIAL["material_add_title_wrong"])


@material_router.message(AddMaterial.description, F.text)
async def material_add_position_description(message: Message, state: FSMContext):
    if message.text == "Оставить как есть" and AddMaterial.material_for_change:
        await state.update_data(
            description=AddMaterial.material_for_change.description
        )
        await message.answer(
            LEXICON_MATERIAL["material_add_input_photo"],
            reply_markup=CHANGE_MATERIAL_KB
            )
    else:
        await state.update_data(description=message.text)
        await message.answer(LEXICON_MATERIAL["material_add_input_photo"])
    await state.set_state(AddMaterial.photo)


@material_router.message(AddMaterial.description)
async def material_add_description_wrong(message: Message, state: FSMContext):
    await message.answer(LEXICON_MATERIAL["material_add_description_wrong"])


@material_router.message(
        AddMaterial.photo,
        or_f(F.photo, F.text == "Оставить как есть")
    )
async def material_add_position_photo(message: Message, state: FSMContext):
    if message.text == "Оставить как есть" and AddMaterial.material_for_change:
        await state.update_data(
            photo=AddMaterial.material_for_change.photo
        )
        await message.answer(
            LEXICON_MATERIAL["material_add_input_packing"],
            reply_markup=CHANGE_MATERIAL_KB
            )
    else:
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
    if message.text == "Оставить как есть" and AddMaterial.material_for_change:
        await state.update_data(
            packing=AddMaterial.material_for_change.packing
        )
        await message.answer(
            LEXICON_MATERIAL["material_add_input_price"],
            reply_markup=CHANGE_MATERIAL_KB
        )
    else:
        answer = message.text.replace(",", ".")
        if float(answer):
            await state.update_data(packing=float(answer))
            await message.answer(
                LEXICON_MATERIAL["material_add_input_price"]
            )
        else:
            await message.answer(LEXICON_MATERIAL["material_add_packing_wrong"])
            return
    await state.set_state(AddMaterial.price)


@material_router.message(AddMaterial.packing)
async def material_add_packing_wrong(message: Message, state: FSMContext):
    await message.answer(LEXICON_MATERIAL["material_add_packing_wrong"])


@material_router.message(AddMaterial.price, F.text)
async def material_add_position_price(message: Message, state: FSMContext):
    if message.text == "Оставить как есть" and AddMaterial.material_for_change:
        await state.update_data(
            price=AddMaterial.material_for_change.price
        )
        await message.answer(
            LEXICON_MATERIAL["material_add_input_quantity"],
            reply_markup=CHANGE_MATERIAL_KB
        )
    else:
        if message.text.isdigit():
            await state.update_data(price=int(message.text))
        else:
            await message.answer(LEXICON_MATERIAL["material_add_price_wrong"])
            return
        await message.answer(LEXICON_MATERIAL["material_add_input_quantity"])
    await state.set_state(AddMaterial.quantity)


@material_router.message(AddMaterial.price)
async def material_add_price_wrong(message: Message, state: FSMContext):
    await message.answer(LEXICON_MATERIAL["material_add_price_wrong"])


@material_router.message(AddMaterial.quantity, F.text)
async def material_add_position_price(
    message: Message,
    state: FSMContext,
    session: AsyncSession
):
    if message.text == "Оставить как есть" and AddMaterial.material_for_change:
        await state.update_data(
            quantity=AddMaterial.material_for_change.quantity
        )
    else:
        if message.text.isdigit():
            await state.update_data(quantity=int(message.text))
        else:
            await message.answer(LEXICON_MATERIAL["material_add_price_wrong"])
            return
    data = await state.get_data()
    try:
        if AddMaterial.material_for_change:
            await orm_update_material(
                session,
                AddMaterial.material_for_change.id,
                data
            )
            await state.clear()
        else:
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
            ),
            reply_markup=MATERIAL_KB
        )
        await state.clear()
    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}", reply_markup=ADMIN_KB,)
        await state.clear()


@material_router.message(AddMaterial.quantity)
async def material_add_price_wrong(message: Message, state: FSMContext):
    await message.answer(LEXICON_MATERIAL["material_add_price_wrong"])


@material_router.callback_query(F.data.startswith("delete_material_"))
async def material_add_position(callback: CallbackQuery, session: AsyncSession):
    record_id = callback.data.split("_")[-1]
    await orm_delete_material(session, int(record_id))

    await callback.answer("Материал удален")
    await callback.message.answer("Материал удален из базы данных.")


@material_router.message(F.text == "Спиок материалов")
async def material_add_position(message: Message, session: AsyncSession):
    for material in await orm_get_materials(session):
        await message.answer_photo(
                photo=material.photo,
                caption=(
                    f"Название: <b>{material.title}\n</b>"
                    f"Описание: <b>{material.description}\n</b>"
                    f"Фасовка: <b>{material.packing}\n</b>"
                    f"Цена: <b>{material.price}\n</b>"
                    f"Количество: <b>{material.quantity}\n</b>"
                ),
                reply_markup=get_callback_btns(
                btns={
                        "Удалить": f"delete_material_{material.id}",
                        "Изменить": f"change_material_{material.id}",
                    }
                ),
            )
    await message.answer(
        "ОК, вот список записей ⏫",
        reply_markup=get_keyboard("Мои материалы", "Главное меню", sizes=(1, ))
    )


@material_router.message(F.text == "Список для покупки")
async def material_add_position(message: Message):
    await message.answer(text=LEXICON['pass'], reply_markup=ADMIN_KB)