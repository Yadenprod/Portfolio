"""
Модуль обнаружения объектов на миникарте
Оптимизирован для поиска только указанных цветов
"""

import cv2
import numpy as np
import math
import logging
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass

try:
    from config import (
        RED_LOWER_1, RED_UPPER_1, RED_LOWER_2, RED_UPPER_2,
        GREEN_LOWER, GREEN_UPPER, GREEN_SQUARE_LOWER, GREEN_SQUARE_UPPER,
        YELLOW_LOWER, YELLOW_UPPER,
        PINK_LOWER, PINK_UPPER,
        WHITE_LOWER, WHITE_UPPER,
        ORANGE_LOWER, ORANGE_UPPER,
        PURPLE_LOWER, PURPLE_UPPER,
        BLACK_LOWER, BLACK_UPPER
    )
except ImportError:
    # Значения по умолчанию
    RED_LOWER_1 = [0, 100, 100]
    RED_UPPER_1 = [10, 255, 255]
    RED_LOWER_2 = [170, 100, 100]
    RED_UPPER_2 = [180, 255, 255]
    GREEN_LOWER = [40, 200, 200]
    GREEN_UPPER = [80, 255, 255]
    GREEN_SQUARE_LOWER = [50, 200, 80]
    GREEN_SQUARE_UPPER = [70, 255, 180]
    YELLOW_LOWER = [25, 200, 200]
    YELLOW_UPPER = [30, 255, 255]
    PINK_LOWER = [145, 200, 200]
    PINK_UPPER = [155, 255, 255]
    WHITE_LOWER = [0, 0, 240]
    WHITE_UPPER = [180, 10, 255]
    ORANGE_LOWER = [8, 200, 200]
    ORANGE_UPPER = [15, 255, 255]
    PURPLE_LOWER = [130, 200, 150]
    PURPLE_UPPER = [140, 255, 200]
    BLACK_LOWER = [0, 0, 0]
    BLACK_UPPER = [180, 255, 50]

logger = logging.getLogger(__name__)


@dataclass
class DetectionResult:
    """Результат обнаружения объекта"""
    found: bool
    center: Optional[Tuple[int, int]] = None
    contour: Optional[np.ndarray] = None
    area: float = 0.0
    color: Optional[str] = None
    type: str = 'square'  # 'square' or 'circle'
    radius: Optional[float] = None


