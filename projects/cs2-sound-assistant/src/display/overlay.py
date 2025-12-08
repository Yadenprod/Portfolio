#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Модуль отображения overlay для CS2 Sound Assistant
Создает overlay окно с радаром для отображения позиций противников
"""

import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
import threading
import time
from typing import List, Dict, Optional

class OverlayDisplay:
    """Класс для отображения overlay с радаром"""
    
    def __init__(self, config):
        self.config = config
        
        # Параметры окна
        self.window_size = config.get('display.window_size', [400, 400])
        self.radar_radius = config.get('display.radar_radius', 150)
        self.update_rate = config.get('display.update_rate', 60)
        
        # Центр радара
        self.radar_center = (self.window_size[0] // 2, self.window_size[1] // 2)
        
        # Состояние
        self.is_initialized = False
        self.is_running = False
        self.window = None
        self.canvas = None
        
        # Данные для отображения
        self.detections = []
        self.detection_history = []
        self.max_history = 10
        
        # Цвета для разных типов звуков
        self.sound_colors = {
            'footsteps': (0, 255, 0),    # Зеленый
            'gunshots': (0, 0, 255),     # Красный
            'explosions': (255, 165, 0), # Оранжевый
            'voices': (255, 255, 0),     # Желтый
            'unknown': (128, 128, 128)   # Серый
        }
        
        # Настройки отображения
        self.show_confidence = True
        self.show_distance = True
        self.show_history = True
        self.fade_time = 3.0  # Время затухания маркеров
        
    def initialize(self):
        """Инициализация overlay"""
        print("🖥️ Инициализация overlay...")
        
        try:
            # Создание окна
            self.create_window()
            
            # Создание canvas
            self.create_canvas()
            
            # Настройка событий
            self.setup_events()
            
            self.is_initialized = True
            print("✅ Overlay инициализирован")
            
        except Exception as e:
            print(f"❌ Ошибка инициализации overlay: {e}")
            raise
    
    def create_window(self):
        """Создание окна overlay"""
        self.window = tk.Tk()
        self.window.title("CS2 Sound Assistant - Overlay")
        self.window.geometry(f"{self.window_size[0]}x{self.window_size[1]}")
        
        # Настройка окна
        self.window.configure(bg='black')
        self.window.attributes('-topmost', True)  # Поверх всех окон
        self.window.attributes('-alpha', 0.8)     # Прозрачность
        self.window.resizable(False, False)
        
        # Удаление рамки окна
        self.window.overrideredirect(True)
        
        # Центрирование окна
        self.center_window()
    
    def create_canvas(self):
        """Создание canvas для отрисовки"""
        self.canvas = tk.Canvas(
            self.window,
            width=self.window_size[0],
            height=self.window_size[1],
            bg='black',
            highlightthickness=0
        )
        self.canvas.pack()
    
    def setup_events(self):
        """Настройка событий окна"""
        # Обработка клавиш
        self.window.bind('<Key>', self.on_key_press)
        self.window.bind('<Escape>', self.on_escape)
        
        # Обработка мыши
        self.window.bind('<Button-1>', self.on_mouse_click)
        self.window.bind('<B1-Motion>', self.on_mouse_drag)
        
        # Обработка закрытия
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def center_window(self):
        """Центрирование окна на экране"""
        self.window.update_idletasks()
        
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        x = (screen_width - self.window_size[0]) // 2
        y = (screen_height - self.window_size[1]) // 2
        
        self.window.geometry(f"+{x}+{y}")
    
    def start(self):
        """Запуск отображения"""
        if not self.is_initialized:
            raise Exception("Overlay не инициализирован")
        
        if self.is_running:
            return
        
        self.is_running = True
        
        # Запуск цикла обновления
        self.update_loop()
        
        # Запуск главного цикла tkinter
        self.window.mainloop()
    
    def update_loop(self):
        """Цикл обновления отображения"""
        if not self.is_running:
            return
        
        try:
            # Очистка canvas
            self.canvas.delete("all")
            
            # Отрисовка радара
            self.draw_radar()
            
            # Отрисовка обнаружений
            self.draw_detections()
            
            # Отрисовка информации
            self.draw_info()
            
            # Обновление истории
            self.update_history()
            
            # Отладочная информация
            if hasattr(self, '_debug_counter'):
                self._debug_counter += 1
            else:
                self._debug_counter = 0
                
            if self._debug_counter % 100 == 0:
                print(f"📊 Overlay обновлен: {len(self.detections)} обнаружений")
                if self.detections:
                    print(f"🎯 Последнее обнаружение: {self.detections[-1]}")
            
            # Планирование следующего обновления
            self.window.after(1000 // self.update_rate, self.update_loop)
            
        except Exception as e:
            print(f"❌ Ошибка обновления overlay: {e}")
            import traceback
            traceback.print_exc()
    
    def draw_radar(self):
        """Отрисовка радара"""
        # Внешний круг
        self.canvas.create_oval(
            self.radar_center[0] - self.radar_radius,
            self.radar_center[1] - self.radar_radius,
            self.radar_center[0] + self.radar_radius,
            self.radar_center[1] + self.radar_radius,
            outline='#00FF00',
            width=2,
            tags="radar"
        )
        
        # Внутренние круги (дистанция)
        for i in range(1, 4):
            radius = self.radar_radius * i // 4
            self.canvas.create_oval(
                self.radar_center[0] - radius,
                self.radar_center[1] - radius,
                self.radar_center[0] + radius,
                self.radar_center[1] + radius,
                outline='#004400',
                width=1,
                tags="radar"
            )
        
        # Линии направлений (каждые 45 градусов)
        for angle in range(0, 360, 45):
            rad = np.radians(angle)
            end_x = self.radar_center[0] + self.radar_radius * np.cos(rad)
            end_y = self.radar_center[1] + self.radar_radius * np.sin(rad)
            
            self.canvas.create_line(
                self.radar_center[0],
                self.radar_center[1],
                end_x,
                end_y,
                fill='#004400',
                width=1,
                tags="radar"
            )
        
        # Центральная точка
        self.canvas.create_oval(
            self.radar_center[0] - 3,
            self.radar_center[1] - 3,
            self.radar_center[0] + 3,
            self.radar_center[1] + 3,
            fill='#00FF00',
            tags="radar"
        )
    
    def draw_detections(self):
        """Отрисовка обнаружений"""
        try:
            current_time = time.time()
            
            # Отрисовка истории
            if self.show_history:
                for detection in self.detection_history:
                    age = current_time - detection['timestamp']
                    if age < self.fade_time:
                        alpha = 1.0 - (age / self.fade_time)
                        self.draw_detection_marker(detection, alpha)
            
            # Отрисовка текущих обнаружений
            print(f"🎯 Отрисовка {len(self.detections)} обнаружений на радаре")
            for i, detection in enumerate(self.detections):
                print(f"   Отрисовка {i}: {detection['sound_type']} - угол:{detection['angle']:.1f}° дистанция:{detection['distance']:.1f}m")
                self.draw_detection_marker(detection, 1.0)
                
        except Exception as e:
            print(f"❌ Ошибка отрисовки обнаружений: {e}")
            import traceback
            traceback.print_exc()
    
    def draw_detection_marker(self, detection: Dict, alpha: float = 1.0):
        """Отрисовка маркера обнаружения"""
        angle = detection['angle']
        distance = detection['distance']
        sound_type = detection.get('sound_type', 'unknown')
        confidence = detection.get('confidence', 0.5)
        
        # Конвертация в координаты
        rad = np.radians(angle)
        normalized_distance = min(distance / 50.0, 1.0)  # Нормализация к радиусу радара
        
        x = self.radar_center[0] + normalized_distance * self.radar_radius * np.cos(rad)
        y = self.radar_center[1] + normalized_distance * self.radar_radius * np.sin(rad)
        
        # Цвет маркера
        base_color = self.sound_colors.get(sound_type, self.sound_colors['unknown'])
        color = self.adjust_color_alpha(base_color, alpha)
        
        # Размер маркера (зависит от уверенности)
        size = int(8 + confidence * 8)
        
        # Отрисовка маркера
        self.canvas.create_oval(
            x - size, y - size,
            x + size, y + size,
            fill=color,
            outline='white',
            width=2,
            tags="detection"
        )
        
        # Текст с информацией
        if self.show_confidence or self.show_distance:
            info_text = []
            if self.show_confidence:
                info_text.append(f"{confidence:.1f}")
            if self.show_distance:
                info_text.append(f"{distance:.1f}m")
            
            if info_text:
                text = " | ".join(info_text)
                self.canvas.create_text(
                    x, y - size - 10,
                    text=text,
                    fill='white',
                    font=('Arial', 8),
                    tags="detection"
                )
    
    def adjust_color_alpha(self, color: tuple, alpha: float) -> str:
        """Корректировка цвета с учетом прозрачности"""
        r, g, b = color
        r = int(r * alpha)
        g = int(g * alpha)
        b = int(b * alpha)
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def draw_info(self):
        """Отрисовка информации"""
        # Статистика
        stats_text = f"Обнаружений: {len(self.detections)}"
        self.canvas.create_text(
            10, 10,
            text=stats_text,
            fill='white',
            anchor='nw',
            font=('Arial', 10),
            tags="info"
        )
        
        # Управление
        controls_text = "ESC - Выход | C - Калибровка | S - Сохранение"
        self.canvas.create_text(
            self.window_size[0] // 2, self.window_size[1] - 20,
            text=controls_text,
            fill='white',
            anchor='center',
            font=('Arial', 8),
            tags="info"
        )
    
    def update_history(self):
        """Обновление истории обнаружений"""
        current_time = time.time()
        
        # Добавление новых обнаружений в историю
        for detection in self.detections:
            self.detection_history.append(detection.copy())
        
        # Удаление старых обнаружений
        self.detection_history = [
            d for d in self.detection_history
            if current_time - d['timestamp'] < self.fade_time
        ]
        
        # Ограничение размера истории
        if len(self.detection_history) > self.max_history:
            self.detection_history = self.detection_history[-self.max_history:]
    
    def update(self, detections: List[Dict]):
        """Обновление данных обнаружений"""
        self.detections = detections
    
    def update_display(self, sound_data: Optional[dict] = None):
        """Обновление отображения с новыми данными"""
        try:
            if sound_data:
                # Добавление нового звука
                self.detections.append(sound_data)
                
                # Ограничение количества звуков
                if len(self.detections) > self.max_history:
                    self.detections.pop(0)
                
                # Отладочная информация
                if hasattr(self, '_debug_counter'):
                    self._debug_counter += 1
                else:
                    self._debug_counter = 0
                    
                if self._debug_counter % 10 == 0:
                    print(f"🎯 Overlay получил данные: {sound_data}")
                    print(f"📊 Всего обнаружений в overlay: {len(self.detections)}")
            
        except Exception as e:
            print(f"❌ Ошибка обновления overlay: {e}")
            import traceback
            traceback.print_exc()
    
    def on_key_press(self, event):
        """Обработка нажатия клавиш"""
        key = event.keysym.lower()
        
        if key == 'escape':
            self.on_escape()
        elif key == 'c':
            print("🔧 Запрос калибровки")
        elif key == 's':
            print("💾 Запрос сохранения")
        elif key == 'h':
            self.show_history = not self.show_history
        elif key == 'i':
            self.show_confidence = not self.show_confidence
        elif key == 'd':
            self.show_distance = not self.show_distance
    
    def on_escape(self, event=None):
        """Обработка клавиши Escape"""
        self.stop()
    
    def on_mouse_click(self, event):
        """Обработка клика мыши"""
        # Перемещение окна
        self.window.focus_set()
    
    def on_mouse_drag(self, event):
        """Обработка перетаскивания мыши"""
        # Перемещение окна
        pass
    
    def on_close(self):
        """Обработка закрытия окна"""
        self.stop()
    
    def get_key(self) -> int:
        """Получение нажатой клавиши"""
        try:
            return self.window.focus_get().winfo_toplevel().winfo_id()
        except:
            return -1
    
    def stop(self):
        """Остановка overlay"""
        print("🛑 Overlay остановлен")
        self.is_running = False
        
        if hasattr(self, 'window') and self.window:
            try:
                self.window.quit()
                self.window.destroy()
            except Exception as e:
                print(f"⚠️ Ошибка закрытия окна: {e}")
            finally:
                self.window = None
    
    def set_position(self, x: int, y: int):
        """Установка позиции окна"""
        if self.window:
            self.window.geometry(f"+{x}+{y}")
    
    def set_transparency(self, alpha: float):
        """Установка прозрачности окна"""
        if self.window:
            self.window.attributes('-alpha', alpha)
    
    def toggle_visibility(self):
        """Переключение видимости окна"""
        if self.window:
            if self.window.state() == 'withdrawn':
                self.window.deiconify()
            else:
                self.window.withdraw()
