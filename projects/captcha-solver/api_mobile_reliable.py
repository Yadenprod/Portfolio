"""
Улучшенный Mobile API для ГИБДД VIN Checker с надежной проверкой данных
Использует систему валидации и повторных попыток для обеспечения качества данных
"""

import asyncio
import time
import uuid
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from concurrent.futures import ThreadPoolExecutor

import uvicorn
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from reliable_checker import check_vin_reliable
from cleanup_tool import CleanupTool
from config import FAST_CONFIG, PRODUCTION_CONFIG

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI приложение
app = FastAPI(
    title="ГИБДД VIN Checker Reliable API",
    description="Надежный API для проверки автомобилей по базам ГИБДД с валидацией данных",
    version="3.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Аутентификация
security = HTTPBearer()

# Хранилище активных запросов
active_requests: Dict[str, Dict[str, Any]] = {}

# Статистика
stats_data = {
    "total_checks": 0,
    "successful_checks": 0,
    "failed_checks": 0,
    "high_quality_checks": 0,  # Новая метрика
    "retries_used": 0,  # Новая метрика
    "total_duration": 0.0,
    "captcha_attempts": 0,
    "captcha_successes": 0
}

# Время запуска
start_time = time.time()

# Модели данных
class VINCheckRequest(BaseModel):
    """Модель запроса на проверку VIN"""
    vin: str = Field(..., min_length=17, max_length=17, description="VIN номер автомобиля")
    priority: Optional[str] = Field("normal", description="Приоритет: fast, normal, detailed")
    callback_url: Optional[str] = Field(None, description="URL для callback уведомления")
    client_id: Optional[str] = Field(None, description="ID клиента для статистики")
    max_attempts: Optional[int] = Field(3, description="Параметр игнорируется - система всегда использует 3 попытки")
    min_quality_score: Optional[float] = Field(60.0, description="Минимальная оценка качества данных")
    auto_cleanup_delay: Optional[int] = Field(300, description="Время задержки автоочистки скриншотов в секундах (по умолчанию 300 = 5 минут, 0 = отключить)")

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
    summary: Optional[Dict[str, Any]] = None  # Новое поле с итоговой информацией

class CheckStatisticsResponse(BaseModel):
    """Модель статистики"""
    total_checks: int
    successful_checks: int
    failed_checks: int
    high_quality_checks: int  # Новая метрика
    retries_used: int  # Новая метрика
    success_rate: float
    high_quality_rate: float  # Новая метрика
    captcha_success_rate: float
    average_check_time: float

class HealthResponse(BaseModel):
    """Модель health check"""
    status: str
    timestamp: str
    version: str
    uptime_seconds: float
    system_stats: Dict[str, Any]

# Пул потоков для выполнения проверок
import psutil
import threading

# Ограничиваем количество воркеров до 5 чтобы не перегружать систему
max_workers = 5  # Максимум 5 одновременных запросов
executor = ThreadPoolExecutor(max_workers=max_workers)

# Трекинг активных запросов
active_requests = set()
active_requests_lock = threading.Lock()

logger.info(f"🚀 Инициализация ThreadPoolExecutor с {max_workers} воркерами")

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Проверка токена"""
    token = credentials.credentials
    if token != "mobile_app_secret_token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный токен авторизации"
        )
    return token

def update_stats(results: List[Dict], duration: float, summary: Dict[str, Any]):
    """Обновление статистики с учетом качества данных"""
    stats_data["total_checks"] += 1
    
    if not results or not isinstance(results, list):
        stats_data["failed_checks"] += 1
        stats_data["total_duration"] += duration
        stats_data["captcha_attempts"] += 1
        return
    
    # Считаем успешные проверки
    successful = 0
    total_retries = 0
    high_quality_sections = 0
    
    for r in results:
        if isinstance(r, dict):
            if r.get("success", False):
                successful += 1
            
            # Считаем повторные попытки
            attempt_number = r.get("attempt_number", 1)
            if attempt_number > 1:
                total_retries += attempt_number - 1
            
            # Считаем высококачественные секции
            quality_score = r.get("quality_score", 0)
            if quality_score >= 60.0:  # Порог высокого качества
                high_quality_sections += 1
    
    # Обновляем статистику
    if successful == len(results):
        stats_data["successful_checks"] += 1
    else:
        stats_data["failed_checks"] += 1
    
    # Проверка общего качества
    avg_quality = summary.get("average_quality_score", 0)
    if avg_quality >= 60.0:
        stats_data["high_quality_checks"] += 1
    
    stats_data["retries_used"] += total_retries
    stats_data["total_duration"] += duration
    stats_data["captcha_attempts"] += 1
    if successful > 0:
        stats_data["captcha_successes"] += 1

def log_full_results(vin: str, result: Dict, duration: float):
    """Подробное логирование результатов с информацией о качестве"""
    if not isinstance(result, dict):
        logger.error(f"❌ Ошибка логирования: результат не является словарем: {type(result)}")
        return
        
    logger.info("=" * 80)
    logger.info(f"📋 НАДЕЖНАЯ ПРОВЕРКА VIN: {vin}")
    logger.info(f"⏱️ Время выполнения: {duration:.2f} сек")
    logger.info(f"📅 Время проверки: {result.get('timestamp', 'Не указано')}")
    
    # Выводим сводную информацию
    summary = result.get("summary", {})
    if summary:
        logger.info(f"📊 СВОДКА:")
        logger.info(f"   ✅ Успешных секций: {summary.get('successful_sections', 0)}/{summary.get('total_sections', 0)}")
        logger.info(f"   🎯 Среднее качество: {summary.get('average_quality_score', 0):.1f}%")
        logger.info(f"   ⭐ Высококачественных: {summary.get('high_quality_sections', 0)}")
    
    logger.info("=" * 80)
    
    results = result.get("results", [])
    
    for i, check_result in enumerate(results, 1):
        if not isinstance(check_result, dict):
            logger.info(f"\n{i}. ❌ НЕКОРРЕКТНЫЙ РЕЗУЛЬТАТ: {type(check_result)} - {str(check_result)[:100]}")
            continue
            
        section_name = check_result.get("type", "Неизвестно").upper()
        success = check_result.get("success", False)
        error = check_result.get("error")
        captcha_solved = check_result.get("captcha_solved", False)
        quality_score = check_result.get("quality_score", 0)
        attempt_number = check_result.get("attempt_number", 1)
        validation_errors = check_result.get("validation_errors", [])
        
        logger.info(f"\n{i}. 📋 СЕКЦИЯ: {section_name}")
        logger.info(f"   ✅ Статус: {'УСПЕХ' if success else 'ОШИБКА'}")
        logger.info(f"   🔐 Капча решена: {'Да' if captcha_solved else 'Нет'}")
        logger.info(f"   🎯 Качество: {quality_score:.1f}%")
        logger.info(f"   🔄 Попытка: {attempt_number}")
        
        if validation_errors:
            logger.info(f"   ⚠️ Ошибки валидации: {', '.join(validation_errors)}")
        
        if error:
            logger.info(f"   ❌ Ошибка: {error}")
        
        if success and check_result.get("data"):
            data = check_result["data"]
            logger.info(f"   📊 Данные получены: {len(data)} блоков")
            
            # Специальная обработка для ДТП
            if section_name == "ACCIDENTS":
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
    
    logger.info("=" * 80)

def cleanup_screenshots_after_check(results: List[Dict], delay_seconds: int = 300):
    """
    Удаляет скриншоты после завершения проверки VIN с задержкой
    
    Args:
        results: Результаты проверки VIN
        delay_seconds: Задержка в секундах перед удалением (по умолчанию 5 минут)
    """
    def delayed_cleanup():
        time.sleep(delay_seconds)
        screenshot_files = []
        
        try:
            # Собираем все пути к скриншотам из результатов
            for result in results:
                if isinstance(result, dict) and result.get('data'):
                    for data_block in result['data']:
                        if isinstance(data_block, dict) and 'screenshot_path' in data_block:
                            screenshot_path = data_block['screenshot_path']
                            if os.path.exists(screenshot_path):
                                screenshot_files.append(screenshot_path)
            
            # Удаляем файлы
            deleted_count = 0
            for file_path in screenshot_files:
                try:
                    os.remove(file_path)
                    deleted_count += 1
                    logger.info(f"🗑️ Удален скриншот: {file_path}")
                except Exception as e:
                    logger.warning(f"⚠️ Не удалось удалить скриншот {file_path}: {e}")
            
            if deleted_count > 0:
                logger.info(f"✅ Автоочистка завершена: удалено {deleted_count} скриншотов")
        
        except Exception as e:
            logger.error(f"❌ Ошибка в автоочистке скриншотов: {e}")
    
    # Запускаем очистку в фоне
    import threading
    cleanup_thread = threading.Thread(target=delayed_cleanup, daemon=True)
    cleanup_thread.start()

@app.get("/", response_model=Dict[str, str])
async def root():
    """Корневой endpoint"""
    return {
        "message": "ГИБДД VIN Checker Reliable API v3.0",
        "docs": "/docs",
        "health": "/health",
        "features": "Надежная проверка с валидацией данных"
    }

@app.get("/load-info")
async def get_load_info(token: str = Depends(verify_token)):
    """Информация о нагрузке сервера"""
    try:
        process = psutil.Process()
        memory_info = process.memory_info()
        
        with active_requests_lock:
            active_count = len(active_requests)
        
        return {
            "active_tasks": active_count,
            "max_workers": executor._max_workers,
            "max_queue_size": 20,  # Максимальный размер очереди
            "queue_size": executor._work_queue.qsize() if hasattr(executor._work_queue, 'qsize') else 0,
            "queue_utilization_percent": (active_count / 20) * 100,  # Процент использования очереди
            "memory_usage_mb": memory_info.rss / 1024 / 1024,
            "memory_percent": psutil.virtual_memory().percent,
            "cpu_percent": psutil.cpu_percent(interval=1),
            "cpu_count": psutil.cpu_count(),
            "status": "overloaded" if active_count >= 20 else "busy" if active_count >= 15 else "normal",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {"error": f"Ошибка получения информации о нагрузке: {e}"}

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check для мониторинга"""
    cleaner = CleanupTool()
    disk_usage = cleaner.get_disk_usage()
    
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="3.0.0",
        uptime_seconds=time.time() - start_time,
        system_stats={
            "active_requests": len(active_requests),
            "temp_files_count": disk_usage["temp_files_count"],
            "total_disk_usage_mb": disk_usage["total_size_mb"],
            "reliability_features": True
        }
    )

