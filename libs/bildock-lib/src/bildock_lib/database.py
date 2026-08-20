from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from bildock_lib.config import get_settings
from typing import AsyncIterator

engine = create_async_engine(get_settings().database_url)
async_session = async_sessionmaker(engine)


class Base(DeclarativeBase):
    pass


async def get_session() -> AsyncIterator[AsyncSession]:
    async with async_session() as session:
        yield session
