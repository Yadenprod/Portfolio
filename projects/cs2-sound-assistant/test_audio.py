#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тест аудио устройств для CS2 Sound Assistant
"""

import sounddevice as sd
import numpy as np
import time

def test_audio_devices():
    """Тестирование доступных аудио устройств"""
    print("🎵 Тест аудио устройств CS2 Sound Assistant")
    print("=" * 50)
    
    # Получение списка устройств
    devices = sd.query_devices()
    
    print(f"📋 Найдено устройств: {len(devices)}")
    print()
    
    # Поиск устройств ввода
    input_devices = []
    system_audio_devices = []
    
    for i, device in enumerate(devices):
        name = device['name']
        max_inputs = device.get('max_inputs', 0)
        max_outputs = device.get('max_outputs', 0)
        
        print(f"Устройство {i}: {name}")
        print(f"  Входы: {max_inputs}, Выходы: {max_outputs}")
        
        if max_inputs > 0:
            input_devices.append((i, name))
            
            # Проверяем на системные аудио устройства
            name_lower = name.lower()
            if any(keyword in name_lower for keyword in ['stereo mix', 'what u hear', 'loopback', 'system']):
                system_audio_devices.append((i, name))
                print(f"  🎯 ОБНАРУЖЕНО СИСТЕМНОЕ АУДИО УСТРОЙСТВО!")
        
        print()
    
    print("📊 Результаты:")
    print(f"Устройств ввода: {len(input_devices)}")
    print(f"Системных аудио устройств: {len(system_audio_devices)}")
    
    if system_audio_devices:
        print("\n✅ Системные аудио устройства найдены:")
        for device_id, name in system_audio_devices:
            print(f"  {device_id}: {name}")
        
        # Тестируем первое системное устройство
        test_device = system_audio_devices[0]
        print(f"\n🧪 Тестируем устройство: {test_device[1]}")
        
        try:
            # Пробуем открыть поток
            stream = sd.InputStream(
                device=test_device[0],
                channels=2,
                samplerate=48000,
                blocksize=1024,
                dtype=np.float32
            )
            
            print("✅ Устройство доступно для захвата!")
            stream.close()
            
        except Exception as e:
            print(f"❌ Ошибка тестирования: {e}")
    
    else:
        print("\n⚠️ Системные аудио устройства НЕ найдены!")
        print("📋 Доступные устройства ввода:")
        for device_id, name in input_devices:
            print(f"  {device_id}: {name}")
        
        if input_devices:
            print(f"\n🧪 Тестируем первое устройство ввода: {input_devices[0][1]}")
            
            try:
                stream = sd.InputStream(
                    device=input_devices[0][0],
                    channels=2,
                    samplerate=48000,
                    blocksize=1024,
                    dtype=np.float32
                )
                
                print("✅ Устройство доступно для захвата!")
                stream.close()
                
            except Exception as e:
                print(f"❌ Ошибка тестирования: {e}")
    
    print("\n" + "=" * 50)
    print("💡 Рекомендации:")
    
    if system_audio_devices:
        print("✅ Система готова к работе с реальным аудио!")
        print("🎮 Запустите CS2 и систему для тестирования")
    else:
        print("⚠️ Требуется настройка аудио устройства")
        print("🔧 Запустите setup_audio.bat для настройки")
        print("📋 Или система будет работать в режиме симуляции")

if __name__ == "__main__":
    test_audio_devices()
