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
                        if field == 'avatar':
                            if value is not None:
                                if value != 'delete':
                                    try:
                                        if user.avatar is not None:
                                            await self.bunny_storage.delete_photo(user.avatar)
                                        url_avatar = await self.bunny_storage.upload_image_to_bunny(item.avatar)
                                        setattr(user, field, url_avatar)
                                    except:
                                        raise BadRequestException(detail='Уведіть в поле avatar фото в base64 форматі')
                                else:
                                    await self.bunny_storage.delete_photo(user.avatar)
                                    setattr(user, field, None)
                        if field == 'password':
                            if value is not None:
                                hashed_password = get_password_hash(item.password)
                                setattr(user, field, hashed_password)
                        elif value != getattr(user, field) or value is None:
                            if value is not None:
                                setattr(user, field, value)
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



