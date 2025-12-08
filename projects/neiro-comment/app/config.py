"""
Конфигурация приложения
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Настройки приложения"""
    
    # Telegram Configuration
    telegram_bot_token: str
    telegram_api_id: Optional[int] = None
    telegram_api_hash: Optional[str] = None
    
    # OpenAI Configuration
    openai_api_key: str
    openai_model: str = "gpt-3.5-turbo"
    
    # Database Configuration
    database_url: str = "sqlite:///./neirocomment.db"
    
    # Redis Configuration
    redis_url: str = "redis://localhost:6379/0"
    
    # Application Configuration
    secret_key: str
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Monitoring
    enable_metrics: bool = True
    log_level: str = "INFO"
    
    # AI Settings
    max_comment_length: int = 200
    comment_delay_min: int = 30  # секунд
    comment_delay_max: int = 300  # секунд
    
    # Rate Limiting
    max_comments_per_hour: int = 10
    max_comments_per_day: int = 50
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Глобальный экземпляр настроек
settings = Settings()
