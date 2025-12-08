"""
Унифицированный модуль управления клавиатурой
Объединяет все способы отправки клавиш и хоткеев
"""

import time
import threading
import logging
from typing import Optional, Callable
from enum import Enum

logger = logging.getLogger(__name__)

# Проверка доступности библиотек
try:
    from pynput.keyboard import Key, Controller, Listener
    PYNPUT_AVAILABLE = True
except ImportError:
    PYNPUT_AVAILABLE = False
    logger.warning("pynput не установлен")

try:
    import keyboard
    KEYBOARD_LIB_AVAILABLE = True
except ImportError:
    KEYBOARD_LIB_AVAILABLE = False

try:
    import win32api
    import win32gui
    import ctypes
    from ctypes import wintypes
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False
    if logging:
        logger.warning("win32 не установлен")

# Windows API структуры для SendInput
if WIN32_AVAILABLE:
    PUL = ctypes.POINTER(ctypes.c_ulong)
    
    class KeyBdInput(ctypes.Structure):
        _fields_ = [("wVk", ctypes.c_ushort),
                    ("wScan", ctypes.c_ushort),
                    ("dwFlags", ctypes.c_ulong),
                    ("time", ctypes.c_ulong),
                    ("dwExtraInfo", PUL)]
    
    class Input_I(ctypes.Union):
        _fields_ = [("ki", KeyBdInput)]
    
    class Input(ctypes.Structure):
        _fields_ = [("type", ctypes.c_ulong),
                    ("ii", Input_I)]
    
    KEYEVENTF_KEYUP = 0x0002
    INPUT_KEYBOARD = 1
    VK_CODE = {
        'w': 0x57,
        'a': 0x41,
        'd': 0x44,
        's': 0x53
    }
    WM_KEYDOWN = 0x0100
    WM_KEYUP = 0x0101


class KeyMethod(Enum):
    """Методы отправки клавиш по приоритету"""
    SENDINPUT = 1
    POSTMESSAGE = 2
    PYNPUT = 3


