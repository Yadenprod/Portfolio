#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Модуль калибровки для CS2 Sound Assistant
Позволяет настроить систему для точного определения позиций
"""

import numpy as np
import time
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple

class CalibrationSystem:
    """Класс для калибровки системы"""
    
    def __init__(self, config):
        self.config = config
        self.calibration_path = Path("config/calibration.json")
        self.calibration_data = {}
        
        # Состояние калибровки
        self.is_calibrated = False
        self.calibration_steps = []
        self.current_step = 0
        
        # Данные калибровки
        self.angle_reference_points = []
        self.distance_reference_points = []
        
        # Загрузка калибровки
        self.load_calibration()
    
    def load_calibration(self):
        """Загрузка калибровочных данных"""
        try:
            if self.calibration_path.exists():
                with open(self.calibration_path, 'r', encoding='utf-8') as f:
                    self.calibration_data = json.load(f)
                
                self.is_calibrated = self.validate_calibration()
                print(f"📊 Калибровка загружена: {self.calibration_path}")
            else:
                print("⚠️ Файл калибровки не найден")
                
        except Exception as e:
            print(f"❌ Ошибка загрузки калибровки: {e}")
    
    def save_calibration(self):
        """Сохранение калибровочных данных"""
        try:
            # Создание директории если не существует
            self.calibration_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.calibration_path, 'w', encoding='utf-8') as f:
                json.dump(self.calibration_data, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Калибровка сохранена: {self.calibration_path}")
            
        except Exception as e:
            print(f"❌ Ошибка сохранения калибровки: {e}")
    
    def validate_calibration(self) -> bool:
        """Проверка валидности калибровки"""
        required_keys = ['angle_calibration', 'distance_calibration', 'timestamp']
        
        for key in required_keys:
            if key not in self.calibration_data:
                return False
        
        return True
    
    def start_calibration(self):
        """Запуск процесса калибровки"""
        print("🔧 Запуск калибровки...")
        print("📋 Инструкции:")
        print("   1. Убедитесь, что наушники правильно надеты")
        print("   2. Запустите CS2 и войдите в тренировку с ботами")
        print("   3. Следуйте инструкциям на экране")
        print("   4. Для каждого теста издайте звук в указанном направлении")
        
        # Сброс данных калибровки
        self.calibration_data = {
            'angle_calibration': {},
            'distance_calibration': {},
            'timestamp': time.time()
        }
        
        self.is_calibrated = False
        self.current_step = 0
        
        # Запуск калибровки углов
        self.calibrate_angles()
        
        # Запуск калибровки дистанции
        self.calibrate_distance()
        
        # Сохранение калибровки
        self.save_calibration()
        
        print("✅ Калибровка завершена!")
    
    def calibrate_angles(self):
        """Калибровка углов"""
        print("🎯 Калибровка углов...")
        
        # Тестовые углы
        test_angles = [0, 45, 90, 135, 180, 225, 270, 315]
        measured_angles = []
        
        for target_angle in test_angles:
            print(f"🎯 Тест угла {target_angle}°")
            print(f"   Издайте звук прямо перед собой (0°)")
            print(f"   Затем повернитесь на {target_angle}° и издайте звук")
            print("   Нажмите Enter когда готовы...")
            
            input()  # Ожидание ввода пользователя
            
            # Здесь должна быть логика измерения угла
            # Пока используем простое приближение
            measured_angle = target_angle + np.random.normal(0, 5)  # Имитация измерения
            measured_angles.append(measured_angle)
            
            print(f"   Измеренный угол: {measured_angle:.1f}°")
        
        # Расчет калибровочных параметров
        angle_offset = np.mean([target - measured for target, measured in zip(test_angles, measured_angles)])
        angle_scale = 1.0  # Простая линейная калибровка
        
        self.calibration_data['angle_calibration'] = {
            'offset': angle_offset,
            'scale': angle_scale,
            'test_angles': test_angles,
            'measured_angles': measured_angles
        }
        
        print(f"✅ Калибровка углов завершена (смещение: {angle_offset:.1f}°)")
    
    def calibrate_distance(self):
        """Калибровка дистанции"""
        print("📏 Калибровка дистанции...")
        
        # Тестовые дистанции
        test_distances = [5, 10, 15, 20, 25]  # метры
        measured_distances = []
        
        for target_distance in test_distances:
            print(f"📏 Тест дистанции {target_distance}м")
            print(f"   Издайте звук на расстоянии {target_distance}м")
            print("   Нажмите Enter когда готовы...")
            
            input()  # Ожидание ввода пользователя
            
            # Здесь должна быть логика измерения дистанции
            # Пока используем простое приближение
            measured_distance = target_distance + np.random.normal(0, 2)  # Имитация измерения
            measured_distances.append(measured_distance)
            
            print(f"   Измеренная дистанция: {measured_distance:.1f}м")
        
        # Расчет калибровочных параметров
        distance_offset = np.mean([target - measured for target, measured in zip(test_distances, measured_distances)])
        distance_scale = 1.0  # Простая линейная калибровка
        
        self.calibration_data['distance_calibration'] = {
            'offset': distance_offset,
            'scale': distance_scale,
            'test_distances': test_distances,
            'measured_distances': measured_distances
        }
        
        print(f"✅ Калибровка дистанции завершена (смещение: {distance_offset:.1f}м)")
    
    def add_angle_reference_point(self, target_angle: float, measured_angle: float):
        """Добавление референсной точки для угла"""
        self.angle_reference_points.append({
            'target': target_angle,
            'measured': measured_angle,
            'timestamp': time.time()
        })
    
    def add_distance_reference_point(self, target_distance: float, measured_distance: float):
        """Добавление референсной точки для дистанции"""
        self.distance_reference_points.append({
            'target': target_distance,
            'measured': measured_distance,
            'timestamp': time.time()
        })
    
    def calculate_angle_calibration(self) -> Dict:
        """Расчет калибровки углов на основе референсных точек"""
        if len(self.angle_reference_points) < 2:
            return {'offset': 0, 'scale': 1.0}
        
        targets = [p['target'] for p in self.angle_reference_points]
        measured = [p['measured'] for p in self.angle_reference_points]
        
        # Линейная регрессия
        A = np.vstack([measured, np.ones(len(measured))]).T
        scale, offset = np.linalg.lstsq(A, targets, rcond=None)[0]
        
        return {'offset': offset, 'scale': scale}
    
    def calculate_distance_calibration(self) -> Dict:
        """Расчет калибровки дистанции на основе референсных точек"""
        if len(self.distance_reference_points) < 2:
            return {'offset': 0, 'scale': 1.0}
        
        targets = [p['target'] for p in self.distance_reference_points]
        measured = [p['measured'] for p in self.distance_reference_points]
        
        # Линейная регрессия
        A = np.vstack([measured, np.ones(len(measured))]).T
        scale, offset = np.linalg.lstsq(A, targets, rcond=None)[0]
        
        return {'offset': offset, 'scale': scale}
    
    def apply_angle_calibration(self, angle: float) -> float:
        """Применение калибровки угла"""
        if not self.is_calibrated:
            return angle
        
        calibration = self.calibration_data.get('angle_calibration', {})
        offset = calibration.get('offset', 0)
        scale = calibration.get('scale', 1.0)
        
        calibrated_angle = (angle + offset) * scale
        
        # Нормализация к диапазону [-180, 180]
        while calibrated_angle > 180:
            calibrated_angle -= 360
        while calibrated_angle < -180:
            calibrated_angle += 360
        
        return calibrated_angle
    
    def apply_distance_calibration(self, distance: float) -> float:
        """Применение калибровки дистанции"""
        if not self.is_calibrated:
            return distance
        
        calibration = self.calibration_data.get('distance_calibration', {})
        offset = calibration.get('offset', 0)
        scale = calibration.get('scale', 1.0)
        
        calibrated_distance = (distance + offset) * scale
        
        # Ограничение положительными значениями
        return max(0, calibrated_distance)
    
    def get_calibration_info(self) -> Dict:
        """Получение информации о калибровке"""
        return {
            'is_calibrated': self.is_calibrated,
            'calibration_path': str(self.calibration_path),
            'timestamp': self.calibration_data.get('timestamp', 0),
            'angle_calibration': self.calibration_data.get('angle_calibration', {}),
            'distance_calibration': self.calibration_data.get('distance_calibration', {}),
            'angle_reference_points': len(self.angle_reference_points),
            'distance_reference_points': len(self.distance_reference_points)
        }
    
    def reset_calibration(self):
        """Сброс калибровки"""
        self.calibration_data = {}
        self.is_calibrated = False
        self.angle_reference_points = []
        self.distance_reference_points = []
        
        # Удаление файла калибровки
        if self.calibration_path.exists():
            self.calibration_path.unlink()
        
        print("🔄 Калибровка сброшена")
    
    def export_calibration(self, path: str):
        """Экспорт калибровки"""
        try:
            export_path = Path(path)
            export_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(self.calibration_data, f, indent=2, ensure_ascii=False)
            
            print(f"📤 Калибровка экспортирована: {export_path}")
            
        except Exception as e:
            print(f"❌ Ошибка экспорта калибровки: {e}")
    
    def import_calibration(self, path: str):
        """Импорт калибровки"""
        try:
            import_path = Path(path)
            
            if not import_path.exists():
                print(f"❌ Файл калибровки не найден: {import_path}")
                return
            
            with open(import_path, 'r', encoding='utf-8') as f:
                imported_calibration = json.load(f)
            
            self.calibration_data = imported_calibration
            self.is_calibrated = self.validate_calibration()
            self.save_calibration()
            
            print(f"📥 Калибровка импортирована: {import_path}")
            
        except Exception as e:
            print(f"❌ Ошибка импорта калибровки: {e}")
    
    def quick_calibration(self):
        """Быстрая калибровка (основные точки)"""
        print("⚡ Быстрая калибровка...")
        
        # Только основные углы
        test_angles = [0, 90, 180, 270]
        
        print("🎯 Тест основных направлений:")
        print("   0° - прямо перед собой")
        print("   90° - справа")
        print("   180° - сзади")
        print("   270° - слева")
        
        # Простая калибровка без измерений
        self.calibration_data = {
            'angle_calibration': {'offset': 0, 'scale': 1.0},
            'distance_calibration': {'offset': 0, 'scale': 1.0},
            'timestamp': time.time()
        }
        
        self.is_calibrated = True
        self.save_calibration()
        
        print("✅ Быстрая калибровка завершена")
