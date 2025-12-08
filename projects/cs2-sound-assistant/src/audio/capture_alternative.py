#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Альтернативный модуль захвата аудио для Arturia MiniFuse 2
"""

import numpy as np
import threading
import time
import pyaudio
from typing import Optional, Callable

class AlternativeAudioCapture:
    """Альтернативный захват аудио для Minifuse"""
    
    def __init__(self, sample_rate: int = 48000, channels: int = 2, chunk_size: int = 1024):
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_size = chunk_size
        self.audio_buffer = []
        self.is_initialized = False
        self.is_capturing = False
        self.audio_stream = None
        self.p = None
        self.callback = None
        
    def initialize(self):
        """Инициализация захвата"""
        print("🎤 Инициализация альтернативного захвата аудио...")
        
        try:
            self.p = pyaudio.PyAudio()
            
            # Поиск устройства Minifuse
            device_id = self.find_minifuse_device()
            
            if device_id is not None:
                # Создание потока захвата
                self.audio_stream = self.p.open(
                    format=pyaudio.paFloat32,
                    channels=self.channels,
                    rate=self.sample_rate,
                    input=True,
                    input_device_index=device_id,
                    frames_per_buffer=self.chunk_size,
                    stream_callback=self.audio_callback
                )
                
                self.is_initialized = True
                print(f"✅ Альтернативный захват инициализирован (устройство: {device_id})")
            else:
                raise Exception("Устройство Minifuse не найдено")
                
        except Exception as e:
            print(f"❌ Ошибка инициализации альтернативного захвата: {e}")
            self.is_initialized = False
    
    def find_minifuse_device(self) -> Optional[int]:
        """Поиск устройства Minifuse"""
        print("🔍 Поиск устройства Minifuse...")
        
        for i in range(self.p.get_device_count()):
            device_info = self.p.get_device_info_by_index(i)
            name = device_info['name'].lower()
            
            print(f"   Устройство {i}: {device_info['name']}")
            print(f"     Входы: {device_info['maxInputChannels']}")
            print(f"     Выходы: {device_info['maxOutputChannels']}")
            
            if 'minifuse' in name and device_info['maxInputChannels'] > 0:
                print(f"   🎯 Найдено устройство Minifuse: {i}")
                return i
        
        return None
    
    def audio_callback(self, in_data, frame_count, time_info, status):
        """Callback для обработки аудио данных"""
        if self.callback:
            try:
                # Преобразование байтов в numpy array
                audio_data = np.frombuffer(in_data, dtype=np.float32)
                audio_data = audio_data.reshape(-1, self.channels)
                
                # Вызов пользовательского callback
                self.callback(audio_data)
                
            except Exception as e:
                print(f"❌ Ошибка в audio callback: {e}")
        
        return (in_data, pyaudio.paContinue)
    
    def start_capture(self):
        """Запуск захвата"""
        if not self.is_initialized:
            print("❌ Захват не инициализирован")
            return
        
        try:
            self.audio_stream.start_stream()
            self.is_capturing = True
            print("🎤 Альтернативный захват аудио запущен")
            
        except Exception as e:
            print(f"❌ Ошибка запуска захвата: {e}")
    
    def stop_capture(self):
        """Остановка захвата"""
        if self.audio_stream:
            try:
                self.audio_stream.stop_stream()
                self.audio_stream.close()
            except Exception as e:
                print(f"❌ Ошибка остановки захвата: {e}")
        
        if self.p:
            self.p.terminate()
        
        self.is_capturing = False
        print("🛑 Альтернативный захват аудио остановлен")
    
    def set_callback(self, callback: Callable):
        """Установка callback функции"""
        self.callback = callback
    
    def get_audio_info(self) -> dict:
        """Получение информации об аудио"""
        return {
            'sample_rate': self.sample_rate,
            'channels': self.channels,
            'chunk_size': self.chunk_size,
            'is_initialized': self.is_initialized,
            'is_capturing': self.is_capturing,
            'mode': 'Alternative Minifuse Capture'
        }
