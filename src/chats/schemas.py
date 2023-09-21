from pydantic import BaseModel


class Messages(BaseModel):
    id: int
    content: str
    user_id: int

class MessageSend(BaseModel):
    content: str = None
    photo: str = None

