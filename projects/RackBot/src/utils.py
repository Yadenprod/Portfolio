"""
Вспомогательные функции для RackBot
"""
import random
import time
import json
from pathlib import Path
from typing import Dict, Any, Tuple, Optional


def load_config(config_path: str) -> Dict[str, Any]:
    """Загружает конфигурацию из JSON файла"""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Конфигурационный файл не найден: {config_path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Ошибка парсинга JSON в {config_path}: {e}")


def human_delay(min_delay: float, max_delay: float) -> None:
    """
    Создает задержку с случайным временем для имитации человеческого поведения
    
    Args:
        min_delay: Минимальная задержка в секундах
        max_delay: Максимальная задержка в секундах
    """
    delay = random.uniform(min_delay, max_delay)
    time.sleep(delay)


def randomize_coordinate(base_x: int, base_y: int, offset: int = 5) -> Tuple[int, int]:
    """
    Добавляет небольшую случайную вариацию к координатам
    
    Args:
        base_x: Базовая координата X
        base_y: Базовая координата Y
        offset: Максимальное смещение в пикселях
    
    Returns:
        Tuple с рандомизированными координатами
    """
    x = base_x + random.randint(-offset, offset)
    y = base_y + random.randint(-offset, offset)
    return x, y


def validate_config(config: Dict[str, Any]) -> bool:
    """
    Валидирует конфигурацию бота
    
    Args:
        config: Словарь конфигурации
    
    Returns:
        True если конфигурация валидна
    """
    required_keys = ['bot', 'delays', 'safety', 'ui', 'rack', 'logging']
    
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Отсутствует обязательный ключ конфигурации: {key}")
    
    return True


def ensure_directory(path: str) -> Path:
    """Создает директорию если она не существует"""
    dir_path = Path(path)
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def clamp(value: float, min_val: float, max_val: float) -> float:
    """Ограничивает значение между min и max"""
    return max(min_val, min(value, max_val))


def format_time(seconds: float) -> str:
    """Форматирует время в читаемый формат"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    if hours > 0:
        return f"{hours}ч {minutes}м {secs}с"
    elif minutes > 0:
        return f"{minutes}м {secs}с"
    else:
        return f"{secs}с"

