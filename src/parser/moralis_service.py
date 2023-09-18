from datetime import datetime, timedelta

from dependency_injector.wiring import Provide
from moralis.evm_api import evm_api

from src.core.containers import Container


class MoralisService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.moralis = evm_api

    def get_all_transactions(self, address: str):
        params = {
            "address": address,
            "chain": "eth",
            "subdomain": "",
            "from_date": datetime.now() - timedelta(days=60),
            "to_date": datetime.now(),
            "cursor": "",
            "limit": 100,
        }

        result = self.moralis.transaction.get_wallet_transactions(api_key=self.api_key,
                                                                  params=params, # noqa
                                                                  )
        return result


if __name__ == "__main__":
    container = Container()
    container.wire(['__main__'])
    moralis = Provide[container.moralis_service]

    print(moralis.get)
