from typing import Optional

from starlette.exceptions import HTTPException
from starlette.responses import Response
from dependency_injector.wiring import inject, Provide
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from config_fastapi import settings
from src.authentication.endpoints import login_user
from src.authentication.permissions import Permission
from src.users import schemas
from src.core.containers import Container
from src.users.service import UserService


class AdminAuth(AuthenticationBackend):
    @inject
    async def login(self, request: Request, user_service: UserService = Provide[Container.user_service]) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]
        item = schemas.LoginUser(email=email, password=password)

        user = await user_service.authorization(item)
        if not user.is_superuser:
            raise HTTPException(detail='Ви не є адміністратором', status_code=400)
        request.session.update({"token": user.access_token})
        return True

    async def logout(self, request: Request) -> bool:
        print(request.session)
        request.session.clear()
        return True

    @inject
    async def authenticate(self, request: Request, permission: Permission = Provide[Container.permission]) -> Optional[RedirectResponse]:
        token = request.session.get("token")

        if not token:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)

authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY)