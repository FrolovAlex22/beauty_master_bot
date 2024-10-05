from datetime import datetime
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Category, Record, Material, Note, Banner


############################ Категории ######################################

async def orm_get_categories(session: AsyncSession):
    query = select(Category)
    result = await session.execute(query)
    return result.scalars().all()

async def orm_create_categories(session: AsyncSession, categories: list):
    query = select(Category)
    result = await session.execute(query)
    if result.first():
        return
    session.add_all([Category(name=name) for name in categories])
    await session.commit()

############### Работа с баннерами (информационными страницами) ###############

async def orm_add_banner_description(session: AsyncSession, data: dict):
    #Добавляем новый или изменяем существующий по именам
    #пунктов меню: main, about, cart, shipping, payment, catalog
    query = select(Banner)
    result = await session.execute(query)
    if result.first():
        return
    session.add_all([Banner(name=name, description=description) for name, description in data.items()])
    await session.commit()


async def orm_change_banner_image(session: AsyncSession, name: str, image: str):
    query = update(Banner).where(Banner.name == name).values(image=image)
    await session.execute(query)
    await session.commit()


async def orm_get_banner(session: AsyncSession, page: str):
    query = select(Banner).where(Banner.name == page)
    result = await session.execute(query)
    return result.scalar()


async def orm_get_info_pages(session: AsyncSession):
    query = select(Banner)
    result = await session.execute(query)
    return result.scalars().all()


############### Работа с записями клиентов ####################################

async def orm_add_record(session: AsyncSession, data: dict):
    date = datetime.strptime(data["date"], '%d.%m.%Y')
    obj = Record(
        name=data["name"],
        phone_number=data["phone_number"],
        date=date,
    )
    session.add(obj)
    await session.commit()



async def orm_get_records(session: AsyncSession):
    query = select(Record)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_record(session: AsyncSession, record_id: int):
    query = select(Record).where(Record.id == record_id)
    result = await session.execute(query)
    return result.scalar()


async def orm_update_record(session: AsyncSession, record_id: int, data):
    query = update(Record).where(Record.id == record_id).values(
        name=data["name"],
        phone_number=data["phone_number"],
        date=data["date"],
    )
    await session.execute(query)
    await session.commit()


async def orm_delete_record(session: AsyncSession, record_id: int):
    query = delete(Record).where(Record.id == record_id)
    await session.execute(query)
    await session.commit()


############### Работа с материаломи мастера ##################################

async def orm_add_material(session: AsyncSession, data: dict):
    obj = Material(
        title=data["title"],
        description=data["description"],
        photo=data["photo"],
        packing=data["packing"],
        price=data["price"],
        quantity=data["quantity"],
    )
    session.add(obj)
    await session.commit()



async def orm_get_materials(session: AsyncSession):
    query = select(Material)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_material(session: AsyncSession, material_id: int):
    query = select(Material).where(Material.id == material_id)
    result = await session.execute(query)
    return result.scalar()


async def orm_update_material(session: AsyncSession, material_id: int, data):
    query = update(Material).where(Material.id == material_id).values(
        title=data["title"],
        description=data["description"],
        photo=data["photo"],
        packing=data["packing"],
        price=data["price"],
        quantity=data["quantity"],
    )
    await session.execute(query)
    await session.commit()


async def orm_delete_material(session: AsyncSession, material_id: int):
    query = delete(Material).where(Material.id == material_id)
    await session.execute(query)
    await session.commit()


############### Работа с записями контента ####################################

async def orm_add_note(session: AsyncSession, data: dict):
    obj = Note(
        title=data["title"],
        description=data["description"],
        photo=data["photo"]
    )
    session.add(obj)
    await session.commit()



async def orm_get_notes(session: AsyncSession):
    query = select(Note)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_note(session: AsyncSession, note_id: int):
    query = select(Note).where(Note.id == note_id)
    result = await session.execute(query)
    return result.scalar()


async def orm_update_note(session: AsyncSession, note_id: int, data):
    query = update(Note).where(Note.id == note_id).values(
        title=data["title"],
        description=data["description"],
        photo=data["photo"]
    )
    await session.execute(query)
    await session.commit()


async def orm_delete_note(session: AsyncSession, note_id: int):
    query = delete(Note).where(Note.id == note_id)
    await session.execute(query)
    await session.commit()
