"""
Модуль для управления клавиатурой и мышью
"""
import time
import keyboard
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController
from typing import Optional


class GameController:
    """Класс для управления игрой через клавиатуру и мышь"""
    
    def __init__(self):
        """Инициализация контроллера"""
        self.mouse = MouseController()
        self.keyboard = KeyboardController()
        self.is_active = False
    
    def press_key(self, key: str, duration: float = 0.1):
        """
        Нажимает клавишу
        
        Args:
            key: Символ клавиши или специальная клавиша
            duration: Длительность нажатия в секундах
        """
        if not self.is_active:
            return
        
        try:
            # Обработка специальных клавиш
            special_keys = {
                'w': 'w', 'a': 'a', 's': 's', 'd': 'd', 'e': 'e', 'f': 'f', 'g': 'g',
                'space': Key.space,
                'shift': Key.shift,
                'ctrl': Key.ctrl,
                'alt': Key.alt,
                'enter': Key.enter,
                'esc': Key.esc,
                'tab': Key.tab
            }
            
            key_lower = key.lower()
            if key_lower in special_keys:
                key_obj = special_keys[key_lower]
                if isinstance(key_obj, str):
                    # Для обычных символов используем keyboard напрямую
                    keyboard.press(key_obj)
                    time.sleep(duration)
                    keyboard.release(key_obj)
                else:
                    # Для специальных клавиш используем pynput
                    self.keyboard.press(key_obj)
                    time.sleep(duration)
                    self.keyboard.release(key_obj)
            else:
                # Неизвестная клавиша - пробуем через keyboard
                keyboard.press(key)
                time.sleep(duration)
                keyboard.release(key)
        except Exception as e:
            print(f"⚠️ Ошибка при нажатии клавиши {key}: {e}")
    
    def move_mouse(self, x: int, y: int, relative: bool = False):
        """
        Двигает мышь
        
        Args:
            x, y: Координаты или смещение
            relative: Если True, то x, y - это смещение, иначе абсолютные координаты
        """
        if not self.is_active:
            return
        
        if relative:
            self.mouse.move(x, y)
        else:
            self.mouse.position = (x, y)
    
    def click(self, button: str = 'left', x: Optional[int] = None, y: Optional[int] = None):
        """
        Кликает мышью
        
        Args:
            button: 'left' или 'right'
            x, y: Координаты клика (если None, то текущая позиция)
        """
        if not self.is_active:
            return
        
        if x is not None and y is not None:
            self.mouse.position = (x, y)
            time.sleep(0.05)
        
        btn = Button.left if button == 'left' else Button.right
        self.mouse.click(btn)
    
    def hold_key(self, key: str):
        """Удерживает клавишу нажатой"""
        if not self.is_active:
            return
        
        try:
            key_lower = key.lower()
            if key_lower in ['w', 'a', 's', 'd', 'e', 'f', 'g']:
                # Для обычных символов используем keyboard
                keyboard.press(key_lower)
            elif key_lower == 'space':
                self.keyboard.press(Key.space)
            elif key_lower == 'shift':
                self.keyboard.press(Key.shift)
            else:
                keyboard.press(key)
        except Exception as e:
            print(f"⚠️ Ошибка при удержании клавиши {key}: {e}")
    
    def release_key(self, key: str):
        """Отпускает клавишу"""
        if not self.is_active:
            return
        
        try:
            key_lower = key.lower()
            if key_lower in ['w', 'a', 's', 'd', 'e', 'f', 'g']:
                # Для обычных символов используем keyboard
                keyboard.release(key_lower)
            elif key_lower == 'space':
                self.keyboard.release(Key.space)
            elif key_lower == 'shift':
                self.keyboard.release(Key.shift)
            else:
                keyboard.release(key)
        except Exception as e:
            print(f"⚠️ Ошибка при отпускании клавиши {key}: {e}")
    
    def set_active(self, active: bool):
        """
        Активирует/деактивирует контроллер
        
        Args:
            active: True для активации, False для деактивации
        """
        self.is_active = active
        if active:
            print(f"✅ Контроллер АКТИВИРОВАН - готов к управлению")
        else:
            print(f"⏸ Контроллер деактивирован")
    
    def move_forward(self, duration: float = 1.0):
        """Двигается вперед"""
        self.press_key('w', duration)
    
    def turn_left(self, duration: float = 0.5):
        """Поворачивает влево"""
        self.press_key('a', duration)
    
    def turn_right(self, duration: float = 0.5):
        """Поворачивает вправо"""
        self.press_key('d', duration)
    
    def move_backward(self, duration: float = 1.0):
        """Двигается назад"""
        self.press_key('s', duration)

