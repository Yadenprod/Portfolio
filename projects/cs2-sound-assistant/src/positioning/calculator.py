#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Модуль расчета позиций для CS2 Sound Assistant
Рассчитывает позиции источников звука на основе стерео аудио
"""

import numpy as np
import scipy.signal as signal
from scipy.fft import fft, fftfreq
from typing import Dict, Optional, Tuple
import math
import time

class PositionCalculator:
    """Класс для расчета позиций источников звука"""
    
    def __init__(self, config):
        self.config = config
        self.sample_rate = config.get('audio.sample_rate', 48000)
        self.chunk_size = config.get('audio.chunk_size', 1024)
        
        # Физические параметры
        self.ear_distance = config.get('positioning.ear_distance', 0.15)  # 15см между ушами
        self.sound_speed = config.get('positioning.sound_speed', 343)      # м/с скорость звука
        self.max_distance = config.get('positioning.max_distance', 50)     # максимальная дистанция
        
        # Калибровочные параметры
        self.calibration_data = config.get('calibration', {})
        self.distance_calibration = self.calibration_data.get('distance_calibration', {})
        self.angle_calibration = self.calibration_data.get('angle_calibration', {})
        
        # Параметры алгоритмов
        self.correlation_threshold = 0.3
        self.phase_threshold = 0.1
        self.amplitude_threshold = 0.05
        
    def initialize(self):
        """Инициализация калькулятора позиций"""
        print("📍 Инициализация калькулятора позиций...")
        
        # Загрузка калибровочных данных
        self.load_calibration()
        
        print("✅ Калькулятор позиций инициализирован")
    
    def load_calibration(self):
        """Загрузка калибровочных данных"""
        if self.calibration_data:
            print("📊 Загружены калибровочные данные")
        else:
            print("⚠️ Калибровочные данные не найдены, используются значения по умолчанию")
    
    def calculate_position(self, left_channel: np.ndarray, right_channel: np.ndarray) -> Optional[Dict]:
        """Расчет позиции источника звука"""
        if left_channel is None or right_channel is None:
            return None
        
        if len(left_channel) != len(right_channel):
            return None
        
        try:
            # Проверка амплитуды
            if not self.check_amplitude(left_channel, right_channel):
                return None
            
            # Расчет угла по разности фаз
            angle = self.calculate_angle(left_channel, right_channel)
            
            if angle is None:
                return None
            
            # Расчет дистанции по амплитуде
            distance = self.calculate_distance(left_channel, right_channel)
            
            # Применение калибровки
            calibrated_angle = self.apply_angle_calibration(angle)
            calibrated_distance = self.apply_distance_calibration(distance)
            
            # Проверка валидности
            if not self.validate_position(calibrated_angle, calibrated_distance):
                return None
            
            return {
                'angle': calibrated_angle,
                'distance': calibrated_distance,
                'raw_angle': angle,
                'raw_distance': distance,
                'confidence': self.calculate_position_confidence(left_channel, right_channel),
                'timestamp': time.time()
            }
            
        except Exception as e:
            print(f"❌ Ошибка расчета позиции: {e}")
            return None
    
    def check_amplitude(self, left_channel: np.ndarray, right_channel: np.ndarray) -> bool:
        """Проверка амплитуды аудио"""
        # RMS амплитуда для обоих каналов
        left_rms = np.sqrt(np.mean(left_channel**2))
        right_rms = np.sqrt(np.mean(right_channel**2))
        
        # Средняя амплитуда
        avg_rms = (left_rms + right_rms) / 2
        
        return avg_rms > self.amplitude_threshold
    
    def calculate_angle(self, left_channel: np.ndarray, right_channel: np.ndarray) -> Optional[float]:
        """Расчет угла источника звука"""
        try:
            # Корреляционный анализ
            correlation = self.cross_correlation(left_channel, right_channel)
            
            if correlation is None:
                return None
            
            # Нахождение пика корреляции
            peak_index = np.argmax(correlation)
            peak_value = correlation[peak_index]
            
            if peak_value < self.correlation_threshold:
                return None
            
            # Расчет задержки
            delay = peak_index - len(left_channel) // 2
            
            # Расчет угла по задержке
            angle = self.delay_to_angle(delay)
            
            return angle
            
        except Exception as e:
            print(f"❌ Ошибка расчета угла: {e}")
            return None
    
    def cross_correlation(self, left_channel: np.ndarray, right_channel: np.ndarray) -> Optional[np.ndarray]:
        """Кросс-корреляция между каналами"""
        try:
            # Нормализация
            left_norm = left_channel / np.max(np.abs(left_channel))
            right_norm = right_channel / np.max(np.abs(right_channel))
            
            # Корреляция
            correlation = signal.correlate(left_norm, right_norm, mode='full')
            
            return correlation
            
        except Exception:
            return None
    
    def delay_to_angle(self, delay: int) -> float:
        """Преобразование задержки в угол"""
        # Задержка в секундах
        delay_time = delay / self.sample_rate
        
        # Расчет угла по формуле ITD (Interaural Time Difference)
        # sin(θ) = (c * Δt) / d
        # где c - скорость звука, Δt - задержка, d - расстояние между ушами
        
        if abs(delay_time) > self.ear_distance / self.sound_speed:
            # Ограничение максимального угла
            return 90.0 if delay_time > 0 else -90.0
        
        angle_rad = math.asin((self.sound_speed * delay_time) / self.ear_distance)
        angle_deg = math.degrees(angle_rad)
        
        return angle_deg
    
    def calculate_distance(self, left_channel: np.ndarray, right_channel: np.ndarray) -> float:
        """Расчет дистанции по амплитуде"""
        # RMS амплитуда для обоих каналов
        left_rms = np.sqrt(np.mean(left_channel**2))
        right_rms = np.sqrt(np.mean(right_channel**2))
        
        # Средняя амплитуда
        avg_rms = (left_rms + right_rms) / 2
        
        # Простая модель дистанции (требует калибровки)
        # Предполагаем, что амплитуда обратно пропорциональна квадрату дистанции
        if avg_rms <= 0:
            return self.max_distance
        
        # Нормализованная дистанция (0-1)
        normalized_distance = 1.0 / (avg_rms + 0.01)
        
        # Преобразование в реальную дистанцию
        distance = normalized_distance * self.max_distance
        
        return min(distance, self.max_distance)
    
    def apply_angle_calibration(self, angle: float) -> float:
        """Применение калибровки угла"""
        if not self.angle_calibration:
            return angle
        
        # Простая линейная калибровка
        offset = self.angle_calibration.get('offset', 0)
        scale = self.angle_calibration.get('scale', 1.0)
        
        calibrated_angle = (angle + offset) * scale
        
        # Ограничение диапазона
        return max(-180, min(180, calibrated_angle))
    
    def apply_distance_calibration(self, distance: float) -> float:
        """Применение калибровки дистанции"""
        if not self.distance_calibration:
            return distance
        
        # Простая линейная калибровка
        offset = self.distance_calibration.get('offset', 0)
        scale = self.distance_calibration.get('scale', 1.0)
        
        calibrated_distance = (distance + offset) * scale
        
        # Ограничение диапазона
        return max(0, min(self.max_distance, calibrated_distance))
    
    def validate_position(self, angle: float, distance: float) -> bool:
        """Проверка валидности позиции"""
        # Проверка угла
        if not (-180 <= angle <= 180):
            return False
        
        # Проверка дистанции
        if not (0 <= distance <= self.max_distance):
            return False
        
        return True
    
    def calculate_position_confidence(self, left_channel: np.ndarray, right_channel: np.ndarray) -> float:
        """Расчет уверенности в позиции"""
        try:
            # Корреляция между каналами
            correlation = self.cross_correlation(left_channel, right_channel)
            
            if correlation is None:
                return 0.0
            
            # Максимальная корреляция
            max_correlation = np.max(correlation)
            
            # Отношение сигнал/шум
            signal_level = np.max([np.sqrt(np.mean(left_channel**2)), np.sqrt(np.mean(right_channel**2))])
            noise_level = np.median(np.abs(left_channel - right_channel))
            
            if noise_level == 0:
                snr = 1.0
            else:
                snr = min(signal_level / noise_level, 10.0) / 10.0
            
            # Итоговая уверенность
            confidence = max_correlation * 0.7 + snr * 0.3
            
            return min(confidence, 1.0)
            
        except Exception:
            return 0.0
    
    def update_calibration(self, calibration_data: dict):
        """Обновление калибровочных данных"""
        self.calibration_data.update(calibration_data)
        self.distance_calibration = self.calibration_data.get('distance_calibration', {})
        self.angle_calibration = self.calibration_data.get('angle_calibration', {})
        
        print("🔄 Калибровочные данные обновлены")
    
    def get_calibration_info(self) -> dict:
        """Получение информации о калибровке"""
        return {
            'ear_distance': self.ear_distance,
            'sound_speed': self.sound_speed,
            'max_distance': self.max_distance,
            'distance_calibration': self.distance_calibration,
            'angle_calibration': self.angle_calibration
        }
    
    def reset_calibration(self):
        """Сброс калибровки"""
        self.calibration_data = {}
        self.distance_calibration = {}
        self.angle_calibration = {}
        
        print("🔄 Калибровка сброшена")
