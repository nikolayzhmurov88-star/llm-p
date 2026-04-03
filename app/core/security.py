from datetime import datetime, timedelta, timezone
from typing import Annotated, Any

from fastapi import Depends, HTTPException, Security, status
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings
from app.core.errors import UnauthorizedError

# Хеширование паролей через passlib

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(plain_password: str) -> str:
    
    """
    Функция хеширования пароля
    """
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
   
    """
    Проверяет, соответствует ли plain_password bcrypt-хешу hashed_password.
    """

    return pwd_context.verify(plain_password, hashed_password)


# JWT‑токены


def create_access_token(
    *,
    sub: str,
    role: str,
    expires_minutes: int,) -> str:
    
    """
    Функция генерирует JWT access token.
    sub: идентификатор пользователя.
    role: роль пользователя.
    expires_minutes: время жизни токена в минутах.

    """
        
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    now = datetime.now(timezone.utc)

    payload = {
        "sub": sub,
        "role": role,
        "exp": expire,
        "iat": now,
    }

    return jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=settings.jwt_alg,
    )



def decode_access_token(token: str) -> dict[str, Any]:

    """
    Функция декодирует JWT access token
    и возвращает Payload
    
    """   

    try:
        # декодируем и проверяем подпись
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_alg],
        )

        # извлекаем обязательные поля
        sub = payload.get("sub")
        role = payload.get("role")
        exp = payload.get("exp")
        iat = payload.get("iat")

        # Обработка ошибок
        if not sub or not role or exp is None or iat is None:
            raise UnauthorizedError("Invalid token format")

        return payload 

    except JWTError:
        # Обработка ошибок
        raise UnauthorizedError("Invalid token")