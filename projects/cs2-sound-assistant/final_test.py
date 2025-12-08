#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Финальный тест overlay
"""

import sys
sys.path.append('src')

from display.overlay import OverlayDisplay
import time

def final_test():
    """Финальный тест overlay"""
    print("🎯 ФИНАЛЬНЫЙ ТЕСТ OVERLAY")
    print("=" * 50)
    
    # Конфигурация
    config = {
        'display.window_size': [400, 400],
        'display.radar_radius': 150,
        'display.update_rate': 60
    }
    
    # Создание overlay
    overlay = OverlayDisplay(config)
    overlay.initialize()
    
    print("✅ Overlay инициализирован")
    
    # Добавляем тестовые данные напрямую
    test_data = {
        'sound_type': 'footsteps',
        'angle': 45.0,
        'distance': 25.0,
        'confidence': 0.8,
        'timestamp': time.time()
    }
    
    print("🎯 Добавляем тестовые данные напрямую...")
    overlay.detections.append(test_data)
    print(f"📊 Данные добавлены: {len(overlay.detections)} обнаружений")
    
    # Запуск overlay в главном потоке
    print("🖥️ Запуск overlay в главном потоке...")
    overlay.start()

if __name__ == "__main__":
    final_test()
