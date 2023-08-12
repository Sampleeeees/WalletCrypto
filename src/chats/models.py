from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy_utils import URLType

from config.database import Base

class Message(Base):
    """Message model"""

    __tablename__ = 'message'

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String(length=1000))
    date_send = Column(DateTime)
    image = Column(URLType)
    user_id = Column(Integer, ForeignKey('users.id'))

    #user: Mapped["User"] = relationship(back_populates="messages")