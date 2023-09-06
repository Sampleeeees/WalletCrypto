import asyncio

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy import select

import src
from config.base import Base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from config_fastapi import settings
from src.core.containers import Container
from src.users.models import User
from src.users.security import get_password_hash


@pytest.fixture(scope="session", autouse=True)
async def test_db_engine():
    engine = create_async_engine(settings.DATABASE_TEST_URI)
    async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        async with async_session_maker() as session:
            hashed_password = get_password_hash("Qwerty123")
            user = User(email='testuser@test.com',
                        username='Test User',
                        password=hashed_password)
            session.add(user)
            await session.commit()
            await session.refresh(user)
    yield engine
    #await engine.dispose()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# Стоврення фастапі з контейнером
def create_test_app() -> FastAPI:
    container = Container()

    container.database(db_url=settings.DATABASE_TEST_URI)

    test_app = FastAPI()
    test_app.container = container
    test_app.include_router(src.core.routers.routers)
    return test_app

test_app = create_test_app()




@pytest.fixture
async def client():
    async with AsyncClient(app=test_app, base_url="http://testserver") as client:
        yield client

@pytest.fixture
def app_test():
    return test_app

@pytest.fixture
async def login_user(client):
    """Успішна авторизація користувача"""
    response = await client.post("/api/v1/login/", json={'email': "testuser@test.com",
                                                             "password": "Qwerty123"})

    assert response.status_code == 200

@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case"""
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

