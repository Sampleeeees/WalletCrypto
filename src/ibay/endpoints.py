from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from starlette import status
from starlette.requests import Request

from src.authentication.exceptions import BadRequestException
from src.authentication.permissions import Permission
from src.core.containers import Container
from src.delivery.service import DeliveryService
from src.ibay import schemas
from src.ibay.service import IBayService
from src.wallets.service import WalletService
from src.wallets import schemas as wallet_schemas
from src.delivery import schemas as delivery_schemas

ibay_router = APIRouter()


@ibay_router.get('/products/', status_code=status.HTTP_200_OK)
@inject
async def get_products(request: Request,
                       permission: Permission = Depends(Provide[Container.permission]),
                       ibay_service: IBayService = Depends(Provide[Container.ibay_service])):
    """Отримання всіх замовлень в бд"""
    user = await permission.get_current_user(request)
    if user:
        products = await ibay_service.get_products()
        return products

@ibay_router.get('/product-ordered/', status_code=status.HTTP_200_OK)
@inject
async def my_order_product(request: Request,
                           permission: Permission = Depends(Provide[Container.permission]),
                           delivery_service: DeliveryService = Depends(Provide[Container.delivery_service])):
    user = await permission.get_current_user(request)
    if user:
        return await delivery_service.get_all_my_product(user.id)

@ibay_router.post('/buy-product/', status_code=status.HTTP_200_OK)
@inject
async def buy_order_by_id(request: Request,
                          product_id: int,
                          wallet_id: int,
                          ibay_service: IBayService = Depends(Provide[Container.ibay_service]),
                          permission: Permission = Depends(Provide[Container.permission]),
                          wallet_service: WalletService = Depends(Provide[Container.wallet_service]),
                          delivery_service: DeliveryService = Depends(Provide[Container.delivery_service])):
    """Купівля продукту"""
    user = await permission.get_current_user(request)
    if user:
        product = await ibay_service.get_product_by_id(order_id=product_id) # Отримання продукту по його id
        wallet_user = await wallet_service.get_wallets_user(user_id=user.id, wallet_id=wallet_id) # Отримання валета юзера по id

        # Якщо продукту під таким id немає то виводим помилку
        if not product:
            raise BadRequestException("Товару під таким id не знайдено")

        # Якщо валета під таким id немає то виводим помилку
        if not wallet_user:
            raise BadRequestException("Такого гаманця у вас немає")

        # Якщо юзер купляє у себе свій продукт виводимо помилку
        if wallet_user.address == product.wallet.address:
            raise BadRequestException('Ви не можете купити товар у самого себе )')

        # Створення схеми для транзакції
        transaction_dict = wallet_schemas.TransactionCreate(from_send=wallet_user.address,
                                                            to_send=product.wallet.address,
                                                            value=product.price,
                                                            private_key=wallet_user.private_key)

        txn_hash = await wallet_service.send_transaction(item=transaction_dict) # Отримання хешу від відправленої транзакції
        transaction_id = await wallet_service.get_transaction_in_db(txn_hash) # Отримання id транзакції яка була створена

        delivery_dict = delivery_schemas.OrderCreate(product_id=product_id, transaction_id=transaction_id.id) # Запис даних в схемиу для створення замовлення
        await delivery_service.create_order(delivery_dict) # Створення замовлення
        return txn_hash

@ibay_router.post('/product/', status_code=status.HTTP_200_OK)
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

