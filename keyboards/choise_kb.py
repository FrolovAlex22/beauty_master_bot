from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from lexicon.lexicon_ru import LEXICON
from keyboards.keyboard_utils import make_row_keyboard

choise_list = [
    LEXICON['add_reception'],
    LEXICON['reception_list']
]


def calendar_choise_ketboard():
    return make_row_keyboard(choise_list)
