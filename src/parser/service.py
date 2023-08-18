from propan.brokers.rabbit import RabbitBroker
from web3 import Web3
from web3.middleware import geth_poa_middleware

from config_fastapi import settings


class ParserService:
    def __init__(self, provider_url:str):
        self.provider_url = provider_url
        self.previous_block_number = None

    async def provider(self):
        provider = Web3(Web3.WebsocketProvider(self.provider_url))
        provider.middleware_onion.inject(geth_poa_middleware, layer=0)
        return provider

    async def get_latest_block(self):
        provider = await self.provider()
        block_number = provider.eth.get_block('latest')['number']
        if self.previous_block_number is None:
            self.previous_block_number = block_number

        print('PreviousBlock', self.previous_block_number)
        print('Block', block_number)

        list_itter = []
        if self.previous_block_number != block_number:
            block_diff = block_number - self.previous_block_number
            for i in range(self.previous_block_number + 1, self.previous_block_number + block_diff):
                print(i)
                list_itter.append(i)
                async with RabbitBroker(settings.RABBITMQ_URI) as broker:
                    await broker.publish(message=i, queue='parser/parser_queue')
        self.previous_block_number = block_number
        return block_number

