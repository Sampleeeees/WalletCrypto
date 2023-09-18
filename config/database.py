import logging
from contextlib import asynccontextmanager

from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import create_async_engine, AsyncAttrs, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from config_fastapi import settings

logger = logging.getLogger(__name__)
engine = create_async_engine(settings.DATABASE_URI, echo=True, future=True) # engine для sqladmin

# Клас який буде використовуватися при створені моделей
class Base(AsyncAttrs, DeclarativeBase):
    pass

class LastSuccessBlock(Base):
    """Save block number in db"""

    __tablename__ = 'blockNumber'

    id = Column(Integer, primary_key=True, autoincrement=True)
    block_number = Column(Integer, default=0)

class Database:
    """Клас для підключення до бази даних та отримання сесії"""
    def __init__(self) -> None:
        self._session_factory = async_sessionmaker(engine, autoflush=False, expire_on_commit=False)

    # Отримання сесії
    @asynccontextmanager
    async def get_db_session(self) -> AsyncSession:
        async with self._session_factory() as session:
            try:
                yield session
            finally:
                await session.close()