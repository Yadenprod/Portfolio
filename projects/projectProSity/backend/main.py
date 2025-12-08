from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import json
import asyncio
from typing import List, Dict
import logging

from models.detection import TheftDetectionSystem
from models.database import DatabaseManager
from models.analytics import AnalyticsEngine
from utils.config import Settings

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация приложения
app = FastAPI(
    title="ProSity Security - Система детекции краж",
    description="AI система для предотвращения краж в торговых центрах",
    version="1.0.0"
)

# CORS настройки
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Инициализация компонентов
settings = Settings()
db_manager = DatabaseManager()
detection_system = TheftDetectionSystem()
analytics_engine = AnalyticsEngine()

# WebSocket соединения для real-time уведомлений
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                pass

manager = ConnectionManager()

@app.on_event("startup")
async def startup_event():
    """Инициализация при запуске"""
    logger.info("🚀 Запуск системы ProSity Security...")
    await db_manager.initialize()
    await detection_system.initialize()
    logger.info("✅ Система готова к работе")

@app.get("/")
async def root():
    """Главная страница API"""
    return {
        "message": "ProSity Security API",
        "version": "1.0.0",
        "status": "active",
        "features": [
            "Детекция подозрительного поведения",
            "Анализ движения к выходам",
            "Детекция вскрытия упаковок",
            "Real-time уведомления",
            "Аналитика и статистика"
        ]
    }

@app.get("/api/stats")
async def get_statistics():
    """Получение статистики краж"""
    try:
        stats = await analytics_engine.get_theft_statistics()
        return {
            "success": True,
            "data": stats
        }
    except Exception as e:
        logger.error(f"Ошибка получения статистики: {e}")
        raise HTTPException(status_code=500, detail="Ошибка получения статистики")

@app.get("/api/analytics/roi")
async def calculate_roi():
    """Расчет ROI системы"""
    try:
        roi_data = await analytics_engine.calculate_roi()
        return {
            "success": True,
            "data": roi_data
        }
    except Exception as e:
        logger.error(f"Ошибка расчета ROI: {e}")
        raise HTTPException(status_code=500, detail="Ошибка расчета ROI")

@app.get("/api/stores/priority")
async def get_priority_stores():
    """Получение приоритетных магазинов для мониторинга"""
    priority_stores = [
        {
            "id": 1,
            "name": "Магазин одежды",
            "category": "Одежда",
            "theft_risk": "Высокий",
            "common_items": ["Джинсы", "Футболки", "Куртки"],
            "recommended_cameras": 4
        },
        {
            "id": 2,
            "name": "Магазин электроники",
            "category": "Электроника",
            "theft_risk": "Очень высокий",
            "common_items": ["Смартфоны", "Наушники", "Планшеты"],
            "recommended_cameras": 6
        },
        {
            "id": 3,
            "name": "Магазин косметики",
            "category": "Косметика",
            "theft_risk": "Средний",
            "common_items": ["Парфюм", "Крема", "Декоративная косметика"],
            "recommended_cameras": 3
        }
    ]
    
    return {
        "success": True,
        "data": priority_stores
    }

@app.websocket("/ws/security")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket для real-time уведомлений"""
    await manager.connect(websocket)
    try:
        while True:
            # Ожидание сообщений от клиента
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Обработка команд
            if message.get("type") == "start_detection":
                await detection_system.start_monitoring()
                await websocket.send_text(json.dumps({
                    "type": "status",
                    "message": "Детекция запущена"
                }))
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.post("/api/detection/start")
async def start_detection():
    """Запуск системы детекции"""
    try:
        await detection_system.start_monitoring()
        return {"success": True, "message": "Система детекции запущена"}
    except Exception as e:
        logger.error(f"Ошибка запуска детекции: {e}")
        raise HTTPException(status_code=500, detail="Ошибка запуска детекции")

@app.post("/api/detection/stop")
async def stop_detection():
    """Остановка системы детекции"""
    try:
        await detection_system.stop_monitoring()
        return {"success": True, "message": "Система детекции остановлена"}
    except Exception as e:
        logger.error(f"Ошибка остановки детекции: {e}")
        raise HTTPException(status_code=500, detail="Ошибка остановки детекции")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
