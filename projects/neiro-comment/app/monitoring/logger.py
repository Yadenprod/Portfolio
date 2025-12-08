"""
Настройка логирования
"""
import logging
import sys
from datetime import datetime
from typing import Dict, Any

from app.config import settings


def setup_logging():
    """Настройка системы логирования"""
    
    # Создаем форматтер
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Настраиваем корневой логгер
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, settings.log_level.upper()))
    
    # Очищаем существующие обработчики
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Консольный обработчик
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, settings.log_level.upper()))
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # Файловый обработчик
    file_handler = logging.FileHandler('neirocomment.log', encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
    
    # Обработчик ошибок
    error_handler = logging.FileHandler('neirocomment_errors.log', encoding='utf-8')
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    root_logger.addHandler(error_handler)
    
    # Настраиваем логгеры для внешних библиотек
    logging.getLogger('telegram').setLevel(logging.WARNING)
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('openai').setLevel(logging.WARNING)
    
    logging.info("Система логирования инициализирована")


class StructuredLogger:
    """Структурированный логгер для системы"""
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
    
    def log_comment_generated(self, channel_id: str, post_id: str, comment: str, 
                             generation_time: float, ai_model: str):
        """Логирование сгенерированного комментария"""
        self.logger.info(
            f"Комментарий сгенерирован",
            extra={
                "event": "comment_generated",
                "channel_id": channel_id,
                "post_id": post_id,
                "comment_length": len(comment),
                "generation_time": generation_time,
                "ai_model": ai_model
            }
        )
    
    def log_comment_sent(self, channel_id: str, post_id: str, comment_id: str, 
                        comment: str, success: bool, error: str = None):
        """Логирование отправки комментария"""
        level = logging.INFO if success else logging.ERROR
        self.logger.log(
            level,
            f"Комментарий {'отправлен' if success else 'не отправлен'}",
            extra={
                "event": "comment_sent",
                "channel_id": channel_id,
                "post_id": post_id,
                "comment_id": comment_id,
                "comment_length": len(comment),
                "success": success,
                "error": error
            }
        )
    
    def log_channel_added(self, channel_id: str, username: str, title: str):
        """Логирование добавления канала"""
        self.logger.info(
            f"Канал добавлен: {username}",
            extra={
                "event": "channel_added",
                "channel_id": channel_id,
                "username": username,
                "title": title
            }
        )
    
    def log_channel_removed(self, channel_id: str, username: str):
        """Логирование удаления канала"""
        self.logger.info(
            f"Канал удален: {username}",
            extra={
                "event": "channel_removed",
                "channel_id": channel_id,
                "username": username
            }
        )
    
    def log_post_processed(self, channel_id: str, post_id: str, content: str, 
                          media_type: str, has_comment: bool):
        """Логирование обработки поста"""
        self.logger.info(
            f"Пост обработан: {post_id}",
            extra={
                "event": "post_processed",
                "channel_id": channel_id,
                "post_id": post_id,
                "content_length": len(content) if content else 0,
                "media_type": media_type,
                "has_comment": has_comment
            }
        )
    
    def log_rate_limit_hit(self, channel_id: str, limit_type: str, current_count: int, 
                          limit_value: int):
        """Логирование срабатывания rate limit"""
        self.logger.warning(
            f"Rate limit превышен: {limit_type}",
            extra={
                "event": "rate_limit_hit",
                "channel_id": channel_id,
                "limit_type": limit_type,
                "current_count": current_count,
                "limit_value": limit_value
            }
        )
    
    def log_ai_error(self, error: str, content: str, model: str):
        """Логирование ошибки AI"""
        self.logger.error(
            f"Ошибка AI: {error}",
            extra={
                "event": "ai_error",
                "error": error,
                "content_length": len(content) if content else 0,
                "model": model
            }
        )
    
    def log_telegram_error(self, error: str, channel_id: str = None, post_id: str = None):
        """Логирование ошибки Telegram"""
        self.logger.error(
            f"Ошибка Telegram: {error}",
            extra={
                "event": "telegram_error",
                "error": error,
                "channel_id": channel_id,
                "post_id": post_id
            }
        )
    
    def log_system_metrics(self, metrics: Dict[str, Any]):
        """Логирование системных метрик"""
        self.logger.info(
            "Системные метрики",
            extra={
                "event": "system_metrics",
                **metrics
            }
        )


# Глобальный экземпляр структурированного логгера
structured_logger = StructuredLogger("neirocomment")
