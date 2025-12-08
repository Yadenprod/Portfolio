#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тест захвата аудио с Arturia MiniFuse 2 Main 1/2
"""

import pyaudio
import numpy as np
import time

def test_minifuse_capture():
    """Тестирование захвата с Minifuse"""
    print("🎵 Тест захвата с Arturia MiniFuse 2")
    print("=" * 50)
    
    p = pyaudio.PyAudio()
    
    # Поиск устройств Minifuse
    minifuse_devices = []
    
    print("📋 Доступные устройства:")
    for i in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        name = device_info['name']
        inputs = device_info['maxInputChannels']
        outputs = device_info['maxOutputChannels']
        
        print(f"  {i}: {name}")
        print(f"    Входы: {inputs}, Выходы: {outputs}")
        
        if 'minifuse' in name.lower():
            minifuse_devices.append((i, name, inputs, outputs))
            print(f"    🎯 ОБНАРУЖЕНО УСТРОЙСТВО MINIFUSE!")
        
        print()
    
    print(f"📊 Найдено устройств Minifuse: {len(minifuse_devices)}")
    
    if not minifuse_devices:
        print("❌ Устройства Minifuse не найдены!")
        return
    
    # Показываем все устройства Minifuse
    for device_id, name, inputs, outputs in minifuse_devices:
        print(f"🎯 Устройство {device_id}: {name}")
        print(f"   Входы: {inputs}, Выходы: {outputs}")
        
        # Пробуем открыть поток для захвата
        if inputs > 0:
            print(f"   🧪 Тестируем захват...")
            try:
                stream = p.open(
                    format=pyaudio.paFloat32,
                    channels=2,
                    rate=48000,
                    input=True,
                    input_device_index=device_id,
                    frames_per_buffer=1024
                )
                
                print(f"   ✅ Захват доступен!")
                
                # Читаем немного данных для проверки
                data = stream.read(1024, exception_on_overflow=False)
                audio_array = np.frombuffer(data, dtype=np.float32)
                
                # Проверяем, есть ли звук
                volume = np.sqrt(np.mean(audio_array**2))
                print(f"   📊 Уровень звука: {volume:.6f}")
                
                if volume > 0.001:
                    print(f"   🎵 ЗВУК ОБНАРУЖЕН!")
                else:
                    print(f"   🔇 Звук не обнаружен")
                
                stream.close()
                
            except Exception as e:
                print(f"   ❌ Ошибка захвата: {e}")
        else:
            print(f"   ⚠️ Нет входов для захвата")
        
        print()
    
    p.terminate()
    
    print("=" * 50)
    print("💡 Рекомендации:")
    print("1. Убедитесь, что CS2 воспроизводит звук через Main 1/2")
    print("2. Проверьте настройки громкости в Windows")
    print("3. Попробуйте другой канал Minifuse")

if __name__ == "__main__":
    test_minifuse_capture()
