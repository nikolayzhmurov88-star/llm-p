from fastapi import FastAPI  # импортируем fast_api
from starlette.middleware.cors import CORSMiddleware # импортируем CORS

from app.api.routes_auth import router as auth_router # Импортируем роутеры
from app.api.routes_chat import router as chat_router # Импортируем роутеры
from app.db import engine, Base # Импортируем подключение к базовую модель


def create_app() -> FastAPI:
    app = FastAPI(title="llm-p")

    # Добавление CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Подключение роутеров
    app.include_router(auth_router, prefix="/auth", tags=["auth"])
    app.include_router(chat_router, prefix="/chat", tags=["chat"])

    # Создание таблиц при старте
    @app.on_event("startup")
    def startup():
        with engine.connect() as conn:
            Base.metadata.create_all(bind=conn)

    # !!!! Технический endpoint GET /health (вернуть окружение)
    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app


app = create_app()