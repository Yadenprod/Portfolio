#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Финальный тест overlay с реальными данными
"""

import sys
sys.path.append('src')

from display.overlay import OverlayDisplay
import time

def test_final():
    """Финальный тест overlay"""
    print("🎯 ФИНАЛЬНЫЙ ТЕСТ OVERLAY С РЕАЛЬНЫМИ ДАННЫМИ")
    print("=" * 60)
    
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
    
    # Добавляем реальные данные из логов
    real_data = [
        {
            'sound_type': 'footsteps',
            'angle': 8.52476,
            'distance': 0.5917413,
            'confidence': 1.0,
            'timestamp': time.time()
        },
        {
            'sound_type': 'voice',
            'angle': -4.160908,
            'distance': 0.41426027,
            'confidence': 1.0,
            'timestamp': time.time()
        },
        {
            'sound_type': 'explosion',
            'angle': 12.860959,
            'distance': 0.098966695,
            'confidence': 1.0,
            'timestamp': time.time()
        }
    ]
    
    print("🎯 Добавляем реальные данные из логов:")
    for i, data in enumerate(real_data):
        print(f"   {i+1}. {data['sound_type']} - угол:{data['angle']:.1f}° дистанция:{data['distance']:.3f}m")
        overlay.update_display(data)
    
    print(f"📊 Всего обнаружений в overlay: {len(overlay.detections)}")
    
    # Запускаем overlay
    print("🎮 Запуск overlay...")
    overlay.start()
    
    print("✅ Тест завершен")

if __name__ == "__main__":
    test_final()
