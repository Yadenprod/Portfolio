#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тест ИИ анализатора CS2
"""

import sys
sys.path.append('src')

import numpy as np
import time
from ai.integrated_analyzer import CS2IntegratedAnalyzer

def generate_test_sounds():
    """Генерация тестовых звуков"""
    sample_rate = 48000
    duration = 0.1  # 100ms
    
    # Генерация разных типов звуков
    test_sounds = {}
    
    # Шаги (низкие частоты)
    t = np.linspace(0, duration, int(sample_rate * duration))
    footsteps = np.sin(2 * np.pi * 50 * t) * 0.5 + np.sin(2 * np.pi * 100 * t) * 0.3
    test_sounds['footsteps'] = footsteps
    
    # Выстрел (высокие частоты)
    gunshot = np.sin(2 * np.pi * 2000 * t) * np.exp(-10 * t) * 0.8
    test_sounds['gunshot'] = gunshot
    
    # Взрыв (средние частоты)
    explosion = np.sin(2 * np.pi * 300 * t) * np.exp(-5 * t) * 0.6
    test_sounds['explosion'] = explosion
    
    # Голос (средние частоты)
    voice = np.sin(2 * np.pi * 500 * t) * 0.4 + np.sin(2 * np.pi * 1000 * t) * 0.2
    test_sounds['voice'] = voice
    
    return test_sounds

def test_ai_analyzer():
    """Тест ИИ анализатора"""
    print("🤖 Тест ИИ анализатора CS2")
    print("=" * 50)
    
    # Создание анализатора
    analyzer = CS2IntegratedAnalyzer()
    
    # Генерация тестовых звуков
    test_sounds = generate_test_sounds()
    
    print(f"✅ Создано {len(test_sounds)} тестовых звуков")
    
    # Тестирование каждого типа звука
    for sound_type, audio_data in test_sounds.items():
        print(f"\n🎵 Тестируем: {sound_type}")
        print("-" * 30)
        
        # Создание стерео данных
        stereo_data = np.column_stack([audio_data, audio_data * 0.8])  # Имитация стерео
        
        # Анализ
        start_time = time.time()
        result = analyzer.analyze_audio(stereo_data)
        processing_time = time.time() - start_time
        
        # Вывод результатов
        print(f"🔍 Результат анализа:")
        print(f"   Тип звука: {result['sound_type']} (ожидался: {sound_type})")
        print(f"   Уверенность звука: {result['sound_confidence']:.3f}")
        print(f"   Угол: {result['angle']:.1f}°")
        print(f"   Дистанция: {result['distance']:.1f}m")
        print(f"   Уверенность позиции: {result['position_confidence']:.3f}")
        print(f"   Общая уверенность: {result['total_confidence']:.3f}")
        print(f"   Метод анализа: {result['analysis_method']}")
        print(f"   Время обработки: {processing_time*1000:.1f}ms")
        
        # Проверка надежности
        if result['is_reliable']:
            print("   ✅ Надежное обнаружение")
        else:
            print("   ⚠️ Ненадежное обнаружение")
    
    # Статистика
    print(f"\n📊 Статистика анализа:")
    print("-" * 30)
    stats = analyzer.get_statistics()
    
    print(f"Всего обнаружений: {stats['total_detections']}")
    print(f"Распределение типов звуков:")
    for sound_type, count in stats['sound_type_distribution'].items():
        print(f"  {sound_type}: {count}")
    
    if stats['position_stats']['avg_angle'] is not None:
        print(f"Средний угол: {stats['position_stats']['avg_angle']:.1f}°")
        print(f"Средняя дистанция: {stats['position_stats']['avg_distance']:.1f}m")
    
    print(f"Статус ИИ:")
    print(f"  Классификатор звуков: {'✅' if stats['ai_status']['sound_classifier_loaded'] else '❌'}")
    print(f"  Анализатор позиций: {'✅' if stats['ai_status']['position_analyzer_loaded'] else '❌'}")
    print(f"  ИИ включен: {'✅' if stats['ai_status']['ai_enabled'] else '❌'}")

def test_position_analysis():
    """Тест анализа позиций"""
    print(f"\n🎯 Тест анализа позиций")
    print("=" * 50)
    
    analyzer = CS2IntegratedAnalyzer()
    sample_rate = 48000
    duration = 0.1
    
    # Тестирование разных позиций
    test_positions = [
        (0, 10, "вперед близко"),
        (45, 25, "вперед-право средне"),
        (90, 50, "право далеко"),
        (-45, 15, "вперед-лево близко"),
        (-90, 100, "лево очень далеко"),
        (180, 5, "назад очень близко")
    ]
    
    for angle, distance, description in test_positions:
        print(f"\n🎯 Тестируем: {description} (угол: {angle}°, дистанция: {distance}m)")
        print("-" * 40)
        
        # Создание звука с имитацией позиции
        t = np.linspace(0, duration, int(sample_rate * duration))
        base_sound = np.sin(2 * np.pi * 1000 * t) * np.exp(-5 * t)
        
        # Имитация стерео эффекта для позиции
        # Чем больше угол, тем больше разность между каналами
        angle_factor = abs(angle) / 90.0  # Нормализация к 0-1
        left_gain = 1.0 - angle_factor if angle < 0 else 1.0
        right_gain = 1.0 - angle_factor if angle > 0 else 1.0
        
        # Имитация дистанции через амплитуду
        distance_factor = max(0.1, 1.0 - distance / 100.0)
        
        stereo_data = np.column_stack([
            base_sound * left_gain * distance_factor,
            base_sound * right_gain * distance_factor
        ])
        
        # Анализ
        result = analyzer.analyze_audio(stereo_data)
        
        # Вывод результатов
        print(f"Ожидалось: {angle}°, {distance}m")
        print(f"Получено: {result['angle']:.1f}°, {result['distance']:.1f}m")
        print(f"Ошибка угла: {abs(result['angle'] - angle):.1f}°")
        print(f"Ошибка дистанции: {abs(result['distance'] - distance):.1f}m")
        print(f"Уверенность: {result['total_confidence']:.3f}")
        print(f"Метод: {result['analysis_method']}")

if __name__ == "__main__":
    try:
        test_ai_analyzer()
        test_position_analysis()
        print(f"\n✅ Тест завершен!")
        
    except Exception as e:
        print(f"❌ Ошибка теста: {e}")
        import traceback
        traceback.print_exc()
