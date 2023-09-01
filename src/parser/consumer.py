from propan import RabbitRouter
from propan.brokers.rabbit import RabbitQueue

from config_celery.tasks import parse_block


parser_broker_router = RabbitRouter(prefix='parser/')

queue_parser = RabbitQueue(name='parser_queue')

# Отримання повідомлень від черги parser_queue в RabbitMQ
@parser_broker_router.handle(queue_parser)
async def send_block_in_celery(block_number):
    print('PArser message', block_number)
    parse_block.apply_async(args=[block_number])



