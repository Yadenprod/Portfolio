"""
Модуль для автоматизации запуска RADMIR через Sandboxie
"""
import json
import logging
import os
import subprocess
import time
import win32api
import win32con
import win32gui
import win32process
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pywinauto import Application, Desktop
from pywinauto.timings import wait_until
import pyautogui


def find_window_by_title_win32(title_substring: str, timeout: int = 20):
    """
    Найти окно через win32gui (работает независимо от прав доступа)
    
    Args:
        title_substring: Подстрока в заголовке окна
        timeout: Таймаут поиска в секундах
    
    Returns:
        hwnd окна или None
    """
    import win32gui
    
    def enum_windows_callback(hwnd, results):
        if win32gui.IsWindowVisible(hwnd):
            window_title = win32gui.GetWindowText(hwnd)
            if title_substring.lower() in window_title.lower():
                results.append(hwnd)
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        results = []
        win32gui.EnumWindows(enum_windows_callback, results)
        
        if results:
            return results[0]  # Возвращаем первое найденное окно
        
        time.sleep(0.5)
    
    return None


def click_button_in_window_win32(hwnd, button_text: str) -> bool:
    """
    Найти и кликнуть на кнопку в окне через win32gui
    
    Args:
        hwnd: Handle окна
        button_text: Текст кнопки
    
    Returns:
        True если кнопка найдена и нажата
    """
    import win32gui
    import win32con
    
    def enum_child_callback(child_hwnd, results):
        try:
            text = win32gui.GetWindowText(child_hwnd)
            class_name = win32gui.GetClassName(child_hwnd)
            
            if text == button_text and "Button" in class_name:
                results.append(child_hwnd)
        except:
            pass
    
    results = []
    win32gui.EnumChildWindows(hwnd, enum_child_callback, results)
    
    if results:
        button_hwnd = results[0]
        # Получаем координаты кнопки
        try:
            rect = win32gui.GetWindowRect(button_hwnd)
            x = (rect[0] + rect[2]) // 2
            y = (rect[1] + rect[3]) // 2
            
            # Кликаем через pyautogui
            pyautogui.click(x, y)
            logging.info(f"✓ Кликнули на кнопку '{button_text}' по координатам ({x}, {y})")
            return True
        except Exception as e:
            logging.error(f"Ошибка клика на кнопку: {e}")
            return False
    
    return False


class TimeManager:
    """Класс для управления системным временем"""
    
    @staticmethod
    def get_current_time() -> datetime:
        """Получить текущее системное время"""
        return datetime.now()
    
    @staticmethod
    def set_system_time(target_time: datetime) -> bool:
        """
        Установить системное время
        Требует прав администратора!
        """
        try:
            # Формат: (год, месяц, день_недели, день, час, минута, секунда, миллисекунды)
            day_of_week = target_time.weekday()
            time_tuple = (
                target_time.year,
                target_time.month,
                day_of_week,
                target_time.day,
                target_time.hour,
                target_time.minute,
                target_time.second,
                0
            )
            win32api.SetSystemTime(*time_tuple)
            logging.info(f"Системное время изменено на: {target_time}")
            return True
        except Exception as e:
            logging.error(f"Ошибка при изменении системного времени: {e}")
            return False
    
    @staticmethod
    def shift_time_back(years: int = 1) -> bool:
        """Сдвинуть время на N лет назад"""
        current_time = TimeManager.get_current_time()
        target_time = current_time - timedelta(days=365 * years)
        return TimeManager.set_system_time(target_time)


