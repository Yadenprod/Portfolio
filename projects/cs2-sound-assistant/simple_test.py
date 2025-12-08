#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Простой тест overlay
"""

import sys
sys.path.append('src')

from display.overlay import OverlayDisplay
import time
import threading

def simple_test():
    """Простой тест overlay"""
    print("🧪 Простой тест overlay")
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
    
    # Запуск overlay
    print("🖥️ Запуск overlay...")
    
    def run_overlay():
        overlay.start()
    
    overlay_thread = threading.Thread(target=run_overlay, daemon=True)
    overlay_thread.start()
    
    # Ждем 10 секунд
    print("⏰ Ждем 10 секунд...")
    time.sleep(10)
    
    overlay.stop()
    print("✅ Тест завершен")

if __name__ == "__main__":
    simple_test()
