#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Модуль конфигурации для CS2 Sound Assistant
Управляет настройками системы
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

class Config:
    """Класс для управления конфигурацией"""
    
    def __init__(self, config_path: str = "config/settings.json"):
        self.config_path = Path(config_path)
        self.config_data = {}
        
        # Значения по умолчанию
        self.default_config = {
            "audio": {
                "sample_rate": 48000,
                "channels": 2,
                "chunk_size": 1024,
                "device_id": None
            },
            "analysis": {
                "amplitude_threshold": 0.05,
                "frequency_threshold": 0.1,
                "fft_size": 1024
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
            },
            "filters": {
                "noise_threshold": 0.01,
                "voice_filter": True,
                "music_filter": True,
                "noise_filter": True
            },
            "calibration": {
                "distance_calibration": {},
                "angle_calibration": {}
            }
        }
        
        # Загрузка конфигурации
        self.load()
    
    def load(self):
        """Загрузка конфигурации из файла"""
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self.config_data = json.load(f)
                print(f"📄 Конфигурация загружена: {self.config_path}")
            else:
                # Создание файла с настройками по умолчанию
                self.config_data = self.default_config.copy()
                self.save()
                print(f"📄 Создан файл конфигурации: {self.config_path}")
                
        except Exception as e:
            print(f"❌ Ошибка загрузки конфигурации: {e}")
            self.config_data = self.default_config.copy()
    
    def save(self):
        """Сохранение конфигурации в файл"""
        try:
            # Создание директории если не существует
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config_data, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Конфигурация сохранена: {self.config_path}")
            
        except Exception as e:
            print(f"❌ Ошибка сохранения конфигурации: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Получение значения по ключу (поддержка точечной нотации)"""
        keys = key.split('.')
        value = self.config_data
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any):
        """Установка значения по ключу (поддержка точечной нотации)"""
        keys = key.split('.')
        config = self.config_data
        
        # Создание структуры если не существует
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # Установка значения
        config[keys[-1]] = value
    
    def update(self, data: Dict):
        """Обновление конфигурации"""
        self.config_data.update(data)
    
    def reset(self):
        """Сброс к настройкам по умолчанию"""
        self.config_data = self.default_config.copy()
        self.save()
        print("🔄 Конфигурация сброшена к настройкам по умолчанию")
    
    def get_audio_config(self) -> Dict:
        """Получение конфигурации аудио"""
        return self.config_data.get('audio', {})
    
    def get_analysis_config(self) -> Dict:
        """Получение конфигурации анализа"""
        return self.config_data.get('analysis', {})
    
    def get_positioning_config(self) -> Dict:
        """Получение конфигурации позиционирования"""
        return self.config_data.get('positioning', {})
    
    def get_display_config(self) -> Dict:
        """Получение конфигурации отображения"""
        return self.config_data.get('display', {})
    
    def get_filters_config(self) -> Dict:
        """Получение конфигурации фильтров"""
        return self.config_data.get('filters', {})
    
    def get_calibration_config(self) -> Dict:
        """Получение конфигурации калибровки"""
        return self.config_data.get('calibration', {})
    
    def set_audio_config(self, config: Dict):
        """Установка конфигурации аудио"""
        self.config_data['audio'] = config
    
    def set_analysis_config(self, config: Dict):
        """Установка конфигурации анализа"""
        self.config_data['analysis'] = config
    
    def set_positioning_config(self, config: Dict):
        """Установка конфигурации позиционирования"""
        self.config_data['positioning'] = config
    
    def set_display_config(self, config: Dict):
        """Установка конфигурации отображения"""
        self.config_data['display'] = config
    
    def set_filters_config(self, config: Dict):
        """Установка конфигурации фильтров"""
        self.config_data['filters'] = config
    
    def set_calibration_config(self, config: Dict):
        """Установка конфигурации калибровки"""
        self.config_data['calibration'] = config
    
    def export_config(self, path: str):
        """Экспорт конфигурации"""
        try:
            export_path = Path(path)
            export_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(self.config_data, f, indent=2, ensure_ascii=False)
            
            print(f"📤 Конфигурация экспортирована: {export_path}")
            
        except Exception as e:
            print(f"❌ Ошибка экспорта конфигурации: {e}")
    
    def import_config(self, path: str):
        """Импорт конфигурации"""
        try:
            import_path = Path(path)
            
            if not import_path.exists():
                print(f"❌ Файл конфигурации не найден: {import_path}")
                return
            
            with open(import_path, 'r', encoding='utf-8') as f:
                imported_config = json.load(f)
            
            self.config_data = imported_config
            self.save()
            
            print(f"📥 Конфигурация импортирована: {import_path}")
            
        except Exception as e:
            print(f"❌ Ошибка импорта конфигурации: {e}")
    
    def validate_config(self) -> bool:
        """Проверка валидности конфигурации"""
        try:
            # Проверка обязательных секций
            required_sections = ['audio', 'analysis', 'positioning', 'display', 'filters']
            
            for section in required_sections:
                if section not in self.config_data:
                    print(f"❌ Отсутствует секция: {section}")
                    return False
            
            # Проверка значений
            if self.get('audio.sample_rate') <= 0:
                print("❌ Неверная частота дискретизации")
                return False
            
            if self.get('audio.channels') not in [1, 2]:
                print("❌ Неверное количество каналов")
                return False
            
            if self.get('positioning.ear_distance') <= 0:
                print("❌ Неверное расстояние между ушами")
                return False
            
            if self.get('positioning.sound_speed') <= 0:
                print("❌ Неверная скорость звука")
                return False
            
            print("✅ Конфигурация валидна")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка валидации конфигурации: {e}")
            return False
    
    def get_config_info(self) -> Dict:
        """Получение информации о конфигурации"""
        return {
            'config_path': str(self.config_path),
            'sections': list(self.config_data.keys()),
            'is_valid': self.validate_config()
        }
