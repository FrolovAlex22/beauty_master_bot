from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from sqlalchemy.ext.asyncio import AsyncSession

from database.methods import (
    orm_change_banner_image,
    # orm_get_categories,
    # orm_add_product,
    # orm_delete_product,
    orm_get_info_pages,
    # orm_get_product,
    # orm_get_products,
    # orm_update_product,
)

# from filters.chat_types import ChatTypeFilter, IsAdmin

from keyboards.inline import get_callback_btns
from keyboards.reply import get_keyboard
from keyboards.other_kb import ADMIN_KB



admin_router = Router()
# admin_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())


@admin_router.message(Command("admin"))
async def admin_features(message: types.Message):
    await message.answer("Что хотите сделать?", reply_markup=ADMIN_KB)


# @admin_router.message(F.text == 'Ассортимент')
# async def admin_features(message: types.Message, session: AsyncSession):
#     categories = await orm_get_categories(session)
#     btns = {category.name : f'category_{category.id}' for category in categories}
#     await message.answer("Выберите категорию", reply_markup=get_callback_btns(btns=btns))


# @admin_router.callback_query(F.data.startswith('category_'))
# async def starring_at_product(callback: types.CallbackQuery, session: AsyncSession):
#     category_id = callback.data.split('_')[-1]
#     for product in await orm_get_products(session, int(category_id)):
#         await callback.message.answer_photo(
#             product.image,
#             caption=f"<strong>{product.name}\
#                     </strong>\n{product.description}\nСтоимость: {round(product.price, 2)}",
#             reply_markup=get_callback_btns(
#                 btns={
#                     "Удалить": f"delete_{product.id}",
#                     "Изменить": f"change_{product.id}",
#                 },
#                 sizes=(2,)
#             ),
#         )
#     await callback.answer()
#     await callback.message.answer("ОК, вот список товаров ⏫")


# @admin_router.callback_query(F.data.startswith("delete_"))
# async def delete_product_callback(callback: types.CallbackQuery, session: AsyncSession):
#     product_id = callback.data.split("_")[-1]
#     await orm_delete_product(session, int(product_id))

#     await callback.answer("Товар удален")
#     await callback.message.answer("Товар удален!")


################# Микро FSM для загрузки/изменения баннеров ############################

class AddBanner(StatesGroup):
    image = State()

# Отправляем перечень информационных страниц бота и становимся в состояние отправки photo
@admin_router.message(StateFilter(None), F.text == 'Добавить/Изменить баннер')
async def add_image2(message: types.Message, state: FSMContext, session: AsyncSession):
    pages_names = [page.name for page in await orm_get_info_pages(session)]
    await message.answer(f"Отправьте фото баннера.\nВ описании укажите для какой страницы:\
                         \n{', '.join(pages_names)}")
    await state.set_state(AddBanner.image)

# Добавляем/изменяем изображение в таблице (там уже есть записанные страницы по именам:
# main, catalog, cart(для пустой корзины), about, payment, shipping
@admin_router.message(AddBanner.image, F.photo)
async def add_banner(message: types.Message, state: FSMContext, session: AsyncSession):
    image_id = message.photo[-1].file_id
    for_page = message.caption.strip()
    pages_names = [page.name for page in await orm_get_info_pages(session)]
    if for_page not in pages_names:
        await message.answer(f"Введите нормальное название страницы, например:\
                         \n{', '.join(pages_names)}")
        return
    await orm_change_banner_image(session, for_page, image_id,)
    await message.answer("Баннер добавлен/изменен.")
    await state.clear()

# ловим некоррекный ввод
@admin_router.message(AddBanner.image)
async def add_banner2(message: types.Message, state: FSMContext):
    await message.answer("Отправьте фото баннера или отмена")