from aiogram import F, Router
from aiogram.types import ReplyKeyboardRemove
from aiogram.filters import Command, CommandStart, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import CallbackQuery, Message, FSInputFile
# from filters.filters import IsDigitCallbackData
# from keyboards.inlines_kb import create_calendar_keyboard, create_product_keyboard
# from keyboards.choise_kb import calendar_choise_ketboard
from keyboards.reply import get_keyboard
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
async def process_main_menu_command(message: Message):
    await message.answer(
        LEXICON[message.text],
        reply_markup=ADMIN_KB
    )

@router.message(Command(commands="calendar"))
@router.message(F.text == "Календарь записей")
async def calendar_menu(message: Message):
    await message.answer(
            text=LEXICON["select_action"],
            reply_markup=get_keyboard(
                "Добавить запись",
                "Удалить запись",
                "Мои записи",
                sizes=(1, )
            )
        )


class AddRecord(StatesGroup):
    # Шаги состояний
    name = State()
    phone_number = State()
    # date = State()

# необходим внедрить изменение даты записи
#    product_for_change = None


@router.message(StateFilter(None), F.text == "Добавить запись")
async def calendar_add_reception(message: Message, state: FSMContext):
    # Требует доработки запуск FSM в хендлере
    await message.answer(text=LEXICON['record_client'], reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(AddRecord.name)


@router.message(StateFilter("*"), F.text.casefold() == "отмена")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    # if AddProduct.product_for_change:
    #     AddProduct.product_for_change = None
    await state.clear()
    await message.answer("Действия отменены", reply_markup=ADMIN_KB)


@router.message(AddRecord.name, F.text)
async def calendar_add_name_client(message: Message, state: FSMContext):
    if len(message.text) >= 30:
        await message.answer(LEXICON_CALENDAR["calendar_add_long_name"])
        return
    await state.update_data(name=message.text)
    await message.answer(LEXICON_CALENDAR["calendar_add_input_name"])
    await state.set_state(AddRecord.phone_number)


@router.message(AddRecord.name)
async def calendar_wrong_name_client(message: Message, state: FSMContext):
    await message.answer(LEXICON_CALENDAR["calendar_wrong_name_client"])


@router.message(AddRecord.phone_number, F.text)
async def calendar_add_phone_number_client(message: Message, state: FSMContext):
    answer = message.text
    number = answer.replace("+", "").replace(" ", "").isnumeric()
    if number and len(number) == 11:
        await state.update_data(phone_number=number)
    else:
        await message.answer(
            LEXICON_CALENDAR["calendar_add_phone_number_invalid_data"]
        )
        return
    data = await state.get_data()
    await message.answer(
        text=f"Запись клиента добавлена\n"
             f"<b>Имя клиента:</b> {data["name"]}\n"
             f"<b>Номер клиента:</b> {data["phone_number"]}",
        reply_markup=ADMIN_KB
    )
    await state.clear()



@router.message(AddRecord.phone_number)
async def calendar_wrong_phone_number_client(message: Message, state: FSMContext):
    await message.answer(LEXICON_CALENDAR["calendar_wrong_phone_number_client"])


@router.message(F.text == "Удалить запись")
async def calendar_delete_reception(message: Message):
    # Требует доработки список записей для удаления
    await message.answer(text=LEXICON['pass'], reply_markup=ADMIN_KB
    )


@router.message(F.text == "Мои записи")
async def calendar_reception_list(message: Message):
    await message.answer(text=LEXICON['pass'], reply_markup=ADMIN_KB
    )


@router.message(Command(commands="material"))
@router.message(F.text == "Мои материалы")
async def material_menu(message: Message):
    await message.answer(
        text=LEXICON['select_action'],
        reply_markup=get_keyboard(
            "Добавить новую позицию в базу данных",
            "Спиок материалов",
            "Список для покупки",
            placeholder="Выберите действие",
            sizes=(1, )
        )
    )


class AddMaterial(StatesGroup):
    # Шаги состояний
    title = State()
    description = State()
    packing = State()
    price = State()
    quantity = State()


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
    await message.answer(
        LEXICON_MATERIAL["material_add_input_packing"]
    )
    await state.set_state(AddMaterial.packing)


@router.message(AddMaterial.description)
async def material_add_description_wrong(message: Message, state: FSMContext):
    await message.answer(
        LEXICON_MATERIAL["material_add_description_wrong"]
    )


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
    await message.answer(
        text=f"<b>Материал добавлен в базу данных</b>\n"
             f"Название: <b>{data["title"]}\n</b>"
             f"Описание: <b>{data["description"]}\n</b>"
             f"Фасовка: <b>{data["packing"]}\n</b>"
             f"Цена: <b>{data["price"]}\n</b>"
             f"Количество: <b>{data["quantity"]}\n</b>",
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
            "Удалить заметку",
            "Посмотреть список заметок",
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
            caption=f"<b>Заметка добавлена в базу данных</b>\n"
                f"Название: <b>{data['title']}\n</b>"
                f"Описание: <b>{data['description']}\n</b>",
            reply_markup=ADMIN_KB
        )
        await state.clear()
        return
    await message.answer(
        text=f"<b>Заметка добавлена в базу данных</b>\n"
             f"Название: <b>{data['title']}\n</b>"
             f"Описание: <b>{data['description']}\n</b>"
             f"Изображение: <b>Отсутствует</b>",
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
