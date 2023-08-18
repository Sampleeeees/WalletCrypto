import asyncio

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy import select

import src
from config.base import Base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from config_fastapi import settings
from src.core.containers import Container
from src.users.models import User
from src.users.security import get_password_hash


@pytest.fixture(scope="session", autouse=True)
async def test_db_engine():
    engine = create_async_engine(settings.DATABASE_TEST_URI)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    #await engine.dispose()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


def create_test_app() -> FastAPI:
    container = Container()

    container.database(db_url=settings.DATABASE_TEST_URI)

    test_app = FastAPI()
    test_app.container = container
    test_app.include_router(src.core.routers.routers)
    return test_app

test_app = create_test_app()



# Створення та видалення таблиць при тестах
@pytest.fixture
async def client():
    async with AsyncClient(app=test_app, base_url="http://testserver") as client:
        yield client

@pytest.fixture
def app_test():
    return test_app


@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case"""
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

