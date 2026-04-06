from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.api.routes_auth import router as auth_router
from app.api.routes_chat import router as chat_router
from app.db.session import engine
from app.db.base import Base

async def lifespan(app: FastAPI):
    
    """Управление жизненным циклом приложения"""
    
    # Создание таблиц
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield

    # Закрытие соединений
    await engine.dispose()


def create_app() -> FastAPI:
    app = FastAPI(
        title="llm-p",
        lifespan=lifespan,
    )

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

    # Технический endpoint GET /health
    @app.get("/health", tags=["technical"])
    def health():
        return {"status": "ok"}

    return app

app = create_app()