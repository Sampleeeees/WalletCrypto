import datetime

from pydantic import BaseModel


class OrderCreate(BaseModel):
    """Схема для створення замовлення"""
    product_id: int
    transaction_id: int