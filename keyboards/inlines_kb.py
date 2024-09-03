from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon_ru import LEXICON


def add_or_delete_reception_keyboard() -> InlineKeyboardMarkup:
    # Создаем объект клавиатуры с библиотекой полезной информации
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(InlineKeyboardButton(
        text=LEXICON['add_reception'],
    ))
    kb_builder.row(InlineKeyboardButton(
        text=LEXICON['delete_reception'],
    ))
    return kb_builder.as_markup()
