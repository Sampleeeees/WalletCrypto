import enum
from typing import List

from sqlalchemy import Integer, String, Column, Numeric, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy_utils import URLType

from ..ibay.models import Product
from ..delivery.models import Order


from config.database import Base

class TransactionStatus(enum.Enum):
    """Enum for transaction status"""
    pending = 'Pending'
    failed = 'Failed'
    success = 'Success'

class Blockchain(Base):
    """Blockchain model"""
    # name table
    __tablename__ = 'blockchain'

    # table fields
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=50))
    short_name = Column(String(length=10))
    image = Column(URLType)


    #asset: Mapped['Asset'] = relationship(back_populates='blockchains')

class Asset(Base):
    """Asset model"""
    # name table
    __tablename__ = 'asset'

    # table fields
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=50))
    decimal_places = Column(Integer)
    blockchain_id = Column(Integer, ForeignKey('blockchain.id'))


    wallets = relationship('Wallet', back_populates='asset')

class Wallet(Base):
    """Wallet model"""
    # name table
    __tablename__ = 'wallets'

    # table fields
    id = Column(Integer, primary_key=True, autoincrement=True)
    address = Column(String)
    balance = Column(Numeric, default=0)
    private_key = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    asset_id = Column(Integer, ForeignKey('asset.id'))

    products = relationship('Product', back_populates='wallet')
    user = relationship('User', back_populates='wallets')
    asset = relationship('Asset', back_populates='wallets')


class Transaction(Base):
    """Transaction Model"""
    # name table
    __tablename__ = 'transaction'

    # table fields
    id = Column(Integer, primary_key=True, autoincrement=True)
    hash = Column(String(length=250))
    from_send = Column(String(length=250))
    to_send = Column(String(length=250))
    value = Column(Numeric)
    date_send = Column(DateTime)
    txn_fee = Column(Numeric)
    status = Column(Enum(TransactionStatus))

    orders = relationship("Order", back_populates='transaction')
