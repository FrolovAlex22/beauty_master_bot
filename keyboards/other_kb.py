from keyboards.reply import get_keyboard
from keyboards.inline import get_callback_btns
from aiogram.types import KeyboardButton


ADMIN_KB = get_keyboard(
        "Календарь записей",
        "Мои материалы",
        "Заметки для соц. сетей",
        "Мастера города",
        placeholder="Выберите действие",
        sizes=(1, ),
)


# COMMANDS_RECORDS_KB = get_keyboard(
#     "Календарь записей",
#     "Главное меню",
#     sizes=(1, ),
# )




CHANGE_RECORD_KB = get_keyboard(
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


CHANGE_MATERIAL_KB = get_keyboard(
        "Оставить как есть",
        "Вернуться на шаг",
        sizes=(1, ),
)


MATERIAL_KB = get_keyboard(
    "Добавить материал в базу данных",
    "Спиок материалов",
    "Список для покупки",
    "Главное меню",
    sizes=(1, )
)


CHANGE_NOTE_KB = get_keyboard(
        "Оставить как есть",
        "Вернуться к предыдущему шагу",
        sizes=(1, ),
)


NOTE_KB = get_keyboard(
    "Добавить новую заметку",
    "Спиок заметок",
    "Главное меню",
    sizes=(1, )
)


CHECK_KB = get_keyboard(
	"Реконструкция волос",
	"Маникюр",
	"Ресницы",
    "Главное меню",
    sizes=(1, )
)

ADMIN_MENU_KB = get_keyboard(
    "Добавить/Изменить запись",
    # "Ассортимент",
    "Добавить/Изменить баннер",
    placeholder="Выберите действие",
    sizes=(2,),
)

CHANGE_RECORD_ADMIN = get_callback_btns(
    btns={
        "Добавить запись": "add_record",
        "Изменить запись": "list_from_change_record",
    },
    sizes=(2,),
)

CHANGE_RECORD_AFTER_FILING = get_callback_btns(
    btns={
        "Добавить запись": "add_record",
        "Список записей": "list_from_change_record",
    },
    sizes=(2,),
)
