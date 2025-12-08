from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import asyncio
import logging
import uvicorn
from datetime import datetime
import uuid
from enum import Enum
import json
from contextlib import asynccontextmanager

from gibdd_checker import GIBDDChecker, CheckType, CheckResult

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Модели данных
class CheckTypeEnum(str, Enum):
    registration = "registration"
    accidents = "accidents" 
    wanted = "wanted"
    restrictions = "restrictions"

class VehicleCheckRequest(BaseModel):
    vin: str = Field(..., min_length=17, max_length=17, description="VIN номер автомобиля (17 символов)")
    check_types: Optional[List[CheckTypeEnum]] = Field(
        default=[CheckTypeEnum.registration, CheckTypeEnum.accidents],
        description="Типы проверок для выполнения"
    )
    callback_url: Optional[str] = Field(None, description="URL для отправки результатов (опционально)")

class VehicleCheckResponse(BaseModel):
    request_id: str = Field(..., description="Уникальный ID запроса")
    vin: str = Field(..., description="VIN номер")
    status: str = Field(..., description="Статус обработки")
    message: str = Field(..., description="Сообщение о статусе")
    estimated_completion: Optional[str] = Field(None, description="Ожидаемое время завершения")

class CheckResultResponse(BaseModel):
    check_type: str
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    captcha_solved: bool = False
    ad_waited: bool = False
    timestamp: datetime

class VehicleCheckResults(BaseModel):
    request_id: str
    vin: str
    results: List[CheckResultResponse]
    total_checks: int
    successful_checks: int
    processing_time: float
    completed_at: datetime

# Глобальные переменные
active_requests: Dict[str, Dict] = {}
completed_requests: Dict[str, VehicleCheckResults] = {}

# Менеджер жизненного цикла приложения
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управление жизненным циклом приложения"""
    logger.info("🚀 Запуск ГИБДД API сервера...")
    yield
    logger.info("🛑 Остановка ГИБДД API сервера...")

# Создание приложения
app = FastAPI(
    title="ГИБДД Vehicle Checker API",
    description="API для автоматизированной проверки автомобилей через сайт ГИБДД с обходом CAPTCHA",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def convert_check_result(result: CheckResult) -> CheckResultResponse:
    """Конвертация результата проверки в модель ответа"""
    return CheckResultResponse(
        check_type=result.check_type.value,
        success=result.success,
        data=result.data,
        error=result.error,
        captcha_solved=result.captcha_solved,
        ad_waited=result.ad_waited,
        timestamp=datetime.now()
    )

async def process_vehicle_check(request_id: str, vin: str, check_types: List[CheckType]):
    """Фоновая обработка проверки автомобиля"""
    start_time = datetime.now()
    
    try:
        logger.info(f"🔍 Начало обработки запроса {request_id} для VIN: {vin}")
        
        # Обновляем статус
        active_requests[request_id]["status"] = "processing"
        active_requests[request_id]["started_at"] = start_time
        
        # Создаем чекер
        checker = GIBDDChecker(headless=True)
        
        try:
            await checker.initialize()
            
            # Выполняем проверки
            results = await checker.check_vehicle(vin, check_types)
            
            # Конвертируем результаты
            response_results = [convert_check_result(result) for result in results]
            
            # Подсчитываем статистику
            successful_checks = sum(1 for r in results if r.success)
            processing_time = (datetime.now() - start_time).total_seconds()
            
            # Создаем финальный результат
            final_result = VehicleCheckResults(
                request_id=request_id,
                vin=vin,
                results=response_results,
                total_checks=len(results),
                successful_checks=successful_checks,
                processing_time=processing_time,
                completed_at=datetime.now()
            )
            
            # Сохраняем результат
            completed_requests[request_id] = final_result
            
            # Обновляем статус
            active_requests[request_id]["status"] = "completed"
            active_requests[request_id]["completed_at"] = datetime.now()
            
            logger.info(f"✅ Запрос {request_id} завершен успешно. Успешных проверок: {successful_checks}/{len(results)}")
            
        finally:
            await checker.close()
            
    except Exception as e:
        logger.error(f"❌ Ошибка обработки запроса {request_id}: {e}")
        
        # Обновляем статус с ошибкой
        active_requests[request_id]["status"] = "failed"
        active_requests[request_id]["error"] = str(e)
        active_requests[request_id]["completed_at"] = datetime.now()

@app.get("/")
async def root():
    """Корневой эндпоинт"""
    return {
        "service": "ГИБДД Vehicle Checker API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "check_vehicle": "/api/v1/check",
            "get_result": "/api/v1/result/{request_id}",
            "get_status": "/api/v1/status/{request_id}",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """Проверка здоровья сервиса"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "active_requests": len(active_requests),
        "completed_requests": len(completed_requests)
    }

