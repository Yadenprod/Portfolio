#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Модуль анализа звуков для CS2 Sound Assistant
Анализирует аудио данные и определяет типы звуков CS2
"""

import numpy as np
import scipy.signal as signal
from scipy.fft import fft, fftfreq
from typing import List, Dict, Optional
import time

class SoundAnalyzer:
    """Класс для анализа звуков CS2"""
    
    def __init__(self, config):
        """Инициализация анализатора звуков"""
        self.config = config
        self.sample_rate = config.get('audio.sample_rate', 48000)
        self.chunk_size = config.get('audio.chunk_size', 1024)
        
        # Фильтры для разных типов звуков
        self.footstep_filter = None
        self.gunshot_filter = None
        self.explosion_filter = None
        self.voice_filter = None
        
        # Паттерны звуков CS2
        self.cs2_sound_patterns = {
            'footsteps': {
                'freq_range': (100, 1000),
                'duration_range': (0.1, 0.5),
                'amplitude_threshold': 0.1
            },
            'gunshot': {
                'freq_range': (1000, 5000),
                'duration_range': (0.05, 0.2),
                'amplitude_threshold': 0.2
            },
            'explosion': {
                'freq_range': (50, 2000),
                'duration_range': (0.2, 1.0),
                'amplitude_threshold': 0.3
            },
            'voice': {
                'freq_range': (200, 3000),
                'duration_range': (0.1, 2.0),
                'amplitude_threshold': 0.15
            }
        }
        
        # Статистика
        self.analysis_count = 0
        self.analysis_time = 0
        self.sounds_detected = 0
        
        # Фильтры для исключения нежелательных звуков
        self.filters = {
            'voice_filter': config.get('filters.voice_filter', True),
            'music_filter': config.get('filters.music_filter', True),
            'noise_filter': config.get('filters.noise_filter', True)
        }
    
    def initialize(self):
        """Инициализация анализатора"""
        print("🔍 Инициализация анализатора звуков...")
        
        # Создание фильтров
        self.create_filters()
        
        print("✅ Анализатор звуков инициализирован")
    
    def create_filters(self):
        """Создание фильтров для обработки аудио"""
        # Фильтр низких частот для шума
        b, a = signal.butter(4, 8000, fs=self.sample_rate, btype='low')
        self.lowpass_filter = (b, a)
        
        # Фильтр высоких частот для голоса
        b, a = signal.butter(4, 300, fs=self.sample_rate, btype='high')
        self.highpass_filter = (b, a)
        
        # Полосовой фильтр для шагов
        b, a = signal.butter(4, [100, 2000], fs=self.sample_rate, btype='band')
        self.footstep_filter = (b, a)
    
    def analyze_audio(self, audio_data: np.ndarray) -> Optional[dict]:
        """Анализ аудио данных"""
        try:
            if audio_data is None or len(audio_data) == 0:
                return None
            
            # Отладочная информация
            if hasattr(self, '_debug_counter'):
                self._debug_counter += 1
            else:
                self._debug_counter = 0
                
            if self._debug_counter % 50 == 0:
                print(f"🔍 Анализатор получил данные: форма={audio_data.shape}")
            
            # Фильтрация аудио
            filtered_audio = self.filter_audio(audio_data)
            if filtered_audio is None:
                return None
            
            # FFT анализ
            fft_result = self.fft_analysis(filtered_audio)
            if fft_result is None:
                return None
            
            # Классификация звука
            sound_type = self.classify_sound(fft_result)
            
            # Расчет позиции
            position = self.calculate_position(filtered_audio)
            
            # Обновление статистики
            self.analysis_count += 1
            self.analysis_time = time.time()
            
            # Отладочная информация для обнаружений
            if sound_type:
                print(f"🎯 Звук классифицирован: {sound_type}, позиция={position}")
            
            return {
                'type': sound_type,
                'position': position,
                'fft': fft_result,
                'timestamp': time.time()
            }
            
        except Exception as e:
            print(f"❌ Ошибка анализа аудио: {e}")
            return None
    
    def check_amplitude(self, audio_data: np.ndarray) -> bool:
        """Проверка амплитуды аудио"""
        # RMS (Root Mean Square) амплитуда
        rms = np.sqrt(np.mean(audio_data**2))
        
        return rms > self.amplitude_threshold
    
    def filter_audio(self, audio_data: np.ndarray) -> Optional[np.ndarray]:
        """Фильтрация аудио данных"""
        try:
            filtered = audio_data.copy()
            
            # Применение фильтров
            if self.filters['noise_filter']:
                # Применяем фильтр к каждому каналу отдельно
                if len(filtered.shape) > 1:
                    for channel in range(filtered.shape[1]):
                        filtered[:, channel] = signal.filtfilt(*self.lowpass_filter, filtered[:, channel])
                else:
                    filtered = signal.filtfilt(*self.lowpass_filter, filtered)
            
            if self.filters['voice_filter']:
                # Исключение частот голоса
                fft_data = fft(filtered, axis=0)
                freqs = fftfreq(len(filtered), 1/self.sample_rate)
                
                # Маска для исключения частот голоса
                voice_mask = (freqs >= 300) & (freqs <= 3400)
                fft_data[voice_mask] = 0
                
                filtered = np.real(np.fft.ifft(fft_data, axis=0))
            
            return filtered
            
        except Exception as e:
            print(f"❌ Ошибка фильтрации аудио: {e}")
            return None
    
    def fft_analysis(self, audio_data: np.ndarray) -> tuple:
        """FFT анализ аудио данных"""
        # Применение окна Хэмминга
        window = np.hamming(len(audio_data))
        windowed_data = audio_data * window[:, np.newaxis]
        
        # FFT
        fft_data = fft(windowed_data, axis=0)
        frequencies = fftfreq(len(audio_data), 1/self.sample_rate)
        
        # Мощность спектра
        power_spectrum = np.abs(fft_data)**2
        
        # Усреднение по каналам
        if len(power_spectrum.shape) > 1:
            power_spectrum = np.mean(power_spectrum, axis=1)
        
        return frequencies, power_spectrum
    
    def classify_sound(self, fft_result):
        """Классификация звука"""
        try:
            # fft_result приходит как кортеж (frequencies, power_spectrum)
            if isinstance(fft_result, tuple):
                frequencies, power_spectrum = fft_result
            else:
                # Если это словарь
                frequencies = fft_result['frequencies']
                power_spectrum = fft_result['power_spectrum']
            
            # Упрощенная классификация
            max_power = np.max(power_spectrum)
            dominant_freq = frequencies[np.argmax(power_spectrum)]
            
            # Классификация по частотам и мощности
            if dominant_freq < 100 and max_power > 0.1:
                return {'type': 'footsteps', 'confidence': min(max_power, 1.0)}
            elif dominant_freq > 2000 and max_power > 0.05:
                return {'type': 'gunshot', 'confidence': min(max_power, 1.0)}
            elif dominant_freq > 1000 and max_power > 0.08:
                return {'type': 'explosion', 'confidence': min(max_power, 1.0)}
            elif 200 < dominant_freq < 2000 and max_power > 0.03:
                return {'type': 'voice', 'confidence': min(max_power, 1.0)}
            else:
                return {'type': 'unknown', 'confidence': min(max_power, 1.0)}
                
        except Exception as e:
            print(f"❌ Ошибка классификации звука: {e}")
            return {'type': 'unknown', 'confidence': 0.0}
    
    def calculate_pattern_score(self, frequencies: np.ndarray, power_spectrum: np.ndarray, pattern: dict) -> float:
        """Расчет оценки совпадения с паттерном"""
        freq_range = pattern['freq_range']
        amp_range = pattern['amplitude_range']
        
        # Фильтрация по диапазону частот
        freq_mask = (frequencies >= freq_range[0]) & (frequencies <= freq_range[1])
        filtered_powers = power_spectrum[freq_mask]
        
        if len(filtered_powers) == 0:
            return 0
        
        # Нормализация амплитуды
        max_power = np.max(filtered_powers)
        normalized_power = max_power / np.max(power_spectrum)
        
        # Проверка амплитуды
        if not (amp_range[0] <= normalized_power <= amp_range[1]):
            return 0
        
        # Расчет оценки на основе распределения мощности
        power_distribution = np.sum(filtered_powers) / np.sum(power_spectrum)
        
        return power_distribution * normalized_power
    
    def calculate_confidence(self, frequencies: np.ndarray, power_spectrum: np.ndarray, sound_type: str) -> float:
        """Расчет уверенности в определении звука"""
        pattern = self.cs2_sound_patterns[sound_type]
        
        # Базовое совпадение с паттерном
        pattern_score = self.calculate_pattern_score(frequencies, power_spectrum, pattern)
        
        # Дополнительные факторы
        signal_to_noise = self.calculate_snr(power_spectrum)
        frequency_stability = self.calculate_frequency_stability(frequencies, power_spectrum)
        
        # Итоговая уверенность
        confidence = pattern_score * 0.6 + signal_to_noise * 0.3 + frequency_stability * 0.1
        
        return min(confidence, 1.0)
    
    def calculate_snr(self, power_spectrum: np.ndarray) -> float:
        """Расчет отношения сигнал/шум"""
        sorted_powers = np.sort(power_spectrum)
        
        # Шум как медиана нижних 50% значений
        noise_level = np.median(sorted_powers[:len(sorted_powers)//2])
        
        # Сигнал как максимальное значение
        signal_level = np.max(power_spectrum)
        
        if noise_level == 0:
            return 1.0
        
        snr = signal_level / noise_level
        return min(snr / 100, 1.0)  # Нормализация
    
    def calculate_frequency_stability(self, frequencies: np.ndarray, power_spectrum: np.ndarray) -> float:
        """Расчет стабильности частот"""
        # Нахождение пиков
        peaks = signal.find_peaks(power_spectrum, height=np.max(power_spectrum)*0.1)[0]
        
        if len(peaks) < 2:
            return 0.5
        
        # Стабильность как обратная величина разброса частот
        peak_freqs = frequencies[peaks]
        freq_spread = np.std(peak_freqs)
        
        # Нормализация
        stability = 1.0 / (1.0 + freq_spread / 1000)
        return min(stability, 1.0)
    
    def analyze_duration(self, audio_data: np.ndarray) -> float:
        """Анализ длительности звука"""
        # Простая оценка длительности
        return len(audio_data) / self.sample_rate
    
    def calculate_position(self, audio_data):
        """Расчет позиции звука"""
        try:
            if audio_data is None or len(audio_data) == 0:
                return {'angle': 0, 'distance': 0}
            
            # Простой расчет позиции на основе стерео каналов
            if audio_data.shape[1] >= 2:  # Стерео
                left_channel = audio_data[:, 0]
                right_channel = audio_data[:, 1]
                
                # Расчет угла на основе разности амплитуд
                left_amplitude = np.sqrt(np.mean(left_channel**2))
                right_amplitude = np.sqrt(np.mean(right_channel**2))
                
                # Нормализация
                total_amplitude = left_amplitude + right_amplitude
                if total_amplitude > 0:
                    left_ratio = left_amplitude / total_amplitude
                    right_ratio = right_amplitude / total_amplitude
                    
                    # Расчет угла (-90 до +90 градусов)
                    angle = (right_ratio - left_ratio) * 90
                else:
                    angle = 0
                
                # Расчет расстояния на основе общей амплитуды
                distance = min(1.0, total_amplitude * 10)  # Нормализация
                
                return {
                    'angle': angle,
                    'distance': distance
                }
            else:
                return {'angle': 0, 'distance': 0}
                
        except Exception as e:
            print(f"❌ Ошибка расчета позиции: {e}")
            return {'angle': 0, 'distance': 0}
    
    def get_statistics(self) -> dict:
        """Получение статистики анализа"""
        return {
            'sounds_detected': self.sounds_detected,
            'analysis_time': self.analysis_time,
            'patterns': self.cs2_sound_patterns,
            'filters': self.filters
        }
    
    def update_patterns(self, new_patterns: dict):
        """Обновление паттернов звуков"""
        self.cs2_sound_patterns.update(new_patterns)
        print("🔄 Паттерны звуков обновлены")
    
    def reset_statistics(self):
        """Сброс статистики"""
        self.sounds_detected = 0
        self.analysis_time = 0
        print("🔄 Статистика анализа сброшена")
