from sqlalchemy.ext.asyncio import (
    AsyncSession, async_sessionmaker, create_async_engine
)
from config_data.config import DATABASE_URL
from database.models import Base
from database.methods import orm_add_banner_description, orm_create_categories
from lexicon.text_for_db import DESCRIPTION_FOR_INFO_PAGES, CATEGORIES


async_engine = create_async_engine(DATABASE_URL, echo=True)

session_maker = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def create_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with session_maker() as session:
        # Создаем таблицы
        await orm_create_categories(session, CATEGORIES)
        await orm_add_banner_description(session, DESCRIPTION_FOR_INFO_PAGES)


async def drop_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
