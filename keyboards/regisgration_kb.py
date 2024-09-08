from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.markdown import hbold


def cancel_registration_kb() -> ReplyKeyboardMarkup:
    row = KeyboardButton(text="Отменить регистрацию")
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)