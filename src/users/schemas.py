from typing import Any, Union

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

    class Config:
        class Config:
            schema_extra = {
                "examples": [
                    {
                        "email": "user@test.gmail.com",
                        "password": "Qwerty123",
                    }
                ]
            }

class UserRegistration(UserBase):
    """Схема для реєстрації"""
    password: str
    repeat_password: str

    class Config:
        schema_extra = {
            "examples": [
                {
                    "username": "John Doe",
                    "email": "user@test.gmail.com",
                    "password": "Qwerty123",
                    "repeat_password": "Qwerty123",
                }
            ]
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
        password = values.get('password')
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
                "summary": "Full update user data",
                "description": "Full items for update users data.",
                "value": {
                    "username": "John Doe",
                    "avatar": "data:image/jpeg;base64...",
                    "password": "Qwerty123",
                    "repeat": "Qwerty123",
                },
            },
            "update_only_username": {
                "summary": "Update only username user ",
                "description": "Item for update user username",
                "value": {
                    "username": "John Doe",
                },
            },
            "update_only_avatar": {
                "summary": "Update only avatar user ",
                "description": "Item for update avatar username",
                "value": {
                    "avatar": "data:image/jpeg;base64...",
                },
            },
            "update_only_password": {
                "summary": "Update only password user ",
                "description": "Item for update user password",
                "value": {
                    "password": "Qwerty",
                    "repeat": "Qwerty",
                },
            },
            "update_username_avatar": {
                "summary": "Update username and avatar user ",
                "description": "Item for update user username and avatar",
                "value": {
                    "username": "John Doe",
                    "avatar": "data:image/jpeg;base64...",
                },
            },
            "update_username_password": {
                "summary": "Update username and password user ",
                "description": "Item for update user username and password",
                "value": {
                    "username": "John Doe",
                    "password": "Qwerty123",
                    "repeat": "Qwerty123",
                },
            },
            "update_avatar_password": {
                "summary": "Update avatar and password user ",
                "description": "Item for update user avatar and password",
                "value": {
                    "avatar": "data:image/jpeg;base64...",
                    "password": "Qwerty123",
                    "repeat": "Qwerty123",
                },
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
        password = values.get('password')
        if value != password:
            raise BadRequestException("Паролі не співпадають")
        return value


class DeleteDetail(BaseModel):
    """Схема для виводу повідомлення про успішне видалення користувача"""
    detail: str

    class Config:
        schema_extra = {
            "examples": [
                {
                    "detail": "Користувача видалено"
                }
            ]
        }
        

