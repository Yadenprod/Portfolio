"""
Определение состояний бота через Enum
"""

from enum import Enum


class BotState(Enum):
    """Состояния конечного автомата бота"""
    # Стартовая последовательность
    Y1 = "Y1"  # Первый желтый квадрат
    P1 = "P1"  # Первый розовый квадрат
    G1 = "G1"  # Первый зеленый квадрат
    
    # Красные чекпоинты до белого
    RED_UNTIL_WHITE = "RED_UNTIL_WHITE"
    W1 = "W1"  # Первый белый квадрат
    P2 = "P2"  # Второй розовый квадрат
    
    # Основные красные чекпоинты
    RED_1_7 = "RED_1_7"  # Красные чекпоинты 1-7
    GREEN_AFTER_7 = "GREEN_AFTER_7"  # Зеленый после 7 красных
    RED_AFTER_GREEN7 = "RED_AFTER_GREEN7"  # Красный после зеленого (после 7)
    Y_AFTER_RED = "Y_AFTER_RED"  # Желтый после красного
    
    # Финальные красные чекпоинты
    RED_9_10 = "RED_9_10"  # Красные чекпоинты 9-10
    GREEN_AFTER_10 = "GREEN_AFTER_10"  # Зеленый после 10 красных
    
    # После 10-го
    PURPLE_AFTER_10 = "PURPLE_AFTER_10"  # Фиолетовый после зеленого (после 10)
    W_AFTER_PURPLE10 = "W_AFTER_PURPLE10"  # Белый после фиолетового (после 10)
    
    # Красные до фиолетового
    RED_UNTIL_PURPLE = "RED_UNTIL_PURPLE"
    
    # Финальная последовательность
    PURPLE_FINAL = "PURPLE_FINAL"
    P_FINAL = "P_FINAL"  # Розовый финальный
    Y_FINAL = "Y_FINAL"  # Желтый финальный
    RED_FINAL = "RED_FINAL"  # Красный финальный
    
    @classmethod
    def from_string(cls, value: str):
        """Создает состояние из строки"""
        for state in cls:
            if state.value == value:
                return state
        raise ValueError(f"Неизвестное состояние: {value}")
    
    def is_red_checkpoint_state(self) -> bool:
        """Проверяет, является ли состояние сбором красных чекпоинтов"""
        return self in [
            BotState.RED_1_7,
            BotState.RED_9_10,
            BotState.RED_AFTER_GREEN7,
            BotState.RED_UNTIL_WHITE,
            BotState.RED_UNTIL_PURPLE,
            BotState.RED_FINAL
        ]

