import asyncio
import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import json
import random

logger = logging.getLogger(__name__)

class AnalyticsEngine:
    """Движок аналитики для системы детекции краж"""
    
    def __init__(self):
        self.theft_statistics = {
            "total_thefts": 0,
            "prevented_thefts": 0,
            "average_loss_per_theft": 5000,  # рублей
            "monthly_thefts": 0,
            "thefts_by_category": {
                "electronics": 0,
                "clothing": 0,
                "cosmetics": 0,
                "other": 0
            }
        }
        
        # Статистика по магазинам
        self.store_statistics = {
            "electronics_store": {
                "name": "Магазин электроники",
                "theft_risk": "Очень высокий",
                "monthly_losses": 150000,
                "common_items": ["Смартфоны", "Наушники", "Планшеты"],
                "prevention_rate": 0.85
            },
            "clothing_store": {
                "name": "Магазин одежды", 
                "theft_risk": "Высокий",
                "monthly_losses": 80000,
                "common_items": ["Джинсы", "Футболки", "Куртки"],
                "prevention_rate": 0.75
            },
            "cosmetics_store": {
                "name": "Магазин косметики",
                "theft_risk": "Средний", 
                "monthly_losses": 40000,
                "common_items": ["Парфюм", "Крема", "Декоративная косметика"],
                "prevention_rate": 0.65
            }
        }
        
    async def get_theft_statistics(self) -> Dict:
        """Получение статистики краж"""
        try:
            # Генерация реалистичных данных
            current_month = datetime.now().month
            seasonal_factor = self._get_seasonal_factor(current_month)
            
            # Обновление статистики
            total_monthly_losses = sum(store["monthly_losses"] for store in self.store_statistics.values())
            total_monthly_losses *= seasonal_factor
            
            # Расчет предотвращенных краж
            prevented_thefts = 0
            for store in self.store_statistics.values():
                prevented_thefts += int(store["monthly_losses"] * store["prevention_rate"] * seasonal_factor / self.theft_statistics["average_loss_per_theft"])
            
            stats = {
                "current_month": {
                    "total_losses": round(total_monthly_losses, 2),
                    "prevented_losses": round(total_monthly_losses * 0.75, 2),
                    "theft_count": int(total_monthly_losses / self.theft_statistics["average_loss_per_theft"]),
                    "prevented_theft_count": prevented_thefts
                },
                "by_store": self.store_statistics,
                "by_category": {
                    "electronics": {
                        "losses": self.store_statistics["electronics_store"]["monthly_losses"] * seasonal_factor,
                        "risk_level": "Очень высокий",
                        "prevention_rate": 0.85
                    },
                    "clothing": {
                        "losses": self.store_statistics["clothing_store"]["monthly_losses"] * seasonal_factor,
                        "risk_level": "Высокий", 
                        "prevention_rate": 0.75
                    },
                    "cosmetics": {
                        "losses": self.store_statistics["cosmetics_store"]["monthly_losses"] * seasonal_factor,
                        "risk_level": "Средний",
                        "prevention_rate": 0.65
                    }
                },
                "trends": {
                    "monthly_growth": 0.05,  # 5% рост в месяц
                    "seasonal_peak": "Декабрь-Январь",
                    "most_vulnerable_hours": ["18:00-20:00", "14:00-16:00"]
                }
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Ошибка получения статистики: {e}")
            return {}
    
    async def calculate_roi(self) -> Dict:
        """Расчет ROI системы детекции краж"""
        try:
            # Параметры системы
            system_cost = 300000  # рублей за ТЦ
            monthly_maintenance = 15000  # рублей в месяц
            installation_time = 2  # недели
            
            # Статистика потерь
            stats = await self.get_theft_statistics()
            current_monthly_losses = stats["current_month"]["total_losses"]
            prevented_losses = stats["current_month"]["prevented_losses"]
            
            # Расчет ROI
            annual_savings = prevented_losses * 12
            annual_cost = system_cost + (monthly_maintenance * 12)
            roi_percentage = ((annual_savings - annual_cost) / annual_cost) * 100
            
            # Время окупаемости
            payback_months = annual_cost / (prevented_losses - monthly_maintenance)
            
            # Прогноз на 3 года
            three_year_savings = annual_savings * 3
            three_year_cost = system_cost + (monthly_maintenance * 36)
            three_year_roi = ((three_year_savings - three_year_cost) / three_year_cost) * 100
            
            roi_data = {
                "system_investment": {
                    "initial_cost": system_cost,
                    "monthly_maintenance": monthly_maintenance,
                    "installation_time_weeks": installation_time
                },
                "current_situation": {
                    "monthly_losses": round(current_monthly_losses, 2),
                    "prevented_losses": round(prevented_losses, 2),
                    "loss_reduction_percentage": round((prevented_losses / current_monthly_losses) * 100, 1)
                },
                "roi_analysis": {
                    "annual_savings": round(annual_savings, 2),
                    "annual_cost": round(annual_cost, 2),
                    "roi_percentage": round(roi_percentage, 1),
                    "payback_months": round(payback_months, 1),
                    "three_year_roi": round(three_year_roi, 1)
                },
                "breakdown_by_store": {
                    store_id: {
                        "name": store["name"],
                        "monthly_savings": round(store["monthly_losses"] * store["prevention_rate"], 2),
                        "annual_savings": round(store["monthly_losses"] * store["prevention_rate"] * 12, 2)
                    }
                    for store_id, store in self.store_statistics.items()
                }
            }
            
            return roi_data
            
        except Exception as e:
            logger.error(f"Ошибка расчета ROI: {e}")
            return {}
    
    async def get_priority_zones(self) -> List[Dict]:
        """Получение приоритетных зон для мониторинга"""
        try:
            zones = [
                {
                    "id": "electronics_zone",
                    "name": "Зона электроники",
                    "priority": "Критическая",
                    "risk_score": 0.95,
                    "recommended_cameras": 6,
                    "coverage_area": "100 кв.м",
                    "common_theft_items": ["Смартфоны", "Наушники", "Планшеты"],
                    "peak_hours": ["18:00-20:00", "14:00-16:00"],
                    "monthly_losses": 150000
                },
                {
                    "id": "clothing_zone", 
                    "name": "Зона одежды",
                    "priority": "Высокая",
                    "risk_score": 0.85,
                    "recommended_cameras": 4,
                    "coverage_area": "150 кв.м",
                    "common_theft_items": ["Джинсы", "Футболки", "Куртки"],
                    "peak_hours": ["16:00-18:00", "12:00-14:00"],
                    "monthly_losses": 80000
                },
                {
                    "id": "cosmetics_zone",
                    "name": "Зона косметики", 
                    "priority": "Средняя",
                    "risk_score": 0.65,
                    "recommended_cameras": 3,
                    "coverage_area": "80 кв.м",
                    "common_theft_items": ["Парфюм", "Крема", "Декоративная косметика"],
                    "peak_hours": ["15:00-17:00", "11:00-13:00"],
                    "monthly_losses": 40000
                },
                {
                    "id": "exit_zones",
                    "name": "Зоны выходов",
                    "priority": "Высокая", 
                    "risk_score": 0.90,
                    "recommended_cameras": 8,
                    "coverage_area": "200 кв.м",
                    "common_theft_items": ["Все категории"],
                    "peak_hours": ["Весь день"],
                    "monthly_losses": 100000
                }
            ]
            
            return zones
            
        except Exception as e:
            logger.error(f"Ошибка получения приоритетных зон: {e}")
            return []
    
    async def get_detection_performance(self) -> Dict:
        """Получение производительности системы детекции"""
        try:
            # Симуляция данных производительности
            performance_data = {
                "accuracy": {
                    "overall": 0.87,
                    "suspicious_behavior": 0.82,
                    "package_opening": 0.91,
                    "exit_movement": 0.85
                },
                "false_positives": {
                    "daily_average": 3.2,
                    "reduction_rate": 0.15  # 15% снижение за месяц
                },
                "response_time": {
                    "average_seconds": 2.3,
                    "target_seconds": 3.0,
                    "improvement": 0.23  # 23% улучшение
                },
                "coverage": {
                    "total_area": "530 кв.м",
                    "monitored_area": "480 кв.м", 
                    "coverage_percentage": 90.6
                },
                "alerts": {
                    "daily_average": 12.5,
                    "confirmed_thefts": 8.2,
                    "prevention_rate": 0.66
                }
            }
            
            return performance_data
            
        except Exception as e:
            logger.error(f"Ошибка получения производительности: {e}")
            return {}
    
    async def generate_monthly_report(self) -> Dict:
        """Генерация месячного отчета"""
        try:
            stats = await self.get_theft_statistics()
            roi_data = await self.calculate_roi()
            performance = await self.get_detection_performance()
            
            report = {
                "report_period": f"{datetime.now().strftime('%B %Y')}",
                "executive_summary": {
                    "total_savings": roi_data["roi_analysis"]["annual_savings"],
                    "roi_percentage": roi_data["roi_analysis"]["roi_percentage"],
                    "prevented_thefts": stats["current_month"]["prevented_theft_count"],
                    "system_performance": performance["accuracy"]["overall"]
                },
                "detailed_analysis": {
                    "theft_statistics": stats,
                    "roi_analysis": roi_data,
                    "performance_metrics": performance
                },
                "recommendations": [
                    "Увеличить количество камер в зоне электроники",
                    "Оптимизировать алгоритмы детекции для снижения ложных срабатываний",
                    "Расширить зону покрытия на 10%",
                    "Внедрить дополнительные датчики движения"
                ],
                "next_month_goals": {
                    "target_accuracy": 0.90,
                    "target_false_positive_reduction": 0.20,
                    "target_coverage": 0.95
                }
            }
            
            return report
            
        except Exception as e:
            logger.error(f"Ошибка генерации отчета: {e}")
            return {}
    
    def _get_seasonal_factor(self, month: int) -> float:
        """Получение сезонного коэффициента"""
        seasonal_factors = {
            1: 1.3,   # Январь - после праздников
            2: 0.9,   # Февраль
            3: 0.8,   # Март
            4: 0.9,   # Апрель
            5: 1.0,   # Май
            6: 1.1,   # Июнь - начало лета
            7: 1.2,   # Июль - отпуска
            8: 1.1,   # Август
            9: 1.0,   # Сентябрь
            10: 1.1,  # Октябрь
            11: 1.2,  # Ноябрь
            12: 1.4   # Декабрь - праздники
        }
        return seasonal_factors.get(month, 1.0)
    
    async def get_real_time_alerts(self) -> List[Dict]:
        """Получение real-time уведомлений"""
        try:
            # Симуляция real-time уведомлений
            alerts = [
                {
                    "id": "alert_001",
                    "timestamp": datetime.now().isoformat(),
                    "type": "suspicious_behavior",
                    "location": "electronics_zone",
                    "severity": "high",
                    "description": "Обнаружено подозрительное поведение в зоне электроники",
                    "confidence": 0.87,
                    "action_required": True
                },
                {
                    "id": "alert_002", 
                    "timestamp": (datetime.now() - timedelta(minutes=5)).isoformat(),
                    "type": "package_opening",
                    "location": "clothing_zone",
                    "severity": "medium",
                    "description": "Возможное вскрытие упаковки в зоне одежды",
                    "confidence": 0.73,
                    "action_required": False
                }
            ]
            
            return alerts
            
        except Exception as e:
            logger.error(f"Ошибка получения уведомлений: {e}")
            return []
