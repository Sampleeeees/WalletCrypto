from fastapi import FastAPI
from config_fastapi import settings
import src
from src.core.routers import routers
from src.core.containers import Container


def create_app() -> FastAPI:
    container = Container()

    app = FastAPI(title=settings.PROJECT_NAME, description='API for CryptoWallet')
    app.container = container
    app.include_router(src.core.routers.routers)
    return app


app = create_app()

