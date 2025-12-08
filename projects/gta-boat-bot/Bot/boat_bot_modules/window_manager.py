"""
Модуль работы с окном игры
Управляет поиском окна и захватом области миникарты
"""

import logging
from typing import Optional, Tuple, Dict
import mss
import numpy as np
import cv2

try:
    import win32gui
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False

logger = logging.getLogger(__name__)


class WindowManager:
    """Менеджер окна игры"""
    
    def __init__(self, window_title: str = "RADMIR CRMP", minimap_region: Optional[Dict] = None):
        """
        Args:
            window_title: Название окна игры
            minimap_region: Область миникарты {'left', 'top', 'width', 'height'}
        """
        self.window_title = window_title
        self.window_handle: Optional[int] = None
        self.window_rect: Optional[Tuple[int, int, int, int]] = None
        self.window_offset_x = 0
        self.window_offset_y = 0
        
        # Область миникарты (относительно окна)
        self.minimap_region = minimap_region or {
            'left': 20,
            'top': 780,
            'width': 300,
            'height': 300
        }
        
        # MSS для захвата экрана
        self.sct = mss.mss()
        
        # Ищем окно при инициализации
        self.find_window()
    
    def find_window(self) -> bool:
        """
        Находит окно игры по названию
        
        Returns:
            True если окно найдено, False иначе
        """
        if not WIN32_AVAILABLE:
            logger.warning("win32gui не установлен. Используется захват всего экрана.")
            return False
        
        def enum_handler(hwnd, ctx):
            window_text = win32gui.GetWindowText(hwnd)
            if self.window_title.lower() in window_text.lower():
                ctx.append((hwnd, window_text))
        
        windows = []
        win32gui.EnumWindows(enum_handler, windows)
        
        if windows:
            self.window_handle = windows[0][0]
            logger.info(f"Найдено окно игры: {windows[0][1]}")
            
            # Получаем координаты окна
            self.window_rect = win32gui.GetWindowRect(self.window_handle)
            window_left, window_top, window_right, window_bottom = self.window_rect
            
            # Проверяем валидность координат
            if window_left < -10000 or window_top < -10000:
                logger.error("Окно игры минимизировано или скрыто.")
                return False
            
            logger.info(f"Координаты окна: {self.window_rect}")
            logger.info(f"Размер окна: {window_right - window_left} x {window_bottom - window_top}")
            
            # Сохраняем смещение окна
            self.window_offset_x = window_left
            self.window_offset_y = window_top
            
            return True
        else:
            logger.error(f"Окно игры '{self.window_title}' не найдено!")
            logger.info("Используется захват всего экрана...")
            return False
    
    def is_window_valid(self) -> bool:
        """Проверяет, что окно существует и доступно"""
        if not WIN32_AVAILABLE or not self.window_handle:
            return False
        
        try:
            if not win32gui.IsWindow(self.window_handle):
                return False
            
            # Обновляем координаты
            self.window_rect = win32gui.GetWindowRect(self.window_handle)
            window_left, window_top, _, _ = self.window_rect
            
            # Проверяем, что окно не минимизировано
            if window_left < -10000 or window_top < -10000:
                return False
            
            return True
        except Exception:
            return False
    
    def capture_minimap(self) -> Optional[np.ndarray]:
        """
        Захватывает область миникарты
        
        Returns:
            Изображение миникарты (BGR) или None если не удалось захватить
        """
        try:
            # Если окно найдено, проверяем его валидность
            if WIN32_AVAILABLE and self.window_handle:
                if not self.is_window_valid():
                    # Попытка переподключения
                    if not self.find_window():
                        return None
                
                # Обновляем координаты окна
                self.window_rect = win32gui.GetWindowRect(self.window_handle)
                window_left, window_top, _, _ = self.window_rect
                
                # Проверяем валидность координат
                if window_left < -10000 or window_top < -10000:
                    return None
                
                # Корректируем координаты миникарты с учетом позиции окна
                capture_region = {
                    'left': window_left + self.minimap_region.get('left', 20),
                    'top': window_top + self.minimap_region.get('top', 780),
                    'width': self.minimap_region.get('width', 300),
                    'height': self.minimap_region.get('height', 300)
                }
            else:
                # Используем координаты относительно всего экрана
                capture_region = self.minimap_region
            
            # Захватываем область
            screenshot = self.sct.grab(capture_region)
            img = np.array(screenshot)
            
            # Конвертируем BGRA в BGR для OpenCV
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            
            return img
        except Exception as e:
            logger.error(f"Ошибка захвата миникарты: {e}")
            return None
    
    def update_minimap_region(self, region: Dict):
        """Обновляет область миникарты"""
        self.minimap_region = region.copy()

