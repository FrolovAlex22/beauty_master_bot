from aiogram import Router
from aiogram.types import Message

router = Router()


# Этот хэндлер будет реагировать на любые сообщения пользователя,
# не предусмотренные логикой работы бота
@router.message()
async def send_echo(message: Message):
    await message.answer(
        'Этот бот не для переписки. Бот помошник бьюти мастерам. '
        'Если вы хотите мной воспользоваться можете написать Лиане '
        'когда у нее хорошее настроение она добавляет новых пользователей ;)'
        )