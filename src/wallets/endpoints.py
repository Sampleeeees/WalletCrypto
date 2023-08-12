from typing import List
from pydantic import TypeAdapter
from starlette.requests import Request

from src.authentication.permissions import Permission
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from . import schemas
from dependency_injector.wiring import Provide, inject
from src.core.containers import Container
from .models import Wallet
from .service import WalletService

wallet_router = APIRouter()


@wallet_router.get('/wallets', status_code=status.HTTP_200_OK, response_model=List[schemas.WalletList])
@inject
async def get_wallets(wallet_service: WalletService = Depends(Provide[Container.wallet_service])) -> List[Wallet]:
    """Отримання всіх гаманців"""
    return await wallet_service.get_wallets()


@wallet_router.get('/wallets/current_user', status_code=status.HTTP_200_OK, response_model=List[schemas.WalletList])
@inject
async def get_wallets_current_user(request: Request,
                                   permission: Permission = Depends(Provide[Container.permission]),
                                   wallet_service: WalletService = Depends(Provide[Container.wallet_service])) -> List[Wallet]:
    """Отримання всіх гаманців авторизованого користувача"""
    user = await permission.get_current_user(request)
    if user:
        return await wallet_service.get_wallets_user(user.id)

@wallet_router.post('/wallet/etherscan', status_code=status.HTTP_200_OK)
@inject
async def get_address_in_etherscan(address: str,
                                   request: Request,
                                   permission: Permission = Depends(Provide[Container.permission]),
                                   wallet_service: WalletService = Depends(Provide[Container.wallet_service])):
    """Отримання url адреси на etherscan"""
    user = permission.get_current_user(request)
    if user:
        return await wallet_service.get_address_etherscan(address)


@wallet_router.post('/wallet', status_code=status.HTTP_200_OK)
@inject
async def create_wallet(request:Request,
                        permission: Permission = Depends(Provide[Container.permission]),
                        wallet_service: WalletService = Depends(Provide[Container.wallet_service])):
    """Стоврення гаманця для авторизованого користувача"""
    user = await permission.get_current_user(request)
    if user:
        return await wallet_service.create_wallet(user_id=user.id)

@wallet_router.post('/wallet/import', status_code=status.HTTP_200_OK)
@inject
async def import_wallet(item: schemas.WalletImport,
                        request: Request,
                        wallet_service: WalletService = Depends(Provide[Container.wallet_service]),
                        permission: Permission = Depends(Provide[Container.permission])):
    """Імпортування гаманця за допомогою приватного ключа"""
    user = await permission.get_current_user(request)
    if user:
        return await wallet_service.import_wallet(item.private_key, user.id)

@wallet_router.post('/send-transaction', status_code=status.HTTP_200_OK)
@inject
async def send_transaction(item: schemas.TransactionCreate,
                           request: Request,
                           permission: Permission = Depends(Provide[Container.permission]),
                           wallet_service: WalletService = Depends(Provide[Container.wallet_service])):
    """Відправка транзакції"""
    user = await permission.get_current_user(request)
    if user:
        return await wallet_service.send_transaction(item)

@wallet_router.post('/wallet/balance', status_code=status.HTTP_200_OK, response_model=schemas.Wallet)
@inject
async def get_balance_by_address(item: schemas.CheckBalance,
                                 request: Request,
                                 permission: Permission = Depends(Provide[Container.permission]),
                                 wallet_service: WalletService = Depends(Provide[Container.wallet_service])):
    """Отримання балансу гаманця"""
    user = await permission.get_current_user(request)
    if user:
        return await wallet_service.get_balance(item)


@wallet_router.get('/wallet/transaction', status_code=status.HTTP_200_OK, response_model=schemas.TransactionInfo)
@inject
async def get_transaction_by_hash(txn_hash: str,
                                  request: Request,
                                  permission: Permission = Depends(Provide[Container.permission]),
                                  wallet_service: WalletService = Depends(Provide[Container.wallet_service])):
    """Отримання даних транзакції через хеш"""
    user = await permission.get_current_user(request)
    if user:
        if txn_hash.startswith("0x"):
            transaction = await wallet_service.get_transaction(txn_hash)
            return schemas.TransactionInfo(**transaction, from_send=transaction['from'])
        raise HTTPException(detail='Ви ввели невірний хеш', status_code=status.HTTP_400_BAD_REQUEST)