@app.post("/check/sync", response_model=VINCheckResponse)
async def check_vin_sync(
    request: VINCheckRequest,
    token: str = Depends(verify_token)
):
    """Синхронная надежная проверка VIN"""
    request_id = str(uuid.uuid4())
    
    # Защита от перегрузки - ограничиваем очередь
    with active_requests_lock:
        active_count = len(active_requests)
    
    MAX_QUEUE_SIZE = 20  # Максимум запросов в очереди (уменьшено с 50 до 20)
    if active_count >= MAX_QUEUE_SIZE:
        logger.warning(f"🚫 Сервер перегружен: {active_count} активных запросов (максимум {MAX_QUEUE_SIZE})")
        raise HTTPException(
            status_code=503,
            detail=f"Сервер перегружен. Активных запросов: {active_count}/{MAX_QUEUE_SIZE}. Попробуйте позже."
        )
    
    # Добавляем запрос в активные
    with active_requests_lock:
        active_requests.add(request_id)
    
    logger.info(f"🔄 Получен запрос на проверку VIN: {request.vin} (ID: {request_id}, активных: {active_count + 1})")
    
    # Валидация VIN
    if not request.vin.isalnum():
        with active_requests_lock:
            active_requests.discard(request_id)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="VIN должен содержать только буквы и цифры"
        )
    
    try:
        # Выполняем надежную проверку (принудительно 3 попытки для максимальной надежности)
        start_time_check = time.time()
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            executor,
            check_vin_reliable,
            request.vin,
            3,  # Всегда 3 попытки для максимальной надежности
            request.min_quality_score
        )
        check_duration = time.time() - start_time_check
        
        # Проверяем результат
        if not isinstance(result, dict):
            logger.error(f"❌ Неожиданный тип результата: {type(result)}")
            error_msg = str(result) if isinstance(result, str) else f"Неожиданный тип результата: {type(result)}"
            return VINCheckResponse(
                request_id=request_id,
                vin=request.vin,
                status="error",
                timestamp=datetime.now().isoformat(),
                error=error_msg
            )
        
        # Проверяем общую ошибку
        if "error" in result and result["error"]:
            logger.error(f"❌ Ошибка в результатах: {result['error']}")
            return VINCheckResponse(
                request_id=request_id,
                vin=request.vin,
                status="error",
                timestamp=datetime.now().isoformat(),
                error=result["error"]
            )
        
        # Обновляем статистику
        summary = result.get("summary", {})
        update_stats(result.get("results", []), check_duration, summary)
        
        # Выводим результаты в логи
        log_full_results(request.vin, result, check_duration)
        
        # Запускаем автоочистку скриншотов если это настроено
        if request.auto_cleanup_delay > 0:
            cleanup_screenshots_after_check(result.get("results", []), delay_seconds=request.auto_cleanup_delay)
            delay_minutes = request.auto_cleanup_delay // 60
            logger.info(f"🗑️ Запланирована автоочистка скриншотов для VIN {request.vin} через {delay_minutes} минут")
        else:
            logger.info(f"🗑️ Автоочистка скриншотов отключена для VIN {request.vin}")
        
        # Формируем ответ
        response = VINCheckResponse(
            request_id=request_id,
            vin=request.vin,
            status="completed",
            timestamp=datetime.now().isoformat(),
            from_cache=False,
            check_duration=check_duration,
            results=result.get("results", []),
            summary=summary
        )
        
        # Удаляем запрос из активных
        with active_requests_lock:
            active_requests.discard(request_id)
        
        return response
        
    except Exception as e:
        logger.error(f"❌ Ошибка надежной проверки VIN {request.vin}: {e}")
        stats_data["failed_checks"] += 1
        
        # Удаляем запрос из активных в случае ошибки
        with active_requests_lock:
            active_requests.discard(request_id)
        
        return VINCheckResponse(
            request_id=request_id,
            vin=request.vin,
            status="error",
            timestamp=datetime.now().isoformat(),
            error=str(e)
        )

