from typing import Optional

import jwt
from jwt import PyJWTError

from fastapi import HTTPException, Request
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param

from starlette import status
from starlette.status import HTTP_403_FORBIDDEN

from .exceptions import BadRequestException

from src.users.service import UserService


class JWTBearerCookie(OAuth2):
    """Клас для первірки access_token в cookies"""
    def __call__(self, request: Request) -> Optional[str]:
        print('Hello')
        cookie_authorization = request.cookies.get('access_token')
        token_type, access_token = get_authorization_scheme_param(cookie_authorization)
        print("Token type", token_type, 'access', access_token)
        if token_type.lower() != 'bearer':
            return None
        return access_token


class Permission:
    def __init__(self, secret_key: str, algorithm: str, user_service: UserService):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.user_service = user_service

    async def get_current_user(self, request: Request):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        cookie_authorization = request.cookies.get('access_token')
        if cookie_authorization is None:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail="Not authenticated"
            )
        token_type, access_token = get_authorization_scheme_param(cookie_authorization)
        print("Token type", token_type, 'access', access_token)
        if token_type.lower() != 'bearer':
            return None
        print("ACCESS TOKEN", access_token)
        try:
            payload = jwt.decode(access_token, self.secret_key, algorithms=self.algorithm)
            user_id = payload.get('user_id')
            if user_id is None:
                return credentials_exception
        except PyJWTError:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail="Not authenticated"
            )
        user = await self.user_service.get_user(user_id=user_id)
        print(user)
        if not user:
            raise HTTPException(status_code=404, detail='User not found')
        return user

    async def get_token_bearer(self, request: Request):
        cookie_authorization = request.cookies.get('access_token')
        if cookie_authorization is None:
            return False
        return True

    async def is_admin(self, request: Request) -> Optional[bool]:
        user = await self.get_current_user(request)
        if user.is_superuser:
            return True
        raise BadRequestException(detail="Ви не маєте прав доступу")

