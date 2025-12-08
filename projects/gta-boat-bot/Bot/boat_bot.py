"""
Бот для автоматического плавания на лодке в GTA
Автоматически находит красные квадраты на миникарте и плывет к ним
"""

import cv2
import numpy as np
import mss
import time
from pynput.keyboard import Key, Controller, Listener
import math
import logging
import os
import threading

# Импорт системы подсчета чекпоинтов
try:
    from boat_bot_modules import CheckpointCounter
    CHECKPOINT_COUNTER_AVAILABLE = True
except ImportError:
    CHECKPOINT_COUNTER_AVAILABLE = False
    logger = logging.getLogger(__name__)
    if 'logger' in globals():
        logger.warning("CheckpointCounter не доступен. Используется старая система подсчета.")

# Импорт для глобальных хоткеев
try:
    import keyboard
    KEYBOARD_AVAILABLE = True
except ImportError:
    KEYBOARD_AVAILABLE = False

# Импорт для работы с окнами Windows
try:
    import win32gui
    import win32con
    import win32api
    import win32clipboard
    import win32ui
    from PIL import Image
    import ctypes
    from ctypes import wintypes
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False

# Настройка SendInput для надежной отправки клавиш
if WIN32_AVAILABLE:
    # Структуры для SendInput
    PUL = ctypes.POINTER(ctypes.c_ulong)
    
    class KeyBdInput(ctypes.Structure):
        _fields_ = [("wVk", ctypes.c_ushort),
                    ("wScan", ctypes.c_ushort),
                    ("dwFlags", ctypes.c_ulong),
                    ("time", ctypes.c_ulong),
                    ("dwExtraInfo", PUL)]
    
    class HardwareInput(ctypes.Structure):
        _fields_ = [("uMsg", ctypes.c_ulong),
                    ("wParamL", ctypes.c_short),
                    ("wParamH", ctypes.c_ushort)]
    
    class MouseInput(ctypes.Structure):
        _fields_ = [("dx", ctypes.c_long),
                    ("dy", ctypes.c_long),
                    ("mouseData", ctypes.c_ulong),
                    ("dwFlags", ctypes.c_ulong),
                    ("time", ctypes.c_ulong),
                    ("dwExtraInfo", PUL)]
    
    class Input_I(ctypes.Union):
        _fields_ = [("ki", KeyBdInput),
                    ("mi", MouseInput),
                    ("hi", HardwareInput)]
    
    class Input(ctypes.Structure):
        _fields_ = [("type", ctypes.c_ulong),
                    ("ii", Input_I)]
    
    # Константы
    KEYEVENTF_KEYUP = 0x0002
    INPUT_KEYBOARD = 1
    
    # Структуры для низкоуровневого хука клавиатуры
    class KBDLLHOOKSTRUCT(ctypes.Structure):
        _fields_ = [("vkCode", wintypes.DWORD),
                    ("scanCode", wintypes.DWORD),
                    ("flags", wintypes.DWORD),
                    ("time", wintypes.DWORD),
                    ("dwExtraInfo", ctypes.POINTER(wintypes.ULONG))]
    
    # Константы для хука клавиатуры
    WH_KEYBOARD_LL = 13
    WM_KEYDOWN = 0x0100
    WM_KEYUP = 0x0101
    WM_SYSKEYDOWN = 0x0104
    WM_SYSKEYUP = 0x0105
    HC_ACTION = 0
    
    # VK_INSERT = 0x2D
    VK_INSERT = 45
    
    # Тип для callback функции хука клавиатуры
    HOOKPROC = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_int, wintypes.WPARAM, wintypes.LPARAM)

# Попытка импортировать конфигурацию
try:
    from config import *
except ImportError:
    # Значения по умолчанию, если config.py не найден
    MINIMAP_REGION = {
        'left': 20,
        'top': 780,
        'width': 300,
        'height': 300
    }
    MINIMAP_CENTER = (150, 150)
    TURN_THRESHOLD = 5
    MIN_DISTANCE = 10
    # Красный чекпоинт #c30202: RGB(195, 2, 2) -> HSV(0, 252, 195)
    RED_LOWER_1 = [0, 200, 150]    # H=0-10, S=200-255, V=150-255
    RED_UPPER_1 = [10, 255, 255]
    RED_LOWER_2 = [170, 200, 150]  # H=170-180 (красный на границе), S=200-255, V=150-255
    RED_UPPER_2 = [180, 255, 255]
    GREEN_LOWER = [40, 200, 200]  # Для зеленой палочки игрока (ярко-зеленый #00f400, #00db00)
    # RGB(0, 244, 0) -> HSV: H=60, S=255, V=244
    # RGB(0, 219, 0) -> HSV: H=60, S=255, V=219
    # Используем высокий V (200-255) чтобы исключить темно-зеленый квадрат (V=154)
    GREEN_UPPER = [80, 255, 255]
    # Отдельные константы для зеленого квадрата (темно-зеленый #0b9a00)
    # RGB(11, 154, 0) -> HSV примерно: H=60 (зеленый в OpenCV), S=255, V=154
    # Используем более узкий диапазон H (50-70) и ограничиваем V (80-180) чтобы исключить ярко-зеленую палочку игрока
    GREEN_SQUARE_LOWER = [50, 200, 80]   # Темно-зеленый: H=50-70, S=200-255, V=80-180
    GREEN_SQUARE_UPPER = [70, 255, 180]
    BLACK_LOWER = [0, 0, 0]
    BLACK_UPPER = [180, 255, 50]
    # Оптимизированные HSV диапазоны для цветов квадратов
    # Желтый #fded00: RGB(253, 237, 0) -> HSV примерно H=55, S=255, V=253 -> OpenCV H=27.5, S=255, V=253
    YELLOW_LOWER = [25, 200, 200]  # H=25-30, S=200-255, V=200-255
    YELLOW_UPPER = [30, 255, 255]
    # Розовый #ff00fa: RGB(255, 0, 250) -> HSV примерно H=300, S=255, V=255 -> OpenCV H=150, S=255, V=255
    PINK_LOWER = [145, 200, 200]  # H=145-155, S=200-255, V=200-255
    PINK_UPPER = [155, 255, 255]
    # Белый #ffffff: RGB(255, 255, 255) -> HSV примерно H=0, S=0, V=255 -> OpenCV H=0, S=0, V=255
    WHITE_LOWER = [0, 0, 240]  # H=0-180, S=0-10, V=240-255
    WHITE_UPPER = [180, 10, 255]
    # Оранжевый #ff6800: RGB(255, 104, 0) -> HSV(12, 255, 255)
    # ВАЖНО: H=11-20 чтобы НЕ пересекаться с красным (H=0-10)
    # Расширенный диапазон для надежного обнаружения в разных условиях освещения
    ORANGE_LOWER = [11, 100, 100]   # H=11-20, S=100-255, V=100-255 (не пересекается с красным H=0-10)
    ORANGE_UPPER = [20, 255, 255]
    # Фиолетовый #6a05b8: RGB(106, 5, 184) -> HSV примерно H=270, S=255, V=184 -> OpenCV H=135, S=255, V=184
    PURPLE_LOWER = [130, 200, 150]  # H=130-140, S=200-255, V=150-200
    PURPLE_UPPER = [140, 255, 200]
    SCREEN_CAPTURE_DELAY = 0.000  # Оптимизировано для 90+ FPS (11мс на кадр, задержка 5мс для стабильности)
    ERROR_RETRY_DELAY = 0.1
    TARGET_NOT_FOUND_DELAY = 0.5
    MAX_CONSECUTIVE_ERRORS = 10
    MAX_ARROW_ERRORS = 30
    GAME_WINDOW_TITLE = "RADMIR CRMP"

# Проверяем наличие названия окна в конфигурации
if 'GAME_WINDOW_TITLE' not in globals():
    GAME_WINDOW_TITLE = "RADMIR CRMP"

# Попытка импортировать калибровку миникарты
try:
    from minimap_config import MINIMAP_REGION as CALIBRATED_REGION, MINIMAP_CENTER as CALIBRATED_CENTER
    MINIMAP_REGION = CALIBRATED_REGION
    MINIMAP_CENTER = CALIBRATED_CENTER
except ImportError:
    pass

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Импорт системы подсчета чекпоинтов
try:
    from boat_bot_modules import CheckpointCounter
    CHECKPOINT_COUNTER_AVAILABLE = True
except ImportError:
    CHECKPOINT_COUNTER_AVAILABLE = False
    logger.warning("CheckpointCounter не доступен. Используется старая система подсчета.")

# Предупреждение о keyboard после инициализации logger
if not KEYBOARD_AVAILABLE:
    logger.warning("keyboard не установлен. Глобальные хоткеи (Insert) не будут работать.")
    logger.warning("Установите: pip install keyboard")

