from dependency_injector.wiring import Provide, inject
from web3 import Web3
import logging
from config_fastapi import settings
from src.core.containers import Container
from src.wallets.web3_service import Web3Service
from .celery_worker import app


logger = logging.getLogger(__name__)

web3 = Web3(Web3.HTTPProvider(settings.INFURA_URI_HTTP))

address = "0x99526b0e49A95833E734EB556A6aBaFFAb0Ee167"

# @app.task
# def parse_block(block_number):
#     get_block = web3.eth.get_block(block_number)
#     transactions = get_block['transactions']
#     list_transactions = []
#     for transaction in transactions:
#         txn = web3.eth.get_transaction(transaction)
#         logger.info('-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*')
#         logger.info(txn['from'])
#         logger.info('-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*')
#         if txn['from'] == address or txn['to'] == address:
#             list_transactions.append(web3.to_hex(transaction))
#
#         # Результат буде повернуто, а таска завершиться
#     return list_transactions


@app.task
@inject
def parse_block(block_number, web3_service: Web3Service = Provide[Container.web3_service]):
    return web3_service.parsing_block(block_number)



# @app.task
# def parse_block(block_number):
#     get_block = web3.eth.get_block(block_number)
#     transactions = get_block['transactions']
#     return transactions


# @app.task
# def parse_block(block_number):
#     time.sleep(5)
#     return block_number






