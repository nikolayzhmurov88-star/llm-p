import httpx  
#import json
from typing import List, Dict, Any
from app.core.config import settings
from app.core.errors import ExternalServiceError


class OpenRouterClient:


    """
    Клиент для работы с OpenRouter API через HTTP-запросы
    """

    def __init__(self):
        self.base_url = settings.openrouter_base_url
        self.headers = {
            "Authorization": f"Bearer {settings.openrouter_api_key}",
            "HTTP-Referer": settings.openrouter_site_url,
            "X-Title": settings.openrouter_app_name,
            "Content-Type": "application/json",
        }

    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float
    ) -> Dict[str, Any]:
        
        """
        Отправляет запрос на генерацию ответа к OpenRouter
        """

        payload = {
            "model": settings.openrouter_model,
            "messages": messages,
            "temperature": temperature
        }

        '''
        Для логирования PayLoad
        print("\n" + "═"*100)
        print("Payload")
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        print("═"*100 + "\n")
        '''
    

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
            )

        if response.status_code != 200:
            raise ExternalServiceError(
                f"OpenRouter API error {response.status_code}: {response.text}"
            )

        return response.json()