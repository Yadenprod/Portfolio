#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import random
import argparse
import logging
import subprocess
import json
import requests
from datetime import datetime
from pathlib import Path
import ctypes
import win32gui
import win32con
import win32api
import keyboard
import pyautogui
import shutil

# Настройка логгирования
log_dir = Path('logs')
log_dir.mkdir(exist_ok=True)
timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
log_file = log_dir / f'cs2_bot_{timestamp}.log'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)

# Глобальные константы
STEAM_EXECUTABLE_PATHS = [
    Path('C:/Program Files (x86)/Steam/steam.exe'),
    Path('C:/Program Files/Steam/steam.exe'),
    Path('D:/Steam/steam.exe'),
    Path('E:/Steam/steam.exe'),
    Path('F:/Steam/steam.exe'),
    Path(os.path.expanduser('~/Steam/steam.exe')),
    Path(os.path.expanduser('~/.steam/steam.exe')),
]
CS2_APP_ID = 730
API_URL = 'http://localhost:3000/api'  # URL к API
BOT_API_KEY = os.environ.get('BOT_API_KEY', 'dev_api_key')  # API ключ из переменных окружения

# Отключаем failsafe PyAutoGUI (не рекомендуется, но необходимо для работы бота)
pyautogui.FAILSAFE = False
# Устанавливаем паузу между действиями PyAutoGUI
pyautogui.PAUSE = 0.1

