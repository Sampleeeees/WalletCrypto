import asyncio

from web3 import Web3
from web3.middleware import geth_poa_middleware
from propan.brokers.rabbit import RabbitBroker

from config_fastapi import settings
from src.wallets.service import WalletService


class Web3Service:

    def __init__(self, provider_url: str, http_provider_url: str, wallet_service: WalletService):
        self.provider_url = provider_url
        self.http_provider_url = http_provider_url
        self.previous_block_number = None
        self.wallet_service = wallet_service

    # Провайдер Web3 для запиту через http
    async def get_ws_provider(self) -> Web3:
        ws_provider = Web3(Web3.WebsocketProvider(self.provider_url))
        ws_provider.middleware_onion.inject(geth_poa_middleware, layer=0)
        return ws_provider

    # Провайдер Web3 для запиту через websocket
    async def get_http_provider(self) -> Web3:
        http_provider = Web3(Web3.HTTPProvider(self.http_provider_url))
        http_provider.middleware_onion.inject(geth_poa_middleware, layer=0)
        return http_provider

    # Перевірка номеру блоку минулого і теперішнього
    async def check_current_block(self, block_number: int) -> None:

        # Встановлення значення останнього блоку якщо воно не встановленно
        if self.previous_block_number is None:
            self.previous_block_number = block_number

        # Перевірка чи відрізняється останній блок з новим отриманим блоком
        if self.previous_block_number != block_number:
            block_diff: int = block_number - self.previous_block_number
            for i in range(self.previous_block_number + 1, self.previous_block_number + block_diff):
                with RabbitBroker() as broker:
                    broker.publish(message=i, queue='parser/parser_queue')

    # парсинг блоку на його номером
    async def parsing_block(self, block_number: int):
        from_address = set() # Set для отримання неповторюємих адресів що робили відправку транзакцій в блоці
        to_address = set() #  Set для отримання неповторюємих адресів що робили відправку транзакцій в блоці
        processed_transactions = []

        provider = await self.get_http_provider() # Запуск провайдера Ethereum
        block_transactions = provider.eth.get_block(block_number)['transactions'] # Отримання всіх транзакцій

        # Цикл по хешу транзакціям та отримання з хешу відправника та отримувача
        for txn_hash in block_transactions:
            txn = provider.eth.get_transaction(txn_hash)
            print('HexByte charge', type(txn_hash.hex()), type(txn_hash))
            from_address.add(txn['from'])
            to_address.add(txn['to'])
            processed_transactions.append({'hash': txn_hash, 'from': txn['from'], 'to': txn['to']})
            print('Processed hash type', type(processed_transactions[0]['hash']))


        # отримання адресів з бази давних із set адресів транзакції
        my_wallet_from, my_wallet_to = await self.wallet_service.get_wallets_from_transaction(from_send=from_address,
                                                                                              to_send=to_address)

        for processed_txn in processed_transactions:
            if processed_txn['from'] in my_wallet_from:
                await self.wallet_service.create_or_update_transaction(processed_txn['hash'])

            elif processed_txn['to'] in my_wallet_to:
                await self.wallet_service.create_or_update_transaction(processed_txn['hash'])

        return my_wallet_from, my_wallet_to

















