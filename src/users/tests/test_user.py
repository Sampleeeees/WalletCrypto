from unittest import mock

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession


from src.users.models import User
from src.users.service import UserService


async def test_get_all_users_with_mock(client, app_test):
    user_service_mock = mock.Mock(spec=UserService)
    user_service_mock.get_users.return_value = [
        User(id=1, username="Dima Rubets", email="rubetsdima100@gmail.com"),
        User(id=101, username="Test", email="test@email.com")
    ]

    with app_test.container.user_service.override(user_service_mock):
        response = await client.get('/api/v1/users')

    assert response.status_code == 200
    data = response.json()
    assert data == [
        {"id": 1, "username": "Dima Rubets", "email": "rubetsdima100@gmail.com", "avatar": None},
        {"id": 101, "username": "Test", "email": "test@email.com", "avatar": None},
    ]






