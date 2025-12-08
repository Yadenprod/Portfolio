#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ИИ классификатор звуков CS2
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

class CS2SoundClassifier:
    """ИИ классификатор звуков CS2"""
    
    def __init__(self, model_path: str = "models/sound_classifier.h5"):
        self.model_path = model_path
        self.model = None
        self.scaler = StandardScaler()
        self.sample_rate = 48000
        self.feature_length = 128
        
        # Классы звуков CS2
        self.sound_classes = [
            'footsteps', 'gunshot', 'explosion', 'voice', 
            'reload', 'grenade', 'bomb_plant', 'bomb_defuse',
            'headshot', 'body_shot', 'wall_shot', 'unknown'
        ]
        
        self._load_model()
    
    def _load_model(self):
        """Загрузка обученной модели"""
        try:
            if os.path.exists(self.model_path):
                self.model = keras.models.load_model(self.model_path)
                print(f"✅ Модель загружена: {self.model_path}")
            else:
                print("⚠️ Модель не найдена, создаем новую")
                self._create_model()
        except Exception as e:
            print(f"❌ Ошибка загрузки модели: {e}")
            self._create_model()
    
    def _create_model(self):
        """Создание новой модели"""
        try:
            # Архитектура CNN для классификации звуков
            self.model = keras.Sequential([
                keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(self.feature_length, self.feature_length, 1)),
                keras.layers.MaxPooling2D((2, 2)),
                keras.layers.Conv2D(64, (3, 3), activation='relu'),
                keras.layers.MaxPooling2D((2, 2)),
                keras.layers.Conv2D(64, (3, 3), activation='relu'),
                keras.layers.Flatten(),
                keras.layers.Dense(128, activation='relu'),
                keras.layers.Dropout(0.5),
                keras.layers.Dense(len(self.sound_classes), activation='softmax')
            ])
            
            self.model.compile(
                optimizer='adam',
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy']
            )
            
            print("✅ Новая модель создана")
        except Exception as e:
            print(f"❌ Ошибка создания модели: {e}")
    
    def extract_features(self, audio_data: np.ndarray) -> np.ndarray:
        """Извлечение признаков из аудио"""
        try:
            # Преобразование в моно если стерео
            if len(audio_data.shape) > 1:
                audio_data = np.mean(audio_data, axis=1)
            
            # Извлечение MFCC признаков
            mfcc = librosa.feature.mfcc(
                y=audio_data.astype(np.float32), 
                sr=self.sample_rate,
                n_mfcc=self.feature_length
            )
            
            # Нормализация
            mfcc_scaled = self.scaler.fit_transform(mfcc)
            
            # Преобразование в квадратную матрицу для CNN
            if mfcc_scaled.shape[1] < self.feature_length:
                # Дополнение нулями
                padding = np.zeros((self.feature_length, self.feature_length - mfcc_scaled.shape[1]))
                mfcc_scaled = np.hstack([mfcc_scaled, padding])
            else:
                # Обрезка
                mfcc_scaled = mfcc_scaled[:, :self.feature_length]
            
            # Добавление размерности канала
            mfcc_scaled = mfcc_scaled.reshape(1, self.feature_length, self.feature_length, 1)
            
            return mfcc_scaled
            
        except Exception as e:
            print(f"❌ Ошибка извлечения признаков: {e}")
            return np.zeros((1, self.feature_length, self.feature_length, 1))
    
    def classify_sound(self, audio_data: np.ndarray) -> Dict:
        """Классификация звука с помощью ИИ"""
        try:
            if self.model is None:
                return {'type': 'unknown', 'confidence': 0.0}
            
            # Извлечение признаков
            features = self.extract_features(audio_data)
            
            # Предсказание
            predictions = self.model.predict(features, verbose=0)
            predicted_class = np.argmax(predictions[0])
            confidence = float(predictions[0][predicted_class])
            
            # Получение названия класса
            sound_type = self.sound_classes[predicted_class]
            
            return {
                'type': sound_type,
                'confidence': confidence,
                'predictions': predictions[0].tolist(),
                'all_classes': self.sound_classes
            }
            
        except Exception as e:
            print(f"❌ Ошибка классификации: {e}")
            return {'type': 'unknown', 'confidence': 0.0}
    
    def train_model(self, training_data: List[Tuple], epochs: int = 50):
        """Обучение модели"""
        try:
            if not training_data:
                print("❌ Нет данных для обучения")
                return
            
            X = []
            y = []
            
            for audio_data, label in training_data:
                features = self.extract_features(audio_data)
                X.append(features[0])  # Убираем batch dimension
                y.append(self.sound_classes.index(label))
            
            X = np.array(X)
            y = np.array(y)
            
            # Обучение
            self.model.fit(X, y, epochs=epochs, validation_split=0.2)
            
            # Сохранение модели
            self.model.save(self.model_path)
            print(f"✅ Модель обучена и сохранена: {self.model_path}")
            
        except Exception as e:
            print(f"❌ Ошибка обучения: {e}")
    
    def get_sound_info(self, sound_type: str) -> Dict:
        """Информация о типе звука"""
        sound_info = {
            'footsteps': {
                'description': 'Шаги игроков',
                'frequency_range': (20, 200),
                'duration_range': (0.1, 0.5),
                'typical_distance': 50
            },
            'gunshot': {
                'description': 'Выстрелы',
                'frequency_range': (1000, 8000),
                'duration_range': (0.05, 0.2),
                'typical_distance': 100
            },
            'explosion': {
                'description': 'Взрывы',
                'frequency_range': (50, 500),
                'duration_range': (0.3, 1.0),
                'typical_distance': 150
            },
            'voice': {
                'description': 'Голоса игроков',
                'frequency_range': (300, 3000),
                'duration_range': (0.5, 2.0),
                'typical_distance': 30
            },
            'reload': {
                'description': 'Перезарядка',
                'frequency_range': (500, 2000),
                'duration_range': (0.2, 0.8),
                'typical_distance': 40
            },
            'grenade': {
                'description': 'Гранаты',
                'frequency_range': (200, 1000),
                'duration_range': (0.5, 1.5),
                'typical_distance': 80
            }
        }
        
        return sound_info.get(sound_type, {
            'description': 'Неизвестный звук',
            'frequency_range': (0, 0),
            'duration_range': (0, 0),
            'typical_distance': 0
        })
