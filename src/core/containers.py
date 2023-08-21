import socketio
from dependency_injector import containers, providers
from config.database import Database
from config_fastapi import settings
from src.authentication.permissions import Permission
from src.core.storage_bunny import BunnyStorage
from src.parser.service import ParserService
from src.users.service import UserService
from src.wallets.service import WalletService
from src.wallets.web3_service import Web3Service


class Container(containers.DeclarativeContainer):

    mgr = None

    wiring_config = containers.WiringConfiguration(packages=settings.APPS_SERVICE, auto_wire=True)

    print(wiring_config.packages)

    database = providers.Singleton(
        Database,
        db_url=settings.DATABASE_URI
    )

    bunny_storage = providers.Singleton(
        BunnyStorage,
        api_key=settings.BUNNY_API_KEY,
        storage_name=settings.BUNNY_STORAGE_NAME,
        storage_region=settings.BUNNY_STORAGE_REGION
    )

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

    web3_service = providers.Factory(
        Web3Service,
        provider_url=settings.INFURA_URI,
        http_provider_url=settings.INFURA_URI_HTTP,
        wallet_service=wallet_service
    )

    permission = providers.Singleton(
        Permission,
        secret_key=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
        user_service=user_service
    )

    parser_service = providers.Factory(
        ParserService,
        provider_url=settings.INFURA_URI
    )



