import asyncio

from propan import PropanApp, RabbitBroker
from propan.annotations import Logger
from propan.brokers.rabbit import ExchangeType, RabbitExchange, RabbitQueue


broker = RabbitBroker("amqp://guest:guest@localhost:5672/")
app = PropanApp(broker)

async def parcer():
    print('Parcer Work')
    return 'Hello parcer'

@broker.handle("test")
async def base_handler(body):
    print(body)
    await parcer()