import asyncio
from dependency_injector.wiring import Provide, inject
import logging
from src.core.containers import Container
from src.delivery.service import DeliveryService
from src.parser.service import ParserService
from .celery_worker import app


logger = logging.getLogger(__name__)


# Таска для парсингу блоку за його номером
@app.task(max_retries=3, retry_backoff=True)
@inject
def parse_block(block_number, parser_service: ParserService = Provide[Container.parser_service]):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(parser_service.parsing_block(block_number))

# Таска для закриття delivery продукту
@app.task(ignore_result=True)
@inject
def random_delivery(delivery_service: DeliveryService = Provide[Container.delivery_service]):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(delivery_service.random_delivery())









