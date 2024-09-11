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
from lexicon.lexicon_ru import (
    LEXICON,
    LEXICON_CALENDAR,
    LEXICON_MATERIAL,
    LEXICON_NOTES
)
# from database.database import library_of_articles, products_in_sale

router = Router()


ADMIN_KB = get_keyboard(
        "Календарь записей",
        "Мои материалы",
        "Заметки для соц. сетей",
        "Мастера города",
        placeholder="Выберите действие",
        sizes=(1, ),
)

CHANGE_KB = get_keyboard(
        "Оставить как есть",
        "Вернуться на шаг назад",
        sizes=(1, ),
)


RECORD_KB = get_keyboard(
    "Добавить запись",
    "Мои записи",
    "Главное меню",
    sizes=(1, )
)

@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(f"Hello, {message.from_user.full_name}!")
    await message.answer(
        text=LEXICON[message.text], reply_markup=ADMIN_KB
    )


@router.message(Command(commands="help"))
async def process_help_command(message: Message):
    await message.answer(LEXICON[message.text])


@router.message(Command(commands="main_menu"))
@router.message(F.text == "Главное меню")
async def process_main_menu_command(message: Message, state: FSMContext):
    # print(f"@@@@@@@@{AddRecord}")
    if state:
        await state.clear()
    await message.answer(
        LEXICON["/main_menu"],
        reply_markup=ADMIN_KB
    )

