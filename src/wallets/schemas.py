from typing import Union, Any
from pydantic import BaseModel, field_validator


class WalletBase(BaseModel):
    """Базова схема гаманця"""
    id: int
    address: str
    balance: Union[int, float, Any]

    class Config:
        from_attributes = True


class WalletList(WalletBase):
    """Схема для отримання всіх гаманців на сервері"""
    private_key: str

    @field_validator("private_key")
    def mask_private_key(cls, value):
        return value[:10] + ("*" * (len(value) - 10))


class CheckBalance(BaseModel):
    """Схема для введеня адреси гаманця"""
    address: str

class Wallet(WalletBase):
    """Схема для відображення ключа та користувача"""
    private_key: str
    user_id: int

    @field_validator("private_key")
    def mask_private_key(cls, value):
        return value[:10] + ("*" * (len(value) - 10))


class WalletCreate(BaseModel):
    """Схема для стоврення гаманця"""
    user: int

class WalletImport(BaseModel):
    """Схема для імпорту гаманця по ключу"""
    private_key: str


class TransactionCreate(BaseModel):
    """Схема для створення транзакції"""
    from_send: str
    to_send: str
    value: Union[int, float]
    private_key: str


class TransactionInfo(BaseModel):
    """Схема для відображення інформації транзакції"""
    blockHash: str
    blockNumber: int
    transactionHash: str
    blockNumber: int
    from_send: str
    to: str
    status: int
    type: int




    
