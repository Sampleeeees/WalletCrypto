from typing import Optional, List, Type, Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Response, Request, Body

from starlette import status

from src.authentication.exceptions import BadRequestException
from src.users.models import User
from src.authentication.permissions import Permission
from src.core.containers import Container

from .service import UserService
from . import schemas


user_router = APIRouter()


@user_router.get("/user/profile/", status_code=status.HTTP_200_OK, response_model=schemas.UserProfile)
@inject
async def get_current(request: Request,
                      permission: Permission = Depends(Provide[Container.permission])
                      ) -> schemas.UserProfile:
    """Отримання даних авторизованого користувача"""
    user = await permission.get_current_user(request)
    return schemas.UserProfile(id=user.id, username=user.username, email=user.email, avatar=user.avatar)

@user_router.get("/user/{user_id}/", status_code=status.HTTP_200_OK, response_model=schemas.UserProfile)
@inject
async def get_user_by_id(user_id: int, user_service: UserService = Depends(Provide[Container.user_service])):
    """Отримання даних юзера по id"""
    user = await user_service.get_user(user_id=user_id)
    return schemas.UserProfile(id=user.id, username=user.username, email=user.email, avatar=user.avatar)

@user_router.get("/users/", status_code=status.HTTP_200_OK, response_model=List[schemas.UserProfile])
@inject
async def get_all_users(user_service: UserService = Depends(Provide[Container.user_service])):
    """Отримання списку користувачів"""
    users = await user_service.get_users()
    return [schemas.UserProfile(id=user.id, username=user.username, email=user.email, avatar=user.avatar) for user in users]


@user_router.patch("/user/", status_code=status.HTTP_200_OK, response_model=schemas.UserProfile)
@inject
async def update_user(request: Request,
                      item: Annotated[schemas.UpdateUserProfile, Body(openapi_examples=schemas.UpdateUserProfile.extra_fields())],
                      permission: Permission = Depends(Provide[Container.permission]),
                      user_service: UserService = Depends(Provide[Container.user_service])):
    """Оновлення користувача"""
    current_user = await permission.get_current_user(request)

    if not current_user:
        raise BadRequestException("Такого користувача не знайдено")
    print('User item', item)

    user = await user_service.update_user(current_user=current_user.id, item=item)
    return schemas.UserProfile(id=user.id, username=user.username, email=user.email, avatar=user.avatar)

@user_router.delete("/user/", status_code=status.HTTP_200_OK, response_description='Successfully deleted')
@inject
async def delete_me(request: Request,
                    response: Response,
                    permission: Permission = Depends(Provide[Container.permission]),
                    user_service: UserService = Depends(Provide[Container.user_service])) -> dict:
    current_user = await permission.get_current_user(request)
    await user_service.delete_user(user_id=current_user.id)
    response.delete_cookie(key='Authorization')
    return {'detail': "Користувача видалено"}

@user_router.delete("/user/{user_id}/", status_code=status.HTTP_200_OK)
@inject
async def delete_user(user_id: int,
                      request: Request,
                      permission: Permission = Depends(Provide[Container.permission]),
                      user_service: UserService = Depends(Provide[Container.user_service])) -> dict:
    if await permission.is_admin(request):
        return await user_service.delete_user(user_id=user_id)
