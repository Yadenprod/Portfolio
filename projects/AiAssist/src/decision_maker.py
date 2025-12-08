"""
Модуль для принятия решений AI
"""
import numpy as np
from typing import Dict, Optional, Tuple
from enum import Enum


class Action(Enum):
    """Доступные действия"""
    MOVE_FORWARD = "move_forward"
    MOVE_BACKWARD = "move_backward"
    TURN_LEFT = "turn_left"
    TURN_RIGHT = "turn_right"
    JUMP = "jump"
    INTERACT = "interact"
    ATTACK = "attack"
    DEFEND = "defend"
    IDLE = "idle"
    FOLLOW_ROAD = "follow_road"
    AVOID_OBSTACLE = "avoid_obstacle"


class DecisionMaker:
    """Класс для принятия решений на основе состояния игры"""
    
    def __init__(self):
        """Инициализация системы принятия решений"""
        self.current_state = {}
        self.last_action = Action.IDLE
    
    def analyze_state(self, vision_data: Dict, game_state: Dict) -> Dict:
        """
        Анализирует текущее состояние игры
        
        Args:
            vision_data: Данные от модуля зрения
            game_state: Дополнительное состояние игры
            
        Returns:
            Dict: Проанализированное состояние
        """
        state = {
            'health': game_state.get('health', 100),
            'has_enemies': vision_data.get('has_enemies', False),
            'has_obstacles': vision_data.get('has_obstacles', False),
            'on_road': vision_data.get('on_road', False),
            'near_object': vision_data.get('near_object', False),
            'text_detected': vision_data.get('text', ''),
        }
        
        self.current_state = state
        return state
    
    def decide_action(self, state: Dict) -> Tuple[Action, Dict]:
        """
        Принимает решение о следующем действии
        
        Args:
            state: Текущее состояние игры
            
        Returns:
            Tuple[Action, Dict]: Выбранное действие и параметры
        """
        # Простая логика принятия решений
        # В реальной системе здесь будет нейронная сеть или более сложная логика
        
        # Если низкое здоровье - защита
        if state.get('health', 100) < 30:
            return Action.DEFEND, {'duration': 2.0}
        
        # Если есть враги - атака
        if state.get('has_enemies', False):
            return Action.ATTACK, {'target': 'nearest'}
        
        # Если есть препятствия - обход
        if state.get('has_obstacles', False):
            return Action.AVOID_OBSTACLE, {'direction': 'right'}
        
        # Если на дороге - следовать по дороге
        if state.get('on_road', False):
            return Action.FOLLOW_ROAD, {'speed': 'normal'}
        
        # Если рядом объект - взаимодействие
        if state.get('near_object', False):
            return Action.INTERACT, {}
        
        # По умолчанию - движение вперед
        return Action.MOVE_FORWARD, {'duration': 1.0}
    
    def process_text(self, text: str) -> Optional[Action]:
        """
        Обрабатывает распознанный текст и возвращает действие
        
        Args:
            text: Распознанный текст
            
        Returns:
            Optional[Action]: Действие на основе текста или None
        """
        text_lower = text.lower()
        
        # Примеры обработки текста из интерфейса
        if 'умер' in text_lower or 'died' in text_lower:
            return Action.IDLE
        
        if 'взаимодействие' in text_lower or 'interact' in text_lower:
            return Action.INTERACT
        
        if 'опасность' in text_lower or 'danger' in text_lower:
            return Action.DEFEND
        
        return None
    
    def update_strategy(self, success_rate: float):
        """
        Обновляет стратегию на основе успешности
        
        Args:
            success_rate: Процент успешных действий (0-1)
        """
        # Здесь можно реализовать обучение с подкреплением
        pass

