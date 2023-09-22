import asyncio
import datetime

import pytest
from fastapi import FastAPI
from httpx import AsyncClient

import src
from config.base import Base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from config_fastapi import settings
from factories import create_user, create_admin, create_message, create_blockchain, create_asset, create_wallet
from src.core.containers import Container



@pytest.fixture(scope="session", autouse=True)
async def test_db_engine():
    engine = create_async_engine(settings.DATABASE_TEST_URI)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        db = AsyncSession(bind=conn)
        await create_user(db)
        await create_admin(db)
        await create_message(db)
        await create_blockchain(db)
        await create_asset(db)
        await create_wallet(db)
    yield engine
    #await engine.dispose()
    async with engine.begin() as conn:
        db = AsyncSession(bind=conn)
        await db.rollback()
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
async def user_auth(app_test, client):

    response = await client.post("/api/v1/login/", json={"email": settings.TEST_USER_EMAIL,
                                                         "password": settings.TEST_USER_PASSWORD})


    assert response.status_code == 200
    yield response


@pytest.fixture
async def admin_auth(app_test, client):

    response = await client.post("/api/v1/login/", json={"email": settings.TEST_ADMIN_EMAIL,
                                                         "password": settings.TEST_ADMIN_PASSWORD})


    assert response.status_code == 200
    yield response

@pytest.fixture
def image_in_base64(app_test) -> str:
    return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAwAAAAOCAIAAACU32q7AAAAA3NCSVQICAjb4U/gAAAAGHRFWHRTb2Z0d2FyZQBtYXRlLXNjcmVlbnNob3TIlvBKAAAB9ElEQVQokQXBO2/TQAAA4LvznZMmdmzHjpM2FVWKgholLYjHUFKpCxMDCwNiY+5fQGLujwAEE0JIMIEoAlHBUhAMoKgBRRRIWhJQm4fPPvvss833wXtb7ecvPt7euhjytKDZvcHJr+NpgvHOyy8AEBgTNmNwUwPXrjQ3mgskR+Q8SWCAYZjEkS4bfynq9Hrr7fPw9Z0bYvIzSX0nYLqpQ5TYRYPOHI/OClatvFiB0EGKNKpZCo/9cqUkhIjCJA5hyOKiZXt01ut2mDdFCe8FwqnXly3LMC0dxiLmYegGcpbohiJhmMEEy3IFmEVGPSwTTZ0LKAYxW1o0ncARcdZnXM7biIcGUPOEEAjTKOJKLmPbZhA4QoQIIYzlKeUoTlwwTXMZPB5Osci7LjgaHw+cE6zKgqat1crdh59QZckH/HAwoLIiMTCEOT9GWk5pRJOoWk2HByCDJsh1ROBS2wyRiBMvmwaKBMIEjhSsAQCePtlda5RRwBqep/3+0ddyqmAB5K6p4tMLRV0rvd/7l52zWnVLKtKDt+/6hdJakpGJKs2fspgP9ruHOC89eLS/srq4PA/w1euXRn/UV3tfn705ury+0jiDBO9vbF743vmWYiVbwIxy+Hm7jVPoO2NknLv/eMewtFs3z3qT7oddGGFYrZnNlv0f46Hv3RBPBK8AAAAASUVORK5CYII="

@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case"""
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

