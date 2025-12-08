"""
Модуль для захвата экрана игры
"""
import mss
import numpy as np
from PIL import Image
import cv2


class ScreenCapture:
    """Класс для захвата экрана"""
    
    def __init__(self, monitor=None):
        """
        Инициализация захвата экрана
        
        Args:
            monitor: Область экрана для захвата (по умолчанию весь экран)
        """
        self.sct = mss.mss()
        self.monitor = monitor or self.sct.monitors[1]  # Основной монитор
    
    def capture(self):
        """
        Захватывает текущий кадр экрана
        
        Returns:
            numpy.ndarray: Изображение в формате BGR для OpenCV
        """
        screenshot = self.sct.grab(self.monitor)
        img = np.array(screenshot)
        # Конвертация BGRA в BGR
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        return img
    
    def capture_region(self, x, y, width, height):
        """
        Захватывает определенную область экрана
        
        Args:
            x, y: Координаты верхнего левого угла
            width, height: Размеры области
            
        Returns:
            numpy.ndarray: Изображение области
        """
        monitor = {
            "top": y,
            "left": x,
            "width": width,
            "height": height
        }
        screenshot = self.sct.grab(monitor)
        img = np.array(screenshot)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        return img
    
    def set_monitor(self, x, y, width, height):
        """
        Устанавливает область для постоянного захвата
        
        Args:
            x, y, width, height: Параметры области
        """
        self.monitor = {
            "top": y,
            "left": x,
            "width": width,
            "height": height
        }

