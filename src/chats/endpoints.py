import datetime
from typing import List

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from starlette import status
from starlette.requests import Request

from config.database import Database
from src.authentication.permissions import Permission
from src.chats import schemas
from src.chats.models import Message
from src.core.containers import Container

chat_router = APIRouter()

@chat_router.get('/message/current-user/', status_code=status.HTTP_200_OK)
@inject
async def get_message_current_user(request: Request,
                                   permission: Permission = Depends(Provide[Container.permission]),
                                   database: Database = Depends(Provide[Container.database])):
    user = await permission.get_current_user(request)
    if user:
        async with database.get_db_session() as db:
            results = await db.execute(select(Message).where(Message.user_id == user.id))
            messages = results.scalars().all()
            if messages:
                return messages
            raise HTTPException(detail='У вас немає жодного повідомлення', status_code=status.HTTP_404_NOT_FOUND)

@chat_router.get('/message/{msg_id}/', status_code=status.HTTP_200_OK)
@inject
async def send_message(request: Request,
                       msg_id: int,
                       permission: Permission = Depends(Provide[Container.permission]),
                       database: Database = Depends(Provide[Container.database])):
    admin = await permission.is_admin(request)
    if admin:
        async with database.get_db_session() as db:
            message = await db.get(Message, msg_id)
            print(message)
            if message:
                return message
            raise HTTPException(detail='Повідомлення під таким id не знайдено', status_code=status.HTTP_404_NOT_FOUND)


@chat_router.post('/message/', status_code=status.HTTP_200_OK)
@inject
async def send_message(request: Request,
                       item: schemas.MessageSend,
                       permission: Permission = Depends(Provide[Container.permission]),
                       database: Database = Depends(Provide[Container.database])):
    user = await permission.get_current_user(request)
    if user:
        async with database.get_db_session() as db:
            photo = item.photo
            if item.photo == 'string':
                photo = None
            message = Message(content=item.content, image=photo, user_id=user.id, date_send=datetime.datetime.now())
            db.add(message)
            await db.commit()
            await db.refresh(message)
            return {'id': message.id,
                    'content': message.content,
                    'photo': message.image,
                    'date_send': message.date_send.strftime("%m/%d/%Y, %H:%M:%S"),
                    'user_id': message.user_id}

@chat_router.delete('/message/', status_code=status.HTTP_200_OK)
@inject
async def delete_message(request: Request,
                       msg_id: int,
                       permission: Permission = Depends(Provide[Container.permission]),
                       database: Database = Depends(Provide[Container.database])):
    user = await permission.get_current_user(request)
    if user:
        async with database.get_db_session() as db:
            result = await db.execute(select(Message).where(Message.id == msg_id, Message.user_id == user.id))
            message = result.scalar()
            if message:
                await db.delete(message)
                await db.commit()
                return {'detail': 'Повідомлення видалено'}
            raise HTTPException(detail='Повідомлення під таким id не знайдено', status_code=status.HTTP_404_NOT_FOUND)


