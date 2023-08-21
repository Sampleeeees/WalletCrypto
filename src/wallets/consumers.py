from propan import RabbitBroker, RabbitRouter
from propan.brokers.rabbit import RabbitExchange, ExchangeType

wallet_consumer = RabbitRouter()

socketio_exchange = RabbitExchange(name='socketio', type=ExchangeType.FANOUT)


@wallet_consumer.handle(queue='socketio', exchange=socketio_exchange)
async def get_test_mgr(body):
    print(body)

