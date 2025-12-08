#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Mobile API сервер для проверки VIN автомобилей
Интеграция с мобильным приложением
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import asyncio
import uvicorn
import os
import time
import uuid
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import logging

# Используем параллельный чекер без кэширования
from parallel_checker import check_vin_parallel
from config import PRODUCTION_CONFIG, FAST_CONFIG
from cleanup_tool import CleanupTool

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Модели данных
class VINCheckRequest(BaseModel):
    """Модель запроса на проверку VIN"""
    vin: str = Field(..., min_length=17, max_length=17, description="VIN номер автомобиля")
    priority: Optional[str] = Field("normal", description="Приоритет: fast, normal, detailed")
    callback_url: Optional[str] = Field(None, description="URL для callback уведомления")
    client_id: Optional[str] = Field(None, description="ID клиента для статистики")

class VINCheckResponse(BaseModel):
    """Модель ответа проверки VIN"""
    request_id: str
    vin: str
    status: str  # pending, processing, completed, error
    timestamp: str
    from_cache: bool = False
    check_duration: Optional[float] = None
    results: Optional[List[Dict[str, Any]]] = None
    error: Optional[str] = None

class CheckStatisticsResponse(BaseModel):
    """Модель статистики"""
    total_checks: int
    successful_checks: int
    failed_checks: int
    success_rate: float
    captcha_success_rate: float
    average_check_time: float

class HealthResponse(BaseModel):
    """Модель health check"""
    status: str
    timestamp: str
    version: str
    uptime_seconds: float
    system_stats: Dict[str, Any]

# Хранилище активных запросов
active_requests = {}
start_time = time.time()

# Простая статистика в памяти (без кэширования)
stats_data = {
    "total_checks": 0,
    "successful_checks": 0,
    "failed_checks": 0,
    "total_duration": 0.0,
    "captcha_successes": 0,
    "captcha_attempts": 0
}

