from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from src.authentication.permissions import Permission
from src.core.containers import Container

templates = Jinja2Templates(directory="templates")

user_views_router = APIRouter()

@user_views_router.get("/", include_in_schema=False)
@inject
async def user_profile(
        request: Request,
        permission: Permission = Depends(Provide[Container.permission])
):
    login_url = "/login/"
    token = await permission.get_token_bearer(request)
    print(token)
    if not token:
        return RedirectResponse(login_url)
    return templates.TemplateResponse("/user/user_profile.html", context={'request': request})