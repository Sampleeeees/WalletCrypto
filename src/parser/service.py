import json

from propan.brokers.rabbit import RabbitBroker
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config.database import LastSuccessBlock
from config_fastapi import settings
from config_fastapi.fastapi_manager import fastapi_mgr
from src.wallets.models import Wallet
from src.wallets.service import WalletService
from src.parser.web3_service import Web3Service


class ParserService:
    def __init__(self, provider_url: str, session_factory: AsyncSession, web3_service: Web3Service):
        self.provider_url = provider_url
        self.session_factory = session_factory
        self.web3_service = web3_service
        self.latest_block = None


    # Отримання тільки тих адресів які були задіяні
    async def get_wallets_from_transaction(self, from_send: set, to_send: set):
        async with self.session_factory() as db:
            result_from = await db.execute(select(Wallet).where(Wallet.address.in_(from_send)))
            result_to = await db.execute(select(Wallet).where(Wallet.address.in_(to_send)))
            return [wallet_from.address for wallet_from in result_from.scalars().all()], [wallet_to.address for
                                                                                              wallet_to in
                                                                                              result_to.scalars().all()]


    # Отримання або оновлення номеру блоку в БД
    async def get_or_update_block_number(self, block_number: int = None, action: str = None):
        async with self.session_factory() as db:
            get_block_number = await db.get(LastSuccessBlock, 1)
            if action == 'update':
                get_block_number.block_number = block_number
                db.add(get_block_number)
                await db.commit()
                await db.refresh(get_block_number)
            return get_block_number.block_number

    # Отримання останнього блоку з бази даних та перевірка чи вже був такий опрацьовано
    async def get_latest_block(self):
        provider = await self.web3_service.get_http_provider() # отрмання провайдеу infura
        block_number = provider.eth.get_block('latest')['number'] # останній номер блоку в інфурі

        if self.latest_block is None:
            self.latest_block = await self.get_or_update_block_number()
            return self.latest_block

        print("---------")
        print("---------")
        print('PreviousBlock', self.latest_block)
        print('Block', block_number)
        print("---------")
        print("---------")

        list_itter = []
        if self.latest_block != block_number:
            block_diff = block_number - self.latest_block
            for i in range(self.latest_block + 1, self.latest_block + block_diff):
                print(i)
                list_itter.append(i)
                async with RabbitBroker(settings.RABBITMQ_URI) as broker:
                    await broker.publish(message=i, queue='parser/parser_queue')
            await self.get_or_update_block_number(block_number=block_number, action='update')
            self.latest_block = block_number
            return block_number
        return None

    # парсинг блоку по його номеру
    async def parsing_block(self, block_number: int):
        from_address = set()  # Set для отримання неповторюємих адресів що робили відправку транзакцій в блоці
        to_address = set()  # Set для отримання неповторюємих адресів що робили відправку транзакцій в блоці
        processed_transactions = []  # Зберігання хешу та адреси з value

        provider = await self.web3_service.get_http_provider()  # Запуск провайдера Ethereum
        block_transactions = provider.eth.get_block(block_number, full_transactions=True)['transactions']  # Отримання всіх транзакцій

        # Цикл по хешу транзакціям та отримання з хешу відправника та отримувача
        for txn in block_transactions:
            from_address.add(txn['from'])
            to_address.add(txn['to'])
            processed_transactions.append(
                {'hash': txn['hash'], 'from': txn['from'], 'to': txn['to'], 'value': txn['value']})

        # отримання адресів з бази давних із set адресів транзакції
        my_wallet_from, my_wallet_to = await self.get_wallets_from_transaction(from_send=from_address,
                                                                               to_send=to_address)

        for processed_txn in processed_transactions:
            if processed_txn['from'] in my_wallet_from:
                async with RabbitBroker() as broker:
                    await broker.publish(message={"type": "create_or_update", "data": processed_txn['hash'].hex()},
                                         queue="wallet/wallet_queue")
                async with RabbitBroker() as broker:
                    await broker.publish(message={"type": "balance_operation",
                                                  "address": processed_txn['from'],
                                                  "value": processed_txn['value'],
                                                  "action": 'from'
                                                  },queue='wallet/wallet_queue')

                async with RabbitBroker() as broker:
                    await broker.publish(message={"type": "send_notification",
                                                  "txn_hash": processed_txn['hash'].hex(),
                                                  "address": processed_txn['from'],
                                                  "operation": "send",
                                                  "value": processed_txn["value"],
                                                  "message": f'З гаманця знято {processed_txn["value"]} Eth'},
                                                  queue='wallet/wallet_queue')



            elif processed_txn['to'] in my_wallet_to:
                async with RabbitBroker() as broker:
                    await broker.publish(message={"type": "create_or_update", "data": processed_txn['hash'].hex()},
                                         queue='wallet/wallet_queue')
                async with RabbitBroker() as broker:
                    await broker.publish(message={"type": "balance_operation",
                                                  "address": processed_txn['from'],
                                                  "value": processed_txn['value'],
                                                  "action": 'to'
                                                  },queue='wallet/wallet_queue')
                async with RabbitBroker() as broker:
                    await broker.publish(message={"type": "send_notification",
                                                  "txn_hash": processed_txn['hash'].hex(),
                                                  "address": processed_txn['to'],
                                                  "operation": "get",
                                                  "value": processed_txn["value"],
                                                  "message": f'На гаманець прийшло {processed_txn["value"]} Eth'},
                                         queue='wallet/wallet_queue')

        return my_wallet_from, my_wallet_to

