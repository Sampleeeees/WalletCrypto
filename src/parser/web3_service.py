from web3 import Web3
from web3.middleware import geth_poa_middleware


class Web3Service:

    def __init__(self, provider_url: str, http_provider_url: str):
        self.provider_url = provider_url
        self.http_provider_url = http_provider_url

    # Провайдер Web3 для запиту через http
    async def get_ws_provider(self) -> Web3:
        ws_provider = Web3(Web3.WebsocketProvider(self.provider_url, websocket_kwargs={'max_size': 2**50}))
        ws_provider.middleware_onion.inject(geth_poa_middleware, layer=0)
        return ws_provider

    # Провайдер Web3 для запиту через websocket
    async def get_http_provider(self) -> Web3:
        http_provider = Web3(Web3.HTTPProvider(self.http_provider_url))
        http_provider.middleware_onion.inject(geth_poa_middleware, layer=0)
        return http_provider























