from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str
    env: str

    jwt_secret: str
    jwt_alg: str
    access_token_expire_minutes: int

    sqlite_path: str

    openrouter_api_key: str
    openrouter_base_url: str
    openrouter_model: str
    openrouter_site_url: str
    openrouter_app_name: str

    # Дополнительные настройки
    chat_history_limit: int = 10
    chat_system_prompt: str = "Отвечай кратко на русском языке."
    openrouter_temperature: float = 0.7


    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()