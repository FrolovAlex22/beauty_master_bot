from keyboards.reply import get_keyboard
from keyboards.inline import ProductCallBack, get_callback_btns
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


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


# АДМИНИСТРАТОР
ADMIN_MENU_KB = get_callback_btns(
    btns={
        "Календарь записей": "calendar_record",
        "Материалы": "admin_choise_material",
        "Мои заметки": "admin_note",
        "Добавить/Изменить баннер": "add_change_banner",
    },
    sizes=(2,),
)


# ПОЛЬЗОВАТЕЛЬ
USER_MENU_KB = get_callback_btns(
    btns={
        "Записи клиентов": "user_record",
        "Материалы для домашнего ухода": ProductCallBack().pack(),
        "Полезная информация от мастера": "user_note_list_choise_type",
    },
    sizes=(2,),
)


USER_RECORD_KB = get_callback_btns(
    btns={
        "Посмотреть дни в которые есть запись": "user_record_list",
        "Оставить заявку на прием": "user_record_bid",
        "Вернуться в главное меню": "main_menu",
    },
    sizes=(2,),
)


USER_SENDING_CONTACT_KB = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text="☎️Отправить номер для связи",
                request_contact=True
            ),
        ],
    ],
    resize_keyboard=True
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


MATERIAL_ADMIN_CHOISE_FOR_EDIT = get_callback_btns(
    btns={
        "Оставить как есть": "material_leave_as_is",
        "Вернуться на шаг назад": "material_step_back",
        },
    sizes=(2,)
)

# ЗАМЕТКИ
# Выбор действия для заметок
NOTE_ADMIN = get_callback_btns(
    btns={
        "Создать заметку": "add_note",
        "Мои заметки": "admin_list_note",
        "Опубликованные заметки": "admin_published_entries",
        "Меню администратора": "admin_menu",
    },
    sizes=(2,),
)


NOTE_CHOISE_TYPE = get_callback_btns(
    btns={
        "Подробно о материалах": "note material_info",
        "Полезно знать": "note good_to_know",
    },
    sizes=(2,),
)


NOTE_CHOISE_TYPE_BY_USER = get_callback_btns(
    btns={
        "Подробно о материалах": "user_note material_info",
        "Полезно знать": "user_note good_to_know",
        "Вернуться в главное меню": "main_menu",

    },
    sizes=(2,),
)


NOTE_EDIT_CHOISE_TYPE = get_callback_btns(
    btns={
        "Оставить как есть": "note_leave_as_is",
        "Вернуться на шаг назад": "note_step_back",
    },
    sizes=(2,),
)


NOTE_ADD_EDIT_PHOTO_STATE = get_keyboard(
    "Пропустить",
    "Оставить как есть",
    sizes=(2, )
)


NOTE_LIST_CHOISE_TYPE = get_callback_btns(
    btns={
        "Подробно о материалах": "note_list material_info",
        "Полезно знать": "note_list good_to_know",
    },
    sizes=(2,),
)


NOTE_ADMIN_AFTER_ADD = get_callback_btns(
    btns={
        "Создать заметку": "add_note",
        "Мои заметки": "admin_list_note",
        "Меню администратора": "admin_menu",
    },
    sizes=(2,),
)

NOTE_IS_PUBLISHED = get_callback_btns(
    btns={
        "Опубликовть": "publish_yes",
        "Оставить как черновик": "publish_no",
    },
    sizes=(2,),
)
