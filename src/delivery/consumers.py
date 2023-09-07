from dependency_injector.wiring import Provide, inject
from propan import RabbitRouter
from propan.brokers.rabbit import RabbitQueue

from src.core.containers import Container
from src.delivery.service import DeliveryService

delivery_consumer = RabbitRouter(prefix='delivery/')

delivery_queue = RabbitQueue(name='delivery_queue')


@inject
async def get_delivery_service(delivery_service: DeliveryService = Provide[Container.delivery_service]):
    return delivery_service

@delivery_consumer.handle(delivery_queue)
async def delivery_handle(body: dict):
    print('Delivery dict', body)
    delivery_service = await get_delivery_service()
    # Від транзакції яка йде на оновлення отримуємо її id та статус і перевіряємо через запит в бд чи була ця транзакція пов'язана з купівлею продукту
    if body['type'] == 'update_order':
        await delivery_service.update_product(txn_id=body['transaction_id'], status=body['status'])