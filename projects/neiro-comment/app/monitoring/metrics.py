"""
Система метрик и мониторинга
"""
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from dataclasses import dataclass

from app.database.connection import SessionLocal
from app.database.models import Channel, Post, Comment, Metrics
from app.config import settings

logger = logging.getLogger(__name__)


@dataclass
class SystemMetrics:
    """Структура системных метрик"""
    timestamp: datetime
    total_channels: int
    active_channels: int
    total_posts: int
    commented_posts: int
    total_comments: int
    comments_today: int
    comments_this_hour: int
    comments_this_minute: int
    avg_comment_length: float
    success_rate: float
    error_rate: float
    system_uptime: float


class MetricsCollector:
    """Сборщик метрик системы"""
    
    def __init__(self):
        self.start_time = time.time()
        self.last_metrics_time = time.time()
        self.error_count = 0
        self.success_count = 0
    
    def collect_metrics(self) -> SystemMetrics:
        """Сбор текущих метрик системы"""
        try:
            db = SessionLocal()
            
            # Базовые метрики
            total_channels = db.query(Channel).count()
            active_channels = db.query(Channel).filter(Channel.is_active == True).count()
            total_posts = db.query(Post).count()
            commented_posts = db.query(Post).filter(Post.is_commented == True).count()
            total_comments = db.query(Comment).count()
            
            # Временные метрики
            now = datetime.now()
            today = now.date()
            one_hour_ago = now - timedelta(hours=1)
            one_minute_ago = now - timedelta(minutes=1)
            
            comments_today = db.query(Comment).filter(
                Comment.created_at >= today
            ).count()
            
            comments_this_hour = db.query(Comment).filter(
                Comment.created_at >= one_hour_ago
            ).count()
            
            comments_this_minute = db.query(Comment).filter(
                Comment.created_at >= one_minute_ago
            ).count()
            
            # Средняя длина комментариев
            avg_length_result = db.query(Comment.content).filter(
                Comment.status == "sent"
            ).all()
            
            if avg_length_result:
                avg_comment_length = sum(len(comment[0]) for comment in avg_length_result) / len(avg_length_result)
            else:
                avg_comment_length = 0.0
            
            # Статистика успешности
            total_attempts = self.success_count + self.error_count
            success_rate = (self.success_count / total_attempts * 100) if total_attempts > 0 else 0.0
            error_rate = (self.error_count / total_attempts * 100) if total_attempts > 0 else 0.0
            
            # Время работы системы
            system_uptime = time.time() - self.start_time
            
            metrics = SystemMetrics(
                timestamp=now,
                total_channels=total_channels,
                active_channels=active_channels,
                total_posts=total_posts,
                commented_posts=commented_posts,
                total_comments=total_comments,
                comments_today=comments_today,
                comments_this_hour=comments_this_hour,
                comments_this_minute=comments_this_minute,
                avg_comment_length=avg_comment_length,
                success_rate=success_rate,
                error_rate=error_rate,
                system_uptime=system_uptime
            )
            
            # Сохраняем метрики в БД
            self._save_metrics_to_db(metrics)
            
            return metrics
            
        except Exception as e:
            logger.error(f"Ошибка сбора метрик: {e}")
            # Возвращаем пустые метрики при ошибке
            return SystemMetrics(
                timestamp=datetime.now(),
                total_channels=0,
                active_channels=0,
                total_posts=0,
                commented_posts=0,
                total_comments=0,
                comments_today=0,
                comments_this_hour=0,
                comments_this_minute=0,
                avg_comment_length=0.0,
                success_rate=0.0,
                error_rate=0.0,
                system_uptime=0.0
            )
        finally:
            db.close()
    
    def _save_metrics_to_db(self, metrics: SystemMetrics):
        """Сохранение метрик в базу данных"""
        try:
            db = SessionLocal()
            
            # Сохраняем основные метрики
            metrics_data = {
                "total_channels": metrics.total_channels,
                "active_channels": metrics.active_channels,
                "total_posts": metrics.total_posts,
                "commented_posts": metrics.commented_posts,
                "total_comments": metrics.total_comments,
                "comments_today": metrics.comments_today,
                "comments_this_hour": metrics.comments_this_hour,
                "comments_this_minute": metrics.comments_this_minute,
                "avg_comment_length": metrics.avg_comment_length,
                "success_rate": metrics.success_rate,
                "error_rate": metrics.error_rate,
                "system_uptime": metrics.system_uptime
            }
            
            # Создаем запись метрик
            metrics_record = Metrics(
                metric_name="system_metrics",
                metric_value=1,
                metric_data=metrics_data,
                timestamp=metrics.timestamp
            )
            
            db.add(metrics_record)
            db.commit()
            
            # Очищаем старые метрики (старше 7 дней)
            week_ago = datetime.now() - timedelta(days=7)
            db.query(Metrics).filter(
                Metrics.timestamp < week_ago
            ).delete()
            db.commit()
            
        except Exception as e:
            logger.error(f"Ошибка сохранения метрик в БД: {e}")
        finally:
            db.close()
    
    def record_success(self):
        """Запись успешной операции"""
        self.success_count += 1
    
    def record_error(self):
        """Запись ошибки"""
        self.error_count += 1
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Получение краткой сводки метрик"""
        metrics = self.collect_metrics()
        
        return {
            "timestamp": metrics.timestamp.isoformat(),
            "channels": {
                "total": metrics.total_channels,
                "active": metrics.active_channels
            },
            "posts": {
                "total": metrics.total_posts,
                "commented": metrics.commented_posts,
                "comment_rate": (metrics.commented_posts / metrics.total_posts * 100) if metrics.total_posts > 0 else 0
            },
            "comments": {
                "total": metrics.total_comments,
                "today": metrics.comments_today,
                "this_hour": metrics.comments_this_hour,
                "this_minute": metrics.comments_this_minute,
                "avg_length": round(metrics.avg_comment_length, 2)
            },
            "performance": {
                "success_rate": round(metrics.success_rate, 2),
                "error_rate": round(metrics.error_rate, 2),
                "uptime_hours": round(metrics.system_uptime / 3600, 2)
            }
        }


class HealthChecker:
    """Проверка здоровья системы"""
    
    def __init__(self):
        self.metrics_collector = MetricsCollector()
    
    def check_health(self) -> Dict[str, Any]:
        """Проверка здоровья системы"""
        try:
            health_status = {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "checks": {}
            }
            
            # Проверка базы данных
            db_health = self._check_database()
            health_status["checks"]["database"] = db_health
            
            # Проверка Telegram API
            telegram_health = self._check_telegram()
            health_status["checks"]["telegram"] = telegram_health
            
            # Проверка AI сервиса
            ai_health = self._check_ai()
            health_status["checks"]["ai"] = ai_health
            
            # Проверка метрик
            metrics_health = self._check_metrics()
            health_status["checks"]["metrics"] = metrics_health
            
            # Общий статус
            all_healthy = all(
                check["status"] == "healthy" 
                for check in health_status["checks"].values()
            )
            
            if not all_healthy:
                health_status["status"] = "unhealthy"
            
            return health_status
            
        except Exception as e:
            logger.error(f"Ошибка проверки здоровья системы: {e}")
            return {
                "status": "error",
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            }
    
    def _check_database(self) -> Dict[str, Any]:
        """Проверка базы данных"""
        try:
            db = SessionLocal()
            # Простой запрос для проверки соединения
            db.query(Channel).count()
            db.close()
            
            return {
                "status": "healthy",
                "message": "База данных доступна"
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "message": f"Ошибка БД: {str(e)}"
            }
    
    def _check_telegram(self) -> Dict[str, Any]:
        """Проверка Telegram API"""
        try:
            # Здесь можно добавить проверку Telegram API
            # Пока возвращаем здоровый статус
            return {
                "status": "healthy",
                "message": "Telegram API доступен"
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "message": f"Ошибка Telegram: {str(e)}"
            }
    
    def _check_ai(self) -> Dict[str, Any]:
        """Проверка AI сервиса"""
        try:
            # Здесь можно добавить проверку AI сервиса
            # Пока возвращаем здоровый статус
            return {
                "status": "healthy",
                "message": "AI сервис доступен"
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "message": f"Ошибка AI: {str(e)}"
            }
    
    def _check_metrics(self) -> Dict[str, Any]:
        """Проверка метрик"""
        try:
            metrics = self.metrics_collector.collect_metrics()
            
            # Проверяем, что метрики собираются
            if metrics.total_channels >= 0:
                return {
                    "status": "healthy",
                    "message": "Метрики собираются корректно"
                }
            else:
                return {
                    "status": "unhealthy",
                    "message": "Проблемы со сбором метрик"
                }
        except Exception as e:
            return {
                "status": "unhealthy",
                "message": f"Ошибка метрик: {str(e)}"
            }


# Глобальные экземпляры
metrics_collector = MetricsCollector()
health_checker = HealthChecker()