class ObjectDetector:
    """Оптимизированный детектор объектов на миникарте"""
    
    def __init__(self, minimap_center: Tuple[int, int]):
        """
        Args:
            minimap_center: Центр миникарты (x, y)
        """
        self.minimap_center = minimap_center
        self._hsv_cache: Optional[np.ndarray] = None
        self._last_minimap_hash: Optional[int] = None
    
    def _get_hsv(self, minimap: np.ndarray, force_refresh: bool = False) -> np.ndarray:
        """Получает HSV изображение с кэшированием"""
        # Простая проверка на изменение изображения (hash первой строки)
        current_hash = hash(minimap[:1].tobytes())
        
        if force_refresh or self._hsv_cache is None or self._last_minimap_hash != current_hash:
            self._hsv_cache = cv2.cvtColor(minimap, cv2.COLOR_BGR2HSV)
            self._last_minimap_hash = current_hash
        
        return self._hsv_cache
    
    def _get_color_ranges(self, color_name: str) -> Tuple[np.ndarray, np.ndarray]:
        """Возвращает HSV диапазоны для указанного цвета"""
        color_ranges = {
            'red': (None, None),  # Специальная обработка для красного
            'green': (np.array(GREEN_SQUARE_LOWER), np.array(GREEN_SQUARE_UPPER)),
            'yellow': (np.array(YELLOW_LOWER), np.array(YELLOW_UPPER)),
            'pink': (np.array(PINK_LOWER), np.array(PINK_UPPER)),
            'white': (np.array(WHITE_LOWER), np.array(WHITE_UPPER)),
            'orange': (np.array(ORANGE_LOWER), np.array(ORANGE_UPPER)),
            'purple': (np.array(PURPLE_LOWER), np.array(PURPLE_UPPER)),
        }
        return color_ranges.get(color_name, (None, None))
    
    def find_colored_square(
        self,
        minimap: np.ndarray,
        color_name: str,
        only_if_needed: bool = True
    ) -> DetectionResult:
        """
        Находит цветной квадрат на миникарте
        
        Args:
            minimap: Изображение миникарты (BGR)
            color_name: Название цвета ('yellow', 'pink', 'white', 'orange', 'green', 'purple')
            only_if_needed: Если True, делает быструю проверку наличия цвета перед полным поиском
        
        Returns:
            DetectionResult
        """
        h, w = minimap.shape[:2]
        center_x, center_y = self.minimap_center
        
        # Получаем HSV (с кэшированием)
        hsv = self._get_hsv(minimap)
        
        # Специальная обработка красного
        if color_name == 'red':
            return self._find_red_square_internal(minimap, hsv, center_x, center_y)
        
        # Получаем диапазоны цвета
        lower, upper = self._get_color_ranges(color_name)
        if lower is None or upper is None:
            logger.warning(f"Неизвестный цвет: {color_name}")
            return DetectionResult(found=False, color=color_name)
        
        # Быстрая проверка наличия цвета (оптимизация)
        if only_if_needed:
            mask = cv2.inRange(hsv, lower, upper)
            if np.sum(mask > 0) == 0:
                return DetectionResult(found=False, color=color_name)
        
        # Полный поиск
        return self._find_colored_square_internal(
            minimap, hsv, color_name, lower, upper, center_x, center_y
        )
    
    def _find_colored_square_internal(
        self,
        minimap: np.ndarray,
        hsv: np.ndarray,
        color_name: str,
        lower: np.ndarray,
        upper: np.ndarray,
        center_x: int,
        center_y: int
    ) -> DetectionResult:
        """Внутренний метод поиска цветного квадрата"""
        # Создаем маску
        mask = cv2.inRange(hsv, lower, upper)
        
        # Морфологические операции
        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        
        # Находим контуры
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if len(contours) == 0:
            return DetectionResult(found=False, color=color_name)
        
        # Фильтруем контуры
        candidates = []
        for contour in contours:
            result = self._validate_square_contour(
                contour, minimap, mask, color_name, center_x, center_y
            )
            if result:
                candidates.append(result)
        
        if len(candidates) == 0:
            return DetectionResult(found=False, color=color_name)
        
        # Выбираем лучший кандидат (самый маленький)
        candidates.sort(key=lambda x: (x['area'], -x['quality']))
        best = candidates[0]
        
        return DetectionResult(
            found=True,
            center=best['center'],
            contour=best['contour'],
            area=best['area'],
            color=color_name,
            type='square'
        )
    
    def _validate_square_contour(
        self,
        contour: np.ndarray,
        minimap: np.ndarray,
        color_mask: np.ndarray,
        color_name: str,
        center_x: int,
        center_y: int
    ) -> Optional[Dict]:
        """Валидирует контур как квадрат"""
        area = cv2.contourArea(contour)
        
        # Фильтр по размеру
        if area < 10 or area > 320:
            return None
        
        # Центр
        M = cv2.moments(contour)
        if M["m00"] == 0:
            return None
        
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        
        # Проверка расстояния
        dist_to_center = math.sqrt((cx - center_x)**2 + (cy - center_y)**2)
        if dist_to_center < 20 and area < 50:
            return None
        
        # Проверка формы
        peri = cv2.arcLength(contour, True)
        if peri == 0:
            return None
        
        approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
        if len(approx) < 3:
            return None
        
        # Bounding rect
        x, y, w_rect, h_rect = cv2.boundingRect(contour)
        if w_rect == 0 or h_rect == 0:
            return None
        
        # Aspect ratio
        aspect_ratio = float(w_rect) / h_rect
        if aspect_ratio < 0.5 or aspect_ratio > 1.5:
            return None
        
        # Extent
        rect_area = w_rect * h_rect
        if rect_area == 0:
            return None
        extent = float(area) / rect_area
        if extent < 0.4:
            return None
        
        # Проверка черной обводки
        border = 3
        x_start = max(0, x - border)
        y_start = max(0, y - border)
        x_end = min(minimap.shape[1], x + w_rect + border)
        y_end = min(minimap.shape[0], y + h_rect + border)
        
        roi = minimap[y_start:y_end, x_start:x_end]
        if roi.size == 0:
            return None
        
        gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        black_mask = gray_roi < 60
        
        color_in_roi = color_mask[y_start:y_end, x_start:x_end]
        color_dilated = cv2.dilate(color_in_roi, np.ones((2, 2), np.uint8), iterations=1)
        black_around = black_mask & (~color_dilated.astype(bool))
        
        black_count = np.sum(black_around)
        perimeter_pixels = 2 * (w_rect + h_rect) + 4
        black_density = float(black_count) / perimeter_pixels if perimeter_pixels > 0 else 0
        
        if black_density < 0.02:
            return None
        
        # Оценка качества
        aspect_score = 1.0 - abs(1.0 - aspect_ratio)
        extent_score = extent
        border_score = min(1.0, black_density / 1.0)
        
        is_near_player = dist_to_center < 40
        if is_near_player:
            quality_score = aspect_score * 0.2 + extent_score * 0.1 + border_score * 0.7
        else:
            quality_score = aspect_score * 0.3 + extent_score * 0.2 + border_score * 0.5
        
        return {
            'contour': contour,
            'center': (cx, cy),
            'area': area,
            'quality': quality_score,
            'black_density': black_density,
            'aspect_ratio': aspect_ratio,
            'extent': extent
        }
    
    def _find_red_square_internal(
        self,
        minimap: np.ndarray,
        hsv: np.ndarray,
        center_x: int,
        center_y: int
    ) -> DetectionResult:
        """Поиск красного квадрата (специальная обработка)"""
        # Красный требует двух диапазонов
        lower_red1 = np.array([0, 150, 150])
        upper_red1 = np.array([7, 255, 255])
        lower_red2 = np.array([170, 150, 150])
        upper_red2 = np.array([180, 255, 255])
        
        mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask_red = cv2.bitwise_or(mask_red1, mask_red2)
        
        # Морфология
        kernel = np.ones((3, 3), np.uint8)
        mask_red = cv2.morphologyEx(mask_red, cv2.MORPH_CLOSE, kernel)
        mask_red = cv2.morphologyEx(mask_red, cv2.MORPH_OPEN, kernel)
        
        # Контуры
        contours, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        candidates = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < 30 or area > 500:
                continue
            
            M = cv2.moments(contour)
            if M["m00"] == 0:
                continue
            
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            
            dist_to_center = math.sqrt((cx - center_x)**2 + (cy - center_y)**2)
            if dist_to_center < 20 and area < 80:
                continue
            
            # Проверка формы (упрощенно)
            peri = cv2.arcLength(contour, True)
            if peri == 0:
                continue
            
            approx = cv2.approxPolyDP(contour, 0.04 * peri, True)
            if len(approx) < 4:
                continue
            
            x, y, w_rect, h_rect = cv2.boundingRect(contour)
            if w_rect == 0 or h_rect == 0:
                continue
            
            aspect_ratio = float(w_rect) / h_rect
            if aspect_ratio < 0.7 or aspect_ratio > 1.3:
                continue
            
            rect_area = w_rect * h_rect
            if rect_area == 0:
                continue
            extent = float(area) / rect_area
            if extent < 0.7:
                continue
            
            # Проверка черной обводки
            border = 5
            x_start = max(0, x - border)
            y_start = max(0, y - border)
            x_end = min(minimap.shape[1], x + w_rect + border)
            y_end = min(minimap.shape[0], y + h_rect + border)
            
            roi = minimap[y_start:y_end, x_start:x_end]
            if roi.size == 0:
                continue
            
            gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            black_mask = gray_roi < 50
            red_in_roi = mask_red[y_start:y_end, x_start:x_end]
            red_dilated = cv2.dilate(red_in_roi, np.ones((3, 3), np.uint8), iterations=2)
            black_around = black_mask & (~red_dilated.astype(bool))
            
            black_count = np.sum(black_around)
            perimeter_pixels = 2 * (w_rect + h_rect) + 4
            black_density = float(black_count) / perimeter_pixels if perimeter_pixels > 0 else 0
            
            if black_density < 0.3:
                continue
            
            # Оценка
            aspect_score = 1.0 - abs(1.0 - aspect_ratio)
            extent_score = extent
            border_score = min(1.0, black_density / 1.0)
            
            # Проверка цвета (исключение оранжевого)
            square_roi = minimap[y:y+h_rect, x:x+w_rect]
            square_hsv_roi = hsv[y:y+h_rect, x:x+w_rect]
            square_mask = np.zeros((h_rect, w_rect), dtype=np.uint8)
            contour_in_roi = contour - [x, y]
            cv2.drawContours(square_mask, [contour_in_roi], -1, 255, -1)
            
            if np.sum(square_mask) > 0:
                masked_hsv = square_hsv_roi[square_mask > 0]
                if len(masked_hsv) > 0:
                    mean_h = np.mean(masked_hsv[:, 0])
                    # Исключаем оранжевый (H=8-15)
                    if 8 <= mean_h <= 15:
                        continue
            
            quality_score = aspect_score * 0.15 + extent_score * 0.10 + border_score * 0.20
            
            candidates.append({
                'contour': contour,
                'center': (cx, cy),
                'area': area,
                'quality': quality_score
            })
        
        if len(candidates) == 0:
            return DetectionResult(found=False, color='red')
        
        candidates.sort(key=lambda x: x['quality'], reverse=True)
        best = candidates[0]
        
        return DetectionResult(
            found=True,
            center=best['center'],
            contour=best['contour'],
            area=best['area'],
            color='red',
            type='square'
        )
    
    def find_red_vs_orange(
        self,
        minimap: np.ndarray,
        red_result: DetectionResult,
        orange_result: DetectionResult
    ) -> DetectionResult:
        """
        Проверяет, не путаем ли мы красный с оранжевым
        Возвращает валидный красный или пустой результат
        """
        if not red_result.found:
            return DetectionResult(found=False, color='red')
        
        if not orange_result.found:
            return red_result
        
        # Проверяем расстояние между центрами
        red_center = red_result.center
        orange_center = orange_result.center
        
        dx = red_center[0] - orange_center[0]
        dy = red_center[1] - orange_center[1]
        distance_between = math.sqrt(dx*dx + dy*dy)
        
        if distance_between < 30:
            # Слишком близко - скорее всего оранжевый
            logger.warning(f"Красный и оранжевый квадраты слишком близко ({distance_between:.1f}px) - игнорирую красный")
            return DetectionResult(found=False, color='red')
        
        # Проверяем площадь
        if red_result.area <= orange_result.area:
            logger.warning(f"Красный квадрат ({red_result.area:.1f}) <= оранжевый ({orange_result.area:.1f}) - игнорирую красный")
            return DetectionResult(found=False, color='red')
        
        return red_result
    
    def find_multiple_colors(
        self,
        minimap: np.ndarray,
        colors: Set[str],
        only_if_needed: bool = True
    ) -> Dict[str, DetectionResult]:
        """
        Находит несколько цветов за один проход (оптимизация)
        
        Args:
            minimap: Изображение миникарты
            colors: Множество цветов для поиска
            only_if_needed: Быстрая проверка наличия цвета
        
        Returns:
            Словарь {цвет: DetectionResult}
        """
        results = {}
        
        # Кэшируем HSV
        hsv = self._get_hsv(minimap)
        
        # Ищем каждый цвет
        for color in colors:
            if color == 'red':
                results['red'] = self._find_red_square_internal(
                    minimap, hsv, self.minimap_center[0], self.minimap_center[1]
                )
            else:
                results[color] = self.find_colored_square(
                    minimap, color, only_if_needed=only_if_needed
                )
        
        return results

