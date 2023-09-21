from typing import Union, Any

from pydantic import BaseModel, validator

from src.authentication.exceptions import BadRequestException
from src.wallets.schemas import ListTransaction


class BuyProduct(BaseModel):
    product_id: int
    wallet_id: int

    class Config:
        schema_extra = {
            "examples": [
                {
                    "product_id": 0,
                    "wallet_id": 0
                }
            ]
        }

class BuyProductResponse(BaseModel):
    id: int
    hash: str

    class Config:
        schema_extra = {
            "examples": [
                {
                    "id": 0,
                    "hash": "0vhgiupof8754jui3ui435433634hio435io4"
                }
            ]
        }

class WalletBase(BaseModel):
    id: int
    address: str
    balance: Union[float, int]
    private_key: str
    asset_id: int
    user_id: int

class ProductList(BaseModel):
    id: int
    name: str
    price: Union[float, int]
    image: Any
    wallet_id: int
    wallet: WalletBase

    class Config:
        schema_extra = {
            "examples": [
                {
                    "id": 0,
                    "name": "name_product",
                    "price": 0.1,
                    "image": "data/base64....",
                    "wallet_id": 0,
                    "wallet": {
                        "id": 0,
                        "address": "your_address",
                        "balance": 0.002,
                        "private_key": "private_key_for_your_address",
                        "asset_id": 0,
                        "user_id": 0,
                    }
                }
            ]
        }



class ProductOrdered(BaseModel):
    id: int
    status: Any
    turning: Union[str, None]
    date_send: Any
    product_id: int
    transaction_id: int
    transaction: ListTransaction

    class Config:
        schema_extra = {
            "examples": [
                {
                    "id": 0,
                    "status": "New, Delivery, Failed, Turning or Finish",
                    "turning": "0xg5f4g6dfgdfg4dfg56df456g6dfg4dsjfj",
                    "date_send": "2022-15-32",
                    "product_id": 0,
                    "transaction_id": 0,
                    "transaction": {
                        "id": 0,
                        "hash": "0x99af5ad073070acf6c3cb446aee024090feaae11fd4a3c74131e800661afcb6e",
                        "from_send": "0x07f4ac16AaAd7B561F0f9C1dE1CAC3A18f2c61d9",
                        "to_send": "0x07f4ac16AaAd7B561F0f9C1dE1CACAA68f2c61d9",
                        "value": 0.005,
                        "txn_fee": 0.000000005,
                        "date_send": "2023-08-14T09:08:48",
                        "status": "Success or Failed"
                    }
                }
            ]
        }


class ProductCreate(BaseModel):
    """Схема для створення продукту"""
    name: str
    price: Union[int, float]
    image: str
    wallet_id: int

    class Config:
        schema_extra = {
            "examples": [
                {
                    "name": "Product 1",
                    "price": 0.1,
                    "image": "data/base64....",
                    "wallet_id": 0
                }
            ]
        }

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
