#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ИИ анализатор позиций звуков CS2
"""

import numpy as np
import librosa
import tensorflow as tf
from tensorflow import keras
from sklearn.preprocessing import StandardScaler
import joblib
import os
from typing import Dict, List, Tuple, Optional
import logging
from scipy import signal
from scipy.spatial.distance import cdist

class CS2PositionAnalyzer:
    """ИИ анализатор позиций звуков CS2"""
    
    def __init__(self, model_path: str = "models/position_analyzer.h5"):
        self.model_path = model_path
        self.model = None
        self.scaler = StandardScaler()
        self.sample_rate = 48000
        self.feature_length = 256
        
        # Параметры анализа
        self.min_confidence = 0.3
        self.max_distance = 200  # метров
        self.angle_resolution = 1  # градус
        
        self._load_model()
    
    def _load_model(self):
        """Загрузка обученной модели"""
        try:
            if os.path.exists(self.model_path):
                self.model = keras.models.load_model(self.model_path)
                print(f"✅ Модель позиций загружена: {self.model_path}")
            else:
                print("⚠️ Модель позиций не найдена, создаем новую")
                self._create_model()
        except Exception as e:
            print(f"❌ Ошибка загрузки модели позиций: {e}")
            self._create_model()
    
    def _create_model(self):
        """Создание новой модели для анализа позиций"""
        try:
            # Архитектура для регрессии позиций
            self.model = keras.Sequential([
                keras.layers.Dense(256, activation='relu', input_shape=(self.feature_length,)),
                keras.layers.Dropout(0.3),
                keras.layers.Dense(128, activation='relu'),
                keras.layers.Dropout(0.3),
                keras.layers.Dense(64, activation='relu'),
                keras.layers.Dense(2)  # angle, distance
            ])
            
            self.model.compile(
                optimizer='adam',
                loss='mse',
                metrics=['mae']
            )
            
            print("✅ Новая модель позиций создана")
        except Exception as e:
            print(f"❌ Ошибка создания модели позиций: {e}")
    
    def extract_position_features(self, audio_data: np.ndarray) -> np.ndarray:
        """Извлечение признаков для анализа позиций"""
        try:
            # Проверка на стерео
            if len(audio_data.shape) == 1:
                # Моно - создаем искусственное стерео
                audio_data = np.column_stack([audio_data, audio_data])
            
            left_channel = audio_data[:, 0]
            right_channel = audio_data[:, 1]
            
            features = []
            
            # 1. Разность амплитуд (ITD - Interaural Time Difference)
            amplitude_diff = np.abs(left_channel) - np.abs(right_channel)
            features.extend([
                np.mean(amplitude_diff),
                np.std(amplitude_diff),
                np.max(amplitude_diff),
                np.min(amplitude_diff)
            ])
            
            # 2. Корреляция между каналами
            correlation = np.corrcoef(left_channel, right_channel)[0, 1]
            features.append(correlation if not np.isnan(correlation) else 0)
            
            # 3. Спектральные признаки
            for channel in [left_channel, right_channel]:
                # FFT
                fft = np.fft.fft(channel)
                fft_magnitude = np.abs(fft)
                
                # Спектральные моменты
                freqs = np.fft.fftfreq(len(channel), 1/self.sample_rate)
                positive_freqs = freqs > 0
                
                if np.any(positive_freqs):
                    features.extend([
                        np.mean(fft_magnitude[positive_freqs]),
                        np.std(fft_magnitude[positive_freqs]),
                        np.max(fft_magnitude[positive_freqs]),
                        np.sum(fft_magnitude[positive_freqs])
                    ])
                else:
                    features.extend([0, 0, 0, 0])
            
            # 4. MFCC признаки
            mfcc_left = librosa.feature.mfcc(y=left_channel.astype(np.float32), sr=self.sample_rate, n_mfcc=13)
            mfcc_right = librosa.feature.mfcc(y=right_channel.astype(np.float32), sr=self.sample_rate, n_mfcc=13)
            
            # Средние значения MFCC
            features.extend(np.mean(mfcc_left, axis=1))
            features.extend(np.mean(mfcc_right, axis=1))
            
            # 5. Энергетические признаки
            energy_left = np.sum(left_channel**2)
            energy_right = np.sum(right_channel**2)
            total_energy = energy_left + energy_right
            
            features.extend([
                energy_left,
                energy_right,
                total_energy,
                energy_left / total_energy if total_energy > 0 else 0.5,
                energy_right / total_energy if total_energy > 0 else 0.5
            ])
            
            # 6. Временные признаки
            features.extend([
                len(audio_data) / self.sample_rate,  # длительность
                np.max(np.abs(audio_data)),  # пиковая амплитуда
                np.mean(np.abs(audio_data))  # средняя амплитуда
            ])
            
            # Дополнение до нужной длины
            while len(features) < self.feature_length:
                features.append(0)
            
            # Обрезка если слишком много
            features = features[:self.feature_length]
            
            return np.array(features)
            
        except Exception as e:
            print(f"❌ Ошибка извлечения признаков позиции: {e}")
            return np.zeros(self.feature_length)
    
    def calculate_position(self, audio_data: np.ndarray, sound_type: str = 'unknown') -> Dict:
        """Расчет позиции звука с помощью ИИ"""
        try:
            # Извлечение признаков
            features = self.extract_position_features(audio_data)
            
            # Нормализация
            features_scaled = self.scaler.fit_transform(features.reshape(1, -1))
            
            if self.model is not None:
                # Предсказание с помощью ИИ
                prediction = self.model.predict(features_scaled, verbose=0)[0]
                predicted_angle = float(prediction[0])
                predicted_distance = float(prediction[1])
            else:
                # Fallback на традиционные методы
                predicted_angle, predicted_distance = self._traditional_position_analysis(audio_data)
            
            # Ограничения
            predicted_angle = np.clip(predicted_angle, -180, 180)
            predicted_distance = np.clip(predicted_distance, 1, self.max_distance)
            
            # Дополнительная информация
            position_info = {
                'angle': predicted_angle,
                'distance': predicted_distance,
                'confidence': self._calculate_position_confidence(audio_data, sound_type),
                'method': 'ai' if self.model is not None else 'traditional',
                'raw_features': features.tolist()
            }
            
            return position_info
            
        except Exception as e:
            print(f"❌ Ошибка расчета позиции: {e}")
            return {
                'angle': 0.0,
                'distance': 50.0,
                'confidence': 0.0,
                'method': 'error',
                'raw_features': []
            }
    
    def _traditional_position_analysis(self, audio_data: np.ndarray) -> Tuple[float, float]:
        """Традиционный анализ позиций (fallback)"""
        try:
            if len(audio_data.shape) == 1:
                # Моно - нет информации о направлении
                return 0.0, 50.0
            
            left_channel = audio_data[:, 0]
            right_channel = audio_data[:, 1]
            
            # Расчет угла через разность амплитуд
            left_energy = np.sum(left_channel**2)
            right_energy = np.sum(right_channel**2)
            total_energy = left_energy + right_energy
            
            if total_energy > 0:
                # Нормализованная разность энергий
                energy_diff = (left_energy - right_energy) / total_energy
                # Преобразование в угол (приблизительно)
                angle = energy_diff * 90  # ±90 градусов
            else:
                angle = 0.0
            
            # Расчет дистанции через общую энергию
            # Чем громче звук, тем ближе источник
            total_amplitude = np.max(np.abs(audio_data))
            # Нормализация к разумному диапазону
            distance = max(1, 100 - total_amplitude * 50)
            
            return angle, distance
            
        except Exception as e:
            print(f"❌ Ошибка традиционного анализа: {e}")
            return 0.0, 50.0
    
    def _calculate_position_confidence(self, audio_data: np.ndarray, sound_type: str) -> float:
        """Расчет уверенности в позиции"""
        try:
            confidence = 0.5  # базовая уверенность
            
            # Факторы, влияющие на уверенность:
            
            # 1. Качество стерео сигнала
            if len(audio_data.shape) > 1:
                left_channel = audio_data[:, 0]
                right_channel = audio_data[:, 1]
                
                # Разность между каналами
                channel_diff = np.mean(np.abs(left_channel - right_channel))
                channel_similarity = np.corrcoef(left_channel, right_channel)[0, 1]
                
                if not np.isnan(channel_similarity):
                    confidence += 0.2 * channel_similarity
                
                # Чем больше разность, тем лучше локализация
                if channel_diff > 0.1:
                    confidence += 0.1
            
            # 2. Энергия сигнала
            total_energy = np.sum(audio_data**2)
            if total_energy > 0.1:
                confidence += 0.1
            
            # 3. Тип звука
            sound_confidence = {
                'gunshot': 0.9,
                'explosion': 0.8,
                'footsteps': 0.7,
                'voice': 0.6,
                'reload': 0.7,
                'grenade': 0.8
            }
            
            confidence += sound_confidence.get(sound_type, 0.5) * 0.2
            
            return np.clip(confidence, 0.0, 1.0)
            
        except Exception as e:
            print(f"❌ Ошибка расчета уверенности: {e}")
            return 0.5
    
    def train_position_model(self, training_data: List[Tuple], epochs: int = 100):
        """Обучение модели позиций"""
        try:
            if not training_data:
                print("❌ Нет данных для обучения позиций")
                return
            
            X = []
            y = []
            
            for audio_data, (true_angle, true_distance) in training_data:
                features = self.extract_position_features(audio_data)
                X.append(features)
                y.append([true_angle, true_distance])
            
            X = np.array(X)
            y = np.array(y)
            
            # Нормализация
            X_scaled = self.scaler.fit_transform(X)
            
            # Обучение
            self.model.fit(X_scaled, y, epochs=epochs, validation_split=0.2)
            
            # Сохранение модели
            self.model.save(self.model_path)
            print(f"✅ Модель позиций обучена и сохранена: {self.model_path}")
            
        except Exception as e:
            print(f"❌ Ошибка обучения модели позиций: {e}")
    
    def get_position_info(self, angle: float, distance: float) -> Dict:
        """Информация о позиции"""
        return {
            'angle_degrees': angle,
            'angle_radians': np.radians(angle),
            'distance_meters': distance,
            'direction': self._get_direction_name(angle),
            'proximity': self._get_proximity_name(distance)
        }
    
    def _get_direction_name(self, angle: float) -> str:
        """Название направления"""
        if -22.5 <= angle <= 22.5:
            return "вперед"
        elif 22.5 < angle <= 67.5:
            return "вперед-право"
        elif 67.5 < angle <= 112.5:
            return "право"
        elif 112.5 < angle <= 157.5:
            return "назад-право"
        elif 157.5 < angle <= 180 or -180 <= angle <= -157.5:
            return "назад"
        elif -157.5 < angle <= -112.5:
            return "назад-лево"
        elif -112.5 < angle <= -67.5:
            return "лево"
        else:
            return "вперед-лево"
    
    def _get_proximity_name(self, distance: float) -> str:
        """Название близости"""
        if distance <= 10:
            return "очень близко"
        elif distance <= 25:
            return "близко"
        elif distance <= 50:
            return "средне"
        elif distance <= 100:
            return "далеко"
        else:
            return "очень далеко"
