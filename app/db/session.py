from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.core.config import settings


# Создаём строку подключения к SQLite
database_url = f"sqlite+aiosqlite:///{settings.sqlite_path}"

# Асинхронный engine
engine = create_async_engine(
    database_url,
    # echo=True
)

# Фабрика асинхронных сессий
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Зависимость для FastAPI: получает новую асинхронную сессию.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()