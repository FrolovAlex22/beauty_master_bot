from aiogram.utils.formatting import Bold, as_marked_section


LEXICON_COMMANDS: dict[str, str] = {
    "/main_menu": "Вернутся в главное меню",
    "/help": "Справка по работе бота",
    "/admin": "Меню администратора",
}

LEXICON: dict[str, str] = {
    # 'forward': '>>',
    # 'backward': '<<',
    "/start": (
        "<b>Добро пожаловать</b>\n\n<b>Это бот, ассистент, "
        "помошник бьюти мастера.</b>\n\nЗдесь вы можете вести записи ваших "
        "клиентов.\n\nВести учет материалов для работы\n\nДелать заметки, для "
        "будущих постов в соцсетях.\n\nПроверять мастеров города.\n\n"
        "Чтобы посмотреть список доступных команд - набери /help"
    ),

    "/help": (
        "<b>Доступные команды:</b>\n\n<b>/calendar</b> - Календарь записей\n"
        "<b>/material</b> - Остаток материалов\n"
        "<b>/notes</b> - Заметки для будущих постов\n"
        "<b>/check</b> - Список мастеров вашего города\n"
        "<b>/registration</b> - Зарегистрироваться\n"
        "<b>/main_menu</b> - Вернуться в главное меню для выбора действия"
    ),

    "/main_menu": "Вы вернулись в главное меню",

    "other_answer": (
        "Этот бот не для переписки. Бот помошник бьюти мастерам. "
        "Если вы хотите мной воспользоваться можете написать Лиане "
        "когда у нее хорошее настроение она добавляет новых пользователей ;)"),

    "record_client": (
        "Если нужно отменить офрмирование записи напишите <b>отмена</b>\n\n"
        "<b>Введите дату приема клиента</b>"
    ),

    "select_action": "Выберите действие",

    "check_list": "Каких мастеров будем проверять?",

    "pass": "Заглушка",
}


LEXICON_CALENDAR: dict[str, str] = {
    "calendar_add_invalid_date": (
        "Вы ввели не допустимые данные, введите дату записи заново"
    ),

    "calendar_add_long_name": (
        "Имя клиента не должно превышать 30 символов.\n Введите заново"
    ),

    "calendar_add_input_name": "Введите номер клиента",

    "calendar_wrong_name_client": (
        "Вы ввели не допустимые данные, введите имя клиента заново"
    ),

    "calendar_add_phone_number_invalid_len_phone": (
        "Длинна телефона должна быть 11 цифр. "
        "Допускаеться наличие знаков '+' и ' '"
    ),

    "calendar_wrong_phone_number_client": (
        "Вы ввели не допустимые данные, введите номер телефона клиента заново"
    ),
}

LEXICON_MATERIAL: dict[str, str] = {
    "material_add_long_name": (
        "Название материала не должно превышать 50 символов.\n Введите заново"
    ),

    "material_add": (
        "Если нужно отменить добавление материала напишите <b>отмена</b>\n\n"
        "<b>Введите название продукта</b>"
    ),

    "material_add_input_description": "<b>Введите описание товара.</b>",

    "material_add_title_wrong": (
        "Вы ввели не допустимые данные, введите текстом названия товара"
    ),

    "material_add_input_photo": "<b>Добавте изображения продукции</b>",

    "material_add_photo_wrong": (
        "Вы ввели не допустимые данные, добавте фотографию продукции"
    ),

    "material_add_input_packing": "<b>Введите вес/объем товара.</b>",

    "material_add_description_wrong": (
        "Вы ввели не допустимые данные, введите текстом описание товара"
    ),

    "material_add_packing_wrong": (
        "Вы ввели не допустимые данные, введите цифрами фасовку товара"
    ),

    "material_add_input_price": "<b>Введите цену товара.</b>",

    "material_add_price_wrong": (
        "Вы ввели не допустимые данные, введите цифрами цену товара"
    ),

    "material_add_input_quantity": "<b>Введите количество материала.</b>",

    "material_add_quantity_wrong": (
        "Вы ввели не допустимые данные, введите цифрами количество товара"
    ),

    "material_add_title_exists": (
        "Материал с таким названием, и фасовкой. Уже существует"
    ),

    "user_action_selection": as_marked_section(
        Bold("Меню записей:"),
        "Список бронированных записей",
        "Оставить заявку на запись",
        marker="✅ ",
    ).as_html(),

    "user_check_date": "<b>Выберите дату приема</b>",
}

LEXICON_NOTES: dict[str, str] = {

    "notes_add": (
        "Если нужно отменить добавление заметки напишите <b>отмена</b>\n\n"
        "<b>Выберите тип заметок</b>\U0001F9D0"
    ),

    "notes_add_title": (
        "<b>Введите название заметки</b>"
    ),

    "notes_add_title_wrong": (
        "<b>Вы ввели не допустимые данные, введите название заметки</b>"
    ),

    "notes_add_input_description": "<b>Введите описание заметки.</b>",

    "notes_add_description_wrong": (
        "<b>Вы ввели не допустимые данные, введите описание заметки</b>"
    ),

    "notes_add_input_image": "<b>Добавте изображение для заметки.</b>",

    "notes_add_image_wrong": (
        "<b>Вы ввели не допустимые данные, нужно добавить изображение</b>"
        "<b> или пропсутить этот шаг нажав на кнопку 'пропустить'</b>"
    ),

    "notes_list_by_user": as_marked_section(
        Bold("Выберите тип статей:"),
        "Подробно о материалах",
        "Полезно знать",
        marker="✅ ",
    ).as_html(),
}
