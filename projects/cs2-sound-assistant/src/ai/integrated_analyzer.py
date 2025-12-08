#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Интегрированный ИИ анализатор CS2
"""

import numpy as np
import time
from typing import Dict, List, Optional, Tuple
import logging
from .sound_classifier import CS2SoundClassifier
from .position_analyzer import CS2PositionAnalyzer

class CS2IntegratedAnalyzer:
    """Интегрированный ИИ анализатор CS2"""
    
    def __init__(self):
        self.sound_classifier = CS2SoundClassifier()
        self.position_analyzer = CS2PositionAnalyzer()
        self.sample_rate = 48000
        
        # Статистика
        self.detection_count = 0
        self.sound_type_stats = {}
        self.position_stats = {
            'angles': [],
            'distances': []
        }
        
        # Настройки
        self.min_confidence = 0.3
        self.enable_ai = True
        self.enable_traditional = True
        
        print("🤖 Интегрированный ИИ анализатор CS2 инициализирован")
    
    def analyze_audio(self, audio_data: np.ndarray) -> Dict:
        """Полный анализ аудио с ИИ"""
        try:
            start_time = time.time()
            
            # 1. Классификация звука
            sound_result = self._classify_sound(audio_data)
            
            # 2. Анализ позиции
            position_result = self._analyze_position(audio_data, sound_result['type'])
            
            # 3. Интеграция результатов
            integrated_result = self._integrate_results(sound_result, position_result)
            
            # 4. Обновление статистики
            self._update_statistics(integrated_result)
            
            # 5. Добавление метаданных
            integrated_result.update({
                'timestamp': time.time(),
                'processing_time': time.time() - start_time,
                'analyzer_version': '2.0',
                'ai_enabled': self.enable_ai,
                'detection_id': self.detection_count
            })
            
            self.detection_count += 1
            
            return integrated_result
            
        except Exception as e:
            print(f"❌ Ошибка интегрированного анализа: {e}")
            return self._get_fallback_result()
    
    def _classify_sound(self, audio_data: np.ndarray) -> Dict:
        """Классификация звука"""
        try:
            if self.enable_ai and self.sound_classifier.model is not None:
                # ИИ классификация
                result = self.sound_classifier.classify_sound(audio_data)
                result['method'] = 'ai'
            else:
                # Традиционная классификация
                result = self._traditional_sound_classification(audio_data)
                result['method'] = 'traditional'
            
            return result
            
        except Exception as e:
            print(f"❌ Ошибка классификации звука: {e}")
            return {'type': 'unknown', 'confidence': 0.0, 'method': 'error'}
    
    def _analyze_position(self, audio_data: np.ndarray, sound_type: str) -> Dict:
        """Анализ позиции"""
        try:
            if self.enable_ai and self.position_analyzer.model is not None:
                # ИИ анализ позиции
                result = self.position_analyzer.calculate_position(audio_data, sound_type)
                result['method'] = 'ai'
            else:
                # Традиционный анализ позиции
                result = self.position_analyzer._traditional_position_analysis(audio_data)
                result = {
                    'angle': result[0],
                    'distance': result[1],
                    'confidence': 0.5,
                    'method': 'traditional'
                }
            
            return result
            
        except Exception as e:
            print(f"❌ Ошибка анализа позиции: {e}")
            return {'angle': 0.0, 'distance': 50.0, 'confidence': 0.0, 'method': 'error'}
    
    def _traditional_sound_classification(self, audio_data: np.ndarray) -> Dict:
        """Традиционная классификация звуков"""
        try:
            # Преобразование в моно
            if len(audio_data.shape) > 1:
                audio_data = np.mean(audio_data, axis=1)
            
            # FFT анализ
            fft = np.fft.fft(audio_data)
            freqs = np.fft.fftfreq(len(audio_data), 1/self.sample_rate)
            power_spectrum = np.abs(fft)**2
            
            # Основная частота
            dominant_freq = freqs[np.argmax(power_spectrum)]
            max_power = np.max(power_spectrum)
            
            # Классификация по частотам и мощности
            if dominant_freq < 100 and max_power > 0.1:
                return {'type': 'footsteps', 'confidence': min(max_power, 1.0)}
            elif dominant_freq > 2000 and max_power > 0.05:
                return {'type': 'gunshot', 'confidence': min(max_power, 1.0)}
            elif dominant_freq > 1000 and max_power > 0.08:
                return {'type': 'explosion', 'confidence': min(max_power, 1.0)}
            elif 300 < dominant_freq < 3000 and max_power > 0.03:
                return {'type': 'voice', 'confidence': min(max_power, 1.0)}
            else:
                return {'type': 'unknown', 'confidence': min(max_power, 1.0)}
                
        except Exception as e:
            print(f"❌ Ошибка традиционной классификации: {e}")
            return {'type': 'unknown', 'confidence': 0.0}
    
    def _integrate_results(self, sound_result: Dict, position_result: Dict) -> Dict:
        """Интеграция результатов анализа"""
        try:
            # Общая уверенность
            sound_confidence = sound_result.get('confidence', 0.0)
            position_confidence = position_result.get('confidence', 0.0)
            
            # Взвешенная уверенность
            total_confidence = (sound_confidence * 0.6 + position_confidence * 0.4)
            
            # Информация о звуке
            sound_info = self.sound_classifier.get_sound_info(sound_result['type'])
            
            # Информация о позиции
            position_info = self.position_analyzer.get_position_info(
                position_result['angle'], 
                position_result['distance']
            )
            
            # Интегрированный результат
            integrated_result = {
                'sound_type': sound_result['type'],
                'sound_confidence': sound_confidence,
                'sound_info': sound_info,
                'sound_method': sound_result.get('method', 'unknown'),
                
                'angle': position_result['angle'],
                'distance': position_result['distance'],
                'position_confidence': position_confidence,
                'position_info': position_info,
                'position_method': position_result.get('method', 'unknown'),
                
                'total_confidence': total_confidence,
                'is_reliable': total_confidence > self.min_confidence,
                
                'analysis_method': 'integrated_ai' if self.enable_ai else 'integrated_traditional'
            }
            
            return integrated_result
            
        except Exception as e:
            print(f"❌ Ошибка интеграции результатов: {e}")
            return self._get_fallback_result()
    
    def _update_statistics(self, result: Dict):
        """Обновление статистики"""
        try:
            # Статистика типов звуков
            sound_type = result['sound_type']
            if sound_type not in self.sound_type_stats:
                self.sound_type_stats[sound_type] = 0
            self.sound_type_stats[sound_type] += 1
            
            # Статистика позиций
            self.position_stats['angles'].append(result['angle'])
            self.position_stats['distances'].append(result['distance'])
            
            # Ограничение размера статистики
            if len(self.position_stats['angles']) > 1000:
                self.position_stats['angles'] = self.position_stats['angles'][-500:]
                self.position_stats['distances'] = self.position_stats['distances'][-500:]
                
        except Exception as e:
            print(f"❌ Ошибка обновления статистики: {e}")
    
    def _get_fallback_result(self) -> Dict:
        """Результат при ошибке"""
        return {
            'sound_type': 'unknown',
            'sound_confidence': 0.0,
            'sound_info': {},
            'sound_method': 'error',
            
            'angle': 0.0,
            'distance': 50.0,
            'position_confidence': 0.0,
            'position_info': {},
            'position_method': 'error',
            
            'total_confidence': 0.0,
            'is_reliable': False,
            'analysis_method': 'error',
            
            'timestamp': time.time(),
            'processing_time': 0.0,
            'analyzer_version': '2.0',
            'ai_enabled': False,
            'detection_id': self.detection_count
        }
    
    def get_statistics(self) -> Dict:
        """Получение статистики анализа"""
        try:
            stats = {
                'total_detections': self.detection_count,
                'sound_type_distribution': self.sound_type_stats.copy(),
                'position_stats': {
                    'avg_angle': np.mean(self.position_stats['angles']) if self.position_stats['angles'] else 0,
                    'avg_distance': np.mean(self.position_stats['distances']) if self.position_stats['distances'] else 0,
                    'angle_std': np.std(self.position_stats['angles']) if self.position_stats['angles'] else 0,
                    'distance_std': np.std(self.position_stats['distances']) if self.position_stats['distances'] else 0
                },
                'ai_status': {
                    'sound_classifier_loaded': self.sound_classifier.model is not None,
                    'position_analyzer_loaded': self.position_analyzer.model is not None,
                    'ai_enabled': self.enable_ai
                }
            }
            
            return stats
            
        except Exception as e:
            print(f"❌ Ошибка получения статистики: {e}")
            return {}
    
    def train_models(self, training_data: List[Tuple], epochs: int = 50):
        """Обучение моделей"""
        try:
            print("🎓 Начинаем обучение моделей...")
            
            # Подготовка данных для обучения
            sound_training_data = []
            position_training_data = []
            
            for audio_data, (sound_label, true_angle, true_distance) in training_data:
                sound_training_data.append((audio_data, sound_label))
                position_training_data.append((audio_data, (true_angle, true_distance)))
            
            # Обучение классификатора звуков
            if sound_training_data:
                print("🎓 Обучение классификатора звуков...")
                self.sound_classifier.train_model(sound_training_data, epochs)
            
            # Обучение анализатора позиций
            if position_training_data:
                print("🎓 Обучение анализатора позиций...")
                self.position_analyzer.train_position_model(position_training_data, epochs)
            
            print("✅ Обучение завершено!")
            
        except Exception as e:
            print(f"❌ Ошибка обучения: {e}")
    
    def set_ai_enabled(self, enabled: bool):
        """Включение/выключение ИИ"""
        self.enable_ai = enabled
        print(f"🤖 ИИ {'включен' if enabled else 'выключен'}")
    
    def set_min_confidence(self, confidence: float):
        """Установка минимальной уверенности"""
        self.min_confidence = max(0.0, min(1.0, confidence))
        print(f"🎯 Минимальная уверенность установлена: {self.min_confidence}")
    
    def get_detection_summary(self) -> Dict:
        """Сводка обнаружений"""
        try:
            recent_detections = min(100, self.detection_count)
            
            summary = {
                'total_detections': self.detection_count,
                'recent_detections': recent_detections,
                'most_common_sound': max(self.sound_type_stats.items(), key=lambda x: x[1])[0] if self.sound_type_stats else 'unknown',
                'average_confidence': np.mean([d.get('total_confidence', 0) for d in self.recent_results]) if hasattr(self, 'recent_results') else 0,
                'ai_usage_percentage': self._calculate_ai_usage_percentage()
            }
            
            return summary
            
        except Exception as e:
            print(f"❌ Ошибка получения сводки: {e}")
            return {}
    
    def _calculate_ai_usage_percentage(self) -> float:
        """Расчет процента использования ИИ"""
        try:
            if not hasattr(self, 'recent_results'):
                return 0.0
            
            ai_used = sum(1 for r in self.recent_results if 'ai' in r.get('analysis_method', ''))
            total = len(self.recent_results)
            
            return (ai_used / total * 100) if total > 0 else 0.0
            
        except Exception:
            return 0.0
