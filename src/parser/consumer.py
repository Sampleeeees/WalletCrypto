from propan import RabbitRouter
from propan.brokers.rabbit import RabbitQueue
from web3 import Web3
from config_celery.tasks import parse_block
from celery.result import AsyncResult

parser_broker_router = RabbitRouter(prefix='parser/')

queue_parser = RabbitQueue(name='parser_queue')

@parser_broker_router.handle(queue_parser)
async def send_block_in_celery(body):
    result: AsyncResult = parse_block.apply_async(args=[body])
    print(result.result)

