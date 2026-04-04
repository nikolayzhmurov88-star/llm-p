from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.db.models import User


class UserRepository:
   
    """
    Репозиторий для работы с пользователями
    """

    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_email(self, email: str) -> User | None:
        
        """
        Получить пользователя по email
        """

        result = await self._session.execute(
            select(User)
            .where(User.email == email)
            .options(selectinload(User.messages))
        )
        return result.scalar_one_or_none()


    async def get_by_id(self, user_id: int) -> User | None:

        """
        Получить пользователя по ID
        """

        result = await self._session.execute(
            select(User)
            .where(User.id == user_id)
            .options(selectinload(User.messages))
        )
        return result.scalar_one_or_none()

    async def create(self, user: User) -> User:

        """
        Создать пользователя в БД
        """

        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user, ["id", "email", "role", "created_at"])
        return user