@router.message(Command(commands="calendar"))
@router.message(F.text == "Календарь записей")
async def calendar_menu(message: Message):
    await message.answer(
            text=LEXICON["select_action"],
            reply_markup=RECORD_KB
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
    if AddMaterial.material_for_change:
        AddMaterial.material_for_change = None
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


@router.message(Command(commands="material"))
@router.message(F.text == "Мои материалы")
async def material_menu(message: Message):
    await message.answer(
        text=LEXICON['select_action'],
        reply_markup=get_keyboard(
            "Добавить новую позицию в базу данных",
            "Спиок материалов",
            "Список для покупки",
            "Главное меню",
            placeholder="Выберите действие",
            sizes=(1, )
        )
    )


class AddMaterial(StatesGroup):
    # Шаги состояний
    title = State()
    description = State()
    photo = State()
    packing = State()
    price = State()
    quantity = State()

    material_for_change = None


@router.message(
        StateFilter(None),
        F.text == "Добавить новую позицию в базу данных"
    )
async def material_add_position(message: Message, state: FSMContext):
    await message.answer(
        LEXICON["material_add"],
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(AddMaterial.title)


@router.message(AddMaterial.title, F.text)
async def material_add_position_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer(LEXICON_MATERIAL["material_add_input_description"])
    await state.set_state(AddMaterial.description)


@router.message(AddMaterial.title)
async def material_add_title_wrong(message: Message, state: FSMContext):
    await message.answer(LEXICON_MATERIAL["material_add_title_wrong"])


@router.message(AddMaterial.description, F.text)
async def material_add_position_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer(LEXICON_MATERIAL["material_add_input_photo"])
    await state.set_state(AddMaterial.photo)


@router.message(AddMaterial.description)
async def material_add_description_wrong(message: Message, state: FSMContext):
    await message.answer(LEXICON_MATERIAL["material_add_description_wrong"])


@router.message(AddMaterial.photo, F.photo)
async def material_add_position_photo(message: Message, state: FSMContext):
    await state.update_data(photo=message.photo[-1].file_id)
    await message.answer(
        LEXICON_MATERIAL["material_add_input_packing"]
    )
    await state.set_state(AddMaterial.packing)


@router.message(AddMaterial.photo)
async def material_add_description_wrong(message: Message, state: FSMContext):
    await message.answer(LEXICON_MATERIAL["material_add_photo_wrong"])


@router.message(AddMaterial.packing, F.text)
async def material_add_position_packing(message: Message, state: FSMContext):
    answer = message.text
    if answer.replace(",", "").replace(".", "").isdigit():
        await state.update_data(packing=message.text)
    else:
        await message.answer(LEXICON_MATERIAL["material_add_packing_wrong"])
        return
    await message.answer(LEXICON_MATERIAL["material_add_input_price"])
    await state.set_state(AddMaterial.price)


@router.message(AddMaterial.packing)
async def material_add_packing_wrong(message: Message, state: FSMContext):
    await message.answer(LEXICON_MATERIAL["material_add_packing_wrong"])


@router.message(AddMaterial.price, F.text)
async def material_add_position_price(message: Message, state: FSMContext):
    answer = message.text
    if answer.isdigit():
        await state.update_data(price=message.text)
    else:
        await message.answer(LEXICON_MATERIAL["material_add_price_wrong"])
        return
    await message.answer(LEXICON_MATERIAL["material_add_input_quantity"])
    await state.set_state(AddMaterial.quantity)


@router.message(AddMaterial.price)
async def material_add_price_wrong(message: Message, state: FSMContext):
    await message.answer(LEXICON_MATERIAL["material_add_price_wrong"])


@router.message(AddMaterial.quantity, F.text)
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


@router.message(AddMaterial.quantity)
async def material_add_price_wrong(message: Message, state: FSMContext):
    await message.answer(LEXICON_MATERIAL["material_add_price_wrong"])

# ###################################################################

@router.message(F.text == "Удалить позицию")
async def material_add_position(message: Message):
    await message.answer(text=LEXICON['pass'], reply_markup=ADMIN_KB)


@router.message(F.text == "Спиок материалов")
async def material_add_position(message: Message):
    await message.answer(text=LEXICON['pass'], reply_markup=ADMIN_KB
    )


@router.message(F.text == "Список для покупки")
async def material_add_position(message: Message):
    await message.answer(text=LEXICON['pass'], reply_markup=ADMIN_KB)


@router.message(Command(commands="notes"))
@router.message(F.text == "Заметки для соц. сетей")
async def calendar_menu(message: Message):
    await message.answer(
        text=LEXICON['select_action'],
        reply_markup=get_keyboard(
            "Добавить новую заметку",
            "Посмотреть список заметок",
            "Главное меню",
            sizes=(1, )
            )
        )


class AddNotes(StatesGroup):
    title = State()
    description = State()
    image = State()


@router.message(StateFilter(None), F.text == "Добавить новую заметку")
async def notes_add(message: Message, state: FSMContext):
    await message.answer(
        LEXICON["notes_add"],
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(AddNotes.title)


@router.message(AddNotes.title, F.text)
async def notes_add_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer(LEXICON_NOTES["notes_add_input_description"])
    await state.set_state(AddNotes.description)


@router.message(AddNotes.title)
async def notes_add_title_wrong(message: Message, state: FSMContext):
    await message.answer(
        LEXICON_NOTES["notes_add_title_wrong"]
    )


@router.message(AddNotes.description, F.text)
async def notes_add_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer(
        LEXICON_NOTES["notes_add_input_image"],
        reply_markup=get_keyboard(
            "пропустить",
            sizes=(1, )
            )
    )
    await state.set_state(AddNotes.image)


@router.message(AddNotes.description)
async def notes_add_description_wrong(message: Message, state: FSMContext):
    await message.answer(LEXICON_NOTES["notes_add_description_wrong"])


@router.message(AddNotes.image, or_f(F.photo, F.text == "пропустить"))
async def notes_add_image(message: Message, state: FSMContext):
    if message.text == "пропустить":
        await state.update_data(image=None)
    else:
        await state.update_data(image=message.photo[-1].file_id)
    data = await state.get_data()
    if data['image']:
        await message.answer_photo(
            data['image'],
            caption=(
                f"<b>Заметка добавлена в базу данных</b>\n"
                f"Название: <b>{data['title']}\n</b>"
                f"Описание: <b>{data['description']}\n</b>"
            ),
            reply_markup=ADMIN_KB
        )
        await state.clear()
        return
    await message.answer(
        text=(
            f"<b>Заметка добавлена в базу данных</b>\n"
            f"Название: <b>{data['title']}\n</b>"
            f"Описание: <b>{data['description']}\n</b>"
            f"Изображение: <b>Отсутствует</b>"),
        reply_markup=ADMIN_KB
    )
    await state.clear()


@router.message(AddNotes.image)
async def notes_add_image_wrong(message: Message, state: FSMContext):
    await message.answer(
        LEXICON_NOTES["notes_add_image_wrong"],
        reply_markup=get_keyboard(
            "пропустить",
            sizes=(1, )
            )
    )


@router.message(F.text == "Удалить заметку")
async def material_add_position(message: Message):
    await message.answer(text=LEXICON['pass'], reply_markup=ADMIN_KB)


@router.message(F.text == "Посмотреть список заметок")
async def material_add_position(message: Message):
    await message.answer(text=LEXICON['pass'], reply_markup=ADMIN_KB)


@router.message(Command(commands="check"))
@router.message(F.text == "Мастера города")
async def calendar_menu(message: Message):
    await message.answer(text=LEXICON['pass'], reply_markup=get_keyboard(
        "Реконструкция волос",
        "Маникюр",
        "Ресницы",
        sizes=(1, )
        )
    )


@router.message(F.text == "Реконструкция волос")
async def material_add_position(message: Message):
    await message.answer(text=LEXICON['pass'], reply_markup=ADMIN_KB)


@router.message(F.text == "Маникюр")
async def material_add_position(message: Message):
    await message.answer(text=LEXICON['pass'], reply_markup=ADMIN_KB)


@router.message(F.text == "Ресницы")
async def material_add_position(message: Message):
    await message.answer(text=LEXICON['pass'], reply_markup=ADMIN_KB)
