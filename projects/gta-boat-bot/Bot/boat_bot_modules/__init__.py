"""
Модульная структура для бота автоматического плавания
"""

from .bot_state import BotState
from .detector import ObjectDetector, DetectionResult
from .state_config import StateConfig
from .state_machine import StateMachine
from .keyboard_manager import KeyboardManager
from .window_manager import WindowManager
from .checkpoint_counter import CheckpointCounter

__all__ = [
    'BotState',
    'ObjectDetector',
    'DetectionResult',
    'StateConfig',
    'StateMachine',
    'KeyboardManager',
    'WindowManager',
    'CheckpointCounter'
]