class SandboxieLauncher:
    """Класс для запуска приложений через Sandboxie"""
    
    def __init__(self, sandboxie_start_path: str):
        self.sandboxie_start_path = sandboxie_start_path
        
    def launch_in_sandbox(self, exe_path: str, sandbox_name: str, elevate: bool = True) -> bool:
        """
        Запустить приложение в песочнице МЫШКОЙ через контекстное меню
        ПКМ на файл -> Запустить в песочнице -> выбор окна + UAC галочка -> OK
        
        Args:
            exe_path: Путь к исполняемому файлу
            sandbox_name: Имя песочницы (okno1, okno2, и т.д.)
            elevate: Поставить ли галочку UAC
        """
        try:
            logging.info(f"Запуск МЫШКОЙ: ПКМ на {exe_path} -> Run Sandboxed -> {sandbox_name}")
            
            # Шаг 1: Открываем проводник с файлом
            subprocess.Popen(f'explorer.exe /select,"{exe_path}"', shell=True)
            time.sleep(2)
            
            desktop = Desktop(backend="uia")
            
            # Шаг 2: Находим окно проводника
            explorer_window = None
            for attempt in range(5):
                try:
                    windows = desktop.windows()
                    for win in windows:
                        try:
                            if "CabinetWClass" in win.class_name():
                                explorer_window = win
                                break
                        except:
                            continue
                    if explorer_window:
                        break
                    time.sleep(1)
                except:
                    time.sleep(1)
            
            if not explorer_window:
                logging.error("Проводник не найден")
                return False
            
            logging.info("✓ Проводник открыт")
            
            # Шаг 3: Устанавливаем фокус на проводник
            explorer_window.set_focus()
            time.sleep(0.5)
            
            # Файл уже выбран через explorer /select
            # Вызываем контекстное меню через Shift+F10
            logging.info("Файл уже выбран, вызываем контекстное меню (Shift+F10)")
            
            import pywinauto.keyboard as keyboard
            keyboard.send_keys('+{F10}')  # Shift+F10 = контекстное меню
            time.sleep(1.5)
            
            logging.info("✓ Контекстное меню вызвано")
            
            # Шаг 5: Ищем контекстное меню и кликаем на "Запустить в песочнице" МЫШКОЙ
            menu_item_found = False
            for attempt in range(5):
                try:
                    windows = desktop.windows()
                    for win in windows:
                        try:
                            class_name = win.class_name()
                            if "#32768" in class_name:  # Класс контекстного меню
                                # Это контекстное меню
                                for child in win.descendants():
                                    try:
                                        text = child.window_text()
                                        if "Запустить в песочнице" in text or "Run Sandboxed" in text:
                                            # Кликаем МЫШКОЙ на пункт меню
                                            child.click_input()
                                            logging.info(f"✓ КЛИКНУЛИ МЫШКОЙ: '{text}'")
                                            menu_item_found = True
                                            break
                                    except:
                                        continue
                                if menu_item_found:
                                    break
                        except:
                            continue
                    if menu_item_found:
                        break
                    time.sleep(0.5)
                except:
                    time.sleep(0.5)
            
            if not menu_item_found:
                logging.error("Пункт 'Запустить в песочнице' не найден в меню")
                explorer_window.close()
                return False
            
            time.sleep(1.5)
            
            # Шаг 6: Ищем диалог "Запустить в песочнице"
            sandboxie_dialog = None
            for attempt in range(10):
                try:
                    windows = desktop.windows()
                    for win in windows:
                        try:
                            title = win.window_text()
                            if "Запустить в песочнице" in title or "Run Sandboxed" in title:
                                sandboxie_dialog = win
                                logging.info(f"✓ Диалог найден: {title}")
                                break
                        except:
                            continue
                    if sandboxie_dialog:
                        break
                    time.sleep(1)
                except:
                    time.sleep(1)
            
            if not sandboxie_dialog:
                logging.error("Диалог Sandboxie не появился")
                explorer_window.close()
                return False
            
            # Шаг 7: МЫШКОЙ выбираем песочницу из списка
            sandbox_selected = False
            try:
                for child in sandboxie_dialog.descendants():
                    try:
                        control_type = str(child.element_info.control_type)
                        if "ListItem" in control_type and child.window_text() == sandbox_name:
                            # Кликаем МЫШКОЙ на нужную песочницу
                            child.click_input()
                            logging.info(f"✓ МЫШКОЙ выбрали: {sandbox_name}")
                            sandbox_selected = True
                            time.sleep(0.5)
                            break
                    except:
                        continue
            except:
                pass
            
            if not sandbox_selected:
                logging.warning(f"Не удалось выбрать {sandbox_name}, используем текущий выбор")
            
            # Шаг 8: МЫШКОЙ ставим галочку UAC
            if elevate:
                uac_checked = False
                try:
                    for child in sandboxie_dialog.descendants():
                        try:
                            text = child.window_text()
                            control_type = str(child.element_info.control_type)
                            if ("UAC" in text or "Администратор" in text) and "CheckBox" in control_type:
                                # Кликаем МЫШКОЙ на чекбокс
                                child.click_input()
                                logging.info(f"✓ МЫШКОЙ кликнули на чекбокс: {text}")
                                uac_checked = True
                                time.sleep(0.5)
                                break
                        except:
                            continue
                except:
                    pass
                
                if not uac_checked:
                    logging.warning("Чекбокс UAC не найден")
            
            # Шаг 9: МЫШКОЙ нажимаем OK
            ok_clicked = False
            try:
                for child in sandboxie_dialog.descendants():
                    try:
                        text = child.window_text()
                        control_type = str(child.element_info.control_type)
                        if text == "OK" and "Button" in control_type:
                            # Кликаем МЫШКОЙ на OK
                            child.click_input()
                            logging.info("✓ МЫШКОЙ нажали OK")
                            ok_clicked = True
                            time.sleep(0.5)
                            break
                    except:
                        continue
            except:
                pass
            
            if not ok_clicked:
                logging.error("Кнопка OK не найдена")
                explorer_window.close()
                return False
            
            # Закрываем проводник
            try:
                explorer_window.close()
            except:
                pass
            
            logging.info("✓ Все действия МЫШКОЙ выполнены успешно!")
            time.sleep(4)
            return True
            
        except Exception as e:
            logging.error(f"Ошибка автоматизации мыши: {e}")
            return False
    
    def _automate_sandboxie_dialog(self, dialog, sandbox_name: str, elevate: bool):
        """Автоматизация диалога Sandboxie"""
        try:
            # Выбираем песочницу из списка
            for child in dialog.descendants():
                try:
                    if child.window_text() == sandbox_name:
                        child.click()
                        logging.info(f"Выбрана песочница: {sandbox_name}")
                        time.sleep(0.5)
                        break
                except:
                    continue
            
            # Ставим галочку UAC
            if elevate:
                for child in dialog.descendants():
                    try:
                        text = child.window_text()
                        control_type = child.element_info.control_type
                        if ("UAC" in text or "Администратор" in text) and "CheckBox" in str(control_type):
                            try:
                                # Проверяем состояние и кликаем если нужно
                                if hasattr(child, 'get_toggle_state'):
                                    if child.get_toggle_state() == 0:
                                        child.click()
                                        logging.info("Включена галочка UAC")
                                else:
                                    child.click()
                                    logging.info("Кликнули по галочке UAC")
                                time.sleep(0.5)
                                break
                            except:
                                pass
                    except:
                        continue
            
            # Нажимаем OK
            for child in dialog.descendants():
                try:
                    if child.window_text() == "OK":
                        child.click()
                        logging.info("Нажата кнопка OK")
                        time.sleep(1)
                        break
                except:
                    continue
                    
        except Exception as e:
            logging.error(f"Ошибка автоматизации диалога: {e}")
    
    def _fallback_launch(self, exe_path: str, sandbox_name: str, elevate: bool) -> bool:
        """Запасной вариант запуска напрямую через Start.exe"""
        try:
            logging.info("Используется fallback метод запуска")
            # Всегда запускаем БЕЗ /elevate, используем DropAdminRights=n из настроек
            cmd = [self.sandboxie_start_path, f"/box:{sandbox_name}", exe_path]
            
            logging.info(f"Команда fallback: {' '.join(cmd)}")
            subprocess.Popen(cmd, shell=False)
            time.sleep(4)
            return True
        except Exception as e:
            logging.error(f"Ошибка fallback запуска: {e}")
            return False


