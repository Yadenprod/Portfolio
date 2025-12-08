#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Система сбора данных для обучения ИИ CS2
"""

import numpy as np
import sounddevice as sd
import time
import json
import os
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import threading
import queue
import wave
import pickle

class CS2DataCollector:
    """Система сбора данных для обучения ИИ"""
    
    def __init__(self, output_dir: str = "training_data"):
        self.output_dir = output_dir
        self.sample_rate = 48000
        self.chunk_size = 4800  # 100ms при 48kHz
        self.recording = False
        self.audio_queue = queue.Queue()
        self.current_session = None
        
        # Создание папок
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(f"{output_dir}/audio", exist_ok=True)
        os.makedirs(f"{output_dir}/metadata", exist_ok=True)
        
        # Статистика
        self.session_stats = {
            'total_samples': 0,
            'sound_types': {},
            'positions': []
        }
        
        print("📊 Система сбора данных инициализирована")
    
    def start_recording(self, session_name: str = None):
        """Начало записи"""
        if self.recording:
            print("⚠️ Запись уже идет")
            return
        
        if session_name is None:
            session_name = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        self.current_session = session_name
        self.recording = True
        
        # Создание папок для сессии
        session_audio_dir = f"{self.output_dir}/audio/{session_name}"
        session_metadata_dir = f"{self.output_dir}/metadata/{session_name}"
        os.makedirs(session_audio_dir, exist_ok=True)
        os.makedirs(session_metadata_dir, exist_ok=True)
        
        # Запуск записи аудио
        self.audio_thread = threading.Thread(target=self._audio_recording_thread)
        self.audio_thread.start()
        
        print(f"🎙️ Начата запись сессии: {session_name}")
        print("💡 Используйте команды для разметки данных:")
        print("  - 'footsteps 45 25' - шаги под углом 45° на расстоянии 25м")
        print("  - 'gunshot 90 50' - выстрел справа на 50м")
        print("  - 'voice 0 10' - голос впереди на 10м")
        print("  - 'stop' - остановить запись")
    
    def stop_recording(self):
        """Остановка записи"""
        if not self.recording:
            print("⚠️ Запись не идет")
            return
        
        self.recording = False
        self.audio_thread.join()
        
        # Сохранение статистики сессии
        self._save_session_stats()
        
        print(f"✅ Запись остановлена. Сессия: {self.current_session}")
        print(f"📊 Собрано {self.session_stats['total_samples']} образцов")
    
    def _audio_recording_thread(self):
        """Поток записи аудио"""
        try:
            with sd.InputStream(
                samplerate=self.sample_rate,
                channels=2,
                dtype=np.float32,
                blocksize=self.chunk_size,
                callback=self._audio_callback
            ):
                while self.recording:
                    time.sleep(0.1)
                    
        except Exception as e:
            print(f"❌ Ошибка записи аудио: {e}")
    
    def _audio_callback(self, indata, frames, time, status):
        """Callback для аудио потока"""
        if status:
            print(f"⚠️ Аудио статус: {status}")
        
        # Добавление в очередь
        self.audio_queue.put({
            'audio': indata.copy(),
            'timestamp': time.time(),
            'session': self.current_session
        })
    
    def mark_sound(self, sound_type: str, angle: float, distance: float, description: str = ""):
        """Разметка звука"""
        if not self.recording:
            print("⚠️ Запись не идет")
            return
        
        try:
            # Получение последнего аудио фрагмента
            if self.audio_queue.empty():
                print("⚠️ Нет аудио данных для разметки")
                return
            
            audio_data = self.audio_queue.get()
            
            # Создание уникального ID
            sample_id = f"{sound_type}_{angle}_{distance}_{int(time.time() * 1000)}"
            
            # Сохранение аудио
            audio_path = f"{self.output_dir}/audio/{self.current_session}/{sample_id}.wav"
            self._save_audio(audio_data['audio'], audio_path)
            
            # Создание метаданных
            metadata = {
                'sample_id': sample_id,
                'session': self.current_session,
                'sound_type': sound_type,
                'angle': float(angle),
                'distance': float(distance),
                'description': description,
                'timestamp': audio_data['timestamp'],
                'audio_path': audio_path,
                'sample_rate': self.sample_rate,
                'channels': 2,
                'duration': len(audio_data['audio']) / self.sample_rate
            }
            
            # Сохранение метаданных
            metadata_path = f"{self.output_dir}/metadata/{self.current_session}/{sample_id}.json"
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            # Обновление статистики
            self.session_stats['total_samples'] += 1
            if sound_type not in self.session_stats['sound_types']:
                self.session_stats['sound_types'][sound_type] = 0
            self.session_stats['sound_types'][sound_type] += 1
            self.session_stats['positions'].append({
                'angle': angle,
                'distance': distance,
                'sound_type': sound_type
            })
            
            print(f"✅ Размечен звук: {sound_type} ({angle}°, {distance}m) - {sample_id}")
            
        except Exception as e:
            print(f"❌ Ошибка разметки: {e}")
    
    def _save_audio(self, audio_data: np.ndarray, file_path: str):
        """Сохранение аудио в WAV"""
        try:
            with wave.open(file_path, 'wb') as wav_file:
                wav_file.setnchannels(2)
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(self.sample_rate)
                wav_file.writeframes((audio_data * 32767).astype(np.int16).tobytes())
        except Exception as e:
            print(f"❌ Ошибка сохранения аудио: {e}")
    
    def _save_session_stats(self):
        """Сохранение статистики сессии"""
        try:
            stats_path = f"{self.output_dir}/metadata/{self.current_session}/session_stats.json"
            with open(stats_path, 'w', encoding='utf-8') as f:
                json.dump(self.session_stats, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Ошибка сохранения статистики: {e}")
    
    def get_training_data(self) -> List[Tuple]:
        """Получение данных для обучения"""
        training_data = []
        
        try:
            # Сканирование всех сессий
            for session_dir in os.listdir(f"{self.output_dir}/metadata"):
                session_path = f"{self.output_dir}/metadata/{session_dir}"
                if not os.path.isdir(session_path):
                    continue
                
                # Чтение метаданных
                for metadata_file in os.listdir(session_path):
                    if not metadata_file.endswith('.json') or metadata_file == 'session_stats.json':
                        continue
                    
                    metadata_path = f"{session_path}/{metadata_file}"
                    with open(metadata_path, 'r', encoding='utf-8') as f:
                        metadata = json.load(f)
                    
                    # Загрузка аудио
                    audio_path = metadata['audio_path']
                    if os.path.exists(audio_path):
                        audio_data = self._load_audio(audio_path)
                        
                        # Создание обучающего примера
                        training_example = (
                            audio_data,
                            (
                                metadata['sound_type'],
                                metadata['angle'],
                                metadata['distance']
                            )
                        )
                        training_data.append(training_example)
            
            print(f"📊 Загружено {len(training_data)} обучающих примеров")
            return training_data
            
        except Exception as e:
            print(f"❌ Ошибка загрузки данных: {e}")
            return []
    
    def _load_audio(self, file_path: str) -> np.ndarray:
        """Загрузка аудио из WAV"""
        try:
            with wave.open(file_path, 'rb') as wav_file:
                frames = wav_file.readframes(wav_file.getnframes())
                audio_data = np.frombuffer(frames, dtype=np.int16)
                audio_data = audio_data.astype(np.float32) / 32767.0
                audio_data = audio_data.reshape(-1, 2)  # Стерео
                return audio_data
        except Exception as e:
            print(f"❌ Ошибка загрузки аудио: {e}")
            return np.zeros((self.chunk_size, 2))
    
    def interactive_collection(self):
        """Интерактивный сбор данных"""
        print("🎮 Интерактивный сбор данных")
        print("=" * 50)
        print("Команды:")
        print("  footsteps <угол> <дистанция> [описание]")
        print("  gunshot <угол> <дистанция> [описание]")
        print("  explosion <угол> <дистанция> [описание]")
        print("  voice <угол> <дистанция> [описание]")
        print("  reload <угол> <дистанция> [описание]")
        print("  grenade <угол> <дистанция> [описание]")
        print("  stop - остановить сбор")
        print("  stats - показать статистику")
        print("=" * 50)
        
        # Начало записи
        session_name = input("Введите название сессии: ").strip()
        if not session_name:
            session_name = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        self.start_recording(session_name)
        
        try:
            while self.recording:
                command = input("> ").strip().lower()
                
                if command == 'stop':
                    break
                elif command == 'stats':
                    self._show_stats()
                elif command.startswith(('footsteps', 'gunshot', 'explosion', 'voice', 'reload', 'grenade')):
                    self._parse_sound_command(command)
                else:
                    print("❌ Неизвестная команда")
                    
        except KeyboardInterrupt:
            print("\n⚠️ Прерывание пользователем")
        
        self.stop_recording()
    
    def _parse_sound_command(self, command: str):
        """Парсинг команды разметки звука"""
        try:
            parts = command.split()
            if len(parts) < 3:
                print("❌ Недостаточно параметров: <тип> <угол> <дистанция> [описание]")
                return
            
            sound_type = parts[0]
            angle = float(parts[1])
            distance = float(parts[2])
            description = " ".join(parts[3:]) if len(parts) > 3 else ""
            
            self.mark_sound(sound_type, angle, distance, description)
            
        except ValueError:
            print("❌ Неверный формат угла или дистанции")
        except Exception as e:
            print(f"❌ Ошибка парсинга команды: {e}")
    
    def _show_stats(self):
        """Показать статистику"""
        print(f"\n📊 Статистика сессии: {self.current_session}")
        print(f"Всего образцов: {self.session_stats['total_samples']}")
        print("Типы звуков:")
        for sound_type, count in self.session_stats['sound_types'].items():
            print(f"  {sound_type}: {count}")
        
        if self.session_stats['positions']:
            angles = [p['angle'] for p in self.session_stats['positions']]
            distances = [p['distance'] for p in self.session_stats['positions']]
            print(f"Средний угол: {np.mean(angles):.1f}°")
            print(f"Средняя дистанция: {np.mean(distances):.1f}m")
