from aiogram.utils.formatting import Bold, as_list, as_marked_section

DESCRIPTION_FOR_INFO_PAGES = {
    "main": "Добро пожаловать в бот мастера Лианы!",
    "about": (
        "Это бот ассистен, здесь вы можете посмотреть расписание моего графика."
        "\n\nТак же здесь можно ознакомитьс с товарами для домашнего ухода"),
    "calendar_entries": as_marked_section(
        Bold("Расписание на вде недели:"),
        "Посмотреть записи",
        "Записаться на прием",
        marker="✅ ",
    ).as_html(),
    # as_marked_section(Bold("Нельзя:"), "Почта", "Голуби", marker="❌ "),
    # sep="\n----------------------\n",
    "information": as_marked_section(
            Bold("Полезные заметки мастера :"),
            "Что нужно знать о уходе за волосами",
            "Часто задаваемые вопросы",
            marker="✅ ",
        ).as_html(),
    # 'catalog': 'Категории:',
    # 'cart': 'В корзине ничего нет!'
}
