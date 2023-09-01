import socketio
from dependency_injector.wiring import Provide
from fastapi import FastAPI, Depends
from propan import RabbitBroker
from starlette.middleware.cors import CORSMiddleware

from config_fastapi import settings
import src

from src.core.routers import routers
from src.core.containers import Container
from config_socketio.socket_application import socketio_app
from src.parser.consumer import parser_broker_router
from src.wallets.consumers import wallet_consumer

# def create_broker() -> RabbitBroker:
#     container = Container()
#     broker = RabbitBroker("amqp://guest:guest@localhost:5672")
#     broker.container = container
#     return broker

# broker = create_broker()

def create_app() -> FastAPI:
    container = Container()

    app = FastAPI(title=settings.PROJECT_NAME, description='API for CryptoWallet')

    app.container = container
    # broker.container = container

    app.include_router(src.core.routers.routers)
    app.socketio_app = socketio_app
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
    app.mount("/socketio/", app.socketio_app)

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





