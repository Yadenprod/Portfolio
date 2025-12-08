#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Модуль захвата аудио для CS2 Sound Assistant
Захватывает системный аудио поток для анализа звуков игры
"""

import numpy as np
import sounddevice as sd
import threading
import time
from typing import Optional, Tuple

class AudioCapture:
    """Класс для захвата системного аудио"""
    
    def __init__(self, sample_rate: int = 48000, channels: int = 2, chunk_size: int = 1024):
        """Инициализация захвата аудио"""
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_size = chunk_size
        self.device_id = None
        self.audio_stream = None
        self.is_initialized = False
        self.is_capturing = False
        self.audio_buffer = []
        self.buffer_size = 5  # Размер буфера
        self.buffer_lock = threading.Lock()
        self.frames_captured = 0
        self.last_activity = 0
    
    def initialize(self):
        """Инициализация захвата аудио"""
        print("🎤 Инициализация захвата аудио...")
        
        try:
            # Попробуем найти устройство захвата системного аудио
            if self.device_id is None:
                self.device_id = self.find_system_audio_device()
            
            # Проверка доступности устройства
            if not self.check_device():
                raise Exception("Устройство аудио недоступно")
            
            # Создание аудио потока для захвата с более гибкими параметрами
            try:
                self.audio_stream = sd.InputStream(
                    device=self.device_id,
                    channels=self.channels,
                    samplerate=self.sample_rate,
                    blocksize=self.chunk_size,
                    dtype=np.float32,
                    callback=self.audio_callback
                )
            except Exception as stream_error:
                print(f"⚠️ Ошибка создания потока: {stream_error}")
                # Попробуем с другими параметрами
                self.audio_stream = sd.InputStream(
                    device=self.device_id,
                    channels=2,  # Принудительно 2 канала
                    samplerate=48000,  # Стандартная частота
                    blocksize=1024,  # Стандартный размер блока
                    dtype=np.float32,
                    callback=self.audio_callback
                )
            
            self.is_initialized = True
            print(f"✅ Аудио захват инициализирован (устройство: {self.device_id})")
            
        except Exception as e:
            print(f"❌ Ошибка инициализации аудио: {e}")
            # Попробуем альтернативный способ
            print("🔄 Попытка альтернативного захвата аудио...")
            try:
                self.initialize_wasapi_capture()
            except Exception as e2:
                print(f"❌ Ошибка альтернативного захвата: {e2}")
                # Если не удалось найти системное аудио, используем симуляцию
                print("🔄 Переключение на режим симуляции аудио...")
                self.is_initialized = True
    
    def find_system_audio_device(self) -> int:
        """Поиск устройства захвата системного аудио"""
        print("🔍 Поиск устройства захвата системного аудио...")
        
        devices = sd.query_devices()
        input_devices = []
        
        for i, device in enumerate(devices):
            if device.get('max_inputs', 0) > 0:
                input_devices.append((i, device['name']))
                print(f"   {i}: {device['name']} (входов: {device.get('max_inputs', 0)})")
        
        # Специальная поддержка для Arturia MiniFuse 2 - используем Loopback
        minifuse_loopback_devices = []
        for i, device in enumerate(devices):
            name = device['name'].lower()
            if 'minifuse' in name and 'loopback' in name:
                minifuse_loopback_devices.append((i, device['name']))
                print(f"   🎯 Найдено устройство Minifuse Loopback: {i}: {device['name']}")
        
        if minifuse_loopback_devices:
            # Используем первое найденное loopback устройство Minifuse
            device_id = minifuse_loopback_devices[0][0]
            print(f"🎯 Выбрано устройство Minifuse Loopback: {device_id}")
            return device_id
        
        # Попробуем найти специальные устройства для захвата системного аудио
        system_audio_devices = []
        for i, device in enumerate(devices):
            name = device['name'].lower()
            if any(keyword in name for keyword in ['stereo mix', 'what u hear', 'loopback', 'system', 'default']):
                if device.get('max_inputs', 0) > 0:
                    system_audio_devices.append((i, device['name']))
                    print(f"   🎯 Найдено системное аудио устройство: {i}: {device['name']}")
        
        if system_audio_devices:
            # Используем первое найденное системное аудио устройство
            device_id = system_audio_devices[0][0]
            print(f"🎯 Выбрано системное аудио устройство: {device_id}")
            return device_id
        
        if not input_devices:
            print("⚠️ Не найдено устройство захвата, используем симуляцию")
            return None
        
        # Попробуем найти устройство по умолчанию
        try:
            default_device = sd.default.device[0]  # Устройство ввода по умолчанию
            print(f"🎯 Выбрано устройство по умолчанию: {default_device}")
            return default_device
        except:
            # Если не удалось, берем первое доступное
            print(f"🎯 Выбрано первое доступное устройство: {input_devices[0][0]}")
            return input_devices[0][0]
    
    def check_device(self) -> bool:
        """Проверка доступности устройства"""
        try:
            if self.device_id is None:
                return False
            
            devices = sd.query_devices()
            if self.device_id >= len(devices):
                return False
            
            device = devices[self.device_id]
            
            # Для Minifuse loopback устройств может не быть max_inputs
            if 'minifuse' in device['name'].lower() and 'loopback' in device['name'].lower():
                print(f"✅ Устройство Minifuse Loopback доступно: {device['name']}")
                return True
            
            # Обычная проверка для других устройств
            if device.get('max_inputs', 0) > 0:
                print(f"✅ Устройство доступно: {device['name']}")
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ Ошибка проверки устройства: {e}")
            return False
    
    def audio_callback(self, indata, frames, time, status):
        """Callback функция для обработки аудио данных"""
        if status:
            print(f"⚠️ Аудио статус: {status}")
        
        # Копирование данных
        audio_data = indata.copy()
        
        # Добавление в буфер
        with self.buffer_lock:
            self.audio_buffer.append(audio_data)
            
            # Ограничение размера буфера
            if len(self.audio_buffer) > 5:
                self.audio_buffer.pop(0)
        
        self.frames_captured += frames
    
    def start_capture(self):
        """Запуск захвата аудио"""
        if not self.is_initialized:
            raise Exception("Аудио захват не инициализирован")
        
        if self.is_capturing:
            return
        
        # Если нет реального устройства, запускаем симуляцию
        if self.device_id is None:
            self.start_simulation()
            return
        
        try:
            self.audio_stream.start()
            self.is_capturing = True
            self.start_time = time.time()
            print("🎤 Захват аудио запущен")
            
        except Exception as e:
            print(f"❌ Ошибка запуска захвата: {e}")
            print("🔄 Переключение на режим симуляции...")
            self.start_simulation()
    
    def start_simulation(self):
        """Запуск симуляции аудио для тестирования"""
        self.is_capturing = True
        self.start_time = time.time()
        print("🎮 Режим симуляции аудио запущен")
        
        # Запуск потока симуляции
        self.simulation_thread = threading.Thread(target=self._simulation_loop, daemon=True)
        self.simulation_thread.start()
    
    def _simulation_loop(self):
        """Петля симуляции аудио"""
        import random
        
        while self.is_capturing:
            # Симуляция различных звуков CS2
            sound_types = ['footsteps', 'gunshot', 'explosion', 'voice']
            sound_type = random.choice(sound_types)
            
            # Создание симулированного аудио сигнала
            duration = 0.1  # 100ms
            samples = int(self.sample_rate * duration)
            
            # Генерация синусоидального сигнала с шумом
            t = np.linspace(0, duration, samples)
            
            if sound_type == 'footsteps':
                # Низкие частоты для шагов
                frequency = random.uniform(50, 200)
                amplitude = random.uniform(0.1, 0.3)
            elif sound_type == 'gunshot':
                # Широкий спектр для выстрелов
                frequency = random.uniform(100, 1000)
                amplitude = random.uniform(0.5, 1.0)
            elif sound_type == 'explosion':
                # Очень низкие частоты для взрывов
                frequency = random.uniform(20, 100)
                amplitude = random.uniform(0.7, 1.0)
            else:  # voice
                # Средние частоты для голоса
                frequency = random.uniform(200, 800)
                amplitude = random.uniform(0.2, 0.5)
            
            # Создание стерео сигнала
            left_channel = amplitude * np.sin(2 * np.pi * frequency * t) + 0.1 * np.random.randn(samples)
            right_channel = amplitude * np.sin(2 * np.pi * frequency * t) + 0.1 * np.random.randn(samples)
            
            # Добавление небольшой разности фаз для стерео эффекта
            phase_diff = random.uniform(-0.1, 0.1)
            right_channel = np.roll(right_channel, int(phase_diff * self.sample_rate))
            
            # Объединение в стерео массив
            audio_data = np.column_stack((left_channel, right_channel)).astype(np.float32)
            
            # Добавление в буфер
            with self.buffer_lock:
                self.audio_buffer.append(audio_data)
                if len(self.audio_buffer) > 5:
                    self.audio_buffer.pop(0)
            
            self.frames_captured += samples
            
            # Пауза между звуками
            time.sleep(random.uniform(1.0, 3.0))
    
    def stop_capture(self):
        """Остановка захвата аудио"""
        if not self.is_capturing:
            return
        
        self.is_capturing = False
        
        try:
            if self.audio_stream is not None:
                self.audio_stream.stop()
            print("🛑 Захват аудио остановлен")
            
        except Exception as e:
            print(f"❌ Ошибка остановки захвата: {e}")
    
    def get_audio_chunk(self) -> Optional[np.ndarray]:
        """Получение аудио данных"""
        with self.buffer_lock:
            if self.audio_buffer:
                return self.audio_buffer.pop(0)
        return None
    
    def get_audio_info(self) -> dict:
        """Получение информации об аудио"""
        if not self.is_capturing:
            return {}
        
        current_time = time.time()
        duration = current_time - self.start_time if self.start_time else 0
        
        mode = "симуляция" if self.device_id is None else "реальное устройство"
        
        return {
            'frames_captured': self.frames_captured,
            'duration': duration,
            'fps': self.frames_captured / duration if duration > 0 else 0,
            'buffer_size': len(self.audio_buffer),
            'device_id': self.device_id,
            'sample_rate': self.sample_rate,
            'channels': self.channels,
            'chunk_size': self.chunk_size,
            'mode': mode
        }
    
    def set_device(self, device_id: int):
        """Изменение устройства аудио"""
        if self.is_capturing:
            self.stop_capture()
        
        self.device_id = device_id
        
        if self.is_initialized:
            self.audio_stream.close()
            self.initialize()
    
    def list_devices(self):
        """Список доступных устройств"""
        devices = sd.query_devices()
        
        print("📋 Доступные аудио устройства:")
        for i, device in enumerate(devices):
            if device['max_outputs'] > 0:
                status = " (по умолчанию)" if i == sd.default.device[1] else ""
                print(f"   {i}: {device['name']}{status}")
    
    def stop(self):
        """Остановка модуля"""
        self.stop_capture()
        
        if self.audio_stream:
            self.audio_stream.close()
        
        print("🛑 Модуль аудио захвата остановлен")

    def initialize_wasapi_capture(self):
        """Инициализация захвата через WASAPI"""
        print("🔧 Попытка захвата через WASAPI...")
        
        # Попробуем найти WASAPI устройства
        devices = sd.query_devices()
        wasapi_devices = []
        
        for i, device in enumerate(devices):
            name = device['name'].lower()
            if 'wasapi' in name and device.get('max_inputs', 0) > 0:
                wasapi_devices.append((i, device['name']))
                print(f"   🎯 Найдено WASAPI устройство: {i}: {device['name']}")
        
        # Если WASAPI не найден, попробуем найти устройства с поддержкой loopback
        if not wasapi_devices:
            print("🔍 Поиск устройств с поддержкой loopback...")
            for i, device in enumerate(devices):
                name = device['name'].lower()
                # Ищем устройства, которые могут захватывать системный звук
                if any(keyword in name for keyword in ['hyperx', 'virtual', 'surround', 'headset', 'minifuse']):
                    if device.get('max_inputs', 0) > 0:
                        wasapi_devices.append((i, device['name']))
                        print(f"   🎯 Найдено устройство: {i}: {device['name']}")
        
        if wasapi_devices:
            # Используем первое найденное устройство
            self.device_id = wasapi_devices[0][0]
            print(f"🎯 Выбрано устройство: {self.device_id}")
            
            # Создание аудио потока
            self.audio_stream = sd.InputStream(
                device=self.device_id,
                channels=self.channels,
                samplerate=self.sample_rate,
                blocksize=self.chunk_size,
                dtype=np.float32,
                callback=self.audio_callback
            )
            
            self.is_initialized = True
            print(f"✅ Аудио захват инициализирован через устройство")
        else:
            # Попробуем создать виртуальный loopback для Main 1/2
            print("🔧 Попытка создания виртуального loopback...")
            try:
                # Создаем поток для захвата с Main 1/2 через WASAPI
                self.audio_stream = sd.InputStream(
                    device=None,  # Используем устройство по умолчанию
                    channels=self.channels,
                    samplerate=self.sample_rate,
                    blocksize=self.chunk_size,
                    dtype=np.float32,
                    callback=self.audio_callback,
                    latency='low'
                )
                
                self.is_initialized = True
                print(f"✅ Виртуальный loopback создан")
            except Exception as e:
                raise Exception(f"Не удалось создать виртуальный loopback: {e}")
