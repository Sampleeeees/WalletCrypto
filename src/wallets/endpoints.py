from typing import List
from starlette.requests import Request

from config_fastapi.fastapi_manager import fastapi_mgr
from src.authentication.permissions import Permission
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from . import schemas
from dependency_injector.wiring import Provide, inject
from src.core.containers import Container
from .models import Wallet
from .service import WalletService
# from ..parser.moralis_service import MoralisService
from ..users.service import UserService

wallet_router = APIRouter()


@wallet_router.get('/wallets/', status_code=status.HTTP_200_OK, response_model=List[schemas.WalletList])
@inject
async def get_wallets(wallet_service: WalletService = Depends(Provide[Container.wallet_service])):
    """Отримання всіх гаманців"""
    wallets = await wallet_service.get_wallets()
    return [schemas.WalletList(id=wallet.id,
                               address=wallet.address,
                               balance=wallet.balance,
                               private_key=wallet.private_key
                               ) for wallet in wallets]


@wallet_router.get('/wallets/current-user/', status_code=status.HTTP_200_OK, response_model=List[schemas.WalletList])
@inject
async def get_wallets_current_user(request: Request,
                                   permission: Permission = Depends(Provide[Container.permission]),
                                   wallet_service: WalletService = Depends(Provide[Container.wallet_service])):
    """Отримання всіх гаманців авторизованого користувача"""
    user = await permission.get_current_user(request)
    if user:
        wallets = await wallet_service.get_wallets_user(user.id)
        return [schemas.WalletList(id=wallet.id,
                                   address=wallet.address,
                                   balance=wallet.balance,
                                   private_key=wallet.private_key
                                   ) for wallet in wallets]


@wallet_router.post('/wallet/etherscan/', status_code=status.HTTP_200_OK, response_model=schemas.WalletEtherscan)
@inject
async def get_address_in_etherscan(address: str,
                                   request: Request,
                                   permission: Permission = Depends(Provide[Container.permission]),
                                   wallet_service: WalletService = Depends(Provide[Container.wallet_service])):
    """Отримання url адреси на etherscan"""
    user = await permission.get_current_user(request)
    if user:
        return await wallet_service.get_address_etherscan(address)


@wallet_router.post('/wallet/', status_code=status.HTTP_200_OK, response_model=schemas.WalletCreate)
@inject
async def create_wallet(request: Request,
                        permission: Permission = Depends(Provide[Container.permission]),
                        wallet_service: WalletService = Depends(Provide[Container.wallet_service])):
    """Стоврення гаманця для авторизованого користувача"""
    user = await permission.get_current_user(request)
    if user:
        wallet = await wallet_service.create_wallet(user_id=user.id)
        return schemas.WalletCreate(id=wallet.id,
                                    address=wallet.address,
                                    balance=wallet.balance,
                                    private_key=wallet.private_key,
                                    user_id=wallet.user_id,
                                    asset_id=wallet.asset_id)


@wallet_router.post('/wallet/import/', status_code=status.HTTP_200_OK, response_model=schemas.WalletList)
@inject
async def import_wallet(item: schemas.WalletImport,
                        request: Request,
                        wallet_service: WalletService = Depends(Provide[Container.wallet_service]),
                        permission: Permission = Depends(Provide[Container.permission])):
                        # moralis_service: MoralisService = Depends(Provide[Container.moralis_service])):
    """Імпортування гаманця за допомогою приватного ключа"""
    user = await permission.get_current_user(request)
    if user:
        wallet = await wallet_service.import_wallet(item.private_key, user.id)
        address = schemas.CheckBalance(address=wallet.address)
        # transactions = await moralis_service.get_all_transactions(address=wallet.address)
        # if transactions:
        #     await wallet_service.create_transactions(transactions)
        await wallet_service.get_balance(address)
        return schemas.WalletList(id=wallet.id,
                                   address=wallet.address,
                                   balance=wallet.balance,
                                   private_key=wallet.private_key
                                   )

@wallet_router.get('/wallet/transactions/{address}', status_code=status.HTTP_200_OK, response_model=List[schemas.ListTransaction])
@inject
async def get_all_transactions_by_address(address: str,
                                          request: Request,
                                          wallet_service: WalletService = Depends(Provide[Container.wallet_service]),
                                          permission: Permission = Depends(Provide[Container.permission])):
    user = await permission.get_current_user(request)
    if user:
        transactions = await wallet_service.get_all_transaction_by_address(address)
        return [schemas.ListTransaction(id=transaction.id,
                                        hash=transaction.hash,
                                        from_send=transaction.from_send,
                                        to_send=transaction.to_send,
                                        value=transaction.value,
                                        txn_fee=transaction.txn_fee,
                                        date_send=transaction.date_send,
                                        status=transaction.status)
                for transaction in transactions]

@wallet_router.post('/send-transaction/', status_code=status.HTTP_200_OK)
@inject
async def send_transaction(item: schemas.TransactionCreate,
                           request: Request,
                           permission: Permission = Depends(Provide[Container.permission]),
                           wallet_service: WalletService = Depends(Provide[Container.wallet_service])):
    """Відправка транзакції"""
    user = await permission.get_current_user(request)
    if user:
        return await wallet_service.send_transaction(item)

@wallet_router.post('/wallet/balance/', status_code=status.HTTP_200_OK, response_model=schemas.Wallet)
@inject
async def get_balance_by_address(item: schemas.CheckBalance,
                                 request: Request,
                                 permission: Permission = Depends(Provide[Container.permission]),
                                 wallet_service: WalletService = Depends(Provide[Container.wallet_service])):
    """Отримання балансу гаманця"""
    user = await permission.get_current_user(request)
    if user:
        wallet = await wallet_service.get_balance(item)
        return schemas.Wallet(id=wallet.id,
                              address=wallet.address,
                              private_key=wallet.private_key,
                              balance=wallet.balance,
                              user_id=wallet.user_id)


@wallet_router.get('/wallet/transaction/', status_code=status.HTTP_200_OK, response_model=schemas.ListTransaction)
@inject
async def get_transaction_by_hash(txn_hash: str,
                                  request: Request,
                                  permission: Permission = Depends(Provide[Container.permission]),
                                  wallet_service: WalletService = Depends(Provide[Container.wallet_service])):
    """Отримання даних транзакції через хеш"""
    user = await permission.get_current_user(request)
    if user:
        if txn_hash.startswith("0x"):
            transaction = await wallet_service.get_transaction_in_db(txn_hash)
            return schemas.ListTransaction(id=transaction.id,
                                           hash=transaction.hash,
                                           from_send=transaction.from_send,
                                           to_send=transaction.to_send,
                                           value=transaction.value,
                                           txn_fee=transaction.txn_fee,
                                           date_send=transaction.date_send,
                                           status=transaction.status)
        raise HTTPException(detail='Ви ввели невірний хеш', status_code=status.HTTP_400_BAD_REQUEST)

@wallet_router.get('/wallet/private_key/', status_code=status.HTTP_200_OK, include_in_schema=False)
@inject
async def get_private_key_address(address: str,
                                  request: Request,
                                  permission: Permission = Depends(Provide[Container.permission]),
                                  wallet_service: WalletService = Depends(Provide[Container.wallet_service]),
                                  user_service: UserService = Depends(Provide[Container.user_service])):
    user = await permission.get_current_user(request)
    if user:
        wallet = await wallet_service.get_wallet_by_address(address)
        return wallet.private_key

