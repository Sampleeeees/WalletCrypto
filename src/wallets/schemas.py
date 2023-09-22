from typing import Union, Any
from pydantic import BaseModel, validator


class WalletBase(BaseModel):
    """Базова схема гаманця"""
    id: int
    address: str
    balance: Union[float, int]

    class Config:
        from_attributes = True


class WalletList(WalletBase):
    """Схема для отримання всіх гаманців на сервері"""
    private_key: str

    @validator("private_key")
    def mask_private_key(cls, value):
        return value[:10] + ("*" * (len(value) - 10))

    class Config:
        schema_extra = {
            "examples": [
                {
                    "id": 0,
                    "address": "0x07f4ac16AaAd7B561F0f9C1dE1CACAA18f2c61d9",
                    "balance": 0.02,
                    "private_Key": "0x101c54e8********************************************************"
                }
            ]
        }


class WalletEtherscan(BaseModel):
    """Схема для виводу адреси з etherscan"""
    url: str

    class Config:
        schema_extra = {
            "examples": [
                {
                    "url": "https://etherscan.io/address/{address}"
                }
            ]
        }


class CheckBalance(BaseModel):
    """Схема для введеня адреси гаманця"""
    address: str

    class Config:
        schema_extra = {
            "examples": [
                {
                    "address": "0xaeCD391A5f45F9dcF059f815B0517Da82993C9eB"
                }
            ]
        }

class Wallet(WalletBase):
    """Схема для відображення ключа та користувача"""
    private_key: str
    user_id: int

    class Config:
        schema_extra = {
            "examples": [
                {
                    "id": 0,
                    "address": "0xaeCD391A5f45F9dcF089f845B0547Da82991C9eB",
                    "balance": 0.001,
                    "private_key": "892349d31a******************************************************",
                    "user_id": 0
                }
            ]
        }

    @validator("private_key")
    def mask_private_key(cls, value):
        return value[:10] + ("*" * (len(value) - 10))



class WalletCreate(BaseModel):
    """Схема для стоврення гаманця"""
    id: int
    address: str
    balance: Union[float, int]
    private_key: str
    user_id: int
    asset_id: int

    class Config:
        schema_extra = {
            "examples": [
                {
                    "id": 0,
                    "address": "0x07f4ac16AaAd7B561F0f9C1dE1CACAA18f2c61d9",
                    "balance": 0.005,
                    "private_key": "0x101c54e8********************************************************",
                    "user_id": 0,
                    "asset_id": 0
                }
            ]
        }


class WalletImport(BaseModel):
    """Схема для імпорту гаманця по ключу"""
    private_key: str


class TransactionCreate(BaseModel):
    """Схема для створення транзакції"""
    from_send: str
    to_send: str
    value: Union[float, int]
    private_key: str

    class Config:
        schema_extra = {
            "examples": [
                {
                    "from_send": "0x6d35801Ab7552631334564b16b7721F64E79ebac",
                    "to_send": "0x6d35801Ab7342631985564b16b7721F64E79ebac",
                    "value": 0.0001,
                    "private_key": "0x101c54e8********************************************************"
                }
            ]
        }


class ListTransaction(BaseModel):
    """Схема для відображення інформації транзакції"""
    id: int
    hash: str
    from_send: str
    to_send: str
    value: Union[float, int]
    txn_fee: Union[float, int, None]
    date_send: Any
    status: Any

    class Config:
        schema_extra = {
            "examples": [
                {
                    "id": 0,
                    "hash": "0x99af5ad073070acf6c3cb446aee024090feaae11fd4a3c74131e800661afcb6e",
                    "from_send": "0x07f4ac16AaAd7B561F0f9C1dE1CAC3A18f2c61d9",
                    "to_send": "0x07f4ac16AaAd7B561F0f9C1dE1CACAA68f2c61d9",
                    "value": 0.005,
                    "txn_fee": 0.000000005,
                    "date_send": "2023-08-14T09:08:48",
                    "status": "Success or Failed"
                }
            ]
        }




    
