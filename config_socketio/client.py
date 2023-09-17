import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import socketio
from dependency_injector.wiring import inject, Provide
from propan import RabbitBroker

from config_fastapi import settings
from src.core.containers import Container
from src.parser.service import ParserService


@inject
async def parse_block(parser_service: ParserService = Provide[Container.parser_service]):
    while True:
        block_number = await parser_service.get_latest_block()
        if block_number is not None:
    # for i in range(2):
            async with RabbitBroker(settings.RABBITMQ_URI) as broker:
                await broker.publish(message=block_number, queue='parser/parser_queue')



if __name__ == '__main__':
    container = Container()
    container.wire(['__main__'])
    asyncio.run(parse_block())