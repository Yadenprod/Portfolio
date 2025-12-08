"""
Система автоматического восстановления после ошибок
"""
import time
import random
from typing import Dict, Optional, List


class AutoRecovery:
    """Система автоматического восстановления"""
    
    def __init__(self):
        """Инициализация"""
        self.error_count = 0
        self.last_error_time = None
        self.recovery_attempts = []
        self.stuck_detection = {
            'last_position': None,
            'position_count': 0,
            'stuck_threshold': 10  # Кадров на одном месте
        }
        self.death_count = 0
        self.last_death_time = None
    
    def detect_stuck(self, current_position: Optional[tuple], 
                     minimap_data: Dict) -> bool:
        """
        Определяет, застрял ли AI
        
        Args:
            current_position: Текущая позиция
            minimap_data: Данные с мини-карты
            
        Returns:
            bool: True если застрял
        """
        if current_position is None:
            return False
        
        if self.stuck_detection['last_position'] == current_position:
            self.stuck_detection['position_count'] += 1
        else:
            self.stuck_detection['last_position'] = current_position
            self.stuck_detection['position_count'] = 0
        
        # Если на одном месте больше порога - застрял
        if self.stuck_detection['position_count'] > self.stuck_detection['stuck_threshold']:
            return True
        
        return False
    
    def handle_stuck(self) -> Dict:
        """
        Обрабатывает ситуацию застревания
        
        Returns:
            Dict: Действия для выхода из застревания
        """
        self.error_count += 1
        print(f"⚠️ Обнаружено застревание! Попытка восстановления #{self.error_count}")
        
        recovery_actions = [
            {'action': 'move_backward', 'duration': 2.0},
            {'action': 'jump', 'count': 3},
            {'action': 'turn_around', 'angle': 180},
            {'action': 'random_movement', 'duration': 3.0},
        ]
        
        # Выбираем случайную стратегию восстановления
        strategy = random.choice(recovery_actions)
        
        return {
            'recovery_action': strategy,
            'reason': 'stuck'
        }
    
    def detect_death(self, health: float, text: str) -> bool:
        """
        Определяет, умер ли персонаж
        
        Args:
            health: Уровень здоровья
            text: Распознанный текст
            
        Returns:
            bool: True если умер
        """
        text_lower = text.lower()
        death_keywords = ['умер', 'died', 'death', 'respawning', 'респавн']
        
        if health <= 0 or any(keyword in text_lower for keyword in death_keywords):
            if self.last_death_time is None or time.time() - self.last_death_time > 10:
                self.death_count += 1
                self.last_death_time = time.time()
                return True
        
        return False
    
    def handle_death(self) -> Dict:
        """
        Обрабатывает смерть персонажа
        
        Returns:
            Dict: Действия после смерти
        """
        print(f"💀 Обнаружена смерть персонажа! Восстановление...")
        
        return {
            'recovery_action': {
                'action': 'wait_respawn',
                'duration': random.uniform(5, 10)
            },
            'reason': 'death',
            'next_action': 'find_safe_location'
        }
    
    def detect_error_state(self, game_state: Dict, vision_data: Dict) -> Optional[Dict]:
        """
        Определяет ошибочное состояние
        
        Args:
            game_state: Состояние игры
            vision_data: Данные зрения
            
        Returns:
            Optional[Dict]: Информация об ошибке или None
        """
        # Проверка застревания
        minimap_data = vision_data.get('minimap_data', {})
        player_pos = minimap_data.get('player_position')
        
        if self.detect_stuck(player_pos, minimap_data):
            return self.handle_stuck()
        
        # Проверка смерти
        health = game_state.get('health', 100)
        text = vision_data.get('text', '')
        
        if self.detect_death(health, text):
            return self.handle_death()
        
        # Проверка других ошибок
        if health < 20 and game_state.get('in_vehicle', False):
            # Низкое здоровье в транспорте - нужно остановиться
            return {
                'recovery_action': {
                    'action': 'stop_vehicle',
                    'reason': 'low_health'
                }
            }
        
        return None
    
    def get_recovery_strategy(self, error_type: str) -> List[Dict]:
        """
        Возвращает стратегию восстановления
        
        Args:
            error_type: Тип ошибки
            
        Returns:
            List[Dict]: Список действий для восстановления
        """
        strategies = {
            'stuck': [
                {'action': 'move_backward', 'duration': 2.0},
                {'action': 'turn_left', 'angle': 90},
                {'action': 'move_forward', 'duration': 3.0},
            ],
            'death': [
                {'action': 'wait', 'duration': 10},
                {'action': 'check_health'},
                {'action': 'find_safe_location'},
            ],
            'low_health': [
                {'action': 'stop_current_action'},
                {'action': 'find_hospital'},
                {'action': 'heal'},
            ],
            'no_response': [
                {'action': 'press_escape'},
                {'action': 'wait', 'duration': 2},
                {'action': 'resume'},
            ]
        }
        
        return strategies.get(error_type, [{'action': 'wait', 'duration': 5}])
    
    def reset_error_count(self):
        """Сбрасывает счетчик ошибок"""
        self.error_count = 0
        self.stuck_detection['position_count'] = 0

