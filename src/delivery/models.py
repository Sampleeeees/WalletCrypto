import enum
from sqlalchemy import Column, Integer, DateTime, Enum, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from config.database import Base

class StatusOrder(enum.Enum):
    new = 'New'
    delivery = 'Delivery'
    finish = 'Finish'
    turning = 'Turning'
    failed = 'Failed'

class Order(Base):
    """Order model"""

    __tablename__ = 'order'

    id = Column(Integer, primary_key=True, autoincrement=True)
    date_send = Column(DateTime)
    status = Column(Enum(StatusOrder))
    turning = Column(String(length=350))
    product_id = Column(Integer, ForeignKey('product.id'))
    transaction_id = Column(Integer, ForeignKey('transaction.id'))

    #product: Mapped["Product"] = relationship(back_populates="orders")
    transaction = relationship('Transaction', back_populates="orders")


