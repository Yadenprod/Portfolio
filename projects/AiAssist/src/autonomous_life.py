"""
Система автономной жизни AI - планирование дня и распорядок
"""
import random
import time
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from enum import Enum


class TimeOfDay(Enum):
    """Время суток"""
    MORNING = "morning"      # 6:00 - 12:00
    AFTERNOON = "afternoon"   # 12:00 - 18:00
    EVENING = "evening"      # 18:00 - 24:00
    NIGHT = "night"          # 0:00 - 6:00


class DailyPlan:
    """План на день для AI"""
    
    def __init__(self):
        """Инициализация плана"""
        self.current_time = datetime.now()
        self.planned_activities = []
        self.completed_activities = []
        self.daily_goals = {
            'work_hours': random.uniform(4, 8),  # Часов работы в день
            'earnings_target': random.uniform(500, 2000),  # Цель по заработку
            'exploration_time': random.uniform(1, 3),  # Часов исследования
            'social_time': random.uniform(0.5, 2),  # Часов общения
        }
        self.money_earned_today = 0
        self.work_hours_today = 0
        
    def get_time_of_day(self) -> TimeOfDay:
        """Определяет время суток"""
        hour = self.current_time.hour
        if 6 <= hour < 12:
            return TimeOfDay.MORNING
        elif 12 <= hour < 18:
            return TimeOfDay.AFTERNOON
        elif 18 <= hour < 24:
            return TimeOfDay.EVENING
        else:
            return TimeOfDay.NIGHT
    
    def should_work(self) -> bool:
        """Определяет, нужно ли работать сейчас"""
        # Проверяем цели на день
        if self.work_hours_today >= self.daily_goals['work_hours']:
            return False
        
        if self.money_earned_today >= self.daily_goals['earnings_target']:
            return False
        
        time_of_day = self.get_time_of_day()
        
        # Ночью меньше работаем
        if time_of_day == TimeOfDay.NIGHT:
            return random.random() < 0.3
        
        # Утром и днем больше работаем
        if time_of_day in [TimeOfDay.MORNING, TimeOfDay.AFTERNOON]:
            return random.random() < 0.7
        
        # Вечером средняя активность
        return random.random() < 0.5
    
    def should_rest(self) -> bool:
        """Определяет, нужно ли отдохнуть"""
        time_of_day = self.get_time_of_day()
        
        # Ночью больше отдыхаем
        if time_of_day == TimeOfDay.NIGHT:
            return random.random() < 0.6
        
        # После долгой работы
        if self.work_hours_today > 6:
            return random.random() < 0.4
        
        return random.random() < 0.1
    
    def should_explore(self) -> bool:
        """Определяет, нужно ли исследовать"""
        # Если выполнили цели по работе
        if (self.work_hours_today >= self.daily_goals['work_hours'] * 0.8 and
            self.money_earned_today >= self.daily_goals['earnings_target'] * 0.8):
            return random.random() < 0.6
        
        return random.random() < 0.2
    
    def update_work_time(self, hours: float):
        """Обновляет отработанное время"""
        self.work_hours_today += hours
    
    def update_earnings(self, amount: float):
        """Обновляет заработок"""
        self.money_earned_today += amount
    
    def reset_daily_goals(self):
        """Сбрасывает цели на новый день"""
        self.money_earned_today = 0
        self.work_hours_today = 0
        self.completed_activities = []
        self.daily_goals = {
            'work_hours': random.uniform(4, 8),
            'earnings_target': random.uniform(500, 2000),
            'exploration_time': random.uniform(1, 3),
            'social_time': random.uniform(0.5, 2),
        }
        print(f"📅 Новый день! Цели: {self.daily_goals['work_hours']:.1f}ч работы, ${self.daily_goals['earnings_target']:.0f} заработка")


class AutonomousLife:
    """Система автономной жизни AI"""
    
    def __init__(self):
        """Инициализация"""
        self.daily_plan = DailyPlan()
        self.last_activity_change = time.time()
        self.current_activity_duration = 0
        self.activity_history = []
        self.needs_break = False
        self.break_start_time = None
        
    def decide_next_activity(self, game_state: Dict) -> Dict:
        """
        Принимает решение о следующей активности
        
        Args:
            game_state: Текущее состояние игры
            
        Returns:
            Dict: Решение о активности
        """
        # Проверка на необходимость перерыва
        if self.needs_break:
            if self.break_start_time is None:
                self.break_start_time = time.time()
                break_duration = random.uniform(300, 900)  # 5-15 минут
                return {
                    'activity': 'rest',
                    'duration': break_duration,
                    'reason': 'scheduled_break'
                }
            elif time.time() - self.break_start_time < 300:
                return {
                    'activity': 'rest',
                    'duration': 60,
                    'reason': 'in_break'
                }
            else:
                # Перерыв закончился
                self.needs_break = False
                self.break_start_time = None
        
        # Проверка здоровья
        health = game_state.get('health', 100)
        if health < 30:
            return {
                'activity': 'find_hospital',
                'priority': 'high',
                'reason': 'low_health'
            }
        
        # Проверка плана на день
        if self.daily_plan.should_work():
            return {
                'activity': 'work',
                'priority': 'normal',
                'reason': 'daily_plan'
            }
        
        if self.daily_plan.should_rest():
            return {
                'activity': 'rest',
                'duration': random.uniform(600, 1800),  # 10-30 минут
                'reason': 'scheduled_rest'
            }
        
        if self.daily_plan.should_explore():
            return {
                'activity': 'explore',
                'duration': random.uniform(600, 1800),
                'reason': 'leisure'
            }
        
        # По умолчанию - свободное время
        activities = ['walk_around', 'drive_around', 'socialize', 'shop']
        return {
            'activity': random.choice(activities),
            'duration': random.uniform(300, 900),
            'reason': 'free_time'
        }
    
    def should_take_break(self, work_duration: float) -> bool:
        """
        Определяет, нужно ли сделать перерыв
        
        Args:
            work_duration: Длительность работы в секундах
            
        Returns:
            bool: True если нужен перерыв
        """
        # Перерывы каждые 1-2 часа работы
        if work_duration > random.uniform(3600, 7200):
            return True
        
        # Случайные перерывы
        if random.random() < 0.1:  # 10% шанс
            return True
        
        return False
    
    def schedule_break(self):
        """Планирует перерыв"""
        self.needs_break = True
        print("⏸ Запланирован перерыв...")
    
    def update_activity(self, activity: str, duration: float):
        """Обновляет историю активности"""
        self.activity_history.append({
            'activity': activity,
            'duration': duration,
            'timestamp': time.time()
        })
        
        # Храним только последние 100 записей
        if len(self.activity_history) > 100:
            self.activity_history.pop(0)
    
    def get_daily_statistics(self) -> Dict:
        """Возвращает статистику за день"""
        return {
            'work_hours': self.daily_plan.work_hours_today,
            'earnings': self.daily_plan.money_earned_today,
            'earnings_target': self.daily_plan.daily_goals['earnings_target'],
            'work_target': self.daily_plan.daily_goals['work_hours'],
            'activities_count': len(self.activity_history)
        }

