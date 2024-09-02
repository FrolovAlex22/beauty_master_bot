# from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
# from aiogram.utils.keyboard import InlineKeyboardBuilder
# from database.database import library_of_articles, products_in_sale


# def create_lybrary_keyboard() -> InlineKeyboardMarkup:
#     # Создаем объект клавиатуры с библиотекой полезной информации
#     kb_builder = InlineKeyboardBuilder()
#     for _, meaning in library_of_articles.items():
#         text = meaning[0]
#         url = meaning[1]
#         kb_builder.row(InlineKeyboardButton(
#             text=f'{text[:100]}',
#             url=url
#         ))
#     return kb_builder.as_markup()