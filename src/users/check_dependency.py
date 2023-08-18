import asyncio

from dependency_injector.wiring import Provide, inject
from fastapi import Depends

from src.core.containers import Container
from src.users.service import UserService
from src.wallets.web3_service import Web3Service


@inject
async def check_dependency(user_service: UserService = Provide[Container.user_service]):
    users = await user_service.get_users()
    return users

async def main():
    await check_dependency()


if __name__ == '__main__':
    container = Container()
    asyncio.run(main())