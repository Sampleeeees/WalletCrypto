from typing import List

from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import URLType
from config.database import Base



class Product(Base):
    """Product model"""

    __tablename__ = 'product'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=70))
    price = Column(Integer, default=0)
    image = Column(URLType)
    wallet_id = Column(Integer, ForeignKey('wallets.id'))

    wallet = relationship('Wallet', back_populates='products')
    #orders: Mapped[List["Order"]] = relationship(back_populates="product")
