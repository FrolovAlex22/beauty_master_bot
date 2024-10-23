from aiogram.filters.callback_data import CallbackData
from aiogram.types import InputMediaPhoto


from database.methods import (
    orm_get_banner,
    orm_get_category_by_name,
    orm_get_material_by_category_id,
)
from keyboards.inline import get_products_btns
from utils.paginator import Paginator


class MaterialCallBack(CallbackData, prefix="material"):
    quantity_material: int = None
    title: str
    description: str
    packing: float
    price: int
    action: str
    material_id: int


async def get_media_banner(session, menu_name):
    """Получить изображение и описание баннера"""
    banner = await orm_get_banner(session, page=menu_name)
    if not banner.image:
        return None
    image = InputMediaPhoto(media=banner.image, caption=banner.description)

    return image


async def collection_of_materials_list(materials: dict):
    """Формирование списка материалов"""
    if len(materials) == 0:
        return "Список пуст"
    materials_list = ""
    for number, material in enumerate(materials):
        materials_list += (
            f"<b>{number+1}</b> .Название: <b>{material.title}</b>, "
            f"Количество: <b>{material.quantity}</b>\n"
        )
    return materials_list


async def client_reception_in_the_list(records: tuple):
    """Формирование текста для списка записей клиентов"""
    text = "Дни в которые уже есть записи:\n\n"
    for record in records:
        text += f"<b>{record.date.strftime('%d.%m.%Y')}</b>\n"
    return text


def pages(paginator: Paginator):
    """Кнопки для пагинации"""
    btns = dict()
    if paginator.has_previous():
        btns["◀ Пред."] = "previous"

    if paginator.has_next():
        btns["След. ▶"] = "next"

    return btns


async def products(session, page):
    """Получение списка продуктов категории домашний уход"""
    category_id = await orm_get_category_by_name(session, "home_care")
    products = await orm_get_material_by_category_id(
        session, category_id=category_id.id
    )

    paginator = Paginator(products, page=page)
    product = paginator.get_page()[0]

    image = InputMediaPhoto(
        media=product.photo,
        caption=f"<strong>{product.title}"
                f"</strong>\n{product.description}\n"
                f"Стоимость: {round(product.price, 2)}\n"
                f"<strong>Товар {paginator.page}"
                f" из {paginator.pages}</strong>",
    )

    pagination_btns = pages(paginator)

    kbds = get_products_btns(
        # level=level,
        # category=category,
        page=page,
        pagination_btns=pagination_btns,
        # product_id=product.id,
    )

    return image, kbds
