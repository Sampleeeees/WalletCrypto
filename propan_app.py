from propan import RabbitBroker, PropanApp

from src.parser.consumer import parser_broker_router

broker = RabbitBroker("amqp://guest:guest@localhost:5672")
broker.include_router(parser_broker_router)
app = PropanApp(broker)