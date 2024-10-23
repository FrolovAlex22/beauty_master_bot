from aiogram.utils.formatting import Bold, as_marked_section

CATEGORIES = [
    'ceratin_botox', 'cold_recovery', "home_care"
]

DESCRIPTION_FOR_INFO_PAGES = {
    "main": "Добро пожаловать в бот мастера Лианы!",
    "admin": "\U0001F60E Меню Администратора \U0001F60E",
    "about": (
        "Это бот ассистен, здесь вы можете посмотреть расписание моего графика"
        "\n\nТак же здесь можно ознакомитьс с товарами для домашнего ухода"),
    "material_entries": as_marked_section(
        Bold("Расписание на две недели:"),
        "Добавить новый материал",
        "Редактировать мои материалы",
        "Посмотреть список к покупке",
        marker="✅ ",
    ).as_html(),
    "material_list": "<b>Выберите категорию</b>",
    "calendar_entries": as_marked_section(
        Bold("Меню записей:"),
        "Посмотреть записи",
        "Добавить запись",
        marker="✅ ",
    ).as_html(),
    "information": as_marked_section(
            Bold("Полезные заметки мастера :"),
            "Что нужно знать о уходе за волосами",
            "Часто задаваемые вопросы",
            marker="✅ ",
        ).as_html(),
}
