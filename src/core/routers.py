from fastapi import APIRouter

from config_fastapi.settings import API_V1
from src.authentication.views import auth_views_router
from src.chats.views import chat_views_router, asyncapi_views_router

from src.ibay.endpoints import ibay_router
from src.ibay.views import ibay_views_router
from src.users.views import user_views_router
from src.wallets.endpoints import wallet_router
from src.authentication.endpoints import auth_router
from src.users.endpoints import user_router
from src.chats.endpoints import chat_router
from src.wallets.views import wallet_views_router

routers = APIRouter()

# endpoint routers
routers.include_router(auth_router, prefix=API_V1, tags=["Auth"])
routers.include_router(user_router, prefix=API_V1, tags=['User'])
routers.include_router(wallet_router, prefix=API_V1, tags=['Wallet'])
routers.include_router(chat_router, prefix=API_V1, tags=['Message'])
routers.include_router(ibay_router, prefix=API_V1, tags=['Product'])
routers.include_router(asyncapi_views_router, tags=["AsyncAPI docs"])

# frontend routers
routers.include_router(user_views_router)
routers.include_router(auth_views_router)
routers.include_router(chat_views_router)
routers.include_router(wallet_views_router)
routers.include_router(ibay_views_router)