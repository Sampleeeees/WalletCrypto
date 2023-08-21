import asyncio
import socketio
from propan import RabbitBroker
from propan.brokers.rabbit import RabbitExchange, RabbitQueue, ExchangeType
from web3 import Web3
from config_fastapi import settings
from dependency_injector.wiring import inject, Provide

from src.core.containers import Container
from src.parser.service import ParserService

mgr = socketio.AsyncAioPikaManager(settings.RABBITMQ_URI)
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins="*", client_manager=mgr)


exchange = RabbitExchange(name='test_exchange', type=ExchangeType.TOPIC, durable=True)
queue_celery = RabbitQueue(name='test_celery_queue', durable=True)

web3_ws = Web3(Web3.WebsocketProvider(settings.INFURA_SEPOLIA_URI))


@sio.on('connect')
async def connect(sid, environ):
    print(f'Client {sid} hello')




@sio.on('test')
async def test_handle(sid, data):
    print('Hello')

@sio.on('parsing')
@inject
async def inject_handle(sid, data, parser_service: ParserService = Provide[Container.parser_service]):
    while True:
        block_number = await parser_service.get_latest_block()
        if block_number is not None:
            async with RabbitBroker(settings.RABBITMQ_URI) as broker:
                await broker.publish(message=block_number, queue='parser/parser_queue')


@sio.event
async def get_balance():
    print('BALANCEEEE')


@sio.on('get_balance')
async def get_balance(sid, data):
    print(f'Balance {sid} and {data}')

@sio.on("disconnect")
async def disconnect(sid):
    print(f"Client {sid} disconnected")

