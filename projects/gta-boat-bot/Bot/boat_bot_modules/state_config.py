"""
Конфигурация состояний бота - определяет какие цвета искать для каждого состояния
"""

from typing import List, Optional, Dict, Set
from .bot_state import BotState


class StateConfig:
    """Конфигурация для определения цели в зависимости от состояния"""
    
    # Конфигурация: какие цвета искать для каждого состояния
    # Формат: {состояние: {'primary': [цвета], 'check_for': [цвета для проверки переключения]}}
    STATE_TARGET_CONFIG: Dict[BotState, Dict[str, List[str]]] = {
        # Стартовая последовательность
        BotState.Y1: {'primary': ['yellow'], 'check_for': []},
        BotState.P1: {'primary': ['pink'], 'check_for': []},
        BotState.G1: {'primary': ['green'], 'check_for': []},
        
        # Красные до белого
        BotState.RED_UNTIL_WHITE: {
            'primary': ['red'],
            'check_for': ['orange', 'white']  # Проверяем оранжевый (чтобы не путать) и белый (для переключения)
        },
        BotState.W1: {'primary': ['white'], 'check_for': []},
        BotState.P2: {'primary': ['pink'], 'check_for': []},
        
        # Основные красные чекпоинты
        BotState.RED_1_7: {
            'primary': ['red'],
            'check_for': ['orange']  # Проверяем оранжевый, чтобы не путать
        },
        BotState.GREEN_AFTER_7: {'primary': ['green'], 'check_for': []},
        BotState.RED_AFTER_GREEN7: {
            'primary': ['red'],
            'check_for': ['orange']
        },
        BotState.Y_AFTER_RED: {'primary': ['yellow'], 'check_for': []},
        
        # Финальные красные
        BotState.RED_9_10: {
            'primary': ['red'],
            'check_for': ['orange']
        },
        BotState.GREEN_AFTER_10: {'primary': ['green'], 'check_for': []},
        BotState.PURPLE_AFTER_10: {'primary': ['purple'], 'check_for': []},
        BotState.W_AFTER_PURPLE10: {'primary': ['white'], 'check_for': []},
        
        # Красные до фиолетового
        BotState.RED_UNTIL_PURPLE: {
            'primary': ['red', 'purple'],  # Ищем красные, но приоритет у фиолетового
            'check_for': ['orange', 'purple']  # Проверяем оранжевый и фиолетовый для переключения
        },
        
        # Финальная последовательность
        BotState.PURPLE_FINAL: {'primary': ['purple'], 'check_for': []},
        BotState.P_FINAL: {'primary': ['pink'], 'check_for': []},
        BotState.Y_FINAL: {'primary': ['yellow'], 'check_for': []},
        BotState.RED_FINAL: {
            'primary': ['red'],
            'check_for': ['orange']
        },
    }
    
    # Состояния, которые могут проверять специальные условия переключения
    # Например, RED_UNTIL_WHITE переключается на W1 при появлении белого
    SPECIAL_TRANSITIONS: Dict[BotState, Dict[str, BotState]] = {
        BotState.RED_UNTIL_WHITE: {'white': BotState.W1},
        BotState.RED_UNTIL_PURPLE: {'purple': BotState.PURPLE_FINAL},
    }
    
    @classmethod
    def get_primary_colors(cls, state: BotState) -> List[str]:
        """Возвращает основные цвета для поиска в указанном состоянии"""
        config = cls.STATE_TARGET_CONFIG.get(state)
        if config:
            return config.get('primary', [])
        return []
    
    @classmethod
    def get_check_colors(cls, state: BotState) -> List[str]:
        """Возвращает цвета для дополнительной проверки (например, оранжевый для исключения)"""
        config = cls.STATE_TARGET_CONFIG.get(state)
        if config:
            return config.get('check_for', [])
        return []
    
    @classmethod
    def get_all_colors_to_search(cls, state: BotState) -> Set[str]:
        """Возвращает все цвета, которые нужно искать для состояния"""
        primary = cls.get_primary_colors(state)
        check = cls.get_check_colors(state)
        # Для состояний RED_UNTIL_PURPLE primary уже содержит оба цвета
        return set(primary + check)
    
    @classmethod
    def get_special_transition_trigger(cls, state: BotState) -> Optional[str]:
        """Возвращает цвет-триггер для специального перехода состояния"""
        transitions = cls.SPECIAL_TRANSITIONS.get(state)
        if transitions:
            # Возвращаем первый ключ (цвет), который вызывает переход
            return list(transitions.keys())[0]
        return None
    
    @classmethod
    def get_special_transition_target(cls, state: BotState, trigger_color: str) -> Optional[BotState]:
        """Возвращает целевое состояние для специального перехода"""
        transitions = cls.SPECIAL_TRANSITIONS.get(state)
        if transitions:
            return transitions.get(trigger_color)
        return None