class KeyboardManager:
    """Унифицированный менеджер клавиатуры"""
    
    def __init__(self, window_handle: Optional[int] = None):
        """
        Args:
            window_handle: Handle окна игры (для PostMessage)
        """
        self.window_handle = window_handle
        self.paused = False
        self.pause_lock = threading.Lock()
        
        # Состояние нажатых клавиш
        self.keys_pressed = {'w': False, 'a': False, 'd': False, 's': False}
        
        # pynput контроллер
        self.pynput_controller: Optional[Controller] = None
        if PYNPUT_AVAILABLE:
            try:
                self.pynput_controller = Controller()
            except Exception as e:
                logger.warning(f"Не удалось инициализировать pynput: {e}")
        
        # Хуки для Insert
        self.keyboard_hook: Optional[int] = None
        self._hook_proc = None
        self.hotkey_registered = False
        self.listener: Optional[Listener] = None
        
        # Для отслеживания Insert
        self.insert_pressed = False
        self.insert_press_time = 0
        
        # Выбираем лучший метод отправки клавиш
        self.primary_method = self._determine_best_method()
        logger.info(f"KeyboardManager инициализирован, метод отправки: {self.primary_method}")
    
    def _determine_best_method(self) -> KeyMethod:
        """Определяет лучший доступный метод отправки клавиш"""
        if WIN32_AVAILABLE:
            return KeyMethod.SENDINPUT
        elif WIN32_AVAILABLE and self.window_handle:
            return KeyMethod.POSTMESSAGE
        elif PYNPUT_AVAILABLE:
            return KeyMethod.PYNPUT
        else:
            logger.error("Нет доступных методов отправки клавиш!")
            return KeyMethod.PYNPUT  # Fallback
    
    def send_key(self, key_char: str, press: bool = True, ignore_pause: bool = False) -> bool:
        """
        Отправляет клавишу используя лучший доступный метод
        
        Args:
            key_char: Символ клавиши ('w', 'a', 'd', 's')
            press: True для нажатия, False для отпускания
            ignore_pause: Игнорировать проверку паузы
        
        Returns:
            True если успешно, False иначе
        """
        if not ignore_pause and self.paused:
            return False
        
        key_char = key_char.lower()
        
        # Пробуем методы по приоритету
        if WIN32_AVAILABLE:
            if self._send_input(key_char, press):
                return True
            if self.window_handle and self._post_message(key_char, press):
                return True
        
        # Fallback на pynput
        if PYNPUT_AVAILABLE and self.pynput_controller:
            return self._pynput_send(key_char, press)
        
        return False
    
    def _send_input(self, key_char: str, press: bool) -> bool:
        """Отправка через SendInput (самый надежный)"""
        if key_char not in VK_CODE:
            return False
        
        try:
            vk_code = VK_CODE[key_char]
            extra = ctypes.c_ulong(0)
            ii_ = Input_I()
            ii_.ki = KeyBdInput(vk_code, 0, 0 if press else KEYEVENTF_KEYUP, 0, ctypes.pointer(extra))
            x = Input(INPUT_KEYBOARD, ii_)
            ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
            return True
        except Exception as e:
            logger.debug(f"SendInput failed: {e}")
            return False
    
    def _post_message(self, key_char: str, press: bool) -> bool:
        """Отправка через PostMessage"""
        if not self.window_handle or key_char not in VK_CODE:
            return False
        
        try:
            vk_code = VK_CODE[key_char]
            if press:
                win32api.PostMessage(self.window_handle, WM_KEYDOWN, vk_code, 0)
            else:
                win32api.PostMessage(self.window_handle, WM_KEYUP, vk_code, 0)
            return True
        except Exception as e:
            logger.debug(f"PostMessage failed: {e}")
            return False
    
    def _pynput_send(self, key_char: str, press: bool) -> bool:
        """Отправка через pynput"""
        if not self.pynput_controller:
            return False
        
        try:
            if press:
                self.pynput_controller.press(key_char)
            else:
                self.pynput_controller.release(key_char)
            return True
        except Exception as e:
            logger.debug(f"pynput failed: {e}")
            return False
    
    def register_pause_hotkey(self, callback: Callable[[], None]) -> bool:
        """
        Регистрирует хоткей Insert для паузы (использует лучший доступный метод)
        
        Args:
            callback: Функция-обработчик
        
        Returns:
            True если успешно зарегистрирован
        """
        success = False
        
        # Метод 1: Низкоуровневый Windows Hook (самый надежный)
        if WIN32_AVAILABLE:
            try:
                success = self._setup_windows_hook(callback)
                if success:
                    logger.info("Низкоуровневый хук Windows установлен для Insert")
            except Exception as e:
                logger.warning(f"Не удалось установить Windows Hook: {e}")
        
        # Метод 2: keyboard библиотека
        if not success and KEYBOARD_LIB_AVAILABLE:
            try:
                keyboard.add_hotkey('insert', callback, suppress=False)
                self.hotkey_registered = True
                success = True
                logger.info("Глобальный хоткей Insert зарегистрирован (keyboard.add_hotkey)")
            except Exception as e:
                logger.warning(f"Не удалось зарегистрировать keyboard hotkey: {e}")
        
        # Метод 3: pynput Listener (запасной)
        if not success and PYNPUT_AVAILABLE:
            try:
                def on_press(key):
                    is_insert = False
                    if key == Key.insert:
                        is_insert = True
                    elif hasattr(key, 'name') and key.name == 'insert':
                        is_insert = True
                    
                    if is_insert:
                        callback()
                
                self.listener = Listener(on_press=on_press)
                self.listener.start()
                success = True
                logger.info("pynput Listener установлен для Insert")
            except Exception as e:
                logger.warning(f"Не удалось установить pynput listener: {e}")
        
        if not success:
            logger.error("Не удалось зарегистрировать хоткей Insert ни одним методом!")
        
        return success
    
    def _setup_windows_hook(self, callback: Callable[[], None]) -> bool:
        """Устанавливает низкоуровневый хук Windows"""
        if not WIN32_AVAILABLE:
            return False
        
        VK_INSERT = 45
        WH_KEYBOARD_LL = 13
        WM_KEYDOWN = 0x0100
        WM_KEYUP = 0x0101
        WM_SYSKEYDOWN = 0x0104
        WM_SYSKEYUP = 0x0105
        HC_ACTION = 0
        
        class KBDLLHOOKSTRUCT(ctypes.Structure):
            _fields_ = [("vkCode", wintypes.DWORD),
                        ("scanCode", wintypes.DWORD),
                        ("flags", wintypes.DWORD),
                        ("time", wintypes.DWORD),
                        ("dwExtraInfo", ctypes.POINTER(wintypes.ULONG))]
        
        HookProc = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_int, wintypes.WPARAM, wintypes.LPARAM)
        
        manager_instance = self
        
        def low_level_keyboard_proc(nCode, wParam, lParam):
            try:
                if nCode >= HC_ACTION:
                    kbd = ctypes.cast(lParam, ctypes.POINTER(KBDLLHOOKSTRUCT)).contents
                    
                    if kbd.vkCode == VK_INSERT:
                        current_time = time.time()
                        
                        if wParam == WM_KEYDOWN or wParam == WM_SYSKEYDOWN:
                            if not manager_instance.insert_pressed or (current_time - manager_instance.insert_press_time) > 0.3:
                                manager_instance.insert_pressed = True
                                manager_instance.insert_press_time = current_time
                                
                                threading.Thread(target=callback, daemon=True).start()
                        elif wParam == WM_KEYUP or wParam == WM_SYSKEYUP:
                            manager_instance.insert_pressed = False
                
                return ctypes.windll.user32.CallNextHookExW(manager_instance.keyboard_hook, nCode, wParam, lParam)
            except Exception as e:
                logger.error(f"Ошибка в хуке: {e}")
                return ctypes.windll.user32.CallNextHookExW(manager_instance.keyboard_hook, nCode, wParam, lParam)
        
        self._hook_proc = HookProc(low_level_keyboard_proc)
        
        self.keyboard_hook = ctypes.windll.user32.SetWindowsHookExW(
            WH_KEYBOARD_LL,
            self._hook_proc,
            ctypes.windll.kernel32.GetModuleHandleW(None),
            0
        )
        
        if not self.keyboard_hook:
            return False
        
        return True
    
    def cleanup(self):
        """Очищает ресурсы (хуки, listeners)"""
        # Удаляем Windows Hook
        if self.keyboard_hook and self.keyboard_hook != 0:
            try:
                ctypes.windll.user32.UnhookWindowsHookExW(self.keyboard_hook)
                self.keyboard_hook = 0
            except Exception as e:
                logger.error(f"Ошибка удаления хука: {e}")
        
        # Удаляем keyboard hotkey
        if self.hotkey_registered and KEYBOARD_LIB_AVAILABLE:
            try:
                keyboard.unhook_all()
            except Exception:
                pass
        
        # Останавливаем pynput listener
        if self.listener:
            try:
                self.listener.stop()
            except Exception:
                pass
    
    def release_all_keys(self, release_w: bool = True):
        """Освобождает все нажатые клавиши"""
        keys_to_release = []
        if release_w and self.keys_pressed.get('w'):
            keys_to_release.append('w')
        if self.keys_pressed.get('a'):
            keys_to_release.append('a')
        if self.keys_pressed.get('d'):
            keys_to_release.append('d')
        if self.keys_pressed.get('s'):
            keys_to_release.append('s')
        
        for key in keys_to_release:
            self.send_key(key, press=False, ignore_pause=True)
            self.keys_pressed[key] = False
        
        time.sleep(0.05)  # Небольшая задержка для обработки

