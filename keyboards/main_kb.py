from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from lexicon.lexicon_ru import LEXICON, LEXICON_BUTTONS

calendar_button = KeyboardButton(text=LEXICON_BUTTONS['calendar_button'])
material_button = KeyboardButton(text=LEXICON_BUTTONS['material_button'])
notes_button = KeyboardButton(text=LEXICON_BUTTONS['notes_button'])
check_masters = KeyboardButton(text=LEXICON_BUTTONS['check_masters_button'])


start_kb_builder = ReplyKeyboardBuilder()

start_kb_builder.row(
    calendar_button, material_button, notes_button, check_masters, width=1
)

start_no_kb: ReplyKeyboardMarkup = start_kb_builder.as_markup(
    # one_time_keyboard=True,
    resize_keyboard=True
    )
