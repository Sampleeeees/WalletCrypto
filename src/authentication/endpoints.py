import asyncio
import functools
from typing import List

from fastapi import APIRouter, Depends, Response
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse
from .send_email import send_new_account_email
from src.users.schemas import UserRegistration, LoginUser, UserProfile
from dependency_injector.wiring import inject, Provide

from .permissions import Permission
from ..core.containers import Container
from ..users.service import UserService

auth_router = APIRouter()

@auth_router.post("/registration/", status_code=status.HTTP_201_CREATED, response_description="Successfully Registration", response_model=UserRegistration)
@inject
async def registration(item: UserRegistration, user_service: UserService = Depends(Provide[Container.user_service])):
    """Endpoint для реєстрації користувача"""
    user = await user_service.create_user(item)

    # Відправка повідомлення на email про успішну реєстрацію
    if await user_service.get_user(user_id=user.id):
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, send_new_account_email, user.email, user.username)
    detail = {
        "message": "Акаунт успішно створений. Повідомлення про реєстрацію надіслано на пошту",
        "detail": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    }
    return JSONResponse(content=detail, status_code=status.HTTP_201_CREATED)



@auth_router.post("/login/", status_code=status.HTTP_200_OK)
@inject
async def login_user(response: Response, item: LoginUser, user_service: UserService = Depends(Provide[Container.user_service])):
    user = await user_service.authorization(item)

    # Записуємо токен в Кукі
    response.set_cookie(
        key='Authorization',
        value=f"Bearer {user.access_token}",
        #expires=jwt.decode(user.access_token, settings.SECRET_KEY, ALGORITHM).get('exp')
    )
    return {"detail": 'Successfully authorization',
            'user_id': user.id,
            'username': user.username,
            'email': user.email}

@auth_router.post('/logout/', status_code=status.HTTP_200_OK)
@inject
async def logout(response: Response, request: Request, permission: Permission = Depends(Provide[Container.permission])):
    print(permission)
    if await permission.get_current_user(request):
        response.delete_cookie(key="Authorization")
        return {"detail": 'Ви успішно вийшли зі свого акаунту'}




