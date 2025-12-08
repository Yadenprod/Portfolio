#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тест работы CS2 Sound Assistant
"""

import sounddevice as sd
import numpy as np
import time
import threading
from queue import Queue

def generate_test_sound(duration=1.0, frequency=440, amplitude=0.3):
    """Генерация тестового звука"""
    sample_rate = 48000
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    # Синусоидальный сигнал
    signal = amplitude * np.sin(2 * np.pi * frequency * t)
    # Стерео (разные фазы для левого и правого канала)
    left = signal
    right = signal * 0.8  # Немного тише для имитации позиции
    return np.column_stack((left, right))

def test_system():
    """Тест системы"""
    print("🧪 Тест CS2 Sound Assistant")
    print("=" * 50)
    
    # Генерируем тестовые звуки
    print("🎵 Генерируем тестовые звуки...")
    
    # Шаги (низкие частоты)
    footsteps = generate_test_sound(0.5, 200, 0.2)
    print("   ✅ Шаги (200Hz)")
    
    # Выстрелы (средние частоты)
    gunshot = generate_test_sound(0.1, 2000, 0.4)
    print("   ✅ Выстрелы (2000Hz)")
    
    # Взрывы (широкий спектр)
    explosion = generate_test_sound(0.3, 100, 0.5)
    print("   ✅ Взрывы (100Hz)")
    
    print("\n🎯 Тест завершен!")
    print("💡 Теперь запустите main.py и воспроизведите эти звуки")
    print("💡 Система должна их обнаружить и показать на overlay")

if __name__ == "__main__":
    test_system()
