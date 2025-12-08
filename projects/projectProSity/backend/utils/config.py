import os
from typing import Dict, List
from pydantic import BaseSettings

class Settings(BaseSettings):
    """Настройки системы детекции краж"""
    
    # Основные настройки
    APP_NAME: str = "ProSity Security"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Настройки сервера
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Настройки базы данных
    DATABASE_URL: str = "sqlite:///./prosity_security.db"
    
    # Настройки Redis для кэширования
    REDIS_URL: str = "redis://localhost:6379"
    
    # Настройки детекции
    DETECTION_CONFIDENCE_THRESHOLD: float = 0.7
    SUSPICIOUS_BEHAVIOR_THRESHOLD: float = 0.6
    PACKAGE_OPENING_THRESHOLD: float = 0.8
    EXIT_MOVEMENT_THRESHOLD: float = 0.7
    
    # Настройки камер
    CAMERA_FPS: int = 30
    CAMERA_RESOLUTION: tuple = (1920, 1080)
    MAX_CAMERAS_PER_STORE: int = 10
    
    # Настройки уведомлений
    ALERT_RETENTION_DAYS: int = 30
    MAX_ALERTS_PER_HOUR: int = 100
    
    # Настройки безопасности
    SECRET_KEY: str = "your-secret-key-here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Настройки логирования
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "prosity_security.log"
    
    # Настройки аналитики
    ANALYTICS_RETENTION_DAYS: int = 365
    REPORT_GENERATION_INTERVAL_HOURS: int = 24
    
    # Настройки производительности
    MAX_CONCURRENT_DETECTIONS: int = 10
    DETECTION_TIMEOUT_SECONDS: int = 5
    
    # Настройки магазинов по умолчанию
    DEFAULT_STORE_CONFIGS: Dict = {
        "electronics_store": {
            "name": "Магазин электроники",
            "category": "Электроника",
            "theft_risk": "Очень высокий",
            "recommended_cameras": 6,
            "monthly_losses": 150000,
            "prevention_rate": 0.85
        },
        "clothing_store": {
            "name": "Магазин одежды",
            "category": "Одежда", 
            "theft_risk": "Высокий",
            "recommended_cameras": 4,
            "monthly_losses": 80000,
            "prevention_rate": 0.75
        },
        "cosmetics_store": {
            "name": "Магазин косметики",
            "category": "Косметика",
            "theft_risk": "Средний",
            "recommended_cameras": 3,
            "monthly_losses": 40000,
            "prevention_rate": 0.65
        }
    }
    
    # Настройки зон выхода
    EXIT_ZONES: List[Dict] = [
        {
            "id": "main_exit",
            "name": "Главный выход",
            "priority": "Высокая",
            "coordinates": {"x": 0.8, "y": 0.5, "width": 0.2, "height": 0.3}
        },
        {
            "id": "side_exit", 
            "name": "Боковой выход",
            "priority": "Средняя",
            "coordinates": {"x": 0.1, "y": 0.7, "width": 0.15, "height": 0.25}
        },
        {
            "id": "parking_exit",
            "name": "Выход на парковку", 
            "priority": "Высокая",
            "coordinates": {"x": 0.9, "y": 0.8, "width": 0.1, "height": 0.2}
        }
    ]
    
    # Настройки типов детекции
    DETECTION_TYPES: List[str] = [
        "suspicious_behavior",
        "package_opening", 
        "exit_movement",
        "face_avoidance",
        "hand_hiding",
        "loitering"
    ]
    
    # Настройки уровней серьезности
    SEVERITY_LEVELS: List[str] = [
        "low",
        "medium", 
        "high",
        "critical"
    ]
    
    # Настройки уведомлений
    NOTIFICATION_CHANNELS: List[str] = [
        "websocket",
        "email",
        "sms",
        "push"
    ]
    
    # Настройки отчетов
    REPORT_TYPES: List[str] = [
        "daily",
        "weekly",
        "monthly",
        "quarterly",
        "annual"
    ]
    
    # Настройки экспорта
    EXPORT_FORMATS: List[str] = [
        "json",
        "csv",
        "pdf",
        "excel"
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Создание экземпляра настроек
settings = Settings()

# Дополнительные константы
class Constants:
    """Константы системы"""
    
    # Коды ошибок
    ERROR_CODES = {
        "DETECTION_FAILED": "DET_001",
        "CAMERA_OFFLINE": "CAM_001", 
        "DATABASE_ERROR": "DB_001",
        "AUTHENTICATION_FAILED": "AUTH_001",
        "PERMISSION_DENIED": "PERM_001"
    }
    
    # Статусы системы
    SYSTEM_STATUS = {
        "ONLINE": "online",
        "OFFLINE": "offline",
        "MAINTENANCE": "maintenance",
        "ERROR": "error"
    }
    
    # Статусы детекции
    DETECTION_STATUS = {
        "ACTIVE": "active",
        "PAUSED": "paused",
        "STOPPED": "stopped",
        "ERROR": "error"
    }
    
    # Типы событий
    EVENT_TYPES = {
        "THEFT_DETECTED": "theft_detected",
        "SUSPICIOUS_BEHAVIOR": "suspicious_behavior",
        "PACKAGE_OPENING": "package_opening",
        "EXIT_MOVEMENT": "exit_movement",
        "SYSTEM_ALERT": "system_alert"
    }
    
    # Цвета для UI
    UI_COLORS = {
        "success": "#10B981",
        "warning": "#F59E0B", 
        "error": "#EF4444",
        "info": "#3B82F6",
        "primary": "#6366F1"
    }
    
    # Размеры файлов
    MAX_FILE_SIZE = {
        "image": 10 * 1024 * 1024,  # 10MB
        "video": 100 * 1024 * 1024,  # 100MB
        "document": 5 * 1024 * 1024   # 5MB
    }
    
    # Форматы файлов
    ALLOWED_FORMATS = {
        "image": [".jpg", ".jpeg", ".png", ".bmp"],
        "video": [".mp4", ".avi", ".mov", ".mkv"],
        "document": [".pdf", ".doc", ".docx", ".xls", ".xlsx"]
    }

# Создание экземпляра констант
constants = Constants()
