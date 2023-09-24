
from fastapi import FastAPI
from sqladmin import Admin
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from config.database import engine
from config_fastapi import settings
from src.core.adminAuth import authentication_backend

from src.core.routers import routers
from src.core.containers import Container
from config_socketio.socket_application import socketio_app

from src.wallets.admin import WalletAdmin, TransactionAdmin, BlockchainAdmin, AssetAdmin
from src.users.admin import UserAdmin
from src.ibay.admin import ProductAdmin
from src.delivery.admin import OrderAdmin
from src.chats.admin import MessageAdmin

# функція дя створення fastapi та підключення wiring container для dependency_injector
def create_app() -> FastAPI:
    container = Container()

    tags_metadata = [
        {
            "name": "AsyncAPI docs",
            "externalDocs": {
                "description": "AsyncAPI documentation for chat",
                "url": "http://127.0.0.1:8000/asyncapi_docs/",
            },
        },
        {
            "name": "Auth",
            "description": "Authorization or registration"
        },
        {
            "name": "User",
            "description": "User CRUD operation"
        },
        {
            "name": "Wallet",
            "description": "Wallet operations"
        },
        {
            "name": "Message",
            "description": "Message operations"
        },
        {
            "name": "Product",
            "description": "Product operations"
        }
    ]

    app = FastAPI(title=settings.PROJECT_NAME,
                  description='API for CryptoWallet',
                  version="1.0.1",
                  openapi_tags=tags_metadata)

    app.container = container
    # broker.container = container

    app.include_router(routers)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
    # Підключення статики та вебсокету до fastapi
    app.mount('/static/', StaticFiles(directory='static'), name='static')
    app.mount("/ws/", socketio_app)

    # Стоврення адмінки sqladmin
    admin = Admin(app, engine=engine, authentication_backend=authentication_backend)

    # Підключення класів моделей для адміністрування
    admin.add_view(UserAdmin)
    admin.add_view(WalletAdmin)
    admin.add_view(BlockchainAdmin)
    admin.add_view(AssetAdmin)
    admin.add_view(TransactionAdmin)
    admin.add_view(ProductAdmin)
    admin.add_view(OrderAdmin)
    admin.add_view(MessageAdmin)

    @app.on_event("startup")
    async def on_startup():
        container.database.provided.init_db()



    # @app.on_event('startup')
    # async def startup_app():
    #     app.broker = broker
    #     app.broker.include_router(parser_broker_router)
    #     app.broker.include_router(wallet_consumer)
    #     print('START')
    #     await broker.start()
    #
    # @app.on_event('shutdown')
    # async def shutdown_app():
    #     print('Closing propan')
    #     await broker.close()
    return app

app = create_app()