@app.get("/statistics", response_model=CheckStatisticsResponse)
async def get_statistics(
    days: int = 7,
    token: str = Depends(verify_token)
):
    """Получить расширенную статистику работы"""
    total = stats_data["total_checks"]
    success_rate = (stats_data["successful_checks"] / total * 100) if total > 0 else 0
    high_quality_rate = (stats_data["high_quality_checks"] / total * 100) if total > 0 else 0
    avg_time = (stats_data["total_duration"] / total) if total > 0 else 0
    captcha_rate = (stats_data["captcha_successes"] / stats_data["captcha_attempts"] * 100) if stats_data["captcha_attempts"] > 0 else 0
    
    return CheckStatisticsResponse(
        total_checks=total,
        successful_checks=stats_data["successful_checks"],
        failed_checks=stats_data["failed_checks"],
        high_quality_checks=stats_data["high_quality_checks"],
        retries_used=stats_data["retries_used"],
        success_rate=success_rate,
        high_quality_rate=high_quality_rate,
        captcha_success_rate=captcha_rate,
        average_check_time=avg_time
    )

@app.get("/screenshot/{filename}")
async def get_screenshot(
    filename: str, 
    delete_after_send: bool = False,
    token: str = Depends(verify_token)
):
    """
    Получить скриншот по имени файла
    
    Args:
        filename: Имя файла скриншота
        delete_after_send: Удалить файл после отправки (по умолчанию False)
    """
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
    
    # Если нужно удалить после отправки
    if delete_after_send:
        def cleanup_file():
            """Удаляет файл после небольшой задержки"""
            try:
                time.sleep(1)  # Небольшая задержка чтобы файл успел отправиться
                if os.path.exists(file_path):
                    os.remove(file_path)
                    logger.info(f"🗑️ Скриншот удален после отправки: {filename}")
            except Exception as e:
                logger.warning(f"⚠️ Не удалось удалить скриншот после отправки {filename}: {e}")
        
        # Запускаем удаление в фоне
        import threading
        cleanup_thread = threading.Thread(target=cleanup_file, daemon=True)
        cleanup_thread.start()
    
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

if __name__ == "__main__":
    print("🚀 Запуск Reliable Mobile API сервера для ГИБДД VIN Checker")
    print("📱 API готов для интеграции с мобильным приложением")
    print("🔄 Надежная проверка с валидацией данных!")
    print("🎯 Автоматические повторные попытки для качественных данных")
    print("📚 Документация: http://localhost:8000/docs")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False,
        access_log=True
    ) 