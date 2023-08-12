from fastapi import APIRouter
from starlette.requests import Request

from config_fastapi.settings import API_V1

from src.wallets.endpoints import wallet_router
from src.authentication.endpoints import auth_router
from src.users.endpoints import user_router
from src.chats.endpoints import chat_router

routers = APIRouter()

routers.include_router(auth_router, prefix=API_V1, tags=["Auth"])
routers.include_router(wallet_router, prefix=API_V1, tags=['Wallet'])
routers.include_router(user_router, prefix=API_V1, tags=['User'])
routers.include_router(chat_router, prefix=API_V1, tags=['Message'])