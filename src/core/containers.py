import sys

from dependency_injector import containers, providers

from config.database import Database
from config_fastapi import settings

from src.authentication.permissions import Permission
from src.chats.service import ChatService
from src.core.storage_bunny import BunnyStorage
from src.delivery.service import DeliveryService
from src.ibay.service import IBayService
# from src.parser.moralis_service import MoralisService
from src.parser.service import ParserService
from src.users.service import UserService
from src.wallets.service import WalletService
from src.parser.web3_service import Web3Service


class Container(containers.DeclarativeContainer):
    # Файли в яких знаходиться @inject
    wiring_config = containers.WiringConfiguration(packages=settings.APPS_SERVICE)


    database = providers.Singleton(
        Database
    )

    bunny_storage = providers.Singleton(
        BunnyStorage,
        api_key=settings.BUNNY_API_KEY,
        storage_name=settings.BUNNY_STORAGE_NAME,
        storage_region=settings.BUNNY_STORAGE_REGION
    )

    web3_service = providers.Factory(
        Web3Service,
        provider_url=settings.INFURA_URI,
        http_provider_url=settings.INFURA_URI_HTTP,
    )

    # moralis_service = providers.Singleton(
    #     MoralisService,
    #     api_key=settings.MORALIS_API_KEY
    # )

    user_service = providers.Factory(
        UserService,
        session_factory=database.provided.get_db_session,
        bunny_storage=bunny_storage
    )

    wallet_service = providers.Factory(
        WalletService,
        session_factory=database.provided.get_db_session,
        provider_url=settings.INFURA_URI,
        http_provider_url=settings.INFURA_URI_HTTP
    )


    permission = providers.Singleton(
        Permission,
        secret_key=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
        user_service=user_service # знаходяться в одному сервісі
    )

    parser_service = providers.Factory(
        ParserService,
        provider_url=settings.INFURA_URI,
        session_factory=database.provided.get_db_session,
        web3_service=web3_service # знаходяться в одному сервісі
    )

    ibay_service = providers.Factory(
        IBayService,
        session_factory=database.provided.get_db_session,
        bunny_storage=bunny_storage
    )

    delivery_service = providers.Factory(
        DeliveryService,
        session_factory=database.provided.get_db_session
    )

    chat_service = providers.Factory(
        ChatService,
        session_factory=database.provided.get_db_session
    )