@app.post("/api/v1/check", response_model=VehicleCheckResponse)
async def check_vehicle(request: VehicleCheckRequest, background_tasks: BackgroundTasks):
    """Запуск проверки автомобиля"""
    try:
        # Генерируем уникальный ID запроса
        request_id = str(uuid.uuid4())
        
        # Конвертируем типы проверок
        check_types = [CheckType(ct.value) for ct in request.check_types]
        
        # Регистрируем запрос
        active_requests[request_id] = {
            "vin": request.vin,
            "check_types": [ct.value for ct in check_types],
            "status": "queued",
            "created_at": datetime.now(),
            "callback_url": request.callback_url
        }
        
        # Запускаем обработку в фоне
        background_tasks.add_task(process_vehicle_check, request_id, request.vin, check_types)
        
        logger.info(f"📝 Создан запрос {request_id} для VIN: {request.vin}")
        
        return VehicleCheckResponse(
            request_id=request_id,
            vin=request.vin,
            status="queued",
            message="Запрос поставлен в очередь на обработку",
            estimated_completion="2-5 минут"
        )
        
    except Exception as e:
        logger.error(f"❌ Ошибка создания запроса: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка создания запроса: {str(e)}")

@app.get("/api/v1/status/{request_id}")
async def get_request_status(request_id: str):
    """Получение статуса запроса"""
    if request_id not in active_requests:
        raise HTTPException(status_code=404, detail="Запрос не найден")
    
    request_info = active_requests[request_id]
    
    return {
        "request_id": request_id,
        "vin": request_info["vin"],
        "status": request_info["status"],
        "created_at": request_info["created_at"],
        "started_at": request_info.get("started_at"),
        "completed_at": request_info.get("completed_at"),
        "error": request_info.get("error")
    }

@app.get("/api/v1/result/{request_id}", response_model=VehicleCheckResults)
async def get_check_results(request_id: str):
    """Получение результатов проверки"""
    if request_id not in active_requests:
        raise HTTPException(status_code=404, detail="Запрос не найден")
    
    request_info = active_requests[request_id]
    
    if request_info["status"] == "queued":
        raise HTTPException(status_code=202, detail="Запрос в очереди на обработку")
    elif request_info["status"] == "processing":
        raise HTTPException(status_code=202, detail="Запрос обрабатывается")
    elif request_info["status"] == "failed":
        raise HTTPException(status_code=500, detail=f"Ошибка обработки: {request_info.get('error')}")
    elif request_info["status"] == "completed":
        if request_id in completed_requests:
            return completed_requests[request_id]
        else:
            raise HTTPException(status_code=500, detail="Результаты не найдены")
    else:
        raise HTTPException(status_code=500, detail="Неизвестный статус запроса")

@app.get("/api/v1/requests")
async def list_requests():
    """Список всех запросов (для отладки)"""
    return {
        "active_requests": len(active_requests),
        "completed_requests": len(completed_requests),
        "requests": {
            request_id: {
                "vin": info["vin"],
                "status": info["status"],
                "created_at": info["created_at"]
            }
            for request_id, info in active_requests.items()
        }
    }

@app.delete("/api/v1/requests/{request_id}")
async def cancel_request(request_id: str):
    """Отмена запроса"""
    if request_id not in active_requests:
        raise HTTPException(status_code=404, detail="Запрос не найден")
    
    request_info = active_requests[request_id]
    
    if request_info["status"] in ["completed", "failed"]:
        raise HTTPException(status_code=400, detail="Запрос уже завершен")
    
    # Помечаем как отмененный
    active_requests[request_id]["status"] = "cancelled"
    active_requests[request_id]["completed_at"] = datetime.now()
    
    return {"message": f"Запрос {request_id} отменен"}

# Пример использования API
@app.get("/api/v1/example")
async def api_example():
    """Пример использования API"""
    return {
        "description": "Пример использования ГИБДД Vehicle Checker API",
        "steps": [
            {
                "step": 1,
                "action": "POST /api/v1/check",
                "description": "Отправить VIN для проверки",
                "example": {
                    "vin": "WVWZZZ1JZYW386752",
                    "check_types": ["registration", "accidents"]
                }
            },
            {
                "step": 2,
                "action": "GET /api/v1/status/{request_id}",
                "description": "Проверить статус обработки"
            },
            {
                "step": 3,
                "action": "GET /api/v1/result/{request_id}",
                "description": "Получить результаты проверки"
            }
        ],
        "curl_examples": {
            "check_vehicle": """curl -X POST "http://localhost:8000/api/v1/check" \\
     -H "Content-Type: application/json" \\
     -d '{"vin": "WVWZZZ1JZYW386752", "check_types": ["registration", "accidents"]}'""",
            "get_status": "curl http://localhost:8000/api/v1/status/{request_id}",
            "get_results": "curl http://localhost:8000/api/v1/result/{request_id}"
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 