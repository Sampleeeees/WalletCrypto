from web3 import Web3
from web3.middleware import geth_poa_middleware
from propan.brokers.rabbit import RabbitBroker


class Web3Service:

    def __init__(self, provider_url: str, http_provider_url: str, user_wallets):
        self.provider_url = provider_url
        self.http_provider_url = http_provider_url
        self.address = "0x99526b0e49A95833E734EB556A6aBaFFAb0Ee167"
        self.previous_block_number = None
        self.user_wallets = user_wallets

    def get_ws_provider(self) -> Web3:
        ws_provider = Web3(Web3.WebsocketProvider(self.provider_url))
        ws_provider.middleware_onion.inject(geth_poa_middleware, layer=0)
        return ws_provider

    def get_http_provider(self) -> Web3:
        http_provider = Web3(Web3.HTTPProvider(self.http_provider_url))
        http_provider.middleware_onion.inject(geth_poa_middleware, layer=0)
        return http_provider

    def check_current_block(self, block_number: int):
        if self.previous_block_number is None:
            self.previous_block_number = block_number

        list_itter = []
        if self.previous_block_number != block_number:
            block_diff = block_number - self.previous_block_number
            for i in range(self.previous_block_number + 1, self.previous_block_number + block_diff):
                print(i)
                list_itter.append(i)
                with RabbitBroker() as broker:
                    broker.publish(message=i, queue='parser/parser_queue')
        return list_itter


    def parsing_block(self, block_number: int):
        transactions = self.get_http_provider().eth.get_block(block_number)['transactions']
        return len(transactions)




