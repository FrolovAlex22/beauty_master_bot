from keyboards.reply import get_keyboard
from keyboards.inline import get_callback_btns
from aiogram.types import KeyboardButton

# Основное меню для пользователя
ADMIN_KB = get_keyboard(
        "Календарь записей",
        "Мои материалы",
        "Заметки для соц. сетей",
        "Мастера города",
        placeholder="Выберите действие",
        sizes=(1, ),
)

# Выбор дополнительного действия при заполнении FSM модели Record
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


CHANGE_MATERIAL_KB = get_callback_btns(
    btns={
        "Оставить как есть": "add_material_leave",
        "Вернуться на шаг": "add_material_back",
    },
    sizes=(2, ),
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


# КЛАВИАТУРЫ ДЛЯ АДМИНИСТРАТОРА!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
ADMIN_MENU_KB = get_callback_btns(
    btns={
        "Календарь записей": "calendar_record",
        "Мои материалы": "admin_choise_material",
        "Добавить/Изменить баннер": "add_change_banner",
    },
    # "Мои записи",
    # "Составы, материалы",
    # # "Ассортимент",
    # "Добавить/Изменить баннер",
    sizes=(2,),
)

# БАНЕРЫ
# Выбор после добавления банера
SELECTION_AFTER_ADDING_BANNER = get_callback_btns(
    btns={
        "Добавить баннер": "add_banner",
        "Меню администратора": "admin_menu",
    },
    sizes=(2,),
)

# КЛАВИАТУРЫ ЗАПИСИ
# Добавить/Изменить запись в меню администратора
ADD_OR_CHANGE_RECORD_ADMIN = get_callback_btns(
    btns={
        "Добавить запись": "add_record",
        "Список записей": "list_from_change_record",
        "Меню администратора": "admin_menu",
    },
    sizes=(2,),
)

# Изменить запись в меню администратора
RECORD_AFTER_FILING = get_callback_btns(
    btns={
        "Добавить запись": "add_record",
        "Список записей": "list_from_change_record",
        "Меню администратора": "admin_menu",
    },
    sizes=(2,),
)

# Изменить запись в меню администратора
RECORD_AFTER_LIST_RESORD = get_callback_btns(
    btns={
        "Добавить запись": "add_record",
        "Меню администратора": "admin_menu",
    },
    sizes=(2,),
)

# КАТЕГОРИИ
# Выбор категории
CHOISE_CATEGORY_ADMIN = get_callback_btns(
    btns={
        "Кератин/Ботокс": "admin ceratin_botox",
        "Холодное восттановление": "admin cold_recovery",
        "Домашний уход": "admin home_care",
    },
    sizes=(2,),
)



CHOISE_CATEGORY_FOR_CHANGE = get_callback_btns(
    btns={
        "Кератин/Ботокс": "list_material_chacnge ceratin_botox",
        "Холодное восттановление": "list_material_chacnge cold_recovery",
        "Домашний уход": "list_material_chacnge home_care",
    },
    sizes=(2,),
)

# МАТЕРИАЛЫ
# Выбор действия для материала
MATERIAL_ADMIN = get_callback_btns(
    btns={
        "Добавить составы": "add_material",
        "Список материалов": "admin_material_list",
        "Нужно докупить": "list_for_buy_material",
        "Меню администратора": "admin_menu",
    },
    sizes=(2,),
)


MATERIAL_ADMIN_AFTER_ADD = get_callback_btns(
    btns={
        "Добавить составы": "add_material",
        "Список материалов": "admin_material_list",
        "Меню администратора": "admin_menu",
    },
    sizes=(2,),
)
