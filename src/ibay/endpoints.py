from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from starlette import status
from starlette.requests import Request

from src.authentication.exceptions import BadRequestException
from src.authentication.permissions import Permission
from src.core.containers import Container
from src.ibay import schemas
from src.ibay.service import IBayService
from src.wallets.service import WalletService

ibay_router = APIRouter()


@ibay_router.get('/orders/', status_code=status.HTTP_200_OK)
@inject
async def get_products(request: Request,
                       permission: Permission = Depends(Provide[Container.permission]),
                       ibay_service: IBayService = Depends(Provide[Container.ibay_service])):
    """Отримання всіх замовлень в бд"""
    user = await permission.get_current_user(request)
    if user:
        products = await ibay_service.get_products()
        return products

@ibay_router.post('/order/', status_code=status.HTTP_200_OK)
@inject
async def create_product(item: schemas.ProductCreate,
                         request: Request,
                         permission: Permission = Depends(Provide[Container.permission]),
                         ibay_service: IBayService = Depends(Provide[Container.ibay_service]),
                         wallet_service: WalletService = Depends(Provide[Container.wallet_service])):
    """Створення замовлення користувачем"""
    user = await permission.get_current_user(request)
    if user:
        wallets_user = await wallet_service.get_wallets_user(user.id)
        if item.wallet_id in [wallet.id for wallet in wallets_user]:
            return await ibay_service.create_product(item)
        raise BadRequestException(detail='У вас немає такої адреси')

