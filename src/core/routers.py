from fastapi import APIRouter

from config_fastapi.settings import API_V1
from config_fastapi.test_endpoint import test_router

from src.ibay.endpoints import ibay_router
from src.wallets.endpoints import wallet_router
from src.authentication.endpoints import auth_router
from src.users.endpoints import user_router
from src.chats.endpoints import chat_router
from src.delivery.endpoints import delivery_router

routers = APIRouter()

routers.include_router(auth_router, prefix=API_V1, tags=["Auth"])
routers.include_router(wallet_router, prefix=API_V1, tags=['Wallet'])
routers.include_router(user_router, prefix=API_V1, tags=['User'])
routers.include_router(chat_router, prefix=API_V1, tags=['Message'])
routers.include_router(ibay_router, prefix=API_V1, tags=['Product'])
routers.include_router(delivery_router, prefix=API_V1, tags=['Delivery'])
routers.include_router(test_router, tags=['Socket'])