import jwt
from datetime import datetime, timedelta

from config_fastapi import settings

ALGORITHM = "HS256"
access_token_jwt_subject = "access"

# Створення токену
def create_token(user_id: int) -> dict:
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access": create_access_token(
            data={"user_id": user_id}, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }

# Генерація access token та часу його дії
def create_access_token(*, data: dict, expires_delta: timedelta = None) -> str:
    """Створення токену"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire, "sub": access_token_jwt_subject})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt