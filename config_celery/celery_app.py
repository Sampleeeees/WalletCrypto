from celery import Celery

from config_celery.celery_worker import app
from src.core.containers import Container


def create_celery_app() -> Celery:
    container = Container()
    celery_app = app
    return celery_app

celery_app = create_celery_app()