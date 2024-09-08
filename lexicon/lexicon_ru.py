LEXICON_COMMANDS: dict[str, str] = {
    '/calendar': 'Календарь записей',
    '/material': 'Остаток материалов',
    '/notes': 'Заметки для будущих постов в социальных сетях',
    '/check': 'Проверить мастеров города',
    '/help': 'Справка по работе бота',
    '/registration': 'регистрация',
}

LEXICON: dict[str, str] = {
    # 'forward': '>>',
    # 'backward': '<<',
    '/start': '<b>Добро пожаловать</b>\n\nЭто бот, ассистент, '
              'помошник бьюти мастера.\n\nЗдесь вы можете вести записи ваших '
              'клиентов\nВести учет материалов для работы\nДелать заметки, для '
              'будущих постов в соцсетях\nПроверять мастеров города\n'
              'Чтобы посмотреть список доступных команд - набери /help',
    '/help': '<b>Доступные команды:\n\n/calendar - Календарь записей\n'
             '/material - Остаток материалов\n'
             '/notes - Заметки для будущих постов'
             '/check - Список мастеров вашего города'
             '/registration - Зарегистрироваться',
    '/registration': 'Для вашего удобства вы можете зарегистрироваться\n'
                     'введите ваше имя',

    # '/library': f'<b>{_LIBRARY_TEXT}</b>',
    # 'product': 'В продаже имеються товары предназначенный для лечения гепатита '
    # 'С\n все препараты приобретаються напрямую у дестребьюторов',
    # 'library_button': 'Полезные статьи',
    # 'no_library': '<b>Библиотека на данный момент пуста</b>',
    # 'product_button': 'ознакомиться с нашей продукцией',
    # 'no_product': '<b>Товары еще не добавлены в продажу</b>',
    # 'formtosend': 'Заполнить форму для заказа продукции',
    'select_action': 'Выберите действие',
    'reception_list': "Список записей",
    'add_or_delete_reception': 'Добавить или удалить запись',
    'add_reception': 'Добавить запись',
    'delete_reception': 'Удалить запись',
    'add_or_delete_position': 'Добавить позицию материала',
    'list_materials': 'Список материалов',
    'pass': 'Заглушка',

}

LEXICON_BUTTONS: dict[str, str] = {
    'calendar_button': 'Календарь записей',
    'material_button': 'Мои материалы',
    'notes_button': 'Заметки для соц. сетей',
    'check_masters_button': 'Мастера города',
}