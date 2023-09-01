from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.core.storage_bunny import BunnyStorage
from src.ibay import schemas
from src.ibay.models import Product
from src.wallets.service import WalletService


class IBayService:
    def __init__(self, session_factory: AsyncSession, bunny_storage: BunnyStorage):
        self.session_factory = session_factory
        self.bunny_storage = bunny_storage

    # Отримання всіх замовлення
    async def get_products(self):
        async with self.session_factory() as db:
            result = await db.execute(select(Product))
            return result.scalars().all()

    # Отримання замовлення по id
    async def get_product_by_id(self, order_id: int):
        async with self.session_factory() as db:
            query = (
                select(Product)
                .options(joinedload(Product.wallet))
                .where(Product.id == order_id)
            )
            result = await db.execute(query)
            product = result.scalar_one_or_none()
            return product

    # Створення замовлення
    async def create_product(self, item: schemas.ProductCreate):
        async with self.session_factory() as db:
            product = Product(name=item.name, price=item.price,
                              image=await self.bunny_storage.upload_image_to_bunny(item.image),
                              wallet_id=item.wallet_id)
            db.add(product)
            await db.commit()
            await db.refresh(product)
            return product