class BoatBot:
    def __init__(self, window_title=None):
        self.keyboard = Controller()
        self.sct = mss.mss()
        self.window_title = window_title or GAME_WINDOW_TITLE
        self.window_handle = None
        self.window_rect = None
        self.window_activation_failed = False  # Флаг для отслеживания проблем с активацией
        self.keys_sent_count = 0  # Счетчик отправленных клавиш для отладки
        
        # Используем конфигурацию
        self.minimap_region = MINIMAP_REGION.copy()
        self.minimap_center = MINIMAP_CENTER
        self.turn_threshold = TURN_THRESHOLD
        try:
            self.turn_threshold_close = TURN_THRESHOLD_CLOSE
        except NameError:
            self.turn_threshold_close = 1.5  # Значение по умолчанию
        try:
            self.close_distance_threshold = CLOSE_DISTANCE_THRESHOLD
        except NameError:
            self.close_distance_threshold = 50  # Значение по умолчанию
        try:
            self.turn_hysteresis = TURN_HYSTERESIS
        except NameError:
            self.turn_hysteresis = 1  # Значение по умолчанию
        self.min_distance = MIN_DISTANCE
        self.current_turn_direction = None  # Текущее направление поворота для гистерезиса ('left', 'right', None)
        self.last_distances = []  # История расстояний для определения кружения (макс 10)
        
        # Параметры для обнаружения
        self.running = False
        self.paused = False  # Флаг паузы
        self.last_angle = 0
        self.last_valid_angle = None  # Последний валидный угол
        self.keys_pressed = {'w': False, 'a': False, 'd': False}
        self.last_log_time = 0
        self.consecutive_arrow_errors = 0  # Счетчик ошибок обнаружения стрелки
        self.last_target_angle = None  # Последний относительный угол к цели (для поворота)
        self.last_absolute_target_angle = None  # Абсолютный угол направления к центру квадрата
        self.last_key_update_time = 0  # Время последнего обновления клавиш
        self.last_continue_log_time = 0  # Время последнего логирования продолжения движения
        self.target_cache = []  # Кэш последних найденных квадратов для стабильности (макс 3)
        self.last_target_cache_time = 0  # Время последнего обновления кэша

        # Система состояний и счетчики
        # Новая последовательность рейса:
        # 1) Желтый -> 2) Розовый -> 3) Зеленый -> 4) Белый -> 5) Розовый ->
        # 6) 7 красных квадратов -> 7) Зеленый -> 8) Красный чекпоинт -> 9) Желтый ->
        # 10) Красные #9 и #10 -> 11) Зеленый -> 12) Оранжевый -> 13) Белый ->
        # 14) Красные до появления оранжевого -> 15) Оранжевый -> 16) Розовый -> 17) Желтый -> 18) Красный, затем цикл повторяется.
        self.state = 'Y1'  # Старт: первый желтый квадрат
        
        # НОВАЯ СИСТЕМА ПОДСЧЕТА (КОСТЫЛЬ для бага):
        # Из-за бага один физический чекпоинт засчитывается 3 раза (вызывает add_checkpoint() 3 раза)
        # Внутренний счетчик: считает каждый вызов add_checkpoint() как +1 (1, 2, 3, 4, 5, 6...)
        # Внешний счетчик: считает тройки (каждые 3 внутренних = 1 внешний) → компенсирует баг
        # Внешний: 0, 0, 0, 1, 1, 1, 2, 2, 2... (каждые 3 вызова = 1 физический чекпоинт)
        # Маршрут зависит от внешнего счетчика!
        if CHECKPOINT_COUNTER_AVAILABLE:
            self.checkpoint_counter = CheckpointCounter()
            logger.info("Инициализирована система подсчета чекпоинтов (костыль для бага: каждые 3 вызова = 1 физический чекпоинт)")
        else:
            self.checkpoint_counter = None
            logger.warning("Используется старая система подсчета (checkpoint_counter недоступен)")
        
        # Старая система (для обратной совместимости и логирования старого формата)
        self.red_squares_collected = 0  # Счетчик собранных красных квадратов (для логирования старого формата)
        self._last_checkpoint_collected_time = 0  # Время последнего засчитывания чекпоинта (для задержки 1.5 секунды)
        self._checkpoint_counted_at_reach = False  # Флаг того, что текущий чекпоинт был засчитан при достижении (чтобы не засчитывать при исчезновении)
        
        self.last_circle_center = None  # Последний центр достигнутого круга
        self.last_circle_distance = None  # Последнее расстояние до круга
        self.circle_reached_threshold = 8  # Порог расстояния для определения достижения круга (уменьшен чтобы бот переезжал круги)
        self.last_collected_square_center = None  # Центр последнего собранного квадрата (для предотвращения повторного подсчета)
        self.min_distance_to_target = None  # Минимальное расстояние до текущей цели (для определения достижения при потере цели)
        self.distance_history = []  # История расстояний для определения проезда через цель
        self.target_reached_flag = False  # Флаг что цель была достигнута (чтобы не переключать состояние несколько раз)
        # Для отслеживания пропадания красных чекпоинтов
        self.last_red_checkpoint_center = None  # Центр последнего видимого красного чекпоинта
        self.last_red_checkpoint_distance = None  # Последнее расстояние до красного чекпоинта
        self.red_checkpoint_min_distance = None  # Минимальное расстояние до красного чекпоинта
        self._green_after_7_transition_time = 0  # Время перехода в GREEN_AFTER_7 для защиты от близких красных чекпоинтов
        self._green_square_reached_time = 0  # Время достижения зеленого квадрата после 7-го чекпоинта (для автоматического +1 к счету)
        self._last_tap_time = {}  # Время последнего точечного нажатия для каждой клавиши (A/D)
        self._is_aligned = False  # Флаг: выровнен ли бот на цель (угол < 2 градусов)
        
        # Для глобального хука клавиатуры (используем библиотеку keyboard)
        self.pause_lock = threading.Lock()
        
        # Для низкоуровневого хука Windows (более надежный способ)
        self.insert_pressed = False
        self.insert_press_time = 0
        self.keyboard_hook = 0
        self._hook_proc = None
        
        # Настройки отладки
        try:
            self.save_debug_screenshots = SAVE_DEBUG_SCREENSHOTS
            self.debug_screenshot_dir = DEBUG_SCREENSHOT_DIR
        except NameError:
            self.save_debug_screenshots = True  # Включаем по умолчанию для визуализации
            self.debug_screenshot_dir = "debug_screenshots"
        
        # Создаем папку для отладочных скриншотов
        if self.save_debug_screenshots:
            os.makedirs(self.debug_screenshot_dir, exist_ok=True)
        
        
        # Находим окно игры
        if WIN32_AVAILABLE:
            if not self.find_game_window():
                logger.warning("Окно игры не найдено. Используется захват всего экрана.")
        else:
            logger.warning("win32gui не установлен. Установите pywin32 для захвата только окна игры.")
            logger.warning("Используется захват всего экрана.")
    
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
            logger.info(f"Найдено окно игры: {windows[0][1]}")
            
            # НЕ разворачиваем и не активируем окно автоматически
            # Пользователь может свернуть игру, и бот не должен мешать
            # Просто проверяем, что окно существует и получаем его координаты
            
            # Получаем координаты окна
            self.window_rect = win32gui.GetWindowRect(self.window_handle)
            window_left, window_top, window_right, window_bottom = self.window_rect
            
            # Проверяем валидность координат
            if window_left < -10000 or window_top < -10000:
                logger.error("Окно игры минимизировано или скрыто. Пожалуйста, восстановите окно вручную.")
                return False
            
            logger.info(f"Координаты окна: {self.window_rect}")
            logger.info(f"Размер окна: {window_right - window_left} x {window_bottom - window_top}")
            
            # Сохраняем смещение окна для дальнейшего использования
            self.window_offset_x = window_left
            self.window_offset_y = window_top
            
            return True
        else:
            logger.error(f"Окно игры '{self.window_title}' не найдено!")
            logger.info("Попытка использовать координаты относительно всего экрана...")
            return False
        
    def capture_minimap(self):
        """Захватывает скриншот области миникарты из окна игры"""
        try:
            # Если окно игры найдено, обновляем координаты
            if WIN32_AVAILABLE and self.window_handle:
                # Проверяем, что окно все еще существует
                if not win32gui.IsWindow(self.window_handle):
                    logger.warning("Окно игры закрыто. Попытка переподключения...")
                    if not self.find_game_window():
                        return None
                
                # Обновляем координаты окна (на случай если оно переместилось)
                self.window_rect = win32gui.GetWindowRect(self.window_handle)
                window_left, window_top, window_right, window_bottom = self.window_rect
                
                # Проверяем, свернуто ли окно
                is_minimized = (window_left < -10000 or window_top < -10000)
                
                if is_minimized:
                    # Окно свернуто - используем PrintWindow API для захвата
                    try:
                        return self._capture_minimap_printwindow()
                    except Exception as e:
                        logger.warning(f"Не удалось захватить через PrintWindow: {e}. Попытка через mss...")
                        # Fallback: пытаемся через mss (может не работать для свернутого окна)
                        return None
                
                # Окно не свернуто - используем обычный метод через mss
                # Корректируем координаты миникарты с учетом текущей позиции окна
                # Используем относительные координаты из конфигурации (относительно окна игры)
                base_region = MINIMAP_REGION.copy()
                capture_region = {
                    'left': window_left + base_region.get('left', 20),
                    'top': window_top + base_region.get('top', 780),
                    'width': base_region.get('width', 300),
                    'height': base_region.get('height', 300)
                }
                
                screenshot = self.sct.grab(capture_region)
                img = np.array(screenshot)
                # Конвертируем BGRA в BGR для OpenCV
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
                return img
            else:
                # Используем координаты относительно всего экрана
                capture_region = self.minimap_region
                screenshot = self.sct.grab(capture_region)
                img = np.array(screenshot)
                # Конвертируем BGRA в BGR для OpenCV
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
                return img
        except Exception as e:
            logger.error(f"Ошибка захвата скриншота: {e}")
            return None
    
    def _capture_minimap_printwindow(self):
        """Захватывает миникарту через PrintWindow API (работает даже когда окно свернуто)"""
        if not WIN32_AVAILABLE or not self.window_handle:
            return None
        
        try:
            # Получаем размеры клиентской области окна
            left, top, right, bottom = win32gui.GetClientRect(self.window_handle)
            width = right - left
            height = bottom - top
            
            if width <= 0 or height <= 0:
                logger.warning("Некорректный размер окна для PrintWindow")
                return None
            
            # Создаем Device Context для окна
            hwndDC = win32gui.GetWindowDC(self.window_handle)
            mfcDC = win32ui.CreateDCFromHandle(hwndDC)
            saveDC = mfcDC.CreateCompatibleDC()
            
            # Создаем битмап для сохранения изображения
            saveBitMap = win32ui.CreateBitmap()
            saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
            saveDC.SelectObject(saveBitMap)
            
            # Копируем содержимое окна в битмап через PrintWindow
            # PW_CLIENTONLY = 0x00000001 - захватываем только клиентскую область
            result = win32gui.PrintWindow(self.window_handle, saveDC.GetSafeHdc(), 0x00000001)
            
            if not result:
                logger.warning("PrintWindow вернул False - возможно окно не поддерживает захват в свернутом режиме")
                # Освобождаем ресурсы
                win32gui.DeleteObject(saveBitMap.GetHandle())
                saveDC.DeleteDC()
                mfcDC.DeleteDC()
                win32gui.ReleaseDC(self.window_handle, hwndDC)
                return None
            
            # Получаем данные битмапа
            bmpinfo = saveBitMap.GetInfo()
            bmpstr = saveBitMap.GetBitmapBits(True)
            
            # Конвертируем в PIL Image
            img = Image.frombuffer(
                'RGB',
                (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
                bmpstr, 'raw', 'BGRX', 0, 1
            )
            
            # Освобождаем ресурсы
            win32gui.DeleteObject(saveBitMap.GetHandle())
            saveDC.DeleteDC()
            mfcDC.DeleteDC()
            win32gui.ReleaseDC(self.window_handle, hwndDC)
            
            # Обрезаем область миникарты
            base_region = MINIMAP_REGION.copy()
            minimap_left = base_region.get('left', 20)
            minimap_top = base_region.get('top', 780)
            minimap_width = base_region.get('width', 300)
            minimap_height = base_region.get('height', 300)
            
            # Обрезаем изображение до области миникарты
            img_cropped = img.crop((
                minimap_left,
                minimap_top,
                minimap_left + minimap_width,
                minimap_top + minimap_height
            ))
            
            # Конвертируем PIL Image в numpy array для OpenCV
            img_array = np.array(img_cropped)
            # Конвертируем RGB в BGR для OpenCV
            img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            
            return img_bgr
            
        except Exception as e:
            logger.error(f"Ошибка захвата через PrintWindow: {e}")
            return None
    
    def find_player_arrow(self, img):
        """
        Находит стрелочку игрока в центре миникарты
        Красная точка теперь сзади, зеленая палочка показывает направление вперед
        Используем зеленую палочку как основной индикатор направления
        """
        h, w = img.shape[:2]
        center_x, center_y = self.minimap_center
        
        # Область поиска вокруг центра (увеличена для большей надежности)
        search_radius = 80
        x1 = max(0, center_x - search_radius)
        y1 = max(0, center_y - search_radius)
        x2 = min(w, center_x + search_radius)
        y2 = min(h, center_y + search_radius)
        
        roi = img[y1:y2, x1:x2]
        roi_center_x = search_radius
        roi_center_y = search_radius
        
        # Конвертируем в HSV для лучшего обнаружения цветов
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        
        # Ищем красный цвет (точка сзади) - используем конфигурацию
        # Расширяем диапазон для более надежного обнаружения
        lower_red1 = np.array([max(0, RED_LOWER_1[0] - 5), max(0, RED_LOWER_1[1] - 30), max(0, RED_LOWER_1[2] - 30)])
        upper_red1 = np.array([min(180, RED_UPPER_1[0] + 5), 255, 255])
        lower_red2 = np.array([max(0, RED_LOWER_2[0] - 5), max(0, RED_LOWER_2[1] - 30), max(0, RED_LOWER_2[2] - 30)])
        upper_red2 = np.array([180, 255, 255])
        
        mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask_red = cv2.bitwise_or(mask_red1, mask_red2)
        
        # Морфологические операции для очистки
        kernel = np.ones((3, 3), np.uint8)
        mask_red = cv2.morphologyEx(mask_red, cv2.MORPH_CLOSE, kernel)
        mask_red = cv2.morphologyEx(mask_red, cv2.MORPH_OPEN, kernel)
        
        # Дополнительная очистка - удаляем шум
        kernel = np.ones((2, 2), np.uint8)
        mask_red = cv2.morphologyEx(mask_red, cv2.MORPH_OPEN, kernel)
        
        # Ищем зеленый цвет (палочка направления вперед) - используем конфигурацию
        lower_green = np.array(GREEN_LOWER)
        upper_green = np.array(GREEN_UPPER)
        mask_green = cv2.inRange(hsv, lower_green, upper_green)
        mask_green = cv2.morphologyEx(mask_green, cv2.MORPH_CLOSE, kernel)
        
        # Находим контуры
        contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours_green, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Ищем зеленую палочку (основной индикатор направления)
        green_contour = None
        green_cx = None
        green_cy = None
        
        if len(contours_green) > 0:
            # Берем самую большую зеленую область (палочка)
            green_contour = max(contours_green, key=cv2.contourArea)
            
            # ВАЖНО: Находим самую дальнюю точку зеленой палочки от центра миникарты
            # Это будет зад персонажа, направление движения - противоположное
            contour_points = green_contour.reshape(-1, 2)
            max_dist = 0
            farthest_point = None
            
            for point in contour_points:
                px, py = point[0], point[1]
                # Расстояние от центра области поиска (центр миникарты)
                dist = math.sqrt((px - roi_center_x)**2 + (py - roi_center_y)**2)
                if dist > max_dist:
                    max_dist = dist
                    farthest_point = (px, py)
            
            if farthest_point:
                # Самая дальняя точка - это зад персонажа
                green_cx, green_cy = farthest_point
            else:
                # Если не нашли, используем центр масс как запасной вариант
                green_moment = cv2.moments(green_contour)
                if green_moment["m00"] != 0:
                    green_cx = int(green_moment["m10"] / green_moment["m00"])
                    green_cy = int(green_moment["m01"] / green_moment["m00"])
                else:
                    green_cx = None
                    green_cy = None
        else:
            green_cx = None
            green_cy = None
        
        # Ищем красную точку (сзади)
        red_contour = None
        red_cx = None
        red_cy = None
        
        for contour in contours_red:
            area = cv2.contourArea(contour)
            if area < 3:
                continue
            
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                
                # Расстояние от центра области поиска
                dist = math.sqrt((cx - roi_center_x)**2 + (cy - roi_center_y)**2)
                
                # Ищем красный контур, который находится на разумном расстоянии от центра
                if dist < 50:
                    red_contour = contour
                    red_cx = cx
                    red_cy = cy
                    break  # Берем первый найденный
        
        # Если нашли зеленую палочку, используем её для определения направления
        line_angle = None  # Инициализируем переменную
        if green_cx is not None and green_cy is not None and green_contour is not None:
            # ВАЖНО: Находим ориентацию самой зеленой палочки для точного направления
            # Используем fitLine для определения главной оси палочки
            contour_points = green_contour.reshape(-1, 2).astype(np.float32)
            
            if len(contour_points) >= 2:
                # Используем fitLine для определения направления палочки
                line_params = cv2.fitLine(contour_points, cv2.DIST_L2, 0, 0.01, 0.01)
                # fitLine возвращает массив формы (4, 1), извлекаем элементы корректно
                vx = float(line_params[0, 0])
                vy = float(line_params[1, 0])
                x0 = float(line_params[2, 0])
                y0 = float(line_params[3, 0])
                
                # Вычисляем угол главной оси палочки
                # vx, vy - вектор направления
                line_angle = math.atan2(vy, vx) * 180 / math.pi
                
                # Переводим в систему координат: 0° = вверх, по часовой
                line_angle = (line_angle + 90) % 360
                
                # Находим самую дальнюю и самую ближнюю точки для определения, какой конец - зад
                min_dist = float('inf')
                max_dist = 0
                nearest_point = None
                farthest_point = None
                
                for point in contour_points:
                    px, py = int(point[0]), int(point[1])
                    dist = math.sqrt((px - roi_center_x)**2 + (py - roi_center_y)**2)
                    if dist < min_dist:
                        min_dist = dist
                        nearest_point = (px, py)
                    if dist > max_dist:
                        max_dist = dist
                        farthest_point = (px, py)
                
                # Проверяем, какой конец палочки - зад (дальняя точка)
                # Вычисляем угол от центра к дальней точке
                if farthest_point:
                    dx_rear = farthest_point[0] - roi_center_x
                    dy_rear = farthest_point[1] - roi_center_y
                    angle_to_rear = math.atan2(dy_rear, dx_rear) * 180 / math.pi
                    angle_to_rear = (angle_to_rear + 90) % 360
                    
                    # Определяем, в какую сторону направлена палочка от центра масс
                    # Находим центр масс для проверки
                    green_moment = cv2.moments(green_contour)
                    if green_moment["m00"] != 0:
                        center_mass_x = int(green_moment["m10"] / green_moment["m00"])
                        center_mass_y = int(green_moment["m01"] / green_moment["m00"])
                        
                        # Проверяем, в какую сторону от центра масс находится дальняя точка
                        # Если дальняя точка дальше от центра масс в направлении палочки, это зад
                        # Вычисляем направление от центра масс к дальней точке
                        dx_center_to_far = farthest_point[0] - center_mass_x
                        dy_center_to_far = farthest_point[1] - center_mass_y
                        
                        # Вычисляем направление палочки от центра масс
                        line_angle_rad = math.radians(line_angle)
                        dx_line = math.sin(line_angle_rad)
                        dy_line = -math.cos(line_angle_rad)  # Минус, т.к. система координат
                        
                        # Скалярное произведение: если > 0, направления совпадают
                        dot_product = dx_center_to_far * dx_line + dy_center_to_far * dy_line
                        
                        if dot_product > 0:
                            # Палочка указывает на зад (дальнюю точку), инвертируем
                            angle = (line_angle + 180) % 360
                        else:
                            # Палочка указывает вперед
                            angle = line_angle
                    else:
                        # Запасной вариант: сравниваем углы
                        angle_diff = abs(line_angle - angle_to_rear)
                        if angle_diff > 180:
                            angle_diff = 360 - angle_diff
                        if angle_diff < 45 or angle_diff > 135:
                            angle = (line_angle + 180) % 360
                        else:
                            angle = line_angle
                else:
                    # Запасной вариант: инвертируем
                    angle = (line_angle + 180) % 360
            else:
                # Запасной вариант: используем угол к дальней точке
                dx = green_cx - roi_center_x
                dy = green_cy - roi_center_y
                angle_to_rear = math.atan2(dy, dx) * 180 / math.pi
                angle_to_rear = (angle_to_rear + 90) % 360
                angle = (angle_to_rear + 180) % 360
            
            # Абсолютные координаты в исходном изображении
            # green_cx, green_cy - это самая дальняя точка (зад персонажа)
            green_rear_x = x1 + green_cx
            green_rear_y = y1 + green_cy
            
            # Находим центр масс зеленой палочки для визуализации (центр игрока)
            green_center_x = None
            green_center_y = None
            green_stick_angle = None  # Угол ориентации самой палочки (для визуализации)
            
            green_moment = cv2.moments(green_contour)
            if green_moment["m00"] != 0:
                green_center_x = int(green_moment["m10"] / green_moment["m00"])
                green_center_y = int(green_moment["m01"] / green_moment["m00"])
            
            # Сохраняем угол ориентации палочки (line_angle) для визуализации
            # Это угол самой палочки, определенный через fitLine
            if line_angle is not None:
                green_stick_angle = line_angle  # Используем уже вычисленный line_angle
            
            red_abs_x = None
            red_abs_y = None
            if red_cx is not None and red_cy is not None:
                red_abs_x = x1 + red_cx
                red_abs_y = y1 + red_cy
            
            return {
                'found': True,
                'angle': angle,  # Угол направления движения (инвертированный)
                'stick_angle': green_stick_angle,  # Угол ориентации палочки (для визуализации)
                'red_point': (red_abs_x, red_abs_y) if red_abs_x is not None else None,
                'green_point': (green_rear_x, green_rear_y),  # Зад персонажа (дальняя точка)
                'green_center': (x1 + green_center_x, y1 + green_center_y) if green_center_x is not None else None,  # Центр зеленой палочки
                'center': (x1 + roi_center_x, y1 + roi_center_y)
            }
        
        # Если зеленой палочки нет, но есть красная точка, используем её как запасной вариант
        # (но это не должно происходить в нормальных условиях)
        if red_cx is not None and red_cy is not None:
            # Вычисляем угол от центра к красной точке (но это направление назад)
            dx = red_cx - roi_center_x
            dy = red_cy - roi_center_y
            
            angle = math.atan2(dy, dx) * 180 / math.pi
            angle = (angle + 90) % 360
            # Инвертируем направление (красная точка сзади, направление - противоположное)
            angle = (angle + 180) % 360
            
            red_abs_x = x1 + red_cx
            red_abs_y = y1 + red_cy
            
            return {
                'found': True,
                'angle': angle,
                'red_point': (red_abs_x, red_abs_y),
                'green_point': None,
                'center': (x1 + roi_center_x, y1 + roi_center_y)
            }
        
        return {'found': False}
    
    def _check_red_color(self, mean_h, mean_s, mean_v):
        """
        Проверяет, соответствует ли цвет ярко-красному квадрату
        Возвращает (is_valid, color_score)
        ВАЖНО: Исключаем оранжевый цвет (H=8-15) из красного
        """
        # ВАЖНО: Исключаем оранжевый цвет (H=8-15) из красного
        # Красный должен быть H=0-7 или H=170-180
        # Оранжевый имеет H=8-15, поэтому исключаем этот диапазон
        if mean_h >= 8 and mean_h <= 15:
            # Это оранжевый цвет, не красный
            return False, 0.0
        
        # Проверяем диапазон красного оттенка (исключая оранжевый)
        if not (mean_h <= 7 or mean_h >= 170):
            return False, 0.0
        
        # Проверяем насыщенность и яркость
        if mean_s < 170 or mean_v < 170:
            return False, 0.0
        
        # Вычисляем оценку качества цвета
        h_diff = min(abs(mean_h - 0), abs(mean_h - 180), abs(mean_h - 360))
        h_score = 1.0 - (h_diff / 7.0)  # Уменьшили делитель, так как диапазон стал уже
        h_score = max(0.0, min(1.0, h_score))
        
        s_score = (mean_s - 170) / 85.0
        s_score = max(0.0, min(1.0, s_score))
        
        v_score = (mean_v - 170) / 85.0
        v_score = max(0.0, min(1.0, v_score))
        
        color_score = (h_score * 0.25 + s_score * 0.375 + v_score * 0.375)
        return True, color_score
    
    def find_red_square(self, img, hsv=None):
        """
        Находит красный квадрат с черной оконтовкой на миникарте
        Игнорирует красный носик стрелки игрока и другие красные объекты
        ТРЕБУЕТ: ярко-красный цвет + ОБЯЗАТЕЛЬНАЯ черная обводка + квадратная форма
        Args:
            img: Изображение миникарты (BGR)
            hsv: Опционально предконвертированное HSV изображение (для оптимизации)
        """
        h, w = img.shape[:2]
        center_x, center_y = self.minimap_center
        
        # Конвертируем в HSV только если не передан
        if hsv is None:
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        # Строгие параметры для ярко-красного цвета (как на скриншоте)
        # Только яркий, насыщенный красный цвет - не темнее, не светлее
        # ВАЖНО: Исключаем оранжевый цвет (H=8-15) из красного
        # Используем умеренные пороги для начальной маски, затем строгая проверка в _check_red_color
        lower_red1 = np.array([0, 150, 150])  # Ярко-красный с высокой насыщенностью и яркостью
        upper_red1 = np.array([7, 255, 255])   # Исключаем H=8-15 (оранжевый)
        lower_red2 = np.array([170, 150, 150])  # Ярко-красный с высокой насыщенностью и яркостью
        upper_red2 = np.array([180, 255, 255])
        
        mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask_red = cv2.bitwise_or(mask_red1, mask_red2)
        
        # Морфологические операции для очистки
        kernel = np.ones((3, 3), np.uint8)
        mask_red = cv2.morphologyEx(mask_red, cv2.MORPH_CLOSE, kernel)
        mask_red = cv2.morphologyEx(mask_red, cv2.MORPH_OPEN, kernel)
        
        # НОВАЯ ЛОГИКА: Вместо полного исключения области вокруг центра,
        # ищем красный цвет везде, но потом фильтруем контуры по размеру и форме.
        # Это позволяет находить квадраты даже когда они частично перекрыты иконкой игрока.
        # НЕ исключаем область вокруг центра полностью - ищем красный цвет везде
        
        # Находим контуры
        contours, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Список кандидатов с оценкой качества
        candidates = []
        
        # Логируем количество найденных красных контуров для отладки
        if len(contours) == 0:
            logger.debug("Не найдено красных контуров на миникарте")
        else:
            logger.debug(f"Найдено {len(contours)} красных контуров на миникарте для анализа")
        
        if len(contours) > 0:
            # Анализируем каждый контур
            for contour in contours:
                area = cv2.contourArea(contour)
                
                # Фильтр по размеру: слишком маленькие или большие объекты не подходят
                if area < 30 or area > 500:  # Разумные границы для квадрата на миникарте
                    continue
                
                # Вычисляем центр квадрата более точно
                # Используем центр bounding rect для более точного позиционирования
                x, y, w_rect, h_rect = cv2.boundingRect(contour)
                cx = int(x + w_rect / 2)
                cy = int(y + h_rect / 2)
                
                # Дополнительно проверяем через моменты для валидации
                M = cv2.moments(contour)
                if M["m00"] == 0:
                    continue
                
                # Используем среднее между центром bounding rect и центром масс для более точного позиционирования
                cx_moments = int(M["m10"] / M["m00"])
                cy_moments = int(M["m01"] / M["m00"])
                
                # Используем среднее значение для более точного центра
                cx = int((cx + cx_moments) / 2)
                cy = int((cy + cy_moments) / 2)
                
                # Проверяем расстояние до центра
                dist_to_center = math.sqrt((cx - center_x)**2 + (cy - center_y)**2)
                
                # ВАЖНО: Если контур очень близко к центру (< 20px), это скорее всего часть игрока
                # Но если он достаточно большой (area > 80) и имеет форму квадрата,
                # это может быть квадрат, частично перекрытый игроком - оставляем его для проверки
                if dist_to_center < 20:
                    # Очень близко к центру - проверяем размер
                    # Если площадь маленькая (< 80), это скорее всего часть игрока (красная метка), игнорируем
                    if area < 80:
                        logger.debug(f"Кандидат отфильтрован: слишком близко к центру и маленький (dist={dist_to_center:.1f}px, area={area:.1f})")
                        continue
                    # Если площадь достаточно большая, возможно это квадрат под игроком
                    # Продолжаем проверку формы и цвета - не исключаем
                # Если расстояние больше 20px, проверяем как обычно - не исключаем
                
                # Аппроксимируем контур для проверки формы
                peri = cv2.arcLength(contour, True)
                if peri == 0:
                    continue
                    
                approx = cv2.approxPolyDP(contour, 0.04 * peri, True)
                
                # Проверяем, что это многоугольник с 4 углами (квадрат)
                if len(approx) < 4:
                    continue
                
                # Получаем bounding rect для проверки формы
                x, y, w_rect, h_rect = cv2.boundingRect(contour)
                if w_rect == 0 or h_rect == 0:
                    continue
                
                # Проверяем соотношение сторон (должно быть близко к 1:1 для квадрата)
                aspect_ratio = float(w_rect) / h_rect
                if aspect_ratio < 0.7 or aspect_ratio > 1.3:  # Строже проверка
                    continue
                
                # Проверяем компактность (отношение площади к площади bounding rect)
                # Для квадрата это должно быть близко к 1.0
                rect_area = w_rect * h_rect
                if rect_area == 0:
                    continue
                extent = float(area) / rect_area
                if extent < 0.7:  # Строгая проверка - квадрат должен быть заполненным
                    continue
                
                # ВАЖНО: Проверяем точный оттенок красного цвета внутри квадрата
                # Инициализируем переменные
                mean_h = 0
                mean_s = 0
                mean_v = 0
                color_match_score = 0.0
                
                # Вырезаем только область самого красного квадрата (без обводки)
                square_roi = img[y:y+h_rect, x:x+w_rect]
                square_hsv_roi = hsv[y:y+h_rect, x:x+w_rect]
                
                # Создаем маску только для пикселей внутри контура (точный квадрат)
                square_mask = np.zeros((h_rect, w_rect), dtype=np.uint8)
                contour_in_roi = contour - [x, y]  # Переводим координаты в локальную систему
                cv2.drawContours(square_mask, [contour_in_roi], -1, 255, -1)
                
                # Находим средний цвет только внутри квадрата
                if np.sum(square_mask) > 0:
                    # Маска для пикселей квадрата в HSV
                    masked_hsv = square_hsv_roi[square_mask > 0]
                    
                    if len(masked_hsv) > 0:
                        # Вычисляем средние значения H, S, V
                        mean_h = np.mean(masked_hsv[:, 0])
                        mean_s = np.mean(masked_hsv[:, 1])
                        mean_v = np.mean(masked_hsv[:, 2])
                        
                        # ЕДИНАЯ проверка цвета через метод
                        is_valid_color, color_match_score = self._check_red_color(mean_h, mean_s, mean_v)
                        if not is_valid_color:
                            continue  # Пропускаем, если цвет не подходит
                else:
                    continue  # Не удалось извлечь цвет - пропускаем
                
                # ВАЖНО: Проверяем наличие черной обводки
                # Увеличиваем область поиска обводки
                border = 5
                x_start = max(0, x - border)
                y_start = max(0, y - border)
                x_end = min(img.shape[1], x + w_rect + border)
                y_end = min(img.shape[0], y + h_rect + border)
                
                roi = img[y_start:y_end, x_start:x_end]
                if roi.size == 0:
                    continue
                
                # Создаем маску для области вокруг квадрата
                roi_h, roi_w = roi.shape[:2]
                if roi_h == 0 or roi_w == 0:
                    continue
                
                # Ищем черные пиксели вокруг красного квадрата
                gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                
                # Создаем маску: ищем черные пиксели (значение < 50)
                black_mask = gray_roi < 50
                
                # Создаем маску красного квадрата в ROI
                red_in_roi = mask_red[y_start:y_end, x_start:x_end]
                
                # Ищем черные пиксели вокруг красного (не внутри него)
                # Расширяем маску красного квадрата немного
                red_dilated = cv2.dilate(red_in_roi, np.ones((3, 3), np.uint8), iterations=2)
                # Исключаем сам красный квадрат из поиска черного
                black_around = black_mask & (~red_dilated.astype(bool))
                
                # Считаем черные пиксели вокруг
                black_count = np.sum(black_around)
                
                # Проверяем периметр - вдоль границы должно быть достаточно черных пикселей
                # Вычисляем периметр квадрата в пикселях (примерно)
                perimeter_pixels = 2 * (w_rect + h_rect) + 4  # Примерная длина периметра
                
                # Оценка качества: сколько черных пикселей на единицу периметра
                black_density = float(black_count) / perimeter_pixels if perimeter_pixels > 0 else 0
                
                # ТРЕБОВАНИЕ: должна быть четкая черная обводка
                # Минимум 0.3 черных пикселей на пиксель периметра
                if black_density < 0.3:  # Строгая проверка
                    continue
                
                # Вычисляем общую оценку качества квадрата
                # Комбинируем несколько факторов:
                # 1. Соотношение сторон (ближе к 1.0 = лучше)
                aspect_score = 1.0 - abs(1.0 - aspect_ratio)
                
                # 2. Заполненность (ближе к 1.0 = лучше)
                extent_score = extent
                
                # 3. Плотность черной обводки
                border_score = min(1.0, black_density / 1.0)  # Нормализуем
                
                # 4. Соответствие палитре красного цвета (ВАЖНО для выбора нужного квадрата)
                # color_match_score уже вычислен выше при проверке цвета
                
                # Общая оценка (цвету придаем ОЧЕНЬ БОЛЬШОЙ вес - 55%, чтобы выбирать только правильный оттенок)
                quality_score = aspect_score * 0.15 + extent_score * 0.10 + border_score * 0.20 + color_match_score * 0.55
                
                candidates.append({
                    'contour': contour,
                    'center': (cx, cy),
                    'area': area,
                    'quality': quality_score,
                    'color_score': color_match_score,
                    'mean_h': mean_h,
                    'mean_s': mean_s,
                    'mean_v': mean_v,
                    'black_density': black_density,
                    'aspect_ratio': aspect_ratio,
                    'extent': extent
                })
        
        # Если есть кандидаты, выбираем лучший
        # Все кандидаты уже прошли проверку цвета выше, просто сортируем по качеству
        if len(candidates) > 0:
            # Сортируем по качеству (лучший первый) - учитывается и цвет, и форма, и обводка
            candidates.sort(key=lambda x: x['quality'], reverse=True)
            best = candidates[0]
            
            # Проверяем черную обводку (цвет уже проверен выше)
            if best['black_density'] >= 0.3:
                # ВАЖНО: Смещаем центр на 4 пикселя вправо для более точного прохождения через центр
                center_x, center_y = best['center']
                adjusted_center = (center_x + 1, center_y)  # Смещение вправо на 4 пикселя
                
                return {
                    'found': True,
                    'center': adjusted_center,
                    'contour': best['contour'],
                    'area': best['area']
                }
            else:
                logger.info(f"[RED] Квадрат отфильтрован: недостаточная черная обводка (density={best['black_density']:.2f}, требуется >= 0.3)")
        
        logger.debug("[RED] Красный квадрат не найден: все контуры отфильтрованы")
        return {'found': False}
    
    def check_circle_surrounding(self, img, hsv, cx, cy, radius, strict=True):
        """
        Проверяет окружение кружка - должно быть вода (синий цвет)
        Если вокруг кружка есть суша (черный) или другие цвета, возвращает False
        Args:
            img: Изображение миникарты (BGR)
            hsv: Изображение миникарты в HSV
            cx, cy: Центр кружка
            radius: Радиус кружка
            strict: Если True - строгая проверка, если False - более мягкая (для целей близко к игроку)
        Returns:
            True если вокруг кружка вода, False если есть суша или другие цвета
        """
        h, w = img.shape[:2]
        
        # Определяем область вокруг кружка (кольцо вокруг него)
        # Расширяем радиус на 5-10 пикселей для проверки окружения
        check_radius = int(radius) + 8
        check_radius = min(check_radius, min(w, h) // 2 - 5)  # Не выходим за границы
        
        # Создаем маску для области вокруг кружка (кольцо)
        mask_ring = np.zeros((h, w), dtype=np.uint8)
        cv2.circle(mask_ring, (cx, cy), check_radius, 255, 2)  # Толщина 2 пикселя для кольца
        cv2.circle(mask_ring, (cx, cy), int(radius) + 2, 0, -1)  # Исключаем сам кружок
        
        # Проверяем пиксели в кольце
        ring_pixels = hsv[mask_ring > 0]
        
        if len(ring_pixels) == 0:
            return False  # Нет пикселей для проверки
        
        # Проверяем на черный цвет (суша)
        black_lower = np.array(BLACK_LOWER)
        black_upper = np.array(BLACK_UPPER)
        black_mask = cv2.inRange(hsv, black_lower, black_upper)
        black_pixels_in_ring = np.sum((mask_ring > 0) & (black_mask > 0))
        black_ratio = black_pixels_in_ring / len(ring_pixels) if len(ring_pixels) > 0 else 0
        
        # Если строгая проверка - более жесткие пороги, если мягкая - более мягкие
        if strict:
            # Строгая проверка: если более 20% окружения - черное (суша), это не наша цель
            if black_ratio > 0.20:
                return False
            
            # Проверяем на синий цвет (вода)
            blue_lower = np.array([100, 50, 50])  # Синий/голубой
            blue_upper = np.array([130, 255, 255])
            blue_mask = cv2.inRange(hsv, blue_lower, blue_upper)
            blue_pixels_in_ring = np.sum((mask_ring > 0) & (blue_mask > 0))
            blue_ratio = blue_pixels_in_ring / len(ring_pixels) if len(ring_pixels) > 0 else 0
            
            # Если менее 30% окружения - синее (вода), возможно это не на воде
            if blue_ratio < 0.30:
                return False
        else:
            # Мягкая проверка (для целей близко к игроку): более мягкие пороги
            # Если более 40% окружения - черное (суша), это не наша цель
            if black_ratio > 0.40:
                return False
            
            # Проверяем на синий цвет (вода)
            blue_lower = np.array([100, 50, 50])  # Синий/голубой
            blue_upper = np.array([130, 255, 255])
            blue_mask = cv2.inRange(hsv, blue_lower, blue_upper)
            blue_pixels_in_ring = np.sum((mask_ring > 0) & (blue_mask > 0))
            blue_ratio = blue_pixels_in_ring / len(ring_pixels) if len(ring_pixels) > 0 else 0
            
            # Если менее 20% окружения - синее (вода), возможно это не на воде
            # Более мягкий порог для целей близко к игроку (может быть перекрытие)
            if blue_ratio < 0.20:
                return False
        
        return True
    
    def find_colored_square(self, img, color_name, hsv=None):
        """
        Находит цветной квадрат с черной оконтовкой на миникарте
        Аналогично find_red_square, но для других цветов (желтый, розовый, белый, оранжевый, зеленый)
        Args:
            img: Изображение миникарты (BGR)
            color_name: Название цвета ('yellow', 'pink', 'white', 'orange', 'green')
            hsv: Опционально предконвертированное HSV изображение (для оптимизации)
        Returns:
            dict с ключами 'found', 'center', 'contour', 'area'
        """
        # Измеряем время обнаружения для статистики
        detection_start = time.time()
        
        h, w = img.shape[:2]
        center_x, center_y = self.minimap_center
        
        # Конвертируем в HSV только если не передан
        if hsv is None:
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        # Выбираем диапазон цвета в зависимости от названия
        if color_name == 'yellow':
            lower = np.array(YELLOW_LOWER)
            upper = np.array(YELLOW_UPPER)
        elif color_name == 'pink':
            lower = np.array(PINK_LOWER)
            upper = np.array(PINK_UPPER)
        elif color_name == 'white':
            lower = np.array(WHITE_LOWER)
            upper = np.array(WHITE_UPPER)
        elif color_name == 'orange':
            lower = np.array(ORANGE_LOWER)
            upper = np.array(ORANGE_UPPER)
        elif color_name == 'green':
            # ВАЖНО: Используем отдельные константы для зеленого квадрата (темно-зеленый #0b9a00)
            # чтобы не путать с зеленой палочкой игрока (ярко-зеленый #00f400, #00db00)
            # Зеленый квадрат: темный (V=100-200), палочка игрока: яркий (V=200-255)
            try:
                lower = np.array(GREEN_SQUARE_LOWER)
                upper = np.array(GREEN_SQUARE_UPPER)
            except NameError:
                # Если константы не определены, используем значения по умолчанию для темно-зеленого
                # RGB(11, 154, 0) -> HSV: H=60, S=255, V=154
                # H=50-70 (зеленый в OpenCV), S=200-255 (высокая насыщенность), V=80-180 (темный, но не черный)
                lower = np.array([50, 200, 80])
                upper = np.array([70, 255, 180])
        elif color_name == 'purple':
            try:
                lower = np.array(PURPLE_LOWER)
                upper = np.array(PURPLE_UPPER)
            except NameError:
                # Если константы не определены, используем значения по умолчанию для фиолетового
                # RGB(106, 5, 184) -> HSV: H=270, S=255, V=184 -> OpenCV H=135, S=255, V=184
                lower = np.array([130, 200, 150])
                upper = np.array([140, 255, 200])
        else:
            return {'found': False}
        
        # Создаем маску для нужного цвета
        mask_color = cv2.inRange(hsv, lower, upper)
        
        # Проверяем, есть ли вообще пиксели нужного цвета
        color_pixels = np.sum(mask_color > 0)
        if color_pixels == 0:
            logger.info(f"{color_name.capitalize()} цвет не найден на миникарте (HSV диапазон: {lower} - {upper})")
            return {'found': False}
        
        logger.debug(f"Найдено {color_pixels} {color_name} пикселей на миникарте")
        
        # Морфологические операции для очистки
        kernel = np.ones((3, 3), np.uint8)
        mask_color = cv2.morphologyEx(mask_color, cv2.MORPH_CLOSE, kernel)
        mask_color = cv2.morphologyEx(mask_color, cv2.MORPH_OPEN, kernel)
        
        # Находим контуры
        contours, _ = cv2.findContours(mask_color, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if len(contours) == 0:
            logger.info(f"Не найдено {color_name} контуров на миникарте (после морфологических операций)")
            return {'found': False}
        
        logger.info(f"Найдено {len(contours)} {color_name} контуров для анализа")
        
        # Список кандидатов с оценкой качества
        candidates = []
        filtered_reasons = {
            'size': 0,
            'moments': 0,
            'vertices': 0,
            'aspect_ratio': 0,
            'extent': 0,
            'black_border': 0
        }
        
        # Анализируем каждый контур
        for contour in contours:
            area = cv2.contourArea(contour)
            
            # Фильтр по размеру
            # Минимальная площадь ослаблена для учета перекрытия игроком и маленьких квадратов.
            # ВАЖНО: Верхний порог сделан намного меньше, чтобы игнорировать большие квадраты
            # (иконки других игроков/лодок), которые по цвету похожи на наши триггеры,
            # но заметно больше по площади.
            min_area = 10
            max_area = 320  # всё, что крупнее – считаем чужими иконками, а не нашими точками
            if area < min_area or area > max_area:
                filtered_reasons['size'] += 1
                if area < min_area:
                    logger.debug(f"  {color_name} контур отфильтрован по размеру: площадь={area:.1f} < {min_area}")
                else:
                    logger.debug(
                        f"  {color_name} контур отфильтрован по размеру: площадь={area:.1f} > {max_area} "
                        f"(вероятно, иконка другого игрока/лодки)"
                    )
                continue
            
            # Вычисляем моменты для центра
            M = cv2.moments(contour)
            if M["m00"] == 0:
                filtered_reasons['moments'] += 1
                continue
                
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            
            # Проверяем расстояние до центра
            dist_to_center = math.sqrt((cx - center_x)**2 + (cy - center_y)**2)
            
            # Определяем, близко ли квадрат к игроку (может быть перекрыт)
            is_near_player = dist_to_center < 40  # Если ближе 40px, может быть перекрыт
            
            # Если контур очень близко к центру (< 20px), проверяем размер
            if dist_to_center < 20:
                if area < 50:  # Ослаблено с 80 до 50 - часть может быть перекрыта
                    continue
            
            # Аппроксимируем контур для проверки формы
            peri = cv2.arcLength(contour, True)
            if peri == 0:
                continue
            
            # Ослабляем параметр аппроксимации для лучшего обнаружения квадратов
            # Используем более мягкую аппроксимацию (0.02 вместо 0.04)
            approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
            
            # Проверяем количество углов
            # Если квадрат близко к игроку, может быть частично перекрыт - допускаем меньше углов
            # ОСЛАБЛЕНО: теперь принимаем контуры с 3+ углами всегда (не только близко к игроку)
            min_vertices = 3  # Всегда минимум 3 угла (квадрат может быть перекрыт или искажен)
            if len(approx) < min_vertices:
                filtered_reasons['vertices'] += 1
                logger.debug(f"  {color_name} контур отфильтрован по углам: найдено {len(approx)}, требуется {min_vertices} (центр=({cx}, {cy}), площадь={area:.1f})")
                continue
            
            # Получаем bounding rect для проверки формы
            x, y, w_rect, h_rect = cv2.boundingRect(contour)
            if w_rect == 0 or h_rect == 0:
                continue
            
            # Проверяем соотношение сторон (должно быть близко к 1:1 для квадрата)
            aspect_ratio = float(w_rect) / h_rect
            # ОСЛАБЛЕНО: более мягкие проверки для учета искажений
            aspect_min = 0.5  # Ослаблено с 0.6/0.7 до 0.5
            aspect_max = 1.5  # Ослаблено с 1.3/1.4 до 1.5
            if aspect_ratio < aspect_min or aspect_ratio > aspect_max:
                filtered_reasons['aspect_ratio'] += 1
                logger.debug(f"  {color_name} контур отфильтрован по aspect_ratio: {aspect_ratio:.2f} (должно быть [{aspect_min:.1f}, {aspect_max:.1f}], центр=({cx}, {cy}))")
                continue
            
            # Проверяем компактность (отношение площади к площади bounding rect)
            rect_area = w_rect * h_rect
            if rect_area == 0:
                continue
            extent = float(area) / rect_area
            # ОСЛАБЛЕНО: более мягкая проверка extent для учета перекрытия и искажений
            min_extent = 0.4  # Ослаблено с 0.5/0.7 до 0.4
            if extent < min_extent:
                filtered_reasons['extent'] += 1
                logger.debug(f"  {color_name} контур отфильтрован по extent: {extent:.2f} < {min_extent:.2f} (центр=({cx}, {cy}), площадь={area:.1f})")
                continue
            
            # ВАЖНО: Проверяем наличие черной обводки (2 пикселя)
            # Увеличиваем область проверки для лучшего обнаружения обводки
            border = 3  # Уменьшено с 5 до 3 для более точной проверки
            x_start = max(0, x - border)
            y_start = max(0, y - border)
            x_end = min(img.shape[1], x + w_rect + border)
            y_end = min(img.shape[0], y + h_rect + border)
            
            roi = img[y_start:y_end, x_start:x_end]
            if roi.size == 0:
                continue
            
            # Ищем черные пиксели вокруг цветного квадрата
            gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            # Более мягкий порог для черного (учитываем возможные искажения)
            black_mask = gray_roi < 60  # Увеличено с 50 до 60
            
            # Создаем маску цветного квадрата в ROI
            color_in_roi = mask_color[y_start:y_end, x_start:x_end]
            
            # Расширяем маску цветного квадрата для поиска обводки вокруг
            # Используем меньший kernel для более точного поиска обводки в 2 пикселя
            color_dilated = cv2.dilate(color_in_roi, np.ones((2, 2), np.uint8), iterations=1)
            # Исключаем сам цветной квадрат из поиска черного
            black_around = black_mask & (~color_dilated.astype(bool))
            
            # Считаем черные пиксели вокруг
            black_count = np.sum(black_around)
            
            # Проверяем периметр - вдоль границы должно быть достаточно черных пикселей
            # Используем более точный расчет периметра
            perimeter_pixels = 2 * (w_rect + h_rect) + 4
            # Также проверяем площадь вокруг квадрата
            roi_area = (x_end - x_start) * (y_end - y_start)
            color_area_in_roi = np.sum(color_in_roi > 0)
            area_around = roi_area - color_area_in_roi
            
            # Вычисляем плотность черных пикселей двумя способами
            black_density_perimeter = float(black_count) / perimeter_pixels if perimeter_pixels > 0 else 0
            black_density_area = float(black_count) / area_around if area_around > 0 else 0
            
            # Используем максимальную плотность (более мягкая проверка)
            black_density = max(black_density_perimeter, black_density_area * 2)
            
            # ТРЕБОВАНИЕ: должна быть четкая черная обводка
            # ОСЛАБЛЕНО: значительно снижен порог для учета частичного перекрытия и искажений
            min_black_density = 0.02  # Снижено с 0.15 до 0.02 (почти отключено, но все еще проверяем)
            if black_density < min_black_density:
                filtered_reasons['black_border'] += 1
                logger.info(f"  {color_name} контур отфильтрован по черной обводке: density={black_density:.2f} < {min_black_density:.2f} "
                           f"(центр=({cx}, {cy}), площадь={area:.1f}, aspect={aspect_ratio:.2f}, extent={extent:.2f}, углов={len(approx)}, "
                           f"perimeter_density={black_density_perimeter:.2f}, area_density={black_density_area:.2f})")
                continue
            
            # Вычисляем общую оценку качества квадрата
            aspect_score = 1.0 - abs(1.0 - aspect_ratio)
            extent_score = extent
            border_score = min(1.0, black_density / 1.0)
            
            # Если квадрат близко к игроку, увеличиваем вес border_score (черная обводка важнее)
            # и уменьшаем вес extent_score (площадь может быть перекрыта)
            if is_near_player:
                quality_score = aspect_score * 0.2 + extent_score * 0.1 + border_score * 0.7
            else:
                quality_score = aspect_score * 0.3 + extent_score * 0.2 + border_score * 0.5
            
            candidates.append({
                'contour': contour,
                'center': (cx, cy),
                'area': area,
                'quality': quality_score,
                'black_density': black_density,
                'aspect_ratio': aspect_ratio,
                'extent': extent
            })
        
        # Логируем статистику фильтрации
        if len(contours) > 0 and len(candidates) == 0:
            logger.info(f"{color_name.capitalize()} контуры отфильтрованы: размер={filtered_reasons['size']}, "
                       f"моменты={filtered_reasons['moments']}, углы={filtered_reasons['vertices']}, "
                       f"aspect_ratio={filtered_reasons['aspect_ratio']}, extent={filtered_reasons['extent']}, "
                       f"черная обводка={filtered_reasons['black_border']}")
        
        # Если есть кандидаты, выбираем самый маленький квадрат (игнорируем большие - это другие игроки)
        # ВАЖНО: Приоритет размера - выбираем самый маленький квадрат среди всех найденных
        if len(candidates) > 0:
            # Сортируем по размеру (площади) - самый маленький первый
            # Если размеры близки (разница < 20%), используем quality как вторичный критерий
            candidates.sort(key=lambda x: (x['area'], -x['quality']))
            best = candidates[0]
            
            # Логируем информацию о всех найденных квадратах для отладки
            if len(candidates) > 1:
                other_areas = [f"{c['area']:.1f}" for c in candidates[1:]]
                logger.debug(f"Найдено {len(candidates)} {color_name} квадратов. Выбран самый маленький: "
                           f"площадь={best['area']:.1f}px (остальные: {', '.join(other_areas)})")
            
            # Проверяем черную обводку с учетом расстояния до игрока
            dist_to_player = math.sqrt((best['center'][0] - center_x)**2 + (best['center'][1] - center_y)**2)
            is_near_player = dist_to_player < 40
            min_black_density = 0.02  # Снижено с 0.15 до 0.02 для учета частичного перекрытия
            
            if best['black_density'] >= min_black_density:
                logger.info(f"Найден {color_name} квадрат: центр={best['center']}, площадь={best['area']:.1f}, "
                           f"расстояние до игрока={dist_to_player:.1f}px, черная обводка={best['black_density']:.2f}, "
                           f"quality={best['quality']:.2f}")
                return {
                    'found': True,
                    'center': best['center'],
                    'contour': best['contour'],
                    'area': best['area']
                }
            else:
                logger.info(f"{color_name.capitalize()} квадрат отфильтрован: недостаточная черная обводка "
                           f"(density={best['black_density']:.2f}, требуется {min_black_density:.2f})")
        else:
            logger.info(f"{color_name.capitalize()} квадрат не найден: все {len(contours)} контуров отфильтрованы")
        
        return {'found': False}
    
    def find_colored_circle(self, img, color_name, hsv=None):
        """
        Находит цветной круг на миникарте
        Args:
            img: Изображение миникарты (BGR)
            color_name: Название цвета ('yellow', 'pink', 'white', 'orange')
            hsv: Опционально предконвертированное HSV изображение (для оптимизации)
        Returns:
            dict с ключами 'found', 'center', 'contour', 'area'
        """
        h, w = img.shape[:2]
        center_x, center_y = self.minimap_center
        
        # Конвертируем в HSV только если не передан
        if hsv is None:
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        # Выбираем диапазон цвета в зависимости от названия
        if color_name == 'yellow':
            lower = np.array(YELLOW_LOWER)
            upper = np.array(YELLOW_UPPER)
        elif color_name == 'pink':
            lower = np.array(PINK_LOWER)
            upper = np.array(PINK_UPPER)
        elif color_name == 'white':
            lower = np.array(WHITE_LOWER)
            upper = np.array(WHITE_UPPER)
        elif color_name == 'orange':
            lower = np.array(ORANGE_LOWER)
            upper = np.array(ORANGE_UPPER)
        else:
            return {'found': False}
        
        # Создаем маску для нужного цвета
        mask = cv2.inRange(hsv, lower, upper)
        
        # Морфологические операции для очистки (более мягкие)
        kernel = np.ones((2, 2), np.uint8)  # Уменьшен размер ядра
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
        
        # Исключаем область вокруг центра (игрок)
        exclude_radius = 25
        center_mask = np.ones((h, w), dtype=np.uint8) * 255
        cv2.circle(center_mask, (center_x, center_y), exclude_radius, 0, -1)
        mask = cv2.bitwise_and(mask, center_mask)
        
        # Находим контуры
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Отладочная информация
        if color_name == 'yellow' and len(contours) == 0:
            # Сохраняем маску для отладки
            if self.save_debug_screenshots and not hasattr(self, '_yellow_mask_saved'):
                debug_path = os.path.join(self.debug_screenshot_dir, f"yellow_mask_{int(time.time())}.png")
                cv2.imwrite(debug_path, mask)
                logger.debug(f"Сохранена маска желтого цвета для отладки: {debug_path}")
                self._yellow_mask_saved = True
        
        if len(contours) == 0:
            return {'found': False}
        
        # Ищем самый подходящий круглый контур
        best_contour = None
        best_score = 0
        filtered_count = 0
        
        for contour in contours:
            area = cv2.contourArea(contour)
            
            # Фильтр по размеру - одинаковый для всех цветов
            if area < 10 or area > 1500:  # Одинаковый диапазон для всех цветов
                filtered_count += 1
                if self.save_debug_screenshots:
                    logger.info(f"{color_name.capitalize()} контур отфильтрован по размеру: площадь={area:.1f} (должно быть 10-1500)")
                continue
            
            # Вычисляем моменты для центра
            M = cv2.moments(contour)
            if M["m00"] == 0:
                filtered_count += 1
                continue
            
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            
            # Проверяем расстояние до центра (не слишком близко к игроку) - одинаково для всех цветов
            dist_to_center = math.sqrt((cx - center_x)**2 + (cy - center_y)**2)
            if dist_to_center < 30:
                filtered_count += 1
                if self.save_debug_screenshots:
                    logger.info(f"{color_name.capitalize()} контур отфильтрован по расстоянию: расстояние={dist_to_center:.1f}px < 30px")
                continue
            
            # Проверяем круглость контура
            peri = cv2.arcLength(contour, True)
            if peri == 0:
                filtered_count += 1
                continue
            
            # Для круга: 4*pi*area / perimeter^2 должно быть близко к 1
            circularity = 4 * math.pi * area / (peri * peri) if peri > 0 else 0
            
            # Проверяем соотношение сторон bounding rect
            x, y, w_rect, h_rect = cv2.boundingRect(contour)
            if w_rect == 0 or h_rect == 0:
                filtered_count += 1
                continue
            
            aspect_ratio = float(w_rect) / h_rect if h_rect > 0 else 0
            aspect_score = 1.0 - abs(1.0 - aspect_ratio)
            
            # Проверяем compactness (плотность заполнения) - для круга должна быть высокой
            rect_area = w_rect * h_rect
            if rect_area == 0:
                filtered_count += 1
                continue
            compactness = area / rect_area if rect_area > 0 else 0
            
            # Проверяем количество вершин (у звездочки их больше, у круга меньше)
            approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
            vertices_count = len(approx)
            
            # УПРОЩЕННЫЕ проверки формы - только самое важное для надежного обнаружения
            # Вычисляем score для оценки качества
            score = circularity * 0.5 + aspect_score * 0.2 + compactness * 0.3
            
            # Сохраняем лучший кандидат для логирования
            if score > best_score:
                best_score = score
                best_contour = contour
                # Логируем параметры лучшего кандидата
                logger.info(f"Лучший {color_name} кандидат: центр=({cx}, {cy}), площадь={area:.1f}, "
                          f"круглость={circularity:.3f}, compactness={compactness:.3f}, "
                          f"aspect_ratio={aspect_ratio:.3f}, вершин={vertices_count}, score={score:.3f}")
            
            # УПРОЩЕННЫЕ ФИЛЬТРЫ - только самое важное:
            # 1. Круглость - должна быть разумной (звездочка и квадрат имеют низкую)
            if circularity < 0.50:  # Ослаблено с 0.60 до 0.50 для надежности
                filtered_count += 1
                logger.info(f"  -> Отфильтрован: круглость {circularity:.3f} < 0.50")
                continue
            
            # 2. Compactness - должна быть разумной
            if compactness < 0.50:  # Ослаблено с 0.60 до 0.50 для надежности
                filtered_count += 1
                logger.info(f"  -> Отфильтрован: compactness {compactness:.3f} < 0.50")
                continue
            
            # 3. Соотношение сторон - должно быть близко к 1 (круг), не квадрат
            if aspect_ratio < 0.70 or aspect_ratio > 1.30:  # Ослаблено с [0.80, 1.20] до [0.70, 1.30]
                filtered_count += 1
                logger.info(f"  -> Отфильтрован: aspect_ratio {aspect_ratio:.3f} не в диапазоне [0.70, 1.30]")
                continue
            
            # 4. Вершины - у круга обычно меньше, у звездочки больше
            if vertices_count > 15:  # Ослаблено с 12 до 15 для надежности
                filtered_count += 1
                logger.info(f"  -> Отфильтрован: вершин {vertices_count} > 15")
                continue
        
        # Отладочная информация для желтого
        if color_name == 'yellow':
            if len(contours) > 0:
                logger.info(f"Найдено {len(contours)} контуров желтого цвета, отфильтровано: {filtered_count}, лучший score: {best_score:.2f}")
                if best_contour is not None:
                    M = cv2.moments(best_contour)
                    if M["m00"] != 0:
                        cx = int(M["m10"] / M["m00"])
                        cy = int(M["m01"] / M["m00"])
                        dist_to_center = math.sqrt((cx - center_x)**2 + (cy - center_y)**2)
                        area = cv2.contourArea(best_contour)
                        peri = cv2.arcLength(best_contour, True)
                        circularity = 4 * math.pi * area / (peri * peri) if peri > 0 else 0
                        x, y, w_rect, h_rect = cv2.boundingRect(best_contour)
                        aspect_ratio = float(w_rect) / h_rect if h_rect > 0 else 0
                        compactness = area / (w_rect * h_rect) if (w_rect * h_rect) > 0 else 0
                        approx = cv2.approxPolyDP(best_contour, 0.02 * peri, True)
                        vertices = len(approx)
                        (center_circle_x, center_circle_y), radius = cv2.minEnclosingCircle(best_contour)
                        enclosing_circle_area = math.pi * radius * radius
                        area_ratio = area / enclosing_circle_area if enclosing_circle_area > 0 else 0
                        logger.info(f"Лучший кандидат: центр=({cx}, {cy}), расстояние={dist_to_center:.1f}px, "
                                   f"площадь={area:.1f}, круглость={circularity:.3f}, compactness={compactness:.3f}, "
                                   f"aspect_ratio={aspect_ratio:.3f}, вершин={vertices}, area_ratio={area_ratio:.3f}, score={best_score:.3f}")
                else:
                    logger.info(f"Желтый круг не найден: все {len(contours)} контуров отфильтрованы")
            else:
                logger.info("Желтый круг не найден: контуров не обнаружено")
        
        # Порог для всех цветов - упрощен и ослаблен для надежного обнаружения
        min_score = 0.35  # Ослаблено с 0.45 до 0.35 для надежного обнаружения реальных кружков
        
        if best_contour is not None and best_score > min_score:
            M = cv2.moments(best_contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                area = cv2.contourArea(best_contour)
                
                # ВАЖНО: Проверяем окружение кружка - должен быть на воде (синий цвет)
                # УПРОЩЕНО: если цель очень близко к игроку (< 50px), ПРОПУСКАЕМ проверку окружения
                # (когда бот близко, круг может перекрываться иконкой игрока и теряться)
                (center_circle_x, center_circle_y), radius = cv2.minEnclosingCircle(best_contour)
                dist_to_player = math.sqrt((cx - center_x)**2 + (cy - center_y)**2)
                
                # Если цель близко к игроку, ПРОПУСКАЕМ проверку окружения (круг может перекрываться)
                if dist_to_player >= 50:
                    # Далеко от игрока - проверяем окружение
                    if not self.check_circle_surrounding(img, hsv, cx, cy, radius, strict=True):
                        filtered_count += 1
                        logger.info(f"{color_name.capitalize()} круг отфильтрован: не на воде (вокруг суша или другие объекты)")
                        return {'found': False}
                else:
                    # Близко к игроку - ПРОПУСКАЕМ проверку окружения (круг может перекрываться иконкой)
                    logger.debug(f"{color_name.capitalize()} круг близко к игроку ({dist_to_player:.1f}px), пропускаю проверку окружения")
                
                if color_name == 'yellow':
                    logger.debug(f"Найден желтый круг: центр=({cx}, {cy}), площадь={area:.1f}, score={best_score:.2f}")
                elif color_name in ['pink', 'white', 'orange']:
                    logger.debug(f"Найден {color_name} круг: центр=({cx}, {cy}), площадь={area:.1f}, score={best_score:.2f}")
                
                # Вычисляем радиус кружка для проверки касания
                (center_circle_x, center_circle_y), circle_radius = cv2.minEnclosingCircle(best_contour)
                
                return {
                    'found': True,
                    'center': (cx, cy),
                    'contour': best_contour,
                    'area': area,
                    'radius': circle_radius  # Сохраняем радиус для проверки касания
                }
        
        return {'found': False}
    
  # По умолчанию пустое множество
    
    def get_current_target(self, minimap, player):
        """
        Определяет текущую цель на основе состояния бота
        Returns:
            dict с ключами 'found', 'center', 'type', 'color' (для кругов) или 'contour' (для квадратов)
        """
        player_pos = self.minimap_center
        if player.get('green_center') is not None:
            player_pos = player['green_center']

        # ОПТИМИЗАЦИЯ: Конвертируем HSV один раз для всех поисков (экономия ~15-20 мс)
        hsv = cv2.cvtColor(minimap, cv2.COLOR_BGR2HSV)

        # Ищем все цвета каждый кадр (передаем предконвертированный HSV)
        yellow_square = self.find_colored_square(minimap, 'yellow', hsv)
        pink_square = self.find_colored_square(minimap, 'pink', hsv)
        white_square = self.find_colored_square(minimap, 'white', hsv)
        orange_square = self.find_colored_square(minimap, 'orange', hsv)
        green_square = self.find_colored_square(minimap, 'green', hsv)
        purple_square = self.find_colored_square(minimap, 'purple', hsv)
        red_square = self.find_red_square(minimap, hsv)

        # Определяем цель в зависимости от состояния
        # Блок 1: стартовая последовательность
        if self.state == 'Y1':  # первый желтый квадрат
            if yellow_square['found']:
                return {
                    'found': True,
                    'center': yellow_square['center'],
                    'type': 'square',
                    'color': 'yellow',
                    'contour': yellow_square.get('contour')
                }
            return {'found': False}

        if self.state == 'P1':  # первый розовый квадрат
            if pink_square['found']:
                return {
                    'found': True,
                    'center': pink_square['center'],
                    'type': 'square',
                    'color': 'pink',
                    'contour': pink_square.get('contour')
                }
            return {'found': False}

        if self.state == 'G1':  # первый зеленый квадрат
            if green_square['found']:
                return {
                    'found': True,
                    'center': green_square['center'],
                    'type': 'square',
                    'color': 'green',
                    'contour': green_square.get('contour')
                }
            return {'found': False}

        # Красные чекпоинты до появления белого (после зеленого):
        # ВАЖНО: Приоритет красным чекпоинтам - плывем к ним, пока не увидим белый
        # Белый проверяется в основном цикле (run) и переключает состояние на W1
        if self.state == 'RED_UNTIL_WHITE':
            if red_square['found']:
                # ВАЖНО: Строгая проверка - не путаем ли мы оранжевый квадрат с красным
                if orange_square['found']:
                    red_area = red_square.get('area', 0)
                    orange_area = orange_square.get('area', 0)
                    
                    # Проверяем расстояние между центрами
                    red_center = red_square['center']
                    orange_center = orange_square['center']
                    dx = red_center[0] - orange_center[0]
                    dy = red_center[1] - orange_center[1]
                    distance_between = math.sqrt(dx*dx + dy*dy)
                    
                    # Если квадраты находятся очень близко друг к другу (< 30px), это скорее всего один и тот же объект
                    if distance_between < 30:
                        logger.warning(f"[RED_UNTIL_WHITE] ❌ Красный и оранжевый квадраты находятся очень близко (расстояние={distance_between:.1f}px) - это скорее всего оранжевый. Игнорирую.")
                        return {'found': False}
                    
                    # УБРАНО: проверка площади не нужна - красные чекпоинты могут быть меньше оранжевых
                    logger.debug(f"[RED_UNTIL_WHITE] ✓ Красный квадрат найден (площадь={red_area:.1f}), оранжевый (площадь={orange_area:.1f}), расстояние={distance_between:.1f}px")
                
                logger.debug(f"[RED_UNTIL_WHITE] Найден красный чекпоинт, плыву к нему")
                return {
                    'found': True,
                    'center': red_square['center'],
                    'type': 'square',
                    'color': 'red',
                    'contour': red_square.get('contour')
                }
            # Если красный не найден - логируем для отладки
            logger.debug(f"[RED_UNTIL_WHITE] Красный чекпоинт не найден")
            return {'found': False}

        if self.state == 'O1':  # первый оранжевый квадрат
            if orange_square['found']:
                return {
                    'found': True,
                    'center': orange_square['center'],
                    'type': 'square',
                    'color': 'orange',
                    'contour': orange_square.get('contour')
                }
            return {'found': False}

        if self.state == 'O_BEFORE_FIRST':  # оранжевый квадрат перед первым чекпоинтом
            if orange_square['found']:
                return {
                    'found': True,
                    'center': orange_square['center'],
                    'type': 'square',
                    'color': 'orange',
                    'contour': orange_square.get('contour')
                }
            return {'found': False}

        if self.state == 'W1':  # первый белый квадрат
            if white_square['found']:
                return {
                    'found': True,
                    'center': white_square['center'],
                    'type': 'square',
                    'color': 'white',
                    'contour': white_square.get('contour')
                }
            return {'found': False}

        if self.state == 'P2':  # второй розовый
            if pink_square['found']:
                return {
                    'found': True,
                    'center': pink_square['center'],
                    'type': 'square',
                    'color': 'pink',
                    'contour': pink_square.get('contour')
                }
            return {'found': False}

        if self.state == 'O2':  # второй оранжевый
            if orange_square['found']:
                return {
                    'found': True,
                    'center': orange_square['center'],
                    'type': 'square',
                    'color': 'orange',
                    'contour': orange_square.get('contour')
                }
            return {'found': False}

        # Блок 2: красные чекпоинты 1–7
        if self.state == 'RED_1_7':
            if red_square['found']:
                # ВАЖНО: Строгая проверка - не путаем ли мы оранжевый квадрат с красным
                if orange_square['found']:
                    red_area = red_square.get('area', 0)
                    orange_area = orange_square.get('area', 0)
                    
                    # Проверяем расстояние между центрами - если они очень близко, это скорее всего один и тот же объект
                    red_center = red_square['center']
                    orange_center = orange_square['center']
                    dx = red_center[0] - orange_center[0]
                    dy = red_center[1] - orange_center[1]
                    distance_between = math.sqrt(dx*dx + dy*dy)
                    
                    # Если квадраты находятся очень близко друг к другу (< 30px), это скорее всего один и тот же объект
                    if distance_between < 30:
                        # Это один и тот же объект - оранжевый, который ошибочно определен как красный
                        logger.warning(f"[RED_1_7] ❌ Красный и оранжевый квадраты находятся очень близко (расстояние={distance_between:.1f}px) - это скорее всего оранжевый, который ошибочно определен как красный. Игнорирую.")
                        return {'found': False}
                    
                    # УБРАНО: проверка площади не нужна - красные чекпоинты могут быть меньше оранжевых
                    # Это нормально. Оставляем только проверку расстояния выше.
                    logger.debug(f"[RED_1_7] ✓ Красный квадрат найден (площадь={red_area:.1f}), оранжевый (площадь={orange_area:.1f}), расстояние между ними={distance_between:.1f}px")
                
                return {
                    'found': True,
                    'center': red_square['center'],
                    'type': 'square',
                    'color': 'red',
                    'contour': red_square.get('contour')
                }
            return {'found': False}

        # Зеленый после 7 чекпоинтов
        if self.state == 'GREEN_AFTER_7':
            if green_square['found']:
                return {
                    'found': True,
                    'center': green_square['center'],
                    'type': 'square',
                    'color': 'green',
                    'contour': green_square.get('contour')
                }
            return {'found': False}

        # 8-й красный чекпоинт (после зеленого после 7-го)
        # КРИТИЧНО: В состоянии RED_8 полностью игнорируем зеленый квадрат
        # Даже если он виден на миникарте, мы его не возвращаем как цель
        if self.state == 'RED_8':
            # Явно игнорируем зеленый квадрат - не возвращаем его как цель, даже если он найден
            if green_square['found']:
                logger.debug(f"[RED_8] ⚠ Зеленый квадрат найден, но игнорирую его (состояние RED_8 - ищу только красный)")
            
            # Логируем, если красный квадрат не найден (для отладки)
            if not red_square['found']:
                logger.debug(f"[RED_8] 🔍 Красный квадрат не найден на миникарте (возможно еще не появился или находится вне видимости)")
            
            if red_square['found']:
                # УБРАНО: Все проверки времени и расстояния до 7-го чекпоинта удалены
                # Теперь бот будет плыть к любому найденному красному квадрату в состоянии RED_8
                
                # ВАЖНО: Строгая проверка - не путаем ли мы оранжевый квадрат с красным
                if orange_square['found']:
                    red_area = red_square.get('area', 0)
                    orange_area = orange_square.get('area', 0)
                    
                    # Проверяем расстояние между центрами
                    red_center = red_square['center']
                    orange_center = orange_square['center']
                    dx = red_center[0] - orange_center[0]
                    dy = red_center[1] - orange_center[1]
                    distance_between = math.sqrt(dx*dx + dy*dy)
                    
                    if distance_between < 30:
                        logger.warning(f"[RED_8] ❌ Красный и оранжевый квадраты находятся очень близко (расстояние={distance_between:.1f}px) - это скорее всего оранжевый. Игнорирую.")
                        return {'found': False}
                
                return {
                    'found': True,
                    'center': red_square['center'],
                    'type': 'square',
                    'color': 'red',
                    'contour': red_square.get('contour')
                }
            return {'found': False}

        # Красный чекпоинт после зеленого (после 7 красных)
        if self.state == 'RED_AFTER_GREEN7':
            if red_square['found']:
                # ВАЖНО: Строгая проверка - не путаем ли мы оранжевый квадрат с красным
                if orange_square['found']:
                    red_area = red_square.get('area', 0)
                    orange_area = orange_square.get('area', 0)
                    
                    # Проверяем расстояние между центрами
                    red_center = red_square['center']
                    orange_center = orange_square['center']
                    dx = red_center[0] - orange_center[0]
                    dy = red_center[1] - orange_center[1]
                    distance_between = math.sqrt(dx*dx + dy*dy)
                    
                    if distance_between < 30:
                        logger.warning(f"[RED_AFTER_GREEN7] ❌ Красный и оранжевый квадраты находятся очень близко (расстояние={distance_between:.1f}px) - это скорее всего оранжевый. Игнорирую.")
                        return {'found': False}
                    
                    # УБРАНО: проверка площади не нужна - красные чекпоинты могут быть меньше оранжевых
                    logger.debug(f"[RED_AFTER_GREEN7] ✓ Красный квадрат найден (площадь={red_area:.1f}), оранжевый (площадь={orange_area:.1f}), расстояние={distance_between:.1f}px")
                
                return {
                    'found': True,
                    'center': red_square['center'],
                    'type': 'square',
                    'color': 'red',
                    'contour': red_square.get('contour')
                }
            return {'found': False}

        # Желтый после красного (после зеленого после 7 красных)
        if self.state == 'Y_AFTER_RED':
            if yellow_square['found']:
                return {
                    'found': True,
                    'center': yellow_square['center'],
                    'type': 'square',
                    'color': 'yellow',
                    'contour': yellow_square.get('contour')
                }
            return {'found': False}

        # 8-й красный чекпоинт (после 7-го) - ДУБЛИКАТ УДАЛЕН, логика уже есть выше

        # Розовый после желтого (перед 9-10 чекпоинтами)
        if self.state == 'P_AFTER_Y':
            if pink_square['found']:
                return {
                    'found': True,
                    'center': pink_square['center'],
                    'type': 'square',
                    'color': 'pink',
                    'contour': pink_square.get('contour')
                }
            return {'found': False}

        # Блок 3: красные чекпоинты 9–10
        if self.state == 'RED_9_10':
            if red_square['found']:
                # ВАЖНО: Строгая проверка - не путаем ли мы оранжевый квадрат с красным
                if orange_square['found']:
                    red_area = red_square.get('area', 0)
                    orange_area = orange_square.get('area', 0)
                    
                    # Проверяем расстояние между центрами
                    red_center = red_square['center']
                    orange_center = orange_square['center']
                    dx = red_center[0] - orange_center[0]
                    dy = red_center[1] - orange_center[1]
                    distance_between = math.sqrt(dx*dx + dy*dy)
                    
                    if distance_between < 30:
                        logger.warning(f"[RED_9_10] ❌ Красный и оранжевый квадраты находятся очень близко (расстояние={distance_between:.1f}px) - это скорее всего оранжевый. Игнорирую.")
                        return {'found': False}
                    
                    # УБРАНО: проверка площади не нужна - красные чекпоинты могут быть меньше оранжевых
                    logger.debug(f"[RED_9_10] ✓ Красный квадрат найден (площадь={red_area:.1f}), оранжевый (площадь={orange_area:.1f}), расстояние={distance_between:.1f}px")
                
                return {
                    'found': True,
                    'center': red_square['center'],
                    'type': 'square',
                    'color': 'red',
                    'contour': red_square.get('contour')
                }
            return {'found': False}

        # Зеленый после 10-го красного
        if self.state == 'GREEN_AFTER_10':
            if green_square['found']:
                return {
                    'found': True,
                    'center': green_square['center'],
                    'type': 'square',
                    'color': 'green',
                    'contour': green_square.get('contour')
                }
            return {'found': False}

        # УБРАНО: Состояния PURPLE_AFTER_10 и W_AFTER_PURPLE10 больше не используются
        # После GREEN_AFTER_10 сразу переходим к RED_UNTIL_PURPLE

        # После 10-го красного – оранжевый и белый
        if self.state == 'O_AFTER_10':
            if orange_square['found']:
                return {
                    'found': True,
                    'center': orange_square['center'],
                    'type': 'square',
                    'color': 'orange',
                    'contour': orange_square.get('contour')
                }
            return {'found': False}

        if self.state == 'W_AFTER_O10':
            if white_square['found']:
                return {
                    'found': True,
                    'center': white_square['center'],
                    'type': 'square',
                    'color': 'white',
                    'contour': white_square.get('contour')
                }
            return {'found': False}

        # Красные до появления фиолетового:
        # ВАЖНО: Переключение на PURPLE_FINAL при обнаружении фиолетового происходит в основном цикле (run)
        # Здесь возвращаем только красный квадрат как цель, пока не переключились на PURPLE_FINAL
        if self.state == 'RED_UNTIL_PURPLE':
            if red_square['found']:
                # ВАЖНО: Строгая проверка - не путаем ли мы оранжевый квадрат с красным
                if orange_square['found']:
                    red_area = red_square.get('area', 0)
                    orange_area = orange_square.get('area', 0)
                    
                    # Проверяем расстояние между центрами
                    red_center = red_square['center']
                    orange_center = orange_square['center']
                    dx = red_center[0] - orange_center[0]
                    dy = red_center[1] - orange_center[1]
                    distance_between = math.sqrt(dx*dx + dy*dy)
                    
                    if distance_between < 30:
                        logger.warning(f"[RED_UNTIL_PURPLE] ❌ Красный и оранжевый квадраты находятся очень близко (расстояние={distance_between:.1f}px) - это скорее всего оранжевый. Игнорирую.")
                        # Если красный квадрат отфильтрован, но есть кэш - используем его
                        if self.last_red_checkpoint_center is not None:
                            logger.info(f"[RED_UNTIL_PURPLE] Использую кэш последнего красного чекпоинта: {self.last_red_checkpoint_center}")
                            return {
                                'found': True,
                                'center': self.last_red_checkpoint_center,
                                'type': 'square',
                                'color': 'red',
                                'contour': None
                            }
                        return {'found': False}
                    
                    # УБРАНО: проверка площади не нужна - красные чекпоинты могут быть меньше оранжевых
                    logger.debug(f"[RED_UNTIL_PURPLE] ✓ Красный квадрат найден (площадь={red_area:.1f}), оранжевый (площадь={orange_area:.1f}), расстояние={distance_between:.1f}px")
                
                # Сохраняем центр красного квадрата в кэш для использования, если он временно исчезнет
                self.last_red_checkpoint_center = red_square['center']
                
                return {
                    'found': True,
                    'center': red_square['center'],
                    'type': 'square',
                    'color': 'red',
                    'contour': red_square.get('contour')
                }
            
            # Если красный квадрат не найден, но есть кэш последнего известного - используем его
            if self.last_red_checkpoint_center is not None:
                logger.debug(f"[RED_UNTIL_PURPLE] Красный квадрат не найден, использую кэш последнего известного: {self.last_red_checkpoint_center}")
                return {
                    'found': True,
                    'center': self.last_red_checkpoint_center,
                    'type': 'square',
                    'color': 'red',
                    'contour': None
                }
            
            return {'found': False}

        # Финальный блок: оранжевый -> розовый -> желтый -> красный
        if self.state == 'PURPLE_FINAL':
            if purple_square['found']:
                return {
                    'found': True,
                    'center': purple_square['center'],
                    'type': 'square',
                    'color': 'purple',
                    'contour': purple_square.get('contour')
                }
            return {'found': False}

        if self.state == 'P_FINAL':
            if pink_square['found']:
                return {
                    'found': True,
                    'center': pink_square['center'],
                    'type': 'square',
                    'color': 'pink',
                    'contour': pink_square.get('contour')
                }
            return {'found': False}

        if self.state == 'Y_FINAL':
            if yellow_square['found']:
                return {
                    'found': True,
                    'center': yellow_square['center'],
                    'type': 'square',
                    'color': 'yellow',
                    'contour': yellow_square.get('contour')
                }
            return {'found': False}

        if self.state == 'RED_FINAL':
            if red_square['found']:
                # ВАЖНО: Строгая проверка - не путаем ли мы оранжевый квадрат с красным
                if orange_square['found']:
                    red_area = red_square.get('area', 0)
                    orange_area = orange_square.get('area', 0)
                    
                    # Проверяем расстояние между центрами
                    red_center = red_square['center']
                    orange_center = orange_square['center']
                    dx = red_center[0] - orange_center[0]
                    dy = red_center[1] - orange_center[1]
                    distance_between = math.sqrt(dx*dx + dy*dy)
                    
                    if distance_between < 30:
                        logger.warning(f"[RED_FINAL] ❌ Красный и оранжевый квадраты находятся очень близко (расстояние={distance_between:.1f}px) - это скорее всего оранжевый. Игнорирую.")
                        return {'found': False}
                    
                    # УБРАНО: проверка площади не нужна - красные чекпоинты могут быть меньше оранжевых
                    logger.debug(f"[RED_FINAL] ✓ Красный квадрат найден (площадь={red_area:.1f}), оранжевый (площадь={orange_area:.1f}), расстояние={distance_between:.1f}px")
                
                return {
                    'found': True,
                    'center': red_square['center'],
                    'type': 'square',
                    'color': 'red',
                    'contour': red_square.get('contour')
                }
            return {'found': False}

        # По умолчанию возвращаем пустую цель
        return {'found': False}
    
    def check_target_reached(self, target, player, distance):
        """
        Проверяет, достигнута ли цель
        Для кружков: проверяет касание иконки персонажа с кружком
        Для квадратов: проверяет расстояние
        Returns:
            True если цель достижена, False иначе
        """
        if not target['found']:
            return False
        
        # Для кружков проверяем касание иконки персонажа с кружком
        if target.get('type') == 'circle':
            # Получаем позицию игрока
            player_pos = self.minimap_center
            if player.get('green_center') is not None:
                player_pos = player['green_center']
            
            # Получаем центр и радиус кружка
            target_center = target['center']
            circle_radius = target.get('radius', 5)  # По умолчанию 5 пикселей если радиус не указан
            
            # Радиус иконки персонажа (примерно 10-12 пикселей)
            player_icon_radius = 12
            
            # Расстояние между центрами
            dx = target_center[0] - player_pos[0]
            dy = target_center[1] - player_pos[1]
            center_distance = math.sqrt(dx*dx + dy*dy)
            
            # Проверяем касание: расстояние между центрами <= сумма радиусов
            touch_distance = circle_radius + player_icon_radius
            
            # Добавляем текущее расстояние в историю (храним последние 5 значений)
            self.distance_history.append(center_distance)
            if len(self.distance_history) > 5:
                self.distance_history.pop(0)
            
            # Если иконка персонажа касается кружка - цель достигнута
            if center_distance <= touch_distance:
                return True
            
            # ВАЖНО: Если расстояние было меньше суммы радиусов (касание), а потом начало увеличиваться,
            # это значит бот ПРОЕХАЛ через цель - нужно переключить состояние
            if len(self.distance_history) >= 3:
                # Проверяем паттерн: расстояние уменьшалось до минимума (касание), потом начало увеличиваться
                min_dist = min(self.distance_history)
                if min_dist <= touch_distance:
                    # Расстояние было меньше суммы радиусов (касание) - проверяем увеличивается ли оно сейчас
                    recent_distances = self.distance_history[-3:]
                    # Если последние 3 расстояния увеличиваются, значит бот проехал через цель
                    if recent_distances[0] < recent_distances[1] < recent_distances[2]:
                        # Расстояние увеличивается после касания - бот проехал через цель
                        return True
            
            return False
        
        # Для квадратов (включая все цветные) используем адаптивный порог
        # Добавляем текущее расстояние в историю (храним последние 5 значений)
        self.distance_history.append(distance)
        if len(self.distance_history) > 5:
            self.distance_history.pop(0)

        # Адаптивный порог:
        # - для чекпоинтов (красные квадраты) используем строгий порог для точного прохождения по центру,
        # - для навигационных квадратов (желтый/розовый/белый/оранжевый/зеленый) делаем порог больше,
        #   чтобы цель засчитывалась, даже если иконка игрока не заходит точно в центр.
        effective_threshold = self.circle_reached_threshold
        color = target.get('color')
        
        if color == 'red':
            # Для красных квадратов - используем более мягкий порог
            # Так как бот не всегда проходит точно по центру, используем порог 20px
            # Это позволит засчитывать чекпоинты когда бот достаточно близко
            effective_threshold = 20.0  # Порог для засчитывания красных чекпоинтов (20px)
        elif color in ('yellow', 'pink', 'white', 'orange', 'green'):
            # Для цветных квадратов - порог 25px (достаточно близко, чтобы считать что достигли)
            effective_threshold = max(effective_threshold, 25)
        
        # Если расстояние меньше порога - считаем что достигли
        if distance < effective_threshold:
            logger.info(f"Квадрат достигнут: расстояние {distance:.2f}px < {effective_threshold}px (color={color}, state={getattr(self, 'state', 'unknown')})")
            return True
        
        # ВАЖНО: Если расстояние было очень маленьким (меньше порога), а потом начало увеличиваться,
        # это значит бот ПРОЕХАЛ через цель - нужно переключить состояние
        if len(self.distance_history) >= 3:
            # Проверяем паттерн: расстояние уменьшалось до минимума, потом начало увеличиваться
            min_dist = min(self.distance_history)
            if min_dist < effective_threshold:
                # Расстояние было меньше порога - проверяем увеличивается ли оно сейчас
                recent_distances = self.distance_history[-3:]
                # Если последние 3 расстояния увеличиваются, значит бот проехал через цель
                if recent_distances[0] < recent_distances[1] < recent_distances[2]:
                    # Расстояние увеличивается после минимума - бот проехал через цель
                    logger.info(f"Квадрат {color} пройден: расстояние уменьшилось до {min_dist:.2f}px, затем начало увеличиваться (state={getattr(self, 'state', 'unknown')})")
                    return True
        
        return False
    
    def update_state(self, target, distance, player):
        """
        Обновляет состояние бота на основе достигнутых целей
        """
        if not target['found']:
            return

        # Проверяем достижение цели
        target_reached = self.check_target_reached(target, player, distance)
        
        # Логирование для красных чекпоинтов (только при проблемах)
        # if target.get('color') == 'red' and target.get('type') == 'square':
        #     min_dist_in_history = min(self.distance_history) if len(self.distance_history) > 0 else distance
        #     logger.debug(f"[RED] State={self.state}, target_reached={target_reached}, distance={distance:.2f}px")
        
        # ВАЖНО: Для красных чекпоинтов используем альтернативную логику засчитывания
        # Если check_target_reached вернул False, но мы были достаточно близко - все равно засчитываем
        if target.get('color') == 'red' and target.get('type') == 'square' and not target_reached:
            if self.state in ['RED_1_7', 'RED_9_10', 'RED_AFTER_GREEN7', 'RED_UNTIL_WHITE', 'RED_UNTIL_PURPLE', 'RED_FINAL']:
                min_dist_in_history = min(self.distance_history) if len(self.distance_history) > 0 else distance
                # Если минимальное расстояние было меньше 25px - считаем что достигли
                if min_dist_in_history < 25.0:
                    logger.debug(f"[RED] Альтернативная проверка: мин. расстояние {min_dist_in_history:.2f}px < 25px -> считаю что достигли")
                    target_reached = True
        
        if not target_reached:
            return
        
        # ВАЖНО: Для красных чекпоинтов используем комбинацию задержки времени + флаг
        # НЕ используем проверку центра, т.к. миникарта динамическая и движется за персонажем
        # Координаты чекпоинтов всегда относительно центра миникарты, поэтому все чекпоинты
        # будут иметь близкие координаты когда мы их забираем (все около центра миникарты)
        if target.get('color') == 'red' and target.get('type') == 'square':
            # Защита 1: проверка флага (как для других целей)
            # Если этот чекпоинт уже был засчитан в этом цикле проверки - блокируем
            if self.target_reached_flag:
                logger.debug(f"[RED] ❌ Блокирую засчитывание - флаг target_reached_flag уже установлен (чекпоинт уже обработан)")
                return
            
            # Защита 2: проверка задержки 1.5 секунды между засчитываниями РАЗНЫХ чекпоинтов
            current_time = time.time()
            time_since_last_collection = current_time - self._last_checkpoint_collected_time
            
            if time_since_last_collection < 1.5:
                logger.warning(f"[RED] ❌ Пропускаю засчитывание - прошло только {time_since_last_collection:.2f} сек с последнего чекпоинта (требуется 1.5 сек)")
                return
            
            # Все проверки пройдены - устанавливаем флаг и обновляем время
            self.target_reached_flag = True  # Устанавливаем флаг ПЕРЕД засчитыванием
            self._last_checkpoint_collected_time = current_time
            
            logger.info(f"[RED CHECKPOINT DEBUG] ✓ Красный чекпоинт достигнут (state={self.state}, distance={distance:.1f}px), перехожу к логике подсчета.")
        else:
            # Для не-красных целей используем стандартную логику с флагом
            if self.target_reached_flag:
                return
            self.target_reached_flag = True

        # Утилита: сброс общих промежуточных данных при смене состояния
        def _reset_for_new_state():
            self.last_circle_center = None
            self.last_circle_distance = None
            self.min_distance_to_target = None
            self.distance_history = []
            self.target_reached_flag = False
            # Сбрасываем отслеживание красного чекпоинта только если переходим в состояние не связанное с красными
            if self.state not in ['RED_1_7', 'RED_8', 'RED_9_10', 'RED_AFTER_GREEN7', 'RED_UNTIL_WHITE', 'RED_UNTIL_PURPLE', 'RED_FINAL']:
                self.last_red_checkpoint_center = None
                self.last_red_checkpoint_distance = None
                self.red_checkpoint_min_distance = None

        # ---- Блок 1: стартовая последовательность ----
        if self.state == 'Y1' and target['type'] == 'square' and target.get('color') == 'yellow':
            logger.info("Достигнут первый желтый квадрат -> перехожу к первому розовому.")
            self.state = 'P1'
            _reset_for_new_state()
            time.sleep(1.0)  # Задержка 1 секунда после достижения цели
            return

        if self.state == 'P1' and target['type'] == 'square' and target.get('color') == 'pink':
            logger.info("Достигнут первый розовый квадрат -> перехожу к первому зеленому.")
            self.state = 'G1'
            _reset_for_new_state()
            time.sleep(1.0)  # Задержка 1 секунда после достижения цели
            return

        if self.state == 'G1' and target['type'] == 'square' and target.get('color') == 'green':
            logger.info("Достигнут первый зеленый квадрат -> плыву к красным чекпоинтам, жду появления белого квадрата.")
            # Сбрасываем счетчик при начале сбора красных чекпоинтов
            if self.checkpoint_counter:
                self.checkpoint_counter.reset()
                logger.info("[CHECKPOINT COUNTER] Счетчик сброшен при переходе в RED_UNTIL_WHITE")
            self.state = 'RED_UNTIL_WHITE'
            _reset_for_new_state()
            time.sleep(1.0)  # Задержка 1 секунда после достижения цели
            return

        # ---- Красные чекпоинты до появления белого (после зеленого) ----
        if self.state == 'RED_UNTIL_WHITE':
            # ВАЖНО: Переключение на W1 при обнаружении белого происходит в основном цикле (run),
            # а не здесь, чтобы переключаться сразу как только УВИДЕЛИ белый, а не ждать достижения.
            # Здесь обрабатываем только достижение красных чекпоинтов.
            if target['type'] == 'square' and target.get('color') == 'red':
                # ВАЖНО: check_target_reached уже проверил достижение цели и вернул True
                # Проверка на дубликат уже выполнена выше, поэтому здесь мы просто увеличиваем счетчик
                
                # Получаем минимальное расстояние для логирования
                min_distance_in_history = min(self.distance_history) if len(self.distance_history) > 0 else distance
                # ВАЖНО: Время задержки уже обновлено выше в update_state
                
                # НОВАЯ СИСТЕМА ПОДСЧЕТА (костыль для бага): каждый вызов add_checkpoint() = +1 внутренний
                # Из-за бага один физический чекпоинт вызывает add_checkpoint() 3 раза
                # Внешний счетчик компенсирует: каждые 3 вызова = 1 внешний (1 физический чекпоинт)
                if self.checkpoint_counter:
                    internal, external = self.checkpoint_counter.add_checkpoint()
                    self.red_squares_collected = external  # Для обратной совместимости логирования
                    logger.info(f"✓ Вызов add_checkpoint() (internal: {internal}, external: {external}, physical: {external}, фаза RED_UNTIL_WHITE, мин. расстояние: {min_distance_in_history:.1f}px).")
                else:
                    # Старая система (fallback)
                    self.red_squares_collected += 1
                    logger.info(f"✓ Собран красный чекпоинт #{self.red_squares_collected}/10 (фаза RED_UNTIL_WHITE, мин. расстояние: {min_distance_in_history:.1f}px, текущее: {distance:.1f}px).")
                
                self.last_collected_square_center = target['center']
                
                # ВАЖНО: Флаг уже установлен выше в update_state перед засчитыванием
                # Сбрасываем отслеживание красного чекпоинта после засчитывания
                self.last_red_checkpoint_center = None
                self.last_red_checkpoint_distance = None
                self.red_checkpoint_min_distance = None
                
                # Сбрасываем флаг, чтобы можно было собирать следующий чекпоинт
                self.target_reached_flag = False
            return

        # Белый квадрат после красных чекпоинтов (после зеленого)
        if self.state == 'W1' and target['type'] == 'square' and target.get('color') == 'white':
            logger.info("Достигнут белый квадрат после красных чекпоинтов -> перехожу ко второму розовому.")
            # НЕ сбрасываем счетчик здесь - он будет сброшен в P2 перед началом RED_1_7
            if self.checkpoint_counter:
                logger.info(f"[CHECKPOINT COUNTER] Текущее состояние счетчика: Internal={self.checkpoint_counter.get_internal()}, External={self.checkpoint_counter.get_external()}")
            self.state = 'P2'
            _reset_for_new_state()
            return

        if self.state == 'P2' and target['type'] == 'square' and target.get('color') == 'pink':
            logger.info("Достигнут второй розовый квадрат -> перехожу к оранжевому квадрату.")
            self.state = 'O_BEFORE_FIRST'
            _reset_for_new_state()
            time.sleep(1.0)  # Задержка 1 секунда после достижения цели
            return

        # ---- Оранжевый квадрат перед первым чекпоинтом (после P2) ----
        if self.state == 'O_BEFORE_FIRST' and target['type'] == 'square' and target.get('color') == 'orange':
            logger.info("Достигнут оранжевый квадрат -> начинаю собирать красные чекпоинты 1-7.")
            self.last_collected_square_center = None
            self.last_red_checkpoint_center = None
            self.last_red_checkpoint_distance = None
            self.red_checkpoint_min_distance = None
            self.distance_history = []  # Сбрасываем историю расстояний
            # Теперь меняем состояние
            self.state = 'RED_1_7'
            self.red_squares_collected = 0  # Старый счетчик для логирования
            # ВАЖНО: Сбрасываем новую систему подсчета перед началом сбора 7 чекпоинтов
            if self.checkpoint_counter:
                old_internal = self.checkpoint_counter.get_internal()
                old_external = self.checkpoint_counter.get_external()
                self.checkpoint_counter.reset()
                logger.info(f"[CHECKPOINT COUNTER] Счетчик сброшен при переходе в RED_1_7 (было: Internal={old_internal}, External={old_external})")
            # ВАЖНО: Сбрасываем время последнего засчитывания, чтобы первый чекпоинт мог быть засчитан сразу
            self._last_checkpoint_collected_time = 0
            # Сбрасываем флаг засчитанного при достижении
            self._checkpoint_counted_at_reach = False
            _reset_for_new_state()
            time.sleep(1.0)  # Задержка 1 секунда после достижения цели
            return

        # ---- Блок 2: красные чекпоинты 1–7 ----
        if self.state == 'RED_1_7' and target['type'] == 'square' and target.get('color') == 'red':
            # ВАЖНО: check_target_reached уже проверил достижение цели и вернул True
            # Проверка на дубликат уже выполнена выше, поэтому здесь мы просто увеличиваем счетчик
            
            # Получаем минимальное расстояние для логирования
            min_distance_in_history = min(self.distance_history) if len(self.distance_history) > 0 else distance
            current_time = time.time()
            
            # НОВАЯ СИСТЕМА ПОДСЧЕТА (костыль для бага): каждый вызов add_checkpoint() = +1 внутренний
            # Из-за бага один физический чекпоинт вызывает add_checkpoint() 3 раза
            # Внешний счетчик компенсирует: каждые 3 вызова = 1 внешний (1 физический чекпоинт)
            if self.checkpoint_counter:
                internal, external = self.checkpoint_counter.add_checkpoint()
                self.red_squares_collected = external  # Для обратной совместимости логирования
                logger.info(f"✓ Вызов add_checkpoint() (internal: {internal}, external: {external}, physical: {external}, мин. расстояние: {min_distance_in_history:.1f}px).")
            else:
                # Старая система (fallback)
                self.red_squares_collected += 1
                logger.info(f"✓ Собран красный чекпоинт #{self.red_squares_collected}/10 (фаза 1–7, мин. расстояние: {min_distance_in_history:.1f}px, текущее: {distance:.1f}px).")
            
            self.last_collected_square_center = target['center']
            self._last_checkpoint_collected_time = current_time

            # ВАЖНО: Сохраняем центр засчитанного чекпоинта для проверки при исчезновении
            # чтобы не засчитывать его повторно при исчезновении
            self.last_red_checkpoint_center = target['center']
            self.last_red_checkpoint_distance = distance
            # Сбрасываем минимальное расстояние, чтобы при исчезновении не засчитывать повторно
            self.red_checkpoint_min_distance = None

            # НОВАЯ СИСТЕМА: проверяем внешний счетчик (маршрут зависит от него)
            # Внешний счетчик компенсирует баг: каждые 3 вызова (1 физический чекпоинт) = 1 внешний
            # 7 внешних = 7 физических чекпоинтов собрано (21 внутренний вызов из-за бага)
            if self.checkpoint_counter:
                if self.checkpoint_counter.check_threshold_external(7):
                    external_count = self.checkpoint_counter.get_external()
                    internal_count = self.checkpoint_counter.get_internal()
                    logger.info(f"Собрано {external_count} физических чекпоинтов (internal calls: {internal_count}) -> плыву к зеленому квадрату.")
                    # КРИТИЧНО: Сохраняем позицию 7-го чекпоинта перед переходом, чтобы потом проверять расстояние до 8-го
                    # self.last_red_checkpoint_center уже сохранен выше (строка 2315)
                    self.state = 'GREEN_AFTER_7'
                    self._green_after_7_transition_time = time.time()  # Время перехода для защиты
                    _reset_for_new_state()
                    time.sleep(1.0)  # Задержка 1 секунда после достижения цели
                else:
                    # Сбрасываем флаг, чтобы можно было собирать следующий чекпоинт
                    self.target_reached_flag = False
            else:
                # Старая система (fallback)
                if self.red_squares_collected >= 7:
                    logger.info("Собрано 7 красных чекпоинтов -> плыву к зеленому квадрату.")
                    # Сохраняем позицию 7-го чекпоинта
                    # self.last_red_checkpoint_center уже сохранен выше (строка 2315)
                    self.state = 'GREEN_AFTER_7'
                    self._green_after_7_transition_time = time.time()  # Время перехода для защиты
                    _reset_for_new_state()
                    time.sleep(1.0)  # Задержка 1 секунда после достижения цели
                else:
                    # Сбрасываем флаг, чтобы можно было собирать следующий чекпоинт
                    self.target_reached_flag = False
            return

        # ---- Зеленый после 7 чекпоинтов ----
        if self.state == 'GREEN_AFTER_7' and target['type'] == 'square' and target.get('color') == 'green':
            # ВАЖНО: target_reached_flag уже установлен выше в update_state для не-красных целей
            # Это предотвращает повторную обработку. Здесь мы просто обрабатываем достижение.
            logger.info("Достигнут зеленый квадрат после 7 чекпоинтов -> плыву к 8-му чекпоинту.")
            self._green_square_reached_time = time.time()  # Сохраняем время достижения для автоматического +1
            self.state = 'RED_8'
            _reset_for_new_state()  # Это сбросит target_reached_flag
            time.sleep(1.0)  # Задержка 1 секунда после достижения цели
            return

        # ---- 8-й красный чекпоинт (после зеленого после 7-го) ----
        if self.state == 'RED_8' and target['type'] == 'square' and target.get('color') == 'red':
            # ВАЖНО: check_target_reached уже проверил достижение цели и вернул True
            # Проверка на дубликат уже выполнена выше, поэтому здесь мы просто увеличиваем счетчик
            
            # Получаем минимальное расстояние для логирования
            min_distance_in_history = min(self.distance_history) if len(self.distance_history) > 0 else distance
            current_time = time.time()
            
            # УБРАНО: Проверка времени и расстояния до 7-го чекпоинта удалена
            # Теперь бот будет засчитывать любой найденный красный квадрат в состоянии RED_8
            
            # НОВАЯ СИСТЕМА ПОДСЧЕТА (костыль для бага): каждый вызов add_checkpoint() = +1 внутренний
            # Из-за бага один физический чекпоинт вызывает add_checkpoint() 3 раза
            # Внешний счетчик компенсирует: каждые 3 вызова = 1 внешний (1 физический чекпоинт)
            # ВАЖНО: Засчитываем чекпоинт сразу, как в RED_1_7, БЕЗ проверки времени и флага
            if self.checkpoint_counter:
                internal, external = self.checkpoint_counter.add_checkpoint()
                self.red_squares_collected = external  # Для обратной совместимости логирования
                logger.info(f"✓ Вызов add_checkpoint() для 8-го чекпоинта (internal: {internal}, external: {external}, physical: {external}, мин. расстояние: {min_distance_in_history:.1f}px).")
            else:
                # Старая система (fallback)
                self.red_squares_collected += 1
                logger.info(f"✓ Собран 8-й красный чекпоинт (мин. расстояние: {min_distance_in_history:.1f}px).")
            
            self.last_collected_square_center = target['center']
            self._last_checkpoint_collected_time = current_time

            # ВАЖНО: Сохраняем центр засчитанного чекпоинта для проверки при исчезновении
            # чтобы не засчитывать его повторно при исчезновении
            self.last_red_checkpoint_center = target['center']
            self.last_red_checkpoint_distance = distance
            # Сбрасываем минимальное расстояние, чтобы при исчезновении не засчитывать повторно
            self.red_checkpoint_min_distance = None

            logger.info(f"Достигнут 8-й красный чекпоинт (мин. расстояние: {min_distance_in_history:.1f}px) -> плыву к желтому квадрату.")
            self.state = 'Y_AFTER_RED'
            self._green_after_7_transition_time = 0  # Сбрасываем время перехода после сбора 8-го
            self._green_square_reached_time = 0  # Сбрасываем время достижения зеленого квадрата
            _reset_for_new_state()
            time.sleep(1.0)  # Задержка 1 секунда после достижения цели
            return

        # ---- Желтый после красного (после зеленого после 7 красных) ----
        if self.state == 'Y_AFTER_RED' and target['type'] == 'square' and target.get('color') == 'yellow':
            logger.info("Достигнут желтый квадрат после красного -> плыву к розовому квадрату.")
            self.state = 'P_AFTER_Y'
            _reset_for_new_state()
            time.sleep(1.0)  # Задержка 1 секунда после достижения цели
            return

        # ---- Розовый после желтого (перед 9-10 чекпоинтами) ----
        if self.state == 'P_AFTER_Y' and target['type'] == 'square' and target.get('color') == 'pink':
            logger.info("Достигнут розовый квадрат после желтого -> собираю 9-й и 10-й красные чекпоинты.")
            self.state = 'RED_9_10'
            _reset_for_new_state()
            time.sleep(1.0)  # Задержка 1 секунда после достижения цели
            return

        # ---- Блок 3: красные чекпоинты 9–10 ----
        if self.state == 'RED_9_10' and target['type'] == 'square' and target.get('color') == 'red':
            # ВАЖНО: check_target_reached уже проверил достижение цели и вернул True
            # Проверка на дубликат уже выполнена выше, поэтому здесь мы просто увеличиваем счетчик
            
            # Получаем минимальное расстояние для логирования
            min_distance_in_history = min(self.distance_history) if len(self.distance_history) > 0 else distance
            current_time = time.time()
            
            # НОВАЯ СИСТЕМА ПОДСЧЕТА (костыль для бага): каждый вызов add_checkpoint() = +1 внутренний
            # Из-за бага один физический чекпоинт вызывает add_checkpoint() 3 раза
            # Внешний счетчик компенсирует: каждые 3 вызова = 1 внешний (1 физический чекпоинт)
            if self.checkpoint_counter:
                internal, external = self.checkpoint_counter.add_checkpoint()
                self.red_squares_collected = external  # Для обратной совместимости логирования
                logger.info(f"✓ Вызов add_checkpoint() (internal: {internal}, external: {external}, physical: {external}, мин. расстояние: {min_distance_in_history:.1f}px).")
            else:
                # Старая система (fallback)
                self.red_squares_collected += 1
                logger.info(f"✓ Собран красный чекпоинт #{self.red_squares_collected}/10 (фаза 9–10, мин. расстояние: {min_distance_in_history:.1f}px, текущее: {distance:.1f}px).")
            
            self.last_collected_square_center = target['center']
            self._last_checkpoint_collected_time = current_time

            # ВАЖНО: Сохраняем центр засчитанного чекпоинта для проверки при исчезновении
            # чтобы не засчитывать его повторно при исчезновении
            self.last_red_checkpoint_center = target['center']
            self.last_red_checkpoint_distance = distance
            # Сбрасываем минимальное расстояние, чтобы при исчезновении не засчитывать повторно
            self.red_checkpoint_min_distance = None

            # НОВАЯ СИСТЕМА: проверяем внешний счетчик (маршрут зависит от него)
            # Внешний счетчик компенсирует баг: каждые 3 вызова (1 физический чекпоинт) = 1 внешний
            # 10 внешних = 10 физических чекпоинтов собрано (30 внутренних вызовов из-за бага)
            if self.checkpoint_counter:
                if self.checkpoint_counter.check_threshold_external(10):
                    external_count = self.checkpoint_counter.get_external()
                    internal_count = self.checkpoint_counter.get_internal()
                    logger.info(f"Собрано {external_count} физических чекпоинтов (internal calls: {internal_count}) -> жду 2 секунды с W без поворотов, затем плыву к зеленому квадрату.")
                    
                    # КРИТИЧНО: Отпускаем все повороты (A/D) перед задержкой
                    if self.keys_pressed['a']:
                        try:
                            self.send_key_to_window('a', press=False)
                            self.keyboard.release('a')
                        except:
                            pass
                        self.keys_pressed['a'] = False
                    if self.keys_pressed['d']:
                        try:
                            self.send_key_to_window('d', press=False)
                            self.keyboard.release('d')
                        except:
                            pass
                        self.keys_pressed['d'] = False
                    self.current_turn_direction = None
                    
                    # Убеждаемся, что W нажата
                    if not self.keys_pressed['w']:
                        try:
                            self.send_key_to_window('w', press=True)
                            self.keyboard.press('w')
                        except:
                            pass
                        self.keys_pressed['w'] = True
                    
                    # Ждем 2 секунды с W без поворотов
                    logger.info("[10-й чекпоинт] Держу W 2 секунды без поворотов для полного забора чекпоинта...")
                    time.sleep(2.0)
                    logger.info("[10-й чекпоинт] Задержка завершена, перехожу к зеленому квадрату.")
                    
                    self.state = 'GREEN_AFTER_10'
                    _reset_for_new_state()
                else:
                    # Сбрасываем флаг, чтобы можно было собирать следующий чекпоинт
                    self.target_reached_flag = False
            else:
                # Старая система (fallback)
                if self.red_squares_collected >= 10:
                    logger.info("Собрано 10 красных чекпоинтов -> жду 2 секунды с W без поворотов, затем плыву к зеленому квадрату.")
                    
                    # КРИТИЧНО: Отпускаем все повороты (A/D) перед задержкой
                    if self.keys_pressed['a']:
                        try:
                            self.send_key_to_window('a', press=False)
                            self.keyboard.release('a')
                        except:
                            pass
                        self.keys_pressed['a'] = False
                    if self.keys_pressed['d']:
                        try:
                            self.send_key_to_window('d', press=False)
                            self.keyboard.release('d')
                        except:
                            pass
                        self.keys_pressed['d'] = False
                    self.current_turn_direction = None
                    
                    # Убеждаемся, что W нажата
                    if not self.keys_pressed['w']:
                        try:
                            self.send_key_to_window('w', press=True)
                            self.keyboard.press('w')
                        except:
                            pass
                        self.keys_pressed['w'] = True
                    
                    # Ждем 2 секунды с W без поворотов
                    logger.info("[10-й чекпоинт] Держу W 2 секунды без поворотов для полного забора чекпоинта...")
                    time.sleep(2.0)
                    logger.info("[10-й чекпоинт] Задержка завершена, перехожу к зеленому квадрату.")
                    
                    self.state = 'GREEN_AFTER_10'
                    _reset_for_new_state()
                else:
                    # Сбрасываем флаг, чтобы можно было собирать следующий чекпоинт
                    self.target_reached_flag = False
            return

        # ---- Зеленый после 10-го красного ----
        if self.state == 'GREEN_AFTER_10' and target['type'] == 'square' and target.get('color') == 'green':
            logger.info("Достигнут зеленый квадрат после 10-го чекпоинта -> плыву к красным чекпоинтам, пока не увижу фиолетовый.")
            # ВАЖНО: Сохраняем информацию о последнем красном чекпоинте перед переключением состояния
            # (если она есть), чтобы использовать ее для навигации, если красный квадрат не найден сразу
            logger.info(f"[GREEN_AFTER_10->RED_UNTIL_PURPLE] Последний красный чекпоинт в кэше: {self.last_red_checkpoint_center}")
            self.state = 'RED_UNTIL_PURPLE'
            _reset_for_new_state()
            return

        # ---- Красные до появления фиолетового ----
        if self.state == 'RED_UNTIL_PURPLE':
            # ВАЖНО: Переключение на PURPLE_FINAL при обнаружении фиолетового происходит в основном цикле (run),
            # а не здесь, чтобы переключаться сразу как только УВИДЕЛИ фиолетовый, а не ждать достижения.
            # Здесь обрабатываем только достижение красных чекпоинтов.
            if target['type'] == 'square' and target.get('color') == 'red':
                # ВАЖНО: check_target_reached уже проверил достижение цели и вернул True
                # Флаг target_reached_flag уже установлен выше в update_state, поэтому здесь
                # мы просто увеличиваем счетчик (не нужно проверять центр, т.к. миникарта динамическая)
                
                # Получаем минимальное расстояние для логирования
                min_distance_in_history = min(self.distance_history) if len(self.distance_history) > 0 else distance
                current_time = time.time()
                
                # НОВАЯ СИСТЕМА ПОДСЧЕТА (костыль для бага): каждый вызов add_checkpoint() = +1 внутренний
                # Из-за бага один физический чекпоинт вызывает add_checkpoint() 3 раза
                # Внешний счетчик компенсирует: каждые 3 вызова = 1 внешний (1 физический чекпоинт)
                if self.checkpoint_counter:
                    internal, external = self.checkpoint_counter.add_checkpoint()
                    self.red_squares_collected = external  # Для обратной совместимости логирования
                    logger.info(f"✓ Вызов add_checkpoint() (internal: {internal}, external: {external}, physical: {external}, фаза RED_UNTIL_PURPLE, мин. расстояние: {min_distance_in_history:.1f}px).")
                else:
                    # Старая система (fallback)
                    self.red_squares_collected += 1
                    logger.info(f"✓ Собран дополнительный красный чекпоинт #{self.red_squares_collected} во фазе RED_UNTIL_PURPLE (мин. расстояние: {min_distance_in_history:.1f}px, текущее: {distance:.1f}px).")
                
                self.last_collected_square_center = target['center']
                self._last_checkpoint_collected_time = current_time
                
                # ВАЖНО: Сохраняем центр засчитанного чекпоинта для проверки при исчезновении
                # чтобы не засчитывать его повторно при исчезновении
                self.last_red_checkpoint_center = target['center']
                self.last_red_checkpoint_distance = distance
                # Сбрасываем минимальное расстояние, чтобы при исчезновении не засчитывать повторно
                self.red_checkpoint_min_distance = None
                
                # Сбрасываем флаг, чтобы можно было собирать следующий чекпоинт
                self.target_reached_flag = False
            return

        # ---- Финальный блок: оранжевый -> розовый -> желтый -> красный, затем рестарт ----
        if self.state == 'PURPLE_FINAL' and target['type'] == 'square' and target.get('color') == 'purple':
            logger.info("Достигнут финальный фиолетовый квадрат -> плыву к финальному розовому.")
            self.state = 'P_FINAL'
            _reset_for_new_state()
            return

        if self.state == 'P_FINAL' and target['type'] == 'square' and target.get('color') == 'pink':
            logger.info("Достигнут финальный розовый квадрат -> плыву к финальному желтому.")
            self.state = 'Y_FINAL'
            _reset_for_new_state()
            return

        if self.state == 'Y_FINAL' and target['type'] == 'square' and target.get('color') == 'yellow':
            logger.info("Достигнут финальный желтый квадрат -> плыву к последнему красному чекпоинту.")
            self.state = 'RED_FINAL'
            _reset_for_new_state()
            return

        if self.state == 'RED_FINAL' and target['type'] == 'square' and target.get('color') == 'red':
            # ВАЖНО: check_target_reached уже проверил достижение цели и вернул True
            # Просто переключаем состояние на рестарт
            min_distance_in_history = min(self.distance_history) if len(self.distance_history) > 0 else distance
            logger.info(f"Достигнут финальный красный чекпоинт (мин. расстояние: {min_distance_in_history:.1f}px) -> рейс завершен, начинаю новый цикл.")
            
            # Сбрасываем отслеживание красного чекпоинта
            self.last_red_checkpoint_center = None
            self.last_red_checkpoint_distance = None
            self.red_checkpoint_min_distance = None
            
            # Полный сброс цикла
            self.state = 'Y1'
            self.red_squares_collected = 0  # Старый счетчик
            if self.checkpoint_counter:
                self.checkpoint_counter.reset()  # Сбрасываем новую систему подсчета
            self.last_collected_square_center = None
            _reset_for_new_state()
            return
    
    def check_special_conditions(self, minimap):
        """
        Проверяет специальные условия для переключения состояний
        (в новой логике специальных условий почти нет,
        основная развилка \"красные до оранжевого\" реализована прямо в get_current_target)
        """
        # На данный момент дополнительных специальных условий нет.
        return False
    
    def calculate_angle_to_target(self, player_angle, player_pos, target_pos):
        """
        Вычисляет угол от игрока к цели
        Учитывает, что карта может вращаться, но стрелка всегда указывает направление движения
        """
        dx = target_pos[0] - player_pos[0]
        dy = target_pos[1] - player_pos[1]
        
        # Угол к цели в градусах
        # В системе координат изображения: 0° = вправо, 90° = вниз
        # Переводим в систему: 0° = вверх, по часовой стрелке
        target_angle = math.atan2(dy, dx) * 180 / math.pi
        target_angle = (target_angle + 90) % 360
        
        # Разница углов (куда нужно повернуть)
        angle_diff = target_angle - player_angle
        
        # Нормализуем в диапазон [-180, 180]
        # Положительное значение = поворот вправо (D)
        # Отрицательное значение = поворот влево (A)
        if angle_diff > 180:
            angle_diff -= 360
        elif angle_diff < -180:
            angle_diff += 360
        
        return angle_diff
    
    def save_debug_minimap(self, minimap, player, target, angle_diff, distance, action):
        """Сохраняет скриншот миникарты с визуализацией расчетов"""
        if not self.save_debug_screenshots:
            return
        
        try:
            # Убеждаемся, что папка существует
            os.makedirs(self.debug_screenshot_dir, exist_ok=True)
            # Создаем копию для рисования
            debug_img = minimap.copy()
            
            # ВАЖНО: Определяем фактический центр игрока
            # Используем центр масс зеленой палочки, если доступен, иначе фиксированный центр миникарты
            actual_player_center = self.minimap_center  # По умолчанию
            if player['found'] and player.get('green_center') is not None:
                actual_player_center = player['green_center']
            
            # Рисуем центр игрока (белый круг) - используем фактический центр
            cv2.circle(debug_img, actual_player_center, 5, (255, 255, 255), -1)
            cv2.circle(debug_img, actual_player_center, 3, (0, 0, 0), -1)
            
            # Рисуем стрелку игрока
            if player['found']:
                # Красная точка (сзади)
                if player.get('red_point'):
                    cv2.circle(debug_img, player['red_point'], 4, (0, 0, 255), -1)
                
                # Зеленая палочка - задняя точка (дальняя точка)
                if player.get('green_point'):
                    cv2.circle(debug_img, player['green_point'], 3, (0, 200, 0), -1)  # Темно-зеленая точка для задней части
                
                # Рисуем направление игрока (зеленая линия) - ВАЖНО: должна проходить точно по центру игрока
                # Линия должна быть параллельна главной оси зеленой палочки и проходить через её центр масс
                if player.get('green_center') is not None:
                    green_center = player['green_center']
                    
                    # ВАЖНО: Используем ориентацию палочки (stick_angle) для визуализации
                    # Это гарантирует, что линия будет точно параллельна оси палочки
                    # Дальняя точка (зад) находится в направлении палочки, поэтому инвертируем на 180°
                    if player.get('stick_angle') is not None:
                        # Используем ориентацию палочки и инвертируем для направления движения
                        visual_angle = (player['stick_angle'] + 180) % 360
                        visual_angle_rad = math.radians(visual_angle)
                    elif player.get('angle') is not None:
                        # Запасной вариант: используем угол движения
                        visual_angle_rad = math.radians(player['angle'])
                    else:
                        visual_angle_rad = 0
                    
                    # Рисуем линию точно через центр палочки параллельно её оси
                    # ВАЖНО: Делаем линию короткой, по размеру иконки игрока, чтобы не перекрывать красный квадрат
                    line_length_forward = 12  # Короткая длина вперед (примерно размер иконки игрока)
                    line_length_back = 8      # Короткая длина назад
                    
                    # Вычисляем точки на линии, проходящей через центр палочки
                    forward_x = int(green_center[0] + line_length_forward * math.sin(visual_angle_rad))
                    forward_y = int(green_center[1] - line_length_forward * math.cos(visual_angle_rad))
                    
                    back_x = int(green_center[0] - line_length_back * math.sin(visual_angle_rad))
                    back_y = int(green_center[1] + line_length_back * math.cos(visual_angle_rad))
                    
                    # Рисуем короткую зеленую линию точно через центр палочки
                    # Эта линия проходит через центр масс палочки и параллельна её оси
                    # Делаем линию короткой, чтобы не перекрывать красный квадрат при приближении
                    cv2.line(debug_img, (back_x, back_y), (forward_x, forward_y), (0, 255, 0), 5)
                    
                    # Рисуем центр зеленой палочки для отладки
                    cv2.circle(debug_img, green_center, 3, (0, 255, 255), -1)  # Желтая точка для видимости центра
                elif player.get('angle') is not None:
                    # Запасной вариант: используем вычисленный угол от центра игрока
                    # ВАЖНО: Делаем линию короткой, по размеру иконки игрока
                    angle_rad = math.radians(player['angle'])
                    line_length = 12  # Короткая длина, по размеру иконки игрока
                    end_x = int(actual_player_center[0] + line_length * math.sin(angle_rad))
                    end_y = int(actual_player_center[1] - line_length * math.cos(angle_rad))
                    cv2.line(debug_img, actual_player_center, (end_x, end_y), (0, 255, 0), 3)
            
            # Рисуем цель (квадрат или круг)
            if target['found']:
                center = target['center']
                target_type = target.get('type', 'square')
                target_color = target.get('color', 'red')
                
                if target_type == 'square':
                    # Рисуем центр квадрата (желтый круг)
                    cv2.circle(debug_img, center, 6, (0, 255, 255), -1)
                    cv2.circle(debug_img, center, 4, (0, 200, 200), -1)
                    # Рисуем контур квадрата
                    if 'contour' in target and target['contour'] is not None:
                        cv2.drawContours(debug_img, [target['contour']], -1, (0, 255, 0), 2)
                else:
                    # Рисуем круг - цвет зависит от типа
                    if target_color == 'yellow':
                        circle_color = (0, 255, 255)  # Желтый
                    elif target_color == 'pink':
                        circle_color = (255, 0, 255)  # Розовый/Маджента
                    elif target_color == 'white':
                        circle_color = (255, 255, 255)  # Белый
                    elif target_color == 'orange':
                        circle_color = (0, 165, 255)  # Оранжевый
                    else:
                        circle_color = (255, 255, 255)  # По умолчанию белый
                    
                    # Рисуем круг
                    cv2.circle(debug_img, center, 8, circle_color, 2)
                    cv2.circle(debug_img, center, 6, circle_color, -1)
                    # Рисуем контур если есть
                    if 'contour' in target and target['contour'] is not None:
                        cv2.drawContours(debug_img, [target['contour']], -1, circle_color, 2)
            
            # НЕ рисуем направление к цели (синяя линия) - она может перекрывать квадрат
            # Вместо этого просто отмечаем центр квадрата желтым кругом
            # Вычисляем угол только для отладки, но не рисуем линию
            if target['found'] and player['found']:
                dx = target['center'][0] - actual_player_center[0]
                dy = target['center'][1] - actual_player_center[1]
                target_angle = math.atan2(dy, dx) * 180 / math.pi
                target_angle = (target_angle + 90) % 360
                # НЕ рисуем линию - она перекрывает квадрат
            
            # Добавляем текст с информацией
            y_offset = 20
            cv2.putText(debug_img, f"State: {self.state}", (10, y_offset), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            y_offset += 20
            # Отображаем счетчик чекпоинтов (новая система)
            if self.checkpoint_counter:
                internal = self.checkpoint_counter.get_internal()
                external = self.checkpoint_counter.get_external()
                remainder = internal % 3
                # Основная информация: ПОНЯТНО показываем что 3 вызова = 1 физический чекпоинт
                text = f"Checkpoints: {external} physical collected (bug: 1 physical = 3 calls, internal={internal}, remainder={remainder}/3)"
                cv2.putText(debug_img, text, (10, y_offset), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)  # Больше и ярче
                y_offset += 25
                # Пояснение для маршрута (внешний счетчик компенсирует баг)
                text2 = f"Route uses EXTERNAL: {external} (need 7 for GREEN, 10 for final) - compensates 3x bug"
                cv2.putText(debug_img, text2, (10, y_offset), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)  # Желтый цвет
                y_offset += 20
            # Старый формат (меньше и менее заметно, только для отладки)
            if hasattr(self, 'red_squares_collected'):
                cv2.putText(debug_img, f"Red Squares (old, deprecated): {self.red_squares_collected}/10", (10, y_offset), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.4, (128, 128, 128), 1)  # Серый, меньше
                y_offset += 18
            else:
                cv2.putText(debug_img, f"Red Squares (old, deprecated): 0/10", (10, y_offset), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.4, (128, 128, 128), 1)  # Серый, меньше
                y_offset += 18
            cv2.putText(debug_img, f"Action: {action}", (10, y_offset), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            y_offset += 20
            if player['found'] and player.get('angle') is not None:
                cv2.putText(debug_img, f"Player Angle: {player['angle']:.1f}deg", (10, y_offset), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                y_offset += 20
            if target['found']:
                target_type = target.get('type', 'unknown')
                target_color = target.get('color', 'unknown')
                cv2.putText(debug_img, f"Target: {target_type} ({target_color})", (10, y_offset), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
                y_offset += 20
                cv2.putText(debug_img, f"Angle Diff: {angle_diff:.1f}deg", (10, y_offset), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
                y_offset += 20
                cv2.putText(debug_img, f"Distance: {distance:.1f}px", (10, y_offset), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
            
            # Сохраняем скриншот (только каждые 0.5 секунды, чтобы не создавать слишком много файлов)
            current_time = time.time()
            if not hasattr(self, '_last_screenshot_time') or (current_time - self._last_screenshot_time) >= 0.5:
                timestamp = int(time.time() * 1000)
                filename = os.path.join(self.debug_screenshot_dir, f"minimap_{timestamp}.png")
                success = cv2.imwrite(filename, debug_img)
                if success:
                    if not hasattr(self, '_screenshot_logged'):
                        logger.info(f"Сохранен отладочный скриншот: {filename}")
                        self._screenshot_logged = True
                else:
                    logger.warning(f"Не удалось сохранить скриншот: {filename}")
                self._last_screenshot_time = current_time
            
        except Exception as e:
            logger.error(f"Ошибка сохранения отладочного скриншота: {e}", exc_info=True)
    
    def send_key_sendinput(self, key_char, press=True, ignore_pause=False):
        """Отправляет клавишу через SendInput (более надежно для игр)
        
        Args:
            key_char: Символ клавиши
            press: True для нажатия, False для отпускания
            ignore_pause: Если True, игнорирует проверку паузы (для освобождения клавиш)
        """
        if not WIN32_AVAILABLE:
            return False
        if not ignore_pause and self.paused:
            return False
        
        try:
            # Коды виртуальных клавиш
            VK_CODE = {
                'w': 0x57,
                'a': 0x41,
                'd': 0x44,
                's': 0x53
            }
            
            if key_char.lower() not in VK_CODE:
                return False
            
            vk_code = VK_CODE[key_char.lower()]
            
            # НЕ активируем окно - пользователь может свернуть игру, и бот не должен мешать
            # SendInput работает даже если окно не в фокусе
            
            # Используем SendInput для отправки клавиш
            extra = ctypes.c_ulong(0)
            ii_ = Input_I()
            ii_.ki = KeyBdInput(vk_code, 0, 0 if press else KEYEVENTF_KEYUP, 0, ctypes.pointer(extra))
            x = Input(INPUT_KEYBOARD, ii_)
            ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
            
            return True
        except Exception as e:
            logger.debug(f"Ошибка SendInput: {e}")
            return False
    
    def send_key_to_window(self, key_char, press=True):
        """Отправляет клавишу - пробует несколько методов"""
        if not WIN32_AVAILABLE or self.paused:
            return False
        
        # Пробуем SendInput (самый надежный)
        if self.send_key_sendinput(key_char, press):
            return True
        
        # Запасной вариант: PostMessage
        if self.window_handle:
            try:
                VK_CODE = {
                    'w': 0x57,
                    'a': 0x41,
                    'd': 0x44,
                    's': 0x53
                }
                
                if key_char.lower() not in VK_CODE:
                    return False
                
                vk_code = VK_CODE[key_char.lower()]
                WM_KEYDOWN = 0x0100
                WM_KEYUP = 0x0101
                
                if press:
                    win32api.PostMessage(self.window_handle, WM_KEYDOWN, vk_code, 0)
                else:
                    win32api.PostMessage(self.window_handle, WM_KEYUP, vk_code, 0)
                return True
            except:
                pass
        
        return False
    
    def control_boat(self, angle_diff, distance=None):
        """
        Управляет лодкой на основе разницы углов
        Всегда движется вперед (W), поворачивает при необходимости (A/D)
        
        Args:
            angle_diff: Разница угла между направлением игрока и целью
            distance: Расстояние до цели (опционально, для адаптивного порога)
        """
        # НЕ активируем окно постоянно - это мешает пользователю
        # PostMessage работает даже если окно не в фокусе

        # Логируем вызов control_boat для отладки (только периодически, чтобы не засорять лог)
        current_time = time.time()
        if not hasattr(self, '_last_control_boat_log') or (current_time - self._last_control_boat_log) >= 2.0:
            logger.debug(f"control_boat вызван: angle_diff={angle_diff:.1f}°, distance={distance:.1f}px if distance else None, W нажата={self.keys_pressed['w']}")
            self._last_control_boat_log = current_time
        
        # ВСЕГДА нажимаем W для движения вперед (и держим ее нажатой, пока бот не на паузе/не остановлен)
        try:
            # ВАЖНО: Нажимаем W каждый раз, когда control_boat вызывается (даже если флаг уже True)
            # Это гарантирует, что клавиша действительно нажата в игре, даже если она была отпущена
            # по какой-то причине (например, потеря фокуса окна, ошибка SendInput и т.д.)
            if not self.keys_pressed['w']:
                # Первый раз жмем W
                win32_success = self.send_key_to_window('w', press=True)
                try:
                    self.keyboard.press('w')
                except Exception:
                    pass
                self.keys_pressed['w'] = True
                self.keys_sent_count += 1
                logger.info(f"Нажата клавиша W для движения вперед (SendInput/PostMessage: {win32_success})")
            else:
                # W уже "нажата" по флагу, но периодически перенажимаем для надежности
                # (каждые 0.5 секунды) чтобы гарантировать, что клавиша действительно нажата
                current_time = time.time()
                if not hasattr(self, '_last_w_repeat') or (current_time - self._last_w_repeat) >= 0.5:
                    # Перенажимаем W для надежности
                    win32_success = self.send_key_to_window('w', press=True)
                    try:
                        self.keyboard.press('w')  # pynput тоже перенажимаем
                    except Exception:
                        pass
                    self._last_w_repeat = current_time
        except Exception as e:
            logger.error(f"Ошибка нажатия W: {e}", exc_info=True)
        
        # Определяем необходимость поворота с использованием гистерезиса для стабилизации
        abs_angle_diff = abs(angle_diff)
        
        # Адаптивный порог: если близко к цели, используем более точный порог
        base_threshold = self.turn_threshold
        # ВАЖНО: Проверяем, является ли текущая цель красным квадратом (через состояние)
        is_red_checkpoint = self.state in ['RED_1_7', 'RED_8', 'RED_9_10', 'RED_AFTER_GREEN7', 'RED_UNTIL_WHITE', 'RED_UNTIL_PURPLE', 'RED_FINAL']
        
        if distance is not None:
            if is_red_checkpoint:
                # Для красных чекпоинтов - ВСЕГДА максимально точный порог (0.1 градуса) независимо от расстояния
                # чтобы всегда следовать строго в центр без разбега
                base_threshold = 0.1  # МАКСИМАЛЬНО точный порог (0.1 градуса) для строгого следования в центр
            else:
                # Для других целей - адаптивный порог
                if distance < 5:  # ОЧЕНЬ близко к цели (< 5px) - используем максимально точный порог
                    base_threshold = 0.1  # МАКСИМАЛЬНО точный порог (0.1 градуса) для идеального наведения на центр
                elif distance < 10:  # Очень близко к цели (< 10px) - используем максимально точный порог
                    base_threshold = 0.2  # Очень точный порог (0.2 градуса) для идеального наведения на центр
                elif distance < 15:  # Близко к цели (< 15px) - используем очень точный порог
                    base_threshold = 0.3  # Очень точный порог (0.3 градуса)
                elif distance < 20:  # Близко к цели (< 20px) - используем точный порог
                    base_threshold = 0.5  # Точный порог (0.5 градуса)
                elif distance < self.close_distance_threshold:
                    # Близко к цели - используем более точный порог для точного наведения на центр
                    base_threshold = self.turn_threshold_close
                elif distance < 80:  # Средняя дистанция - используем средний порог
                    base_threshold = (self.turn_threshold + self.turn_threshold_close) / 2
        
        # Гистерезис: если уже поворачиваем, требуем меньший угол для остановки
        # Если не поворачиваем, требуем больший угол для начала поворота
        # ВАЖНО: Для красных чекпоинтов используем минимальный гистерезис для максимальной точности
        is_red_checkpoint = self.state in ['RED_1_7', 'RED_8', 'RED_9_10', 'RED_AFTER_GREEN7', 'RED_UNTIL_WHITE', 'RED_UNTIL_PURPLE', 'RED_FINAL']
        
        if is_red_checkpoint:
            # Для красных чекпоинтов - минимальный гистерезис для максимальной точности
            hysteresis = 0.02
        elif base_threshold < 0.5:
            # МАКСИМАЛЬНО точное наведение - используем минимальный гистерезис
            hysteresis = 0.05
        elif base_threshold < 1.0:
            # Очень точное наведение - используем минимальный гистерезис
            hysteresis = 0.1
        else:
            hysteresis = self.turn_hysteresis
        
        if self.current_turn_direction is not None:
            # Уже поворачиваем - используем меньший порог для остановки (порог - гистерезис)
            threshold = base_threshold - hysteresis
            if is_red_checkpoint:
                threshold = max(0.01, threshold)  # Для красных чекпоинтов минимум 0.01 градуса
            else:
                threshold = max(0.05, threshold)  # Минимум 0.05 градуса для МАКСИМАЛЬНО точного наведения
        else:
            # Не поворачиваем - используем больший порог для начала (порог + гистерезис)
            threshold = base_threshold + hysteresis
        
        # Определяем, выровнен ли бот (угол очень маленький)
        ALIGNED_ANGLE_THRESHOLD = 2.0  # Порог для выравнивания (градусы)
        self._is_aligned = abs_angle_diff < ALIGNED_ANGLE_THRESHOLD
        
        # Проверяем, пройдена ли цель (расстояние увеличивается)
        is_passed = False
        if distance is not None and len(self.distance_history) >= 3:
            # Если последние расстояния увеличиваются, цель пройдена
            recent_distances = self.distance_history[-3:]
            if recent_distances[0] < recent_distances[1] < recent_distances[2]:
                is_passed = True
        
        try:
            # ВАЖНО: Для RED_8 и больших углов (цель сзади) используем более агрессивный поворот
            # Если угол больше 90 градусов, это значит цель сзади - нужно поворачиваться быстрее
            is_large_angle = abs_angle_diff > 90
            is_red_8 = self.state == 'RED_8'
            
            if abs_angle_diff > threshold:
                # Определяем, использовать ли точечные нажатия или зажатие
                # Точечные нажатия: когда бот выровнен (маленький угол) И цель не пройдена
                # Зажатие: когда угол большой (не выровнен) ИЛИ цель пройдена ИЛИ это RED_8 с большим углом
                use_tap_mode = self._is_aligned and not is_passed and not (is_red_8 and is_large_angle)
                
                # Определяем направление поворота
                if angle_diff > 0:
                    # Поворачиваем вправо (D) - цель справа от направления движения
                    if use_tap_mode:
                        # Точечные нажатия для точной корректировки
                        key = 'd'
                        current_time = time.time()
                        # Нажимаем точечно каждые 0.1 секунды
                        if key not in self._last_tap_time or (current_time - self._last_tap_time[key]) >= 0.1:
                            # Отпускаем противоположную клавишу, если нажата
                            if self.keys_pressed['a']:
                                try:
                                    self.send_key_to_window('a', press=False)
                                    self.keyboard.release('a')
                                except:
                                    pass
                                self.keys_pressed['a'] = False
                            
                            # Точечное нажатие: нажали и сразу отпустили
                            try:
                                self.send_key_to_window('d', press=True)
                                self.keyboard.press('d')
                                time.sleep(0.02)  # Очень короткое нажатие
                                self.send_key_to_window('d', press=False)
                                self.keyboard.release('d')
                            except:
                                pass
                            self.keys_pressed['d'] = False  # Не держим клавишу
                            self._last_tap_time[key] = current_time
                            self.current_turn_direction = 'right'
                    elif self.current_turn_direction != 'right':
                        # Меняем направление или начинаем поворот
                        if self.keys_pressed['a']:
                            try:
                                self.send_key_to_window('a', press=False)
                                self.keyboard.release('a')
                            except:
                                pass
                            time.sleep(0.01)
                            self.keys_pressed['a'] = False
                        if not self.keys_pressed['d']:
                            try:
                                self.send_key_to_window('d', press=True)
                                self.keyboard.press('d')
                            except:
                                pass
                            self.keys_pressed['d'] = True
                        self.current_turn_direction = 'right'
                    elif not self.keys_pressed['d']:
                        # Продолжаем поворот вправо
                        try:
                            self.send_key_to_window('d', press=True)
                            self.keyboard.press('d')
                        except:
                            pass
                        self.keys_pressed['d'] = True
                else:
                    # Поворачиваем влево (A) - цель слева от направления движения
                    if use_tap_mode:
                        # Точечные нажатия для точной корректировки
                        key = 'a'
                        current_time = time.time()
                        # Нажимаем точечно каждые 0.1 секунды
                        if key not in self._last_tap_time or (current_time - self._last_tap_time[key]) >= 0.1:
                            # Отпускаем противоположную клавишу, если нажата
                            if self.keys_pressed['d']:
                                try:
                                    self.send_key_to_window('d', press=False)
                                    self.keyboard.release('d')
                                except:
                                    pass
                                self.keys_pressed['d'] = False
                            
                            # Точечное нажатие: нажали и сразу отпустили
                            try:
                                self.send_key_to_window('a', press=True)
                                self.keyboard.press('a')
                                time.sleep(0.02)  # Очень короткое нажатие
                                self.send_key_to_window('a', press=False)
                                self.keyboard.release('a')
                            except:
                                pass
                            self.keys_pressed['a'] = False  # Не держим клавишу
                            self._last_tap_time[key] = current_time
                            self.current_turn_direction = 'left'
                    elif self.current_turn_direction != 'left':
                        # Меняем направление или начинаем поворот
                        if self.keys_pressed['d']:
                            try:
                                self.send_key_to_window('d', press=False)
                                self.keyboard.release('d')
                            except:
                                pass
                            time.sleep(0.01)
                            self.keys_pressed['d'] = False
                        if not self.keys_pressed['a']:
                            try:
                                self.send_key_to_window('a', press=True)
                                self.keyboard.press('a')
                            except:
                                pass
                            self.keys_pressed['a'] = True
                        self.current_turn_direction = 'left'
                    elif not self.keys_pressed['a']:
                        # Продолжаем поворот влево
                        try:
                            self.send_key_to_window('a', press=True)
                            self.keyboard.press('a')
                        except:
                            pass
                        self.keys_pressed['a'] = True
            else:
                # Угол недостаточен для поворота - двигаемся прямо
                if self.current_turn_direction is not None:
                    # Останавливаем поворот только если угол стал достаточно маленьким
                    if self.keys_pressed['a']:
                        try:
                            self.send_key_to_window('a', press=False)
                            self.keyboard.release('a')
                        except:
                            pass
                        time.sleep(0.01)
                        self.keys_pressed['a'] = False
                    if self.keys_pressed['d']:
                        try:
                            self.send_key_to_window('d', press=False)
                            self.keyboard.release('d')
                        except:
                            pass
                        time.sleep(0.01)
                        self.keys_pressed['d'] = False
                    self.current_turn_direction = None
                    self._is_aligned = True  # Бот выровнен
        except Exception as e:
            logger.error(f"Ошибка управления поворотом: {e}", exc_info=True)
    
    def _setup_keyboard_hook(self):
        """Устанавливает низкоуровневый хук клавиатуры для перехвата Insert"""
        if not WIN32_AVAILABLE:
            return
        
        # Используем замыкание для доступа к self
        bot_instance = self
        
        # Callback функция для хука
        def low_level_keyboard_proc(nCode, wParam, lParam):
            try:
                if nCode >= HC_ACTION:
                    # Получаем структуру с информацией о клавише
                    kbd = ctypes.cast(lParam, ctypes.POINTER(KBDLLHOOKSTRUCT)).contents
                    
                    # Проверяем Insert (VK_INSERT = 45)
                    if kbd.vkCode == VK_INSERT:
                        current_time = time.time()
                        logger.info(f"Хук: Insert обнаружен, wParam={wParam}")
                        
                        # Обрабатываем только нажатие (не отпускание)
                        if wParam == WM_KEYDOWN or wParam == WM_SYSKEYDOWN:
                            # Защита от повторных срабатываний (debounce)
                            if not bot_instance.insert_pressed or (current_time - bot_instance.insert_press_time) > 0.3:
                                bot_instance.insert_pressed = True
                                bot_instance.insert_press_time = current_time
                                
                                # Переключаем паузу в отдельном потоке
                                def toggle_pause():
                                    try:
                                        logger.info("Insert нажат! Переключаю паузу...")
                                        with bot_instance.pause_lock:
                                            bot_instance.paused = not bot_instance.paused
                                            if bot_instance.paused:
                                                logger.info("=== БОТ ПРИОСТАНОВЛЕН ===")
                                                bot_instance.stop_boat()
                                            else:
                                                logger.info("=== БОТ ВОЗОБНОВЛЕН ===")
                                    except Exception as e:
                                        logger.error(f"Ошибка в toggle_pause: {e}", exc_info=True)
                                
                                # Запускаем в отдельном потоке чтобы не блокировать хук
                                threading.Thread(target=toggle_pause, daemon=True).start()
                                
                                # НЕ блокируем клавишу - пусть проходит в игру тоже
                                # Возвращаем CallNextHookEx чтобы клавиша прошла дальше
                        elif wParam == WM_KEYUP or wParam == WM_SYSKEYUP:
                            bot_instance.insert_pressed = False
                            # НЕ блокируем клавишу - пусть проходит в игру тоже
                
                # Для всех остальных клавиш передаем дальше
                return ctypes.windll.user32.CallNextHookExW(bot_instance.keyboard_hook, nCode, wParam, lParam)
            except Exception as e:
                logger.error(f"Ошибка в хуке клавиатуры: {e}", exc_info=True)
                # В случае ошибки все равно передаем дальше
                return ctypes.windll.user32.CallNextHookExW(bot_instance.keyboard_hook, nCode, wParam, lParam)
        
        # Оборачиваем callback в правильный тип HOOKPROC
        self._hook_proc = HOOKPROC(low_level_keyboard_proc)
        
        # Устанавливаем хук (используем сохраненный callback)
        self.keyboard_hook = ctypes.windll.user32.SetWindowsHookExW(
            WH_KEYBOARD_LL,
            self._hook_proc,
            ctypes.windll.kernel32.GetModuleHandleW(None),
            0
        )
        
        if not self.keyboard_hook:
            error_code = ctypes.windll.kernel32.GetLastError()
            raise Exception(f"Не удалось установить хук клавиатуры. Код ошибки: {error_code}")
        else:
            logger.info(f"Низкоуровневый хук клавиатуры успешно установлен (handle: {self.keyboard_hook})")
    
    def _cleanup_keyboard_hook(self):
        """Удаляет хук клавиатуры"""
        if self.keyboard_hook and self.keyboard_hook != 0 and WIN32_AVAILABLE:
            try:
                ctypes.windll.user32.UnhookWindowsHookExW(self.keyboard_hook)
                self.keyboard_hook = 0
            except Exception as e:
                logger.error(f"Ошибка удаления хука: {e}")
    
    def stop_boat(self, release_w=True):
        """Останавливает лодку - освобождает нажатые клавиши.
        
        Args:
            release_w: если True, отпускаем W, иначе оставляем W зажатой.
        """
        # Освобождаем W (по желанию)
        if release_w and self.keys_pressed['w']:
            # Отправляем событие отпускания через SendInput (ignore_pause=True чтобы освободить даже на паузе)
            if WIN32_AVAILABLE:
                try:
                    self.send_key_sendinput('w', press=False, ignore_pause=True)
                except:
                    pass
            # Также освобождаем через pynput
            try:
                self.keyboard.release('w')
            except:
                pass
            self.keys_pressed['w'] = False
        
        # Освобождаем A
        if self.keys_pressed['a']:
            # Отправляем событие отпускания через SendInput
            if WIN32_AVAILABLE:
                try:
                    self.send_key_sendinput('a', press=False, ignore_pause=True)
                except:
                    pass
            # Также освобождаем через pynput
            try:
                self.keyboard.release('a')
            except:
                pass
            self.keys_pressed['a'] = False
        
        # Освобождаем D
        if self.keys_pressed['d']:
            # Отправляем событие отпускания через SendInput
            if WIN32_AVAILABLE:
                try:
                    self.send_key_sendinput('d', press=False, ignore_pause=True)
                except:
                    pass
            # Также освобождаем через pynput
            try:
                self.keyboard.release('d')
            except:
                pass
            self.keys_pressed['d'] = False
        
        # Небольшая задержка чтобы система успела обработать события отпускания
        time.sleep(0.05)
    
    def run(self):
        """Основной цикл бота"""
        logger.info("Запуск бота...")
        logger.info("Нажмите 'q' для остановки")
        logger.info("Нажмите 'Insert' для паузы/возобновления (работает в игре)")
        
        self.running = True
        self.paused = False
        
        # Запускаем слушатель клавиатуры для остановки (q) и паузы (Insert)
        def on_press(key):
            try:
                if key.char == 'q':
                    self.running = False
                    logger.info("Остановка бота...")
            except AttributeError:
                # Обрабатываем специальные клавиши (Insert, F-клавиши и т.д.)
                # В pynput Insert может быть как Key.insert, так и key.name == 'insert'
                is_insert = False
                if key == Key.insert:
                    is_insert = True
                elif hasattr(key, 'name') and key.name == 'insert':
                    is_insert = True
                
                if is_insert:
                    # Переключаем паузу
                    try:
                        logger.info("Insert нажат через pynput! Переключаю паузу...")
                        with self.pause_lock:
                            self.paused = not self.paused
                            if self.paused:
                                logger.info("=== БОТ ПРИОСТАНОВЛЕН ===")
                                # При паузе отпускаем все клавиши, включая W
                                self.stop_boat(release_w=True)
                            else:
                                logger.info("=== БОТ ВОЗОБНОВЛЕН ===")
                    except Exception as e:
                        logger.error(f"Ошибка в toggle_pause через pynput: {e}", exc_info=True)
                pass
        
        listener = Listener(on_press=on_press)
        listener.start()
        
        # Устанавливаем низкоуровневый хук Windows для Insert (более надежный способ)
        if WIN32_AVAILABLE:
            try:
                self._setup_keyboard_hook()
                logger.info("Низкоуровневый хук клавиатуры установлен (Windows Hook)")
            except Exception as e:
                logger.error(f"Ошибка установки низкоуровневого хука: {e}", exc_info=True)
                logger.warning("Низкоуровневый хук не установлен. Используется keyboard.add_hotkey")
        
        # Регистрируем глобальный хоткей Insert для паузы/возобновления (резервный способ)
        if KEYBOARD_AVAILABLE:
            pause_lock = threading.Lock()
            
            def toggle_pause():
                """Переключает состояние паузы"""
                try:
                    logger.info("Insert нажат! Переключаю паузу...")
                    with pause_lock:
                        self.paused = not self.paused
                        if self.paused:
                            logger.info("=== БОТ ПРИОСТАНОВЛЕН ===")
                            # При паузе отпускаем все клавиши, включая W
                            self.stop_boat(release_w=True)
                        else:
                            logger.info("=== БОТ ВОЗОБНОВЛЕН ===")
                except Exception as e:
                    logger.error(f"Ошибка в toggle_pause: {e}", exc_info=True)
            
            try:
                # Используем keyboard.add_hotkey - самый надежный способ для глобальных хоткеев
                # suppress=False чтобы клавиша проходила в игру тоже (но хоткей сработает)
                keyboard.add_hotkey('insert', toggle_pause, suppress=False)
                logger.info("Глобальный хоткей Insert зарегистрирован (keyboard.add_hotkey)")
            except Exception as e:
                logger.error(f"Ошибка установки хука клавиатуры: {e}", exc_info=True)
                logger.warning("Insert может не работать. Попробуйте запустить от имени администратора.")
        else:
            logger.warning("Библиотека keyboard не установлена. Insert не будет работать.")
            logger.warning("Установите: pip install keyboard")
        
        consecutive_errors = 0
        
        try:
            while self.running:
                # Измеряем время кадра для статистики
                frame_start = time.time()
                
                # Проверяем состояние паузы
                if self.paused:
                    time.sleep(0.1)
                    continue
                
                # Захватываем миникарту
                minimap = self.capture_minimap()
                
                if minimap is None:
                    # Если окно минимизировано, отпускаем поворотные клавиши, W оставляем зажатой
                    self.stop_boat(release_w=False)
                    consecutive_errors += 1
                    if consecutive_errors >= MAX_CONSECUTIVE_ERRORS:
                        logger.error("Слишком много ошибок захвата. Остановка.")
                        break
                    # Не логируем каждую ошибку, чтобы не засорять лог
                    if consecutive_errors % 10 == 0:
                        logger.warning(f"Окно игры минимизировано или недоступно ({consecutive_errors} раз)")
                    time.sleep(ERROR_RETRY_DELAY)
                    continue
                
                # Находим стрелочку игрока
                player = self.find_player_arrow(minimap)
                if not player['found']:
                    self.consecutive_arrow_errors += 1
                    
                    # Сохраняем скриншот для отладки, если включено
                    if self.save_debug_screenshots and self.consecutive_arrow_errors % 10 == 0:
                        debug_path = os.path.join(self.debug_screenshot_dir, f"arrow_not_found_{int(time.time())}.png")
                        cv2.imwrite(debug_path, minimap)
                        logger.debug(f"Сохранен отладочный скриншот: {debug_path}")
                    
                    # Если есть последний валидный угол, используем его
                    if self.last_valid_angle is not None and self.consecutive_arrow_errors < 20:
                        # Используем последний валидный угол
                        player = {
                            'found': True,
                            'angle': self.last_valid_angle
                        }
                        if self.consecutive_arrow_errors % 10 == 0:  # Логируем каждые 10 ошибок
                            logger.warning(f"Стрелочка игрока не найдена ({self.consecutive_arrow_errors} раз). Использую последний валидный угол: {self.last_valid_angle:.1f}°")
                    else:
                        if self.consecutive_arrow_errors >= MAX_ARROW_ERRORS:
                            logger.error(f"Не удается найти игрока длительное время ({self.consecutive_arrow_errors} ошибок). Остановка.")
                            break
                        if self.consecutive_arrow_errors % 5 == 0:  # Логируем каждые 5 ошибок
                            logger.warning(f"Стрелочка игрока не найдена ({self.consecutive_arrow_errors} раз)")
                        time.sleep(ERROR_RETRY_DELAY)
                        continue
                else:
                    # Стрелочка найдена - сохраняем угол и сбрасываем счетчик
                    self.last_valid_angle = player['angle']
                    self.consecutive_arrow_errors = 0
                
                # Сохраняем позицию игрока для использования в других методах
                player_pos = self.minimap_center
                if player.get('green_center') is not None:
                    player_pos = player['green_center']
                self.last_player_pos = player_pos
                
                # Проверяем специальные условия (например, оранжевый круг при движении к 11-му квадрату)
                self.check_special_conditions(minimap)
                
                # КРИТИЧНО: Автоматическое увеличение счетчика до 8 через 5 секунд после достижения зеленого квадрата
                # Это костыль для бага, когда 8-й чекпоинт не засчитывается
                if self._green_square_reached_time > 0 and self.checkpoint_counter:
                    current_time = time.time()
                    time_since_green = current_time - self._green_square_reached_time
                    external_count = self.checkpoint_counter.get_external()
                    
                    # Если прошло 5 секунд после достижения зеленого и счетчик все еще на 7
                    if time_since_green >= 5.0 and external_count == 7:
                        logger.warning(f"[AUTO FIX] Прошло {time_since_green:.1f}с после достижения зеленого квадрата, счетчик на 7 -> принудительно увеличиваю до 8 (костыль для бага)")
                        # Принудительно увеличиваем счетчик до 8
                        # Вызываем add_checkpoint() 3 раза, чтобы внешний счетчик увеличился на 1
                        for i in range(3):
                            self.checkpoint_counter.add_checkpoint()
                        new_external = self.checkpoint_counter.get_external()
                        logger.info(f"[AUTO FIX] ✓ Счетчик принудительно увеличен до {new_external} (было 7)")
                        self._green_square_reached_time = 0  # Сбрасываем, чтобы не делать повторно
                
                # Определяем текущую цель на основе состояния
                target = self.get_current_target(minimap, player)
                
                # ВАЖНО: Специальная логика для RED_UNTIL_WHITE - проверяем наличие белого на карте каждый кадр
                # независимо от текущей цели. Если белый появился - сразу переключаемся на W1.
                if self.state == 'RED_UNTIL_WHITE':
                    # Ищем белый квадрат на карте независимо от того, что вернул get_current_target
                    white_square = self.find_colored_square(minimap, 'white')
                    if white_square['found']:
                        logger.info("В состоянии RED_UNTIL_WHITE обнаружен белый квадрат на карте -> сразу переключаюсь на W1 (забываю красные чекпоинты).")
                        self.state = 'W1'
                        self.last_circle_center = None
                        self.last_circle_distance = None
                        self.min_distance_to_target = None
                        self.distance_history = []
                        self.target_reached_flag = False
                        # Теперь get_current_target вернет белый как цель (так как состояние уже W1)
                        target = self.get_current_target(minimap, player)
                        if not target['found']:
                            logger.warning("После переключения на W1 белый квадрат не найден. Ожидание...")
                            time.sleep(TARGET_NOT_FOUND_DELAY)
                            continue
                        # ВАЖНО: После переключения на W1 мы получили новую цель (белый),
                        # теперь нужно продолжить обработку этой новой цели, а не старой (красный)
                        # Поэтому мы НЕ делаем continue здесь, а продолжаем выполнение с новой целью
                
                # ВАЖНО: Специальная логика для RED_UNTIL_PURPLE - проверяем наличие фиолетового на карте каждый кадр
                # независимо от текущей цели. Если фиолетовый появился - сразу переключаемся на PURPLE_FINAL.
                if self.state == 'RED_UNTIL_PURPLE':
                    # Ищем фиолетовый квадрат на карте независимо от того, что вернул get_current_target
                    purple_square = self.find_colored_square(minimap, 'purple')
                    if purple_square['found']:
                        logger.info("В состоянии RED_UNTIL_PURPLE обнаружен фиолетовый квадрат на карте -> сразу переключаюсь на PURPLE_FINAL (забываю красные чекпоинты).")
                        self.state = 'PURPLE_FINAL'
                        self.last_circle_center = None
                        self.last_circle_distance = None
                        self.min_distance_to_target = None
                        self.distance_history = []
                        self.target_reached_flag = False
                        # Теперь get_current_target вернет фиолетовый как цель (так как состояние уже PURPLE_FINAL)
                        target = self.get_current_target(minimap, player)
                        if not target['found']:
                            logger.warning("После переключения на PURPLE_FINAL фиолетовый квадрат не найден. Ожидание...")
                            time.sleep(TARGET_NOT_FOUND_DELAY)
                            continue
                        # ВАЖНО: После переключения на PURPLE_FINAL мы получили новую цель (фиолетовый),
                        # теперь нужно продолжить обработку этой новой цели, а не старой (красный)
                        # Поэтому мы НЕ делаем continue здесь, а продолжаем выполнение с новой целью
                
                    # Если цель не найдена, используем кэш для продолжения движения
                    if not target['found']:
                        # СПЕЦИАЛЬНАЯ ЛОГИКА ДЛЯ КРАСНЫХ ЧЕКПОИНТОВ:
                        # Если мы собираем красные чекпоинты и красный квадрат пропал,
                        # проверяем, были ли мы близко к нему - если да, засчитываем чекпоинт
                        if self.state in ['RED_1_7', 'RED_8', 'RED_9_10', 'RED_AFTER_GREEN7', 'RED_UNTIL_O', 'RED_UNTIL_WHITE', 'RED_UNTIL_PURPLE', 'RED_FINAL']:
                            if self.last_red_checkpoint_center is not None and self.red_checkpoint_min_distance is not None:
                                # Проверяем, были ли мы достаточно близко к красному чекпоинту перед его исчезновением
                                close_threshold = 5.0  # Порог близости для засчитывания чекпоинта (5px)
                                
                                # ВАЖНО: Проверяем, не был ли уже засчитан этот чекпоинт при достижении
                                # Если _checkpoint_counted_at_reach = True, значит чекпоинт уже был засчитан при достижении
                                # - не засчитываем повторно при исчезновении
                                if self._checkpoint_counted_at_reach:
                                    logger.info(f"[RED] Чекпоинт уже был засчитан при достижении, пропускаю засчитывание при исчезновении.")
                                    # Сбрасываем отслеживание
                                    self.last_red_checkpoint_center = None
                                    self.last_red_checkpoint_distance = None
                                    self.red_checkpoint_min_distance = None
                                    # Сбрасываем флаг засчитанного при достижении
                                    self._checkpoint_counted_at_reach = False
                                    # Ищем новый красный квадрат для продолжения
                                    new_red_square = self.find_red_square(minimap)
                                    if new_red_square['found']:
                                        target = new_red_square
                                        continue
                                    else:
                                        # Новый квадрат не найден - продолжаем без цели
                                        continue
                                
                                # Если чекпоинт не был засчитан при достижении, проверяем минимальное расстояние
                                if not self._checkpoint_counted_at_reach and self.red_checkpoint_min_distance is not None and self.red_checkpoint_min_distance < close_threshold:
                                    # Были близко к чекпоинту - проверяем, появился ли новый красный квадрат
                                    new_red_square = self.find_red_square(minimap)
                                    
                                    if new_red_square['found']:
                                        # Проверяем, что это действительно новый квадрат (не тот же самый)
                                        dx = new_red_square['center'][0] - self.last_red_checkpoint_center[0]
                                        dy = new_red_square['center'][1] - self.last_red_checkpoint_center[1]
                                        square_distance = math.sqrt(dx * dx + dy * dy)
                                        
                                        if square_distance > 30:  # Это новый квадрат (расстояние между центрами > 30px)
                                            # Чекпоинт получен! Засчитываем его
                                            # ВАЖНО: Задержка 1.5 секунды проверяется только при достижении,
                                            # при исчезновении засчитываем если чекпоинт не был засчитан при достижении
                                            logger.info(f"✓ Красный чекпоинт исчез после близкого прохождения (мин. расстояние: {self.red_checkpoint_min_distance:.2f}px), появился новый -> засчитываю чекпоинт.")
                                            
                                            # Создаем фиктивную цель для засчитывания чекпоинта
                                            fake_target = {
                                                'found': True,
                                                'center': self.last_red_checkpoint_center,
                                                'type': 'square',
                                                'color': 'red',
                                                'contour': None
                                            }
                                            
                                            # Увеличиваем счетчик через update_state
                                            self.update_state(fake_target, self.red_checkpoint_min_distance, player)
                                            
                                            # Сбрасываем отслеживание красного чекпоинта
                                            self.last_red_checkpoint_center = None
                                            self.last_red_checkpoint_distance = None
                                            self.red_checkpoint_min_distance = None
                                            # Сбрасываем флаг засчитанного при достижении
                                            self._checkpoint_counted_at_reach = False
                                            
                                            # Продолжаем с новым красным квадратом
                                            target = new_red_square
                                            continue
                                elif not self._checkpoint_counted_at_reach:
                                    # Новый красный квадрат не появился - возможно мы еще не достигли чекпоинт
                                    # Но если мы были очень близко и начали отдаляться - это может быть пропуск мимо
                                    if self.last_red_checkpoint_distance is not None:
                                        current_distance_to_last = math.sqrt(
                                            (self.last_red_checkpoint_center[0] - player_pos[0])**2 +
                                            (self.last_red_checkpoint_center[1] - player_pos[1])**2
                                        )
                                        
                                        # Если мы отдаляемся от чекпоинта и были близко - возможно пропустили
                                        # УВЕЛИЧИВАЕМ порог отдаления до 20px, так как при исчезновении расстояние может быть 11-15px
                                        if current_distance_to_last > self.last_red_checkpoint_distance + 20:
                                            logger.warning(f"⚠ Красный чекпоинт пропал, но мы отдаляемся (было {self.last_red_checkpoint_distance:.1f}px, стало {current_distance_to_last:.1f}px, разница: {current_distance_to_last - self.last_red_checkpoint_distance:.1f}px). Возможно пропустили мимо.")
                                            # Не засчитываем - возможно пропустили мимо
                                            self.last_red_checkpoint_center = None
                                            self.last_red_checkpoint_distance = None
                                            self.red_checkpoint_min_distance = None
                                        else:
                                            # Мы не отдаляемся значительно - возможно чекпоинт просто исчез
                                            logger.debug(f"[RED CHECKPOINT] Чекпоинт пропал, но мы не отдаляемся значительно (было {self.last_red_checkpoint_distance:.1f}px, стало {current_distance_to_last:.1f}px). Ждем появления нового.")
                    
                    # ВАЖНО: Проверяем, не достигли ли мы цель (были очень близко, но цель потеряна)
                    # Это происходит когда бот проплывает через круг и теряет его
                    # Увеличено до 30px чтобы учитывать случаи когда круг теряется из-за перекрытия иконкой
                    if self.min_distance_to_target is not None and self.min_distance_to_target < 30:
                        # Были очень близко к цели (менее 30px) - считаем что достигли
                        logger.info(f"Цель потеряна, но были очень близко (мин. расстояние: {self.min_distance_to_target:.1f}px). Считаю что достигли цель.")
                        # Создаем фиктивную цель для переключения состояния
                        fake_target = {
                            'found': True,
                            'center': player_pos,
                            'type': 'square',
                            'color': 'red' if self.state in ['RED_1_7', 'RED_9_10', 'RED_AFTER_GREEN7', 'RED_UNTIL_WHITE', 'RED_UNTIL_PURPLE', 'RED_FINAL'] else None,
                            'contour': None
                        }
                        self.update_state(fake_target, self.min_distance_to_target, player)
                        self.min_distance_to_target = None
                        time.sleep(0.1)
                        continue
                    else:
                        # Не были близко - просто ждем, поворотные клавиши отпускаем, W держим
                        logger.info(f"Цель не найдена (состояние: {self.state}). Ожидание...")
                        self.stop_boat(release_w=False)
                        self.min_distance_to_target = None
                        time.sleep(TARGET_NOT_FOUND_DELAY)
                        continue
                
                # Цель найдена - обрабатываем её
                if target['found']:
                    consecutive_errors = 0
                    self.consecutive_arrow_errors = 0
                    
                    # Вычисляем расстояние до цели
                    dx = target['center'][0] - player_pos[0]
                    dy = target['center'][1] - player_pos[1]
                    distance = math.sqrt(dx*dx + dy*dy)
                    
                    # Отслеживаем минимальное расстояние до цели
                    if self.min_distance_to_target is None or distance < self.min_distance_to_target:
                        self.min_distance_to_target = distance
                    
                    # Обновляем состояние на основе достижения цели (используем оригинальную цель)
                    # ВАЖНО: Для RED_UNTIL_PURPLE мы уже переключились выше, если увидели фиолетовый
                    self.update_state(target, distance, player)
                    
                    # ВАЖНО: Отслеживаем красные чекпоинты для логики засчитывания при пропадании
                    if target.get('color') == 'red' and target.get('type') == 'square':
                        if self.state in ['RED_1_7', 'RED_9_10', 'RED_AFTER_GREEN7', 'RED_UNTIL_WHITE', 'RED_UNTIL_PURPLE', 'RED_FINAL']:
                            # ВАЖНО: Обновляем центр последнего видимого красного чекпоинта ТОЛЬКО если он еще не был засчитан при достижении
                            # Если чекпоинт уже был засчитан при достижении (_checkpoint_counted_at_reach = True),
                            # не обновляем last_red_checkpoint_center, чтобы при исчезновении можно было правильно проверить
                            if not self._checkpoint_counted_at_reach:
                                # Обновляем центр последнего видимого красного чекпоинта
                                self.last_red_checkpoint_center = target['center']
                                self.last_red_checkpoint_distance = distance
                                
                                # Обновляем минимальное расстояние до красного чекпоинта
                                if self.red_checkpoint_min_distance is None or distance < self.red_checkpoint_min_distance:
                                    old_min = self.red_checkpoint_min_distance
                                    self.red_checkpoint_min_distance = distance
                                    if old_min is None or distance < old_min:
                                        logger.debug(f"[RED CHECKPOINT] Обновлено мин. расстояние: {old_min if old_min is not None else 'None'}px -> {distance:.2f}px")
                    
                    # Вычисляем относительный угол к цели (для поворота)
                    angle_diff = self.calculate_angle_to_target(
                        player['angle'],
                        player_pos,
                        target['center']  # Используем центр цели для навигации
                    )
                    
                    # Сохраняем относительный угол к цели
                    self.last_target_angle = angle_diff
                    
                    # Отслеживаем историю расстояний для определения кружения
                    self.last_distances.append(distance)
                    if len(self.last_distances) > 10:
                        self.last_distances.pop(0)
                    
                    # Проверяем, не кружим ли мы вокруг цели
                    is_circling = False
                    if len(self.last_distances) >= 5:
                        recent_distances = self.last_distances[-5:]
                        min_dist = min(recent_distances)
                        max_dist = max(recent_distances)
                        if max_dist - min_dist < 5 and distance > 10:
                            is_circling = True
                            logger.debug(f"Обнаружено кружение вокруг цели (расстояние стабильное: {distance:.1f}px)")
                    
                    # Если кружим, сбрасываем направление поворота
                    if is_circling:
                        if self.current_turn_direction is not None:
                            if self.keys_pressed['a']:
                                if not self.send_key_to_window('a', press=False):
                                    self.keyboard.release('a')
                                self.keys_pressed['a'] = False
                            if self.keys_pressed['d']:
                                if not self.send_key_to_window('d', press=False):
                                    self.keyboard.release('d')
                                self.keys_pressed['d'] = False
                            self.current_turn_direction = None
                            logger.debug("Сброшено направление поворота из-за кружения")
                    
                    # Логируем информацию
                    current_time = time.time()
                    if current_time - self.last_log_time >= 0.5:
                        action = "Прямо"
                        if abs(angle_diff) > self.turn_threshold:
                            action = "Вправо (D)" if angle_diff > 0 else "Влево (A)"
                        
                        target_type = target.get('type', 'unknown')
                        target_color = target.get('color', 'unknown')
                        state_info = f"Состояние: {self.state}"
                        if target_type == 'square':
                            if self.checkpoint_counter:
                                internal = self.checkpoint_counter.get_internal()
                                external = self.checkpoint_counter.get_external()
                                state_info += f", Чекпоинтов: внутренний={internal}, внешний={external}"
                            else:
                                state_info += f", Квадратов (old): {self.red_squares_collected}"
                        
                        logger.info(f"{state_info} | Угол: {angle_diff:.1f}°, Расстояние: {distance:.1f}px, {action}")
                        self.last_log_time = current_time
                    
                    # Сохраняем отладочный скриншот
                    action = "Прямо"
                    if abs(angle_diff) > self.turn_threshold:
                        action = "Вправо (D)" if angle_diff > 0 else "Влево (A)"
                    self.save_debug_minimap(minimap, player, target, angle_diff, distance, action)
                    
                    # Управляем лодкой
                    try:
                        # ВАЖНО: Убеждаемся, что W нажата перед вызовом control_boat
                        # Нажимаем W каждый раз, когда цель найдена (даже если флаг уже True)
                        # Это гарантирует, что клавиша действительно нажата в игре
                        win32_success = self.send_key_to_window('w', press=True)
                        try:
                            self.keyboard.press('w')
                        except:
                            pass
                        if not self.keys_pressed['w']:
                            logger.info(f"Нажата клавиша W для движения вперед (SendInput/PostMessage: {win32_success})")
                        self.keys_pressed['w'] = True
                        
                        self.control_boat(angle_diff, distance=distance)
                    except Exception as e:
                        logger.error(f"Ошибка в control_boat: {e}", exc_info=True)
                
                # Небольшая задержка для стабильности
                time.sleep(SCREEN_CAPTURE_DELAY)
        
        except KeyboardInterrupt:
            logger.info("Прервано пользователем")
        except Exception as e:
            logger.error(f"Критическая ошибка: {e}", exc_info=True)
        finally:
            # Полная остановка бота: отпускаем все клавиши, включая W
            self.stop_boat(release_w=True)
            listener.stop()
            # Очищаем низкоуровневый хук Windows
            if WIN32_AVAILABLE:
                try:
                    self._cleanup_keyboard_hook()
                except Exception as e:
                    logger.error(f"Ошибка очистки хука: {e}")
            # Очищаем хоткеи keyboard
            if KEYBOARD_AVAILABLE:
                try:
                    keyboard.unhook_all()
                except:
                    pass
            logger.info("Бот остановлен")

def main():
    """Точка входа"""
    print("=" * 50)
    print("Бот для автоматического плавания на лодке в GTA")
    print("=" * 50)
    print("\nИнструкция:")
    print("1. Запустите игру GTA")
    print("2. Сядьте на лодку")
    print("3. Запустите бота")
    print("4. Нажмите 'q' для остановки бота")
    print("5. Нажмите 'Insert' для паузы/возобновления (работает в игре)")
    print("\nВАЖНО: Настройте координаты миникарты!")
    print("Используйте calibrate.py для автоматической калибровки")
    print("=" * 50)
    
    input("\nНажмите Enter для запуска бота...")
    
    bot = BoatBot()
    bot.run()

if __name__ == "__main__":
    main()

