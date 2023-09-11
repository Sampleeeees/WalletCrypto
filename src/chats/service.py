import datetime

from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from src.chats.models import Message


class ChatService:
    def __init__(self, session_factory: AsyncSession):
        self.session_factory = session_factory

    async def save_message(self, content: str, user_id: int, image):
        async with self.session_factory() as db:
            message = Message(content=content, image=image, user_id=user_id, date_send=datetime.datetime.now())
            db.add(message)
            await db.commit()
            await db.refresh(message)

    async def get_messages(self):
        async with self.session_factory() as db:
            results = await db.execute(select(Message).order_by(desc(Message.id)).limit(10))
            return results.scalars().all()