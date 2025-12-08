import asyncio
import logging
from typing import Dict, List, Optional
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Менеджер базы данных для системы детекции краж"""
    
    def __init__(self):
        self.is_initialized = False
        self.data_storage = {
            "theft_events": [],
            "detection_logs": [],
            "alerts": [],
            "performance_metrics": [],
            "store_configurations": []
        }
        
    async def initialize(self):
        """Инициализация базы данных"""
        try:
            logger.info("🔧 Инициализация базы данных...")
            
            # Создание начальных данных
            await self._create_initial_data()
            
            self.is_initialized = True
            logger.info("✅ База данных инициализирована")
            
        except Exception as e:
            logger.error(f"Ошибка инициализации БД: {e}")
            raise
    
    async def _create_initial_data(self):
        """Создание начальных данных"""
        # Конфигурации магазинов
        self.data_storage["store_configurations"] = [
            {
                "id": "electronics_store",
                "name": "Магазин электроники",
                "category": "Электроника",
                "theft_risk": "Очень высокий",
                "cameras": [
                    {"id": "cam_1", "location": "entrance", "status": "active"},
                    {"id": "cam_2", "location": "display_area", "status": "active"},
                    {"id": "cam_3", "location": "cashier", "status": "active"},
                    {"id": "cam_4", "location": "storage", "status": "active"}
                ],
                "exit_zones": [
                    {"id": "exit_1", "x": 0.8, "y": 0.5, "width": 0.2, "height": 0.3}
                ]
            },
            {
                "id": "clothing_store", 
                "name": "Магазин одежды",
                "category": "Одежда",
                "theft_risk": "Высокий",
                "cameras": [
                    {"id": "cam_5", "location": "entrance", "status": "active"},
                    {"id": "cam_6", "location": "fitting_rooms", "status": "active"},
                    {"id": "cam_7", "location": "cashier", "status": "active"}
                ],
                "exit_zones": [
                    {"id": "exit_2", "x": 0.7, "y": 0.6, "width": 0.3, "height": 0.2}
                ]
            },
            {
                "id": "cosmetics_store",
                "name": "Магазин косметики", 
                "category": "Косметика",
                "theft_risk": "Средний",
                "cameras": [
                    {"id": "cam_8", "location": "entrance", "status": "active"},
                    {"id": "cam_9", "location": "perfume_section", "status": "active"},
                    {"id": "cam_10", "location": "cashier", "status": "active"}
                ],
                "exit_zones": [
                    {"id": "exit_3", "x": 0.6, "y": 0.7, "width": 0.4, "height": 0.2}
                ]
            }
        ]
        
        # Начальные метрики производительности
        self.data_storage["performance_metrics"] = [
            {
                "id": "perf_001",
                "timestamp": datetime.now().isoformat(),
                "accuracy": 0.87,
                "false_positives": 3.2,
                "response_time": 2.3,
                "coverage_percentage": 90.6
            }
        ]
    
    async def save_theft_event(self, event_data: Dict) -> str:
        """Сохранение события кражи"""
        try:
            event_id = f"theft_{len(self.data_storage['theft_events']) + 1:04d}"
            event = {
                "id": event_id,
                "timestamp": datetime.now().isoformat(),
                "store_id": event_data.get("store_id"),
                "location": event_data.get("location"),
                "event_type": event_data.get("event_type"),
                "severity": event_data.get("severity", "medium"),
                "confidence": event_data.get("confidence", 0.0),
                "description": event_data.get("description"),
                "prevented": event_data.get("prevented", False),
                "estimated_loss": event_data.get("estimated_loss", 0),
                "details": event_data.get("details", {})
            }
            
            self.data_storage["theft_events"].append(event)
            logger.info(f"Сохранено событие кражи: {event_id}")
            
            return event_id
            
        except Exception as e:
            logger.error(f"Ошибка сохранения события кражи: {e}")
            raise
    
    async def save_detection_log(self, log_data: Dict) -> str:
        """Сохранение лога детекции"""
        try:
            log_id = f"detection_{len(self.data_storage['detection_logs']) + 1:04d}"
            log = {
                "id": log_id,
                "timestamp": datetime.now().isoformat(),
                "camera_id": log_data.get("camera_id"),
                "store_id": log_data.get("store_id"),
                "detection_type": log_data.get("detection_type"),
                "confidence": log_data.get("confidence", 0.0),
                "frame_data": log_data.get("frame_data", {}),
                "processed": log_data.get("processed", False)
            }
            
            self.data_storage["detection_logs"].append(log)
            
            return log_id
            
        except Exception as e:
            logger.error(f"Ошибка сохранения лога детекции: {e}")
            raise
    
    async def save_alert(self, alert_data: Dict) -> str:
        """Сохранение уведомления"""
        try:
            alert_id = f"alert_{len(self.data_storage['alerts']) + 1:04d}"
            alert = {
                "id": alert_id,
                "timestamp": datetime.now().isoformat(),
                "type": alert_data.get("type"),
                "severity": alert_data.get("severity", "medium"),
                "location": alert_data.get("location"),
                "description": alert_data.get("description"),
                "confidence": alert_data.get("confidence", 0.0),
                "action_required": alert_data.get("action_required", False),
                "acknowledged": False,
                "resolved": False
            }
            
            self.data_storage["alerts"].append(alert)
            logger.info(f"Сохранено уведомление: {alert_id}")
            
            return alert_id
            
        except Exception as e:
            logger.error(f"Ошибка сохранения уведомления: {e}")
            raise
    
    async def get_theft_events(self, 
                             store_id: Optional[str] = None,
                             start_date: Optional[str] = None,
                             end_date: Optional[str] = None,
                             limit: int = 100) -> List[Dict]:
        """Получение событий краж"""
        try:
            events = self.data_storage["theft_events"].copy()
            
            # Фильтрация по магазину
            if store_id:
                events = [e for e in events if e.get("store_id") == store_id]
            
            # Фильтрация по дате
            if start_date:
                events = [e for e in events if e["timestamp"] >= start_date]
            if end_date:
                events = [e for e in events if e["timestamp"] <= end_date]
            
            # Сортировка по времени (новые сначала)
            events.sort(key=lambda x: x["timestamp"], reverse=True)
            
            return events[:limit]
            
        except Exception as e:
            logger.error(f"Ошибка получения событий краж: {e}")
            return []
    
    async def get_alerts(self, 
                        severity: Optional[str] = None,
                        acknowledged: Optional[bool] = None,
                        limit: int = 50) -> List[Dict]:
        """Получение уведомлений"""
        try:
            alerts = self.data_storage["alerts"].copy()
            
            # Фильтрация по серьезности
            if severity:
                alerts = [a for a in alerts if a.get("severity") == severity]
            
            # Фильтрация по статусу подтверждения
            if acknowledged is not None:
                alerts = [a for a in alerts if a.get("acknowledged") == acknowledged]
            
            # Сортировка по времени
            alerts.sort(key=lambda x: x["timestamp"], reverse=True)
            
            return alerts[:limit]
            
        except Exception as e:
            logger.error(f"Ошибка получения уведомлений: {e}")
            return []
    
    async def get_store_configuration(self, store_id: str) -> Optional[Dict]:
        """Получение конфигурации магазина"""
        try:
            for store in self.data_storage["store_configurations"]:
                if store["id"] == store_id:
                    return store
            return None
            
        except Exception as e:
            logger.error(f"Ошибка получения конфигурации магазина: {e}")
            return None
    
    async def update_store_configuration(self, store_id: str, config_data: Dict) -> bool:
        """Обновление конфигурации магазина"""
        try:
            for i, store in enumerate(self.data_storage["store_configurations"]):
                if store["id"] == store_id:
                    self.data_storage["store_configurations"][i].update(config_data)
                    logger.info(f"Обновлена конфигурация магазина: {store_id}")
                    return True
            return False
            
        except Exception as e:
            logger.error(f"Ошибка обновления конфигурации магазина: {e}")
            return False
    
    async def get_performance_metrics(self, 
                                    start_date: Optional[str] = None,
                                    end_date: Optional[str] = None) -> List[Dict]:
        """Получение метрик производительности"""
        try:
            metrics = self.data_storage["performance_metrics"].copy()
            
            # Фильтрация по дате
            if start_date:
                metrics = [m for m in metrics if m["timestamp"] >= start_date]
            if end_date:
                metrics = [m for m in metrics if m["timestamp"] <= end_date]
            
            # Сортировка по времени
            metrics.sort(key=lambda x: x["timestamp"], reverse=True)
            
            return metrics
            
        except Exception as e:
            logger.error(f"Ошибка получения метрик производительности: {e}")
            return []
    
    async def save_performance_metrics(self, metrics_data: Dict) -> str:
        """Сохранение метрик производительности"""
        try:
            metric_id = f"perf_{len(self.data_storage['performance_metrics']) + 1:04d}"
            metric = {
                "id": metric_id,
                "timestamp": datetime.now().isoformat(),
                "accuracy": metrics_data.get("accuracy", 0.0),
                "false_positives": metrics_data.get("false_positives", 0.0),
                "response_time": metrics_data.get("response_time", 0.0),
                "coverage_percentage": metrics_data.get("coverage_percentage", 0.0),
                "additional_metrics": metrics_data.get("additional_metrics", {})
            }
            
            self.data_storage["performance_metrics"].append(metric)
            
            return metric_id
            
        except Exception as e:
            logger.error(f"Ошибка сохранения метрик производительности: {e}")
            raise
    
    async def acknowledge_alert(self, alert_id: str) -> bool:
        """Подтверждение уведомления"""
        try:
            for alert in self.data_storage["alerts"]:
                if alert["id"] == alert_id:
                    alert["acknowledged"] = True
                    alert["acknowledged_at"] = datetime.now().isoformat()
                    logger.info(f"Подтверждено уведомление: {alert_id}")
                    return True
            return False
            
        except Exception as e:
            logger.error(f"Ошибка подтверждения уведомления: {e}")
            return False
    
    async def resolve_alert(self, alert_id: str, resolution_notes: str = "") -> bool:
        """Разрешение уведомления"""
        try:
            for alert in self.data_storage["alerts"]:
                if alert["id"] == alert_id:
                    alert["resolved"] = True
                    alert["resolved_at"] = datetime.now().isoformat()
                    alert["resolution_notes"] = resolution_notes
                    logger.info(f"Разрешено уведомление: {alert_id}")
                    return True
            return False
            
        except Exception as e:
            logger.error(f"Ошибка разрешения уведомления: {e}")
            return False
    
    async def get_statistics_summary(self) -> Dict:
        """Получение сводной статистики"""
        try:
            total_thefts = len(self.data_storage["theft_events"])
            prevented_thefts = len([e for e in self.data_storage["theft_events"] if e.get("prevented")])
            total_alerts = len(self.data_storage["alerts"])
            active_alerts = len([a for a in self.data_storage["alerts"] if not a.get("resolved")])
            
            # Расчет средних потерь
            total_losses = sum(e.get("estimated_loss", 0) for e in self.data_storage["theft_events"])
            prevented_losses = sum(e.get("estimated_loss", 0) for e in self.data_storage["theft_events"] if e.get("prevented"))
            
            summary = {
                "total_theft_events": total_thefts,
                "prevented_thefts": prevented_thefts,
                "prevention_rate": round(prevented_thefts / max(total_thefts, 1) * 100, 1),
                "total_alerts": total_alerts,
                "active_alerts": active_alerts,
                "total_losses": total_losses,
                "prevented_losses": prevented_losses,
                "savings_percentage": round(prevented_losses / max(total_losses, 1) * 100, 1),
                "stores_configured": len(self.data_storage["store_configurations"])
            }
            
            return summary
            
        except Exception as e:
            logger.error(f"Ошибка получения сводной статистики: {e}")
            return {}
    
    async def backup_data(self) -> Dict:
        """Резервное копирование данных"""
        try:
            backup = {
                "timestamp": datetime.now().isoformat(),
                "data": self.data_storage.copy()
            }
            
            # В реальной системе здесь было бы сохранение в файл или облако
            logger.info("Резервная копия данных создана")
            
            return backup
            
        except Exception as e:
            logger.error(f"Ошибка создания резервной копии: {e}")
            raise
