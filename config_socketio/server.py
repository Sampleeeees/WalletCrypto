import asyncio

import socketio
from propan.brokers.rabbit import RabbitExchange, RabbitQueue, ExchangeType
from web3 import Web3
from config_fastapi import settings
from dependency_injector.wiring import inject, Provide

from src.core.containers import Container
from src.parser.service import ParserService
from src.rabbitmq.testrabbit import broker
from src.wallets.web3_service import Web3Service


sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins="*")



exchange = RabbitExchange(name='test_exchange', type=ExchangeType.TOPIC, durable=True)
queue_celery = RabbitQueue(name='test_celery_queue', durable=True)

web3_ws = Web3(Web3.WebsocketProvider(settings.INFURA_SEPOLIA_URI))


@sio.on('connect')
async def connect(sid, environ):
    print(f'Client {sid} hello')

#@sio.on('event')
#async def handler(sid, data):
#    print(f'Hello event {sid}, {data}')
#    try:
#        latest_block = web3_ws.eth.get_block('latest')
#        tx_json = web3_ws.to_json(latest_block)
#        transactions = latest_block['transactions']
#        print(transactions)
#        for txn_hash in transactions:
#            txn = web3_ws.eth.get_transaction(txn_hash)
#            print(f"Transaction Hash: {web3_ws.to_hex(txn['hash'])}")
#            print(f"From: {txn['from']}")
#            print(f"To: {txn['to']}")
#            print(f"Value: {web3_ws.from_wei(txn['value'], 'ether')} Ether")
#            print("---------------------------")
#    except:
#        pass

last_transaction_block = None



@sio.on('test')
@inject
async def inject_handle(sid, data, parser_service: ParserService = Provide[Container.parser_service]):
    while True:
        if not broker.started:
            print('Broker Start')
            await broker.start()
        block_number = await parser_service.get_latest_block()
        await broker.publish(message=block_number, queue='parser/parser_queue')
        await asyncio.sleep(50)


# @sio.on('test')
# async def test_handler(sid, data):
#     global last_transaction_block
#     if not broker.started:
#         await broker.start()
#     while True:
#         latest_block = web3_ws.eth.get_block('latest')
#         if last_transaction_block is None or latest_block['number'] > last_transaction_block:
#             print(latest_block['number'])
#             await broker.publish(message=latest_block['number'], queue='parser/parser_queue')
#             last_transaction_block = latest_block['number']
#             await asyncio.sleep(50)

# @sio.on('event')
# async def test_handler(sid, data):
#     global last_transaction_block
#     while True:
#         latest_block = web3_ws.eth.get_block('latest')
#         print(latest_block['number'])
#         if last_transaction_block is None or latest_block['number'] > last_transaction_block:
#             result = task_parse_block.delay(latest_block['number'])



@sio.on("disconnect")
async def disconnect(sid):
    print(f"Client {sid} disconnected")

