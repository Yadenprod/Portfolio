"""
Главный файл приложения NeiroComment
"""
import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import settings
from app.database.connection import init_db
from app.telegram.monitor import start_monitoring
from app.web.routes import router as web_router
from app.monitoring.logger import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управление жизненным циклом приложения"""
    # Startup
    setup_logging()
    await init_db()
    
    # Запуск мониторинга каналов в фоновом режиме
    asyncio.create_task(start_monitoring())
    
    yield
    
    # Shutdown
    logging.info("Приложение завершает работу")


# Создание FastAPI приложения
app = FastAPI(
    title="NeiroComment",
    description="Система нейрокомейтинга для Telegram",
    version="1.0.0",
    lifespan=lifespan
)

# Подключение маршрутов
app.include_router(web_router, prefix="/api/v1")

# Статические файлы и шаблоны
app.mount("/static", StaticFiles(directory="app/web/static"), name="static")
templates = Jinja2Templates(directory="app/web/templates")


@app.get("/")
async def root():
    """Главная страница"""
    return {"message": "NeiroComment API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    """Проверка здоровья системы"""
    return {"status": "healthy", "version": "1.0.0"}


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
