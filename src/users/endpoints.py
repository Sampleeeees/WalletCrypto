from typing import Optional, List

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Response, Request

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
async def get_current(request: Request, permission: Permission = Depends(Provide[Container.permission])) -> Optional[User]:
    user = await permission.get_current_user(request)
    return user

@user_router.get("/user/{user_id}/", status_code=status.HTTP_200_OK)
@inject
async def get_user_by_id(user_id: int, user_service: UserService = Depends(Provide[Container.user_service])):
    return await user_service.get_user(user_id=user_id)

@user_router.get("/users/", status_code=status.HTTP_200_OK, response_model=List[schemas.UserProfile])
@inject
async def get_all_users(user_service: UserService = Depends(Provide[Container.user_service])) -> List[User]:
    return await user_service.get_users()

@user_router.patch("/user/", status_code=status.HTTP_200_OK, response_model=schemas.UserProfile)
@inject
async def update_user(request: Request, item:schemas.UpdateUserProfile, permission: Permission = Depends(Provide[Container.permission])) -> Optional[User]:
    current_user = await permission.get_current_user(request)

    if not current_user:
        raise BadRequestException("Такого користувача не знайдено")

    return await permission.user_service.update_user(current_user=current_user.id, item=item)

@user_router.delete("/user/", status_code=status.HTTP_200_OK)
@inject
async def delete_me(request: Request, response: Response, permission: Permission = Depends(Provide[Container.permission])) -> dict:
    current_user = await permission.get_current_user(request)
    await permission.user_service.delete_user(user_id=current_user.id)
    response.delete_cookie(key='Authorization')
    return {'detail': "Користувача видалено"}

@user_router.delete("/user/{user_id}/", status_code=status.HTTP_200_OK)
@inject
async def delete_user(user_id:int, request:Request, permission: Permission = Depends(Provide[Container.permission])) -> dict:
    if await permission.is_admin(request):
        return await permission.user_service.delete_user(user_id=user_id)
