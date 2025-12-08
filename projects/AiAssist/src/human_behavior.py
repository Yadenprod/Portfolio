"""
Модуль имитации человеческого поведения
"""
import random
import time
from typing import Dict, List, Optional
import math


class HumanBehaviorSimulator:
    """Симулятор человеческого поведения для более естественной игры"""
    
    def __init__(self):
        """Инициализация симулятора"""
        self.reaction_times = []  # История времени реакции
        self.last_action_time = time.time()
        self.action_history = []
        
        # Параметры поведения
        self.avg_reaction_time = 0.3  # Среднее время реакции (секунды)
        self.reaction_variance = 0.2  # Вариативность времени реакции
        
        # Паттерны поведения
        self.behavior_patterns = {
            'cautious': {'reaction_multiplier': 1.5, 'error_rate': 0.05},
            'normal': {'reaction_multiplier': 1.0, 'error_rate': 0.1},
            'aggressive': {'reaction_multiplier': 0.7, 'error_rate': 0.15}
        }
        self.current_pattern = 'normal'
    
    def add_human_delay(self, base_delay: float = 0.0) -> float:
        """
        Добавляет человеческую задержку к действию
        
        Args:
            base_delay: Базовая задержка
            
        Returns:
            float: Итоговая задержка с человеческим фактором
        """
        pattern = self.behavior_patterns[self.current_pattern]
        multiplier = pattern['reaction_multiplier']
        
        # Нормальное распределение времени реакции
        reaction_time = random.gauss(
            self.avg_reaction_time * multiplier,
            self.reaction_variance * multiplier
        )
        
        # Минимальная задержка
        reaction_time = max(0.1, reaction_time)
        
        total_delay = base_delay + reaction_time
        self.reaction_times.append(reaction_time)
        
        # Сохраняем только последние 100 значений
        if len(self.reaction_times) > 100:
            self.reaction_times.pop(0)
        
        return total_delay
    
    def should_make_mistake(self) -> bool:
        """
        Определяет, должен ли AI сделать ошибку (для реалистичности)
        
        Returns:
            bool: True если нужно сделать ошибку
        """
        pattern = self.behavior_patterns[self.current_pattern]
        return random.random() < pattern['error_rate']
    
    def add_micro_pauses(self) -> float:
        """
        Добавляет микропаузы между действиями
        
        Returns:
            float: Длительность паузы
        """
        # Случайные короткие паузы (0.1-0.5 сек)
        pause = random.uniform(0.1, 0.5)
        return pause
    
    def random_mouse_movement(self, base_x: int, base_y: int, 
                              variance: int = 5) -> tuple:
        """
        Добавляет случайное движение мыши (имитация дрожания руки)
        
        Args:
            base_x, base_y: Базовые координаты
            variance: Разброс в пикселях
            
        Returns:
            tuple: Новые координаты с небольшим смещением
        """
        offset_x = random.randint(-variance, variance)
        offset_y = random.randint(-variance, variance)
        return (base_x + offset_x, base_y + offset_y)
    
    def add_typing_delay(self, text: str) -> List[float]:
        """
        Генерирует задержки между символами при вводе текста
        
        Args:
            text: Текст для ввода
            
        Returns:
            List[float]: Список задержек между символами
        """
        delays = []
        for char in text:
            if char == ' ':
                # Пробелы набираются быстрее
                delay = random.uniform(0.05, 0.15)
            elif char.isupper():
                # Заглавные буквы требуют больше времени (Shift)
                delay = random.uniform(0.15, 0.3)
            else:
                # Обычные символы
                delay = random.uniform(0.1, 0.25)
            
            delays.append(delay)
        
        return delays
    
    def random_look_around(self) -> Dict:
        """
        Генерирует случайное движение камеры (осмотр вокруг)
        
        Returns:
            Dict: Параметры движения камеры
        """
        # Случайный поворот камеры
        angle = random.uniform(-30, 30)  # градусы
        duration = random.uniform(0.3, 1.0)  # секунды
        
        return {
            'action': 'look_around',
            'angle': angle,
            'duration': duration
        }
    
    def should_take_break(self, work_duration: float) -> bool:
        """
        Определяет, нужно ли сделать перерыв
        
        Args:
            work_duration: Длительность работы в секундах
            
        Returns:
            bool: True если нужен перерыв
        """
        # Перерывы каждые 10-20 минут
        if work_duration > random.uniform(600, 1200):
            return random.random() < 0.3  # 30% шанс сделать перерыв
        return False
    
    def generate_idle_behavior(self) -> Dict:
        """
        Генерирует поведение во время бездействия
        
        Returns:
            Dict: Действия для бездействия
        """
        behaviors = [
            {'action': 'look_around', 'duration': random.uniform(2, 5)},
            {'action': 'check_phone', 'duration': random.uniform(3, 8)},
            {'action': 'stretch', 'duration': random.uniform(1, 2)},
            {'action': 'wait', 'duration': random.uniform(5, 15)}
        ]
        
        return random.choice(behaviors)
    
    def adjust_driving_style(self) -> Dict:
        """
        Генерирует стиль вождения (для разнообразия)
        
        Returns:
            Dict: Параметры стиля вождения
        """
        styles = {
            'careful': {
                'speed_multiplier': 0.7,
                'brake_distance': 1.5,
                'turn_smoothness': 0.9
            },
            'normal': {
                'speed_multiplier': 1.0,
                'brake_distance': 1.0,
                'turn_smoothness': 0.8
            },
            'aggressive': {
                'speed_multiplier': 1.3,
                'brake_distance': 0.7,
                'turn_smoothness': 0.6
            }
        }
        
        # Выбираем стиль на основе текущего паттерна
        style_name = self.current_pattern if self.current_pattern in styles else 'normal'
        style = styles[style_name].copy()
        
        # Добавляем случайные вариации
        style['speed_multiplier'] += random.uniform(-0.1, 0.1)
        
        return style
    
    def set_behavior_pattern(self, pattern: str):
        """
        Устанавливает паттерн поведения
        
        Args:
            pattern: Название паттерна ('cautious', 'normal', 'aggressive')
        """
        if pattern in self.behavior_patterns:
            self.current_pattern = pattern
            print(f"Паттерн поведения изменен на: {pattern}")
    
    def get_statistics(self) -> Dict:
        """
        Возвращает статистику поведения
        
        Returns:
            Dict: Статистика
        """
        avg_reaction = sum(self.reaction_times) / len(self.reaction_times) if self.reaction_times else 0
        
        return {
            'avg_reaction_time': avg_reaction,
            'total_actions': len(self.action_history),
            'current_pattern': self.current_pattern,
            'mistake_rate': self.behavior_patterns[self.current_pattern]['error_rate']
        }

