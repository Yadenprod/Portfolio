#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CS2 Sound Assistant - Демо версия
Упрощенная версия для демонстрации концепции
"""

import time
import random
import math
import json
from pathlib import Path

class DemoConfig:
    """Демо конфигурация"""
    def __init__(self):
        self.config = {
            "audio": {
                "sample_rate": 48000,
                "channels": 2,
                "chunk_size": 1024
            },
            "analysis": {
                "amplitude_threshold": 0.05,
                "frequency_threshold": 0.1
            },
            "positioning": {
                "ear_distance": 0.15,
                "sound_speed": 343,
                "max_distance": 50
            },
            "display": {
                "window_size": [400, 400],
                "radar_radius": 150,
                "update_rate": 60
            }
        }
    
    def get(self, key, default=None):
        keys = key.split('.')
        value = self.config
        try:
            for k in keys:
                value = value[k]
            return value
        except:
            return default

class DemoAudioCapture:
    """Демо захват аудио - генерирует тестовые данные"""
    def __init__(self, config):
        self.config = config
        self.sample_rate = config.get('audio.sample_rate', 48000)
        self.chunk_size = config.get('audio.chunk_size', 1024)
        
    def get_audio_chunk(self):
        """Генерация тестовых аудио данных"""
        # Симуляция стерео аудио
        left_channel = [random.uniform(-0.1, 0.1) for _ in range(self.chunk_size)]
        right_channel = [random.uniform(-0.1, 0.1) for _ in range(self.chunk_size)]
        
        # Иногда добавляем "звуки" (более высокие амплитуды)
        if random.random() < 0.1:  # 10% вероятность звука
            sound_type = random.choice(['footsteps', 'gunshots', 'explosions'])
            if sound_type == 'footsteps':
                # Шаги - короткие звуки
                start = random.randint(0, self.chunk_size - 100)
                for i in range(start, min(start + 50, self.chunk_size)):
                    left_channel[i] = random.uniform(-0.3, 0.3)
                    right_channel[i] = random.uniform(-0.3, 0.3)
            elif sound_type == 'gunshots':
                # Выстрелы - громкие короткие звуки
                start = random.randint(0, self.chunk_size - 20)
                for i in range(start, min(start + 20, self.chunk_size)):
                    left_channel[i] = random.uniform(-0.8, 0.8)
                    right_channel[i] = random.uniform(-0.8, 0.8)
            elif sound_type == 'explosions':
                # Взрывы - длинные громкие звуки
                start = random.randint(0, self.chunk_size - 200)
                for i in range(start, min(start + 200, self.chunk_size)):
                    left_channel[i] = random.uniform(-0.6, 0.6)
                    right_channel[i] = random.uniform(-0.6, 0.6)
        
        return [[left_channel[i], right_channel[i]] for i in range(self.chunk_size)]

class DemoSoundAnalyzer:
    """Демо анализатор звуков"""
    def __init__(self, config):
        self.config = config
        
    def analyze_audio(self, audio_data):
        """Анализ аудио данных"""
        if not audio_data:
            return []
        
        # Простой анализ амплитуды
        max_amplitude = 0
        for sample in audio_data:
            amplitude = abs(sample[0]) + abs(sample[1])  # Сумма каналов
            max_amplitude = max(max_amplitude, amplitude)
        
        # Определение типа звука по амплитуде
        if max_amplitude > 0.5:
            sound_type = 'gunshots'
            confidence = min(max_amplitude, 1.0)
        elif max_amplitude > 0.3:
            sound_type = 'explosions'
            confidence = min(max_amplitude / 0.5, 1.0)
        elif max_amplitude > 0.1:
            sound_type = 'footsteps'
            confidence = min(max_amplitude / 0.3, 1.0)
        else:
            return []  # Слишком тихий звук
        
        return [{
            'type': sound_type,
            'confidence': confidence,
            'amplitude': max_amplitude
        }]

class DemoPositionCalculator:
    """Демо калькулятор позиций"""
    def __init__(self, config):
        self.config = config
        
    def calculate_position(self, left_channel, right_channel):
        """Расчет позиции источника звука"""
        if not left_channel or not right_channel:
            return None
        
        # Простой расчет на основе разности амплитуд
        left_amplitude = sum(abs(x) for x in left_channel) / len(left_channel)
        right_amplitude = sum(abs(x) for x in right_channel) / len(right_channel)
        
        # Расчет угла (упрощенный)
        if left_amplitude + right_amplitude < 0.01:
            return None  # Слишком тихий звук
        
        # Разность амплитуд определяет направление
        amplitude_diff = left_amplitude - right_amplitude
        angle = math.degrees(math.atan(amplitude_diff * 10))  # Масштабирование
        
        # Ограничение угла
        angle = max(-90, min(90, angle))
        
        # Расчет дистанции (упрощенный)
        total_amplitude = left_amplitude + right_amplitude
        distance = max(1, 50 / (total_amplitude * 100))  # Обратная зависимость
        
        return {
            'angle': angle,
            'distance': distance,
            'confidence': min(total_amplitude * 2, 1.0)
        }

class DemoOverlay:
    """Демо overlay отображение"""
    def __init__(self, config):
        self.config = config
        self.detections = []
        
    def update(self, detections):
        """Обновление отображения"""
        self.detections = detections
        
    def draw_radar(self):
        """Отрисовка радара в консоли"""
        print("\033[2J\033[H")  # Очистка экрана
        
        # Простой ASCII радар
        radar_size = 20
        radar = [[' ' for _ in range(radar_size)] for _ in range(radar_size)]
        
        # Центр радара
        center = radar_size // 2
        
        # Отрисовка обнаружений
        for detection in self.detections:
            angle = detection['angle']
            distance = detection['distance']
            sound_type = detection.get('sound_type', 'unknown')
            
            # Конвертация в координаты радара
            rad = math.radians(angle)
            normalized_distance = min(distance / 50.0, 1.0)  # Нормализация
            
            x = center + int(normalized_distance * (center - 1) * math.cos(rad))
            y = center + int(normalized_distance * (center - 1) * math.sin(rad))
            
            # Ограничение координат
            x = max(0, min(radar_size - 1, x))
            y = max(0, min(radar_size - 1, y))
            
            # Маркер в зависимости от типа звука
            if sound_type == 'footsteps':
                marker = '🟢'
            elif sound_type == 'gunshots':
                marker = '🔴'
            elif sound_type == 'explosions':
                marker = '🟠'
            else:
                marker = '⚪'
            
            radar[y][x] = marker
        
        # Отрисовка радара
        print("🎵 CS2 Sound Assistant - Демо")
        print("=" * 40)
        print("Радар обнаружений:")
        print()
        
        for row in radar:
            print(' '.join(row))
        
        print()
        print("Легенда:")
        print("🟢 - Шаги | 🔴 - Выстрелы | 🟠 - Взрывы | ⚪ - Неизвестно")
        print()
        print(f"Обнаружений: {len(self.detections)}")
        print("=" * 40)

class CS2SoundAssistantDemo:
    """Демо версия CS2 Sound Assistant"""
    
    def __init__(self):
        self.config = DemoConfig()
        self.audio_capture = DemoAudioCapture(self.config)
        self.sound_analyzer = DemoSoundAnalyzer(self.config)
        self.position_calculator = DemoPositionCalculator(self.config)
        self.overlay = DemoOverlay(self.config)
        
        self.running = False
        
    def start(self):
        """Запуск демо"""
        print("🎵 Запуск CS2 Sound Assistant - Демо версия")
        print("📊 Режим: Симуляция звуков")
        print("🎯 Цель: Демонстрация концепции")
        print()
        print("💡 Управление:")
        print("   Ctrl+C - Выход")
        print("   Enter - Пауза/Продолжение")
        print()
        
        self.running = True
        
        try:
            while self.running:
                # Захват аудио
                audio_data = self.audio_capture.get_audio_chunk()
                
                # Анализ звуков
                sounds = self.sound_analyzer.analyze_audio(audio_data)
                
                # Расчет позиций
                detections = []
                for sound in sounds:
                    # Извлечение каналов из аудио данных
                    left_channel = [sample[0] for sample in audio_data]
                    right_channel = [sample[1] for sample in audio_data]
                    
                    position = self.position_calculator.calculate_position(left_channel, right_channel)
                    
                    if position:
                        detections.append({
                            'sound_type': sound['type'],
                            'angle': position['angle'],
                            'distance': position['distance'],
                            'confidence': sound['confidence']
                        })
                
                # Обновление отображения
                self.overlay.update(detections)
                self.overlay.draw_radar()
                
                # Пауза
                time.sleep(1.0)  # Обновление каждую секунду
                
        except KeyboardInterrupt:
            print("\n🛑 Остановка демо...")
        except Exception as e:
            print(f"❌ Ошибка: {e}")
        finally:
            self.stop()
    
    def stop(self):
        """Остановка демо"""
        self.running = False
        print("✅ Демо остановлено")

def main():
    """Главная функция"""
    print("🎵 CS2 Sound Assistant - Демо версия")
    print("=" * 50)
    print()
    print("Это демонстрационная версия системы.")
    print("Она симулирует работу реальной системы без захвата аудио.")
    print()
    print("В реальной версии система будет:")
    print("- Захватывать системный аудио поток")
    print("- Анализировать звуки CS2 в реальном времени")
    print("- Отображать позиции противников на overlay")
    print("- Работать с калибровкой для точности")
    print()
    
    input("Нажмите Enter для запуска демо...")
    
    # Создание и запуск демо
    demo = CS2SoundAssistantDemo()
    demo.start()

if __name__ == "__main__":
    main()
