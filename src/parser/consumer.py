from dependency_injector.wiring import Provide, inject
from propan import RabbitRouter, Depends
from propan.brokers.rabbit import RabbitQueue
from web3 import Web3
from config_celery.tasks import parse_block
from celery.result import AsyncResult

from src.core.containers import Container
from src.wallets.service import WalletService

parser_broker_router = RabbitRouter(prefix='parser/')

queue_parser = RabbitQueue(name='parser_queue')
queue_transaction_hash = RabbitQueue(name='parser_transaction')

@parser_broker_router.handle(queue_parser)
async def send_block_in_celery(body):
    result: AsyncResult = parse_block.apply_async(args=[body])
    print(result.result)


@parser_broker_router.handle(queue_transaction_hash)
@inject
async def send_transaction_in_celery(body, wallet_service=Depends(Provide[Container.wallet_service])):
    splited_body = body.split()
    transaction, action = splited_body[0], splited_body[1]
    provider = await wallet_service.provider()
    txn_data = provider.eth.get_transaction(transaction)
    await wallet_service.create_transaction({'hash': txn_data['hash'],
                                             'from_send': txn_data['from'],
                                             'to_send': txn_data['to'],
                                             'value': txn_data['value'],
                                             'gas': txn_data['gas']})