# Инициализация API
app = FastAPI(
    title="ГИБДД VIN Checker API",
    description="API для проверки VIN номеров автомобилей через сайт ГИБДД",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS для мобильного приложения
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Простая аутентификация (в продакшене использовать JWT)
security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Проверка токена"""
    # В продакшене здесь должна быть проверка JWT токена
    token = credentials.credentials
    if token != "mobile_app_secret_token":  # Замените на вашу логику
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный токен авторизации"
        )
    return token

# Пул потоков для выполнения проверок - ограничиваем до 5 воркеров для предотвращения перегрузки
executor = ThreadPoolExecutor(max_workers=5)

logger.info(f"🚀 Инициализация ThreadPoolExecutor с 5 воркерами для предотвращения перегрузки системы")

def update_stats(results: List[Dict], duration: float):
    """Обновление статистики в памяти"""
    stats_data["total_checks"] += 1
    
    # Проверяем что results - это список словарей
    if not results or not isinstance(results, list):
        stats_data["failed_checks"] += 1
        stats_data["total_duration"] += duration
        stats_data["captcha_attempts"] += 1
        return
    
    # Считаем успешные проверки, безопасно обрабатывая каждый элемент
    successful = 0
    for r in results:
        if isinstance(r, dict) and r.get("success", False):
            successful += 1
    
    if successful == len(results):
        stats_data["successful_checks"] += 1
    else:
        stats_data["failed_checks"] += 1
    
    stats_data["total_duration"] += duration
    
    # Подсчет успешности капчи (примерная оценка)
    stats_data["captcha_attempts"] += 1
    if successful > 0:
        stats_data["captcha_successes"] += 1

def log_full_results(vin: str, result: Dict, duration: float):
    """Подробное логирование результатов для контроля"""
    if not isinstance(result, dict):
        logger.error(f"❌ Ошибка логирования: результат не является словарем: {type(result)}")
        return
        
    logger.info("=" * 80)
    logger.info(f"📋 ПОЛНЫЕ РЕЗУЛЬТАТЫ ПРОВЕРКИ VIN: {vin}")
    logger.info(f"⏱️ Время выполнения: {duration:.2f} сек")
    logger.info(f"📅 Время проверки: {result.get('timestamp', 'Не указано')}")
    logger.info("=" * 80)
    
    results = result.get("results", [])
    successful_count = 0
    for r in results:
        if isinstance(r, dict) and r.get("success", False):
            successful_count += 1
    
    logger.info(f"✅ Успешных проверок: {successful_count}/{len(results)}")
    
    for i, check_result in enumerate(results, 1):
        if not isinstance(check_result, dict):
            logger.info(f"\n{i}. ❌ НЕКОРРЕКТНЫЙ РЕЗУЛЬТАТ: {type(check_result)} - {str(check_result)[:100]}")
            continue
            
        section_name = check_result.get("type", "Неизвестно").upper()
        success = check_result.get("success", False)
        error = check_result.get("error")
        captcha_solved = check_result.get("captcha_solved", False)
        
        logger.info(f"\n{i}. 📋 СЕКЦИЯ: {section_name}")
        logger.info(f"   ✅ Статус: {'УСПЕХ' if success else 'ОШИБКА'}")
        logger.info(f"   🔐 Капча решена: {'Да' if captcha_solved else 'Нет'}")
        
        if error:
            logger.info(f"   ❌ Ошибка: {error}")
        
        if success and check_result.get("data"):
            data = check_result["data"]
            logger.info(f"   📊 Данные получены: {len(data)} блоков")
            
            # Детальный вывод данных по типам
            if section_name == "REGISTRATION":
                for j, data_block in enumerate(data, 1):
                    block_type = data_block.get("block", "unknown")
                    text = data_block.get("text", "")
                    logger.info(f"      {j}. Блок '{block_type}':")
                    if text:
                        # Выводим первые 200 символов текста
                        preview = text.replace("\n", " ").strip()[:200]
                        logger.info(f"         Текст: {preview}{'...' if len(text) > 200 else ''}")
                        
                        # Ищем ключевые поля
                        lines = text.split('\n')
                        for line in lines:
                            if any(keyword in line for keyword in ['Марка', 'Модель', 'Год выпуска', 'VIN', 'Номер кузова']):
                                logger.info(f"         📌 {line.strip()}")
            
            elif section_name == "ACCIDENTS":
                total_accidents = 1
                screenshot_count = 0
                
                # Подсчитываем общее количество ДТП и скриншотов  
                for data_block in data:
                    if "total_accidents" in data_block:
                        total_accidents = data_block["total_accidents"]
                    if "screenshot_path" in data_block:
                        screenshot_count += 1
                
                logger.info(f"      📊 Всего ДТП: {total_accidents}, Скриншотов: {screenshot_count}")
                
                for j, data_block in enumerate(data, 1):
                    accident_num = data_block.get("accident_number", j)
                    logger.info(f"      📋 ДТП #{accident_num}:")
                    
                    if "screenshot_path" in data_block:
                        logger.info(f"         📸 Скриншот: {data_block['screenshot_path']}")
                    if "text" in data_block:
                        text = data_block["text"].replace("\n", " ").strip()[:150]
                        logger.info(f"         📝 Текст: {text}{'...' if len(data_block.get('text', '')) > 150 else ''}")
            
            elif section_name in ["WANTED", "RESTRICTIONS"]:
                for j, data_block in enumerate(data, 1):
                    if "text" in data_block:
                        text = data_block["text"].replace("\n", " ").strip()[:200]
                        logger.info(f"      {j}. {text}")
    
    logger.info("=" * 80)
    logger.info(f"🎯 ИТОГО: {successful_count} успешных из {len(results)} проверок за {duration:.2f} сек")
    logger.info("=" * 80)

@app.get("/", response_model=Dict[str, str])
async def root():
    """Корневой endpoint"""
    return {
        "message": "ГИБДД VIN Checker API v2.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check для мониторинга"""
    cleaner = CleanupTool()
    disk_usage = cleaner.get_disk_usage()
    
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="2.0.0",
        uptime_seconds=time.time() - start_time,
        system_stats={
            "active_requests": len(active_requests),
            "temp_files_count": disk_usage["temp_files_count"],
            "total_disk_usage_mb": disk_usage["total_size_mb"]
        }
    )

@app.post("/check", response_model=VINCheckResponse)
async def check_vin_async(
    request: VINCheckRequest,
    background_tasks: BackgroundTasks,
    token: str = Depends(verify_token)
):
    """Асинхронная проверка VIN"""
    request_id = str(uuid.uuid4())
    
    # Валидация VIN
    if not request.vin.isalnum():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="VIN должен содержать только буквы и цифры"
        )
    
    # Создаем запрос
    active_requests[request_id] = {
        "vin": request.vin,
        "status": "pending",
        "timestamp": datetime.now().isoformat(),
        "priority": request.priority,
        "client_id": request.client_id
    }
    
    # Выбираем конфигурацию по приоритету
    config = FAST_CONFIG if request.priority == "fast" else PRODUCTION_CONFIG
    
    # Запускаем проверку в фоне
    background_tasks.add_task(
        perform_vin_check_background,
        request_id,
        request.vin,
        config,
        request.callback_url
    )
    
    return VINCheckResponse(
        request_id=request_id,
        vin=request.vin,
        status="pending",
        timestamp=datetime.now().isoformat()
    )

