from propan import RabbitBroker, PropanApp
from src.parser.consumer import parser_broker_router
from src.wallets.consumers import wallet_consumer

broker = RabbitBroker("amqp://guest:guest@localhost:5672")
broker.include_router(parser_broker_router)
broker.include_router(wallet_consumer)
app = PropanApp(broker)