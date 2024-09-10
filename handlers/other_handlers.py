from aiogram import Router
from aiogram.types import Message

from handlers.user_handlers import ADMIN_KB
from lexicon.lexicon_ru import LEXICON

router = Router()


# Этот хэндлер будет реагировать на любые сообщения пользователя,
# не предусмотренные логикой работы бота
@router.message()
async def send_echo(message: Message):
    await message.answer(LEXICON["other_answer"], reply_markup=ADMIN_KB)