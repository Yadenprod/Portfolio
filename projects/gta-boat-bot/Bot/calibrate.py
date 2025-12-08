"""
Утилита для калибровки координат миникарты
Помогает определить точные координаты области миникарты на экране
"""

import mss
import cv2
import numpy as np
import sys
import time

# Импорт для работы с окнами Windows
try:
    import win32gui
    import win32con
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False
    print("Предупреждение: win32gui не установлен. Установите pywin32 для захвата окна игры.")

class MinimapCalibrator:
    def __init__(self, window_title="RADMIR CRMP"):
        self.sct = mss.mss()
        self.window_title = window_title
        self.window_handle = None
        self.window_rect = None
        
        # Попытка найти окно игры
        if WIN32_AVAILABLE:
            self.find_game_window()
        
    def find_game_window(self):
        """Находит окно игры по названию и восстанавливает его, если минимизировано"""
        def enum_handler(hwnd, ctx):
            window_text = win32gui.GetWindowText(hwnd)
            if self.window_title.lower() in window_text.lower():
                ctx.append((hwnd, window_text))
        
        windows = []
        if WIN32_AVAILABLE:
            win32gui.EnumWindows(enum_handler, windows)
        
        if windows:
            self.window_handle = windows[0][0]
            print(f"Найдено окно игры: {windows[0][1]}")
            
            # Проверяем, минимизировано ли окно
            placement = win32gui.GetWindowPlacement(self.window_handle)
            is_minimized = placement[1] == win32con.SW_SHOWMINIMIZED
            
            if is_minimized:
                print("Окно минимизировано. Восстанавливаю...")
                # Восстанавливаем окно
                win32gui.ShowWindow(self.window_handle, win32con.SW_RESTORE)
                time.sleep(0.5)  # Даем время окну восстановиться
            
            # Активируем окно и выводим на передний план
            win32gui.SetForegroundWindow(self.window_handle)
            win32gui.ShowWindow(self.window_handle, win32con.SW_SHOW)
            time.sleep(0.3)  # Даем время окну активироваться
            
            # Получаем координаты окна
            self.window_rect = win32gui.GetWindowRect(self.window_handle)
            window_left, window_top, window_right, window_bottom = self.window_rect
            
            # Проверяем валидность координат (не должны быть отрицательными большими числами)
            if window_left < -10000 or window_top < -10000:
                print("Предупреждение: Координаты окна выглядят некорректно.")
                print("Убедитесь, что окно игры видимо на экране.")
                print(f"Координаты окна: {self.window_rect}")
                return False
            
            print(f"Координаты окна: {self.window_rect}")
            print(f"Размер окна: {window_right - window_left} x {window_bottom - window_top}")
            return True
        else:
            print(f"Окно игры '{self.window_title}' не найдено. Будет использован весь экран.")
            self.monitor = self.sct.monitors[1]  # Основной монитор
            return False
        
    def capture_full_screen(self):
        """Захватывает весь экран или окно игры"""
        if self.window_rect and self.window_handle:
            # Проверяем, что окно все еще существует и видимо
            if not win32gui.IsWindow(self.window_handle):
                print("Окно игры было закрыто.")
                return None
            
            # Обновляем координаты на случай, если окно переместилось
            self.window_rect = win32gui.GetWindowRect(self.window_handle)
            window_left, window_top, window_right, window_bottom = self.window_rect
            
            # Проверяем валидность координат
            if window_left < -10000 or window_top < -10000:
                print("Ошибка: Окно игры минимизировано или скрыто.")
                print("Пожалуйста, восстановите окно игры вручную и попробуйте снова.")
                return None
            
            # Захватываем только окно игры
            width = window_right - window_left
            height = window_bottom - window_top
            
            if width <= 0 or height <= 0:
                print("Ошибка: Некорректный размер окна.")
                return None
            
            region = {
                'left': window_left,
                'top': window_top,
                'width': width,
                'height': height
            }
            
            try:
                screenshot = self.sct.grab(region)
            except Exception as e:
                print(f"Ошибка захвата окна: {e}")
                return None
        else:
            # Захватываем весь экран
            screenshot = self.sct.grab(self.monitor)
        
        img = np.array(screenshot)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        return img
    
    def select_region(self):
        """Позволяет пользователю выбрать область миникарты"""
        print("Захватываю скриншот экрана...")
        img = self.capture_full_screen()
        
        if img is None:
            print("Ошибка: Не удалось захватить изображение.")
            print("Убедитесь, что окно игры видимо на экране и не минимизировано.")
            return None
        
        if img.size == 0:
            print("Ошибка: Захвачено пустое изображение.")
            print("Убедитесь, что окно игры видимо на экране.")
            return None
        
        print(f"Захвачено изображение размером: {img.shape[1]} x {img.shape[0]}")
        
        # Создаем окно для выбора области
        print("\nИнструкция:")
        print("1. В открывшемся окне зажмите левую кнопку мыши")
        print("2. Перетащите мышь, чтобы выделить область миникарты")
        print("3. Отпустите кнопку мыши")
        print("4. Нажмите 'Enter' для подтверждения или 'Esc' для отмены")
        
        # Переменные для хранения координат
        drawing = False
        ix, iy = -1, -1
        fx, fy = -1, -1
        
        def mouse_callback(event, x, y, flags, param):
            nonlocal drawing, ix, iy, fx, fy, img_copy
            
            if event == cv2.EVENT_LBUTTONDOWN:
                drawing = True
                ix, iy = x, y
                img_copy = img.copy()
            
            elif event == cv2.EVENT_MOUSEMOVE:
                if drawing:
                    img_copy = img.copy()
                    cv2.rectangle(img_copy, (ix, iy), (x, y), (0, 255, 0), 2)
                    cv2.imshow('Выберите область миникарты', img_copy)
            
            elif event == cv2.EVENT_LBUTTONUP:
                drawing = False
                fx, fy = x, y
                cv2.rectangle(img_copy, (ix, iy), (fx, fy), (0, 255, 0), 2)
                cv2.imshow('Выберите область миникарты', img_copy)
        
        img_copy = img.copy()
        cv2.namedWindow('Выберите область миникарты', cv2.WINDOW_NORMAL)
        cv2.setMouseCallback('Выберите область миникарты', mouse_callback)
        cv2.imshow('Выберите область миникарты', img_copy)
        
        while True:
            key = cv2.waitKey(1) & 0xFF
            if key == 13:  # Enter
                if ix != -1 and iy != -1 and fx != -1 and fy != -1:
                    break
            elif key == 27:  # Esc
                cv2.destroyAllWindows()
                return None
        
        cv2.destroyAllWindows()
        
        # Вычисляем координаты
        x1 = min(ix, fx)
        y1 = min(iy, fy)
        x2 = max(ix, fx)
        y2 = max(iy, fy)
        
        width = x2 - x1
        height = y2 - y1
        
        # Координаты для mss
        # Если окно игры найдено, координаты относительны окна
        # Если нет - относительно всего экрана
        if self.window_rect:
            # Координаты относительны окна игры
            region = {
                'left': x1,
                'top': y1,
                'width': width,
                'height': height
            }
        else:
            # Координаты относительно всего экрана
            region = {
                'left': x1,
                'top': y1,
                'width': width,
                'height': height
            }
        
        # Центр миникарты (относительно области)
        center = (width // 2, height // 2)
        
        return region, center
    
    def test_capture(self, region):
        """Тестирует захват выбранной области"""
        print("\nТестирую захват области...")
        print("Нажмите 'q' для выхода из теста")
        
        while True:
            screenshot = self.sct.grab(region)
            img = np.array(screenshot)
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            
            # Рисуем центр
            center_x, center_y = region['width'] // 2, region['height'] // 2
            cv2.circle(img, (center_x, center_y), 5, (0, 255, 0), -1)
            cv2.putText(img, 'CENTER', (center_x + 10, center_y), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            cv2.imshow('Тест захвата миникарты', img)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cv2.destroyAllWindows()

def main():
    print("=" * 60)
    print("Калибровка координат миникарты")
    print("=" * 60)
    
    # Попытка получить название окна из конфигурации
    window_title = "RADMIR CRMP"
    try:
        from config import GAME_WINDOW_TITLE
        window_title = GAME_WINDOW_TITLE
    except ImportError:
        pass
    
    calibrator = MinimapCalibrator(window_title)
    
    result = calibrator.select_region()
    
    if result:
        region, center = result
        
        print("\n" + "=" * 60)
        print("Найденные координаты:")
        print("=" * 60)
        print(f"MINIMAP_REGION = {{")
        print(f"    'left': {region['left']},")
        print(f"    'top': {region['top']},")
        print(f"    'width': {region['width']},")
        print(f"    'height': {region['height']}")
        print(f"}}")
        print(f"\nMINIMAP_CENTER = ({center[0]}, {center[1]})")
        print("=" * 60)
        
        # Сохраняем в файл
        config_content = f"""# Автоматически сгенерированные координаты миникарты
MINIMAP_REGION = {{
    'left': {region['left']},
    'top': {region['top']},
    'width': {region['width']},
    'height': {region['height']}
}}

MINIMAP_CENTER = ({center[0]}, {center[1]})
"""
        
        with open('minimap_config.py', 'w', encoding='utf-8') as f:
            f.write(config_content)
        
        print("\nКоординаты сохранены в файл 'minimap_config.py'")
        print("Скопируйте эти значения в config.py или boat_bot.py")
        
        # Предлагаем протестировать
        test = input("\nХотите протестировать захват? (y/n): ")
        if test.lower() == 'y':
            calibrator.test_capture(region)

if __name__ == "__main__":
    main()

