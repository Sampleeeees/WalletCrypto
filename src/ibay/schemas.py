from typing import Union

from pydantic import BaseModel, validator

from src.authentication.exceptions import BadRequestException


class BuyProduct(BaseModel):
    product_id: int
    wallet_id: int

class ProductCreate(BaseModel):
    """Схема для створення продукту"""
    name: str
    price: Union[int, float]
    image: str
    wallet_id: int

    @validator('image')
    def validate_image64(cls, value):
        if not value.startswith('data'):
            raise BadRequestException(detail='Введіть фото в base64 форматі')
        return value

    @validator('name')
    def validate_name(cls, value):
        if value is None:
            raise BadRequestException(detail='Назва продукту не може бути пустою')
        return value

    @validator('price')
    def validate_price(cls, value):
        if value <= 0:
            raise BadRequestException(detail="Ціна не може бути 0 чи від'ємним числом")
        return value
