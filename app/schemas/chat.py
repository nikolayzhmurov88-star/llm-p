from pydantic import BaseModel, Field


class ChatRequest(BaseModel):

    """
    Схема запроса к чату
    """

    prompt: str = Field(
        description="Основной текст запроса пользователя"
    )
    system: str = Field(
        default="", 
        description="Системная инструкция для модели"
    )
    max_history: int = Field(
        default=10, 
        ge=0,
        description="Сколько сообщений из истории брать для контекста"
    )
    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
        description="Параметр температуры для управления креативностью модели"
    )


class ChatResponse(BaseModel):

    """
    Схема ответа чата
    """

    answer: str = Field(
        description="Ответ модели на запрос пользователя"
    )