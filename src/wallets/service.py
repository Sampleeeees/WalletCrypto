import json
import secrets
from hexbytes import HexBytes
from datetime import datetime
from typing import Optional
from eth_keys import keys
from eth_utils import decode_hex
from eth_account import Account
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from config_fastapi import settings
from starlette import status
from web3 import Web3
from web3.middleware import geth_poa_middleware
from . import schemas
from .models import Wallet, Transaction


class WalletService:
    def __init__(self, session_factory: AsyncSession):
        self.session_factory = session_factory

    # Провайдер для роботи з Web3
    async def provider(self):
        provider = Web3(Web3.WebsocketProvider(settings.INFURA_URI))
        provider.middleware_onion.inject(geth_poa_middleware, layer=0)
        return provider

    # Створення приватного ключа
    async def create_private_key(self):
        private_token = secrets.token_hex(32)
        private_key = "0x" + private_token
        return private_key

    # отримання всіх гаманців
    async def get_wallets(self):
        async with self.session_factory() as db:
            result = await db.execute(select(Wallet))
            return result.scalars().all()


    # Отримання гаманців для авторизованого користувача
    async def get_wallets_user(self, user_id: int):
        async with self.session_factory() as db:
            result = await db.execute(select(Wallet).where(Wallet.user_id == user_id))
            return result.scalars().all()

    # Отримання адреси на сайті etherscan
    async def get_address_etherscan(self, address: str):
        provide = await self.provider()
        if not provide.is_address(address):
            raise HTTPException(detail='Ви ввели невірний гаманець', status_code=status.HTTP_400_BAD_REQUEST)
        return {'url': f"https://etherscan.io/address/{address}"}


    # Створення гаманця
    async def create_wallet(self, user_id: int) -> Optional[Wallet]:
        async with self.session_factory() as db:
            private_key = await self.create_private_key()
            try:
                account = Account.from_key(private_key)
                address = account.address

                if any(wallet.address == address for wallet in await self.get_wallets_user(user_id)):
                    raise HTTPException(detail="Таку адресу гаманця вже зареєстровано", status_code=status.HTTP_400_BAD_REQUEST)

                add_wallet = Wallet(private_key=private_key, address=address, user_id=user_id)
                db.add(add_wallet)
                await db.commit()
                await db.refresh(add_wallet)
                return add_wallet

            except Exception:
                raise HTTPException(detail='Не вдалося стоврити гаманець', status_code=status.HTTP_400_BAD_REQUEST)

    # Імпорт гаманця по приватному ключу
    async def import_wallet(self, private_key: str, user_id: int) -> Optional[Wallet]:
        async with self.session_factory() as db:
            try:
                decode_key = decode_hex(private_key)
                print(decode_key)
                pk = keys.PrivateKey(decode_key)
                print(pk)
                public = pk.public_key
                print(public)
                public_key = public.to_checksum_address()

                if any(wallet.address == public_key for wallet in await self.get_wallets_user(user_id)):
                    raise HTTPException(detail="Таку адресу ви вже зареєстрували", status_code=status.HTTP_400_BAD_REQUEST)

                wallet = Wallet(private_key=private_key, address=public_key, user_id=user_id)
                db.add(wallet)
                await db.commit()
                await db.refresh(wallet)
                return wallet
            except Exception:
                raise HTTPException(detail='Не вийшло імпортувати гаманець. Схоже ви ввели невірний приватний ключ', status_code=status.HTTP_400_BAD_REQUEST)

    # Отримання балансу з гаманця
    async def get_balance(self, item: schemas.CheckBalance) -> Optional[Wallet]:
        provide = await self.provider()
        async with self.session_factory() as db:
            if not provide.is_address(item.address):
                raise HTTPException(detail='Ви ввели невірний або неіснуючий адрес', status_code=status.HTTP_400_BAD_REQUEST)
            balance = provide.eth.get_balance(item.address)
            result = await db.execute(select(Wallet).where(Wallet.address == item.address))
            wallet = result.scalars().first()
            if wallet is None:
                raise HTTPException(detail='Така адреса не зареєстрована на сервері',
                                    status_code=status.HTTP_400_BAD_REQUEST)
            if wallet.balance == balance:
                return wallet
            else:
                wallet.balance = balance
                db.add(wallet)
                await db.commit()
                await db.refresh(wallet)
                return wallet

    # Відправка транзакції
    async def send_transaction(self, item: schemas.TransactionCreate):
        provider = await self.provider()

        # Розрахунок скільки потрібно щоб було на гаманці відправника
        gas_price = provider.eth.gas_price
        gas_limit = 200000
        total_cost = gas_price * gas_limit + provider.to_wei(item.value, 'ether')

        txn = {
            'nonce': provider.eth.get_transaction_count(item.from_send),
            'to': item.to_send,
            'value': provider.to_wei(item.value, 'ether'),
            'gas': gas_limit,
            'gasPrice': gas_price
        }

        # перевірка чи справжні адреси гаманців введено
        if not provider.is_address(item.from_send) or not provider.is_address(item.to_send):
            raise HTTPException(detail='Ви ввели невірний гаманець', status_code=status.HTTP_400_BAD_REQUEST)

        # перевірка чи є на акаунту стільки коштів
        account_balance = provider.eth.get_balance(item.from_send)
        if account_balance < total_cost:
            raise HTTPException(detail='На вашому гаманці немає стільки eth', status_code=status.HTTP_400_BAD_REQUEST)


        try:
            signed_tx = provider.eth.account.sign_transaction(txn, item.private_key)
            txn_hash = provider.eth.send_raw_transaction(signed_tx.rawTransaction)
            async with self.session_factory() as db:
                transaction = Transaction(**item.model_dump(), hash=txn_hash, date_send=datetime.now(), txn_fee=gas_price)
                db.add(transaction)
                await db.commit
                await db.refresh(transaction)
            return provider.to_hex(txn_hash)
        except ValueError:
            raise HTTPException(detail='Не вийшло провести транзакцію', status_code=status.HTTP_400_BAD_REQUEST)

    # Отримання транзакції по її хешу
    async def get_transaction(self, txn_hash: str):
        provider = await self.provider()
        txn = provider.eth.get_transaction_receipt(txn_hash)
        txn_json = provider.to_json(txn)
        return json.loads(txn_json)









