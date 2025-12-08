"""
Модуль навигации и работы с картой
"""
import cv2
import numpy as np
from typing import Tuple, List, Optional, Dict
import math


class NavigationSystem:
    """Система навигации по карте"""
    
    def __init__(self):
        """Инициализация системы навигации"""
        self.current_position = None
        self.target_position = None
        self.route = []
        self.is_navigating = False
        
        # Известные точки интереса (можно расширить)
        self.landmarks = {
            'spawn': (0, 0),  # Точка спавна
            'city_center': (0, 0),  # Центр города
            'work_zone': (0, 0),  # Зона работы
        }
    
    def extract_minimap_data(self, minimap_image: np.ndarray) -> Dict:
        """
        Извлекает данные из мини-карты
        
        Args:
            minimap_image: Изображение мини-карты
            
        Returns:
            Dict: Данные с мини-карты (позиция, направление и т.д.)
        """
        # Конвертация в HSV для лучшей обработки
        hsv = cv2.cvtColor(minimap_image, cv2.COLOR_BGR2HSV)
        
        # Поиск маркера игрока (обычно белый/желтый треугольник)
        # Нужно настроить под конкретный интерфейс
        player_marker = self._find_player_marker(minimap_image)
        
        # Поиск маркеров целей (обычно красные/желтые точки)
        target_markers = self._find_target_markers(minimap_image)
        
        # Определение направления взгляда
        direction = self._get_direction(minimap_image, player_marker)
        
        return {
            'player_position': player_marker,
            'targets': target_markers,
            'direction': direction,
            'has_route': len(target_markers) > 0
        }
    
    def _find_player_marker(self, minimap: np.ndarray) -> Optional[Tuple[int, int]]:
        """
        Находит маркер игрока на мини-карте
        
        Args:
            minimap: Изображение мини-карты
            
        Returns:
            Optional[Tuple[int, int]]: Позиция маркера или None
        """
        # Поиск белого/желтого треугольника (маркер игрока)
        # Это пример - нужно настроить под конкретный интерфейс
        hsv = cv2.cvtColor(minimap, cv2.COLOR_BGR2HSV)
        
        # Белый цвет (маркер игрока)
        lower_white = np.array([0, 0, 200])
        upper_white = np.array([180, 30, 255])
        mask = cv2.inRange(hsv, lower_white, upper_white)
        
        # Поиск центра масс
        moments = cv2.moments(mask)
        if moments["m00"] != 0:
            cx = int(moments["m10"] / moments["m00"])
            cy = int(moments["m01"] / moments["m00"])
            return (cx, cy)
        
        return None
    
    def _find_target_markers(self, minimap: np.ndarray) -> List[Tuple[int, int]]:
        """
        Находит маркеры целей на мини-карте
        
        Args:
            minimap: Изображение мини-карты
            
        Returns:
            List[Tuple[int, int]]: Список позиций целей
        """
        hsv = cv2.cvtColor(minimap, cv2.COLOR_BGR2HSV)
        
        # Красный/желтый цвет (маркеры целей)
        lower_red = np.array([0, 100, 100])
        upper_red = np.array([10, 255, 255])
        lower_yellow = np.array([20, 100, 100])
        upper_yellow = np.array([30, 255, 255])
        
        mask_red = cv2.inRange(hsv, lower_red, upper_red)
        mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
        mask = cv2.bitwise_or(mask_red, mask_yellow)
        
        # Поиск контуров
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        targets = []
        for contour in contours:
            if cv2.contourArea(contour) > 10:  # Минимальный размер
                M = cv2.moments(contour)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    targets.append((cx, cy))
        
        return targets
    
    def _get_direction(self, minimap: np.ndarray, player_pos: Optional[Tuple[int, int]]) -> float:
        """
        Определяет направление взгляда игрока
        
        Args:
            minimap: Изображение мини-карты
            player_pos: Позиция игрока
            
        Returns:
            float: Угол направления в градусах
        """
        if player_pos is None:
            return 0.0
        
        # Поиск направления по форме маркера игрока
        # Обычно это треугольник, указывающий направление
        # Упрощенная версия - нужно доработать
        return 0.0  # Заглушка
    
    def calculate_route(self, start: Tuple[int, int], end: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Вычисляет маршрут от точки до точки
        
        Args:
            start: Начальная точка
            end: Конечная точка
            
        Returns:
            List[Tuple[int, int]]: Список точек маршрута
        """
        # Упрощенная версия - прямая линия
        # В реальной системе здесь будет A* или другой алгоритм поиска пути
        return [start, end]
    
    def get_direction_to_target(self, current_pos: Tuple[int, int], 
                                target_pos: Tuple[int, int]) -> Tuple[float, float]:
        """
        Вычисляет направление к цели
        
        Args:
            current_pos: Текущая позиция
            target_pos: Целевая позиция
            
        Returns:
            Tuple[float, float]: (расстояние, угол в градусах)
        """
        dx = target_pos[0] - current_pos[0]
        dy = target_pos[1] - current_pos[1]
        
        distance = math.sqrt(dx*dx + dy*dy)
        angle = math.degrees(math.atan2(dy, dx))
        
        return (distance, angle)
    
    def is_on_road(self, minimap_data: Dict) -> bool:
        """
        Определяет, находится ли игрок на дороге
        
        Args:
            minimap_data: Данные с мини-карты
            
        Returns:
            bool: True если на дороге
        """
        # Анализ мини-карты для определения дороги
        # Упрощенная версия
        return True  # Заглушка
    
    def find_nearest_landmark(self, current_pos: Tuple[int, int], 
                             landmark_type: str = None) -> Optional[Tuple[str, Tuple[int, int]]]:
        """
        Находит ближайшую точку интереса
        
        Args:
            current_pos: Текущая позиция
            landmark_type: Тип точки интереса (None = любой)
            
        Returns:
            Optional[Tuple[str, Tuple[int, int]]]: (название, позиция) или None
        """
        if not self.landmarks:
            return None
        
        nearest = None
        min_distance = float('inf')
        
        for name, pos in self.landmarks.items():
            if landmark_type and name != landmark_type:
                continue
            
            distance = math.sqrt(
                (pos[0] - current_pos[0])**2 + 
                (pos[1] - current_pos[1])**2
            )
            
            if distance < min_distance:
                min_distance = distance
                nearest = (name, pos)
        
        return nearest

