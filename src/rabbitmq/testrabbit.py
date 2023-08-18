import asyncio

from dependency_injector.wiring import inject, Provide
from propan import PropanApp, RabbitBroker
from propan.annotations import Logger
from propan.brokers.rabbit import ExchangeType, RabbitExchange, RabbitQueue
from web3 import Web3

web3 = Web3(Web3.WebsocketProvider("wss://mainnet.infura.io/ws/v3/0541bae5c97049309f8d2324648c2c2c"))

broker = RabbitBroker("amqp://guest:guest@localhost:5672")
app = PropanApp(broker)
exchange = RabbitExchange(name='test_exchange', type=ExchangeType.TOPIC, durable=True)

queue_test = RabbitQueue(name='test_queue', durable=True)
queue_celery = RabbitQueue(name='celery_queue', durable=True, routing_key='.celery')


@broker.handle(queue=queue_test, exchange=exchange)
async def parse_block(body):
    get_block = web3.eth.get_block(body)
    transactions=get_block['transactions']
    for transaction in transactions:
        txn = web3.eth.get_transaction(transaction)
        print('-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*')
        print(txn['from'])
        print(txn['to'])
        print('-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*')