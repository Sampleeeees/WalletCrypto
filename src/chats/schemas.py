from typing import Any, Union

from pydantic import BaseModel


class Message(BaseModel):
    id: int
    content: Union[str, None]
    image: Any
    date_send: Any
    user_id: int

    class Config:
        schema_extra = {
            "examples": [
                {
                    "id": 0,
                    "content": "test message",
                    "image": "http://example.com/basic.jpg",
                    "date_send": "2023-09-20T16:23:05.921678",
                    "user_id": 0
                }
            ]
        }

class MessageSend(BaseModel):
    content: str = None
    photo: str = None

class DeleteMessage(BaseModel):
    detail: str

    class Config:
        schema_extra = {
            "examples": [
                {
                    "detail": "Повідомлення видалено"
                }
            ]
        }

