from aiogram.types import InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder


class ProductCallBack(CallbackData, prefix="user_product"):
    # level: int
    # menu_name: str
    # category: int | None = None
    page: int = 1
    product_id: int | None = None


def get_callback_btns(
    *,
    btns: dict[str, str],
    sizes: tuple[int] = (2,)
) -> InlineKeyboardBuilder:

    keyboard = InlineKeyboardBuilder()

    for text, data in btns.items():

        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))

    return keyboard.adjust(*sizes).as_markup()


def get_products_btns(
    *,
    page: int,
    pagination_btns: dict,
    sizes: tuple[int] = (2, 1)
):
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text='Назад', callback_data='main_menu'))

    keyboard.adjust(*sizes)

    row = []
    for text, menu_name in pagination_btns.items():
        if menu_name == "next":
            row.append(InlineKeyboardButton(
                text=text,
                callback_data=ProductCallBack(
                    page=page + 1).pack()))

        elif menu_name == "previous":
            row.append(InlineKeyboardButton(
                text=text,
                callback_data=ProductCallBack(

                        page=page - 1).pack()))

    return keyboard.row(*row).as_markup()
