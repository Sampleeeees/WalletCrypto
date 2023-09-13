from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from src.authentication.permissions import Permission
from src.core.containers import Container

templates = Jinja2Templates(directory='templates')

ibay_views_router = APIRouter()


@ibay_views_router.get('/ibay/', include_in_schema=False)
@inject
async def ibay(request: Request,
               permission: Permission = Depends(Provide[Container.permission])):
    token = await permission.get_token_bearer(request)
    if not token:
        return RedirectResponse('/login/')
    return templates.TemplateResponse('/ibay/ibay.html', {'request': request})


