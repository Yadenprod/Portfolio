import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import matplotlib.pyplot as plt
from typing import Optional, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CaptchaPreprocessor:
    """
    Мощный препроцессор для очистки капчи от шума и артефактов
    Специально оптимизирован для капчи с сеткой и цветными линиями
    """
    
    def __init__(self):
        self.debug = False
        
    def enable_debug(self, enable: bool = True):
        """Включить/выключить режим отладки с визуализацией"""
        self.debug = enable
        
    def preprocess(self, image_path: str, show_steps: bool = False) -> np.ndarray:
        """
        Основной метод предобработки изображения капчи
        
        Args:
            image_path: путь к изображению
            show_steps: показать промежуточные шаги
            
        Returns:
            Очищенное изображение готовое для распознавания
        """
        logger.info(f"Начинаем обработку изображения: {image_path}")
        
        # Загрузка изображения
        original = cv2.imread(image_path)
        if original is None:
            raise ValueError(f"Не удалось загрузить изображение: {image_path}")
            
        if show_steps:
            self._show_image(original, "1. Оригинал")
        
        # Попробуем мягкую обработку для сохранения искаженных цифр
        processed = self.preprocess_grid_captcha_gentle(original, show_steps)
        
        logger.info("Предобработка завершена успешно")
        return processed
    
    def preprocess_grid_captcha_gentle(self, image: np.ndarray, show_steps: bool = False) -> np.ndarray:
        """
        Мягкая обработка капчи с сеткой, сохраняющая искаженные цифры
        """
        if show_steps:
            self._show_image(image, "1. Оригинал")
        
        # 1. Увеличиваем изображение для лучшей обработки
        height, width = image.shape[:2]
        scale_factor = 2 if width < 200 else 1.5
        enlarged = cv2.resize(image, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_CUBIC)
        
        if show_steps:
            self._show_image(enlarged, "2. Увеличено")
        
        # 2. Конвертируем в HSV для работы с цветами
        hsv = cv2.cvtColor(enlarged, cv2.COLOR_BGR2HSV)
        
        # 3. Создаем маску для текста (темные области)
        # Берем канал Value (яркость) 
        v_channel = hsv[:, :, 2]
        
        # Находим темные области (потенциальный текст)
        text_mask = cv2.threshold(v_channel, 120, 255, cv2.THRESH_BINARY_INV)[1]
        
        if show_steps:
            self._show_image(text_mask, "3. Маска текста")
        
        # 4. Удаляем тонкие линии сетки, сохраняя толстые символы
        # Горизонтальные линии
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 1))
        horizontal_lines = cv2.morphologyEx(text_mask, cv2.MORPH_OPEN, horizontal_kernel)
        
        # Вертикальные линии  
        vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 30))
        vertical_lines = cv2.morphologyEx(text_mask, cv2.MORPH_OPEN, vertical_kernel)
        
        # Убираем линии сетки из маски текста
        text_cleaned = cv2.subtract(text_mask, horizontal_lines)
        text_cleaned = cv2.subtract(text_cleaned, vertical_lines)
        
        if show_steps:
            self._show_image(text_cleaned, "4. Без линий сетки")
        
        # 5. Мягкое шумоподавление
        # Закрываем небольшие разрывы в символах
        closing_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        text_cleaned = cv2.morphologyEx(text_cleaned, cv2.MORPH_CLOSE, closing_kernel)
        
        # Удаляем очень мелкие объекты (шум)
        opening_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
        text_cleaned = cv2.morphologyEx(text_cleaned, cv2.MORPH_OPEN, opening_kernel)
        
        if show_steps:
            self._show_image(text_cleaned, "5. Шумоподавление")
        
        # 6. Применяем медианный фильтр для сглаживания
        text_cleaned = cv2.medianBlur(text_cleaned, 3)
        
        if show_steps:
            self._show_image(text_cleaned, "6. Финальная очистка")
        
        return text_cleaned
        
    def preprocess_grid_captcha_advanced(self, image: np.ndarray, show_steps: bool = False) -> np.ndarray:
        """
        Продвинутая обработка капчи с защитной сеткой и искаженными цифрами
        """
        if show_steps:
            self._show_image(image, "1. Оригинал")
        
        # 1. Сильное увеличение изображения
        height, width = image.shape[:2]
        scale_factor = 4  # Увеличиваем в 4 раза
        enlarged = cv2.resize(image, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_CUBIC)
        
        if show_steps:
            self._show_image(enlarged, "2. Увеличено в 4 раза")
        
        # 2. Работаем с каналами цвета отдельно
        # Конвертируем в разные цветовые пространства
        
        # RGB каналы
        b, g, r = cv2.split(enlarged)
        
        # HSV
        hsv = cv2.cvtColor(enlarged, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        
        # LAB
        lab = cv2.cvtColor(enlarged, cv2.COLOR_BGR2LAB)
        l, a, b_lab = cv2.split(lab)
        
        # 3. Находим темные области (цифры) в разных каналах
        masks = []
        
        # Маска из канала яркости (V)
        mask_v = cv2.threshold(v, 100, 255, cv2.THRESH_BINARY_INV)[1]
        masks.append(mask_v)
        
        # Маска из канала L (яркость в LAB)
        mask_l = cv2.threshold(l, 120, 255, cv2.THRESH_BINARY_INV)[1]
        masks.append(mask_l)
        
        # Маска из синего канала (часто цифры темнее)
        mask_b = cv2.threshold(b, 80, 255, cv2.THRESH_BINARY_INV)[1]
        masks.append(mask_b)
        
        if show_steps:
            combined_mask = cv2.bitwise_or(cv2.bitwise_or(mask_v, mask_l), mask_b)
            self._show_image(combined_mask, "3. Объединенная маска")
        
        # 4. Комбинируем маски
        text_mask = np.zeros_like(mask_v)
        for mask in masks:
            text_mask = cv2.bitwise_or(text_mask, mask)
        
        # 5. Удаляем линии сетки более агрессивно
        # Горизонтальные линии
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (50, 1))
        horizontal_lines = cv2.morphologyEx(text_mask, cv2.MORPH_OPEN, horizontal_kernel)
        
        # Вертикальные линии
        vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 50))
        vertical_lines = cv2.morphologyEx(text_mask, cv2.MORPH_OPEN, vertical_kernel)
        
        # Диагональные линии
        diagonal_kernel1 = np.array([[0,0,1],[0,1,0],[1,0,0]], dtype=np.uint8)
        diagonal_kernel2 = np.array([[1,0,0],[0,1,0],[0,0,1]], dtype=np.uint8)
        diagonal_lines1 = cv2.morphologyEx(text_mask, cv2.MORPH_OPEN, diagonal_kernel1)
        diagonal_lines2 = cv2.morphologyEx(text_mask, cv2.MORPH_OPEN, diagonal_kernel2)
        
        # Убираем все линии
        text_cleaned = cv2.subtract(text_mask, horizontal_lines)
        text_cleaned = cv2.subtract(text_cleaned, vertical_lines)
        text_cleaned = cv2.subtract(text_cleaned, diagonal_lines1)
        text_cleaned = cv2.subtract(text_cleaned, diagonal_lines2)
        
        if show_steps:
            self._show_image(text_cleaned, "4. Без линий сетки")
        
        # 6. Улучшаем символы
        # Закрываем разрывы в символах
        closing_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        text_cleaned = cv2.morphologyEx(text_cleaned, cv2.MORPH_CLOSE, closing_kernel)
        
        # Удаляем мелкий шум
        opening_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        text_cleaned = cv2.morphologyEx(text_cleaned, cv2.MORPH_OPEN, opening_kernel)
        
        if show_steps:
            self._show_image(text_cleaned, "5. Улучшенные символы")
        
        # 7. Утолщаем символы для лучшего распознавания
        dilate_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
        text_cleaned = cv2.dilate(text_cleaned, dilate_kernel, iterations=1)
        
        # 8. Финальная очистка по размеру компонентов
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(text_cleaned, connectivity=8)
        
        final_mask = np.zeros_like(text_cleaned)
        
        for i in range(1, num_labels):
            area = stats[i, cv2.CC_STAT_AREA]
            width = stats[i, cv2.CC_STAT_WIDTH]
            height = stats[i, cv2.CC_STAT_HEIGHT]
            
            # Фильтруем по размеру - оставляем только символы подходящего размера
            if (50 <= area <= 5000 and 
                10 <= width <= 100 and 
                15 <= height <= 120):
                final_mask[labels == i] = 255
        
        if show_steps:
            self._show_image(final_mask, "6. Финальный результат")
        
        return final_mask
    
    def preprocess_aggressive(self, image_path: str, show_steps: bool = False) -> np.ndarray:
        """
        Агрессивная обработка (старая версия) - для сравнения
        """
        original = cv2.imread(image_path)
        if original is None:
            raise ValueError(f"Не удалось загрузить изображение: {image_path}")
            
        if show_steps:
            self._show_image(original, "1. Оригинал")
            
        # Последовательная обработка
        step1 = self._enhance_contrast(original)
        if show_steps:
            self._show_image(step1, "2. Улучшение контраста")
            
        step2 = self._convert_to_grayscale(step1)
        if show_steps:
            self._show_image(step2, "3. Оттенки серого")
            
        step3 = self._remove_colored_lines(original)
        if show_steps:
            self._show_image(step3, "4. Удаление цветных линий")
            
        step4 = self._remove_grid_pattern(step3)
        if show_steps:
            self._show_image(step4, "5. Удаление сетки")
            
        step5 = self._denoise(step4)
        if show_steps:
            self._show_image(step5, "6. Шумоподавление")
            
        step6 = self._adaptive_threshold(step5)
        if show_steps:
            self._show_image(step6, "7. Адаптивная бинаризация")
            
        step7 = self._morphological_operations(step6)
        if show_steps:
            self._show_image(step7, "8. Морфологические операции")
            
        final = self._final_cleanup(step7)
        if show_steps:
            self._show_image(final, "9. Финальная очистка")
            
        return final
        
    def _enhance_contrast(self, image: np.ndarray) -> np.ndarray:
        """Улучшение контраста изображения"""
        # CLAHE (Contrast Limited Adaptive Histogram Equalization)
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        lab[:,:,0] = clahe.apply(lab[:,:,0])
        enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        return enhanced
        
    def _convert_to_grayscale(self, image: np.ndarray) -> np.ndarray:
        """Конвертация в оттенки серого с весами для лучшего контраста"""
        # Используем веса для лучшего выделения текста
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return gray
        
    def _remove_colored_lines(self, image: np.ndarray) -> np.ndarray:
        """Удаление цветных линий помех"""
        # Конвертируем в HSV для лучшей работы с цветами
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Маска для удаления красных и зеленых линий
        # Красный цвет
        lower_red1 = np.array([0, 50, 50])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([170, 50, 50])
        upper_red2 = np.array([180, 255, 255])
        
        mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask_red = mask_red1 + mask_red2
        
        # Зеленый цвет
        lower_green = np.array([40, 50, 50])
        upper_green = np.array([80, 255, 255])
        mask_green = cv2.inRange(hsv, lower_green, upper_green)
        
        # Синий цвет
        lower_blue = np.array([100, 50, 50])
        upper_blue = np.array([130, 255, 255])
        mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
        
        # Общая маска цветных линий
        color_mask = mask_red + mask_green + mask_blue
        
        # Инвертируем маску и применяем
        color_mask_inv = cv2.bitwise_not(color_mask)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        result = cv2.bitwise_and(gray, gray, mask=color_mask_inv)
        
        return result
        
    def _remove_grid_pattern(self, image: np.ndarray) -> np.ndarray:
        """Удаление сетчатого паттерна"""
        # Создаем ядра для обнаружения линий сетки
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
        vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))
        
        # Обнаруживаем горизонтальные линии
        horizontal_lines = cv2.morphologyEx(image, cv2.MORPH_OPEN, horizontal_kernel)
        horizontal_lines = cv2.dilate(horizontal_lines, horizontal_kernel, iterations=1)
        
        # Обнаруживаем вертикальные линии  
        vertical_lines = cv2.morphologyEx(image, cv2.MORPH_OPEN, vertical_kernel)
        vertical_lines = cv2.dilate(vertical_lines, vertical_kernel, iterations=1)
        
        # Удаляем линии сетки
        image_no_horizontal = cv2.subtract(image, horizontal_lines)
        result = cv2.subtract(image_no_horizontal, vertical_lines)
        
        return result
        
    def _denoise(self, image: np.ndarray) -> np.ndarray:
        """Шумоподавление"""
        # Применяем несколько методов шумоподавления
        # 1. Медианный фильтр
        denoised = cv2.medianBlur(image, 3)
        
        # 2. Гауссово размытие
        denoised = cv2.GaussianBlur(denoised, (3, 3), 0)
        
        # 3. Морфологическое закрытие для заполнения разрывов в символах
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
        denoised = cv2.morphologyEx(denoised, cv2.MORPH_CLOSE, kernel)
        
        return denoised
        
    def _adaptive_threshold(self, image: np.ndarray) -> np.ndarray:
        """Адаптивная бинаризация"""
        # Применяем адаптивную пороговую обработку
        binary = cv2.adaptiveThreshold(
            image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 11, 2
        )
        
        # Альтернативный метод - OTSU
        _, otsu = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Комбинируем результаты
        combined = cv2.bitwise_and(binary, otsu)
        
        return combined
        
    def _morphological_operations(self, image: np.ndarray) -> np.ndarray:
        """Морфологические операции для улучшения символов"""
        # Удаление мелких объектов
        kernel_small = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
        cleaned = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel_small)
        
        # Заполнение разрывов в символах
        kernel_close = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_CLOSE, kernel_close)
        
        return cleaned
        
    def _final_cleanup(self, image: np.ndarray) -> np.ndarray:
        """Финальная очистка и подготовка к распознаванию"""
        # Удаление очень мелких компонентов
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(image, connectivity=8)
        
        # Создаем маску для компонентов подходящего размера
        min_area = 20  # Минимальная площадь компонента
        max_area = image.shape[0] * image.shape[1] // 4  # Максимальная площадь
        
        cleaned = np.zeros_like(image)
        
        for i in range(1, num_labels):  # Пропускаем фон (i=0)
            area = stats[i, cv2.CC_STAT_AREA]
            if min_area <= area <= max_area:
                # Оставляем этот компонент
                cleaned[labels == i] = 255
                
        return cleaned
        
    def _show_image(self, image: np.ndarray, title: str):
        """Показ изображения для отладки"""
        if self.debug:
            plt.figure(figsize=(10, 6))
            if len(image.shape) == 3:
                plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            else:
                plt.imshow(image, cmap='gray')
            plt.title(title)
            plt.axis('off')
            plt.show()
    
    def get_character_regions(self, processed_image: np.ndarray) -> list:
        """Получение областей отдельных символов"""
        # Поиск контуров
        contours, _ = cv2.findContours(processed_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Фильтрация контуров по размеру
        char_regions = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            # Фильтруем по размеру (символы должны быть определенного размера)
            if 15 <= w <= 50 and 20 <= h <= 60:
                char_regions.append((x, y, w, h))
        
        # Сортируем по x-координате (слева направо)
        char_regions.sort(key=lambda region: region[0])
        
        return char_regions
        
    def extract_characters(self, processed_image: np.ndarray) -> list:
        """Извлечение отдельных символов из обработанного изображения"""
        regions = self.get_character_regions(processed_image)
        characters = []
        
        for x, y, w, h in regions:
            # Извлекаем символ с небольшим отступом
            char_img = processed_image[max(0, y-2):min(processed_image.shape[0], y+h+2),
                                     max(0, x-2):min(processed_image.shape[1], x+w+2)]
            
            # Нормализуем размер символа
            char_img = cv2.resize(char_img, (32, 32))
            characters.append(char_img)
            
        return characters
    
    def create_multiple_variants(self, image_path: str) -> list:
        """
        Создает множественные варианты обработки для улучшения распознавания
        """
        original = cv2.imread(image_path)
        if original is None:
            raise ValueError(f"Не удалось загрузить изображение: {image_path}")
        
        variants = []
        
        # 1. Мягкая обработка
        gentle = self.preprocess_grid_captcha_gentle(original)
        variants.append(('gentle', gentle))
        
        # 2. Продвинутая обработка
        advanced = self.preprocess_grid_captcha_advanced(original)
        variants.append(('advanced', advanced))
        
        # 3. Только увеличение без агрессивной обработки
        enlarged = cv2.resize(original, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
        gray_enlarged = cv2.cvtColor(enlarged, cv2.COLOR_BGR2GRAY)
        variants.append(('enlarged_only', gray_enlarged))
        
        # 4. Простая бинаризация на увеличенном
        _, simple_binary = cv2.threshold(gray_enlarged, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        variants.append(('simple_binary', simple_binary))
        
        # 5. Инвертированная бинаризация
        inverted_binary = cv2.bitwise_not(simple_binary)
        variants.append(('inverted_binary', inverted_binary))
        
        # 6. Адаптивная пороговая обработка
        adaptive = cv2.adaptiveThreshold(gray_enlarged, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 4)
        variants.append(('adaptive', adaptive))
        
        # 7. Инвертированная адаптивная
        adaptive_inv = cv2.bitwise_not(adaptive)
        variants.append(('adaptive_inv', adaptive_inv))
        
        return variants 