#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CS2 Sound Assistant - Главный файл системы
Система анализа звуков Counter-Strike 2 для определения позиций противников
"""

import sys
import time
import threading
import argparse
from pathlib import Path

# Добавляем путь к модулям
sys.path.append(str(Path(__file__).parent / "src"))

try:
    from src.audio.capture import AudioCapture
    from src.analysis.analyzer import SoundAnalyzer
    from src.positioning.calculator import PositionCalculator
    from src.display.overlay import OverlayDisplay
    from src.utils.calibration import CalibrationSystem
    from src.utils.config import Config
except ImportError as e:
    print(f"❌ Ошибка импорта модулей: {e}")
    print("Убедитесь, что все файлы созданы в правильных папках")
    exit(1)

class CS2SoundAssistant:
    """Основной класс системы CS2 Sound Assistant"""
    
    def __init__(self, config):
        """Инициализация системы"""
        self.config = config
        self.running = False
        
        # Компоненты будут инициализированы в initialize_components
        self.audio_capture = None
        self.sound_analyzer = None
        self.position_calculator = None
        self.overlay_display = None
        
        # Потоки
        self.audio_thread = None
        self.analysis_thread = None
        
        # Данные для анализа
        self.audio_buffer = []
        self.detections = []
        
    def start(self):
        """Запуск системы"""
        print("🎵 Запуск CS2 Sound Assistant...")
        print("📊 Режим: Тренировка с ботами")
        print("🎯 Цель: Настройка отображения по звуку")
        
        try:
            # Инициализация компонентов
            self.initialize_components()
            
            # Запуск потоков
            self.running = True
            self.start_threads()
            
            # Основной цикл
            self.main_loop()
            
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.stop()
    
    def initialize_components(self):
        """Инициализация всех компонентов"""
        print("🔧 Инициализация компонентов...")
        
        # Инициализация захвата аудио
        self.audio_capture = AudioCapture(
            sample_rate=self.config.get('audio.sample_rate', 48000),
            channels=self.config.get('audio.channels', 2),
            chunk_size=self.config.get('audio.chunk_size', 1024)
        )
        self.audio_capture.initialize()
        self.audio_capture.start_capture()  # Запуск захвата
        
        # Инициализация анализатора
        self.sound_analyzer = SoundAnalyzer(self.config)
        self.sound_analyzer.initialize()
        
        # Инициализация калькулятора позиций
        self.position_calculator = PositionCalculator(self.config)
        self.position_calculator.initialize()
        
        # Инициализация overlay
        self.overlay_display = OverlayDisplay(self.config)
        self.overlay_display.initialize()
        
        print("✅ Компоненты инициализированы")
    
    def start_threads(self):
        """Запуск рабочих потоков"""
        print("🚀 Запуск потоков...")
        
        # Установка флага запуска
        self.running = True
        
        # Поток захвата аудио
        self.audio_thread = threading.Thread(target=self.audio_loop, daemon=True)
        self.audio_thread.start()
        
        # Поток анализа
        self.analysis_thread = threading.Thread(target=self.analysis_loop, daemon=True)
        self.analysis_thread.start()
        
        print("✅ Потоки запущены")
    
    def audio_loop(self):
        """Поток захвата аудио"""
        while self.running:
            try:
                # Захват аудио данных
                audio_data = self.audio_capture.get_audio_chunk()
                
                if audio_data is not None:
                    # Добавление в буфер
                    self.audio_buffer.append(audio_data)
                    
                    # Ограничение размера буфера
                    if len(self.audio_buffer) > 10:
                        self.audio_buffer.pop(0)
                
                time.sleep(0.01)  # 100 FPS
                
            except Exception as e:
                print(f"❌ Ошибка в аудио потоке: {e}")
                time.sleep(0.1)
    
    def analysis_loop(self):
        """Поток анализа звуков"""
        while self.running:
            try:
                if self.audio_buffer:
                    # Берем последние данные
                    audio_data = self.audio_buffer[-1]
                    
                    # Анализ звуков
                    sounds = self.sound_analyzer.analyze_audio(audio_data)
                    
                    if sounds:
                        # Расчет позиций
                        positions = []
                        
                        # Проверяем тип sounds
                        if not isinstance(sounds, dict):
                            print(f"❌ sounds не словарь: {type(sounds)}")
                            continue
                            
                        # Извлекаем тип звука из вложенного словаря
                        sound_type_data = sounds.get('type', {})
                        if isinstance(sound_type_data, dict):
                            sound_type = sound_type_data.get('type', 'unknown')
                            confidence = sound_type_data.get('confidence', 0.5)
                        else:
                            sound_type = sound_type_data
                            confidence = 0.5
                            
                        # Пропускаем звуки с низкой уверенностью
                        if confidence < 0.0001:  # Сниженный порог уверенности
                            print(f"❌ Низкая уверенность: {confidence}")
                            continue
                            
                        print(f"🎯 Высокая уверенность: {confidence}, тип: {sound_type}, рассчитываем позицию")
                        
                        position = self.position_calculator.calculate_position(
                            audio_data[:, 0],  # Левый канал
                            audio_data[:, 1]   # Правый канал
                        )
                        
                        # Проверяем тип position
                        if position:
                            if isinstance(position, str):
                                # Если position это строка, пропускаем
                                continue
                            elif isinstance(position, dict):
                                try:
                                    detection_data = {
                                        'sound_type': sound_type,
                                        'angle': float(position['angle']),
                                        'distance': float(position['distance']),
                                        'confidence': float(confidence),
                                        'timestamp': time.time()
                                    }
                                    
                                    positions.append(detection_data)
                                    print(f"✅ detection_data создан: {detection_data}")
                                except (KeyError, ValueError, TypeError) as e:
                                    print(f"❌ Ошибка создания detection_data: {e}")
                                    continue
                            else:
                                print(f"❌ Неизвестный тип position: {type(position)}")
                                continue
                        
                        # Обновление обнаружений
                        self.detections = positions
                        
                        # Передача данных в overlay напрямую
                        if self.overlay_display:
                            self.overlay_display.detections = positions.copy()
                        
                        # Отладочная информация
                        if positions:
                            print(f"🎯 Передано в overlay: {len(positions)} обнаружений")
                            print(f"🎯 Последнее обнаружение: {positions[-1]}")
                
                time.sleep(0.02)  # 50 FPS
                
            except Exception as e:
                print(f"❌ Ошибка в потоке анализа: {e}")
                time.sleep(0.1)
    
    def main_loop(self):
        """Основной цикл отображения"""
        print("🎮 Основной цикл запущен")
        print("💡 Управление:")
        print("   ESC - Выход")
        print("   C - Калибровка")
        print("   S - Сохранение настроек")
        print("   R - Сброс обнаружений")
        
        # Запуск overlay в главном потоке
        self.overlay_display.start()
        
        # Основной цикл теперь не нужен, так как overlay.mainloop() блокирует выполнение
    
    def stop(self):
        """Остановка системы"""
        print("🛑 Остановка системы...")
        
        self.running = False
        
        # Остановка компонентов
        self.audio_capture.stop()
        self.overlay_display.stop()
        
        print("✅ Система остановлена")

def main():
    """Главная функция"""
    parser = argparse.ArgumentParser(description="CS2 Sound Assistant")
    parser.add_argument("--calibrate", action="store_true", help="Запуск калибровки")
    parser.add_argument("--config", type=str, help="Путь к файлу конфигурации")
    
    args = parser.parse_args()
    
    # Создание и запуск системы
    assistant = CS2SoundAssistant(Config()) # Pass Config() to the constructor
    
    if args.calibrate:
        assistant.calibration_system.start_calibration()
    else:
        assistant.start()

if __name__ == "__main__":
    main()
