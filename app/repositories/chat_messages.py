from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from app.db.models import ChatMessage

class ChatMessageRepository:
   
    """
    Репозиторий для работы с сообщениями чата
    """

    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, user_id: int, role: str, content: str) -> ChatMessage:

        """
        Добавить сообщение в БД
        """

        message = ChatMessage(
            user_id=user_id,
            role=role,
            content=content
        )
        self._session.add(message)
        await self._session.commit()
        await self._session.refresh(message, ["id", "role", "content", "created_at"])
        return message

    async def get_last_n_by_user(self, user_id: int, n: int) -> list[ChatMessage]:

        """
        Получить последние N сообщений пользователя
        """

        result = await self._session.execute(
            select(ChatMessage)
            .where(ChatMessage.user_id == user_id)
            .order_by(ChatMessage.created_at.asc())
            .limit(n)
            .options(selectinload(ChatMessage.user))
        )
        return result.scalars().all()

    async def delete_user_history(self, user_id: int) -> None:
        
        """
        Удалить всю историю сообщений пользователя
        """
        
        await self._session.execute(
            delete(ChatMessage)
            .where(ChatMessage.user_id == user_id)
        )
        await self._session.commit()