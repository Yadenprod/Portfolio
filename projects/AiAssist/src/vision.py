"""
Модуль для обработки изображений и распознавания элементов игры
"""
import cv2
import numpy as np
import pytesseract
from typing import List, Tuple, Dict, Optional


class VisionProcessor:
    """Класс для обработки визуальной информации из игры"""
    
    def __init__(self):
        """Инициализация процессора зрения"""
        # Настройки для распознавания текста
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    
    def detect_text(self, image: np.ndarray, region: Optional[Tuple[int, int, int, int]] = None) -> str:
        """
        Распознает текст на изображении
        
        Args:
            image: Входное изображение
            region: Область для распознавания (x, y, width, height)
            
        Returns:
            str: Распознанный текст
        """
        if region:
            x, y, w, h = region
            roi = image[y:y+h, x:x+w]
        else:
            roi = image
        
        # Конвертация в grayscale для лучшего распознавания
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        
        # Улучшение контраста
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        
        try:
            text = pytesseract.image_to_string(gray, lang='rus+eng')
            return text.strip()
        except:
            return ""
    
    def find_color(self, image: np.ndarray, color_range: Tuple[Tuple[int, int, int], Tuple[int, int, int]]) -> List[Tuple[int, int]]:
        """
        Находит пиксели определенного цвета
        
        Args:
            image: Входное изображение
            color_range: Диапазон цветов в HSV ((min_h, min_s, min_v), (max_h, max_s, max_v))
            
        Returns:
            List[Tuple[int, int]]: Список координат найденных пикселей
        """
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower, upper = color_range
        mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
        coords = np.column_stack(np.where(mask > 0))
        return [(int(y), int(x)) for x, y in coords]
    
    def detect_objects(self, image: np.ndarray, template: np.ndarray, threshold: float = 0.8) -> List[Tuple[int, int]]:
        """
        Находит объекты на изображении с помощью шаблона
        
        Args:
            image: Входное изображение
            template: Шаблон для поиска
            threshold: Порог совпадения (0-1)
            
        Returns:
            List[Tuple[int, int]]: Координаты найденных объектов
        """
        result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        locations = np.where(result >= threshold)
        matches = list(zip(*locations[::-1]))
        return matches
    
    def detect_health_bar(self, image: np.ndarray) -> float:
        """
        Определяет уровень здоровья из интерфейса
        
        Returns:
            float: Уровень здоровья (0-100)
        """
        # Примерная область полоски здоровья (нужно настроить под ваш интерфейс)
        # Это пример - нужно будет настроить под конкретный интерфейс
        height, width = image.shape[:2]
        health_region = image[int(height * 0.95):height, 0:int(width * 0.3)]
        
        # Поиск красного/зеленого цвета (полоска здоровья)
        # Нужно настроить под конкретный интерфейс игры
        return 100.0  # Заглушка
    
    def detect_minimap(self, image: np.ndarray) -> np.ndarray:
        """
        Извлекает мини-карту из интерфейса
        
        Args:
            image: Входное изображение
            
        Returns:
            np.ndarray: Изображение мини-карты
        """
        height, width = image.shape[:2]
        # Обычно мини-карта в правом верхнем углу
        minimap = image[0:int(height * 0.2), int(width * 0.8):width]
        return minimap
    
    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """
        Предобработка изображения для лучшего анализа
        
        Args:
            image: Входное изображение
            
        Returns:
            np.ndarray: Обработанное изображение
        """
        # Улучшение контраста
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        enhanced = cv2.merge([l, a, b])
        enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
        
        return enhanced
    
    def detect_work_marker(self, image: np.ndarray) -> bool:
        """
        Определяет наличие маркера работы в интерфейсе
        
        Args:
            image: Входное изображение
            
        Returns:
            bool: True если найден маркер работы
        """
        # Поиск характерных цветов/форм маркеров работы
        # Обычно это иконки или текст в определенных областях
        height, width = image.shape[:2]
        
        # Область интерфейса работы (пример - нужно настроить)
        work_region = image[int(height * 0.1):int(height * 0.3), int(width * 0.7):width]
        
        # Поиск ярких цветов (желтый, зеленый - маркеры заданий)
        hsv = cv2.cvtColor(work_region, cv2.COLOR_BGR2HSV)
        yellow_lower = np.array([20, 100, 100])
        yellow_upper = np.array([30, 255, 255])
        green_lower = np.array([40, 100, 100])
        green_upper = np.array([80, 255, 255])
        
        yellow_mask = cv2.inRange(hsv, yellow_lower, yellow_upper)
        green_mask = cv2.inRange(hsv, green_lower, green_upper)
        combined = cv2.bitwise_or(yellow_mask, green_mask)
        
        # Если найдено достаточно пикселей - есть маркер
        if np.sum(combined) > 1000:
            return True
        
        return False
    
    def detect_chat_text(self, image: np.ndarray) -> str:
        """
        Извлекает текст из чата
        
        Args:
            image: Входное изображение
            
        Returns:
            str: Текст из чата
        """
        height, width = image.shape[:2]
        # Обычно чат в левом нижнем углу
        chat_region = image[int(height * 0.7):height, 0:int(width * 0.4)]
        return self.detect_text(chat_region)
    
    def detect_interaction_prompt(self, image: np.ndarray) -> bool:
        """
        Определяет наличие подсказки взаимодействия (например, [E] Взаимодействовать)
        
        Args:
            image: Входное изображение
            
        Returns:
            bool: True если найдена подсказка
        """
        height, width = image.shape[:2]
        # Подсказки обычно в центре или внизу экрана
        center_region = image[int(height * 0.4):int(height * 0.6), int(width * 0.3):int(width * 0.7)]
        
        # Поиск текста с клавишей (обычно в скобках)
        text = self.detect_text(center_region)
        if any(key in text.lower() for key in ['[e]', '[f]', '[g]', 'взаимодей', 'interact']):
            return True
        
        return False
    
    def detect_vehicle(self, image: np.ndarray) -> bool:
        """
        Определяет, находится ли игрок в транспорте
        
        Args:
            image: Входное изображение
            
        Returns:
            bool: True если в транспорте
        """
        # Анализ интерфейса транспорта (спидометр, руль и т.д.)
        # Упрощенная версия - можно улучшить
        height, width = image.shape[:2]
        
        # Область спидометра (обычно внизу)
        speedo_region = image[int(height * 0.85):height, int(width * 0.4):int(width * 0.6)]
        
        # Поиск характерных элементов интерфейса транспорта
        # Это нужно настроить под конкретный интерфейс
        return False  # Заглушка
    
    def detect_players_nearby(self, image: np.ndarray) -> int:
        """
        Определяет количество игроков поблизости
        
        Args:
            image: Входное изображение
            
        Returns:
            int: Количество игроков
        """
        # Анализ мини-карты или основного экрана
        # Упрощенная версия
        minimap = self.detect_minimap(image)
        
        # Поиск маркеров игроков на мини-карте
        # Нужно настроить под конкретный интерфейс
        return 0  # Заглушка

