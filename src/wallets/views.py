from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from src.authentication.permissions import Permission
from src.core.containers import Container

templates = Jinja2Templates(directory='templates')

wallet_views_router = APIRouter()

# Отримання сторінки гаманців
@wallet_views_router.get('/wallet/', include_in_schema=False)
@inject
async def wallets(request: Request,
                  permission: Permission = Depends(Provide[Container.permission])):
    token = await permission.get_token_bearer(request) # Отримання токену з кукіс
    if not token:
        return RedirectResponse('/login/') # Якщо токену немає тоді перекидуємо на логін
    return templates.TemplateResponse('/wallet/wallets.html', {'request': request}) # Якщо токен є віддаємо користувачу темплейт