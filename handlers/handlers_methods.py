from aiogram.filters.callback_data import CallbackData
from aiogram.types import InputMediaPhoto
from sqlalchemy.ext.asyncio import AsyncSession


from database.methods import (
    # orm_add_to_cart,
    # orm_delete_from_cart,
    orm_get_banner,
    orm_get_categories,
    # orm_get_products,
    # orm_get_user_carts,
    # orm_reduce_product_in_cart,
)
# from keyboards.inline import (
#     # get_products_btns,
#     # get_user_cart,
#     # get_user_catalog_btns,
#     # get_user_main_btns,
# )

# from utils.paginator import Paginator


class MaterialCallBack(CallbackData, prefix="material"):
    quantity_material: int = None
    title:str
    description:str
    packing:float
    price:int
    action: str
    material_id: int


# Получить изображение и описание баннера
async def get_media_banner(session, menu_name):
    banner = await orm_get_banner(session, page=menu_name)
    if not banner.image:
        return None
    image = InputMediaPhoto(media=banner.image, caption=banner.description)

    return image


async def collection_of_materials_list(materials: dict):
    if len(materials) == 0:
        return "Список пуст"
    materials_list = ""
    for number, material in enumerate(materials):
        materials_list += (
            f"<b>{number+1}</b> .Название: <b>{material.title}</b>, Количество:"
            f" <b>{material.quantity}</b>\n"
        )
    return materials_list


async def client_reception_in_the_list(records: tuple):
    text = "Дни в которые уже есть записи:\n\n"
    for record in records:
        text += f"<b>{record.date.strftime('%d.%m.%Y')}</b>\n"
    return text
