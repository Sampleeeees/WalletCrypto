import json
import secrets
from hexbytes import HexBytes
from datetime import datetime
from typing import Optional, Union, List
from eth_keys import keys
from eth_utils import decode_hex
from eth_account import Account
from fastapi import HTTPException
from propan import RabbitBroker
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from web3 import Web3
from web3.middleware import geth_poa_middleware
from decimal import Decimal

from config.database import LastSuccessBlock
from config_fastapi import settings
from . import schemas
from .models import Wallet, Transaction, TransactionStatus, Asset


class WalletService:
    def __init__(self, session_factory: AsyncSession, provider_url: str, http_provider_url: str):
        self.session_factory = session_factory
        self.provider_url = provider_url
        self.http_provider_url = http_provider_url

    # Провайдер для роботи з Web3
    async def provider(self) -> Web3:
        provider = Web3(Web3.WebsocketProvider(self.provider_url))
        provider.middleware_onion.inject(geth_poa_middleware, layer=0)
        return provider

    async def get_http_provider(self) -> Web3:
        http_provider = Web3(Web3.HTTPProvider(self.http_provider_url))
        http_provider.middleware_onion.inject(geth_poa_middleware, layer=0)
        return http_provider

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

    # отримання гаманця по адресі
    async def get_wallet_by_address(self, address: str):
        async with self.session_factory() as db:
            result = await db.execute(select(Wallet).where(Wallet.address == address))
            if result:
                return result.scalar()

    async def get_wallets_from_transaction_new(self, addresses: set):
        async with self.session_factory() as db:
            results = await db.execute(select(Wallet).where(Wallet.address.in_(addresses)))
            return [wallet.address for wallet in results.scalars().all()]


    # async def get_pending_transactions(self) -> List[Transaction]:
    #     async with self.session_factory() as db:
    #         result = await db.execute(select(Transaction).where(Transaction.status == TransactionStatus.pending))
    #         return result.scalars().all()

    # Отримання гаманців для авторизованого користувача
    async def get_wallets_user(self, user_id: int, wallet_id: int = None):
        async with self.session_factory() as db:
            if wallet_id:
                result = await db.execute(select(Wallet).where(Wallet.user_id == user_id, Wallet.id == wallet_id))
                return result.scalar_one_or_none()
            else:
                result = await db.execute(select(Wallet).where(Wallet.user_id == user_id))
                return result.scalars().all()


    # Перевірка чи є така транзакція в базі даних
    async def get_transaction_in_db(self, txn_hash: str) -> Union[Transaction, bool]:
        async with self.session_factory() as db:
            result = await db.execute(select(Transaction).where(Transaction.hash == txn_hash))
            transaction = result.scalar()
            if transaction:
                return transaction
            return False

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

                add_wallet = Wallet(private_key=private_key, address=address, user_id=user_id, asset_id=1)
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
                pk = keys.PrivateKey(decode_key)
                public = pk.public_key
                public_key = public.to_checksum_address()

                if any(wallet.address == public_key for wallet in await self.get_wallets_user(user_id)):
                    raise HTTPException(detail="Таку адресу ви вже зареєстрували", status_code=status.HTTP_400_BAD_REQUEST)

                wallet = Wallet(private_key=private_key, address=public_key, user_id=user_id, asset_id=1)
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
            if wallet:
                if wallet.asset_id is not None:
                    asset = await db.get(Asset, wallet.asset_id)
                    balance = balance / (int("1" + ("0" * asset.decimal_places)))

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
                transaction = Transaction(from_send=item.from_send, to_send=item.to_send, value=item.value, hash=txn_hash.hex(), date_send=datetime.now(),status=TransactionStatus.pending)

                db.add(transaction)
                await db.commit()
                await db.refresh(transaction)
            return provider.to_hex(txn_hash)
        except ValueError as e:
            raise HTTPException(detail=f'Не вийшло провести транзакцію. Error: {e}', status_code=status.HTTP_400_BAD_REQUEST)

    # Отримання транзакції по її хешу
    async def get_transaction(self, txn_hash: HexBytes):
        provider = await self.get_http_provider()
        try:
            txn = provider.eth.get_transaction_receipt(txn_hash)
            txn_json = provider.to_json(txn)
            return json.loads(txn_json)
        except Exception:
            raise HTTPException(detail='Транзакції не було знайдено', status_code=status.HTTP_404_NOT_FOUND)

    # Ствоерння транзакції через transaction_hash
    async def create_transaction(self, txn_hash: HexBytes) -> str:
        provider = await self.get_http_provider()
        txn = provider.eth.get_transaction(txn_hash)
        txn_receipt = provider.eth.get_transaction_receipt(txn_hash)
        txn_status = txn_receipt['status']
        txn_gasUsed = txn_receipt['gasUsed']
        async with self.session_factory() as db:
            asset = await db.get(Asset, 1)
            transaction = Transaction(hash=txn_hash.hex(),
                                      from_send=txn['from'],
                                      to_send=txn['to'],
                                      value=txn['value'] / (int("1" + ("0" * asset.decimal_places))),
                                      date_send=datetime.now(),
                                      txn_fee=((txn['gasPrice'] * txn_gasUsed) / (int("1" + ("0" * asset.decimal_places)))),
                                      status=TransactionStatus.success if txn_status == 1 else TransactionStatus.failed if txn_status == 0 else TransactionStatus.pending )
            db.add(transaction)
            await db.commit()
            await db.refresh(transaction)
            return 'Success created'

    # Оновлення транзакції
    async def update_transaction(self, txn_hash: HexBytes) -> Union[str, None]:
        provider = await self.get_http_provider()
        txn_gasPrice = provider.eth.get_transaction(txn_hash)['gasPrice']
        txn_receipt = provider.eth.get_transaction_receipt(txn_hash)
        txn_status = txn_receipt['status']
        txn_gasUsed = txn_receipt['gasUsed']
        async with self.session_factory() as db:
            result = await db.execute(select(Transaction).where(Transaction.hash == txn_hash.hex()))
            transaction = result.scalar()
            if transaction:
                asset = await db.get(Asset, 1)
                transaction.txn_fee = (txn_gasPrice * txn_gasUsed) / (int("1" + ("0" * asset.decimal_places)))
                transaction.date_send = datetime.now()
                transaction.status = (TransactionStatus.success if txn_status == 1 else TransactionStatus.failed if txn_status == 0 else TransactionStatus.pending)
                async with RabbitBroker(settings.RABBITMQ_URI) as broker:
                    await broker.publish(message={'transaction_id': transaction.id,
                                                  'type': 'update_order',
                                                  'status': True if transaction.status.success else False},
                                         queue='delivery/delivery_queue')
                db.add(transaction)
                await db.commit()
                await db.refresh(transaction)
                return 'Success update'

    # Створення або оновлення транзакції
    async def create_or_update_transaction(self, txn_hash: HexBytes) -> str:
        get_transaction = await self.get_transaction_in_db(txn_hash.hex())
        if get_transaction:
            updated_txn = await self.update_transaction(txn_hash)
            return updated_txn
        else:
            created_txn = await self.create_transaction(txn_hash)
            return created_txn

    # оновлення балансу гаманця коли отримав транзакцію з парсеру
    async def balance_operation(self, address: str, value: Union[int, float], action: str) -> None:
        wallet = await self.get_wallet_by_address(address=address)
        if wallet:
            async with self.session_factory() as db:
                asset = await db.get(Asset, 1)
                if wallet.balance is None:
                    wallet.balance = 0
                if action == 'from':
                    wallet.balance -= (Decimal(value) / (int("1" + ("0" * asset.decimal_places))))
                elif action == 'to':
                    wallet.balance += (Decimal(value) / (int("1" + ("0" * asset.decimal_places))))
                db.add(wallet)
                await db.commit()
                await db.refresh(wallet)







