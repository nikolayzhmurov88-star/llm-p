from datetime import datetime, timezone
from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from app.db.base import Base


class User(Base):
    
    """
    Модель пользователя
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    password_hash: Mapped[str] = mapped_column()
    role: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))

    # Связь
    messages: Mapped[List["ChatMessage"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )


class ChatMessage(Base):
    
    """
    Модель сообщения чата
    """

    __tablename__ = "chat_messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    role: Mapped[str] = mapped_column()
    content: Mapped[str] = mapped_column()
    from datetime import datetime, timezone
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc)
)

    # Связь
    user: Mapped["User"] = relationship(back_populates="messages")