"""
Пример использования оптимизированных модулей бота
Демонстрирует ключевые улучшения
"""

import numpy as np
from bot_state import BotState
from detector import ObjectDetector, DetectionResult
from state_config import StateConfig


def example_optimized_detection():
    """
    Пример оптимизированного обнаружения - ищем только нужные цвета
    """
    # Инициализация
    minimap_center = (150, 150)
    detector = ObjectDetector(minimap_center)
    
    # Текущее состояние
    current_state = BotState.Y1
    
    # БЫЛО: искали все 7 цветов каждый кадр
    # yellow = detector.find_colored_square(minimap, 'yellow')
    # pink = detector.find_colored_square(minimap, 'pink')
    # white = detector.find_colored_square(minimap, 'white')
    # orange = detector.find_colored_square(minimap, 'orange')
    # green = detector.find_colored_square(minimap, 'green')
    # purple = detector.find_colored_square(minimap, 'purple')
    # red = detector.find_red_square(minimap)
    # = 7x больше работы! 😱
    
    # СТАЛО: ищем только нужные цвета для текущего состояния
    colors_to_search = StateConfig.get_all_colors_to_search(current_state)
    print(f"Состояние {current_state.value}: ищем цвета {colors_to_search}")
    # Результат: {'yellow'} - только желтый! ⚡
    
    # Ищем только указанные цвета (оптимизация)
    # results = detector.find_multiple_colors(minimap, colors_to_search)
    # yellow_result = results.get('yellow', DetectionResult(found=False))
    
    print(f"✅ Оптимизация: вместо 7 цветов ищем {len(colors_to_search)}")
    print(f"   Экономия: {100 * (1 - len(colors_to_search)/7):.1f}% вычислительных ресурсов")


def example_state_transitions():
    """
    Пример работы с состояниями через Enum
    """
    # БЫЛО: строки (легко опечататься)
    # state = 'Y1'  # Опечатка? state = 'Yl' - никто не заметит!
    
    # СТАЛО: Enum (безопасно и с автодополнением)
    state = BotState.Y1
    print(f"Текущее состояние: {state.value}")
    
    # Проверка типа состояния
    if state.is_red_checkpoint_state():
        print("Собираем красные чекпоинты")
    else:
        print("Не собираем красные чекпоинты")
    
    # Переход состояния
    next_state = BotState.P1
    print(f"Переход: {state.value} → {next_state.value}")


def example_red_vs_orange_check():
    """
    Пример использования утилиты проверки красный vs оранжевый
    Убираем дублирование кода
    """
    detector = ObjectDetector((150, 150))
    
    # БЫЛО: повторялась логика проверки 6+ раз в разных местах
    # if orange_square['found']:
    #     red_area = red_square.get('area', 0)
    #     orange_area = orange_square.get('area', 0)
    #     # ... 20+ строк проверок в каждом месте
    
    # СТАЛО: один метод
    # red_result = detector.find_red_square(minimap)
    # orange_result = detector.find_colored_square(minimap, 'orange')
    # valid_red = detector.find_red_vs_orange(minimap, red_result, orange_result)
    
    print("✅ Убрана дубликация: один метод вместо 6+ повторений")


def example_special_transitions():
    """
    Пример работы со специальными переходами состояний
    """
    state = BotState.RED_UNTIL_WHITE
    
    # Проверяем, есть ли специальный переход для этого состояния
    trigger_color = StateConfig.get_special_transition_trigger(state)
    if trigger_color:
        print(f"Состояние {state.value} проверяет появление {trigger_color}")
        
        target_state = StateConfig.get_special_transition_target(state, trigger_color)
        print(f"  → При появлении переключается на {target_state.value}")
    
    # Это упрощает логику в основном цикле:
    # Вместо проверки в каждом состоянии отдельно:
    # if state == 'RED_UNTIL_WHITE' and white_square['found']:
    #     state = 'W1'
    # if state == 'RED_UNTIL_PURPLE' and purple_square['found']:
    #     state = 'PURPLE_FINAL'
    # 
    # Можно использовать общий код:
    # trigger = StateConfig.get_special_transition_trigger(state)
    # if trigger and results[trigger].found:
    #     state = StateConfig.get_special_transition_target(state, trigger)


if __name__ == "__main__":
    print("=" * 60)
    print("Примеры использования оптимизированных модулей")
    print("=" * 60)
    print()
    
    print("1. Оптимизированное обнаружение:")
    example_optimized_detection()
    print()
    
    print("2. Работа с состояниями:")
    example_state_transitions()
    print()
    
    print("3. Проверка красный vs оранжевый:")
    example_red_vs_orange_check()
    print()
    
    print("4. Специальные переходы:")
    example_special_transitions()
    print()
    
    print("=" * 60)
    print("✅ Все примеры демонстрируют ключевые улучшения!")
    print("=" * 60)

