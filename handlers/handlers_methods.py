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


# Получить изображение и описание баннера
async def get_media_banner(session, menu_name):
    banner = await orm_get_banner(session, page=menu_name)
    if not banner.image:
        return None
    image = InputMediaPhoto(media=banner.image, caption=banner.description)

    return image

# async def get_menu_content(
#     session: AsyncSession,
#     level: int,
#     menu_name: str,
#     category: int | None = None,
#     page: int | None = None,
#     product_id: int | None = None,
#     user_id: int | None = None,
# ):
#     if level == 0:
#         return await main_menu(session, level, menu_name)
#     elif level == 1:
#         return await catalog(session, level, menu_name)
#     elif level == 2:
#         return await products(session, level, category, page)
#     elif level == 3:
#         return await carts(session, level, menu_name, page, user_id, product_id)