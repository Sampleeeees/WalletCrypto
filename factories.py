import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from config_fastapi import settings
from src.chats.models import Message
from src.users.models import User
from src.users.security import get_password_hash
from src.wallets.models import Asset, Blockchain, Wallet


async def create_user(db: AsyncSession) -> None:
    db_user = User(
        username=settings.TEST_USER_USERNAME,
        email=settings.TEST_USER_EMAIL,
        password=get_password_hash(settings.TEST_USER_PASSWORD),
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

async def create_admin(db: AsyncSession) -> None:
    db_user = User(
        username=settings.TEST_ADMIN_USERNAME,
        email=settings.TEST_ADMIN_EMAIL,
        password=get_password_hash(settings.TEST_ADMIN_PASSWORD),
        is_superuser=True
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)


async def create_message(db: AsyncSession) -> None:
    message_data = Message(content="Test message",
                           date_send=datetime.datetime.strptime("2023-09-16T13:53:57.004610", "%Y-%m-%dT%H:%M:%S.%f"),
                           image="https://cryptowallet.b-cdn.net/basic.jpg",
                           user_id=1)

    db.add(message_data)
    await db.commit()
    await db.refresh(message_data)

async def create_blockchain(db: AsyncSession) -> None:
    blockchain_data = Blockchain(name="Ethereum", short_name="eth", image=None)
    db.add(blockchain_data)
    await db.commit()
    await db.refresh(blockchain_data)

async def create_asset(db: AsyncSession):
    asset_data = Asset(name="ETH", decimal_places=18, blockchain_id=1)
    db.add(asset_data)
    await db.commit()
    await db.refresh(asset_data)

async def create_wallet(db: AsyncSession):
    wallet_data = Wallet(address="0xF0265774D447A2329776EAf6a1A362D76ea17d34",
                         balance=0,
                         private_key="0x776425569c8ac09f4ec71c7dc554de38b1cbb1b9308f326deb4f71ae986b070f",
                         user_id=1,
                         asset_id=1)
    db.add(wallet_data)
    await db.commit()
    await db.refresh(wallet_data)

