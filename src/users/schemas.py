from typing import Any, Optional

from pydantic import BaseModel, EmailStr, field_validator
from ..authentication.exceptions import BadRequestException


class UserBase(BaseModel):
    username: str
    email: EmailStr

    class Config:
        from_attributes = True

class LoginUser(BaseModel):
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

    @field_validator('password')
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

    @field_validator('repeat_password')
    def validate_repeat_password(cls, value, values):
        print(values.data.get('password'), value)
        password = values.data.get('password')
        if value != password:
            raise BadRequestException("Паролі не співпадають")
        return value


class UserProfile(BaseModel):
    id: int
    username: str
    email: EmailStr
    avatar: Any

class UpdateUserProfile(BaseModel):
    username: Optional[str] = None
    avatar: Any = None
    password: Optional[str] = None
    repeat: Optional[str] = None

    @field_validator('password')
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

    @field_validator('repeat')
    def validate_repeat_password(cls, value, values):
        print(values.data.get('password'), value)
        password = values.data.get('password')
        if value != password:
            raise BadRequestException("Паролі не співпадають")
        return value

