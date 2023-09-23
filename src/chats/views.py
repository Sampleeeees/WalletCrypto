from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from src.authentication.permissions import Permission
from src.core.containers import Container

templates = Jinja2Templates(directory="templates")

chat_views_router = APIRouter()
asyncapi_views_router = APIRouter()

@chat_views_router.get('/chat/', include_in_schema=False)
@inject
async def chat(request: Request,
               permission: Permission = Depends(Provide[Container.permission])):
    token = await permission.get_token_bearer(request)
    if not token:
        return RedirectResponse('/login/')
    return templates.TemplateResponse('/chat/chat.html', {'request': request})

@asyncapi_views_router.get('/asyncapi_docs/', include_in_schema=False)
@inject
async def asyncapi_docs(request: Request,
                        permission: Permission = Depends(Provide[Container.permission])):
    token = await permission.get_token_bearer(request)
    if not token:
        return RedirectResponse('/login/')
    return templates.TemplateResponse('/chat/asyncapi/index.html', {"request": request})
