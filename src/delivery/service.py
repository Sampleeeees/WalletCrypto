import asyncio
import datetime
import random

from propan import RabbitBroker
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from config_celery.requests_google import fetch
from config_fastapi import settings
from config_fastapi.fastapi_manager import fastapi_mgr
from src.delivery import schemas
from src.delivery.models import Order, StatusOrder
from src.ibay.models import Product
from src.wallets.models import Wallet


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

    async def get_all_my_product(self, user_id: int):
        async with self.session_factory() as db:
            query = (
                select(Order)
                .join(Product, Order.product_id == Product.id)
                .where(Product.wallet.has(Wallet.user_id == user_id))
                .options(joinedload(Order.product))  # Завантажуємо пов'язаний продукт (optional)
                .options(joinedload(Order.transaction))  # Завантажуємо пов'язаний продукт (optional)
            )

            results = await db.execute(query)
            return results.scalars().all()

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
                    await fastapi_mgr.emit("update_product", {"status": "Turning",
                                                              "turning": order.transaction.to_send,
                                                              "order_id": order.id,
                                                              "comment": 'Отримали що order status == turning то відправляємо повернення коштів'})
                elif not order.status == StatusOrder.turning:
                    # Виконуємо якщо ця транзакція була успішною
                    if status:
                        request_google = await fetch() # 10000 запитів на гугл
                        # Якщо запит на гугл успішний
                        if request_google:
                            order.status = StatusOrder.delivery
                            await fastapi_mgr.emit("update_product", {"status": "Delivery",
                                                                      "order_id": order.id,
                                                                      "comment": "Запит на гугл пройшов успішно ставимо значення delivery"})
                        # Якщо запит на гугл неуспішний
                        elif not request_google:
                            order.status = StatusOrder.failed
                            # Відправка даних для транзакціх з поверненням комісії * 1.5
                            async with RabbitBroker(settings.RABBITMQ_URI) as broker:
                                new_transaction_id = await broker.publish(
                                    message={'from_send': order.transaction.from_send,
                                             'to_send': order.transaction.to_send,
                                             'value': order.transaction.txn_fee * 1.5},
                                    queue='wallet/wallet_turning',
                                    callback=True)
                                order.transaction_id = new_transaction_id

                            await fastapi_mgr.emit("update_product", {"status": "Failed",
                                                                      "order_id": order.id,
                                                                      "comment": "Запит на гугл пройшов не успішно ставимо status order failed"})
                    # Якщо транзакція все таки не пройшла
                    else:
                        order.status = StatusOrder.failed
                        async with RabbitBroker(settings.RABBITMQ_URI) as broker:
                            new_transaction_id = await broker.publish(
                                message={'from_send': order.transaction.from_send,
                                         'to_send': order.transaction.to_send,
                                         'value': order.transaction.txn_fee * 1.5},
                                queue='wallet/wallet_turning',
                                callback=True)
                            order.transaction_id = new_transaction_id
                        await fastapi_mgr("update_product", {'status': "Failed",
                                                             "order_id": order.id,
                                                             "comment": "Якщо транзакція відразу дала помилку"})
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
                    await fastapi_mgr.emit("update_product", {'status': "Finish",
                                                              "order_id": last_order.id,
                                                              "comment": "Ставимо значення finish"})
                elif random_int == 0:
                    last_order.status = StatusOrder.failed
                    async with RabbitBroker(settings.RABBITMQ_URI) as broker:
                        new_transaction_id = await broker.publish(
                            message={'from_send': last_order.transaction.from_send,
                                     'to_send': last_order.transaction.to_send,
                                     'value': last_order.transaction.txn_fee * 1.5},
                            queue='wallet/wallet_turning',
                            callback=True)
                        last_order.transaction_id = new_transaction_id
                    await fastapi_mgr.emit("update_product", {'status': "Failed",
                                                              "order_id": last_order.id,
                                                              "comment": "Random сказав що нам потрібо повернути кошти"})
                await db.commit()
                await db.refresh(last_order)
                return 'Random finished'

