import asyncio
import socketio
from propan import RabbitBroker
from config_fastapi import settings
from dependency_injector.wiring import inject, Provide

from src.core.containers import Container
from src.parser.service import ParserService

mgr = socketio.AsyncAioPikaManager(settings.RABBITMQ_URI)
sio = socketio.AsyncServer(client_manager=mgr, async_mode='asgi', cors_allowed_origins="*", logger=True)


@sio.event
async def connect(sid, environ):
    print('New connect')


@sio.on('test')
async def test_handle(sid, data):
    print('Hello', data)


@sio.on('fastapi')
async def conn_fastapi(sid, data):
    print('HI FASTAPI')

@sio.on('parsing')
@inject
async def parse_block(sid, data, parser_service: ParserService = Provide[Container.parser_service]):
    while True:
        block_number = await parser_service.get_latest_block()
        if block_number is not None:
            async with RabbitBroker(settings.RABBITMQ_URI) as broker:
                await broker.publish(message=block_number, queue='parser/parser_queue')



@sio.on('get_balance')
async def get_balance(sid, data):
    print(f'Balance {sid} and {data}')

@sio.on("disconnect")
async def disconnect(sid):
    print(f"Client {sid} disconnected")

