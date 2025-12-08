"""
Чистая версия автоматизации RADMIR Launcher
Без AutoHotkey, только win32gui + pyautogui
"""
import json
import logging
import os
import subprocess
import time
import ctypes
import random
import threading
from ctypes import wintypes
import win32api
import win32con
import win32gui
import win32process
from datetime import datetime, timedelta
from typing import Dict, Optional, List
from pywinauto import Desktop
import pyautogui

# Отключаем failsafe
pyautogui.FAILSAFE = False

# Структуры для SendInput (определяем на уровне модуля)
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

KEYEVENTF_KEYUP = 0x0002
INPUT_KEYBOARD = 1


class AutoMovementManager:
    """Управление автоматическим движением для окон игры"""
    
    def __init__(self):
        self.active_threads = {}  # account_key -> thread
        self.enabled = False
        self.pending_accounts = []  # Список аккаунтов, ожидающих запуска движения
        self.all_accounts_launched = False  # Флаг, что все аккаунты запущены
        
        # Очередь движений - для последовательной обработки
        self.movement_queue = []  # Очередь аккаунтов для движения
        self.movement_lock = threading.Lock()  # Блокировка для очереди
        self.movement_thread = None  # Поток обработки очереди
        self.last_movement_time = {}  # account_key -> время последнего движения
        self.max_idle_time = 8 * 60  # Максимальное время простоя (8 минут)
    
    def send_key_sendinput(self, key: str, press: bool = True):
        """
        Отправить клавишу через SendInput (работает даже если окно свернуто)
        
        Args:
            key: Клавиша ('w' или 's')
            press: True для нажатия, False для отпускания
        """
        try:
            # Коды виртуальных клавиш
            VK_CODE = {
                'w': 0x57,
                's': 0x53
            }
            
            if key.lower() not in VK_CODE:
                return False
            
            vk_code = VK_CODE[key.lower()]
            
            # Используем SendInput для отправки клавиш (работает даже если окно не в фокусе)
            extra = ctypes.c_ulong(0)
            ii_ = Input_I()
            ii_.ki = KeyBdInput(
                vk_code, 
                0, 
                0 if press else KEYEVENTF_KEYUP, 
                0, 
                ctypes.cast(ctypes.pointer(extra), PUL)
            )
            x = Input(INPUT_KEYBOARD, ii_)
            result = ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
            
            if result == 0:
                error = ctypes.windll.kernel32.GetLastError()
                logging.debug(f"[Движение] SendInput вернул 0, ошибка: {error}")
                return False
            
            return True
        except Exception as e:
            logging.error(f"[Движение] Ошибка SendInput для {key}: {e}")
            import traceback
            logging.debug(traceback.format_exc())
            return False
    
    def send_key_to_window(self, hwnd: int, key: str, hold_duration: float):
        """
        Отправить клавишу в окно и удерживать её
        
        Активирует и разворачивает окно перед отправкой клавиш (как в боте)
        
        Args:
            hwnd: Handle окна
            key: Клавиша ('w' или 's')
            hold_duration: Время удержания в секундах
        """
        try:
            # Активируем и разворачиваем окно перед отправкой клавиш
            try:
                # Восстанавливаем окно, если оно свернуто
                if win32gui.IsIconic(hwnd):
                    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                    time.sleep(0.2)
                
                # Разворачиваем окно (SW_MAXIMIZE или SW_RESTORE)
                # Проверяем текущее состояние окна
                placement = win32gui.GetWindowPlacement(hwnd)
                if placement[1] != win32con.SW_SHOWMAXIMIZED:
                    # Разворачиваем окно
                    win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
                    time.sleep(0.2)
                
                # Активируем окно (берем в фокус)
                win32gui.SetForegroundWindow(hwnd)
                time.sleep(0.2)
                
                # Проверяем, что окно действительно активно
                active_hwnd = win32gui.GetForegroundWindow()
                if active_hwnd != hwnd:
                    # Пробуем еще раз через BringWindowToTop
                    win32gui.BringWindowToTop(hwnd)
                    win32gui.SetForegroundWindow(hwnd)
                    time.sleep(0.2)
                
                logging.debug(f"[Движение] Окно {hwnd} активировано и развернуто")
            except Exception as e:
                logging.debug(f"[Движение] Ошибка активации окна {hwnd}: {e}")
            
            # Метод 1: Пробуем SendInput (работает с активным окном)
            if self.send_key_sendinput(key, press=True):
                logging.debug(f"[Движение] Зажата клавиша {key.upper()} через SendInput в окне {hwnd}")
                
                # Удерживаем клавишу
                time.sleep(hold_duration)
                
                # Отпускаем клавишу
                self.send_key_sendinput(key, press=False)
                logging.debug(f"[Движение] Отпущена клавиша {key.upper()} через SendInput в окне {hwnd}")
                return
            
            # Метод 2: Fallback - используем PostMessage
            logging.debug(f"[Движение] SendInput не сработал, используем PostMessage для окна {hwnd}")
            
            # Коды виртуальных клавиш
            VK_W = 0x57
            VK_S = 0x53
            WM_KEYDOWN = 0x0100
            WM_KEYUP = 0x0101
            
            vk_code = VK_W if key.lower() == 'w' else VK_S
            
            # Отправляем WM_KEYDOWN (нажатие)
            win32api.PostMessage(hwnd, WM_KEYDOWN, vk_code, 0)
            logging.debug(f"[Движение] Зажата клавиша {key.upper()} в окне {hwnd} через PostMessage")
            
            # Удерживаем клавишу
            time.sleep(hold_duration)
            
            # Отправляем WM_KEYUP (отпускание)
            win32api.PostMessage(hwnd, WM_KEYUP, vk_code, 0)
            logging.debug(f"[Движение] Отпущена клавиша {key.upper()} в окне {hwnd} через PostMessage")
            
        except Exception as e:
            logging.error(f"[Движение] Ошибка отправки клавиши {key} в окно {hwnd}: {e}")
            import traceback
            logging.debug(traceback.format_exc())
    
    def movement_queue_worker(self, automation_instance):
        """
        Рабочий поток для обработки очереди движений
        
        Обрабатывает движения по очереди, чтобы избежать конфликтов
        Гарантирует, что каждое окно двигается не реже чем раз в 15 минут
        
        Args:
            automation_instance: Экземпляр RadmirAutomation для доступа к методам
        """
        logging.info("[Движение] Запущен поток обработки очереди движений")
        
        while self.enabled:
            try:
                # Получаем список всех активных аккаунтов
                accounts_to_check = []
                with self.movement_lock:
                    # Копируем список аккаунтов из active_threads
                    for account_key, account_info in list(self.active_threads.items()):
                        if isinstance(account_info, dict):
                            accounts_to_check.append(account_info)
                
                # Если нет аккаунтов, ждем
                if not accounts_to_check:
                    time.sleep(10)
                    continue
                
                # Проверяем, какие аккаунты нужно двигать
                current_time = time.time()
                accounts_need_movement = []
                
                for account_info in accounts_to_check:
                    if isinstance(account_info, dict):
                        account = account_info.get('account')
                        pid = account_info.get('pid')
                        account_key = account_info.get('account_key', f"{account['nickname']}_{account['sandbox']}")
                    else:
                        continue
                    
                    # Обновляем PID из актуального маппинга (на случай перезапуска)
                    if automation_instance and hasattr(automation_instance, '_pid_to_account'):
                        # Ищем актуальный PID для этого аккаунта
                        sandbox = account.get('sandbox')
                        nickname = account.get('nickname')
                        actual_pid = None
                        for mapped_pid, mapped_account in automation_instance._pid_to_account.items():
                            if mapped_account.get('sandbox') == sandbox and mapped_account.get('nickname') == nickname:
                                actual_pid = mapped_pid
                                break
                        
                        if actual_pid and actual_pid != pid:
                            # Обновляем PID в active_threads
                            self.active_threads[account_key]['pid'] = actual_pid
                            pid = actual_pid
                            logging.debug(f"[Движение] Обновлен PID для {nickname}: {account_key} -> {actual_pid}")
                    
                    # Проверяем, что процесс еще существует
                    try:
                        import psutil
                        proc = psutil.Process(pid)
                        if not proc.is_running():
                            continue
                    except:
                        continue
                    
                    # Проверяем время последнего движения
                    last_time = self.last_movement_time.get(account_key, 0)
                    time_since_last = current_time - last_time
                    
                    # Если прошло больше 8 минут или это первое движение - добавляем в очередь
                    if time_since_last >= self.max_idle_time or last_time == 0:
                        accounts_need_movement.append({
                            'account': account,
                            'pid': pid,  # Используем актуальный PID
                            'account_key': account_key,
                            'automation_instance': automation_instance
                        })
                
                # Если есть аккаунты, которым нужно движение - обрабатываем по очереди
                for movement_info in accounts_need_movement:
                    if not self.enabled:
                        break
                    
                    account = movement_info['account']
                    pid = movement_info['pid']
                    account_key = movement_info['account_key']
                    automation_instance = movement_info['automation_instance']
                    nickname = account['nickname']
                    sandbox = account['sandbox']
                    
                    # Находим окно игры СТРОГО по PID (используем сохраненный PID для точного поиска)
                    game_hwnd = None
                    try:
                        # Ищем окно СТРОГО по PID процесса (PID был сохранен при запуске аккаунта)
                        # Сначала пробуем с фильтром "RADMIR CRMP"
                        game_hwnd = automation_instance.get_window_by_process_id(pid, window_title_filter="RADMIR CRMP")
                        
                        # Если не нашли с фильтром, пробуем без фильтра (но все равно строго по PID)
                        if not game_hwnd:
                            game_hwnd = automation_instance.get_window_by_process_id(pid)
                        
                        # СТРОГАЯ проверка: окно должно принадлежать ТОЧНО этому PID
                        if game_hwnd:
                            try:
                                _, window_pid = win32process.GetWindowThreadProcessId(game_hwnd)
                                if window_pid != pid:
                                    logging.warning(f"[Движение] ⚠ Несоответствие PID: окно {game_hwnd} принадлежит PID {window_pid}, ожидался {pid} для {nickname}")
                                    game_hwnd = None
                                else:
                                    # Дополнительная проверка: получаем название окна для логирования
                                    try:
                                        window_title = win32gui.GetWindowText(game_hwnd)
                                        logging.debug(f"[Движение] ✓ Найдено окно для {nickname}: {window_title} (hwnd: {game_hwnd}, PID: {pid})")
                                    except:
                                        logging.debug(f"[Движение] ✓ Найдено окно для {nickname} (hwnd: {game_hwnd}, PID: {pid})")
                            except Exception as e:
                                logging.warning(f"[Движение] ⚠ Ошибка проверки PID окна {game_hwnd}: {e}")
                                game_hwnd = None
                    except Exception as e:
                        logging.error(f"[Движение] ✗ Ошибка поиска окна для PID {pid} ({nickname}): {e}")
                    
                    if not game_hwnd:
                        logging.warning(f"[Движение] ⚠ Окно не найдено для {nickname} (PID: {pid}), пропускаем движение")
                        continue
                    
                    # Выбираем случайную клавишу (W или S)
                    key = random.choice(['w', 's'])
                    
                    # Выбираем случайное время удержания (максимум 4 секунды)
                    hold_duration = random.uniform(1, 4)
                    
                    logging.info(f"[Движение] {nickname} ({sandbox}): зажимаю {key.upper()} на {hold_duration:.1f} секунд")
                    
                    # Отправляем клавишу в окно
                    self.send_key_to_window(game_hwnd, key, hold_duration)
                    
                    # Обновляем время последнего движения
                    self.last_movement_time[account_key] = time.time()
                    
                    logging.info(f"[Движение] {nickname}: движение завершено")
                    
                    # Пауза между движениями разных окон (чтобы не было конфликтов)
                    time.sleep(2)
                
                # Если нет аккаунтов, которым нужно движение - ждем
                if not accounts_need_movement:
                    # Проверяем каждые 30 секунд
                    time.sleep(30)
                else:
                    # После обработки всех движений ждем перед следующей проверкой
                    time.sleep(10)
                    
            except Exception as e:
                logging.error(f"[Движение] Ошибка в потоке обработки очереди: {e}")
                import traceback
                logging.debug(traceback.format_exc())
                time.sleep(10)
        
        logging.info("[Движение] Поток обработки очереди движений завершен")
    
    def add_pending_account(self, automation_instance, account: Dict, pid: int):
        """
        Добавить аккаунт в очередь ожидания запуска движения
        
        Движение начнется только после того, как все аккаунты будут запущены
        
        Args:
            automation_instance: Экземпляр RadmirAutomation для доступа к методам
            account: Данные аккаунта
            pid: PID процесса игры
        """
        if not self.enabled:
            return
        
        sandbox = account["sandbox"]
        nickname = account["nickname"]
        account_key = f"{nickname}_{sandbox}"
        
        # Добавляем в очередь ожидания
        self.pending_accounts.append({
            'automation_instance': automation_instance,
            'account': account,
            'pid': pid,
            'account_key': account_key
        })
        logging.info(f"[Движение] Аккаунт {nickname} добавлен в очередь ожидания (PID: {pid})")
    
    def start_all_pending_movements(self):
        """Запустить движение для всех аккаунтов в очереди ожидания"""
        if not self.enabled:
            return
        
        self.all_accounts_launched = True
        logging.info(f"[Движение] Запуск движения для {len(self.pending_accounts)} аккаунтов...")
        
        # Сохраняем информацию об аккаунтах для обработки очереди
        for pending in self.pending_accounts:
            account = pending['account']
            pid = pending['pid']
            account_key = pending['account_key']
            automation_instance = pending['automation_instance']
            nickname = account['nickname']
            
            # Сохраняем информацию об аккаунте
            self.active_threads[account_key] = {
                'account': account,
                'pid': pid,
                'account_key': account_key,
                'automation_instance': automation_instance
            }
            
            # Инициализируем время последнего движения (0 = еще не двигался)
            self.last_movement_time[account_key] = 0
            
            logging.info(f"[Движение] Аккаунт {nickname} добавлен в очередь движений (PID: {pid})")
        
        # Запускаем поток обработки очереди движений (один поток для всех аккаунтов)
        if self.pending_accounts and not self.movement_thread:
            automation_instance = self.pending_accounts[0]['automation_instance']
            self.movement_thread = threading.Thread(
                target=self.movement_queue_worker,
                args=(automation_instance,),
                daemon=True,
                name="MovementQueue"
            )
            self.movement_thread.start()
            logging.info(f"[Движение] Запущен поток обработки очереди движений для {len(self.pending_accounts)} аккаунтов")
        
        # Очищаем очередь ожидания
        self.pending_accounts.clear()
        logging.info(f"[Движение] Все аккаунты добавлены в очередь движений")
    
    def stop_all(self):
        """Остановить все потоки движения"""
        self.enabled = False
        logging.info("[Движение] Остановка всех потоков движения...")
        # Потоки завершатся сами при следующей проверке self.enabled


