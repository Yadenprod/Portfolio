"""
Модуль управления состояниями бота
Упрощает логику переходов между состояниями
"""

import time
import logging
from typing import Optional, Tuple, Dict, List
from dataclasses import dataclass

from .bot_state import BotState
from .state_config import StateConfig
from .detector import DetectionResult

logger = logging.getLogger(__name__)


@dataclass
class StateTransition:
    """Информация о переходе состояния"""
    from_state: BotState
    to_state: BotState
    condition_color: str
    condition_type: str = 'square'
    reset_counter: bool = False
    message: Optional[str] = None


class StateMachine:
    """Управление состояниями бота"""
    
    # Простые переходы состояний (линейные)
    SIMPLE_TRANSITIONS: Dict[BotState, StateTransition] = {
        BotState.Y1: StateTransition(BotState.Y1, BotState.P1, 'yellow', message="Достигнут первый желтый квадрат"),
        BotState.P1: StateTransition(BotState.P1, BotState.G1, 'pink', message="Достигнут первый розовый квадрат"),
        BotState.G1: StateTransition(BotState.G1, BotState.RED_UNTIL_WHITE, 'green', 
                                     message="Достигнут первый зеленый квадрат -> плыву к красным чекпоинтам"),
        BotState.W1: StateTransition(BotState.W1, BotState.P2, 'white', 
                                     message="Достигнут белый квадрат после красных чекпоинтов"),
        BotState.P2: StateTransition(BotState.P2, BotState.RED_1_7, 'pink', reset_counter=True,
                                     message="Достигнут второй розовый квадрат -> начинаю собирать красные чекпоинты 1-7"),
        BotState.GREEN_AFTER_7: StateTransition(BotState.GREEN_AFTER_7, BotState.RED_AFTER_GREEN7, 'green',
                                                 message="Достигнут зеленый квадрат после 7 чекпоинтов"),
        BotState.RED_AFTER_GREEN7: StateTransition(BotState.RED_AFTER_GREEN7, BotState.Y_AFTER_RED, 'red',
                                                    message="Достигнут красный чекпоинт после зеленого"),
        BotState.Y_AFTER_RED: StateTransition(BotState.Y_AFTER_RED, BotState.RED_9_10, 'yellow',
                                               message="Достигнут желтый квадрат после красного"),
        BotState.GREEN_AFTER_10: StateTransition(BotState.GREEN_AFTER_10, BotState.PURPLE_AFTER_10, 'green',
                                                  message="Достигнут зеленый квадрат после 10-го чекпоинта"),
        BotState.PURPLE_AFTER_10: StateTransition(BotState.PURPLE_AFTER_10, BotState.W_AFTER_PURPLE10, 'purple',
                                                   message="Достигнут фиолетовый квадрат после зеленого"),
        BotState.W_AFTER_PURPLE10: StateTransition(BotState.W_AFTER_PURPLE10, BotState.RED_UNTIL_PURPLE, 'white',
                                                    message="Достигнут белый квадрат после фиолетового"),
        BotState.PURPLE_FINAL: StateTransition(BotState.PURPLE_FINAL, BotState.P_FINAL, 'purple',
                                                message="Достигнут финальный фиолетовый квадрат"),
        BotState.P_FINAL: StateTransition(BotState.P_FINAL, BotState.Y_FINAL, 'pink',
                                          message="Достигнут финальный розовый квадрат"),
        BotState.Y_FINAL: StateTransition(BotState.Y_FINAL, BotState.RED_FINAL, 'yellow',
                                          message="Достигнут финальный желтый квадрат"),
        BotState.RED_FINAL: StateTransition(BotState.RED_FINAL, BotState.Y1, 'red', reset_counter=True,
                                            message="Достигнут финальный красный чекпоинт -> рейс завершен, начинаю новый цикл"),
    }
    
    def __init__(self, initial_state: BotState = BotState.Y1):
        """
        Args:
            initial_state: Начальное состояние
        """
        self.state = initial_state
        self.red_squares_collected = 0
        self._last_checkpoint_collected_time = 0
        self._checkpoint_counted_at_reach = False
        self.last_collected_square_center: Optional[Tuple[int, int]] = None
        
        # Для отслеживания пропадания красных чекпоинтов
        self.last_red_checkpoint_center: Optional[Tuple[int, int]] = None
        self.last_red_checkpoint_distance: Optional[float] = None
        self.red_checkpoint_min_distance: Optional[float] = None
    
    def can_transition(self, target: DetectionResult) -> bool:
        """Проверяет, можно ли выполнить переход на основе цели"""
        if not target.found:
            return False
        
        # Проверяем простой переход
        transition = self.SIMPLE_TRANSITIONS.get(self.state)
        if transition:
            return (target.color == transition.condition_color and 
                   target.type == transition.condition_type)
        
        return False
    
    def transition(self, target: DetectionResult) -> Optional[BotState]:
        """
        Выполняет переход состояния на основе цели
        
        Returns:
            Новое состояние или None если переход не выполнен
        """
        transition = self.SIMPLE_TRANSITIONS.get(self.state)
        if not transition:
            return None
        
        if (target.color == transition.condition_color and 
            target.type == transition.condition_type):
            
            if transition.message:
                logger.info(transition.message + f" -> перехожу к {transition.to_state.value}.")
            
            old_state = self.state
            self.state = transition.to_state
            
            if transition.reset_counter:
                self.red_squares_collected = 0
                self._last_checkpoint_collected_time = 0
                self.last_collected_square_center = None
                self.last_red_checkpoint_center = None
                self.last_red_checkpoint_distance = None
                self.red_checkpoint_min_distance = None
            
            return self.state
        
        return None
    
    def handle_red_checkpoint(self, target: DetectionResult, distance: float, 
                             distance_history: List[float]) -> bool:
        """
        Обрабатывает достижение красного чекпоинта
        
        Args:
            target: Результат обнаружения красного квадрата
            distance: Текущее расстояние до цели
            distance_history: История расстояний
        
        Returns:
            True если чекпоинт засчитан, False иначе
        """
        if not self.state.is_red_checkpoint_state():
            return False
        
        if not target.found or target.color != 'red':
            return False
        
        # Проверка задержки 1.5 секунды между засчитываниями
        current_time = time.time()
        time_since_last = current_time - self._last_checkpoint_collected_time
        
        if time_since_last < 1.5:
            logger.warning(f"[RED] ❌ Пропускаю засчитывание - прошло только {time_since_last:.2f} сек (требуется 1.5 сек)")
            return False
        
        # Обновляем время
        self._last_checkpoint_collected_time = current_time
        
        # Увеличиваем счетчик
        min_distance = min(distance_history) if distance_history else distance
        self.red_squares_collected += 1
        self.last_collected_square_center = target.center
        
        logger.info(f"✓ Собран красный чекпоинт #{self.red_squares_collected}/10 "
                   f"(state={self.state.value}, мин. расстояние: {min_distance:.1f}px)")
        
        # Сохраняем для отслеживания пропадания
        self.last_red_checkpoint_center = target.center
        self.last_red_checkpoint_distance = distance
        self.red_checkpoint_min_distance = None
        
        # Проверяем специальные переходы для красных чекпоинтов
        if self.state == BotState.RED_1_7 and self.red_squares_collected >= 7:
            logger.info("Собрано 7 красных чекпоинтов -> плыву к зеленому квадрату.")
            self.state = BotState.GREEN_AFTER_7
            return True
        
        if self.state == BotState.RED_9_10 and self.red_squares_collected >= 10:
            logger.info("Собрано 10 красных чекпоинтов -> плыву к зеленому квадрату.")
            self.state = BotState.GREEN_AFTER_10
            return True
        
        return True
    
    def check_special_transition(self, detector_results: Dict[str, DetectionResult]) -> Optional[BotState]:
        """
        Проверяет специальные переходы (например, появление белого при RED_UNTIL_WHITE)
        
        Args:
            detector_results: Результаты обнаружения всех цветов
        
        Returns:
            Новое состояние или None
        """
        trigger_color = StateConfig.get_special_transition_trigger(self.state)
        if not trigger_color:
            return None
        
        result = detector_results.get(trigger_color)
        if result and result.found:
            target_state = StateConfig.get_special_transition_target(self.state, trigger_color)
            if target_state:
                logger.info(f"В состоянии {self.state.value} обнаружен {trigger_color} квадрат -> "
                          f"переключаюсь на {target_state.value}.")
                old_state = self.state
                self.state = target_state
                return self.state
        
        return None
    
    def reset_state_tracking(self):
        """Сбрасывает отслеживание состояния (для смены состояния)"""
        self.last_collected_square_center = None
        self.last_red_checkpoint_center = None
        self.last_red_checkpoint_distance = None
        self.red_checkpoint_min_distance = None
        self._checkpoint_counted_at_reach = False
    
    def reset_for_new_state(self):
        """Сбрасывает все отслеживание при смене состояния"""
        self.reset_state_tracking()
        # Дополнительные сбросы можно добавить здесь

