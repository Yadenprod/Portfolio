#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тест работы overlay
"""

import sys
sys.path.append('src')

from display.overlay import OverlayDisplay
import time

def test_overlay():
    """Тест overlay"""
    print("🧪 Тест overlay")
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
    
    # Тестовые данные
    test_data = [
        {
            'sound_type': 'footsteps',
            'angle': 45.0,
            'distance': 25.0,
            'confidence': 0.8,
            'timestamp': time.time()
        },
        {
            'sound_type': 'gunshot',
            'angle': -30.0,
            'distance': 15.0,
            'confidence': 0.9,
            'timestamp': time.time()
        }
    ]
    
    print("🎯 Передаем тестовые данные...")
    
    # Передача данных
    for data in test_data:
        overlay.update_display(data)
        print(f"   Передано: {data}")
        time.sleep(0.1)
    
    print(f"📊 Всего обнаружений в overlay: {len(overlay.detections)}")
    
    # Запуск overlay на 5 секунд
    print("🖥️ Запуск overlay на 5 секунд...")
    
    import threading
    
    def run_overlay():
        overlay.start()
    
    overlay_thread = threading.Thread(target=run_overlay, daemon=True)
    overlay_thread.start()
    
    time.sleep(5)
    
    overlay.stop()
    print("✅ Тест завершен")

if __name__ == "__main__":
    test_overlay()
