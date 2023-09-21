from typing import Any, Optional, Union

from pydantic import BaseModel, EmailStr, validator
from ..authentication.exceptions import BadRequestException


class UserBase(BaseModel):
    """Базова схема юзера"""
    username: str
    email: EmailStr

    class Config:
        from_attributes = True

class LoginUser(BaseModel):
    """Схема для логіна"""
    email: str
    password: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    'email': 'your_email@example.com',
                    'password': 'Qwerty123'
                }
            ]
        }
    }

class UserRegistration(UserBase):
    """Схема для реєстрації"""
    password: str
    repeat_password: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    'username': 'John Doe',
                    "email": 'user@example.com',
                    "password": 'Qwerty123',
                    "repeat_password": "Qwerty123"
                }
            ]
        }
    }

    @validator('password')
    def validate_password(cls, value):

        # Перевірка на довжину від 8 до 20 символів
        if not 8 <= len(value) <= 20:
            raise BadRequestException("Пароль повинен містити від 8 до 20 символів")

        # Перевірка на наявність мінімум 1 цифри
        if not any(char.isdigit() for char in value):
            raise BadRequestException("Пароль повинен містити принаймні одну цифру")

        # Перевірка на наявність мінімум 1 літери в нижньому регістрі
        if not any(char.islower() for char in value):
            raise BadRequestException("Пароль повинен містити принаймні одну літеру в нижньому регістрі")

        # Перевірка на наявність мінімум 1 літери в верхньому регістрі
        if not any(char.isupper() for char in value):
            raise BadRequestException("Пароль повинен містити принаймні одну літеру в верхньому регістрі")

        return value

    @validator('repeat_password')
    def validate_repeat_password(cls, value, values):
        print(values.data.get('password'), value)
        password = values.data.get('password')
        if value != password:
            raise BadRequestException("Паролі не співпадають")
        return value


class UserProfile(BaseModel):
    """Схема для отримання даних авторизованого користувача"""
    id: int
    username: str
    email: EmailStr
    avatar: Any

    class Config:
        schema_extra = {
            "examples": [
                {
                    "id": 0,
                    "username": "John Doe",
                    "email": "user@test.gmail.com",
                    "avatar": "http://example.com/basic.jpg"
                }
            ]
        }


class UpdateUserProfile(BaseModel):
    """Схема для оновлення користувача"""
    username: Union[str, None] = None
    avatar: Union[Any, None] = None
    password: Union[str, None] = None
    repeat: Union[str, None] = None

    @classmethod
    def extra_fields(cls):
        return {
                "full_update": {
                    "username": "John Doe",
                    "avatar": "data:image/jpeg;base64...",
                    "password": "Qwerty123",
                    "repeat": "Qwerty123",
                },
                "update_only_username": {
                    "username": "John Doe",
                },
                "update_only_avatar": {
                    "avatar": "data:image/jpeg;base63...",
                },
                "update_only_password": {
                    "password": "Qwerty123",
                    "repeat": "Qwerty123",
                },
            }


    @validator('password')
    def validate_password(cls, value):
        if value is not None:
            # Перевірка на довжину від 8 до 20 символів
            if not 8 <= len(value) <= 20:
                raise BadRequestException("Пароль повинен містити від 8 до 20 символів")

            # Перевірка на наявність мінімум 1 цифри
            if not any(char.isdigit() for char in value):
                raise BadRequestException("Пароль повинен містити принаймні одну цифру")

            # Перевірка на наявність мінімум 1 літери в нижньому регістрі
            if not any(char.islower() for char in value):
                raise BadRequestException("Пароль повинен містити принаймні одну літеру в нижньому регістрі")

            # Перевірка на наявність мінімум 1 літери в верхньому регістрі
            if not any(char.isupper() for char in value):
                raise BadRequestException("Пароль повинен містити принаймні одну літеру в верхньому регістрі")

            return value

    @validator('repeat')
    def validate_repeat_password(cls, value, values):
        print(values.data.get('password'), value)
        password = values.data.get('password')
        if value != password:
            raise BadRequestException("Паролі не співпадають")
        return value

