from contextlib import contextmanager
from typing import Optional, Type, Union, List
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from . import schemas
from .security import verify_password
from .models import User
from .schemas import UserRegistration, LoginUser
from .security import get_password_hash
from src.authentication.exceptions import BadRequestException, NotFoundException
from ..authentication.jwt import create_token
from ..core.storage_bunny import BunnyStorage


class UserService:
    def __init__(self, session_factory: AsyncSession, bunny_storage: BunnyStorage) -> None:
        self.session_factory = session_factory
        self.bunny_storage = bunny_storage

    async def get_users(self):
        async with self.session_factory() as session:
            result = await session.execute(select(User))
            return result.scalars().all()

    async def get_user(self, user_id: int) -> Optional[User]:
        async with self.session_factory() as db:
            user = await db.get(User, user_id)
            if user:
                return user
            raise NotFoundException(detail="Такого користувача не знайдено")

    async def delete_user(self, user_id: int):
        async with self.session_factory() as db:
            user = await self.get_user(user_id)
            if user:
                await db.delete(user)
                await db.commit()
                return {'detail': 'Користувача видалено'}
            raise NotFoundException(detail="Такого користувача не знайдено")

    async def update_user(self, current_user, item: schemas.UpdateUserProfile):
        async with self.session_factory() as db:
            user = await self.get_user(user_id=current_user)
            if user:
                # Цикл для перевірки кожного поля та його значення при patch методі
                for field, value in item.model_dump().items():
                    try:
                        if field == 'avatar': # Якщо редагуємо поле аватар
                            if value is not None: # Перевіряємо чи не пусте поле value
                                if value != 'delete': # Якщо значення value != delete
                                    try:
                                        if user.avatar is not None: # Якщо до цього у полі avatar була url картинки то видаляємо
                                            await self.bunny_storage.delete_photo(user.avatar)
                                        url_avatar = await self.bunny_storage.upload_image_to_bunny(item.avatar) # Завантажуємо нове фото в storage
                                        setattr(user, field, url_avatar) # Записуємо значення в бд
                                    except: # Якщо фото прийшло не в base64 о цього моменту то видаємо помилку
                                        raise BadRequestException(detail='Уведіть в поле avatar фото в base64 форматі')
                                else: # Якщо у полі avatar отримуємо delete то видаляємо картинку
                                    await self.bunny_storage.delete_photo(user.avatar)
                                    setattr(user, field, None) # Ставимо значення None в бд
                        elif field == 'password': # Для поля паролю
                            if value is not None: # Перевіряємо чи не пусте значення
                                hashed_password = get_password_hash(item.password) # Хешуємо пароль в бд
                                setattr(user, field, hashed_password) # Ставимо значення в бдшку
                        elif value != getattr(user, field) or value is None: # Первірка чи є таке начення як в моделі юзера
                            if value is not None: # Якщо значення не пусте
                                setattr(user, field, value) # Записуємо нове значення
                        else:
                            raise BadRequestException(
                                detail=f"Помилка в пол  і {field}, таке значення вже записано в моделі")
                    except AttributeError:
                        pass
                db.add(user)
                await db.commit()
                await db.refresh(user)
                return user

    async def create_user(self, item: UserRegistration) -> Optional[User]:
        async with self.session_factory() as db:
            user_exists = await db.execute(select(User).where(User.email == item.email))
            # перевірка чи існує email в базі даних
            if user_exists.scalar():
                raise BadRequestException("Такий email вже існує")

            # створення користувача
            form_data = item.model_dump()
            hashed_password = get_password_hash(form_data.get('password'))
            user = User(
                email=form_data.get('email'),
                username=form_data.get('username'),
                password=hashed_password
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)
            return user

    async def authorization(self, item: LoginUser) -> Optional[Type[User]]:
        async with self.session_factory() as db:
            result = await db.execute(select(User).where(User.email == item.email))
            user = result.scalar()
            print(user)

            # Перевірка чи існує такий email
            if not user:
                raise BadRequestException("Такий email не існує в системі")

            # Перевірка чи вірно вказаний пароль від акаунту
            if not verify_password(item.password, user.password):
                raise BadRequestException("Не вірний пароль")

            # Створення токену
            access_token = create_token(user_id=user.id)

            # Оновлення токену у юзера
            user.access_token = access_token.get('access')

            # Коміт нових даних в db
            await db.commit()
            return user



