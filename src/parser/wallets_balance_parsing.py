import asyncio

from dependency_injector.wiring import Provide

from config_fastapi.fastapi_manager import fastapi_mgr
from src.core.containers import Container
from src.wallets.schemas import CheckBalance
from src.wallets.service import WalletService


async def verify_balance(wallet_service: WalletService = Provide[Container.wallet_service]):
    while True:
        await asyncio.sleep(60)
        wallets = await wallet_service.get_wallets()
        for wallet in wallets:
            item = CheckBalance(address=wallet.address)
            wallet_balance = await wallet_service.get_balance(item)
            await fastapi_mgr.emit("update_wallet_balance", {"balance": wallet_balance.balance,
                                                             "wallet_id": wallet_balance.id})

