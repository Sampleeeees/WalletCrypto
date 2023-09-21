from typing import List

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


@ibay_router.get('/products/', status_code=status.HTTP_200_OK, response_model=List[schemas.ProductList])
@inject
async def get_products(request: Request,
                       permission: Permission = Depends(Provide[Container.permission]),
                       ibay_service: IBayService = Depends(Provide[Container.ibay_service])):
    """Отримання всіх замовлень в бд"""
    user = await permission.get_current_user(request)
    if user:
        products = await ibay_service.get_products()
        return [schemas.ProductList(id=product.id,
                                    name=product.name,
                                    price=product.price,
                                    image=product.image,
                                    wallet_id=product.wallet_id,
                                    wallet=schemas.WalletBase(
                                                              id=product.wallet.id,
                                                              address=product.wallet.address,
                                                              balance=product.wallet.balance,
                                                              private_key=product.wallet.private_key,
                                                              asset_id=product.wallet.asset_id,
                                                              user_id=product.wallet.user_id,
                                                            ))
                for product in products]

@ibay_router.get('/product-ordered/', status_code=status.HTTP_200_OK, response_model=List[schemas.ProductOrdered])
@inject
async def my_order_product(request: Request,
                           permission: Permission = Depends(Provide[Container.permission]),
                           delivery_service: DeliveryService = Depends(Provide[Container.delivery_service])):
    user = await permission.get_current_user(request)
    if user:
        orders = await delivery_service.get_all_my_product(user.id)
        return [schemas.ProductOrdered(
                id=order.id,
                status=order.status,
                turning=order.turning,
                date_send=order.date_send,
                product_id=order.product_id,
                transaction_id=order.transaction_id,
                transaction=schemas.ListTransaction(
                    id=order.transaction.id,
                    hash=order.transaction.hash,
                    from_send=order.transaction.from_send,
                    to_send=order.transaction.to_send,
                    value=order.transaction.value,
                    txn_fee=order.transaction.txn_fee,
                    date_send=order.transaction.date_send,
                    status=order.transaction.status,
                ),
            )
            for order in orders]

@ibay_router.post('/buy-product/', status_code=status.HTTP_200_OK, response_model=schemas.BuyProductResponse)
@inject
async def buy_order_by_id(request: Request,
                          item: schemas.BuyProduct,
                          ibay_service: IBayService = Depends(Provide[Container.ibay_service]),
                          permission: Permission = Depends(Provide[Container.permission]),
                          wallet_service: WalletService = Depends(Provide[Container.wallet_service]),
                          delivery_service: DeliveryService = Depends(Provide[Container.delivery_service])):
    """Купівля продукту"""
    user = await permission.get_current_user(request)
    if user:
        product = await ibay_service.get_product_by_id(order_id=item.product_id) # Отримання продукту по його id
        wallet_user = await wallet_service.get_wallets_user(user_id=user.id, wallet_id=item.wallet_id) # Отримання валета юзера по id

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

        delivery_dict = delivery_schemas.OrderCreate(product_id=item.product_id, transaction_id=transaction_id.id) # Запис даних в схемиу для створення замовлення
        order = await delivery_service.create_order(delivery_dict) # Створення замовлення
        return {'id': order.id,
                'hash': txn_hash}

@ibay_router.post('/product/', status_code=status.HTTP_200_OK, response_model=schemas.ProductList)
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
            product = await ibay_service.create_product(item)
            return schemas.ProductList(id=product.id,
                                       name=product.name,
                                       price=product.price,
                                       image=product.image,
                                       wallet_id=product.wallet_id,
                                       wallet=schemas.WalletBase(
                                                              id=product.wallet.id,
                                                              address=product.wallet.address,
                                                              balance=product.wallet.balance,
                                                              private_key=product.wallet.private_key,
                                                              asset_id=product.wallet.asset_id,
                                                              user_id=product.wallet.user_id,
                                                            ))
        raise BadRequestException(detail='У вас немає такої адреси')

