from typing import List

from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.sql import func
from sqlalchemy_utils import EmailType, URLType
from src.wallets.models import Wallet


from config.database import Base

class User(Base):
    """User model"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(EmailType, unique=True, index=True)
    username = Column(String(length=100))
    password = Column(String(length=250))
    access_token = Column(String())
    avatar = Column(URLType)
    created_on = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    wallets = relationship('Wallet', back_populates='user')

    #messages: Mapped[List["Message"]] = relationship(back_populates="user")

    def __repr__(self):
        return f"User(id={self.id}, " \
               f"email={self.email}, " \
               f"username={self.username}, " \
               f"is_active={self.is_active}"
