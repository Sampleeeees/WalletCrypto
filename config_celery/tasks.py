import asyncio
from dependency_injector.wiring import Provide, inject
import logging
from src.core.containers import Container
from src.wallets.web3_service import Web3Service
from .celery_worker import app


logger = logging.getLogger(__name__)


@app.task
@inject
def parse_block(block_number, web3_service: Web3Service = Provide[Container.web3_service]):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(web3_service.parsing_block(block_number))







