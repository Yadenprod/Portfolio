"""
Утилита для отладки - показывает что видит бот
Помогает настроить параметры обнаружения
"""

import cv2
import numpy as np
import mss
import time
import sys

# Импорт для работы с окнами Windows
try:
    import win32gui
    import win32con
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False

# Попытка импортировать конфигурацию
try:
    from config import *
except ImportError:
    print("Ошибка: config.py не найден!")
    sys.exit(1)

try:
    from minimap_config import MINIMAP_REGION as CALIBRATED_REGION, MINIMAP_CENTER as CALIBRATED_CENTER
    MINIMAP_REGION = CALIBRATED_REGION
    MINIMAP_CENTER = CALIBRATED_CENTER
except ImportError:
    pass

# Проверяем наличие названия окна в конфигурации
if 'GAME_WINDOW_TITLE' not in globals():
    GAME_WINDOW_TITLE = "RADMIR CRMP"

class DebugViewer:
    def __init__(self, window_title=None):
        self.sct = mss.mss()
        self.minimap_region = MINIMAP_REGION.copy()
        self.minimap_center = MINIMAP_CENTER
        self.window_title = window_title or GAME_WINDOW_TITLE
        self.window_handle = None
        self.window_rect = None
        
        # Находим окно игры
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
                win32gui.ShowWindow(self.window_handle, win32con.SW_RESTORE)
                time.sleep(0.5)
            
            # Активируем окно
            win32gui.SetForegroundWindow(self.window_handle)
            win32gui.ShowWindow(self.window_handle, win32con.SW_SHOW)
            time.sleep(0.3)
            
            self.window_rect = win32gui.GetWindowRect(self.window_handle)
            window_left, window_top, window_right, window_bottom = self.window_rect
            
            if window_left < -10000 or window_top < -10000:
                print("Ошибка: Окно игры минимизировано или скрыто.")
                return False
            
            print(f"Координаты окна: {self.window_rect}")
            return True
        else:
            print(f"Окно игры '{self.window_title}' не найдено. Используется весь экран.")
            return False
        
    def capture_minimap(self):
        """Захватывает скриншот области миникарты из окна игры"""
        try:
            # Если окно игры найдено, обновляем координаты
            if WIN32_AVAILABLE and self.window_handle:
                if not win32gui.IsWindow(self.window_handle):
                    if not self.find_game_window():
                        return None
                
                self.window_rect = win32gui.GetWindowRect(self.window_handle)
                window_left, window_top, window_right, window_bottom = self.window_rect
                
                # Проверяем валидность координат
                if window_left < -10000 or window_top < -10000:
                    print("Окно минимизировано. Попытка восстановления...")
                    win32gui.ShowWindow(self.window_handle, win32con.SW_RESTORE)
                    time.sleep(0.3)
                    self.window_rect = win32gui.GetWindowRect(self.window_handle)
                    window_left, window_top, window_right, window_bottom = self.window_rect
                
                base_region = MINIMAP_REGION.copy()
                capture_region = {
                    'left': window_left + base_region.get('left', 20),
                    'top': window_top + base_region.get('top', 780),
                    'width': base_region.get('width', 300),
                    'height': base_region.get('height', 300)
                }
            else:
                capture_region = self.minimap_region
            
            screenshot = self.sct.grab(capture_region)
            img = np.array(screenshot)
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            return img
        except Exception as e:
            print(f"Ошибка захвата: {e}")
            return None
    
    def find_player_arrow(self, img):
        """Находит стрелочку игрока"""
        h, w = img.shape[:2]
        center_x, center_y = self.minimap_center
        
        search_radius = 60
        x1 = max(0, center_x - search_radius)
        y1 = max(0, center_y - search_radius)
        x2 = min(w, center_x + search_radius)
        y2 = min(h, center_y + search_radius)
        
        roi = img[y1:y2, x1:x2]
        roi_center_x = search_radius
        roi_center_y = search_radius
        
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        
        lower_red1 = np.array(RED_LOWER_1)
        upper_red1 = np.array(RED_UPPER_1)
        lower_red2 = np.array(RED_LOWER_2)
        upper_red2 = np.array(RED_UPPER_2)
        
        mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask_red = cv2.bitwise_or(mask_red1, mask_red2)
        
        kernel = np.ones((3, 3), np.uint8)
        mask_red = cv2.morphologyEx(mask_red, cv2.MORPH_CLOSE, kernel)
        mask_red = cv2.morphologyEx(mask_red, cv2.MORPH_OPEN, kernel)
        
        lower_green = np.array(GREEN_LOWER)
        upper_green = np.array(GREEN_UPPER)
        mask_green = cv2.inRange(hsv, lower_green, upper_green)
        mask_green = cv2.morphologyEx(mask_green, cv2.MORPH_CLOSE, kernel)
        
        contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours_green, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        red_contour = None
        min_dist_to_center = float('inf')
        red_cx = red_cy = None
        
        for contour in contours_red:
            area = cv2.contourArea(contour)
            if area < 5:
                continue
            
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                dist = np.sqrt((cx - roi_center_x)**2 + (cy - roi_center_y)**2)
                
                if dist < 40 and dist < min_dist_to_center:
                    min_dist_to_center = dist
                    red_contour = contour
                    red_cx = cx
                    red_cy = cy
        
        return {
            'found': red_contour is not None,
            'red_contour': red_contour,
            'red_point': (x1 + red_cx, y1 + red_cy) if red_cx is not None else None,
            'green_contours': contours_green,
            'roi': roi,
            'roi_center': (roi_center_x, roi_center_y)
        }
    
    def find_red_square(self, img):
        """Находит красный квадрат"""
        h, w = img.shape[:2]
        center_x, center_y = self.minimap_center
        
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        lower_red1 = np.array(RED_LOWER_1)
        upper_red1 = np.array(RED_UPPER_1)
        lower_red2 = np.array(RED_LOWER_2)
        upper_red2 = np.array(RED_UPPER_2)
        
        mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask_red = cv2.bitwise_or(mask_red1, mask_red2)
        
        kernel = np.ones((3, 3), np.uint8)
        mask_red = cv2.morphologyEx(mask_red, cv2.MORPH_CLOSE, kernel)
        mask_red = cv2.morphologyEx(mask_red, cv2.MORPH_OPEN, kernel)
        
        exclude_radius = 50
        center_mask = np.ones((h, w), dtype=np.uint8) * 255
        cv2.circle(center_mask, (center_x, center_y), exclude_radius, 0, -1)
        mask_red = cv2.bitwise_and(mask_red, center_mask)
        
        contours, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        valid_contours = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < 15:
                continue
            
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                dist_to_center = np.sqrt((cx - center_x)**2 + (cy - center_y)**2)
                if dist_to_center < 40:
                    continue
            
            peri = cv2.arcLength(contour, True)
            if peri == 0:
                continue
            
            approx = cv2.approxPolyDP(contour, 0.04 * peri, True)
            if len(approx) >= 4:
                valid_contours.append(contour)
        
        return {
            'found': len(valid_contours) > 0,
            'contours': valid_contours,
            'mask': mask_red
        }
    
    def run(self):
        """Запускает отладочный просмотр"""
        print("Запуск отладочного просмотра...")
        print("Нажмите 'q' для выхода")
        print("Нажмите 's' для сохранения текущего кадра")
        
        frame_count = 0
        
        while True:
            minimap = self.capture_minimap()
            if minimap is None:
                time.sleep(0.1)
                continue
            
            # Создаем копию для отрисовки
            debug_img = minimap.copy()
            
            # Рисуем центр миникарты
            cv2.circle(debug_img, self.minimap_center, 5, (255, 255, 255), -1)
            cv2.circle(debug_img, self.minimap_center, 50, (255, 255, 255), 1)
            
            # Ищем стрелочку
            player = self.find_player_arrow(minimap)
            if player['found']:
                if player['red_point']:
                    cv2.circle(debug_img, player['red_point'], 5, (0, 0, 255), -1)
                    cv2.line(debug_img, self.minimap_center, player['red_point'], (0, 0, 255), 2)
                cv2.putText(debug_img, "PLAYER FOUND", (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            else:
                cv2.putText(debug_img, "PLAYER NOT FOUND", (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
            # Ищем красный квадрат
            target = self.find_red_square(minimap)
            if target['found']:
                for contour in target['contours']:
                    cv2.drawContours(debug_img, [contour], -1, (0, 255, 0), 2)
                    M = cv2.moments(contour)
                    if M["m00"] != 0:
                        cx = int(M["m10"] / M["m00"])
                        cy = int(M["m01"] / M["m00"])
                        cv2.circle(debug_img, (cx, cy), 5, (0, 255, 0), -1)
                        cv2.line(debug_img, self.minimap_center, (cx, cy), (0, 255, 0), 2)
                cv2.putText(debug_img, "TARGET FOUND", (10, 60), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            else:
                cv2.putText(debug_img, "TARGET NOT FOUND", (10, 60), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
            # Показываем изображение
            cv2.imshow('Debug Viewer - Minimap', debug_img)
            
            # Показываем маски
            if target['found']:
                cv2.imshow('Red Mask', target['mask'])
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                filename = f'debug_frame_{frame_count}.png'
                cv2.imwrite(filename, debug_img)
                print(f"Сохранено: {filename}")
                frame_count += 1
            
            time.sleep(0.05)
        
        cv2.destroyAllWindows()
        print("Отладочный просмотр завершен")

def main():
    print("=" * 60)
    print("Отладочный просмотр миникарты")
    print("=" * 60)
    print("\nЭта утилита показывает что видит бот:")
    print("- Белый круг: центр миникарты")
    print("- Красная точка: носик стрелки игрока")
    print("- Зеленые контуры: найденные красные квадраты")
    print("\nУправление:")
    print("- 'q': выход")
    print("- 's': сохранить текущий кадр")
    print("=" * 60)
    
    input("\nНажмите Enter для запуска...")
    
    viewer = DebugViewer()
    viewer.run()

if __name__ == "__main__":
    main()

