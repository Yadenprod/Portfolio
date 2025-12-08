"""
Система состояний (State Machine) для управления поведением AI
"""
from enum import Enum
from typing import Dict, Optional, Callable
import random
import time


class GameState(Enum):
    """Основные состояния игры"""
    IDLE = "idle"  # Бездействие
    WALKING = "walking"  # Пешком
    DRIVING = "driving"  # За рулем
    WORKING = "working"  # Работа
    SHOPPING = "shopping"  # Покупки
    SOCIALIZING = "socializing"  # Общение
    EXPLORING = "exploring"  # Исследование города
    RESTING = "resting"  # Отдых
    EMERGENCY = "emergency"  # Экстренная ситуация


class StateMachine:
    """Конечный автомат состояний для управления поведением AI"""
    
    def __init__(self):
        """Инициализация state machine"""
        self.current_state = GameState.IDLE
        self.previous_state = None
        self.state_start_time = time.time()
        self.state_duration = 0
        self.transitions = {}  # Правила переходов между состояниями
        self.state_handlers = {}  # Обработчики состояний
        
        # Настройка переходов
        self._setup_transitions()
        
        # Счетчики активности
        self.work_sessions = 0
        self.driving_time = 0
        self.walking_time = 0
    
    def _setup_transitions(self):
        """Настройка возможных переходов между состояниями"""
        self.transitions = {
            GameState.IDLE: [
                GameState.WALKING, GameState.DRIVING, GameState.WORKING,
                GameState.EXPLORING, GameState.RESTING
            ],
            GameState.WALKING: [
                GameState.IDLE, GameState.DRIVING, GameState.WORKING,
                GameState.SHOPPING, GameState.SOCIALIZING
            ],
            GameState.DRIVING: [
                GameState.IDLE, GameState.WALKING, GameState.WORKING,
                GameState.EXPLORING
            ],
            GameState.WORKING: [
                GameState.IDLE, GameState.DRIVING, GameState.WALKING
            ],
            GameState.EXPLORING: [
                GameState.IDLE, GameState.DRIVING, GameState.WALKING,
                GameState.SHOPPING
            ],
            GameState.RESTING: [
                GameState.IDLE, GameState.WALKING, GameState.DRIVING
            ],
            GameState.EMERGENCY: [
                GameState.IDLE, GameState.DRIVING, GameState.WALKING
            ]
        }
    
    def can_transition(self, new_state: GameState) -> bool:
        """
        Проверяет, возможен ли переход в новое состояние
        
        Args:
            new_state: Новое состояние
            
        Returns:
            bool: True если переход возможен
        """
        return new_state in self.transitions.get(self.current_state, [])
    
    def transition_to(self, new_state: GameState, force: bool = False):
        """
        Переходит в новое состояние
        
        Args:
            new_state: Новое состояние
            force: Принудительный переход (игнорирует правила)
        """
        if not force and not self.can_transition(new_state):
            print(f"Переход из {self.current_state.value} в {new_state.value} невозможен")
            return False
        
        # Сохраняем предыдущее состояние
        self.previous_state = self.current_state
        
        # Обновляем время в состоянии
        self.state_duration = time.time() - self.state_start_time
        
        # Переходим в новое состояние
        self.current_state = new_state
        self.state_start_time = time.time()
        
        print(f"Переход: {self.previous_state.value} -> {self.current_state.value}")
        return True
    
    def get_state_duration(self) -> float:
        """Возвращает время в текущем состоянии в секундах"""
        return time.time() - self.state_start_time
    
    def should_change_state(self, game_data: Dict) -> Optional[GameState]:
        """
        Определяет, нужно ли сменить состояние на основе данных игры
        
        Args:
            game_data: Данные о текущем состоянии игры
            
        Returns:
            Optional[GameState]: Новое состояние или None
        """
        current_duration = self.get_state_duration()
        
        # Логика смены состояний
        if self.current_state == GameState.IDLE:
            # После бездействия выбираем активность
            if current_duration > random.uniform(5, 15):
                options = [GameState.WALKING, GameState.DRIVING, GameState.EXPLORING]
                return random.choice(options)
        
        elif self.current_state == GameState.WORKING:
            # Работаем определенное время
            if current_duration > random.uniform(300, 600):  # 5-10 минут
                return GameState.IDLE
        
        elif self.current_state == GameState.DRIVING:
            # Едем определенное время
            if current_duration > random.uniform(60, 180):  # 1-3 минуты
                if random.random() < 0.3:  # 30% шанс продолжить
                    return None
                return random.choice([GameState.WALKING, GameState.IDLE, GameState.WORKING])
        
        elif self.current_state == GameState.WALKING:
            # Ходим определенное время
            if current_duration > random.uniform(30, 90):  # 30-90 секунд
                return random.choice([GameState.IDLE, GameState.DRIVING, GameState.SHOPPING])
        
        elif self.current_state == GameState.EXPLORING:
            # Исследуем город
            if current_duration > random.uniform(120, 300):  # 2-5 минут
                return random.choice([GameState.IDLE, GameState.WALKING, GameState.DRIVING])
        
        # Проверка на экстренные ситуации
        if game_data.get('health', 100) < 20:
            return GameState.EMERGENCY
        
        if game_data.get('has_police', False):
            return GameState.EMERGENCY
        
        return None
    
    def get_state_priority(self) -> int:
        """
        Возвращает приоритет текущего состояния
        
        Returns:
            int: Приоритет (чем выше, тем важнее)
        """
        priorities = {
            GameState.EMERGENCY: 100,
            GameState.WORKING: 50,
            GameState.DRIVING: 30,
            GameState.WALKING: 20,
            GameState.EXPLORING: 15,
            GameState.SHOPPING: 10,
            GameState.SOCIALIZING: 10,
            GameState.IDLE: 5,
            GameState.RESTING: 5
        }
        return priorities.get(self.current_state, 0)