@app.post("/check/sync", response_model=VINCheckResponse)
async def check_vin_sync(
    request: VINCheckRequest,
    token: str = Depends(verify_token)
):
    """Синхронная проверка VIN"""
    request_id = str(uuid.uuid4())
    
    # Валидация VIN
    if not request.vin.isalnum():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="VIN должен содержать только буквы и цифры"
        )
    
    # Выбираем конфигурацию
    config = FAST_CONFIG if request.priority == "fast" else PRODUCTION_CONFIG
    
    try:
        # Выполняем проверку синхронно без кэширования
        start_time_check = time.time()
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            executor,
            check_vin_parallel,
            request.vin
        )
        check_duration = time.time() - start_time_check
        
        # Проверяем что результат - это словарь
        if not isinstance(result, dict):
            logger.error(f"❌ Неожиданный тип результата: {type(result)}, значение: {result}")
            # Если результат - строка, рассматриваем как ошибку
            error_msg = str(result) if isinstance(result, str) else f"Неожиданный тип результата: {type(result)}"
            return VINCheckResponse(
                request_id=request_id,
                vin=request.vin,
                status="error",
                timestamp=datetime.now().isoformat(),
                error=error_msg
            )
        
        # Проверяем есть ли общая ошибка в результате
        if "error" in result and result["error"]:
            logger.error(f"❌ Ошибка в результатах проверки: {result['error']}")
            return VINCheckResponse(
                request_id=request_id,
                vin=request.vin,
                status="error",
                timestamp=datetime.now().isoformat(),
                error=result["error"]
            )
        
        # Обновляем статистику
        update_stats(result.get("results", []), check_duration)
        
        # Выводим полные результаты в логи
        log_full_results(request.vin, result, check_duration)
        
        # Форматируем ответ
        return VINCheckResponse(
            request_id=request_id,
            vin=request.vin,
            status="completed",
            timestamp=datetime.now().isoformat(),
            from_cache=False,  # Всегда False, так как кэша нет
            check_duration=check_duration,
            results=result.get("results", [])
        )
        
    except Exception as e:
        logger.error(f"❌ Ошибка синхронной проверки VIN {request.vin}: {e}")
        logger.error("=" * 80)
        logger.error(f"📋 ОШИБКА ПРОВЕРКИ VIN: {request.vin}")
        logger.error(f"❌ Исключение: {str(e)}")
        logger.error("=" * 80)
        stats_data["failed_checks"] += 1
        return VINCheckResponse(
            request_id=request_id,
            vin=request.vin,
            status="error",
            timestamp=datetime.now().isoformat(),
            error=str(e)
        )

@app.get("/check/{request_id}", response_model=VINCheckResponse)
async def get_check_status(request_id: str, token: str = Depends(verify_token)):
    """Получить статус проверки по ID"""
    if request_id not in active_requests:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Запрос не найден"
        )
    
    request_data = active_requests[request_id]
    
    return VINCheckResponse(
        request_id=request_id,
        vin=request_data["vin"],
        status=request_data["status"],
        timestamp=request_data["timestamp"],
        from_cache=False,  # Всегда False
        check_duration=request_data.get("check_duration"),
        results=request_data.get("results"),
        error=request_data.get("error")
    )

@app.get("/statistics", response_model=CheckStatisticsResponse)
async def get_statistics(
    days: int = 7,
    token: str = Depends(verify_token)
):
    """Получить статистику работы"""
    total = stats_data["total_checks"]
    success_rate = (stats_data["successful_checks"] / total * 100) if total > 0 else 0
    avg_time = (stats_data["total_duration"] / total) if total > 0 else 0
    captcha_rate = (stats_data["captcha_successes"] / stats_data["captcha_attempts"] * 100) if stats_data["captcha_attempts"] > 0 else 0
    
    return CheckStatisticsResponse(
        total_checks=total,
        successful_checks=stats_data["successful_checks"],
        failed_checks=stats_data["failed_checks"],
        success_rate=success_rate,
        captcha_success_rate=captcha_rate,
        average_check_time=avg_time
    )

