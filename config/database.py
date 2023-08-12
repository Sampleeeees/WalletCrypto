import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager, contextmanager
from typing import ContextManager

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncAttrs, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from sqlalchemy.util.preloaded import orm

logger = logging.getLogger(__name__)

class Base(AsyncAttrs, DeclarativeBase):
    pass


class Database:
    """Клас для підключення до бази даних та отримання сесії"""
    def __init__(self, db_url: str) -> None:
        self._engine = create_async_engine(db_url, echo=True, future=True)
        self._session_factory = async_sessionmaker(self._engine, autoflush=False, expire_on_commit=False)

    # Отримання сесії
    @asynccontextmanager
    async def get_db_session(self) -> AsyncSession:
        async with self._session_factory() as session:
            try:
                yield session
            finally:
                await session.close()