from typing import AsyncGenerator
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.errors import UnauthorizedError
from app.core.security import decode_access_token
from app.db.session import get_async_session
from app.repositories.users import UserRepository
from app.repositories.chat_messages import ChatMessageRepository
from app.usecases.auth import AuthUseCase
from app.usecases.chat import ChatUseCase
from app.services.openrouter_client import OpenRouterClient


# OAuth2 схема для Swagger
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
    auto_error=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Зависимость для получения сессии базы данных."""
    async for session in get_async_session():
        yield session


async def get_user_repository(
    db: AsyncSession = Depends(get_db),
) -> UserRepository:
    """Зависимость для получения репозитория пользователей."""
    return UserRepository(db)


async def get_chat_message_repository(
    db: AsyncSession = Depends(get_db),
) -> ChatMessageRepository:
    """Зависимость для получения репозитория сообщений чата."""
    return ChatMessageRepository(db)


async def get_openrouter_client() -> OpenRouterClient:
    """Зависимость для получения клиента OpenRouter."""
    return OpenRouterClient()


async def get_auth_usecase(
    user_repo: UserRepository = Depends(get_user_repository),
) -> AuthUseCase:
    """Зависимость для получения usecase аутентификации."""
    return AuthUseCase(user_repo)


async def get_chat_usecase(
    message_repo: ChatMessageRepository = Depends(get_chat_message_repository),
    openrouter_client: OpenRouterClient = Depends(get_openrouter_client),
) -> ChatUseCase:
    """Зависимость для получения usecase чата."""
    return ChatUseCase(message_repo, openrouter_client)


async def get_current_user_id(
    token: str | None = Security(oauth2_scheme),
) -> int:
    """
    Зависимость для получения ID текущего пользователя из JWT токена.

    Если токен не предоставлен или невалиден, выбрасывает HTTP 401.
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user id",
            )

        return int(user_id)

    except UnauthorizedError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e.message),
        )
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: invalid user id format",
        )