@app.get("/screenshot/{filename}")
async def get_screenshot(filename: str, token: str = Depends(verify_token)):
    """Получить скриншот по имени файла"""
    # Проверяем безопасность пути
    if not filename.startswith("dtp_block_") or not filename.endswith(".png"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неверное имя файла"
        )
    
    file_path = os.path.join(os.getcwd(), filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Файл не найден"
        )
    
    return FileResponse(
        file_path,
        media_type="image/png",
        filename=filename
    )

@app.delete("/cleanup")
async def cleanup_files(
    hours: int = 24,
    token: str = Depends(verify_token)
):
    """Очистка старых файлов"""
    cleaner = CleanupTool(max_age_hours=hours)
    removed_files = cleaner.clean_old_files(dry_run=False)
    
    return {
        "message": f"Очищено {len(removed_files)} файлов",
        "removed_files": removed_files,
        "hours_threshold": hours
    }

@app.get("/active-requests")
async def get_active_requests(token: str = Depends(verify_token)):
    """Получить список активных запросов"""
    return {
        "count": len(active_requests),
        "requests": list(active_requests.keys())
    }

# Фоновые задачи
async def perform_vin_check_background(
    request_id: str,
    vin: str,
    config,
    callback_url: Optional[str] = None
):
    """Выполнение проверки VIN в фоне"""
    try:
        # Обновляем статус
        active_requests[request_id]["status"] = "processing"
        
        # Выполняем проверку без кэширования
        start_time_check = time.time()
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            executor,
            check_vin_parallel,
            vin
        )
        check_duration = time.time() - start_time_check
        
        # Проверяем что результат - это словарь
        if not isinstance(result, dict):
            logger.error(f"❌ Неожиданный тип результата: {type(result)}, значение: {result}")
            error_msg = str(result) if isinstance(result, str) else f"Неожиданный тип результата: {type(result)}"
            active_requests[request_id].update({
                "status": "error",
                "error": error_msg
            })
            return
        
        # Проверяем есть ли общая ошибка в результате
        if "error" in result and result["error"]:
            logger.error(f"❌ Ошибка в результатах проверки: {result['error']}")
            active_requests[request_id].update({
                "status": "error",
                "error": result["error"]
            })
            return
        
        # Обновляем статистику
        update_stats(result.get("results", []), check_duration)
        
        # Выводим полные результаты в логи
        log_full_results(vin, result, check_duration)
        
        # Обновляем результат
        active_requests[request_id].update({
            "status": "completed",
            "from_cache": False,  # Всегда False
            "check_duration": check_duration,
            "results": result.get("results", [])
        })
        
        # Отправляем callback если указан
        if callback_url:
            await send_callback(callback_url, request_id, active_requests[request_id])
            
    except Exception as e:
        logger.error(f"❌ Ошибка фоновой проверки VIN {vin}: {e}")
        logger.error("=" * 80)
        logger.error(f"📋 ОШИБКА ФОНОВОЙ ПРОВЕРКИ VIN: {vin}")
        logger.error(f"❌ Исключение: {str(e)}")
        logger.error("=" * 80)
        stats_data["failed_checks"] += 1
        active_requests[request_id].update({
            "status": "error",
            "error": str(e)
        })

async def send_callback(callback_url: str, request_id: str, data: dict):
    """Отправка callback уведомления"""
    import aiohttp
    
    try:
        async with aiohttp.ClientSession() as session:
            payload = {"request_id": request_id, "data": data}
            async with session.post(callback_url, json=payload) as response:
                if response.status == 200:
                    logger.info(f"Callback отправлен успешно для {request_id}")
                else:
                    logger.warning(f"Ошибка callback для {request_id}: {response.status}")
    except Exception as e:
        logger.error(f"Ошибка отправки callback для {request_id}: {e}")

if __name__ == "__main__":
    print("🚀 Запуск Mobile API сервера для ГИБДД VIN Checker")
    print("📱 API готов для интеграции с мобильным приложением")
    print("🔄 Кэширование отключено - всегда свежие данные!")
    print("📋 Подробное логирование результатов включено!")
    print("📚 Документация: http://localhost:8000/docs")
    
    # Устанавливаем уровень логирования для детального вывода
    logging.getLogger("api_mobile").setLevel(logging.INFO)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False,
        access_log=True
    ) 