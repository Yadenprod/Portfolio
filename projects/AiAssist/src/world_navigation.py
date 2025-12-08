"""
Продвинутая система навигации по открытому миру
"""
import cv2
import numpy as np
import math
import time
from typing import Tuple, List, Optional, Dict
from collections import deque


class WorldNavigation:
    """Система навигации по открытому миру"""
    
    def __init__(self):
        """Инициализация навигации"""
        self.current_position = None
        self.target_position = None
        self.route = []
        self.is_navigating = False
        self.navigation_start_time = None
        
        # История позиций для отслеживания движения
        self.position_history = deque(maxlen=50)
        
        # Известные локации (будут изучаться)
        self.known_locations = {
            'spawn': None,
            'work_delivery': [],
            'work_taxi': [],
            'work_trucker': [],
            'work_miner': [],
            'work_fisher': [],
            'work_mechanic': [],
            'hospitals': [],
            'shops': [],
            'garages': []
        }
        
        # Статистика навигации
        self.nav_stats = {
            'successful_routes': 0,
            'failed_routes': 0,
            'average_route_time': 0,
            'learned_locations': 0
        }
    
    def find_work_location_on_map(self, minimap_image: np.ndarray, 
                                  work_type: str) -> Optional[Tuple[int, int]]:
        """
        Находит место работы на мини-карте
        
        Args:
            minimap_image: Изображение мини-карты
            work_type: Тип работы
            
        Returns:
            Optional[Tuple[int, int]]: Позиция места работы или None
        """
        # Конвертация в HSV для лучшей обработки
        hsv = cv2.cvtColor(minimap_image, cv2.COLOR_BGR2HSV)
        
        # Цвета маркеров работы (нужно настроить под Radmir RP)
        work_marker_colors = {
            'delivery': {
                'lower': np.array([20, 100, 100]),   # Желтый
                'upper': np.array([30, 255, 255])
            },
            'taxi': {
                'lower': np.array([100, 100, 100]),   # Синий
                'upper': np.array([130, 255, 255])
            },
            'trucker': {
                'lower': np.array([0, 100, 100]),     # Красный
                'upper': np.array([10, 255, 255])
            },
            'miner': {
                'lower': np.array([15, 100, 100]),   # Оранжевый
                'upper': np.array([25, 255, 255])
            },
            'fisher': {
                'lower': np.array([80, 100, 100]),    # Голубой
                'upper': np.array([100, 255, 255])
            },
            'mechanic': {
                'lower': np.array([40, 100, 100]),   # Зеленый
                'upper': np.array([80, 255, 255])
            }
        }
        
        color_range = work_marker_colors.get(work_type, work_marker_colors['delivery'])
        mask = cv2.inRange(hsv, color_range['lower'], color_range['upper'])
        
        # Поиск контуров (маркеров)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # Берем самый большой контур (вероятно маркер работы)
            largest_contour = max(contours, key=cv2.contourArea)
            if cv2.contourArea(largest_contour) > 10:  # Минимальный размер
                M = cv2.moments(largest_contour)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    return (cx, cy)
        
        return None
    
    def find_all_work_markers(self, minimap_image: np.ndarray) -> Dict[str, List[Tuple[int, int]]]:
        """
        Находит все маркеры работы на карте
        
        Args:
            minimap_image: Изображение мини-карты
            
        Returns:
            Dict: Типы работы и их позиции
        """
        work_types = ['delivery', 'taxi', 'trucker', 'miner', 'fisher', 'mechanic']
        found_work = {}
        
        for work_type in work_types:
            location = self.find_work_location_on_map(minimap_image, work_type)
            if location:
                if work_type not in found_work:
                    found_work[work_type] = []
                found_work[work_type].append(location)
        
        return found_work
    
    def get_player_position(self, minimap_image: np.ndarray) -> Optional[Tuple[int, int]]:
        """
        Определяет позицию игрока на мини-карте
        
        Args:
            minimap_image: Изображение мини-карты
            
        Returns:
            Optional[Tuple[int, int]]: Позиция игрока
        """
        hsv = cv2.cvtColor(minimap_image, cv2.COLOR_BGR2HSV)
        
        # Белый/желтый треугольник - маркер игрока
        lower_white = np.array([0, 0, 200])
        upper_white = np.array([180, 30, 255])
        lower_yellow = np.array([20, 100, 200])
        upper_yellow = np.array([30, 255, 255])
        
        mask_white = cv2.inRange(hsv, lower_white, upper_white)
        mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
        mask = cv2.bitwise_or(mask_white, mask_yellow)
        
        # Поиск центра масс
        moments = cv2.moments(mask)
        if moments["m00"] != 0:
            cx = int(moments["m10"] / moments["m00"])
            cy = int(moments["m01"] / moments["m00"])
            return (cx, cy)
        
        return None
    
    def calculate_direction_to_target(self, player_pos: Tuple[int, int],
                                     target_pos: Tuple[int, int]) -> Dict:
        """
        Вычисляет направление к цели
        
        Args:
            player_pos: Позиция игрока
            target_pos: Позиция цели
            
        Returns:
            Dict: Направление и расстояние
        """
        dx = target_pos[0] - player_pos[0]
        dy = target_pos[1] - player_pos[1]
        
        distance = math.sqrt(dx*dx + dy*dy)
        angle_rad = math.atan2(dy, dx)
        angle_deg = math.degrees(angle_rad)
        
        # Нормализуем угол (0-360)
        if angle_deg < 0:
            angle_deg += 360
        
        return {
            'distance': distance,
            'angle': angle_deg,
            'dx': dx,
            'dy': dy
        }
    
    def plan_route(self, start: Tuple[int, int], end: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Планирует маршрут от точки до точки
        
        Args:
            start: Начальная точка
            end: Конечная точка
            
        Returns:
            List[Tuple[int, int]]: Список точек маршрута
        """
        # Упрощенная версия - прямая линия
        # В реальной системе здесь будет A* или другой алгоритм
        # с учетом дорог и препятствий
        
        # Для начала - простая линейная интерполяция
        steps = max(10, int(math.sqrt((end[0]-start[0])**2 + (end[1]-start[1])**2) / 5))
        
        route = []
        for i in range(steps + 1):
            t = i / steps
            x = int(start[0] + (end[0] - start[0]) * t)
            y = int(start[1] + (end[1] - start[1]) * t)
            route.append((x, y))
        
        return route
    
    def navigate_to_target(self, minimap_image: np.ndarray,
                          target_pos: Tuple[int, int]) -> Dict:
        """
        Навигация к цели на основе мини-карты
        
        Args:
            minimap_image: Изображение мини-карты
            target_pos: Позиция цели
            
        Returns:
            Dict: Команды для движения
        """
        player_pos = self.get_player_position(minimap_image)
        
        if not player_pos:
            return {
                'action': 'wait',
                'reason': 'player_position_unknown'
            }
        
        # Сохраняем позицию в историю
        self.position_history.append(player_pos)
        self.current_position = player_pos
        
        # Вычисляем направление к цели
        direction_info = self.calculate_direction_to_target(player_pos, target_pos)
        
        distance = direction_info['distance']
        angle = direction_info['angle']
        
        # Если очень близко - достигли цели
        if distance < 5:
            return {
                'action': 'arrived',
                'reason': 'target_reached',
                'distance': distance
            }
        
        # Определяем направление движения
        # Упрощенная версия - поворачиваем к цели и едем вперед
        # В реальной системе здесь будет более сложная логика
        
        # Определяем нужный поворот
        turn_needed = self._calculate_turn_needed(angle)
        
        return {
            'action': 'navigate',
            'target': target_pos,
            'distance': distance,
            'angle': angle,
            'turn': turn_needed,
            'move_forward': True
        }
    
    def _calculate_turn_needed(self, target_angle: float) -> Dict:
        """
        Вычисляет необходимый поворот
        
        Args:
            target_angle: Угол к цели
            
        Returns:
            Dict: Информация о повороте
        """
        # Упрощенная версия - предполагаем что игрок смотрит на север (0°)
        # В реальной системе нужно определять текущее направление
        
        # Нормализуем угол
        if target_angle > 180:
            target_angle = target_angle - 360
        
        # Определяем направление поворота
        if abs(target_angle) < 10:  # Почти прямо
            return {'direction': 'none', 'amount': 0}
        elif target_angle > 0:
            return {'direction': 'right', 'amount': min(abs(target_angle) / 90.0, 1.0)}
        else:
            return {'direction': 'left', 'amount': min(abs(target_angle) / 90.0, 1.0)}
    
    def is_on_road(self, minimap_image: np.ndarray) -> bool:
        """
        Определяет, находится ли игрок на дороге
        
        Args:
            minimap_image: Изображение мини-карты
            
        Returns:
            bool: True если на дороге
        """
        # Анализ мини-карты для определения дороги
        # Дороги обычно серые/светлые на карте
        
        gray = cv2.cvtColor(minimap_image, cv2.COLOR_BGR2GRAY)
        
        # Дороги обычно имеют среднюю яркость
        mean_brightness = np.mean(gray)
        
        # Если средняя яркость в определенном диапазоне - вероятно дорога
        if 80 < mean_brightness < 200:
            return True
        
        return False
    
    def detect_obstacles(self, minimap_image: np.ndarray) -> List[Tuple[int, int]]:
        """
        Обнаруживает препятствия на пути
        
        Args:
            minimap_image: Изображение мини-карты
            
        Returns:
            List[Tuple[int, int]]: Позиции препятствий
        """
        # Упрощенная версия
        # В реальной системе здесь будет более сложная логика
        # с анализом карты и определением препятствий
        
        obstacles = []
        # TODO: Реализовать детекцию препятствий
        
        return obstacles
    
    def learn_location(self, location_type: str, position: Tuple[int, int]):
        """
        Запоминает новую локацию
        
        Args:
            location_type: Тип локации
            position: Позиция локации
        """
        if location_type in self.known_locations:
            # Проверяем, нет ли уже такой локации
            for loc in self.known_locations[location_type]:
                dist = math.sqrt(
                    (loc[0] - position[0])**2 + 
                    (loc[1] - position[1])**2
                )
                if dist < 10:  # Уже знаем эту локацию
                    return
            
            self.known_locations[location_type].append(position)
            self.nav_stats['learned_locations'] += 1
            print(f"📍 Изучена новая локация: {location_type} в позиции {position}")
    
    def find_nearest_known_location(self, current_pos: Tuple[int, int],
                                   location_type: str) -> Optional[Tuple[int, int]]:
        """
        Находит ближайшую известную локацию
        
        Args:
            current_pos: Текущая позиция
            location_type: Тип локации
            
        Returns:
            Optional[Tuple[int, int]]: Позиция локации или None
        """
        if location_type not in self.known_locations:
            return None
        
        locations = self.known_locations[location_type]
        if not locations:
            return None
        
        nearest = None
        min_distance = float('inf')
        
        for loc in locations:
            distance = math.sqrt(
                (loc[0] - current_pos[0])**2 + 
                (loc[1] - current_pos[1])**2
            )
            if distance < min_distance:
                min_distance = distance
                nearest = loc
        
        return nearest
    
    def update_navigation_stats(self, success: bool, route_time: float):
        """
        Обновляет статистику навигации
        
        Args:
            success: Успешность маршрута
            route_time: Время маршрута
        """
        if success:
            self.nav_stats['successful_routes'] += 1
        else:
            self.nav_stats['failed_routes'] += 1
        
        # Обновляем среднее время
        total_routes = (self.nav_stats['successful_routes'] + 
                       self.nav_stats['failed_routes'])
        if total_routes > 0:
            self.nav_stats['average_route_time'] = (
                (self.nav_stats['average_route_time'] * (total_routes - 1) + route_time) 
                / total_routes
            )
    
    def is_moving(self) -> bool:
        """
        Определяет, движется ли игрок
        
        Returns:
            bool: True если движется
        """
        if len(self.position_history) < 2:
            return False
        
        # Сравниваем последние позиции
        last_pos = self.position_history[-1]
        prev_pos = self.position_history[-2]
        
        # Если позиция изменилась - движемся
        distance = math.sqrt(
            (last_pos[0] - prev_pos[0])**2 + 
            (last_pos[1] - prev_pos[1])**2
        )
        
        return distance > 2  # Минимальное изменение для движения

