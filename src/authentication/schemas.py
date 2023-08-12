from pydantic import BaseModel

class Token(BaseModel):
    """Схема для токена"""
    access_token: str
    token_type: str

    class Config:
        from_attributes = True


class TokenPayload(BaseModel):
    """Схема для токена юзера"""
    user_id: int

    class Config:
        from_attributes = True
