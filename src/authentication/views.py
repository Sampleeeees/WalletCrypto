from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from src.authentication.permissions import Permission
from src.core.containers import Container

templates = Jinja2Templates(directory='templates')


auth_views_router = APIRouter()

@auth_views_router.get("/login/", include_in_schema=False)
@inject
async def login_user(request: Request,
                     permission: Permission = Depends(Provide[Container.permission])):
    token = await permission.get_token_bearer(request)
    if token:
        return RedirectResponse('/')
    return templates.TemplateResponse('auth/login.html', context={'request': request})


@auth_views_router.get("/registration/", include_in_schema=False)
@inject
async def registration(request: Request,
                       permission: Permission = Depends(Provide[Container.permission])):
    token = await permission.get_token_bearer(request)
    if token:
        return RedirectResponse('/')
    return templates.TemplateResponse('auth/registration.html', context={'request': request})
