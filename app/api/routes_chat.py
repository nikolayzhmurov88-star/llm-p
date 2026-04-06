from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.core.errors import ExternalServiceError
from app.schemas.chat import ChatRequest, ChatResponse
from app.schemas.user import UserPublic
from app.usecases.chat import ChatUseCase
from app.api.deps import get_chat_usecase, get_current_user_id
from app.db.models import ChatMessage


router = APIRouter(tags=["chat"])


@router.post(
    "/",
    response_model=ChatResponse,
    summary="Отправить сообщение LLM",
)
async def chat(
    request: ChatRequest,
    user_id: int = Depends(get_current_user_id),
    chat_usecase: ChatUseCase = Depends(get_chat_usecase),
) -> ChatResponse:
    """
    Отправляет запрос к LLM и возвращает ответ.

    - **prompt**: Текст запроса пользователя
    - **system**: Системная инструкция (опционально)
    - **max_history**: Количество сообщений из истории для контекста
    - **temperature**: Креативность модели (0.0 - 2.0)
    """
    try:

        chat_usecase.history_limit = request.max_history

        answer = await chat_usecase.ask(
            user_id=user_id,
            prompt=request.prompt,
            system=request.system,
        )
        return ChatResponse(answer=answer)
    except ExternalServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"LLM service error: {str(e.message)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal error: {str(e)}",
        )


@router.get(
    "/history",
    response_model=List[UserPublic],
    summary="Получить историю сообщений",
)
async def get_history(
    user_id: int = Depends(get_current_user_id),
    chat_usecase: ChatUseCase = Depends(get_chat_usecase),
    limit: int = 50,
) -> List[ChatMessage]:
    """
    Возвращает историю сообщений текущего пользователя.
    """
    history = await chat_usecase.message_repo.get_last_n_by_user(user_id, limit)
    
    return list(reversed(history))


@router.delete(
    "/history",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Очистить историю сообщений",
)
async def clear_history(
    user_id: int = Depends(get_current_user_id),
    chat_usecase: ChatUseCase = Depends(get_chat_usecase),
) -> None:
    """
    Удаляет всю историю сообщений текущего пользователя.
    """
    await chat_usecase.message_repo.delete_user_history(user_id)