class RadmirAutomation:
    """Основной класс автоматизации RADMIR Launcher"""
    
    def __init__(self, config_path: str = "config.json"):
        self.config = self._load_config(config_path)
        self.sandboxie = SandboxieLauncher(self.config["sandboxie_start"])
        self.time_manager = TimeManager()
        
        # Настройка логирования
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('radmir_automation.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
    
    def _send_keys_low_level(self, hwnd, keys):
        """Отправка клавиш напрямую окну через SendMessage"""
        try:
            WM_KEYDOWN = 0x0100
            WM_KEYUP = 0x0101
            
            key_codes = {
                'left': 0x25,  # VK_LEFT
                'right': 0x27,  # VK_RIGHT
                'enter': 0x0D,  # VK_RETURN
                'tab': 0x09     # VK_TAB
            }
            
            for key in keys:
                if key in key_codes:
                    vk_code = key_codes[key]
                    win32api.SendMessage(hwnd, WM_KEYDOWN, vk_code, 0)
                    time.sleep(0.1)
                    win32api.SendMessage(hwnd, WM_KEYUP, vk_code, 0)
                    logging.info(f"✓ SendMessage: {key.upper()}")
                    time.sleep(0.3)
        except Exception as e:
            logging.error(f"Ошибка _send_keys_low_level: {e}")
    
    def _load_config(self, config_path: str) -> Dict:
        """Загрузить конфигурацию из JSON"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Ошибка загрузки конфигурации: {e}")
            raise
    
    def wait_and_click_button(self, title: str, button_name: str, timeout: int = 30) -> bool:
        """
        Ожидание окна и нажатие кнопки
        
        Args:
            title: Заголовок окна (можно использовать regex)
            button_name: Имя кнопки для нажатия
            timeout: Таймаут ожидания в секундах
        """
        try:
            # Ищем окно по заголовку
            desktop = Desktop(backend="uia")
            window = None
            
            start_time = time.time()
            while time.time() - start_time < timeout:
                try:
                    windows = desktop.windows()
                    for win in windows:
                        try:
                            win_title = win.window_text()
                            if title.lower() in win_title.lower():
                                window = win
                                break
                        except:
                            continue
                    
                    if window:
                        break
                    
                    time.sleep(0.5)
                except:
                    time.sleep(0.5)
            
            if not window:
                logging.warning(f"Окно '{title}' не найдено за {timeout} секунд")
                return False
            
            logging.info(f"Найдено окно: {window.window_text()}")
            
            # Ищем и нажимаем кнопку МЫШКОЙ
            try:
                # Сначала пробуем найти напрямую
                for child in window.descendants():
                    try:
                        text = child.window_text()
                        control_type = str(child.element_info.control_type)
                        
                        # Проверяем точное совпадение или вхождение
                        if (text == button_name or button_name.lower() in text.lower()) and "Button" in control_type:
                            # Кликаем МЫШКОЙ
                            child.click_input()
                            logging.info(f"✓ МЫШКОЙ нажали кнопку: {text}")
                            time.sleep(1)
                            return True
                    except:
                        continue
                
                logging.warning(f"Кнопка '{button_name}' не найдена")
                return False
                
            except Exception as e:
                logging.error(f"Ошибка поиска кнопки: {e}")
                return False
                
        except Exception as e:
            logging.error(f"Ошибка при работе с окном '{title}': {e}")
            return False
    
    def handle_sandboxie_dialogs(self) -> bool:
        """Обработка диалога НОВЫЙ ЛАУНЧЕР (UAC отключен через FakeAdminRights=y)"""
        try:
            # UAC диалог отключен через FakeAdminRights=y - пропускаем
            logging.info("✓ UAC диалог отключен (FakeAdminRights=y)")
            
            # Ждём появления диалога НОВЫЙ ЛАУНЧЕР
            logging.info("Ожидание диалога НОВЫЙ ЛАУНЧЕР...")
            
            # Проверяем, есть ли AutoHotkey
            ahk_paths = [
                r"C:\Program Files\AutoHotkey\AutoHotkey.exe",
                r"C:\Program Files (x86)\AutoHotkey\AutoHotkey.exe",
                r"C:\ProgramData\chocolatey\bin\AutoHotkey.exe"
            ]
            
            ahk_exe = None
            for path in ahk_paths:
                if os.path.exists(path):
                    ahk_exe = path
                    break
            
            if ahk_exe and os.path.exists("click_sandboxie_yes.ahk"):
                # Запускаем AHK скрипт
                logging.info("✓ AutoHotkey найден, запускаем скрипт")
                process = subprocess.Popen([ahk_exe, "click_sandboxie_yes.ahk"])
                process.wait(timeout=25)  # Ждём завершения скрипта
                
                # Проверяем лог
                if os.path.exists("sandboxie_ahk.log"):
                    with open("sandboxie_ahk.log", "r") as f:
                        log_content = f.read()
                    if "SUCCESS" in log_content:
                        logging.info("✓ AutoHotkey успешно нажал Yes")
                    else:
                        logging.warning("AutoHotkey завершился, но статус неизвестен")
                
                time.sleep(2)
            else:
                # Fallback: используем SendMessage через win32api (низкоуровневый)
                logging.warning("AutoHotkey не найден, используем win32api.SendMessage")
                
                # Ждём чтобы окно появилось
                logging.info("Ожидаем 2 секунды появления диалога...")
                time.sleep(2)
                
                # Ищем окно Sandboxie
                hwnd = find_window_by_title_win32("Sandboxie", timeout=10)
                
                if hwnd:
                    logging.info(f"✓ Найдено окно Sandboxie (hwnd={hwnd})")
                    
                    # Находим кнопку Yes через EnumChildWindows
                    def find_yes_button(child_hwnd, results):
                        try:
                            text = win32gui.GetWindowText(child_hwnd)
                            class_name = win32gui.GetClassName(child_hwnd)
                            if text == "Yes" and "Button" in class_name:
                                results.append(child_hwnd)
                        except:
                            pass
                    
                    yes_buttons = []
                    win32gui.EnumChildWindows(hwnd, find_yes_button, yes_buttons)
                    
                    if yes_buttons:
                        yes_hwnd = yes_buttons[0]
                        logging.info(f"✓ Найдена кнопка Yes (hwnd={yes_hwnd})")
                        
                        # Получаем координаты кнопки
                        try:
                            rect = win32gui.GetWindowRect(yes_hwnd)
                            x = (rect[0] + rect[2]) // 2
                            y = (rect[1] + rect[3]) // 2
                            
                            logging.info(f"Координаты кнопки Yes: ({x}, {y})")
                            
                            # Отключаем failsafe pyautogui
                            pyautogui.FAILSAFE = False
                            
                            # Двигаем мышь к кнопке
                            pyautogui.moveTo(x, y, duration=0.3)
                            logging.info(f"✓ Мышь перемещена к ({x}, {y})")
                            time.sleep(0.2)
                            
                            # Кликаем
                            pyautogui.click()
                            logging.info(f"✓ КЛИК выполнен")
                            time.sleep(2)
                            
                            # Включаем failsafe обратно
                            pyautogui.FAILSAFE = True
                            
                        except Exception as e:
                            logging.error(f"Ошибка клика по координатам: {e}")
                            # Fallback
                            time.sleep(1)
                            pyautogui.press('left')
                            time.sleep(0.3)
                            pyautogui.press('enter')
                            time.sleep(2)
                    else:
                        logging.warning("Кнопка Yes не найдена, используем клавиши")
                        # Используем SendInput для отправки клавиш
                        self._send_keys_low_level(hwnd, ['left', 'enter'])
                        time.sleep(2)
                else:
                    logging.warning("Окно не найдено, нажимаем вслепую")
                    time.sleep(2)
                    pyautogui.press('left')
                    time.sleep(0.3)
                    pyautogui.press('enter')
                    time.sleep(2)
            
            # Диалог 2: НОВЫЙ ЛАУНЧЕР - закрыть через SendMessage
            logging.info("Шаг 2: Обработка диалога НОВЫЙ ЛАУНЧЕР...")
            
            # Ждём появления диалога
            time.sleep(2)
            
            # Ищем окно
            hwnd = find_window_by_title_win32("ЛАУНЧЕР", timeout=10)
            
            if hwnd:
                logging.info(f"✓ Найдено окно НОВЫЙ ЛАУНЧЕР (hwnd={hwnd})")
                
                # Находим кнопку Закрыть
                def find_close_button(child_hwnd, results):
                    try:
                        text = win32gui.GetWindowText(child_hwnd)
                        class_name = win32gui.GetClassName(child_hwnd)
                        if "Закрыть" in text and "Button" in class_name:
                            results.append(child_hwnd)
                    except:
                        pass
                
                close_buttons = []
                win32gui.EnumChildWindows(hwnd, find_close_button, close_buttons)
                
                if close_buttons:
                    close_hwnd = close_buttons[0]
                    logging.info(f"✓ Найдена кнопка Закрыть (hwnd={close_hwnd})")
                    
                    # Получаем координаты кнопки и кликаем ФИЗИЧЕСКОЙ МЫШЬЮ
                    try:
                        rect = win32gui.GetWindowRect(close_hwnd)
                        x = (rect[0] + rect[2]) // 2
                        y = (rect[1] + rect[3]) // 2
                        
                        logging.info(f"Координаты кнопки Закрыть: ({x}, {y})")
                        
                        # Кликаем физической мышью
                        pyautogui.click(x, y)
                        logging.info(f"✓ КЛИКНУЛИ МЫШЬЮ по координатам ({x}, {y})")
                        time.sleep(2)
                        
                    except Exception as e:
                        logging.error(f"Ошибка клика: {e}")
                        pyautogui.press('tab')
                        time.sleep(0.3)
                        pyautogui.press('enter')
                        time.sleep(2)
                else:
                    logging.warning("Кнопка Закрыть не найдена, используем Tab+Enter")
                    self._send_keys_low_level(hwnd, ['tab', 'enter'])
                    time.sleep(2)
            else:
                logging.warning("⚠ Окно НОВЫЙ ЛАУНЧЕР не найдено")
                time.sleep(2)
            
            return True
        except Exception as e:
            logging.error(f"Ошибка при обработке диалогов: {e}")
            return False
    
    def interact_with_launcher(self, server: str, nickname: str) -> bool:
        """
        Взаимодействие с лаунчером RADMIR МЫШКОЙ
        1. Клик на кнопку выбора сервера
        2. Скролл и выбор сервера во всплывающем окне
        3. Клик на поле никнейма
        4. Удаление старого и ввод нового ника
        5. Клик на кнопку "Играть"
        
        Args:
            server: Название сервера (например, "SERVER 20")
            nickname: Никнейм для входа
        """
        try:
            logging.info(f"Ожидание лаунчера RADMIR...")
            time.sleep(5)
            
            # Ищем окно лаунчера через win32gui
            hwnd = find_window_by_title_win32("RADMIR LAUNCHER", timeout=30)
            
            if not hwnd:
                logging.error("Окно RADMIR LAUNCHER не найдено")
                return False
            
            window_title = win32gui.GetWindowText(hwnd)
            logging.info(f"✓ Найден лаунчер: {window_title}")
            
            # Активируем окно
            try:
                win32gui.SetForegroundWindow(hwnd)
                logging.info("✓ Лаунчер активирован")
                time.sleep(1)
            except:
                pass
            
            # Получаем размер окна для работы с координатами
            rect = win32gui.GetWindowRect(hwnd)
            left, top, right, bottom = rect
            width = right - left
            height = bottom - top
            center_x = (left + right) // 2
            center_y = (top + bottom) // 2
            
            logging.info(f"Размеры лаунчера: {width}x{height}, центр: ({center_x}, {center_y})")
            
            # Шаг 1: Кликаем на кнопку выбора сервера
            # По скринам: кнопка выбора сервера находится в верхней части, по центру
            server_button_x = center_x
            server_button_y = top + 120  # ~120px от верха
            
            logging.info(f"Шаг 1: Клик на кнопку выбора сервера ({server_button_x}, {server_button_y})")
            pyautogui.click(server_button_x, server_button_y)
            time.sleep(1.5)
            
            # Шаг 2: Выбор сервера из всплывающего списка
            logging.info(f"Шаг 2: Выбор {server} из списка...")
            
            # Извлекаем номер сервера (SERVER 20 -> 20)
            server_num = int(server.replace("SERVER ", "").strip())
            
            # Список серверов обычно показывает первые ~6 серверов
            # Если нужен сервер 20, нужно скроллить вниз
            if server_num > 6:
                # Скроллим вниз в списке
                scroll_times = (server_num - 1) // 6  # Сколько раз крутить колесико
                for _ in range(scroll_times):
                    pyautogui.scroll(-3)  # Скролл вниз
                    time.sleep(0.3)
                logging.info(f"✓ Проскроллили список ({scroll_times} раз)")
                time.sleep(0.5)
            
            # Теперь кликаем на нужный сервер
            # Сервера обычно расположены в сетке 2x3 или списком
            # Попробуем найти координаты через номер
            
            # Упрощенно: нажимаем стрелки для выбора
            down_presses = (server_num - 1) % 6  # Позиция в текущем view
            if down_presses > 0:
                pyautogui.press('down', presses=down_presses)
                logging.info(f"✓ Нажали вниз {down_presses} раз")
                time.sleep(0.3)
            
            pyautogui.press('enter')
            logging.info(f"✓ Выбрали сервер (Enter)")
            time.sleep(1)
            
            # Шаг 3: Клик на поле ввода никнейма
            # По скринам: поле ника находится справа, примерно в центре по высоте
            nick_field_x = center_x + int(width * 0.25)  # Справа от центра
            nick_field_y = center_y
            
            logging.info(f"Шаг 3: Клик на поле ника ({nick_field_x}, {nick_field_y})")
            pyautogui.click(nick_field_x, nick_field_y)
            time.sleep(0.5)
            
            # Удаляем старый текст
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.2)
            pyautogui.press('delete')
            logging.info("✓ Удалили старый ник")
            time.sleep(0.3)
            
            # Вводим новый никнейм
            pyautogui.write(nickname, interval=0.05)
            logging.info(f"✓ Введен никнейм: {nickname}")
            time.sleep(1)
            
            # Шаг 4: Клик на кнопку "ИГРАТЬ"
            # По скринам: кнопка ИГРАТЬ находится внизу слева, оранжевая большая кнопка
            play_button_x = left + int(width * 0.3)  # ~30% от левого края
            play_button_y = bottom - 80  # ~80px от низа
            
            logging.info(f"Шаг 4: Клик на ИГРАТЬ ({play_button_x}, {play_button_y})")
            pyautogui.click(play_button_x, play_button_y)
            time.sleep(3)
            
            logging.info("✓ Все действия с лаунчером выполнены")
            return True
            
        except Exception as e:
            logging.error(f"Ошибка при взаимодействии с лаунчером: {e}")
            return False
    
    def enter_game_password(self, password: str) -> bool:
        """
        Ввод пароля в игре
        
        Args:
            password: Пароль для входа
        """
        try:
            logging.info("Ожидание окна ввода пароля в игре...")
            time.sleep(10)  # Даём время игре загрузиться
            
            desktop = Desktop(backend="uia")
            
            # Ищем окно игры
            game_window = None
            for _ in range(30):
                try:
                    windows = desktop.windows()
                    for win in windows:
                        try:
                            title = win.window_text()
                            # Игра может иметь различные заголовки
                            if "GTA" in title or "SAMP" in title or len(title) > 0:
                                game_window = win
                                break
                        except:
                            continue
                    
                    if game_window:
                        break
                    
                    time.sleep(1)
                except:
                    time.sleep(1)
            
            if not game_window:
                logging.warning("Окно игры не найдено, попробуем ввести пароль вслепую")
                # Вводим пароль вслепую
                time.sleep(5)
                import pywinauto.keyboard as keyboard
                keyboard.send_keys(password)
                keyboard.send_keys('{ENTER}')
                logging.info("Пароль введен вслепую")
                return True
            
            logging.info(f"Найдено окно игры: {game_window.window_text()}")
            
            # Устанавливаем фокус на окно игры
            game_window.set_focus()
            time.sleep(1)
            
            # Вводим пароль
            import pywinauto.keyboard as keyboard
            keyboard.send_keys(password)
            time.sleep(0.5)
            keyboard.send_keys('{ENTER}')
            
            logging.info("Пароль введен в игру")
            return True
            
        except Exception as e:
            logging.error(f"Ошибка при вводе пароля в игру: {e}")
            return False
    
    def process_account(self, account: Dict) -> bool:
        """
        Обработка одного аккаунта
        
        Args:
            account: Словарь с данными аккаунта (sandbox, nickname, server)
        """
        try:
            sandbox = account["sandbox"]
            nickname = account["nickname"]
            server = account["server"]
            password = self.config["common_password"]
            
            logging.info(f"="*60)
            logging.info(f"Обработка аккаунта: {nickname} в песочнице {sandbox}")
            logging.info(f"="*60)
            
            # Шаг 1: Изменить системное время на год назад
            logging.info("Шаг 1: Изменение системного времени...")
            if not self.time_manager.shift_time_back(self.config["time_shift_years"]):
                logging.error("Не удалось изменить системное время!")
                return False
            
            time.sleep(2)
            
            # Шаг 2: Запустить лаунчер в песочнице БЕЗ /elevate
            # (права админа даются через DropAdminRights=n в Sandboxie.ini)
            logging.info("Шаг 2: Запуск лаунчера в песочнице...")
            if not self.sandboxie.launch_in_sandbox(
                self.config["launcher_path"],
                sandbox,
                elevate=False  # БЕЗ /elevate - используем DropAdminRights=n
            ):
                logging.error("Не удалось запустить лаунчер!")
                return False
            
            time.sleep(3)
            
            # Шаг 3: Обработать диалоги Sandboxie
            logging.info("Шаг 3: Обработка диалогов Sandboxie...")
            self.handle_sandboxie_dialogs()
            
            # Шаг 4: Взаимодействие с лаунчером (выбор сервера, ввод никнейма, запуск)
            logging.info("Шаг 4: Взаимодействие с лаунчером...")
            if not self.interact_with_launcher(server, nickname):
                logging.warning("Возможны проблемы при взаимодействии с лаунчером")
            
            # Шаг 5: Ввод пароля в игре
            logging.info("Шаг 5: Ввод пароля в игре...")
            if not self.enter_game_password(password):
                logging.warning("Возможны проблемы при вводе пароля")
            
            logging.info(f"Аккаунт {nickname} обработан успешно!")
            logging.info("")
            
            return True
            
        except Exception as e:
            logging.error(f"Ошибка при обработке аккаунта: {e}")
            return False
    
    def run(self, start_index: int = 0, end_index: Optional[int] = None):
        """
        Запустить автоматизацию для всех аккаунтов
        
        Args:
            start_index: С какого аккаунта начать (индекс в списке)
            end_index: На каком аккаунте закончить (None = до конца)
        """
        accounts = self.config["accounts"]
        
        if end_index is None:
            end_index = len(accounts)
        
        logging.info(f"Начало автоматизации для аккаунтов {start_index} - {end_index}")
        logging.info(f"Всего аккаунтов: {len(accounts)}")
        
        successful = 0
        failed = 0
        
        for i in range(start_index, min(end_index, len(accounts))):
            account = accounts[i]
            
            if self.process_account(account):
                successful += 1
            else:
                failed += 1
                logging.error(f"Не удалось обработать аккаунт {account['nickname']}")
            
            # Небольшая пауза между аккаунтами
            time.sleep(3)
        
        logging.info(f"="*60)
        logging.info(f"Автоматизация завершена!")
        logging.info(f"Успешно обработано: {successful}")
        logging.info(f"Ошибок: {failed}")
        logging.info(f"="*60)


if __name__ == "__main__":
    # Создаём экземпляр автоматизации
    automation = RadmirAutomation("config.json")
    
    # Запускаем для всех аккаунтов
    automation.run()

