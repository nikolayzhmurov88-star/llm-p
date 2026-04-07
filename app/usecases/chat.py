from typing import List, Dict
from app.repositories.chat_messages import ChatMessageRepository
from app.services.openrouter_client import OpenRouterClient

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
    
    async def ask(self, user_id: int, prompt: str, system: str, max_history: int, temperature: float) -> str:
        
        messages = await self._build_context(user_id, prompt, system, max_history)
        
        await self.message_repo.create(user_id, "user", prompt)
    
        response = await self.openrouter_client.chat_completion(messages, temperature)
        
        assistant_content = response["choices"][0]["message"]["content"]
    
        await self.message_repo.create(user_id, "assistant", assistant_content)
        
        return assistant_content
    
    async def _build_context(
        self, 
        user_id: int, 
        prompt: str, 
        system: str,
        max_history: int
    ) -> List[Dict[str, str]]:
        
        """
        Формирует messages: system + история + текущий prompt
        """

        messages: List[Dict[str, str]] = []
        
        # System-сообщение при наличии
        if system.strip():
            messages.append({"role": "system", "content": system})
        
        # История пользователя из репозитория
        history = await self.message_repo.get_last_n_by_user(
            user_id, 
            max_history
        )
        messages.extend([
            {"role": msg.role, "content": msg.content}
            for msg in history
        ])
        
        # Текущий prompt как user-сообщение
        messages.append({"role": "user", "content": prompt})
        
        return messages