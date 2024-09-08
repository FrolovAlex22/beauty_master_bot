from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from config_data.config import call_db
from database.models import Base


async_engine = create_async_engine(call_db(), echo=True)

session_maker = async_sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)


async def create_model():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)