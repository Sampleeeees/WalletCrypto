from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from propan import RabbitRouter

from config_fastapi.fastapi_manager import fastapi_mgr
from src.core.containers import Container
from propan.brokers.rabbit import RabbitQueue
from hexbytes import HexBytes

from src.wallets import schemas as schemas_wallet
from src.wallets.service import WalletService


wallet_consumer = RabbitRouter(prefix='wallet/')

wallet_queue = RabbitQueue(name='wallet_queue')


@inject
async def get_wallet_service(wallet_service=Depends(Provide[Container.wallet_service])):
    return wallet_service


@wallet_consumer.handle(wallet_queue)
@inject
async def get_wallet(body: dict):
    print("body", body)
    wallet_service: WalletService = await get_wallet_service()

    if body['type'] == 'create_or_update':
        await wallet_service.create_or_update_transaction(HexBytes(body['data']))

    elif body['type'] == 'send_notification':
        user_id = await wallet_service.get_user_by_wallet_address(address=body['address'])
        wallet = await wallet_service.get_wallet_by_address(address=body["address"])
        await fastapi_mgr.emit(event='txn_notification', data={"txn_hash": body['txn_hash'],
                                                               "address": body['address'],
                                                               "operation": body['operation'],
                                                               "message": body["message"],
                                                               "value": body["value"],
                                                               "wallet_id": wallet.id},
                               room=f'user_{user_id}')

    elif body['type'] == 'balance':
        await wallet_service.balance_operation(address=body['address'],
                                               value=body['value'],
                                               action=body['action'])

    elif body['type'] == 'turning':
        wallet = await wallet_service.get_wallet_by_address(body['from_send'])
        wallet_dict = schemas_wallet.TransactionCreate(from_send=body['from_send'],
                                                       to_send=body['to_send'],
                                                       value=body['value'],
                                                       private_key=wallet.private_key)
        txn_hash = await wallet_service.send_transaction(item=wallet_dict)
        txn_id = await wallet_service.get_transaction_in_db(txn_hash)
        return txn_id.id

