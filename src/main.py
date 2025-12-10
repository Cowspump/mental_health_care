"""
FastAPI application entry point.
Configures the app with all routers, middleware, and settings.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.v1 import (
    ai_assistant,
    assessments,
    first_aid,
    journaling,
    monitoring,
)
from src.config import settings

# Создаём FastAPI приложение
app = FastAPI(
    title=settings.project_name,
    description="Mental Health Care Platform API for tracking mental state, journaling, and assessments",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# CORS middleware для frontend интеграции
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В production указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры API v1
app.include_router(journaling.router, prefix=settings.api_v1_str)
app.include_router(assessments.router, prefix=settings.api_v1_str)
app.include_router(ai_assistant.router, prefix=settings.api_v1_str)
app.include_router(first_aid.router, prefix=settings.api_v1_str)
app.include_router(monitoring.router, prefix=settings.api_v1_str)


@app.get("/")
async def root():
    """Root endpoint with basic API information."""
    return {
        "message": "Mental Health Care Platform API",
        "version": "1.0.0",
        "docs_url": "/docs",
        "health_check": "/health"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy", "service": "mental-health-platform"}


# Event handlers для инициализации и очистки
@app.on_event("startup")
async def startup_event():
    """Выполняется при запуске приложения."""
    # TODO: Создать таблицы БД, если нужно
    # TODO: Инициализировать внешние сервисы
    print("🚀 Mental Health Platform API started successfully")


@app.on_event("shutdown")
async def shutdown_event():
    """Выполняется при остановке приложения."""
    # TODO: Закрыть соединения с БД и внешними сервисами
    print("👋 Mental Health Platform API shutting down")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,  # Автоперезагрузка в debug режиме
        log_level="info"
    )