class TimeManager:
    """Управление системным временем"""
    
    def __init__(self):
        self.original_time = None  # Сохраняем оригинальное время для восстановления
        # Настраиваем вызов SetLocalTime через ctypes
        self.kernel32 = ctypes.windll.kernel32
        # Определяем структуру SYSTEMTIME
        class SYSTEMTIME(ctypes.Structure):
            _fields_ = [
                ("wYear", wintypes.WORD),
                ("wMonth", wintypes.WORD),
                ("wDayOfWeek", wintypes.WORD),
                ("wDay", wintypes.WORD),
                ("wHour", wintypes.WORD),
                ("wMinute", wintypes.WORD),
                ("wSecond", wintypes.WORD),
                ("wMilliseconds", wintypes.WORD),
            ]
        self.SYSTEMTIME = SYSTEMTIME
    
    def _set_local_time(self, dt: datetime) -> bool:
        """Установить локальное время через Windows API"""
        try:
            # Получаем день недели для Windows API
            # Python weekday(): 0=понедельник, 1=вторник, ..., 6=воскресенье
            # Windows API: 0=воскресенье, 1=понедельник, ..., 6=суббота
            python_weekday = dt.weekday()
            windows_weekday = (python_weekday + 1) % 7
            
            # Создаем структуру SYSTEMTIME
            st = self.SYSTEMTIME()
            st.wYear = dt.year
            st.wMonth = dt.month
            st.wDayOfWeek = windows_weekday
            st.wDay = dt.day
            st.wHour = dt.hour
            st.wMinute = dt.minute
            st.wSecond = dt.second
            st.wMilliseconds = 0
            
            # Вызываем SetLocalTime (работает с локальным временем, в отличие от SetSystemTime)
            result = self.kernel32.SetLocalTime(ctypes.byref(st))
            if not result:
                error = self.kernel32.GetLastError()
                raise Exception(f"SetLocalTime failed with error {error}")
            return True
        except Exception as e:
            logging.error(f"Ошибка установки локального времени: {e}")
            return False
    
    def shift_time_back(self, years: int = 1) -> bool:
        """
        Сдвинуть время назад на указанное количество лет
        Изначальный способ - вычитает дни из текущего времени
        """
        try:
            current = datetime.now()
            
            # Сохраняем оригинальное время при первом вызове
            if self.original_time is None:
                self.original_time = current
                logging.info(f"Сохранили оригинальное время: {self.original_time}")
            
            # Вычитаем дни (как было изначально)
            target = current - timedelta(days=365 * years)
            
            if self._set_local_time(target):
                logging.info(f"✓ Время: {target}")
                return True
            return False
        except Exception as e:
            logging.error(f"Ошибка времени: {e}")
            return False
    
    def _check_service_status(self):
        """Проверить статус службы времени"""
        try:
            result = subprocess.run(
                ['sc', 'query', 'w32time'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if 'RUNNING' in result.stdout:
                return 'running'
            elif 'STOPPED' in result.stdout:
                return 'stopped'
            else:
                return 'unknown'
        except:
            return 'unknown'
    
    def restore_time(self) -> bool:
        """Восстановить актуальное время через синхронизацию с интернетом"""
        try:
            logging.info("Синхронизация времени с интернетом...")
            
            # Шаг 1: Проверка статуса службы времени
            status = self._check_service_status()
            logging.info(f"Статус службы времени: {status}")
            
            # Шаг 2: Настройка службы на автоматический запуск
            try:
                subprocess.run(
                    ['sc', 'config', 'w32time', 'start=auto'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                logging.info("✓ Служба настроена на автоматический запуск")
            except Exception as e:
                logging.debug(f"Ошибка настройки службы: {e}")
            
            # Шаг 3: Запуск службы, если она не запущена
            if status != 'running':
                try:
                    result = subprocess.run(
                        ['sc', 'start', 'w32time'],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    if result.returncode == 0:
                        logging.info("✓ Служба запущена")
                        time.sleep(2)  # Даем время службе запуститься
                    else:
                        # Пробуем через net start
                        subprocess.run(['net', 'start', 'w32time'], 
                                     capture_output=True, timeout=10)
                        time.sleep(2)
                except Exception as e:
                    logging.debug(f"Ошибка запуска службы: {e}")
            else:
                logging.info("✓ Служба уже запущена")
            
            # Проверяем статус еще раз
            status = self._check_service_status()
            if status != 'running':
                logging.warning("⚠ Служба времени не запущена, но продолжаем...")
            
            # Шаг 4: Настройка синхронизации с time.windows.com
            try:
                result = subprocess.run([
                    'w32tm', '/config', 
                    '/manualpeerlist:time.windows.com',
                    '/syncfromflags:manual',
                    '/update'
                ], capture_output=True, text=True, timeout=10)
                
                if result.returncode == 0:
                    logging.info("✓ Настройка синхронизации выполнена")
            except Exception as e:
                logging.debug(f"Ошибка настройки синхронизации: {e}")
            
            # Шаг 5: Перезапуск службы времени
            try:
                subprocess.run(['sc', 'stop', 'w32time'], 
                             capture_output=True, timeout=10)
                logging.info("✓ Служба остановлена")
                time.sleep(2)
                subprocess.run(['sc', 'start', 'w32time'], 
                             capture_output=True, timeout=10)
                logging.info("✓ Служба запущена")
                time.sleep(3)  # Увеличено время ожидания
                
                # Проверяем, что служба действительно запущена
                status = self._check_service_status()
                if status == 'running':
                    logging.info("✓ Служба успешно запущена и работает")
            except Exception as e:
                logging.debug(f"Ошибка перезапуска службы: {e}")
            
            # Шаг 6: Принудительная синхронизация с интернетом
            result = subprocess.run(
                ['w32tm', '/resync', '/force'],
                capture_output=True,
                text=True,
                timeout=15
            )
            
            if result.returncode == 0 or "successfully" in result.stdout.lower():
                # Получаем текущее время после синхронизации
                time.sleep(1)  # Небольшая задержка для применения изменений
                current_time = datetime.now()
                logging.info(f"✓ Время синхронизировано и восстановлено: {current_time}")
                return True
            else:
                # Если синхронизация не удалась, пробуем еще раз через другой сервер
                logging.warning("Синхронизация через time.windows.com не удалась, пробуем pool.ntp.org...")
                try:
                    subprocess.run([
                        'w32tm', '/config', 
                        '/manualpeerlist:pool.ntp.org',
                        '/syncfromflags:manual',
                        '/update'
                    ], capture_output=True, text=True, timeout=10)
                    time.sleep(1)
                    subprocess.run(['sc', 'stop', 'w32time'], capture_output=True, timeout=10)
                    time.sleep(2)
                    subprocess.run(['sc', 'start', 'w32time'], capture_output=True, timeout=10)
                    time.sleep(3)
                    
                    result2 = subprocess.run(
                        ['w32tm', '/resync', '/force'],
                        capture_output=True,
                        text=True,
                        timeout=15
                    )
                    
                    if result2.returncode == 0 or "successfully" in result2.stdout.lower():
                        time.sleep(1)
                        current_time = datetime.now()
                        logging.info(f"✓ Время синхронизировано через pool.ntp.org: {current_time}")
                        return True
                except Exception as e:
                    logging.warning(f"Ошибка синхронизации через pool.ntp.org: {e}")
                
                # Если все не удалось, просто логируем
                current_time = datetime.now()
                logging.warning(f"Не удалось синхронизировать время. Текущее системное время: {current_time}")
                logging.warning("Рекомендуется вручную синхронизировать время через настройки Windows")
                return False
                
        except Exception as e:
            logging.error(f"Ошибка восстановления времени: {e}")
            return False


def find_window(title_part: str, timeout: int = 20):
    """Найти окно по части заголовка"""
    def enum_callback(hwnd, results):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title_part.lower() in title.lower():
                results.append((hwnd, title))
    
    start = time.time()
    while time.time() - start < timeout:
        results = []
        win32gui.EnumWindows(enum_callback, results)
        if results:
            return results[0]
        time.sleep(0.5)
    return None, None


class SandboxieLauncher:
    """Запуск через Sandboxie"""
    
    def __init__(self, sandboxie_path: str):
        self.path = sandboxie_path
        self.reusable_explorer_hwnd = None  # Окно проводника для переиспользования
        self.explorer_launcher_path = None  # Путь к лаунчеру в открытом проводнике
    
    def launch(self, exe_path: str, sandbox_name: str) -> bool:
        """Запустить через диалог Sandboxie"""
        try:
            logging.info(f"Запуск {sandbox_name}...")
            
            # Проверяем, есть ли уже открытое окно проводника для переиспользования
            explorer_hwnd = None
            
            if self.reusable_explorer_hwnd:
                # Проверяем, что окно еще существует
                try:
                    if win32gui.IsWindow(self.reusable_explorer_hwnd):
                        explorer_hwnd = self.reusable_explorer_hwnd
                        logging.info("✓ Используем уже открытое окно проводника")
                        
                        # Активируем окно проводника
                        try:
                            win32gui.SetForegroundWindow(explorer_hwnd)
                            time.sleep(0.3)
                            
                            # Если путь к лаунчеру изменился, открываем новый путь
                            if self.explorer_launcher_path != exe_path:
                                # Открываем новый путь через Ctrl+L (адресная строка)
                                pyautogui.hotkey('ctrl', 'l')
                                time.sleep(0.2)
                                pyautogui.typewrite(exe_path, interval=0.05)
                                time.sleep(0.2)
                                pyautogui.press('enter')
                                time.sleep(0.5)
                                self.explorer_launcher_path = exe_path
                        except Exception as e:
                            logging.debug(f"Ошибка активации окна проводника: {e}")
                            explorer_hwnd = None
                    else:
                        # Окно закрыто, сбрасываем
                        self.reusable_explorer_hwnd = None
                        self.explorer_launcher_path = None
                except:
                    # Окно не существует, сбрасываем
                    self.reusable_explorer_hwnd = None
                    self.explorer_launcher_path = None
            
            # Если нет переиспользуемого окна - открываем новое
            if not explorer_hwnd:
                # Открываем проводник
                proc = subprocess.Popen(f'explorer.exe /select,"{exe_path}"', shell=True)
                time.sleep(0.8)
                
                # Находим окно проводника
                try:
                    time.sleep(0.5)  # Даем время окну появиться
                    def find_explorer_window(hwnd, results):
                        try:
                            if win32gui.IsWindowVisible(hwnd):
                                title = win32gui.GetWindowText(hwnd)
                                class_name = win32gui.GetClassName(hwnd)
                                # Проверяем, что это окно проводника с путем к лаунчеру
                                if "CabinetWClass" in class_name or "ExplorerWClass" in class_name:
                                    if exe_path.split('\\')[-1] in title or "RADMIR" in title:
                                        _, pid = win32process.GetWindowThreadProcessId(hwnd)
                                        results.append((hwnd, pid, title))
                        except:
                            pass
                    
                    explorer_windows = []
                    win32gui.EnumWindows(find_explorer_window, explorer_windows)
                    if explorer_windows:
                        # Берем первое найденное окно и сохраняем для переиспользования
                        explorer_hwnd, pid, title = explorer_windows[0]
                        self.reusable_explorer_hwnd = explorer_hwnd
                        self.explorer_launcher_path = exe_path
                        logging.info("✓ Окно проводника открыто и сохранено для переиспользования")
                        
                        # Добавляем в список для последующего закрытия
                        if hasattr(self, 'opened_explorer_windows'):
                            self.opened_explorer_windows.append(explorer_windows[0])
                except Exception as e:
                    logging.debug(f"Ошибка поиска окна проводника: {e}")
            
            # Убеждаемся, что окно проводника активно и файл выбран
            if explorer_hwnd:
                try:
                    win32gui.SetForegroundWindow(explorer_hwnd)
                    time.sleep(0.2)
                    
                    # Если используем переиспользуемое окно, нужно убедиться что файл выбран
                    if self.reusable_explorer_hwnd == explorer_hwnd and self.explorer_launcher_path == exe_path:
                        # Файл уже выбран в этом окне, просто активируем
                        logging.debug("✓ Файл уже выбран в переиспользуемом окне проводника")
                    elif self.reusable_explorer_hwnd == explorer_hwnd:
                        # Нужно выбрать другой файл - используем Ctrl+L для адресной строки
                        logging.debug("✓ Выбираем файл в переиспользуемом окне проводника")
                        pyautogui.hotkey('ctrl', 'l')
                        time.sleep(0.2)
                        pyautogui.typewrite(exe_path, interval=0.05)
                        time.sleep(0.2)
                        pyautogui.press('enter')
                        time.sleep(0.5)
                        self.explorer_launcher_path = exe_path
                except Exception as e:
                    logging.debug(f"Ошибка подготовки окна проводника: {e}")
            
            # Контекстное меню
            pyautogui.hotkey('shift', 'f10')
            logging.info("✓ Контекстное меню")
            time.sleep(0.5)  # Уменьшено с 1 до 0.5
            
            # Используем pywinauto для клика на пункт меню
            desktop = Desktop(backend="uia")
            for attempt in range(3):
                windows = desktop.windows()
                for win in windows:
                    try:
                        class_name = win.class_name()
                        if "#32768" in class_name:  # Контекстное меню
                            for child in win.descendants():
                                try:
                                    text = child.window_text()
                                    if "Запустить в песочнице" in text:
                                        child.click_input()
                                        logging.info("✓ Запустить в песочнице")
                                        time.sleep(1)  # Уменьшено с 2 до 1
                                        raise StopIteration
                                except:
                                    continue
                    except StopIteration:
                        break
                    except:
                        continue
                time.sleep(0.5)
            
            # Диалог выбора песочницы
            for win in desktop.windows():
                try:
                    if "Запустить в песочнице" in win.window_text():
                        # Выбираем песочницу
                        for child in win.descendants():
                            try:
                                if child.window_text() == sandbox_name:
                                    child.click_input()
                                    logging.info(f"✓ Выбрали {sandbox_name}")
                                    time.sleep(0.1)  # Уменьшено с 0.2 до 0.1
                                    break
                            except:
                                continue
                        
                        # Галочка UAC
                        for child in win.descendants():
                            try:
                                text = child.window_text()
                                if "UAC" in text and "Администратор" in text:
                                    child.click_input()
                                    logging.info("✓ Галочка UAC")
                                    time.sleep(0.05)  # Уменьшено с 0.15 до 0.05
                                    break
                            except:
                                continue
                        
                        # OK
                        for child in win.descendants():
                            try:
                                if child.window_text() == "OK":
                                    child.click_input()
                                    logging.info("✓ OK")
                                    time.sleep(0.5)  # Уменьшено с 1.5 до 0.5
                                    break
                            except:
                                continue
                        break
                except:
                    continue
            
            return True
        except Exception as e:
            logging.error(f"Ошибка запуска: {e}")
            return False


class RadmirAutomation:
    """Автоматизация RADMIR"""
    
    def __init__(self, config_path: str = "config.json", enable_auto_movement: bool = False):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        self.sandboxie = SandboxieLauncher(self.config["sandboxie_start"])
        self.time_manager = TimeManager()
        self.opened_explorer_windows = []  # Список открытых окон проводника
        self.auto_movement = AutoMovementManager()
        self.auto_movement.enabled = enable_auto_movement
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('radmir_clean.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        
        if enable_auto_movement:
            logging.info("✓ Автоматическое движение активировано")
    
    def check_and_close_sandboxie_support_dialog(self) -> bool:
        """
        Проверка и закрытие окна поддержки Sandboxie
        
        Окно "О Sandboxie" появляется после запуска через песочницу.
        Используем прямой поиск кнопки через Windows API без OCR.
        """
        logging.info("Проверка окна поддержки Sandboxie...")
        time.sleep(0.5)
        
        # Ищем окно по разным вариантам названия
        hwnd = None
        title = None
        
        # Вариант 1: "О Sandboxie"
        hwnd, title = find_window("О Sandboxie", timeout=1)
        if not hwnd:
            # Вариант 2: "About Sandboxie"
            hwnd, title = find_window("About Sandboxie", timeout=1)
        if not hwnd:
            # Вариант 3: Просто "Sandboxie" (может быть окно поддержки)
            hwnd, title = find_window("Sandboxie", timeout=1)
        
        if not hwnd:
            return False
        
        try:
            window_text = win32gui.GetWindowText(hwnd)
            
            # Проверяем, что это именно окно поддержки
            is_support_dialog = (
                "поддержк" in window_text.lower() or 
                "support" in window_text.lower() or
                "сертификат" in window_text.lower() or
                "certificate" in window_text.lower() or
                "О Sandboxie" in window_text or
                "About Sandboxie" in window_text
            )
            
            if not is_support_dialog:
                return False
            
            logging.info("✓ Найдено окно поддержки Sandboxie, ждем 6 секунд...")
            time.sleep(6)  # Ждем 6 секунд (таймер)
            
            # Активируем окно
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.3)
            
            # Проверяем, что окно действительно в фокусе
            active_hwnd = win32gui.GetForegroundWindow()
            if active_hwnd != hwnd:
                win32gui.BringWindowToTop(hwnd)
                win32gui.SetForegroundWindow(hwnd)
                time.sleep(0.3)
            
            # МЕТОД 1: Прямой поиск кнопки через win32gui.EnumChildWindows
            continue_button_hwnd = None
            
            def find_continue_button(child_hwnd, results):
                try:
                    class_name = win32gui.GetClassName(child_hwnd)
                    if "Button" in class_name:
                        text = win32gui.GetWindowText(child_hwnd)
                        if "Продолжить" in text or "Continue" in text:
                            results.append((child_hwnd, text))
                except:
                    pass
                return True
            
            buttons = []
            win32gui.EnumChildWindows(hwnd, find_continue_button, buttons)
            
            if buttons:
                continue_button_hwnd, button_text = buttons[0]
                logging.info(f"✓ Кнопка 'Продолжить' найдена через win32gui: '{button_text}'")
                
                # Отправляем BM_CLICK сообщение напрямую к кнопке
                BM_CLICK = 0x00F5
                win32api.SendMessage(continue_button_hwnd, BM_CLICK, 0, 0)
                logging.info("✓ Отправлено BM_CLICK сообщение к кнопке 'Продолжить'")
                time.sleep(0.5)
                
                if not win32gui.IsWindow(hwnd):
                    logging.info("✓ Окно поддержки закрыто")
                    return True
            
            # МЕТОД 2: Если не нашли через win32gui, пробуем pywinauto
            if continue_button_hwnd is None:
                try:
                    from pywinauto import Application
                    app = Application(backend="uia").connect(handle=hwnd)
                    window = app.window(handle=hwnd)
                    
                    for child in window.descendants():
                        try:
                            text = child.window_text()
                            control_type = str(child.element_info.control_type)
                            
                            if ("Продолжить" in text or "Continue" in text) and "Button" in control_type:
                                logging.info(f"✓ Кнопка 'Продолжить' найдена через pywinauto: '{text}'")
                                child.click_input()
                                logging.info("✓ Клик по кнопке 'Продолжить' через pywinauto")
                                time.sleep(0.5)
                                
                                if not win32gui.IsWindow(hwnd):
                                    logging.info("✓ Окно поддержки закрыто")
                                    return True
                                break
                        except:
                            continue
                except Exception as e:
                    logging.debug(f"Ошибка поиска через pywinauto: {e}")
            
            # МЕТОД 3: Tab навигация с проверкой текста кнопок через GetWindowText
            if continue_button_hwnd is None:
                logging.info("Поиск кнопки 'Продолжить' через Tab навигацию...")
                
                # Собираем все кнопки в окне
                all_buttons = []
                def collect_buttons(child_hwnd, results):
                    try:
                        class_name = win32gui.GetClassName(child_hwnd)
                        if "Button" in class_name:
                            text = win32gui.GetWindowText(child_hwnd)
                            results.append((child_hwnd, text))
                    except:
                        pass
                    return True
                
                win32gui.EnumChildWindows(hwnd, collect_buttons, all_buttons)
                
                # Ищем кнопку "Продолжить" среди всех кнопок
                for btn_hwnd, btn_text in all_buttons:
                    if "Продолжить" in btn_text or "Continue" in btn_text:
                        continue_button_hwnd = btn_hwnd
                        logging.info(f"✓ Кнопка 'Продолжить' найдена в списке кнопок: '{btn_text}'")
                        break
                
                if continue_button_hwnd:
                    # Отправляем BM_CLICK
                    BM_CLICK = 0x00F5
                    win32api.SendMessage(continue_button_hwnd, BM_CLICK, 0, 0)
                    logging.info("✓ Отправлено BM_CLICK сообщение к кнопке 'Продолжить'")
                    time.sleep(0.5)
                    
                    if not win32gui.IsWindow(hwnd):
                        logging.info("✓ Окно поддержки закрыто")
                        return True
                
                # Если не нашли напрямую, используем Tab навигацию
                # Перебираем все кнопки через Tab и проверяем их текст
                for i in range(len(all_buttons) + 1):  # +1 на случай, если нужно вернуться к началу
                    # Получаем текущую активную кнопку (фокус)
                    focused_hwnd = win32gui.GetFocus()
                    if focused_hwnd:
                        try:
                            focused_text = win32gui.GetWindowText(focused_hwnd)
                            if "Продолжить" in focused_text or "Continue" in focused_text:
                                logging.info(f"✓ Кнопка 'Продолжить' найдена через Tab (попытка {i+1}): '{focused_text}'")
                                time.sleep(0.2)
                                pyautogui.press('enter')
                                logging.info("✓ Нажат Enter на кнопке 'Продолжить'")
                                time.sleep(0.5)
                                
                                if not win32gui.IsWindow(hwnd):
                                    logging.info("✓ Окно поддержки закрыто")
                                    return True
                                break
                        except:
                            pass
                    
                    # Нажимаем Tab для перехода к следующей кнопке
                    if i < len(all_buttons):
                        pyautogui.press('tab')
                        time.sleep(0.2)
            
            # Если все методы не сработали
            if win32gui.IsWindow(hwnd):
                logging.error("✗ Не удалось закрыть окно поддержки Sandboxie")
                return False
            else:
                logging.info("✓ Окно поддержки закрыто")
                return True
                
        except Exception as e:
            logging.error(f"✗ Ошибка при закрытии окна поддержки: {e}")
            return False
    
    def wait_and_select_sandbox(self, sandbox_name: str, timeout: int = 10) -> bool:
        """
        Ожидание и выполнение выбора песочницы после закрытия окна поддержки
        
        Args:
            sandbox_name: Название песочницы (okno1, okno2 и т.д.)
            timeout: Максимальное время ожидания в секундах
        
        Returns:
            True если выбор выполнен успешно
        """
        logging.info(f"Ожидание диалога выбора песочницы для {sandbox_name}...")
        
        start_time = time.time()
        desktop = Desktop(backend="uia")
        
        while time.time() - start_time < timeout:
            elapsed = int(time.time() - start_time)
            
            # Ищем диалог выбора песочницы
            for win in desktop.windows():
                try:
                    if "Запустить в песочнице" in win.window_text():
                        logging.info(f"✓ Диалог выбора песочницы найден (через {elapsed} сек)")
                        
                        # Выбираем песочницу
                        sandbox_selected = False
                        for child in win.descendants():
                            try:
                                if child.window_text() == sandbox_name:
                                    child.click_input()
                                    logging.info(f"✓ Выбрали {sandbox_name}")
                                    time.sleep(0.1)
                                    sandbox_selected = True
                                    break
                            except:
                                continue
                        
                        if not sandbox_selected:
                            logging.warning(f"Песочница {sandbox_name} не найдена в списке")
                            return False
                        
                        # Галочка UAC
                        uac_checked = False
                        for child in win.descendants():
                            try:
                                text = child.window_text()
                                if "UAC" in text and "Администратор" in text:
                                    child.click_input()
                                    logging.info("✓ Галочка UAC")
                                    time.sleep(0.05)
                                    uac_checked = True
                                    break
                            except:
                                continue
                        
                        # OK
                        ok_clicked = False
                        for child in win.descendants():
                            try:
                                if child.window_text() == "OK":
                                    child.click_input()
                                    logging.info("✓ OK")
                                    time.sleep(0.5)
                                    ok_clicked = True
                                    break
                            except:
                                continue
                        
                        if ok_clicked:
                            logging.info("✓ Выбор песочницы выполнен успешно")
                            return True
                        else:
                            logging.warning("Кнопка OK не найдена")
                            return False
                except:
                    continue
            
            if elapsed % 2 == 0 and elapsed > 0:
                logging.info(f"Ожидание диалога выбора песочницы... ({elapsed}/{timeout} сек)")
            
            time.sleep(0.5)
        
        logging.warning(f"Диалог выбора песочницы не найден за {timeout} секунд")
        return False
    
    def check_and_close_sandboxie_error_dialog(self) -> bool:
        """
        Проверка и закрытие окна ошибок Sandboxie
        
        Окно "Сообщения от Sandboxie" может появиться в любой момент.
        Если найдено - закрываем его.
        """
        hwnd, title = find_window("Сообщения от Sandboxie", timeout=1)
        
        if hwnd and "Сообщения от Sandboxie" in title:
            logging.warning("⚠ Найдено окно ошибок Sandboxie! Закрываем...")
            
            try:
                # Ищем кнопку "Закрыть" или "Close"
                def find_close_button(child_hwnd, results):
                    try:
                        text = win32gui.GetWindowText(child_hwnd)
                        if "Закрыть" in text or "Close" in text:
                            results.append(child_hwnd)
                    except:
                        pass
                
                buttons = []
                win32gui.EnumChildWindows(hwnd, find_close_button, buttons)
                
                if buttons:
                    rect = win32gui.GetWindowRect(buttons[0])
                    x = (rect[0] + rect[2]) // 2
                    y = (rect[1] + rect[3]) // 2
                    
                    win32gui.SetForegroundWindow(hwnd)
                    time.sleep(0.2)
                    pyautogui.click(x, y)
                    logging.info(f"✓ Окно ошибок закрыто ({x}, {y})")
                    time.sleep(1)
                    return True
                else:
                    # Если кнопка не найдена, пробуем Alt+F4 или Escape
                    win32gui.SetForegroundWindow(hwnd)
                    time.sleep(0.2)
                    pyautogui.press('escape')
                    time.sleep(0.5)
                    logging.info("✓ Окно ошибок закрыто (Escape)")
                    return True
            except Exception as e:
                logging.error(f"Ошибка закрытия окна ошибок: {e}")
                return False
        
        return False
    
    def close_new_launcher_dialog(self) -> bool:
        """Закрыть диалог НОВЫЙ ЛАУНЧЕР"""
        logging.info("Закрытие НОВЫЙ ЛАУНЧЕР...")
        time.sleep(0.5)  # Уменьшено с 1.5 до 0.5
        
        hwnd, title = find_window("ЛАУНЧЕР", timeout=3)  # Уменьшено с 10 до 3
        
        if hwnd:
            logging.info(f"✓ Найден: {title}")
            
            # Активируем окно сразу
            try:
                win32gui.SetForegroundWindow(hwnd)
                time.sleep(0.1)
            except:
                pass
            
            # Находим кнопку Закрыть
            def find_close(child_hwnd, results):
                try:
                    text = win32gui.GetWindowText(child_hwnd)
                    if "Закрыть" in text:
                        results.append(child_hwnd)
                except:
                    pass
            
            buttons = []
            win32gui.EnumChildWindows(hwnd, find_close, buttons)
            
            if buttons:
                rect = win32gui.GetWindowRect(buttons[0])
                x = (rect[0] + rect[2]) // 2
                y = (rect[1] + rect[3]) // 2
                pyautogui.click(x, y)
                logging.info(f"✓ Закрыть ({x}, {y})")
                time.sleep(0.3)  # Уменьшено с 0.8 до 0.3
                return True
        
        logging.warning("Диалог не найден")
        return False
    
    def interact_with_launcher(self, server: str, nickname: str):
        """Работа с лаунчером: нажатие ИГРАТЬ (ник уже сохранен в окне)
        
        Returns:
            float: Время нажатия кнопки "ИГРАТЬ" (для отслеживания нового процесса)
            None: Если произошла ошибка
        """
        logging.info("Работа с лаунчером...")
        time.sleep(2)
        
        hwnd, title = find_window("RADMIR LAUNCHER", timeout=20)
        
        if not hwnd:
            logging.error("Лаунчер не найден")
            return None
        
        logging.info(f"✓ Лаунчер: {title}")
        
        # Активируем окно
        try:
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.3)
        except:
            pass
        
        # Ник уже сохранен в окне, просто переходим на кнопку ИГРАТЬ
        logging.info("Переход на кнопку ИГРАТЬ (Tab x12 + Space)...")
        pyautogui.press('tab', presses=12, interval=0.03)
        time.sleep(0.2)
        
        # Запоминаем время ПЕРЕД нажатием "ИГРАТЬ" (для отслеживания нового процесса)
        play_button_time = time.time()
        pyautogui.press('space')
        logging.info("✓ ИГРАТЬ нажата")
        time.sleep(1.5)
        
        logging.info("✓ Всё выполнено")
        return play_button_time  # Возвращаем время для отслеживания нового процесса
    
    def get_processes_by_name(self, process_name: str):
        """Получить все процессы с указанным именем с временем запуска"""
        processes = []
        try:
            import psutil
            for proc in psutil.process_iter(['pid', 'name', 'create_time']):
                try:
                    if proc.info['name'].lower() == process_name.lower():
                        processes.append({
                            'pid': proc.info['pid'],
                            'create_time': proc.info['create_time']
                        })
                except:
                    continue
        except ImportError:
            # Fallback: через wmic
            try:
                result = subprocess.run(
                    ['wmic', 'process', 'where', f'name="{process_name}"', 'get', 'ProcessId,CreationDate'],
                    capture_output=True,
                    text=True,
                    timeout=2
                )
                # Парсим результат (формат сложный, но можно упростить)
                if 'ProcessId' in result.stdout:
                    # Если wmic работает, считаем что процесс есть
                    # Но без точного времени создания
                    processes.append({'pid': 0, 'create_time': time.time()})
            except:
                pass
        
        return processes
    
    def find_newest_process(self, process_name: str, after_time: float) -> Optional[int]:
        """Найти самый свежий процесс, запущенный ПОСЛЕ указанного времени"""
        processes = self.get_processes_by_name(process_name)
        
        if not processes:
            return None
        
        # Фильтруем процессы, запущенные после указанного времени
        new_processes = [p for p in processes if p['create_time'] > after_time]
        
        if not new_processes:
            return None
        
        # Находим самый свежий (с максимальным временем создания)
        newest = max(new_processes, key=lambda x: x['create_time'])
        return newest['pid']
    
    def get_window_by_process_id(self, pid: int, window_title_filter: Optional[str] = None) -> Optional[int]:
        """
        Найти окно по PID процесса (даже если окно свернуто)
        
        Строго ищет окно по указанному PID, не возвращает первое попавшееся.
        Приоритет у окна, соответствующего фильтру.
        
        Args:
            pid: PID процесса
            window_title_filter: Фильтр по названию окна (например, "RADMIR CRMP")
        
        Returns:
            HWND окна, которое точно принадлежит указанному PID, или None
        """
        result_hwnd = None
        
        def enum_callback(hwnd, results):
            try:
                # Получаем PID процесса, которому принадлежит окно
                _, window_pid = win32process.GetWindowThreadProcessId(hwnd)
                
                # СТРОГАЯ проверка: окно должно принадлежать ТОЧНО этому PID
                if window_pid != pid:
                    return
                
                # УБИРАЕМ проверку IsWindowVisible - ищем все окна, даже свернутые
                # Проверяем, что это не пустое окно
                title = win32gui.GetWindowText(hwnd)
                if not title:  # Пропускаем окна без заголовка
                    return
                
                # Пропускаем служебные окна
                if title in ['Default IME', 'MSCTFIME UI']:
                    return
                
                # Если указан фильтр, проверяем название
                if window_title_filter:
                    if window_title_filter.lower() in title.lower():
                        results.append((hwnd, title, True))  # True = соответствует фильтру
                    else:
                        results.append((hwnd, title, False))  # False = не соответствует фильтру
                else:
                    results.append((hwnd, title, True))  # Без фильтра - все подходят
            except:
                pass
        
        windows = []
        win32gui.EnumWindows(enum_callback, windows)
        
        if not windows:
            return None
        
        # Если есть несколько окон, приоритет у окна с фильтром
        if window_title_filter:
            # Сначала ищем окна, соответствующие фильтру
            for hwnd, title, matches_filter in windows:
                if matches_filter:
                    # Дополнительная проверка: убеждаемся, что PID правильный
                    try:
                        _, window_pid = win32process.GetWindowThreadProcessId(hwnd)
                        if window_pid == pid:
                            logging.debug(f"[get_window_by_process_id] Найдено окно по PID {pid} с фильтром '{window_title_filter}': {title} (hwnd: {hwnd})")
                            return hwnd
                    except:
                        continue
        
        # Если не нашли с фильтром или фильтра нет, возвращаем первое окно с правильным PID
        for hwnd, title, _ in windows:
            # Дополнительная проверка PID перед возвратом
            try:
                _, window_pid = win32process.GetWindowThreadProcessId(hwnd)
                if window_pid == pid:
                    logging.debug(f"[get_window_by_process_id] Найдено окно по PID {pid}: {title} (hwnd: {hwnd})")
                    return hwnd
            except:
                continue
        
        return None
    
    def find_radmir_crmp_window(self, gta_pid: int, timeout: int = 30, existing_hwnds: Optional[set] = None) -> Optional[int]:
        """
        Найти НОВОЕ окно "RADMIR CRMP", связанное с процессом gta_sa.exe
        
        Логика:
        1. Ищем окно "RADMIR CRMP" по названию
        2. Проверяем, что оно связано с процессом gta_sa.exe (PID)
        3. Проверяем, что это НОВОЕ окно (которого не было в existing_hwnds)
        4. Ждем появления окна
        """
        logging.info(f"Поиск НОВОГО окна 'RADMIR CRMP' для процесса gta_sa.exe (PID: {gta_pid})...")
        
        if existing_hwnds is None:
            existing_hwnds = set()
        
        start_time = time.time()
        check_interval = 0.5
        
        while time.time() - start_time < timeout:
            elapsed = int(time.time() - start_time)
            
            # Ищем окно "RADMIR CRMP"
            def enum_callback(hwnd, results):
                try:
                    if win32gui.IsWindowVisible(hwnd):
                        title = win32gui.GetWindowText(hwnd)
                        if "RADMIR" in title.upper() and "CRMP" in title.upper():
                            # Получаем PID процесса окна
                            _, window_pid = win32process.GetWindowThreadProcessId(hwnd)
                            results.append((hwnd, title, window_pid))
                except:
                    pass
            
            windows = []
            win32gui.EnumWindows(enum_callback, windows)
            
            if windows:
                # Проверяем, что окно связано с процессом gta_sa.exe и это НОВОЕ окно
                for hwnd, title, window_pid in windows:
                    # Проверяем, что это НОВОЕ окно (которого не было в списке)
                    if hwnd in existing_hwnds:
                        continue
                    
                    # Проверяем, что окно связано с нужным процессом (или его дочерним)
                    # Для начала просто проверим, что окно существует и видимо
                    try:
                        # Проверяем, что окно действительно видимо и имеет размер
                        rect = win32gui.GetWindowRect(hwnd)
                        window_width = rect[2] - rect[0]
                        window_height = rect[3] - rect[1]
                        
                        if window_width > 100 and window_height > 100:  # Минимальный размер
                            logging.info(f"✓ НОВОЕ окно 'RADMIR CRMP' найдено: {title} (PID: {window_pid}, {window_width}x{window_height})")
                            logging.info(f"  Найдено через {elapsed} секунд")
                            return hwnd
                    except:
                        pass
            
            if elapsed % 3 == 0 and elapsed > 0:
                logging.info(f"Ожидание НОВОГО окна 'RADMIR CRMP'... ({elapsed}/{timeout} сек)")
            
            time.sleep(check_interval)
        
        logging.warning(f"Новое окно 'RADMIR CRMP' не найдено за {timeout} секунд")
        return None
    
    def get_existing_windows(self):
        """Получить список существующих окон игры (только от процессов gta_sa.exe)"""
        existing_windows = []
        
        # Получаем все процессы gta_sa.exe
        gta_processes = self.get_processes_by_name("gta_sa.exe")
        gta_pids = {p['pid'] for p in gta_processes}
        
        logging.debug(f"[get_existing_windows] Найдено процессов gta_sa.exe: {len(gta_processes)}, PIDs: {gta_pids}")
        
        # Если процессов нет, возвращаем пустой список
        if not gta_pids:
            logging.debug(f"[get_existing_windows] Процессы gta_sa.exe не найдены")
            return existing_windows
        
        def enum_callback(hwnd, results):
            try:
                # Убираем проверку IsWindowVisible - ищем все окна, даже свернутые
                # Получаем PID процесса окна
                _, window_pid = win32process.GetWindowThreadProcessId(hwnd)
                # Проверяем, что окно принадлежит процессу gta_sa.exe
                if window_pid in gta_pids:
                    title = win32gui.GetWindowText(hwnd)
                    if title:  # Окно должно иметь заголовок
                        rect = win32gui.GetWindowRect(hwnd)
                        is_visible = win32gui.IsWindowVisible(hwnd)
                        results.append({
                            'hwnd': hwnd,
                            'title': title,
                            'rect': rect,
                            'pid': window_pid,
                            'visible': is_visible
                        })
            except Exception as e:
                logging.debug(f"[get_existing_windows] Ошибка при перечислении окна: {e}")
        
        win32gui.EnumWindows(enum_callback, existing_windows)
        logging.debug(f"[get_existing_windows] Найдено окон игры: {len(existing_windows)}")
        for win in existing_windows:
            # Определяем sandbox для каждого окна
            win_sandbox = self.find_sandbox_by_pid(win['pid'])
            logging.debug(f"  - PID {win['pid']}: {win['title']} -> sandbox: {win_sandbox} (видимо: {win.get('visible', 'unknown')})")
        return existing_windows
    
    def find_game_window_fullscreen(self, timeout: int = 30, after_time: float = 0) -> Optional[int]:
        """
        Поиск НОВОГО окна игры, появившегося ПОСЛЕ указанного времени
        
        Важно: отслеживает только НОВОЕ окно, чтобы не перепутать с другими аккаунтами
        
        Логика:
        1. Запоминаем существующие окна игры
        2. Ищем процесс gta_sa.exe, запущенный ПОСЛЕ указанного времени
        3. Ищем НОВОЕ окно игры (которого не было в списке)
        4. Возвращаем новое окно (не проверяем размеры - игра может быть растянута)
        """
        logging.info(f"Ожидание загрузки игры (максимум {timeout} секунд)...")
        
        start_time = time.time()
        check_interval = 1
        
        # Получаем размер экрана
        screen_width = win32api.GetSystemMetrics(0)
        screen_height = win32api.GetSystemMetrics(1)
        logging.info(f"Размер экрана: {screen_width}x{screen_height}")
        
        # Запоминаем существующие окна игры (чтобы найти только новое)
        existing_windows = self.get_existing_windows()
        existing_hwnds = {w['hwnd'] for w in existing_windows}
        logging.info(f"Найдено существующих окон игры: {len(existing_windows)}")
        
        # Запоминаем время для поиска нового процесса
        if after_time == 0:
            after_time = time.time()
        
        newest_process_pid = None
        
        while time.time() - start_time < timeout:
            elapsed = int(time.time() - start_time)
            
            # Шаг 1: Ищем НОВЫЙ процесс gta_sa.exe (запущенный после after_time)
            if newest_process_pid is None:
                pid = self.find_newest_process("gta_sa.exe", after_time)
                if pid:
                    newest_process_pid = pid
                    logging.info(f"✓ Новый процесс gta_sa.exe найден (PID: {pid}, через {elapsed} сек)")
                elif elapsed % 5 == 0:
                    logging.info(f"Ожидание нового процесса gta_sa.exe... ({elapsed}/{timeout} сек)")
            
            # Шаг 2: Ищем окно "RADMIR CRMP" (подпроцесс gta_sa.exe, где находится поле для пароля)
            if newest_process_pid:
                # Сначала пробуем найти окно "RADMIR CRMP"
                radmir_hwnd = self.find_radmir_crmp_window(newest_process_pid, timeout=min(10, timeout - elapsed))
                
                if radmir_hwnd:
                    return radmir_hwnd
                
                # Если не нашли "RADMIR CRMP", ищем любое окно процесса gta_sa.exe
                game_hwnd = self.get_window_by_process_id(newest_process_pid)
                
                if game_hwnd:
                    try:
                        game_title = win32gui.GetWindowText(game_hwnd)
                        rect = win32gui.GetWindowRect(game_hwnd)
                        window_width = rect[2] - rect[0]
                        window_height = rect[3] - rect[1]
                        
                        logging.info(f"✓ Окно игры найдено по PID {newest_process_pid}: {game_title} ({window_width}x{window_height})")
                        logging.info(f"  Найдено через {elapsed} секунд (ожидаем появления 'RADMIR CRMP')")
                        # Возвращаем это окно, но будем искать "RADMIR CRMP" дальше
                        return game_hwnd
                    except Exception as e:
                        logging.debug(f"Ошибка получения информации об окне: {e}")
                        logging.info(f"✓ Окно игры найдено по PID {newest_process_pid}")
                        return game_hwnd
                elif elapsed % 5 == 0:
                    logging.info(f"Ожидание окна для процесса PID {newest_process_pid}... ({elapsed}/{timeout} сек)")
            
            time.sleep(check_interval)
        
        # Если не нашли новое окно, но процесс есть - продолжаем
        if newest_process_pid:
            logging.info("Новый процесс найден, но новое окно еще не появилось. Продолжаем...")
            return None
        
        logging.warning(f"Игра не найдена за {timeout} секунд")
        return None
    
    def find_edit_field_recursive(self, parent_hwnd: int, max_depth: int = 10, current_depth: int = 0) -> list:
        """Рекурсивный поиск всех полей Edit в окне и его дочерних окнах"""
        edit_fields = []
        
        if current_depth >= max_depth:
            return edit_fields
        
        # Список для хранения дочерних окон для рекурсивного поиска
        child_windows = []
        
        def enum_callback(child_hwnd, results):
            try:
                class_name = win32gui.GetClassName(child_hwnd)
                
                # Проверяем, является ли это полем Edit
                if "Edit" in class_name:
                    if win32gui.IsWindowVisible(child_hwnd):
                        # Получаем текст поля (может быть пустым, но это нормально)
                        try:
                            text = win32gui.GetWindowText(child_hwnd)
                            # Проверяем размеры поля (должно быть видимым)
                            rect = win32gui.GetWindowRect(child_hwnd)
                            width = rect[2] - rect[0]
                            height = rect[3] - rect[1]
                            
                            if width > 10 and height > 10:  # Минимальный размер
                                results.append({
                                    'hwnd': child_hwnd,
                                    'class': class_name,
                                    'text': text,
                                    'rect': rect
                                })
                        except:
                            pass
                
                # Сохраняем дочерние окна для рекурсивного поиска
                child_windows.append(child_hwnd)
            except:
                pass
        
        # Ищем поля Edit в текущем уровне
        win32gui.EnumChildWindows(parent_hwnd, enum_callback, edit_fields)
        
        # Рекурсивно ищем в дочерних окнах
        if current_depth < max_depth - 1:
            for child_hwnd in child_windows:
                try:
                    child_edits = self.find_edit_field_recursive(child_hwnd, max_depth, current_depth + 1)
                    edit_fields.extend(child_edits)
                except:
                    continue
        
        return edit_fields
    
    def find_button_by_ocr(self, window_hwnd: int, button_text: str) -> Optional[tuple]:
        """
        Поиск кнопки по тексту через OCR с поиском синего контура
        
        Args:
            window_hwnd: Handle окна
            button_text: Текст кнопки для поиска
        
        Returns:
            (x, y) координаты центра кнопки с синим контуром, или None если не найдено
        """
        try:
            import pytesseract
            from PIL import ImageGrab
            import numpy as np
            import cv2
            
            # Настраиваем путь к Tesseract
            tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
            if os.path.exists(tesseract_path):
                pytesseract.pytesseract.tesseract_cmd = tesseract_path
            
            # Получаем координаты окна
            rect = win32gui.GetWindowRect(window_hwnd)
            left, top, right, bottom = rect
            window_width = right - left
            window_height = bottom - top
            
            # Делаем скриншот области окна
            screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
            
            # Конвертируем в numpy array для OpenCV
            img_array = np.array(screenshot)
            img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            
            # ШАГ 1: Сначала находим текст кнопки "Продолжить" через OCR
            img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
            try:
                ocr_data = pytesseract.image_to_data(img_gray, lang='rus+eng', output_type=pytesseract.Output.DICT)
            except:
                ocr_data = pytesseract.image_to_data(img_gray, lang='eng', output_type=pytesseract.Output.DICT)
            
            button_text_lower = button_text.lower()
            
            # Ищем текст кнопки в OCR результатах
            found_texts = []
            for i, text in enumerate(ocr_data.get('text', [])):
                if text and button_text_lower in text.lower():
                    x = ocr_data['left'][i]
                    y = ocr_data['top'][i]
                    w = ocr_data['width'][i]
                    h = ocr_data['height'][i]
                    found_texts.append({
                        'text': text,
                        'bbox': (x, y, x + w, y + h),
                        'center': (x + w // 2, y + h // 2)
                    })
            
            if not found_texts:
                logging.debug(f"Текст '{button_text}' не найден через OCR")
                return None
            
            # ШАГ 2: Для каждого найденного текста "Продолжить" проверяем, есть ли вокруг него синий контур
            # Синий контур означает, что кнопка выделена (активна)
            
            # Метод 1: HSV для поиска синего цвета (рамка обычно яркая и насыщенная)
            hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
            # Диапазон для яркого синего (рамка кнопки Windows обычно RGB ~0, 120, 215 или похожий)
            lower_blue_hsv = np.array([100, 150, 150])  # Яркий насыщенный синий
            upper_blue_hsv = np.array([130, 255, 255])
            blue_mask_hsv = cv2.inRange(hsv, lower_blue_hsv, upper_blue_hsv)
            
            # Метод 2: RGB - ищем области где синий канал доминирует
            blue_channel = img_bgr[:, :, 0]  # B канал
            green_channel = img_bgr[:, :, 1]  # G канал
            red_channel = img_bgr[:, :, 2]  # R канал
            # Рамка кнопки: синий > 150, синий значительно больше красного и зеленого
            blue_contour_mask_rgb = (blue_channel > 150) & (blue_channel > red_channel + 40) & (blue_channel > green_channel + 40)
            blue_contour_mask_rgb = blue_contour_mask_rgb.astype(np.uint8) * 255
            
            # Объединяем маски
            combined_mask = cv2.bitwise_or(blue_mask_hsv, blue_contour_mask_rgb)
            
            # Морфологические операции для улучшения контуров
            kernel = np.ones((3, 3), np.uint8)
            combined_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_CLOSE, kernel)
            combined_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_OPEN, kernel)
            
            # Находим все синие контуры
            contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # ШАГ 3: Для каждого текста "Продолжить" проверяем, есть ли вокруг него синий контур
            for text_info in found_texts:
                text_x1, text_y1, text_x2, text_y2 = text_info['bbox']
                text_center_x, text_center_y = text_info['center']
                
                # Ищем контур, который содержит этот текст
                for contour in contours:
                    x_cont, y_cont, w_cont, h_cont = cv2.boundingRect(contour)
                    cont_x2 = x_cont + w_cont
                    cont_y2 = y_cont + h_cont
                    
                    # Проверяем размер контура (рамка кнопки обычно 50-300x15-60 пикселей)
                    if not (50 <= w_cont <= 300 and 15 <= h_cont <= 60):
                        continue
                    
                    # Проверяем, находится ли текст СТРОГО внутри этого контура
                    # Текст должен быть полностью внутри с небольшим отступом (рамка обычно имеет отступ)
                    margin = 3  # Небольшой отступ для рамки
                    if (x_cont + margin <= text_x1 and text_x2 <= cont_x2 - margin and
                        y_cont + margin <= text_y1 and text_y2 <= cont_y2 - margin):
                        # Текст строго внутри синего контура - это выделенная кнопка!
                        contour_center_x = x_cont + w_cont // 2
                        contour_center_y = y_cont + h_cont // 2
                        button_x = left + contour_center_x
                        button_y = top + contour_center_y
                        logging.info(f"✓ Кнопка '{button_text}' найдена через OCR с синим контуром: ({button_x}, {button_y})")
                        return (button_x, button_y)
                    
                    # Более мягкая проверка: центр текста внутри контура
                    if (x_cont <= text_center_x <= cont_x2 and 
                        y_cont <= text_center_y <= cont_y2):
                        contour_center_x = x_cont + w_cont // 2
                        contour_center_y = y_cont + h_cont // 2
                        button_x = left + contour_center_x
                        button_y = top + contour_center_y
                        logging.info(f"✓ Кнопка '{button_text}' найдена через OCR (центр текста в синем контуре): ({button_x}, {button_y})")
                        return (button_x, button_y)
            
            # Если не нашли через OCR+контур, просто возвращаем None
            return None
            
        except ImportError:
            logging.debug("OCR библиотеки не установлены, пропускаем проверку")
            return None
        except Exception as e:
            logging.debug(f"Ошибка OCR поиска кнопки: {e}")
            return None
    
    def detect_password_field_ocr(self, game_hwnd: int) -> bool:
        """
        Определение готовности поля пароля через OCR (распознавание текста на экране)
        
        Для игр с DirectX/OpenGL стандартные методы не работают.
        Используем OCR для поиска текста "Введите пароль" на экране.
        """
        try:
            import pytesseract
            from PIL import ImageGrab
            import numpy as np
            import cv2
            
            # Настраиваем путь к Tesseract
            tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
            if os.path.exists(tesseract_path):
                pytesseract.pytesseract.tesseract_cmd = tesseract_path
            
            # Получаем координаты окна
            rect = win32gui.GetWindowRect(game_hwnd)
            left, top, right, bottom = rect
            
            # Делаем скриншот области окна
            screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
            
            # Конвертируем в numpy array для OpenCV
            img_array = np.array(screenshot)
            img_gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            
            # Используем OCR для поиска текста
            # Пробуем найти "Введите пароль", "пароль", "password" и т.д.
            try:
                text = pytesseract.image_to_string(img_gray, lang='rus+eng')
            except:
                # Если русский язык не установлен, пробуем только английский
                text = pytesseract.image_to_string(img_gray, lang='eng')
            
            text_lower = text.lower()
            
            # Проверяем наличие ключевых слов
            keywords = ['введите пароль', 'пароль', 'password', 'enter password', 'введите']
            found = any(keyword in text_lower for keyword in keywords)
            
            if found:
                logging.info(f"✓ Текст 'Введите пароль' найден на экране через OCR")
                return True
            
            return False
            
        except ImportError:
            logging.debug("OCR библиотеки не установлены, пропускаем проверку")
            return False
        except Exception as e:
            logging.debug(f"Ошибка OCR: {e}")
            return False
    
    def detect_disconnect_ocr(self, game_hwnd: int) -> Optional[str]:
        """
        Определение отключения от сервера через OCR (распознавание текста на экране)
        
        Ищет тексты типа "Disconnected", "Connection lost", "Отключено" и т.д.
        
        Использует PrintWindow API для скриншота окна даже если оно свернуто/скрыто.
        Это позволяет мониторить каждое окно отдельно без разворачивания на экране.
        
        Returns:
            None если подключен, строка с причиной отключения если отключен
        """
        try:
            import pytesseract
            from PIL import Image
            import numpy as np
            import cv2
            
            # Настраиваем путь к Tesseract
            tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
            if os.path.exists(tesseract_path):
                pytesseract.pytesseract.tesseract_cmd = tesseract_path
            
            # Получаем размеры клиентской области окна (даже если оно свернуто)
            try:
                client_rect = win32gui.GetClientRect(game_hwnd)
                width = client_rect[2]
                height = client_rect[3]
            except:
                # Если не получилось, используем GetWindowRect
                rect = win32gui.GetWindowRect(game_hwnd)
                width = rect[2] - rect[0]
                height = rect[3] - rect[1]
            
            if width <= 0 or height <= 0:
                logging.debug(f"[OCR] Некорректные размеры окна: {width}x{height}")
                return None
            
            # Используем PrintWindow API для скриншота окна (работает даже если окно свернуто/скрыто)
            # Это позволяет мониторить каждое окно отдельно без разворачивания на экране
            try:
                # Создаем DC (Device Context) для окна
                hwndDC = win32gui.GetWindowDC(game_hwnd)
                if not hwndDC:
                    logging.debug(f"[OCR] Не удалось получить DC окна")
                    return None
                
                # Создаем совместимый DC в памяти
                mfcDC = win32gui.CreateCompatibleDC(hwndDC)
                if not mfcDC:
                    win32gui.ReleaseDC(game_hwnd, hwndDC)
                    logging.debug(f"[OCR] Не удалось создать совместимый DC")
                    return None
                
                # Создаем битмап
                saveBitMap = win32gui.CreateCompatibleBitmap(hwndDC, width, height)
                if not saveBitMap:
                    win32gui.DeleteDC(mfcDC)
                    win32gui.ReleaseDC(game_hwnd, hwndDC)
                    logging.debug(f"[OCR] Не удалось создать битмап")
                    return None
                
                # Выбираем битмап в DC
                win32gui.SelectObject(mfcDC, saveBitMap)
                
                # Используем PrintWindow для копирования содержимого окна в битмап
                # PW_RENDERFULLCONTENT = 0x00000002 - полное содержимое (для DWM)
                result = ctypes.windll.user32.PrintWindow(
                    game_hwnd, 
                    mfcDC, 
                    0x00000002  # PW_RENDERFULLCONTENT
                )
                
                if not result:
                    # Если PrintWindow не сработал, пробуем без флага
                    result = ctypes.windll.user32.PrintWindow(game_hwnd, mfcDC, 0)
                
                if not result:
                    win32gui.DeleteObject(saveBitMap)
                    win32gui.DeleteDC(mfcDC)
                    win32gui.ReleaseDC(game_hwnd, hwndDC)
                    logging.debug(f"[OCR] PrintWindow не удалось скопировать окно")
                    return None
                
                # Конвертируем битмап в PIL Image
                bmpinfo = win32gui.GetObject(saveBitMap)
                bmpstr = win32gui.GetBitmapBits(saveBitMap, bmpinfo.bmWidthBytes * bmpinfo.bmHeight)
                
                screenshot = Image.frombuffer(
                    'RGB',
                    (bmpinfo.bmWidth, bmpinfo.bmHeight),
                    bmpstr, 'raw', 'BGRX', 0, 1
                )
                
                # Очищаем ресурсы
                win32gui.DeleteObject(saveBitMap)
                win32gui.DeleteDC(mfcDC)
                win32gui.ReleaseDC(game_hwnd, hwndDC)
                
            except Exception as e:
                logging.debug(f"[OCR] Ошибка PrintWindow, пробуем ImageGrab как fallback: {e}")
                # Fallback на ImageGrab если PrintWindow не работает (только для видимых окон)
                from PIL import ImageGrab
                rect = win32gui.GetWindowRect(game_hwnd)
                screenshot = ImageGrab.grab(bbox=(rect[0], rect[1], rect[2], rect[3]))
            
            # Конвертируем в numpy array для OpenCV
            img_array = np.array(screenshot)
            img_gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            
            # Используем OCR для поиска текста
            try:
                text = pytesseract.image_to_string(img_gray, lang='rus+eng')
            except:
                # Если русский язык не установлен, пробуем только английский
                text = pytesseract.image_to_string(img_gray, lang='eng')
            
            text_lower = text.lower()
            
            # Проверяем наличие ключевых слов отключения
            disconnect_keywords = [
                'disconnected', 'connection lost', 'lost connection',
                'отключено', 'потеряно соединение', 'соединение потеряно',
                'reconnecting', 'trying to reconnect', 'reconnecting to server',
                'повторяем подключение', 'переподключение',
                'connection timeout', 'timeout', 'таймаут соединения',
                'не удалось подключиться', 'failed to connect',
                'server connection failed', 'connection error',
                'ошибка соединения', 'ошибка подключения',
                # Кик администратором (только если есть "Вас" - значит именно вас кикнули)
                'вас кикнул', 'вас кикнули', 'вас выгнали', 'вас исключили',
                'you were kicked', 'you were banned', 'you have been kicked'
            ]
            
            # Специальная проверка для кика администратором - должно быть слово "Вас"
            kick_keywords = ['вас кикнул', 'вас кикнули', 'вас выгнали', 'вас исключили', 
                           'you were kicked', 'you were banned', 'you have been kicked']
            is_kick = any(kw in text_lower for kw in kick_keywords)
            
            # Для кика проверяем, что есть слово "вас" или "you" (именно вас, а не других)
            if is_kick:
                # Проверяем, что это именно про вас (есть "вас" или "you")
                if 'вас' in text_lower or 'you' in text_lower:
                    found_keywords = [kw for kw in kick_keywords if kw in text_lower]
                    reason_text = f"Кик администратором: {', '.join(found_keywords)}"
                    logging.warning(f"⚠ КИК АДМИНИСТРАТОРОМ ОБНАРУЖЕН через OCR: {found_keywords}")
                    return reason_text  # Возвращаем причину отключения
                else:
                    # Если нет слова "вас" - это кик другого игрока, игнорируем
                    logging.debug(f"[OCR] Найден текст о кике, но без слова 'вас' - это не про вас, игнорируем")
            
            # Проверяем остальные ключевые слова отключения
            other_keywords = [kw for kw in disconnect_keywords if kw not in kick_keywords]
            found = any(keyword in text_lower for keyword in other_keywords)
            
            if found:
                # Найдено ключевое слово отключения - логируем что именно найдено
                found_keywords = [kw for kw in other_keywords if kw in text_lower]
                reason_text = ", ".join(found_keywords)
                logging.warning(f"⚠ ОТКЛЮЧЕНИЕ ОБНАРУЖЕНО через OCR: {found_keywords}")
                return reason_text  # Возвращаем причину отключения
            
            return None  # Не обнаружено отключение
            
        except ImportError:
            logging.debug("OCR библиотеки не установлены, пропускаем проверку")
            return None
        except Exception as e:
            logging.debug(f"Ошибка OCR проверки отключения: {e}")
            return None
    
    def check_process_network_activity(self, pid: int, check_duration: int = 5) -> tuple[bool, Optional[str]]:
        """
        Проверка сетевой активности процесса в течение указанного времени

        Проверяет наличие TCP соединений в течение check_duration секунд.
        Если в течение всего времени не было ни одного пакета - фиксирует проблему.

        Args:
            pid: PID процесса
            check_duration: Длительность проверки в секундах (по умолчанию 30)

        Returns:
            (True, None) если есть сетевая активность, (False, reason) если нет пакетов в течение всего времени
        """
        try:
            import psutil
            proc = psutil.Process(pid)
            
            # Проверяем, что процесс еще работает
            if not proc.is_running():
                return False, "Процесс не запущен"
            
            # Проверяем наличие пакетов в течение check_duration секунд
            start_time = time.time()
            check_interval = 1  # Проверяем каждую секунду (быстрее)
            found_connections = False
            failed_checks = 0  # Счетчик неудачных проверок подряд
            
            while time.time() - start_time < check_duration:
                try:
                    # Получаем сетевые соединения процесса
                    connections = proc.connections(kind='tcp')
                    
                    # Фильтруем только ESTABLISHED соединения (активные)
                    established = [conn for conn in connections if conn.status == psutil.CONN_ESTABLISHED]
                    
                    if established:
                        # Нашли активные соединения - процесс подключен
                        logging.debug(f"[Сеть] PID {pid}: найдено {len(established)} активных TCP соединений")
                        found_connections = True
                        break
                    else:
                        # Нет соединений в этой проверке
                        failed_checks += 1
                except (psutil.AccessDenied, psutil.NoSuchProcess):
                    # Не можем проверить соединения - считаем нормальным
                    logging.debug(f"[Сеть] PID {pid}: не удалось проверить соединения, но процесс работает")
                    return True, None
                except Exception as e:
                    logging.debug(f"[Сеть] PID {pid}: ошибка проверки соединений: {e}")
                
                # Ждем перед следующей проверкой
                time.sleep(check_interval)
            
            if found_connections:
                # Нашли соединения в течение проверки
                return True, None
            else:
                # В течение всего времени проверки не было ни одного пакета
                elapsed = time.time() - start_time
                logging.warning(f"[Сеть] PID {pid}: нет активных TCP соединений в течение {elapsed:.1f} секунд (неудачных проверок: {failed_checks})")
                return False, f"Нет активных TCP соединений в течение {check_duration} секунд (неудачных проверок: {failed_checks})"
                
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            logging.debug(f"[Сеть] Не удалось проверить сетевую активность PID {pid}: {e}")
            return False, f"Ошибка проверки сети: {e}"
        except Exception as e:
            logging.debug(f"[Сеть] Ошибка проверки сетевой активности PID {pid}: {e}")
            return False, f"Ошибка: {e}"
    
    def wake_up_window_by_movement(self, pid: int, account: Dict) -> bool:
        """
        Пробуждение окна через движение (если нет сетевых пакетов)
        
        Открывает окно по PID, зажимает W на 20 секунд, чтобы "пробудить" соединение.
        
        Args:
            pid: PID процесса игры
            account: Данные аккаунта
            
        Returns:
            True если окно найдено и движение выполнено
        """
        try:
            nickname = account.get('nickname', 'unknown')
            sandbox = account.get('sandbox', 'unknown')
            
            logging.info(f"[Пробуждение] Пробуждение окна для {nickname} (PID: {pid})...")
            
            # Находим окно по PID
            game_hwnd = self.get_window_by_process_id(pid, window_title_filter="RADMIR CRMP")
            if not game_hwnd:
                game_hwnd = self.get_window_by_process_id(pid)
            
            if not game_hwnd:
                logging.warning(f"[Пробуждение] ⚠ Окно не найдено для {nickname} (PID: {pid})")
                return False
            
            # Проверяем, что окно действительно принадлежит этому PID
            try:
                _, window_pid = win32process.GetWindowThreadProcessId(game_hwnd)
                if window_pid != pid:
                    logging.warning(f"[Пробуждение] ⚠ Несоответствие PID: окно {game_hwnd} принадлежит PID {window_pid}, ожидался {pid}")
                    return False
            except:
                pass
            
            logging.info(f"[Пробуждение] ✓ Окно найдено для {nickname} (hwnd: {game_hwnd}, PID: {pid})")
            
            # Используем метод send_key_to_window для движения (он уже активирует и разворачивает окно)
            logging.info(f"[Пробуждение] Зажимаю W на 20 секунд для пробуждения соединения...")
            
            # Проверяем, что auto_movement доступен
            if hasattr(self, 'auto_movement') and self.auto_movement:
                self.auto_movement.send_key_to_window(game_hwnd, 'w', 20.0)
            else:
                # Если auto_movement не доступен, создаем временный экземпляр
                temp_movement = AutoMovementManager()
                temp_movement.send_key_to_window(game_hwnd, 'w', 20.0)
            
            logging.info(f"[Пробуждение] ✓ Движение завершено для {nickname}")
            return True
            
        except Exception as e:
            logging.error(f"[Пробуждение] ✗ Ошибка пробуждения окна для {account.get('nickname', 'unknown')}: {e}")
            import traceback
            logging.debug(traceback.format_exc())
            return False
    
    def check_account_connection(self, account: Dict) -> tuple[bool, Optional[str]]:
        """
        Проверка подключения конкретного аккаунта
        
        Использует комбинированный подход:
        1. Проверка сохраненного PID процесса
        2. Проверка сетевой активности процесса (TCP соединения)
        3. Проверка окна через OCR (только если сеть не активна или OCR обнаружил отключение)
        
        ВАЖНО: Использует ТОЛЬКО сохраненный PID процесса для этого аккаунта
        (который был сохранен при запуске через process_account)
        
        Returns:
            (True, None) если подключен, (False, reason) если отключен
            reason - причина отключения для логирования
        """
        try:
            sandbox = account["sandbox"]
            nickname = account["nickname"]
            
            # Шаг 1: Находим сохраненный PID для этого аккаунта
            # ВАЖНО: Используем ТОЛЬКО сохраненный маппинг, не ищем по всем процессам!
            process_pid = None
            pids_to_remove = []  # Список PID для удаления (чтобы не изменять словарь во время итерации)
            
            if hasattr(self, '_pid_to_sandbox') and self._pid_to_sandbox:
                # Создаем копию словаря для безопасной итерации
                pid_to_sandbox_copy = dict(self._pid_to_sandbox)
                for pid, mapped_sandbox in pid_to_sandbox_copy.items():
                    if mapped_sandbox == sandbox:
                        # Проверяем, что процесс еще существует
                        try:
                            import psutil
                            proc = psutil.Process(pid)
                            if proc.is_running():
                                process_pid = pid
                                logging.debug(f"[Проверка] Найден сохраненный PID {pid} для {nickname} ({sandbox})")
                                break
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            # Процесс не существует, помечаем для удаления
                            logging.debug(f"[Проверка] Процесс PID {pid} не существует, помечаем для удаления из маппинга")
                            pids_to_remove.append(pid)
                        except Exception as e:
                            logging.debug(f"[Проверка] Ошибка проверки процесса PID {pid}: {e}")
            
            # Удаляем несуществующие PID из маппинга (после итерации)
            for pid in pids_to_remove:
                if hasattr(self, '_pid_to_sandbox'):
                    self._pid_to_sandbox.pop(pid, None)
                if hasattr(self, '_pid_to_account'):
                    self._pid_to_account.pop(pid, None)
            
            # Если сохраненный PID не найден - аккаунт отключен
            if not process_pid:
                reason = f"Сохраненный PID процесса не найден или процесс не запущен (sandbox: {sandbox})"
                logging.warning(f"[Проверка] {reason} для {nickname}")
                return False, reason
            
            # Шаг 2: Проверяем сетевую активность процесса (более надежный способ)
            # Используем счетчик неудачных проверок для отслеживания двух подряд неудач
            account_key = f"{nickname}_{sandbox}"
            if not hasattr(self, '_network_check_failures'):
                self._network_check_failures = {}  # account_key -> количество неудачных проверок подряд
            
            network_active, network_reason = self.check_process_network_activity(process_pid, check_duration=5)
            
            if network_active:
                # Есть сетевая активность - процесс точно подключен
                # Сбрасываем счетчик неудачных проверок
                self._network_check_failures.pop(account_key, None)
                logging.debug(f"[Проверка] ✓ {nickname} подключен (PID: {process_pid}, есть TCP соединения)")
                return True, None
            
            # Нет сетевой активности - увеличиваем счетчик неудачных проверок
            failure_count = self._network_check_failures.get(account_key, 0) + 1
            self._network_check_failures[account_key] = failure_count
            logging.debug(f"[Проверка] {nickname}: нет сетевой активности (неудачных проверок подряд: {failure_count})")
            
            # Если два раза подряд нет пакетов - пробуем "пробудить" окно
            if failure_count >= 2:
                logging.warning(f"[Проверка] ⚠ {nickname}: нет пакетов {failure_count} раза подряд, пробуем пробудить окно...")
                
                # Пробуем пробудить окно через движение
                wake_success = self.wake_up_window_by_movement(process_pid, account)
                
                if wake_success:
                    # Ждем немного после движения (быстрее)
                    time.sleep(1)
                    
                    # Перепроверяем сетевую активность (быстрее)
                    network_active_after, network_reason_after = self.check_process_network_activity(process_pid, check_duration=5)
                    
                    if network_active_after:
                        # После пробуждения появились пакеты - все в порядке
                        self._network_check_failures.pop(account_key, None)
                        logging.info(f"[Проверка] ✓ {nickname}: после пробуждения появились пакеты, соединение восстановлено")
                        return True, None
                    else:
                        # После пробуждения все еще нет пакетов - нужно перезапустить
                        logging.warning(f"[Проверка] ⚠ {nickname}: после пробуждения все еще нет пакетов, требуется перезапуск")
                        self._network_check_failures.pop(account_key, None)  # Сбрасываем счетчик перед перезапуском
                        # Возвращаем False с явным указанием, что требуется перезапуск
                        return False, f"ТРЕБУЕТСЯ ПЕРЕЗАПУСК: Нет пакетов после пробуждения окна: {network_reason_after}"
                else:
                    # Не удалось пробудить окно - возможно окно не найдено
                    logging.warning(f"[Проверка] ⚠ {nickname}: не удалось пробудить окно, требуется перезапуск")
                    self._network_check_failures.pop(account_key, None)  # Сбрасываем счетчик перед перезапуском
                    # Возвращаем False с явным указанием, что требуется перезапуск
                    return False, f"ТРЕБУЕТСЯ ПЕРЕЗАПУСК: Не удалось пробудить окно: {network_reason}"
            
            # Если только один раз нет пакетов - считаем нормальным (может быть временная пауза)
            logging.debug(f"[Проверка] {nickname}: нет пакетов (проверка #{failure_count}), ждем следующей проверки")
            return True, None  # Пока не критично, ждем следующей проверки
                
        except Exception as e:
            error_msg = f"Ошибка проверки подключения: {e}"
            logging.error(f"[Проверка] {error_msg} для {account.get('nickname', 'unknown')}")
            # При ошибке НЕ считаем отключенным - это может быть временная проблема
            # Лучше пропустить проверку, чем перезапускать без причины
            return True, None
    
    def check_process_stability(self, pid: int, check_duration: int = 3) -> bool:
        """
        Проверка стабильности процесса (CPU usage снизился = игра загрузилась)
        """
        try:
            import psutil
            proc = psutil.Process(pid)
            
            # Измеряем CPU usage в течение check_duration секунд
            cpu_samples = []
            for _ in range(check_duration * 2):  # Проверяем каждые 0.5 сек
                try:
                    cpu_percent = proc.cpu_percent(interval=0.5)
                    cpu_samples.append(cpu_percent)
                except:
                    pass
            
            if not cpu_samples:
                return False
            
            # Если средний CPU usage низкий (< 5%) или стабильный - игра загрузилась
            avg_cpu = sum(cpu_samples) / len(cpu_samples)
            if avg_cpu < 5.0:
                logging.info(f"✓ Процесс стабилен (CPU: {avg_cpu:.1f}%)")
                return True
            
            return False
            
        except Exception as e:
            logging.debug(f"Ошибка проверки стабильности процесса: {e}")
            return False
    
    def wait_for_password_field_ready(self, game_hwnd: int, timeout: int = 45) -> bool:
        """
        Ожидание появления поля "Введите пароль" в игре
        
        Для игр с DirectX/OpenGL стандартные методы поиска Windows-контролов не работают.
        Используем комбинированный подход:
        1. OCR для поиска текста "Введите пароль" на экране
        2. Проверка стабильности процесса (CPU usage снизился)
        3. Активация окна и проверка готовности
        """
        logging.info("Ожидание появления поля 'Введите пароль' в игре...")
        
        # Активируем окно игры
        try:
            win32gui.SetForegroundWindow(game_hwnd)
            time.sleep(0.3)
            logging.info("✓ Окно игры активировано")
        except Exception as e:
            logging.debug(f"Ошибка активации окна: {e}")
        
        start_time = time.time()
        check_interval = 1.0  # Проверяем каждую секунду
        
        # Получаем PID процесса для проверки стабильности
        try:
            _, process_pid = win32process.GetWindowThreadProcessId(game_hwnd)
        except:
            process_pid = None
        
        last_ocr_check = 0
        ocr_check_interval = 3  # Проверяем OCR каждые 3 секунды (чтобы не нагружать систему)
        
        while time.time() - start_time < timeout:
            elapsed = int(time.time() - start_time)
            
            # Метод 1: OCR для поиска текста "Введите пароль" (каждые 3 секунды)
            if elapsed - last_ocr_check >= ocr_check_interval:
                if self.detect_password_field_ocr(game_hwnd):
                    logging.info(f"✓ Поле 'Введите пароль' готово (найдено через OCR, через {elapsed} сек)")
                    time.sleep(0.5)  # Небольшая задержка для стабильности
                    return True
                last_ocr_check = elapsed
            
            # Метод 2: Проверка стабильности процесса (CPU usage снизился)
            if process_pid and elapsed >= 5:  # Начинаем проверять после 5 секунд
                if self.check_process_stability(process_pid, check_duration=2):
                    logging.info(f"✓ Игра загрузилась (процесс стабилен, через {elapsed} сек)")
                    # Дополнительная проверка OCR
                    if self.detect_password_field_ocr(game_hwnd):
                        logging.info("✓ Поле 'Введите пароль' готово (найдено через OCR)")
                        return True
                    # Если OCR не нашел, но процесс стабилен - все равно продолжаем
                    # (поле может быть готово, но OCR не распознал)
                    logging.info("✓ Игра загрузилась, поле должно быть готово")
                    time.sleep(1)
                    return True
            
            # Метод 3: Рекурсивный поиск через win32gui (на случай, если это стандартный контрол)
            try:
                edit_fields = self.find_edit_field_recursive(game_hwnd, max_depth=10)
                if edit_fields:
                    logging.info(f"✓ Поле Edit найдено через win32gui (через {elapsed} сек)")
                    return True
            except:
                pass
            
            # Проверка окна ошибок Sandboxie во время ожидания
            if self.check_and_close_sandboxie_error_dialog():
                logging.warning("⚠ Окно ошибок Sandboxie обнаружено во время ожидания!")
                # Продолжаем, но это может означать проблему
            
            # Логируем прогресс
            if elapsed % 5 == 0 and elapsed > 0:
                logging.info(f"Ожидание поля 'Введите пароль'... ({elapsed}/{timeout} сек)")
            
            time.sleep(check_interval)
        
        # Если не нашли за timeout, но окно есть - все равно продолжаем
        # (поле может быть готово, но методы не сработали)
        logging.warning(f"Поле 'Введите пароль' не найдено за {timeout} секунд, но продолжаем...")
        logging.info("Поле должно быть готово (окно игры активно)")
        return True
    
    def wait_for_password_field(self, timeout: int = 30, after_time: float = 0) -> Optional[int]:
        """
        Ожидание нового окна игры и поля для пароля
        
        Логика:
        1. Запоминает существующие окна "RADMIR CRMP"
        2. Находит процесс gta_sa.exe, запущенный ПОСЛЕ нажатия "ИГРАТЬ" (after_time)
        3. Находит НОВОЕ окно "RADMIR CRMP" (которого не было в списке)
        4. Ждет появления поля "Введите пароль" в новом окне "RADMIR CRMP"
        5. Проверяет, что поле готово к вводу
        """
        # Запоминаем существующие окна "RADMIR CRMP" (чтобы найти только новое)
        existing_windows = []
        def enum_callback(hwnd, results):
            try:
                if win32gui.IsWindowVisible(hwnd):
                    title = win32gui.GetWindowText(hwnd)
                    if "RADMIR" in title.upper() and "CRMP" in title.upper():
                        results.append(hwnd)
            except:
                pass
        
        win32gui.EnumWindows(enum_callback, existing_windows)
        existing_hwnds = set(existing_windows)
        logging.info(f"Найдено существующих окон 'RADMIR CRMP': {len(existing_windows)}")
        
        # Находим НОВЫЙ процесс gta_sa.exe (запущенный после after_time)
        if after_time == 0:
            after_time = time.time()
        
        newest_process_pid = None
        start_time = time.time()
        
        while time.time() - start_time < 10:  # Ждем процесс максимум 10 секунд
            pid = self.find_newest_process("gta_sa.exe", after_time)
            if pid:
                newest_process_pid = pid
                logging.info(f"✓ НОВЫЙ процесс gta_sa.exe найден (PID: {pid})")
                break
            time.sleep(0.5)
        
        if not newest_process_pid:
            logging.warning("Новый процесс gta_sa.exe не найден")
            return None
        
        # Ищем НОВОЕ окно "RADMIR CRMP" (которого не было в списке)
        radmir_hwnd = self.find_radmir_crmp_window(newest_process_pid, timeout=timeout, existing_hwnds=existing_hwnds)
        
        if not radmir_hwnd:
            logging.warning("Новое окно 'RADMIR CRMP' не найдено, но продолжаем...")
            # Fallback: ищем любое окно процесса (но это может быть старое окно!)
            radmir_hwnd = self.get_window_by_process_id(newest_process_pid, window_title_filter="RADMIR CRMP")
            if not radmir_hwnd:
                return None
        
        # Теперь ждем появления поля для пароля в окне "RADMIR CRMP"
        if self.wait_for_password_field_ready(radmir_hwnd, timeout=timeout):
            return radmir_hwnd
        
        # Если поле не найдено, все равно возвращаем окно
        logging.warning("Поле не найдено, но окно 'RADMIR CRMP' есть, продолжаем...")
        return radmir_hwnd
    
    def enter_game_password(self, password: str, after_time: float = 0, account_index: int = 0) -> tuple[bool, Optional[int]]:
        """
        Ввод пароля в игре с ожиданием появления поля
        
        Args:
            password: Пароль для ввода
            after_time: Время нажатия "ИГРАТЬ", чтобы отслеживать только новый процесс
            account_index: Индекс аккаунта (0-based) для определения таймаута
        
        Returns:
            (success: bool, pid: Optional[int]) - успех операции и PID процесса игры
        """
        # Определяем таймаут в зависимости от номера окна
        # Окна 1-6 (индексы 0-5): 30 секунд
        # Окна 7-10 (индексы 6-9): 60 секунд (1 минута)
        # Окна 11-15 (индексы 10-14): 120 секунд (2 минуты)
        if account_index < 6:
            timeout = 30
        elif account_index < 10:
            timeout = 60
        else:
            timeout = 120
        
        logging.info(f"Ожидание загрузки игры (таймаут: {timeout} секунд для окна #{account_index + 1})...")
        
        # Ждем появления нового окна игры и поля для пароля
        game_hwnd = self.wait_for_password_field(timeout=timeout, after_time=after_time)
        
        if not game_hwnd:
            logging.error("✗ Окно игры не найдено! Не могу ввести пароль.")
            return False, None
        
        # Получаем PID из окна игры (это правильный PID нового процесса)
        try:
            _, game_pid = win32process.GetWindowThreadProcessId(game_hwnd)
            logging.debug(f"[Ввод пароля] PID окна игры: {game_pid}")
        except:
            game_pid = None
            logging.warning("[Ввод пароля] Не удалось получить PID из окна игры")
        
        # Окно найдено, активируем его
        try:
            win32gui.SetForegroundWindow(game_hwnd)
            game_title = win32gui.GetWindowText(game_hwnd)
            logging.info(f"✓ Окно игры активировано: {game_title}")
            time.sleep(0.3)
        except:
            pass
        
        # Дополнительная небольшая задержка для стабильности
        time.sleep(0.5)
        
        # Вводим пароль
        logging.info("Ввод пароля...")
        try:
            from pywinauto.keyboard import send_keys
            send_keys(password, with_spaces=False, pause=0.1)
        except:
            # Fallback: через pyautogui
            pyautogui.typewrite(password, interval=0.1)
        
        time.sleep(0.5)
        pyautogui.press('enter')
        logging.info("✓ Пароль введен и нажат Enter")
        
        # Задержка перед повторным нажатием Enter для спавна
        time.sleep(2)
        pyautogui.press('enter')
        logging.info("✓ Нажат Enter для спавна")
        
        # ВАЖНО: Снова меняем время на год назад после входа в игру (иначе крашит)
        logging.info("6. Изменение времени после входа в игру (важно для стабильности)...")
        time.sleep(2)  # Небольшая пауза после входа
        self.time_manager.shift_time_back(self.config["time_shift_years"])
        logging.info("✓ Время изменено после входа в игру")
        time.sleep(2)
        
        return True, game_pid
    
    def get_account_index(self, account: Dict) -> int:
        """Получить индекс аккаунта в списке accounts"""
        try:
            accounts = self.config.get("accounts", [])
            for i, acc in enumerate(accounts):
                if acc.get("sandbox") == account.get("sandbox") and acc.get("nickname") == account.get("nickname"):
                    return i
            return 0  # По умолчанию 0, если не найден
        except:
            return 0
    
    def process_account(self, account: Dict, retry_count: int = 0, account_index: Optional[int] = None) -> bool:
        """
        Обработка аккаунта
        
        Args:
            account: Данные аккаунта
            retry_count: Количество попыток (для ретрая при ошибке Sandboxie)
            account_index: Индекс аккаунта для тайминга (если None, определяется автоматически)
        """
        try:
            sandbox = account["sandbox"]
            nickname = account["nickname"]
            server = account["server"]
            password = self.config["common_password"]
            
            logging.info("="*60)
            logging.info(f"{nickname} в {sandbox} на {server}")
            if retry_count > 0:
                logging.info(f"Повторная попытка #{retry_count}")
            logging.info("="*60)
            
            # Инициализируем маппинги PID -> account и PID -> sandbox
            if not hasattr(self, '_pid_to_account'):
                self._pid_to_account = {}
            if not hasattr(self, '_pid_to_sandbox'):
                self._pid_to_sandbox = {}
            
            # Постоянная проверка окна ошибок Sandboxie (в начале)
            if self.check_and_close_sandboxie_error_dialog():
                logging.warning("⚠ Окно ошибок Sandboxie обнаружено! Начинаем аккаунт заново...")
                time.sleep(2)
                # Рекурсивно вызываем себя заново (максимум 3 попытки)
                if retry_count < 3:
                    return self.process_account(account, retry_count=retry_count + 1)
                else:
                    logging.error(f"✗ Превышено максимальное количество попыток для {nickname}")
                    return False
            
            # 1. Время
            logging.info("1. Изменение времени...")
            self.time_manager.shift_time_back(self.config["time_shift_years"])
            time.sleep(2)
            
            # Проверка окна ошибок
            if self.check_and_close_sandboxie_error_dialog():
                logging.warning("⚠ Окно ошибок Sandboxie обнаружено! Начинаем аккаунт заново...")
                time.sleep(2)
                if retry_count < 3:
                    return self.process_account(account, retry_count=retry_count + 1)
                else:
                    logging.error(f"✗ Превышено максимальное количество попыток для {nickname}")
                    return False
            
            # 2. Запуск в Sandboxie
            logging.info("2. Запуск в Sandboxie...")
            if not self.sandboxie.launch(self.config["launcher_path"], sandbox):
                return False
            
            # Запоминаем открытые окна проводника
            if hasattr(self.sandboxie, 'opened_explorer_windows'):
                self.opened_explorer_windows.extend(self.sandboxie.opened_explorer_windows)
            
            # 2.1. Проверка и закрытие окна поддержки Sandboxie (если появилось)
            support_dialog_closed = self.check_and_close_sandboxie_support_dialog()
            
            # Если окно поддержки было закрыто, нужно дождаться и выполнить выбор песочницы
            if support_dialog_closed:
                logging.info("Окно поддержки было закрыто, проверяем диалог выбора песочницы...")
                if not self.wait_and_select_sandbox(sandbox, timeout=10):
                    logging.error("✗ Не удалось выполнить выбор песочницы после закрытия окна поддержки! Перезапускаем аккаунт...")
                    time.sleep(2)
                    if retry_count < 3:
                        return self.process_account(account, retry_count=retry_count + 1)
                    else:
                        logging.error(f"✗ Превышено максимальное количество попыток для {nickname}")
                        return False
            
            # Проверка окна ошибок после запуска
            if self.check_and_close_sandboxie_error_dialog():
                logging.warning("⚠ Окно ошибок Sandboxie обнаружено! Начинаем аккаунт заново...")
                time.sleep(2)
                if retry_count < 3:
                    return self.process_account(account, retry_count=retry_count + 1)
                else:
                    logging.error(f"✗ Превышено максимальное количество попыток для {nickname}")
                    return False
            
            # 3. Закрыть НОВЫЙ ЛАУНЧЕР
            logging.info("3. Закрытие НОВЫЙ ЛАУНЧЕР...")
            if not self.close_new_launcher_dialog():
                logging.warning("⚠ Диалог НОВЫЙ ЛАУНЧЕР не найден, но продолжаем...")
                # Не перезапускаем, так как диалог может быть уже закрыт
            
            # Проверка окна ошибок после закрытия диалога
            if self.check_and_close_sandboxie_error_dialog():
                logging.warning("⚠ Окно ошибок Sandboxie обнаружено! Начинаем аккаунт заново...")
                time.sleep(2)
                if retry_count < 3:
                    return self.process_account(account, retry_count=retry_count + 1)
                else:
                    logging.error(f"✗ Превышено максимальное количество попыток для {nickname}")
                    return False
            
            # 4. Работа с лаунчером
            logging.info("4. Работа с лаунчером...")
            play_button_time = self.interact_with_launcher(server, nickname)
            if not play_button_time:
                logging.error("✗ Не удалось выполнить работу с лаунчером! Перезапускаем аккаунт...")
                time.sleep(2)
                if retry_count < 3:
                    return self.process_account(account, retry_count=retry_count + 1)
                else:
                    logging.error(f"✗ Превышено максимальное количество попыток для {nickname}")
                    return False
            
            # Проверка окна ошибок после работы с лаунчером
            if self.check_and_close_sandboxie_error_dialog():
                logging.warning("⚠ Окно ошибок Sandboxie обнаружено! Начинаем аккаунт заново...")
                time.sleep(2)
                if retry_count < 3:
                    return self.process_account(account, retry_count=retry_count + 1)
                else:
                    logging.error(f"✗ Превышено максимальное количество попыток для {nickname}")
                    return False
            
            # 5. Пароль в игре (передаем время нажатия "ИГРАТЬ" для отслеживания нового процесса)
            # Получаем индекс аккаунта из списка всех аккаунтов для определения таймаута
            # Если account_index не передан, определяем автоматически
            if account_index is None:
                account_index = self.get_account_index(account)
            logging.info("5. Ввод пароля...")
            password_success, game_pid = self.enter_game_password(password, after_time=play_button_time, account_index=account_index)
            
            if not password_success:
                logging.error("✗ Не удалось ввести пароль")
                return False
            
            # Сохраняем маппинг PID -> account для мониторинга отключений
            # ВАЖНО: Используем PID из окна игры, которое мы уже нашли (это правильный PID нового процесса)
            logging.info("6. Поиск и сохранение PID процесса игры...")
            
            new_process_pid = game_pid
            
            # Если PID не был получен из окна, пробуем найти другим способом
            if not new_process_pid:
                logging.warning(f"⚠ PID не получен из окна, пробуем найти через find_newest_process...")
                for attempt in range(10):  # Пробуем 10 раз с интервалом 1 секунда
                    time.sleep(1)
                    new_process_pid = self.find_newest_process("gta_sa.exe", play_button_time)
                    if new_process_pid:
                        # Проверяем, что процесс действительно существует
                        try:
                            import psutil
                            proc = psutil.Process(new_process_pid)
                            if proc.is_running():
                                logging.info(f"✓ Процесс найден: PID {new_process_pid} (попытка {attempt + 1})")
                                break
                        except:
                            pass
                    if attempt % 3 == 2:
                        logging.debug(f"Ожидание процесса gta_sa.exe... (попытка {attempt + 1}/10)")
                
                # Если не нашли через find_newest_process, пробуем найти через окно игры
                if not new_process_pid:
                    logging.warning(f"⚠ Не удалось найти процесс через find_newest_process, пробуем через окно...")
                    time.sleep(3)
                    
                    # Ищем окно игры и определяем PID через него
                    game_windows = self.get_existing_windows()
                    for window_info in game_windows:
                        window_pid = window_info['pid']
                        # Пробуем определить sandbox для этого PID
                        window_sandbox = self.find_sandbox_by_pid(window_pid)
                        if window_sandbox == sandbox:
                            new_process_pid = window_pid
                            logging.info(f"✓ Процесс найден через окно: PID {new_process_pid} -> {sandbox}")
                            break
                    
                    # Если все еще не нашли, берем последний несохраненный процесс
                    if not new_process_pid and game_windows:
                        unmapped_windows = [w for w in game_windows if w['pid'] not in (self._pid_to_sandbox if hasattr(self, '_pid_to_sandbox') else {})]
                        if unmapped_windows:
                            new_process_pid = unmapped_windows[0]['pid']
                            logging.warning(f"⚠ Используем предположительный PID {new_process_pid} (не найден точный маппинг)")
            
            if new_process_pid:
                # Сохраняем маппинг PID -> account и PID -> sandbox
                if not hasattr(self, '_pid_to_account'):
                    self._pid_to_account = {}
                if not hasattr(self, '_pid_to_sandbox'):
                    self._pid_to_sandbox = {}
                
                self._pid_to_account[new_process_pid] = account
                self._pid_to_sandbox[new_process_pid] = sandbox
                logging.info(f"✓ Маппинг сохранен: PID {new_process_pid} -> {nickname} ({sandbox})")
                
                # Проверяем, что процесс действительно существует
                try:
                    import psutil
                    proc = psutil.Process(new_process_pid)
                    if proc.is_running():
                        logging.info(f"✓ Процесс подтвержден: PID {new_process_pid} запущен")
                        
                        # Добавляем аккаунт в очередь ожидания движения (запустится после всех аккаунтов)
                        if self.auto_movement.enabled:
                            self.auto_movement.add_pending_account(self, account, new_process_pid)
                    else:
                        logging.warning(f"⚠ Процесс PID {new_process_pid} не запущен")
                except Exception as e:
                    logging.warning(f"⚠ Ошибка проверки процесса PID {new_process_pid}: {e}")
            else:
                logging.error(f"✗ Не удалось найти процесс gta_sa.exe для {nickname} ({sandbox})")
                logging.error(f"✗ Маппинг не сохранен - мониторинг отключений может работать некорректно")
            
            # Финальная проверка окна ошибок
            if self.check_and_close_sandboxie_error_dialog():
                logging.warning("⚠ Окно ошибок Sandboxie обнаружено после ввода пароля!")
                # Не перезапускаем, так как пароль уже введен
            
            logging.info(f"✓ Аккаунт {nickname} готов!")
            return True
            
        except Exception as e:
            logging.error(f"Ошибка: {e}")
            # Проверяем окно ошибок при исключении
            self.check_and_close_sandboxie_error_dialog()
            return False
    
    def close_opened_explorer_windows(self):
        """Закрыть все открытые окна проводника"""
        # Инициализируем список, если его нет
        if not hasattr(self, 'opened_explorer_windows'):
            self.opened_explorer_windows = []
        
        # Собираем все окна проводника (из списка и находим все открытые)
        all_explorer_windows = []
        
        # Добавляем сохраненные окна
        if self.opened_explorer_windows:
            all_explorer_windows.extend(self.opened_explorer_windows)
        
        # Также находим все открытые окна проводника с RADMIR в названии
        def find_explorer_windows(hwnd, results):
            try:
                if win32gui.IsWindowVisible(hwnd):
                    title = win32gui.GetWindowText(hwnd)
                    class_name = win32gui.GetClassName(hwnd)
                    # Проверяем, что это окно проводника
                    if ("CabinetWClass" in class_name or "ExplorerWClass" in class_name) and "RADMIR" in title.upper():
                        _, pid = win32process.GetWindowThreadProcessId(hwnd)
                        results.append((hwnd, pid, title))
            except:
                pass
        
        found_windows = []
        win32gui.EnumWindows(find_explorer_windows, found_windows)
        
        # Объединяем списки
        all_explorer_windows.extend(found_windows)
        
        if not all_explorer_windows:
            logging.info("Нет открытых окон проводника для закрытия")
            return
        
        logging.info(f"Закрытие {len(all_explorer_windows)} открытых окон проводника...")
        
        closed_count = 0
        for window_info in all_explorer_windows:
            try:
                if isinstance(window_info, tuple) and len(window_info) >= 1:
                    hwnd = window_info[0]
                    try:
                        title = win32gui.GetWindowText(hwnd)
                        if win32gui.IsWindowVisible(hwnd):
                            win32gui.SetForegroundWindow(hwnd)
                            time.sleep(0.2)
                            pyautogui.hotkey('alt', 'f4')
                            logging.info(f"✓ Закрыто окно проводника: {title}")
                            time.sleep(0.2)
                            closed_count += 1
                    except:
                        pass
            except Exception as e:
                logging.debug(f"Ошибка закрытия окна проводника: {e}")
        
        # Очищаем список
        self.opened_explorer_windows.clear()
        if hasattr(self.sandboxie, 'opened_explorer_windows'):
            self.sandboxie.opened_explorer_windows.clear()
        
        logging.info(f"✓ Закрыто {closed_count} окон проводника")
    
    def close_all_game_windows(self) -> int:
        """
        Закрыть все окна игр (gta_sa.exe)
        
        Returns:
            int: Количество закрытых окон
        """
        logging.info("Закрытие всех окон игр...")
        
        # Получаем все окна игр
        game_windows = self.get_existing_windows()
        
        if not game_windows:
            logging.info("Нет открытых окон игр для закрытия")
            return 0
        
        logging.info(f"Найдено {len(game_windows)} окон игр для закрытия")
        
        closed_count = 0
        for window_info in game_windows:
            try:
                hwnd = window_info['hwnd']
                title = window_info['title']
                pid = window_info['pid']
                
                if not win32gui.IsWindowVisible(hwnd):
                    continue
                
                # Пробуем закрыть окно через WM_CLOSE (корректное закрытие)
                try:
                    win32gui.SetForegroundWindow(hwnd)
                    time.sleep(0.2)
                    
                    # Отправляем сообщение WM_CLOSE
                    win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
                    time.sleep(0.5)
                    
                    # Проверяем, закрылось ли окно
                    if not win32gui.IsWindow(hwnd) or not win32gui.IsWindowVisible(hwnd):
                        logging.info(f"✓ Окно игры закрыто (WM_CLOSE): {title}")
                        closed_count += 1
                        continue
                except Exception as e:
                    logging.debug(f"Ошибка закрытия через WM_CLOSE: {e}")
                
                # Если WM_CLOSE не сработал, пробуем Alt+F4
                try:
                    win32gui.SetForegroundWindow(hwnd)
                    time.sleep(0.2)
                    pyautogui.hotkey('alt', 'f4')
                    time.sleep(0.5)
                    
                    if not win32gui.IsWindow(hwnd) or not win32gui.IsWindowVisible(hwnd):
                        logging.info(f"✓ Окно игры закрыто (Alt+F4): {title}")
                        closed_count += 1
                        continue
                except Exception as e:
                    logging.debug(f"Ошибка закрытия через Alt+F4: {e}")
                
                # Если ничего не помогло, принудительно завершаем процесс
                try:
                    import psutil
                    proc = psutil.Process(pid)
                    proc.terminate()
                    time.sleep(0.5)
                    logging.info(f"✓ Процесс игры завершен принудительно (PID: {pid}): {title}")
                    closed_count += 1
                except Exception as e:
                    logging.warning(f"Не удалось закрыть окно игры {title}: {e}")
                    
            except Exception as e:
                logging.debug(f"Ошибка закрытия окна игры: {e}")
        
        logging.info(f"✓ Закрыто {closed_count} окон игр из {len(game_windows)}")
        return closed_count
    
    def close_all_sandboxie_dialogs(self) -> int:
        """
        Закрыть все окна сообщений Sandboxie
        
        Returns:
            int: Количество закрытых окон
        """
        logging.info("Закрытие всех окон сообщений Sandboxie...")
        
        closed_count = 0
        max_attempts = 10  # Максимум попыток (на случай множественных окон)
        
        for attempt in range(max_attempts):
            # Ищем окна "Сообщения от Sandboxie"
            sandboxie_windows = []
            
            def enum_callback(hwnd, results):
                try:
                    if win32gui.IsWindowVisible(hwnd):
                        title = win32gui.GetWindowText(hwnd)
                        if "Сообщения от Sandboxie" in title or "Sandboxie Messages" in title:
                            results.append((hwnd, title))
                except:
                    pass
            
            win32gui.EnumWindows(enum_callback, sandboxie_windows)
            
            if not sandboxie_windows:
                break  # Больше нет окон
            
            # Закрываем найденные окна
            for hwnd, title in sandboxie_windows:
                try:
                    # Пробуем найти кнопку "Закрыть"
                    def find_close_button(child_hwnd, results):
                        try:
                            text = win32gui.GetWindowText(child_hwnd)
                            if "Закрыть" in text or "Close" in text:
                                results.append(child_hwnd)
                        except:
                            pass
                    
                    buttons = []
                    win32gui.EnumChildWindows(hwnd, find_close_button, buttons)
                    
                    if buttons:
                        rect = win32gui.GetWindowRect(buttons[0])
                        x = (rect[0] + rect[2]) // 2
                        y = (rect[1] + rect[3]) // 2
                        
                        win32gui.SetForegroundWindow(hwnd)
                        time.sleep(0.2)
                        pyautogui.click(x, y)
                        logging.info(f"✓ Окно Sandboxie закрыто (клик): {title}")
                        closed_count += 1
                        time.sleep(0.5)
                    else:
                        # Если кнопка не найдена, пробуем Escape или Alt+F4
                        win32gui.SetForegroundWindow(hwnd)
                        time.sleep(0.2)
                        pyautogui.press('escape')
                        time.sleep(0.3)
                        
                        # Проверяем, закрылось ли
                        if not win32gui.IsWindow(hwnd) or not win32gui.IsWindowVisible(hwnd):
                            logging.info(f"✓ Окно Sandboxie закрыто (Escape): {title}")
                            closed_count += 1
                        else:
                            # Пробуем Alt+F4
                            pyautogui.hotkey('alt', 'f4')
                            time.sleep(0.3)
                            if not win32gui.IsWindow(hwnd) or not win32gui.IsWindowVisible(hwnd):
                                logging.info(f"✓ Окно Sandboxie закрыто (Alt+F4): {title}")
                                closed_count += 1
                except Exception as e:
                    logging.debug(f"Ошибка закрытия окна Sandboxie: {e}")
            
            time.sleep(0.5)  # Небольшая задержка между попытками
        
        if closed_count > 0:
            logging.info(f"✓ Закрыто {closed_count} окон сообщений Sandboxie")
        else:
            logging.info("Нет открытых окон сообщений Sandboxie")
        
        return closed_count
    
    def close_all_launcher_windows(self) -> int:
        """
        Закрыть все окна лаунчеров (RADMIR LAUNCHER)
        
        Returns:
            int: Количество закрытых окон
        """
        logging.info("Закрытие всех окон лаунчеров...")
        
        launcher_windows = []
        
        def enum_callback(hwnd, results):
            try:
                if win32gui.IsWindowVisible(hwnd):
                    title = win32gui.GetWindowText(hwnd)
                    if "RADMIR" in title.upper() and "LAUNCHER" in title.upper():
                        _, pid = win32process.GetWindowThreadProcessId(hwnd)
                        results.append({
                            'hwnd': hwnd,
                            'title': title,
                            'pid': pid
                        })
            except:
                pass
        
        win32gui.EnumWindows(enum_callback, launcher_windows)
        
        if not launcher_windows:
            logging.info("Нет открытых окон лаунчеров для закрытия")
            return 0
        
        logging.info(f"Найдено {len(launcher_windows)} окон лаунчеров для закрытия")
        
        closed_count = 0
        for window_info in launcher_windows:
            try:
                hwnd = window_info['hwnd']
                title = window_info['title']
                pid = window_info['pid']
                
                if not win32gui.IsWindowVisible(hwnd):
                    continue
                
                # Пробуем закрыть окно через WM_CLOSE
                try:
                    win32gui.SetForegroundWindow(hwnd)
                    time.sleep(0.2)
                    win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
                    time.sleep(0.5)
                    
                    if not win32gui.IsWindow(hwnd) or not win32gui.IsWindowVisible(hwnd):
                        logging.info(f"✓ Окно лаунчера закрыто (WM_CLOSE): {title}")
                        closed_count += 1
                        continue
                except Exception as e:
                    logging.debug(f"Ошибка закрытия через WM_CLOSE: {e}")
                
                # Если WM_CLOSE не сработал, пробуем Alt+F4
                try:
                    win32gui.SetForegroundWindow(hwnd)
                    time.sleep(0.2)
                    pyautogui.hotkey('alt', 'f4')
                    time.sleep(0.5)
                    
                    if not win32gui.IsWindow(hwnd) or not win32gui.IsWindowVisible(hwnd):
                        logging.info(f"✓ Окно лаунчера закрыто (Alt+F4): {title}")
                        closed_count += 1
                        continue
                except Exception as e:
                    logging.debug(f"Ошибка закрытия через Alt+F4: {e}")
                
                # Если ничего не помогло, принудительно завершаем процесс
                try:
                    import psutil
                    proc = psutil.Process(pid)
                    proc.terminate()
                    time.sleep(0.5)
                    logging.info(f"✓ Процесс лаунчера завершен принудительно (PID: {pid}): {title}")
                    closed_count += 1
                except Exception as e:
                    logging.warning(f"Не удалось закрыть окно лаунчера {title}: {e}")
                    
            except Exception as e:
                logging.debug(f"Ошибка закрытия окна лаунчера: {e}")
        
        logging.info(f"✓ Закрыто {closed_count} окон лаунчеров из {len(launcher_windows)}")
        return closed_count
    
    def wait_until_time(self, target_minute: int) -> None:
        """
        Ожидание до указанной минуты часа
        
        Args:
            target_minute: Минута часа (0-59), до которой нужно ждать
        """
        while True:
            now = datetime.now()
            current_minute = now.minute
            
            if current_minute == target_minute:
                # Проверяем, что мы точно в нужной минуте (ждем секунду для точности)
                time.sleep(1)
                now = datetime.now()
                if now.minute == target_minute:
                    logging.info(f"✓ Достигнуто время {now.hour:02d}:{target_minute:02d}")
                    return
            
            # Логируем каждые 10 секунд
            if now.second % 10 == 0:
                logging.info(f"Ожидание времени :{target_minute:02d}... Текущее время: {now.hour:02d}:{now.minute:02d}:{now.second:02d}")
            
            time.sleep(1)
    
    def run_all_accounts(self, start_index: int = 0, end_index: Optional[int] = None):
        """
        Запуск автоматизации для всех аккаунтов (без финального закрытия окон)
        
        Args:
            start_index: Индекс начального аккаунта
            end_index: Индекс конечного аккаунта (None = все)
        
        Returns:
            list: Список аккаунтов, которые были успешно запущены
        """
        accounts = self.config["accounts"]
        
        if end_index is None:
            end_index = len(accounts)
        
        total = min(end_index, len(accounts)) - start_index
        logging.info("="*60)
        logging.info(f"ЗАПУСК АВТОМАТИЗАЦИИ ДЛЯ {total} АККАУНТОВ")
        logging.info("="*60)
        
        # Список успешно запущенных аккаунтов для мониторинга
        launched_accounts = []
        
        for i in range(start_index, min(end_index, len(accounts))):
            account = accounts[i]
            
            # Проверяем поле ban (по умолчанию "no" если отсутствует)
            ban_status = account.get("ban", "no").lower()
            if ban_status == "yes":
                logging.info("")
                logging.info(f">>> АККАУНТ {i+1}/{len(accounts)}: {account['nickname']} - ПРОПУЩЕН (ban: yes) <<<")
                logging.info("")
                continue
            
            logging.info("")
            logging.info(f">>> АККАУНТ {i+1}/{len(accounts)}: {account['nickname']} <<<")
            logging.info("")
            
            try:
                success = self.process_account(account)
                
                if success:
                    logging.info(f"✓ Аккаунт {i+1} ({account['nickname']}) успешно обработан")
                    # Добавляем в список запущенных аккаунтов
                    launched_accounts.append(account)
                else:
                    logging.error(f"✗ Ошибка при обработке аккаунта {i+1} ({account['nickname']})")
            except Exception as e:
                logging.error(f"✗ Критическая ошибка при обработке аккаунта {i+1} ({account['nickname']}): {e}")
                import traceback
                logging.error(traceback.format_exc())
                # Продолжаем со следующим аккаунтом
            
            # Пауза между аккаунтами (кроме последнего)
            if i < min(end_index, len(accounts)) - 1:
                logging.info(f"Пауза перед следующим аккаунтом...")
                time.sleep(2)
        
        logging.info("")
        logging.info("="*60)
        logging.info("АВТОМАТИЗАЦИЯ ЗАВЕРШЕНА!")
        logging.info(f"Успешно запущено аккаунтов: {len(launched_accounts)}")
        logging.info("="*60)
        
        # Проверяем все запущенные аккаунты после завершения
        if len(launched_accounts) > 0:
            logging.info("")
            logging.info("="*60)
            logging.info("ПРОВЕРКА ВСЕХ ЗАПУЩЕННЫХ АККАУНТОВ")
            logging.info("="*60)
            self.verify_and_restart_accounts(launched_accounts)
        
        # Запускаем движение для всех аккаунтов (если включено)
        if self.auto_movement.enabled and len(launched_accounts) > 0:
            logging.info("")
            logging.info("="*60)
            logging.info("ЗАПУСК АВТОМАТИЧЕСКОГО ДВИЖЕНИЯ")
            logging.info("="*60)
            self.auto_movement.start_all_pending_movements()
        
        # Закрываем открытые окна проводника
        self.close_opened_explorer_windows()
        
        # Восстановление времени сразу после закрытия окон проводника
        logging.info("Восстановление времени через 60 секунд...")
        time.sleep(60)
        self.time_manager.restore_time()
        
        return launched_accounts
    
    def verify_and_restart_accounts(self, accounts: List[Dict]) -> None:
        """
        Проверка всех аккаунтов после запуска: PID процесса и сетевая активность
        
        Args:
            accounts: Список аккаунтов для проверки
        """
        logging.info("Начинаем проверку всех аккаунтов...")
        time.sleep(2)  # Короткая пауза после запуска всех аккаунтов (быстрее)
        
        problem_accounts = []
        
        for account in accounts:
            sandbox = account.get("sandbox")
            nickname = account.get("nickname")
            
            logging.info(f"Проверка аккаунта: {nickname} ({sandbox})...")
            
            # Проверяем подключение (основная проверка)
            is_connected, reason = self.check_account_connection(account)
            
            if not is_connected:
                logging.warning(f"⚠ Проблема с аккаунтом {nickname} ({sandbox}): {reason}")
                problem_accounts.append(account)
            else:
                # Дополнительно проверяем наличие PID
                pid = self.get_account_pid(account)
                if not pid:
                    logging.warning(f"⚠ PID не найден для аккаунта {nickname} ({sandbox})")
                    problem_accounts.append(account)
                else:
                    # Проверяем сетевую активность (быстрее - 5 секунд)
                    network_active, network_reason = self.check_process_network_activity(pid, check_duration=5)
                    if not network_active:
                        logging.warning(f"⚠ Нет сетевой активности для аккаунта {nickname} ({sandbox}): {network_reason}")
                        problem_accounts.append(account)
                    else:
                        logging.info(f"✓ Аккаунт {nickname} ({sandbox}) в порядке (PID: {pid}, есть сетевая активность)")
        
        # Перезапускаем проблемные аккаунты
        if problem_accounts:
            logging.info("")
            logging.info("="*60)
            logging.info(f"ОБНАРУЖЕНО ПРОБЛЕМ: {len(problem_accounts)} АККАУНТОВ")
            logging.info("="*60)
            
            for account in problem_accounts:
                nickname = account.get("nickname")
                sandbox = account.get("sandbox")
                logging.info(f"Перезапуск аккаунта: {nickname} ({sandbox})...")
                
                success = self.restart_account(account)
                if success:
                    logging.info(f"✓ Аккаунт {nickname} успешно перезапущен")
                else:
                    logging.error(f"✗ Не удалось перезапустить аккаунт {nickname}")
                
                time.sleep(1)  # Короткая пауза между перезапусками (быстрее)
        else:
            logging.info("")
            logging.info("="*60)
            logging.info("✓ ВСЕ АККАУНТЫ В ПОРЯДКЕ!")
            logging.info("="*60)
    
    def close_all_windows(self):
        """Закрыть все окна: игры, лаунчеры и сообщения Sandboxie"""
        logging.info("="*60)
        logging.info("ЗАКРЫТИЕ ВСЕХ ОКОН")
        logging.info("="*60)
        
        # Закрываем все окна игр
        game_closed = self.close_all_game_windows()
        
        # Закрываем все окна лаунчеров
        launcher_closed = self.close_all_launcher_windows()
        
        # Закрываем все окна сообщений Sandboxie
        sandboxie_closed = self.close_all_sandboxie_dialogs()
        
        logging.info("")
        logging.info(f"Итого закрыто: {game_closed} окон игр, {launcher_closed} окон лаунчеров, {sandboxie_closed} окон Sandboxie")
        logging.info("")
    
    def get_account_by_pid(self, pid: int) -> Optional[Dict]:
        """
        Найти аккаунт по PID процесса игры
        
        Args:
            pid: PID процесса gta_sa.exe
            
        Returns:
            Dict с данными аккаунта или None
        """
        try:
            # Метод 1: Используем сохраненный маппинг (самый надежный)
            if hasattr(self, '_pid_to_account'):
                account = self._pid_to_account.get(pid)
                if account:
                    return account
            
            # Метод 2: Определяем sandbox по PID и находим аккаунт
            sandbox = self.find_sandbox_by_pid(pid)
            if sandbox:
                return self.get_account_by_sandbox(sandbox)
                
        except Exception as e:
            logging.debug(f"Ошибка поиска аккаунта по PID: {e}")
        
        return None
    
    def get_account_by_sandbox(self, sandbox_name: str) -> Optional[Dict]:
        """Найти аккаунт по названию песочницы"""
        for account in self.config["accounts"]:
            if account["sandbox"] == sandbox_name:
                return account
        return None
    
    def find_sandbox_by_pid(self, pid: int) -> Optional[str]:
        """
        Определить песочницу по PID процесса
        
        Args:
            pid: PID процесса gta_sa.exe
            
        Returns:
            Название песочницы или None
        """
        try:
            # Метод 1: Используем сохраненный маппинг (самый надежный)
            if hasattr(self, '_pid_to_sandbox') and self._pid_to_sandbox:
                sandbox = self._pid_to_sandbox.get(pid)
                if sandbox:
                    logging.debug(f"[find_sandbox_by_pid] PID {pid} -> {sandbox} (из маппинга)")
                    return sandbox
            
            # Метод 2: Пробуем найти через Sandboxie Control API (если доступен)
            try:
                import subprocess
                # Используем Sandboxie Control для определения sandbox процесса
                # SbieCtrl.exe queryprocess <pid> возвращает информацию о процессе
                sbie_paths = [
                    'C:\\Program Files\\Sandboxie\\SbieCtrl.exe',
                    'C:\\Program Files (x86)\\Sandboxie\\SbieCtrl.exe',
                    self.config.get("sandboxie_start", "").replace("Start.exe", "SbieCtrl.exe")
                ]
                
                sbie_found = False
                for sbie_path in sbie_paths:
                    if not sbie_path or not os.path.exists(sbie_path):
                        continue
                    
                    try:
                        result = subprocess.run(
                            [sbie_path, 'queryprocess', str(pid)],
                            capture_output=True,
                            text=True,
                            timeout=3
                        )
                        if result.returncode == 0 and result.stdout:
                            # Парсим вывод SbieCtrl - ищем название sandbox
                            output_lower = result.stdout.lower()
                            for account in self.config["accounts"]:
                                sandbox = account["sandbox"]
                                # Ищем sandbox в выводе (может быть в разных форматах)
                                if sandbox.lower() in output_lower:
                                    # Сохраняем маппинг
                                    if not hasattr(self, '_pid_to_sandbox'):
                                        self._pid_to_sandbox = {}
                                    self._pid_to_sandbox[pid] = sandbox
                                    logging.debug(f"[find_sandbox_by_pid] PID {pid} -> {sandbox} (через SbieCtrl)")
                                    return sandbox
                            sbie_found = True
                            break
                    except Exception as e:
                        logging.debug(f"[find_sandbox_by_pid] Ошибка SbieCtrl {sbie_path}: {e}")
                        continue
                
                if not sbie_found:
                    logging.debug(f"[find_sandbox_by_pid] SbieCtrl не доступен или не нашел sandbox для PID {pid}")
            except Exception as e:
                logging.debug(f"[find_sandbox_by_pid] Общая ошибка SbieCtrl: {e}")
            
            # Метод 3: Ищем через путь к процессу
            try:
                import psutil
                proc = psutil.Process(pid)
                exe_path = proc.exe()
                
                # Ищем в пути название песочницы (okno1, okno2 и т.д.)
                for account in self.config["accounts"]:
                    sandbox = account["sandbox"]
                    # Проверяем, есть ли sandbox в пути (может быть в разных местах)
                    if sandbox.lower() in exe_path.lower():
                        # Сохраняем маппинг для будущего использования
                        if not hasattr(self, '_pid_to_sandbox'):
                            self._pid_to_sandbox = {}
                        self._pid_to_sandbox[pid] = sandbox
                        logging.debug(f"[find_sandbox_by_pid] PID {pid} -> {sandbox} (через путь: {exe_path})")
                        return sandbox
                
                # Метод 4: Ищем через рабочую директорию процесса
                try:
                    cwd = proc.cwd()
                    for account in self.config["accounts"]:
                        sandbox = account["sandbox"]
                        if sandbox.lower() in cwd.lower():
                            if not hasattr(self, '_pid_to_sandbox'):
                                self._pid_to_sandbox = {}
                            self._pid_to_sandbox[pid] = sandbox
                            logging.debug(f"[find_sandbox_by_pid] PID {pid} -> {sandbox} (через CWD: {cwd})")
                            return sandbox
                except:
                    pass
            except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                logging.debug(f"[find_sandbox_by_pid] Не удалось получить информацию о процессе {pid}: {e}")
            except Exception as e:
                logging.debug(f"[find_sandbox_by_pid] Ошибка при работе с процессом {pid}: {e}")
                
        except Exception as e:
            logging.debug(f"[find_sandbox_by_pid] Общая ошибка определения sandbox по PID {pid}: {e}")
        
        logging.debug(f"[find_sandbox_by_pid] Не удалось определить sandbox для PID {pid}")
        return None
    
    def get_account_pid(self, account: Dict) -> Optional[int]:
        """
        Получить PID процесса для аккаунта
        
        Args:
            account: Данные аккаунта
            
        Returns:
            PID процесса или None
        """
        try:
            import psutil
            sandbox = account.get("sandbox")
            nickname = account.get("nickname")
            
            # Пробуем найти через сохраненный маппинг
            if hasattr(self, '_pid_to_account'):
                for pid, acc_info in self._pid_to_account.items():
                    if acc_info.get('sandbox') == sandbox and acc_info.get('nickname') == nickname:
                        # Проверяем, что процесс еще существует
                        try:
                            psutil.Process(pid)
                            return pid
                        except:
                            continue
            
            # Пробуем найти через find_sandbox_by_pid
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'] == 'gta_sa.exe':
                    pid = proc.info['pid']
                    found_sandbox = self.find_sandbox_by_pid(pid)
                    if found_sandbox == sandbox:
                        return pid
            
            return None
        except Exception as e:
            logging.debug(f"Ошибка получения PID для аккаунта: {e}")
            return None
    
    def restart_account(self, account: Dict) -> bool:
        """
        Перезапуск конкретного аккаунта
        
        Сначала закрывает старое окно игры, затем перезапускает аккаунт.
        
        Args:
            account: Данные аккаунта для перезапуска
            
        Returns:
            True если перезапуск успешен
        """
        logging.info("")
        logging.info("="*60)
        logging.info(f"ПЕРЕЗАПУСК АККАУНТА: {account['nickname']} ({account['sandbox']})")
        logging.info("="*60)
        
        sandbox = account["sandbox"]
        nickname = account["nickname"]
        
        # Шаг 1: Находим и закрываем старое окно игры для этого аккаунта
        logging.info(f"[Перезапуск] Поиск старого окна игры для {nickname} ({sandbox})...")
        game_windows = self.get_existing_windows()
        
        # Находим окно игры для этого аккаунта (используем маппинг и find_sandbox_by_pid)
        target_pid = None
        target_hwnd = None
        old_pid = None  # Инициализируем old_pid заранее (может быть None, если старое окно не найдено)
        
        # Сначала пробуем через маппинг (самый надежный способ)
        if hasattr(self, '_pid_to_sandbox'):
            # Используем копию словаря для итерации, чтобы избежать изменения размера во время итерации
            pid_to_sandbox_copy = dict(self._pid_to_sandbox)
            pids_to_remove = []  # Собираем PIDs для удаления после итерации
            
            for pid, mapped_sandbox in pid_to_sandbox_copy.items():
                if mapped_sandbox == sandbox:
                    # Проверяем, что процесс еще существует
                    try:
                        import psutil
                        proc = psutil.Process(pid)
                        if proc.is_running():
                            target_pid = pid
                            # Находим hwnd для этого PID
                            for window_info in game_windows:
                                if window_info['pid'] == pid:
                                    target_hwnd = window_info['hwnd']
                                    break
                            logging.info(f"[Перезапуск] Найдено окно через маппинг: PID {pid}")
                            break
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        # Процесс уже не существует, удаляем из маппинга после итерации
                        pids_to_remove.append(pid)
            
            # Удаляем несуществующие процессы из маппинга после итерации
            for pid in pids_to_remove:
                self._pid_to_sandbox.pop(pid, None)
                if hasattr(self, '_pid_to_account'):
                    self._pid_to_account.pop(pid, None)
        
        # Если не нашли через маппинг, пробуем через find_sandbox_by_pid
        if not target_pid:
            for window_info in game_windows:
                window_pid = window_info['pid']
                window_sandbox = self.find_sandbox_by_pid(window_pid)
                if window_sandbox == sandbox:
                    target_pid = window_pid
                    target_hwnd = window_info['hwnd']
                    logging.info(f"[Перезапуск] Найдено окно через find_sandbox_by_pid: PID {window_pid}")
                    break
        
        # Шаг 2: Закрываем найденное окно
        if target_pid:
            logging.info(f"[Перезапуск] Закрытие старого окна игры (PID: {target_pid})...")
            
            closed = False
            
            # Метод 1: Пробуем закрыть через WM_CLOSE (самый мягкий способ)
            if target_hwnd:
                try:
                    win32gui.PostMessage(target_hwnd, win32con.WM_CLOSE, 0, 0)
                    logging.debug(f"[Перезапуск] Отправлен WM_CLOSE для окна {target_hwnd}")
                    time.sleep(2)
                    
                    # Проверяем, закрылось ли окно
                    if not win32gui.IsWindow(target_hwnd):
                        closed = True
                        logging.info(f"[Перезапуск] ✓ Окно закрыто через WM_CLOSE")
                except Exception as e:
                    logging.debug(f"[Перезапуск] Ошибка WM_CLOSE: {e}")
            
            # Метод 2: Если не закрылось, пробуем Alt+F4
            if not closed and target_hwnd:
                try:
                    win32gui.SetForegroundWindow(target_hwnd)
                    time.sleep(0.3)
                    pyautogui.hotkey('alt', 'f4')
                    time.sleep(2)
                    
                    if not win32gui.IsWindow(target_hwnd):
                        closed = True
                        logging.info(f"[Перезапуск] ✓ Окно закрыто через Alt+F4")
                except Exception as e:
                    logging.debug(f"[Перезапуск] Ошибка Alt+F4: {e}")
            
            # Метод 3: Если все еще не закрылось, принудительно завершаем процесс
            if not closed:
                try:
                    import psutil
                    proc = psutil.Process(target_pid)
                    proc.terminate()
                    time.sleep(1)
                    
                    # Проверяем, что процесс завершился
                    if not proc.is_running():
                        closed = True
                        logging.info(f"[Перезапуск] ✓ Процесс завершен принудительно (PID: {target_pid})")
                    else:
                        # Если не завершился, пробуем kill
                        proc.kill()
                        time.sleep(1)
                        if not proc.is_running():
                            closed = True
                            logging.info(f"[Перезапуск] ✓ Процесс убит принудительно (PID: {target_pid})")
                except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                    closed = True
                    logging.info(f"[Перезапуск] ✓ Процесс уже не существует (PID: {target_pid})")
                except Exception as e:
                    logging.warning(f"[Перезапуск] Ошибка принудительного завершения процесса: {e}")
            
            # Сохраняем old_pid для дальнейшего использования
            old_pid = target_pid if target_pid else None
            
            # Удаляем маппинг для закрытого процесса
            if target_pid:
                if hasattr(self, '_pid_to_sandbox'):
                    self._pid_to_sandbox.pop(target_pid, None)
                if hasattr(self, '_pid_to_account'):
                    self._pid_to_account.pop(target_pid, None)
            
            # Обновляем PID в auto_movement (удаляем старый, если есть)
            if old_pid and hasattr(self, 'auto_movement') and self.auto_movement.enabled:
                account_key = f"{nickname}_{sandbox}"
                # Удаляем старый PID из всех мест в auto_movement
                if hasattr(self.auto_movement, 'pending_accounts'):
                    self.auto_movement.pending_accounts = [
                        p for p in self.auto_movement.pending_accounts 
                        if p.get('pid') != old_pid and p.get('account_key') != account_key
                    ]
                if hasattr(self.auto_movement, 'account_pids'):
                    self.auto_movement.account_pids.pop(account_key, None)
                if hasattr(self.auto_movement, 'active_threads') and account_key in self.auto_movement.active_threads:
                    # Обновляем PID в active_threads (будет обновлен новым PID позже)
                    pass
                logging.info(f"[Перезапуск] Старый PID {old_pid} удален из auto_movement")
        
        # Шаг 3: Подсчитываем количество активных окон для определения тайминга
        active_windows_count = len(self.get_existing_windows())
        logging.info(f"[Перезапуск] Активных окон игры: {active_windows_count}")
        
        # Определяем индекс аккаунта для тайминга (на основе количества окон)
        # Если окон много, используем большие тайминги
        if active_windows_count < 7:
            account_index = active_windows_count - 1  # Окна 1-6: индексы 0-5
        elif active_windows_count < 11:
            account_index = active_windows_count - 1  # Окна 7-10: индексы 6-9
        else:
            account_index = active_windows_count - 1  # Окна 11+: индексы 10+
        
        # Шаг 4: Перезапускаем аккаунт (используем process_account с account_index для тайминга)
        logging.info(f"[Перезапуск] Запуск нового процесса для {nickname}...")
        try:
            success = self.process_account(account, retry_count=0, account_index=account_index)
            
            if success:
                logging.info(f"[Перезапуск] ✓ Аккаунт {nickname} успешно перезапущен")
                
                # Шаг 5: Обновляем PID в auto_movement с новым PID
                new_pid = self.get_account_pid(account)
                if new_pid:
                    if hasattr(self, 'auto_movement') and self.auto_movement.enabled:
                        account_key = f"{nickname}_{sandbox}"
                        
                        # Обновляем PID в active_threads (основное хранилище для движения)
                        if hasattr(self.auto_movement, 'active_threads'):
                            if account_key in self.auto_movement.active_threads:
                                self.auto_movement.active_threads[account_key]['pid'] = new_pid
                                logging.info(f"[Перезапуск] PID обновлен в active_threads: {account_key} -> {new_pid}")
                            else:
                                # Если аккаунта нет в active_threads, добавляем его
                                self.auto_movement.active_threads[account_key] = {
                                    'account': account,
                                    'pid': new_pid,
                                    'account_key': account_key,
                                    'automation_instance': self
                                }
                                logging.info(f"[Перезапуск] Аккаунт {nickname} добавлен в active_threads с новым PID {new_pid}")
                        
                        # Обновляем PID в account_pids (если используется)
                        if hasattr(self.auto_movement, 'account_pids'):
                            self.auto_movement.account_pids[account_key] = new_pid
                            logging.info(f"[Перезапуск] PID обновлен в account_pids: {account_key} -> {new_pid}")
                        
                        # Обновляем PID для всех остальных аккаунтов, которые могут использовать старый PID
                        if old_pid is not None and hasattr(self.auto_movement, 'active_threads'):
                            for other_key, other_info in list(self.auto_movement.active_threads.items()):
                                if other_info.get('pid') == old_pid and other_key != account_key:
                                    # Находим актуальный PID для этого аккаунта
                                    other_account = other_info.get('account')
                                    if other_account:
                                        other_sandbox = other_account.get('sandbox')
                                        other_nickname = other_account.get('nickname')
                                        actual_pid = self.get_account_pid(other_account)
                                        if actual_pid and actual_pid != old_pid:
                                            self.auto_movement.active_threads[other_key]['pid'] = actual_pid
                                            logging.info(f"[Перезапуск] Обновлен PID для {other_nickname}: {other_key} -> {actual_pid}")
                        
                        logging.info(f"[Перезапуск] PID обновлен в auto_movement: {account_key} -> {new_pid}")
                
                # Шаг 6: Восстанавливаем время через минуту после перезапуска
                logging.info(f"[Перезапуск] Восстановление времени через 60 секунд...")
                time.sleep(60)
                self.time_manager.restore_time()
                logging.info(f"[Перезапуск] ✓ Время восстановлено")
                
                return True
            else:
                logging.error(f"[Перезапуск] ✗ Ошибка при перезапуске аккаунта {nickname}")
                return False
        except Exception as e:
            logging.error(f"[Перезапуск] ✗ Критическая ошибка при перезапуске аккаунта {nickname}: {e}")
            import traceback
            logging.error(traceback.format_exc())
            return False
            if hasattr(self, '_pid_to_sandbox') and target_pid in self._pid_to_sandbox:
                del self._pid_to_sandbox[target_pid]
                logging.debug(f"[Перезапуск] Маппинг удален для PID {target_pid}")
            if hasattr(self, '_pid_to_account') and target_pid in self._pid_to_account:
                del self._pid_to_account[target_pid]
                logging.debug(f"[Перезапуск] Маппинг аккаунта удален для PID {target_pid}")
            
            # Ждем, пока окно полностью закроется
            time.sleep(2)
        else:
            logging.warning(f"[Перезапуск] ⚠ Старое окно игры не найдено для {nickname} ({sandbox})")
            logging.warning(f"[Перезапуск] Продолжаем перезапуск без закрытия старого окна")
        
        # Шаг 3: Подсчитываем количество активных окон для определения тайминга
        active_windows_count = len(self.get_existing_windows())
        logging.info(f"[Перезапуск] Активных окон игры: {active_windows_count}")
        
        # Определяем индекс аккаунта для тайминга (на основе количества окон)
        # Если окон много, используем большие тайминги
        if active_windows_count < 7:
            account_index = active_windows_count - 1  # Окна 1-6: индексы 0-5
        elif active_windows_count < 11:
            account_index = active_windows_count - 1  # Окна 7-10: индексы 6-9
        else:
            account_index = active_windows_count - 1  # Окна 11+: индексы 10+
        
        # Шаг 4: Небольшая пауза перед перезапуском
        logging.info(f"[Перезапуск] Пауза перед перезапуском...")
        time.sleep(3)
        
        # Шаг 5: Перезапускаем аккаунт (используем process_account)
        logging.info(f"[Перезапуск] Запуск нового процесса для {nickname}...")
        try:
            success = self.process_account(account, retry_count=0)
            
            if success:
                logging.info(f"[Перезапуск] ✓ Аккаунт {nickname} успешно перезапущен")
                
                # Шаг 6: Восстанавливаем время через минуту после перезапуска
                logging.info(f"[Перезапуск] Восстановление времени через 60 секунд...")
                time.sleep(60)
                self.time_manager.restore_time()
                logging.info(f"[Перезапуск] ✓ Время восстановлено")
                
                return True
            else:
                logging.error(f"[Перезапуск] ✗ Ошибка при перезапуске аккаунта {nickname}")
                return False
        except Exception as e:
            logging.error(f"[Перезапуск] ✗ Критическая ошибка при перезапуске аккаунта {nickname}: {e}")
            import traceback
            logging.error(traceback.format_exc())
            return False
    
    def monitor_disconnects(self, accounts_to_monitor: Optional[list] = None):
        """
        Мониторинг отключений через OCR (без Lua скриптов)
        
        Бесконечно проверяет указанные аккаунты по очереди через OCR,
        определяя отключение по текстам на экране игры.
        
        Args:
            accounts_to_monitor: Список аккаунтов для мониторинга (None = все из конфига)
        """
        # Если список не указан, используем все аккаунты из конфига
        if accounts_to_monitor is None:
            accounts_to_monitor = self.config["accounts"]
        
        logging.info("="*60)
        logging.info("МОНИТОРИНГ ОТКЛЮЧЕНИЙ ЧЕРЕЗ OCR")
        logging.info("="*60)
        logging.info(f"Мониторинг {len(accounts_to_monitor)} аккаунтов:")
        for acc in accounts_to_monitor:
            logging.info(f"  - {acc['nickname']} ({acc['sandbox']})")
        logging.info("")
        logging.info("Проверка отключений через распознавание текста на экране")
        logging.info("Триггеры: 'Disconnected', 'Connection lost', 'Отключено' и т.д.")
        logging.info("")
        
        check_interval = 10  # Проверяем каждые 10 секунд
        check_counter = 0
        
        # Счетчики для подтверждения отключения (нужно несколько проверок подряд)
        # Это защитит от ложных срабатываний OCR
        disconnect_confirmations = {}  # account_key -> количество подряд идущих проверок отключения
        
        while True:
            try:
                time.sleep(check_interval)
                check_counter += 1
                
                # Логируем каждую минуту (6 проверок по 10 секунд)
                if check_counter % 6 == 0:
                    logging.info(f"[Мониторинг] Проверка #{check_counter} - проверяю {len(accounts_to_monitor)} аккаунтов...")
                
                # Проверяем только указанные аккаунты
                for account in accounts_to_monitor:
                    sandbox = account["sandbox"]
                    nickname = account["nickname"]
                    account_key = f"{nickname}_{sandbox}"
                    
                    try:
                        # Проверяем подключение через OCR
                        is_connected, disconnect_reason = self.check_account_connection(account)
                        
                        if not is_connected:
                            # Обнаружено отключение - увеличиваем счетчик подтверждений
                            if account_key not in disconnect_confirmations:
                                disconnect_confirmations[account_key] = {'count': 0, 'reason': None}
                            
                            disconnect_confirmations[account_key]['count'] += 1
                            # Сохраняем причину отключения (берем последнюю)
                            if disconnect_reason:
                                disconnect_confirmations[account_key]['reason'] = disconnect_reason
                            
                            # Проверяем, требуется ли немедленный перезапуск (после пробуждения окна)
                            reason = disconnect_confirmations[account_key]['reason'] or "Причина не указана"
                            requires_restart = "ТРЕБУЕТСЯ ПЕРЕЗАПУСК" in reason.upper()
                            
                            # Если требуется немедленный перезапуск (после пробуждения) - перезапускаем сразу
                            # Иначе требуем минимум 2 проверки подряд (20 секунд) для подтверждения отключения
                            if requires_restart or disconnect_confirmations[account_key]['count'] >= 2:
                                if requires_restart:
                                    logging.warning(f"[Мониторинг] ⚠ НЕМЕДЛЕННЫЙ ПЕРЕЗАПУСК ТРЕБУЕТСЯ: {nickname} ({sandbox})")
                                else:
                                    logging.warning(f"[Мониторинг] ⚠ ОТКЛЮЧЕНИЕ ПОДТВЕРЖДЕНО ({disconnect_confirmations[account_key]['count']} проверок): {nickname} ({sandbox})")
                                logging.warning(f"[Мониторинг] 📋 ПРИЧИНА ОТКЛЮЧЕНИЯ: {reason}")
                                logging.info(f"[Мониторинг] Перезапуск аккаунта {nickname}...")
                                
                                restart_success = self.restart_account(account)
                                
                                if restart_success:
                                    logging.info(f"[Мониторинг] ✓ Аккаунт {nickname} успешно перезапущен")
                                    # Сбрасываем счетчик после успешного перезапуска
                                    disconnect_confirmations[account_key] = {'count': 0, 'reason': None}
                                    # Даем время на запуск перед следующей проверкой
                                    time.sleep(30)
                                else:
                                    logging.error(f"[Мониторинг] ✗ Не удалось перезапустить аккаунт {nickname}, повторим попытку позже")
                                    time.sleep(10)
                            else:
                                # Еще недостаточно подтверждений - ждем еще проверку
                                logging.debug(f"[Мониторинг] Отключение обнаружено для {nickname}, но ждем подтверждения ({disconnect_confirmations[account_key]['count']}/2). Причина: {reason}")
                        else:
                            # Подключен - сбрасываем счетчик отключений
                            if account_key in disconnect_confirmations:
                                if disconnect_confirmations[account_key]['count'] > 0:
                                    logging.debug(f"[Мониторинг] ✓ {nickname} подключен (счетчик отключений сброшен с {disconnect_confirmations[account_key]['count']})")
                                disconnect_confirmations[account_key] = {'count': 0, 'reason': None}
                            
                            # Логируем каждые 2 минуты
                            if check_counter % 12 == 0:
                                logging.debug(f"[Мониторинг] ✓ {nickname} подключен")
                    
                    except Exception as e:
                        logging.error(f"[Мониторинг] Ошибка проверки аккаунта {nickname}: {e}")
                        time.sleep(5)
                
                # Небольшая пауза между циклами проверки всех аккаунтов
                time.sleep(2)
                
            except KeyboardInterrupt:
                logging.info("[Мониторинг] Остановка мониторинга по запросу пользователя")
                break
            except Exception as e:
                logging.error(f"[Мониторинг] Ошибка в цикле мониторинга: {e}")
                time.sleep(10)
    
    def run(self, start_index: int = 0, end_index: Optional[int] = None):
        """
        Запуск автоматизации для всех аккаунтов и мониторинг отключений
        
        Args:
            start_index: Индекс начального аккаунта
            end_index: Индекс конечного аккаунта (None = все)
        """
        logging.info("="*60)
        logging.info("ЗАПУСК АВТОМАТИЗАЦИИ С МОНИТОРИНГОМ ОТКЛЮЧЕНИЙ")
        logging.info("="*60)
        logging.info("")
        
        # Запускаем аккаунты и получаем список успешно запущенных
        launched_accounts = self.run_all_accounts(start_index, end_index)
        
        if not launched_accounts:
            logging.warning("⚠ Не запущено ни одного аккаунта, мониторинг не будет работать")
            return
        
        # Запускаем мониторинг только для успешно запущенных аккаунтов
        import threading
        monitor_thread = threading.Thread(
            target=self.monitor_disconnects, 
            args=(launched_accounts,), 
            daemon=True
        )
        monitor_thread.start()
        logging.info(f"✓ Мониторинг отключений запущен для {len(launched_accounts)} аккаунтов")
        
        try:
            while True:
                time.sleep(60)
        except KeyboardInterrupt:
            logging.info("")
            logging.info("="*60)
            logging.info("ОСТАНОВКА ПОЛЬЗОВАТЕЛЕМ (Ctrl+C)")
            logging.info("="*60)


if __name__ == "__main__":
    # Вопрос о включении автоматического движения
    print("="*60)
    print("АВТОМАТИЧЕСКОЕ ДВИЖЕНИЕ")
    print("="*60)
    print("Автоматическое движение будет периодически зажимать W или S")
    print("на 15-30 секунд с интервалом 2-7 минут для каждого окна.")
    print("")
    
    enable_movement = False
    while True:
        try:
            user_input = input("Активировать автоматическое движение? (y/n): ").strip().lower()
            if user_input in ['y', 'yes', 'да', 'д']:
                enable_movement = True
                print("✓ Автоматическое движение активировано")
                break
            elif user_input in ['n', 'no', 'нет', 'н']:
                enable_movement = False
                print("✓ Автоматическое движение отключено")
                break
            else:
                print("✗ Ошибка: Введите 'y' или 'n'")
        except KeyboardInterrupt:
            print("\n\nОстановка пользователем")
            exit(0)
    
    print("")
    
    # Создаем экземпляр с настройкой движения
    automation = RadmirAutomation(enable_auto_movement=enable_movement)
    
    # Выбор количества аккаунтов для запуска
    accounts = automation.config["accounts"]
    total_accounts = len(accounts)
    
    print("="*60)
    print("ВЫБОР КОЛИЧЕСТВА АККАУНТОВ ДЛЯ ЗАПУСКА")
    print("="*60)
    print(f"Всего аккаунтов в конфигурации: {total_accounts}")
    print("")
    print("Доступные аккаунты:")
    for i, account in enumerate(accounts, 1):
        print(f"  {i}. {account['nickname']} ({account['sandbox']}) - {account['server']}")
    print("")
    
    while True:
        try:
            user_input = input(f"Введите количество аккаунтов для запуска (1-{total_accounts}) или 'all' для всех: ").strip().lower()
            
            if user_input == 'all' or user_input == '':
                start_index = 0
                end_index = None
                print(f"✓ Запуск всех {total_accounts} аккаунтов")
                break
            else:
                count = int(user_input)
                if 1 <= count <= total_accounts:
                    start_index = 0
                    end_index = count
                    print(f"✓ Запуск {count} аккаунтов (с 1-го по {count}-й)")
                    break
                else:
                    print(f"✗ Ошибка: Введите число от 1 до {total_accounts}")
        except ValueError:
            print("✗ Ошибка: Введите число или 'all'")
        except KeyboardInterrupt:
            print("\n\nОстановка пользователем")
            exit(0)
    
    print("")
    automation.run(start_index=start_index, end_index=end_index)

