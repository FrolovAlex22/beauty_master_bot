from datetime import datetime
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Record, Material, Note


# Методы для модели Record
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


# Методы для модели Material
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


# Методы для модели Note
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