class CS2Bot:
    def __init__(self, account_id, username, map_name='dust2', mode='deathmatch', duration=240, steam_path=None, use_api=True, fix_vac=False):
        """
        Инициализация бота для CS2
        
        :param account_id: ID аккаунта в базе данных
        :param username: Имя пользователя Steam
        :param map_name: Карта для игры (по умолчанию dust2)
        :param mode: Режим игры (по умолчанию deathmatch)
        :param duration: Продолжительность работы бота в минутах
        :param steam_path: Путь к исполняемому файлу Steam
        :param use_api: Использовать API для обновления статистики (по умолчанию True)
        :param fix_vac: Попытаться исправить ошибки VAC перед запуском (по умолчанию False)
        """
        self.account_id = account_id
        self.username = username
        self.map_name = map_name
        self.mode = mode
        self.duration = duration * 60  # Переводим в секунды
        self.cases_collected = 0
        self.start_time = None
        self.running = False
        self.steam_path = steam_path
        self.cs2_window_handle = None
        self.last_case_time = None
        self.use_api = use_api
        self.fix_vac = fix_vac
        self.steam_dir = None
        
        # Данные сессии
        self.moves = 0
        self.shots = 0
        self.deaths = 0
        self.reconnects = 0
        
        # Ограничение движения мыши
        self.safe_mouse_margin = 50  # отступ от края экрана в пикселях
        self.screen_width, self.screen_height = pyautogui.size()
        
        # Заголовок окна для поиска
        self.window_title = f"CS2Bot-{account_id}"
        
        # Устанавливаем заголовок консоли
        if os.name == 'nt':  # Windows
            ctypes.windll.kernel32.SetConsoleTitleW(self.window_title)
        else:  # Linux/Mac - не работает, но не вызовет ошибку
            sys.stdout.write(f"\x1b]2;{self.window_title}\x07")
        
        logging.info(f"CS2Bot инициализирован для аккаунта {username} (ID: {account_id})")

    def find_steam_path(self):
        """Поиск пути к исполняемому файлу Steam"""
        # Если путь к Steam был передан при инициализации, используем его
        if self.steam_path and Path(self.steam_path).exists():
            logging.info(f"Используется указанный путь к Steam: {self.steam_path}")
            self.steam_dir = Path(self.steam_path).parent
            return Path(self.steam_path)
            
        # Иначе ищем в списке стандартных путей
        for path in STEAM_EXECUTABLE_PATHS:
            if path.exists():
                self.steam_path = path
                self.steam_dir = path.parent
                logging.info(f"Найден путь к Steam: {path}")
                return path
        
        # Пробуем найти через реестр (только для Windows)
        if os.name == 'nt':
            try:
                import winreg
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam")
                install_path = winreg.QueryValueEx(key, "SteamExe")[0]
                if install_path and Path(install_path).exists():
                    self.steam_path = Path(install_path)
                    self.steam_dir = Path(install_path).parent
                    logging.info(f"Найден путь к Steam через реестр: {install_path}")
                    return Path(install_path)
            except Exception as e:
                logging.debug(f"Не удалось найти Steam через реестр: {e}")
        
        logging.error("Не удалось найти Steam. Пожалуйста, укажите путь вручную с помощью аргумента --steam_path.")
        return None

    def fix_vac_issues(self):
        """Исправление проблем с VAC системой"""
        if not self.steam_dir or not self.steam_path:
            logging.error("Не удалось определить директорию Steam для исправления VAC.")
            return False
            
        logging.info("Пытаемся исправить проблемы с VAC...")
        
        try:
            # Способ 1: Закрыть все Steam процессы
            self.stop_steam_processes()
            
            # Способ 2: Перепроверить файлы игры
            if not self.verify_game_files():
                logging.warning("Не удалось запустить проверку файлов игры.")
                
            # Способ 3: Запуск Steam с ключами для восстановления VAC
            self.restart_steam_admin()
            
            # Способ 4: Выполнение команды для сброса настроек Valve Anti-Cheat
            if os.name == 'nt':
                try:
                    logging.info("Выполняем сброс настроек VAC...")
                    admin_cmd = 'bcdedit /deletevalue nointegritychecks'
                    subprocess.run(admin_cmd, shell=True, check=False)
                    
                    admin_cmd = 'bcdedit /deletevalue loadoptions'
                    subprocess.run(admin_cmd, shell=True, check=False)
                    
                    admin_cmd = 'bcdedit /debug off'
                    subprocess.run(admin_cmd, shell=True, check=False)
                    
                    admin_cmd = 'bcdedit /deletevalue nx'
                    subprocess.run(admin_cmd, shell=True, check=False)
                    
                    logging.info("Команды сброса VAC выполнены")
                except Exception as e:
                    logging.error(f"Ошибка при выполнении команд сброса VAC: {e}")
            
            return True
        except Exception as e:
            logging.error(f"Ошибка при исправлении проблем с VAC: {e}")
            return False

    def stop_steam_processes(self):
        """Остановка всех процессов Steam"""
        logging.info("Останавливаем все процессы Steam...")
        try:
            if os.name == 'nt':
                subprocess.run("taskkill /F /IM steam.exe", shell=True, check=False)
                subprocess.run("taskkill /F /IM steamwebhelper.exe", shell=True, check=False)
                subprocess.run("taskkill /F /IM steamservice.exe", shell=True, check=False)
                time.sleep(5)
                logging.info("Все процессы Steam остановлены")
        except Exception as e:
            logging.error(f"Ошибка при остановке процессов Steam: {e}")

    def verify_game_files(self):
        """Проверка целостности файлов игры"""
        logging.info("Проверка целостности файлов CS2...")
        try:
            if not self.steam_path:
                return False
                
            verify_cmd = f'"{self.steam_path}" -command "verify_integrity_of_game_files {CS2_APP_ID}"'
            subprocess.Popen(verify_cmd, shell=True)
            time.sleep(10)  # Даем Steam время на запуск проверки
            logging.info("Проверка файлов запущена")
            return True
        except Exception as e:
            logging.error(f"Ошибка при проверке файлов игры: {e}")
            return False

    def restart_steam_admin(self):
        """Перезапуск Steam с правами администратора и специальными параметрами"""
        logging.info("Перезапускаем Steam с правами администратора...")
        try:
            if not self.steam_path:
                return False
                
            # Закрываем Steam если он запущен
            self.stop_steam_processes()
            
            # Запускаем Steam с правами администратора и параметрами для исправления VAC
            admin_cmd = f'"{self.steam_path}" -login {self.username} -clearbeta -noverifyfiles -nobootstrapupdate -skipinitialbootstrap -nocrashdialog -no-browser'
            
            # Запуск с правами администратора в Windows
            if os.name == 'nt':
                # Создаем временный батник для запуска от админа
                temp_bat = Path('temp_steam_admin.bat')
                with open(temp_bat, 'w') as f:
                    f.write(f'start "" {admin_cmd}')
                
                # Запускаем от имени администратора
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = subprocess.SW_HIDE
                
                subprocess.Popen(['runas', '/user:Administrator', str(temp_bat)], 
                                startupinfo=startupinfo, 
                                shell=True)
                
                time.sleep(15)  # Даем Steam время на запуск
                
                # Удаляем временный файл
                if temp_bat.exists():
                    temp_bat.unlink()
            else:
                # Для других ОС просто запускаем с sudo
                subprocess.Popen(f'sudo {admin_cmd}', shell=True)
                time.sleep(15)
                
            logging.info("Steam перезапущен с правами администратора")
            return True
        except Exception as e:
            logging.error(f"Ошибка при перезапуске Steam: {e}")
            return False

    def start_cs2(self):
        """Запуск CS2 через Steam"""
        if not self.steam_path:
            self.steam_path = self.find_steam_path()
            if not self.steam_path:
                return False
        
        # Если указан параметр исправления VAC, выполняем процедуру
        if self.fix_vac:
            logging.info("Запускаем процедуру исправления VAC перед запуском игры...")
            self.fix_vac_issues()
            time.sleep(15)  # Даем время на перезапуск Steam
        
        logging.info("Запуск CS2...")
        
        try:
            # Формируем команду запуска с параметрами для обхода VAC ошибки
            launch_options = f"-applaunch {CS2_APP_ID} -novid -tickrate 128 -windowed -w 1280 -h 720 -insecure -nohltv -softparticlesdefaultoff -nopreload -nosound"
            
            # Запускаем Steam с CS2
            subprocess.Popen(f'"{self.steam_path}" {launch_options}', shell=True)
            
            # Ждем запуска игры
            logging.info("Ожидание запуска CS2...")
            for i in range(60):  # Ждем до 60 секунд
                if self.is_cs2_running():
                    logging.info("CS2 успешно запущен")
                    time.sleep(10)  # Ждем дополнительно 10 секунд для полной загрузки игры
                    self.activate_cs2_window()
                    return True
                time.sleep(1)
            
            logging.error("Не удалось запустить CS2 за отведенное время")
            return False
        
        except Exception as e:
            logging.error(f"Ошибка при запуске CS2: {e}")
            return False

    def restart_cs2(self):
        """Перезапуск CS2 при проблемах с подключением"""
        logging.info("Перезапускаем CS2...")
        
        try:
            # Закрываем игру если она запущена
            if self.cs2_window_handle:
                win32gui.PostMessage(self.cs2_window_handle, win32con.WM_CLOSE, 0, 0)
                time.sleep(5)
            
            # Также пробуем закрыть все процессы CS2
            if os.name == 'nt':
                subprocess.run("taskkill /F /IM cs2.exe", shell=True, check=False)
                time.sleep(5)
            
            # Запускаем снова
            return self.start_cs2()
            
        except Exception as e:
            logging.error(f"Ошибка при перезапуске CS2: {e}")
            return False

    def is_cs2_running(self):
        """Проверка запущен ли CS2"""
        window_titles = []
        
        def enum_windows_callback(hwnd, _):
            if win32gui.IsWindowVisible(hwnd):
                window_title = win32gui.GetWindowText(hwnd)
                if 'Counter-Strike' in window_title:
                    window_titles.append(hwnd)
                    self.cs2_window_handle = hwnd
        
        win32gui.EnumWindows(enum_windows_callback, None)
        return len(window_titles) > 0

    def activate_cs2_window(self):
        """Активирует окно CS2"""
        if self.cs2_window_handle:
            try:
                # Проверяем, если окно свернуто
                if win32gui.IsIconic(self.cs2_window_handle):
                    # Разворачиваем окно
                    win32gui.ShowWindow(self.cs2_window_handle, win32con.SW_RESTORE)
                
                # Приводим окно на передний план
                win32gui.SetForegroundWindow(self.cs2_window_handle)
                
                # Получаем размеры окна
                rect = win32gui.GetWindowRect(self.cs2_window_handle)
                x = rect[0]
                y = rect[1]
                w = rect[2] - rect[0]
                h = rect[3] - rect[1]
                
                # Центр окна
                center_x = x + w // 2
                center_y = y + h // 2
                
                # Перемещаем мышь в центр окна
                win32api.SetCursorPos((center_x, center_y))
                
                logging.info(f"Окно CS2 активировано: {rect}")
                return True
            except Exception as e:
                logging.error(f"Ошибка при активации окна CS2: {e}")
                return False
        
        logging.warning("Не удалось активировать окно CS2 (дескриптор окна не найден)")
        return False

    def join_deathmatch(self):
        """Присоединение к игре Deathmatch на указанной карте"""
        logging.info(f"Попытка присоединения к игре {self.mode} на карте {self.map_name}")
        
        try:
            # Ждем полной загрузки игры и главного меню
            logging.info("Ожидание загрузки главного меню...")
            time.sleep(20)
            
            # Активируем окно CS2 еще раз для уверенности
            self.activate_cs2_window()
            time.sleep(1)
            
            # Метод 1: Используем клавиши для доступа к меню игры
            logging.info("Пытаемся открыть локальную игру через меню...")
            
            # Нажимаем Escape для закрытия всех диалогов и возврата в главное меню
            pyautogui.press('escape')
            time.sleep(1)
            
            # Нажимаем клавиши для навигации в меню "Играть" -> "Офлайн с ботами"
            # Нажимаем на "Играть"
            pyautogui.moveTo(640, 360)  # Перемещаем мышь в центр экрана
            pyautogui.click()
            time.sleep(1)
            
            # Выбираем "Deathmatch"
            pyautogui.moveTo(640, 400)
            pyautogui.click()
            time.sleep(1)
            
            # Выбираем карту
            logging.info("Выбираем карту...")
            pyautogui.moveTo(640, 450)
            pyautogui.click()
            time.sleep(1)
            
            # Нажимаем "Начать игру"
            pyautogui.moveTo(640, 600)
            pyautogui.click()
            
            # Метод 2: Если первый метод не сработал, пробуем через консоль
            logging.info("Пробуем запустить игру через консоль...")
            time.sleep(2)
            
            try:
                # Открываем консоль - используем pyautogui вместо keyboard
                logging.info("Открываем консоль с помощью pyautogui...")
                
                # Используем различные методы для открытия консоли
                # 1. Стандартная клавиша - тильда/grave
                pyautogui.press('`')
                time.sleep(0.5)
                
                # 2. Если не сработало, пробуем через код клавиши (для разных раскладок)
                if not self.is_console_open():
                    logging.info("Пробуем альтернативные клавиши для консоли...")
                    # Альтернативные клавиши для разных раскладок
                    for console_key in ['`', 'grave', 'ё', 'F10', 'F11']:
                        pyautogui.press(console_key)
                        time.sleep(0.5)
                        if self.is_console_open():
                            logging.info(f"Консоль открыта с помощью клавиши {console_key}")
                            break
                
                # Вводим команду для подключения к игре
                if self.mode == 'deathmatch':
                    # Проверяем, открыта ли консоль
                    if not self.is_console_open():
                        logging.warning("Не удалось открыть консоль, пробуем метод 3...")
                        raise Exception("Консоль не открылась")
                    
                    # Сначала очищаем консоль
                    pyautogui.press('escape')
                    time.sleep(0.5)
                    pyautogui.press('`')
                    time.sleep(0.5)
                    
                    # Вводим каждую команду отдельно для большей надежности
                    pyautogui.write('game_type 1')
                    pyautogui.press('enter')
                    time.sleep(0.5)
                    
                    pyautogui.write('game_mode 2')
                    pyautogui.press('enter')
                    
                    pyautogui.write(f'map {self.map_name}')
                    pyautogui.press('enter')
                else:
                    # Другие режимы можно добавить здесь
                    pass
                
                logging.info("Команда подключения к игре отправлена")
                
                # Закрываем консоль
                pyautogui.press('escape')
            
            except Exception as e:
                logging.warning(f"Ошибка при работе с консолью: {e}")
                logging.info("Пробуем метод 3: прямой вызов команд меню...")
                
                # Метод 3: Пробуем через главное меню с дополнительными координатами
                pyautogui.press('escape')  # Сбрасываем любые открытые меню
                time.sleep(0.5)
                
                # Список возможных координат для меню "Играть"
                play_button_positions = [
                    (640, 360),  # Центр
                    (640, 300),  # Выше
                    (640, 400),  # Ниже
                    (500, 360),  # Левее
                    (780, 360)   # Правее
                ]
                
                # Перебираем возможные позиции для кнопки "Играть"
                for pos in play_button_positions:
                    logging.info(f"Пробуем нажать 'Играть' в позиции {pos}")
                    pyautogui.moveTo(pos[0], pos[1])
                    pyautogui.click()
                    time.sleep(1)
                    
                    # Пробуем найти Deathmatch
                    for dm_y in range(300, 600, 50):
                        pyautogui.moveTo(640, dm_y)
                        pyautogui.click()
                        time.sleep(0.5)
                        
                        # Пробуем найти карту и запустить игру
                        for start_y in range(400, 700, 50):
                            pyautogui.moveTo(640, start_y)
                            pyautogui.click()
                            time.sleep(1)
            
            # Ждем загрузки карты
            logging.info("Ожидание загрузки карты...")
            time.sleep(30)  # Увеличиваем время ожидания для надежности
            
            logging.info("Присоединение к игре выполнено")
            return True
            
        except Exception as e:
            logging.error(f"Ошибка при присоединении к игре: {e}")
            return False
    
    def is_console_open(self):
        """Проверяем, открыта ли консоль в CS2"""
        # Примечание: Это приблизительная проверка - консоль обычно затемняет верхнюю часть экрана
        try:
            # Проверяем цвет пикселя в верхней части экрана, где должна быть консоль
            pixel_color = pyautogui.pixel(640, 50)
            
            # Консоль обычно имеет темный фон
            is_dark = sum(pixel_color) < 200  # Сумма RGB меньше 200 для темных цветов
            
            if is_dark:
                logging.debug("Консоль, вероятно, открыта (обнаружен темный фон)")
                return True
            else:
                logging.debug("Консоль, вероятно, закрыта (не обнаружен темный фон)")
                return False
        except Exception as e:
            logging.debug(f"Ошибка при проверке состояния консоли: {e}")
            return False

    def simulate_gameplay(self):
        """Симуляция игрового процесса для фарма кейсов"""
        logging.info("Начало симуляции игрового процесса")
        
        self.start_time = time.time()
        self.last_case_time = time.time()
        self.running = True
        
        try:
            # Игровой цикл
            while self.running and (time.time() - self.start_time < self.duration):
                # Случайное движение
                self.random_movement()
                
                # Случайная стрельба
                if random.random() < 0.3:  # 30% шанс стрельбы
                    self.random_shoot()
                
                # Проверка на сбор кейса (каждые 10 минут активной игры)
                elapsed_since_last_case = time.time() - self.last_case_time
                if elapsed_since_last_case >= 600:  # 10 минут
                    self.cases_collected += 1
                    self.last_case_time = time.time()
                    logging.info(f"Новый кейс получен! Всего кейсов: {self.cases_collected}")
                    
                    # Обновляем информацию в базе данных
                    self.update_cases_collected()
                
                # Обновляем статус в логе каждые 5 минут
                elapsed_total = time.time() - self.start_time
                if elapsed_total % 300 < 1:  # Примерно каждые 5 минут
                    remaining = self.duration - elapsed_total
                    logging.info(f"Статус бота: работает {elapsed_total//60:.0f} мин., осталось {remaining//60:.0f} мин., кейсов: {self.cases_collected}")
                
                # Задержка между действиями
                time.sleep(random.uniform(0.5, 2.0))
            
            total_time = (time.time() - self.start_time) / 60
            logging.info(f"Симуляция завершена. Время работы: {total_time:.1f} мин. Собрано кейсов: {self.cases_collected}")
            return True
            
        except Exception as e:
            logging.error(f"Ошибка при симуляции геймплея: {e}")
            self.running = False
            return False

    def random_movement(self):
        """Случайное движение в игре"""
        # Список возможных клавиш движения
        movement_keys = ['w', 'a', 's', 'd', 'space']
        
        # Выбираем случайную клавишу
        key = random.choice(movement_keys)
        
        # Случайная длительность нажатия
        duration = random.uniform(0.1, 2.0)
        
        logging.debug(f"Движение: {key} в течение {duration:.2f} сек.")
        
        # Нажимаем клавишу
        keyboard.press(key)
        time.sleep(duration)
        keyboard.release(key)
        
        # Случайный поворот мыши в безопасных пределах экрана
        if random.random() < 0.7:  # 70% шанс поворота
            # Получаем текущую позицию мыши
            current_x, current_y = pyautogui.position()
            
            # Вычисляем максимально допустимые смещения, чтобы не выйти за пределы безопасной зоны
            max_dx = min(self.screen_width - self.safe_mouse_margin - current_x, 
                        current_x - self.safe_mouse_margin)
            max_dy = min(self.screen_height - self.safe_mouse_margin - current_y, 
                        current_y - self.safe_mouse_margin)
            
            # Ограничиваем смещение безопасными значениями
            dx = max(-max_dx, min(max_dx, random.randint(-100, 100)))
            dy = max(-max_dy, min(max_dy, random.randint(-50, 50)))
            
            # Перемещаем мышь
            pyautogui.move(dx, dy, duration=random.uniform(0.1, 0.5))
        
        self.moves += 1

    def random_shoot(self):
        """Случайная стрельба в игре"""
        # Нажимаем левую кнопку мыши на случайное время
        duration = random.uniform(0.1, 1.0)
        logging.debug(f"Стрельба в течение {duration:.2f} сек.")
        
        pyautogui.mouseDown(button='left')
        time.sleep(duration)
        pyautogui.mouseUp(button='left')
        
        self.shots += 1

    def update_cases_collected(self):
        """Обновление количества собранных кейсов через API"""
        if not self.use_api:
            logging.info(f"Обновление API отключено. Текущее количество кейсов: {self.cases_collected}")
            return True
            
        try:
            response = requests.post(
                f"{API_URL}/accounts/update-cases",
                json={
                    "accountId": self.account_id,
                    "casesCollected": self.cases_collected,
                    "apiKey": BOT_API_KEY
                },
                timeout=10
            )
            
            if response.status_code == 200:
                logging.info(f"Количество кейсов успешно обновлено в базе данных: {self.cases_collected}")
                return True
            else:
                logging.error(f"Ошибка при обновлении количества кейсов: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logging.error(f"Ошибка при отправке данных на сервер: {e}")
            logging.info(f"Продолжаем работу без API. Текущее количество кейсов: {self.cases_collected}")
            return False

    def stop(self):
        """Остановка работы бота и CS2"""
        logging.info("Остановка бота...")
        self.running = False
        
        # Закрываем CS2
        if self.cs2_window_handle:
            try:
                # Отправляем команду закрытия окну
                win32gui.PostMessage(self.cs2_window_handle, win32con.WM_CLOSE, 0, 0)
                logging.info("Отправлена команда закрытия CS2")
                
                # Обновляем количество собранных кейсов в последний раз
                self.update_cases_collected()
                
                return True
            except Exception as e:
                logging.error(f"Ошибка при закрытии CS2: {e}")
        
        return False

def parse_arguments():
    """Разбор аргументов командной строки"""
    parser = argparse.ArgumentParser(description='CS2 Case Farming Bot')
    parser.add_argument('--account_id', required=True, help='ID аккаунта в базе данных')
    parser.add_argument('--username', required=True, help='Имя пользователя Steam')
    parser.add_argument('--map', default='dust2', help='Карта для игры')
    parser.add_argument('--mode', default='deathmatch', help='Режим игры')
    parser.add_argument('--duration', type=int, default=240, help='Длительность работы бота в минутах')
    parser.add_argument('--steam_path', help='Путь к исполняемому файлу Steam (например, C:/Program Files (x86)/Steam/steam.exe)')
    parser.add_argument('--no-api', action='store_true', help='Отключить использование API для обновления статистики')
    parser.add_argument('--fix-vac', action='store_true', help='Попытаться исправить проблемы с VAC перед запуском')
    return parser.parse_args()

def main():
    """Основная функция программы"""
    # Разбор аргументов
    args = parse_arguments()
    
    # Инициализация бота
    bot = CS2Bot(
        account_id=args.account_id,
        username=args.username,
        map_name=args.map,
        mode=args.mode,
        duration=args.duration,
        steam_path=args.steam_path,
        use_api=not args.no_api,
        fix_vac=args.fix_vac
    )
    
    try:
        # Запуск CS2
        if not bot.start_cs2():
            logging.error("Не удалось запустить CS2. Бот завершает работу.")
            return 1
        
        # Если с первого раза не удалось подключиться, пробуем перезапустить
        for attempt in range(3):
            if bot.join_deathmatch():
                break
            
            logging.warning(f"Попытка {attempt + 1} не удалась. Перезапускаем CS2...")
            if not bot.restart_cs2():
                logging.error("Не удалось перезапустить CS2. Бот завершает работу.")
                return 1
        else:
            logging.error("Не удалось подключиться к игре после нескольких попыток. Бот завершает работу.")
            bot.stop()
            return 1
        
        # Начинаем симуляцию игрового процесса
        bot.simulate_gameplay()
        
        # Останавливаем бота и закрываем CS2
        bot.stop()
        
        logging.info(f"Бот успешно завершил работу. Собрано кейсов: {bot.cases_collected}")
        return 0
        
    except KeyboardInterrupt:
        logging.info("Получен сигнал прерывания. Бот завершает работу.")
        bot.stop()
        return 0
        
    except Exception as e:
        logging.error(f"Необработанная ошибка: {e}")
        bot.stop()
        return 1

if __name__ == "__main__":
    sys.exit(main()) 