from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Product, Calendar, Note


async def orm_add_record(session: AsyncSession, data: dict):
    obj = Calendar(
        name=data["name"],
        phone_number=data["phone_number"],
    )
    session.add(obj)
    await session.commit()



async def orm_get_records(session: AsyncSession):
    query = select(Calendar)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_record(session: AsyncSession, record_id: int):
    query = select(Calendar).where(Calendar.id == record_id)
    result = await session.execute(query)
    return result.scalar()


async def orm_update_record(session: AsyncSession, record_id: int, data):
    query = update(Calendar).where(Calendar.id == record_id).values(
        name=data["name"],
        phone_number=data["phone_number"],
    )
    await session.execute(query)
    await session.commit()


async def orm_delete_record(session: AsyncSession, record_id: int):
    query = delete(Calendar).where(Calendar.id == record_id)
    await session.execute(query)
    await session.commit()
