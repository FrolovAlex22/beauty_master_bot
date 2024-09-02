from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from lexicon.lexicon_ru import LEXICON

calendar_list = KeyboardButton(text=LEXICON['add_reception'])
reception_list  = KeyboardButton(text=LEXICON['reception_list'])


calendar_builder = ReplyKeyboardBuilder()

calendar_builder.row(calendar_list, reception_list, width=1)

calendar_choise_ketboard: ReplyKeyboardMarkup = calendar_builder.as_markup(
    # one_time_keyboard=True,
    resize_keyboard=True
    )
