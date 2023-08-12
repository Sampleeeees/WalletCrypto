from dependency_injector import containers, providers
from dependency_injector.wiring import Provide

from config.database import Database
from config_fastapi import settings
from src.authentication.permissions import Permission
from src.users.service import UserService
from src.wallets.service import WalletService


class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(packages=settings.APPS_SERVICE)

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
        session_factory=database.provided.get_db_session
    )

    permission = providers.Singleton(
        Permission,
        secret_key=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
        user_service=user_service
    )



