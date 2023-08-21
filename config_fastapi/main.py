from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from config_fastapi import settings
import src

from src.core.routers import routers
from src.core.containers import Container
from config_socketio.socket_application import socketio_app


def create_app() -> FastAPI:
    container = Container()

    app = FastAPI(title=settings.PROJECT_NAME, description='API for CryptoWallet')
    app.container = container
    app.include_router(src.core.routers.routers)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
    app.mount("/socketio/", socketio_app)
    return app

app = create_app()



