import asyncio
import datetime
import random

from propan import RabbitBroker
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from config_celery.requests_google import fetch
from config_fastapi import settings
from src.delivery import schemas
from src.delivery.models import Order, StatusOrder


class DeliveryService:
    def __init__(self, session_factory: AsyncSession):
        self.session_factory = session_factory

    # Створення замовлення в бдшку
    async def create_order(self, item: schemas.OrderCreate):
        async with self.session_factory() as db:
            order = Order(date_send=datetime.datetime.now(),
                          status=StatusOrder.new,
                          product_id=item.product_id,
                          transaction_id=item.transaction_id)
            db.add(order)
            await db.commit()
            await db.refresh(order)
            return order


    # Оновлення замовлення. Юзається коли парсер ловить транзакцію і знаходить її в ордер таблиці
    async def update_product(self, txn_id: int, status: bool):
        async with self.session_factory() as db:
            query = (
                select(Order)
                .options(joinedload(Order.transaction))
                .where(Order.transaction_id == txn_id)
            )
            result = await db.execute(query)
            order = result.scalar_one_or_none()
            # Перевірка чи знайдено таке замовлення взагалі
            if order:
                # Якщо замовлення зі статусом failed і отримало повідомлення про те що парсер отримав транзакцію яка йшла для повернення коштів
                if order.status == StatusOrder.failed:
                    order.status = StatusOrder.turning # Ставимо значення на повернення
                    order.turning = order.transaction.to_send # В поле записуємо адресу на яку було повернути кошти
                else:
                    # Виконуємо якщо ця транзакція була успішною
                    if status:
                        request_google = await fetch() # 10000 запитів на гугл
                        # Якщо запит на гугл успішний
                        if request_google:
                            order.status = StatusOrder.delivery
                        # Якщо запит на гугл неуспішний
                        elif not request_google:
                            order.status = StatusOrder.failed
                            # Відправка даних для транзакціх з поверненням комісії * 1.5
                            async with RabbitBroker(settings.RABBITMQ_URI) as broker:
                                new_transaction_id = await broker.publish(
                                    message={'type': 'turning',
                                             'from_send': order.transaction.from_send,
                                             'to_send': order.transaction.to_send,
                                             'value': order.transaction.txn_fee * 1.5},
                                    queue='wallet/wallet_queue',
                                    callback=True)
                                order.transaction_id = new_transaction_id
                    # Якщо транзакція все таки не пройшла
                    else:
                        order.status = StatusOrder.failed
                        async with RabbitBroker(settings.RABBITMQ_URI) as broker:
                            new_transaction_id = await broker.publish(
                                message={'type': 'turning',
                                         'from_send': order.transaction.from_send,
                                         'to_send': order.transaction.to_send,
                                         'value': order.transaction.txn_fee * 1.5},
                                queue='wallet/wallet_queue',
                                callback=True)
                            order.transaction_id = new_transaction_id
                db.add(order)
                await db.commit()
                await db.refresh(order)
                return 'Finished operation'

    # Рандомне закриття замовлень
    async def random_delivery(self):
        async with self.session_factory() as db:
            query = (
                select(Order)
                .options(joinedload(Order.transaction))
                .where(Order.status == StatusOrder.delivery)
                .order_by(Order.id.asc())
            )
            result = await db.execute(query)
            last_order = result.scalars().first()

            if last_order:
                random_int = random.randint(0, 1)
                if random_int == 1:
                    last_order.status = StatusOrder.finish
                elif random_int == 0:
                    last_order.status = StatusOrder.failed
                    async with RabbitBroker(settings.RABBITMQ_URI) as broker:
                        new_transaction_id = await broker.publish(
                            message={'type': 'turning',
                                     'from_send': last_order.transaction.from_send,
                                     'to_send': last_order.transaction.to_send,
                                     'value': last_order.transaction.txn_fee * 1.5},
                            queue='wallet/wallet_queue',
                            callback=True)
                        last_order.transaction_id = new_transaction_id
                await db.commit()
                await db.refresh(last_order)
                return 'Random finished'

