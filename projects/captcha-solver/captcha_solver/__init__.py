"""
CaptchaSolver - Мощная система для распознавания капчи
Поддерживает множественные подходы для максимальной точности
"""

from .preprocessor import CaptchaPreprocessor
from .models import CaptchaModel
from .solver import CaptchaSolver
from .api import create_app

__version__ = "1.0.0"
__author__ = "CapchaProd Team"

__all__ = ['CaptchaPreprocessor', 'CaptchaModel', 'CaptchaSolver', 'create_app'] 