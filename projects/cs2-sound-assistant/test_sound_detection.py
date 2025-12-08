#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тест обнаружения звуков CS2 Sound Assistant
"""

import sounddevice as sd
import numpy as np
import time
import threading
from queue import Queue

def generate_test_sound(duration=0.5, frequency=440, amplitude=0.5):
    """Генерация тестового звука"""
    sample_rate = 48000
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Синусоидальный сигнал
    signal = amplitude * np.sin(2 * np.pi * frequency * t)
    
    # Стерео (разные амплитуды для имитации позиции)
    left = signal
    right = signal * 0.7  # Правая сторона тише
    
    return np.column_stack((left, right))

def test_sound_detection():
    """Тест обнаружения звуков"""
    print("🧪 Тест обнаружения звуков")
    print("=" * 50)
    
    # Импорт компонентов
    import sys
    sys.path.append('src')
    
    from audio.capture import AudioCapture
    from analysis.analyzer import SoundAnalyzer
    from positioning.calculator import PositionCalculator
    
    # Инициализация компонентов
    config = {
        'audio.sample_rate': 48000,
        'audio.channels': 2,
        'audio.chunk_size': 1024
    }
    
    # Создание компонентов
    audio_capture = AudioCapture()
    sound_analyzer = SoundAnalyzer(config)
    position_calculator = PositionCalculator(config)
    
    # Инициализация
    audio_capture.initialize()
    sound_analyzer.initialize()
    position_calculator.initialize()
    
    print("✅ Компоненты инициализированы")
    
    # Генерируем тестовые звуки
    print("\n🎵 Генерируем тестовые звуки...")
    
    # Шаги (низкие частоты)
    footsteps = generate_test_sound(duration=0.3, frequency=200, amplitude=0.3)
    print("   Шаги: 200Hz, 0.3s")
    
    # Выстрелы (средние частоты)
    gunshot = generate_test_sound(duration=0.1, frequency=2000, amplitude=0.8)
    print("   Выстрел: 2000Hz, 0.1s")
    
    # Взрывы (широкий спектр)
    explosion = generate_test_sound(duration=0.5, frequency=100, amplitude=0.9)
    print("   Взрыв: 100Hz, 0.5s")
    
    # Тестируем каждый звук
    test_sounds = [
        ("Шаги", footsteps),
        ("Выстрел", gunshot),
        ("Взрыв", explosion)
    ]
    
    for name, sound_data in test_sounds:
        print(f"\n🔍 Тестируем: {name}")
        
        # Анализ звука
        analysis_result = sound_analyzer.analyze_audio(sound_data)
        
        if analysis_result:
            print(f"   ✅ Обнаружен: {analysis_result}")
            
            # Расчет позиции
            position = position_calculator.calculate_position(
                sound_data[:, 0],  # Левый канал
                sound_data[:, 1]   # Правый канал
            )
            
            if position:
                print(f"   📍 Позиция: угол={position['angle']:.1f}°, дистанция={position['distance']:.1f}m")
            else:
                print(f"   ❌ Позиция не рассчитана")
        else:
            print(f"   ❌ Звук не обнаружен")
    
    print("\n" + "=" * 50)
    print("🎯 Тест завершен!")

if __name__ == "__main__":
    test_sound_detection()
