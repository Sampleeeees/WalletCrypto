from dependency_injector import containers, providers
from config.database import Database
from config_fastapi import settings
from src.authentication.permissions import Permission
from src.parser.service import ParserService
from src.users.service import UserService
from src.wallets.service import WalletService
from src.wallets.web3_service import Web3Service


class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(packages=settings.APPS_SERVICE, auto_wire=True)

    print(wiring_config.packages)

    database = providers.Singleton(
        Database,
        db_url=settings.DATABASE_URI
    )

    user_service = providers.Factory(
        UserService,
        session_factory=database.provided.get_db_session
    )

    wallet_service = providers.Factory(
        WalletService,
        session_factory=database.provided.get_db_session,
        provider_url=settings.INFURA_SEPOLIA_URI
    )

    web3_service = providers.Factory(
        Web3Service,
        provider_url=settings.INFURA_URI,
        http_provider_url=settings.INFURA_URI_HTTP,
        user_wallets=wallet_service.provided.get_wallets
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



