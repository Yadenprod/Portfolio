#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Отладка обработки аудио данных CS2 Sound Assistant
"""

import sounddevice as sd
import numpy as np
import time
import threading
from queue import Queue

class AudioDebugger:
    """Отладчик аудио данных"""
    
    def __init__(self):
        self.audio_queue = Queue()
        self.is_running = False
        self.device_id = None
        
    def find_minifuse_loopback(self):
        """Поиск устройства Minifuse Loopback"""
        devices = sd.query_devices()
        
        for i, device in enumerate(devices):
            name = device['name'].lower()
            if 'minifuse' in name and 'loopback' in name:
                print(f"🎯 Найдено устройство: {i}: {device['name']}")
                return i
        
        return None
    
    def audio_callback(self, indata, frames, time, status):
        """Callback для обработки аудио"""
        if status:
            print(f"⚠️ Статус аудио: {status}")
        
        # Проверяем уровень звука
        volume = np.sqrt(np.mean(indata**2))
        
        if volume > 0.01:  # Порог для обнаружения звука
            print(f"🎵 ЗВУК ОБНАРУЖЕН! Уровень: {volume:.6f}")
            print(f"   Данные: {indata.shape}, Максимум: {np.max(indata):.6f}")
            
            # Анализируем частотный спектр
            if indata.shape[1] >= 2:  # Стерео
                left_channel = indata[:, 0]
                right_channel = indata[:, 1]
                
                # FFT для анализа частот
                fft_left = np.fft.fft(left_channel)
                fft_right = np.fft.fft(right_channel)
                
                # Находим доминирующие частоты
                freqs = np.fft.fftfreq(len(left_channel), 1/48000)
                dominant_freq_left = freqs[np.argmax(np.abs(fft_left))]
                dominant_freq_right = freqs[np.argmax(np.abs(fft_right))]
                
                print(f"   Доминирующие частоты: L={dominant_freq_left:.0f}Hz, R={dominant_freq_right:.0f}Hz")
                
                # Определяем тип звука по частотам
                if 100 < abs(dominant_freq_left) < 1000:
                    print("   🎯 Возможные шаги (низкие частоты)")
                elif 1000 < abs(dominant_freq_left) < 5000:
                    print("   🔫 Возможные выстрелы (средние частоты)")
                elif abs(dominant_freq_left) > 5000:
                    print("   💥 Возможные взрывы (высокие частоты)")
        
        # Сохраняем данные для анализа
        self.audio_queue.put((indata.copy(), volume))
    
    def start_debug(self):
        """Запуск отладки"""
        print("🔍 Запуск отладки аудио...")
        
        # Поиск устройства
        self.device_id = self.find_minifuse_loopback()
        
        if self.device_id is None:
            print("❌ Устройство Minifuse Loopback не найдено!")
            return
        
        try:
            # Создание потока
            stream = sd.InputStream(
                device=self.device_id,
                channels=2,
                samplerate=48000,
                blocksize=1024,
                dtype=np.float32,
                callback=self.audio_callback
            )
            
            print(f"✅ Поток создан для устройства {self.device_id}")
            
            # Запуск захвата
            stream.start()
            self.is_running = True
            print("🎤 Захват аудио запущен")
            print("💡 Сделайте несколько шагов или выстрелов в CS2...")
            print("💡 Нажмите Ctrl+C для остановки")
            
            # Основной цикл
            try:
                while self.is_running:
                    time.sleep(0.1)
                    
                    # Показываем статистику каждые 5 секунд
                    if int(time.time()) % 5 == 0:
                        queue_size = self.audio_queue.qsize()
                        print(f"📊 Размер очереди: {queue_size}")
                        
            except KeyboardInterrupt:
                print("\n🛑 Остановка отладки...")
            
            # Остановка
            stream.stop()
            stream.close()
            
        except Exception as e:
            print(f"❌ Ошибка отладки: {e}")
    
    def analyze_audio_data(self):
        """Анализ накопленных аудио данных"""
        print("\n📊 Анализ аудио данных:")
        
        if self.audio_queue.empty():
            print("   Нет данных для анализа")
            return
        
        volumes = []
        while not self.audio_queue.empty():
            try:
                data, volume = self.audio_queue.get_nowait()
                volumes.append(volume)
            except:
                break
        
        if volumes:
            print(f"   Обработано блоков: {len(volumes)}")
            print(f"   Средний уровень: {np.mean(volumes):.6f}")
            print(f"   Максимальный уровень: {np.max(volumes):.6f}")
            print(f"   Минимальный уровень: {np.min(volumes):.6f}")
            
            # Подсчет обнаружений
            detections = sum(1 for v in volumes if v > 0.01)
            print(f"   Обнаружений звука: {detections}")

if __name__ == "__main__":
    debugger = AudioDebugger()
    debugger.start_debug()
    debugger.analyze_audio_data()
