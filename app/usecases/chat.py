from typing import List, Dict
from app.core.config import settings
from app.repositories.chat_messages import ChatMessageRepository
from app.services.openrouter_client import OpenRouterClient
from app.db.models import ChatMessage 

class ChatUseCase:
    """Бизнес-логика общения с LLM"""
    
    def __init__(
        self, 
        message_repo: ChatMessageRepository,
        openrouter_client: OpenRouterClient
    ):
        """
        Инициализация с репозиторием и OpenRouter клиентом

        """
        self.message_repo = message_repo
        self.openrouter_client = openrouter_client
        self.history_limit = settings.chat_history_limit 
    
    async def ask(self, user_id: int, prompt: str, system: str = "") -> str:
        
        messages = await self._build_context(user_id, prompt, system)
    
   
        await self.message_repo.create(user_id, "user", prompt)
    
        response = await self.openrouter_client.chat_completion(messages)
        
        assistant_content = response["choices"][0]["message"]["content"]
    
   
        await self.message_repo.create(user_id, "assistant", assistant_content)
        return assistant_content
    
    async def _build_context(
        self, 
        user_id: int, 
        prompt: str, 
        system: str
    ) -> List[Dict[str, str]]:
        
        """
        Формирует messages: system + история + текущий prompt
        """

        messages: List[Dict[str, str]] = []
        
        # System-сообщение при наличии
        if system.strip():
            messages.append({"role": "system", "content": system})
        elif settings.chat_system_prompt.strip(): 
            messages.append({"role": "system", "content": settings.chat_system_prompt})
        
        # История пользователя из репозитория
        history = await self.message_repo.get_last_n_by_user(
            user_id, 
            self.history_limit 
        )
        messages.extend([
            {"role": msg.role, "content": msg.content}
            for msg in history
        ])
        
        # Текущий prompt как user-сообщение
        messages.append({"role": "user", "content": prompt})
        
        return messages