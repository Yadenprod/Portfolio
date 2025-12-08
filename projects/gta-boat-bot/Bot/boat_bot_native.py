"""
Бот для автоматического плавания на лодке в GTA SAMP
Использует нативные API через MoonLoader вместо компьютерного зрения

Требования:
- MoonLoader скрипт (boat_bot_ml.lua) должен быть загружен в игру
- SAMPFUNCS должен быть установлен
"""

import time
import math
import logging
import os
from typing import Optional, Dict
from pathlib import Path

# Импорт системы подсчета чекпоинтов
try:
    from boat_bot_modules import CheckpointCounter
    CHECKPOINT_COUNTER_AVAILABLE = True
except ImportError:
    CHECKPOINT_COUNTER_AVAILABLE = False

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class GameDataReader:
    """Читает данные из игры через файл (от MoonLoader скрипта)"""
    
    def __init__(self, data_file="bot_shared_data.txt"):
        self.data_file = data_file
        self.last_data = None
        self.game_directory = self._find_game_directory()
    
    def _find_game_directory(self) -> Optional[Path]:
        """Пытается найти директорию игры"""
        # Стандартные пути (включая путь пользователя)
        possible_paths = [
            Path("C:/Program Files (x86)/Radic/RADMIR LAUNCHER/resources/projects/crmp"),
            Path("C:/Program Files (x86)/Rockstar Games/GTA San Andreas"),
            Path("C:/Games/GTA San Andreas"),
            Path("D:/Games/GTA San Andreas"),
            Path(os.getcwd()),  # Текущая директория
        ]
        
        for path in possible_paths:
            if path.exists():
                # Проверяем наличие moonloader или gta_sa.exe
                if (path / "moonloader").exists() or (path / "gta_sa.exe").exists():
                    logger.info(f"Найдена директория игры: {path}")
                    return path
        
        logger.warning("Директория игры не найдена, используем текущую директорию")
        return Path(os.getcwd())  # По умолчанию текущая директория
    
    def read_game_data(self) -> Optional[Dict]:
        """Читает данные из файла, созданного MoonLoader скриптом"""
        try:
            # Пробуем несколько путей (включая путь пользователя)
            possible_files = [
                Path(self.data_file),  # Текущая директория
                self.game_directory / self.data_file,  # Директория игры
                Path("C:/Program Files (x86)/Radic/RADMIR LAUNCHER/resources/projects/crmp") / self.data_file,  # Путь пользователя
                Path(os.getcwd()) / self.data_file,  # Текущая рабочая директория
            ]
            
            data_file_path = None
            for path in possible_files:
                if path.exists():
                    data_file_path = path
                    if not hasattr(self, '_last_found_path') or self._last_found_path != str(path):
                        logger.debug(f"Файл данных найден: {path}")
                        self._last_found_path = str(path)
                    break
            
            if not data_file_path or not data_file_path.exists():
                # Выводим отладочную информацию только периодически
                if not hasattr(self, '_last_debug_time') or time.time() - self._last_debug_time > 5:
                    logger.debug(f"Файл данных не найден. Искали в:")
                    for path in possible_files:
                        logger.debug(f"  - {path} (существует: {path.exists()})")
                    self._last_debug_time = time.time()
                return None
            
            with open(data_file_path, 'r') as f:
                line = f.read().strip()
                if not line:
                    return None
                
                parts = line.split(',')
                if len(parts) < 12:
                    return None
                
                try:
                    data = {
                        'player_x': float(parts[0]),
                        'player_y': float(parts[1]),
                        'player_z': float(parts[2]),
                        'player_angle': float(parts[3]),
                        'checkpoint_x': float(parts[4]),
                        'checkpoint_y': float(parts[5]),
                        'checkpoint_z': float(parts[6]),
                        'checkpoint_type': int(parts[7]),
                        'checkpoint_id': int(parts[8]),
                        'checkpoint_distance': float(parts[9]),
                        'bot_enabled': int(parts[10]) == 1,
                        'bot_command': int(parts[11])
                    }
                    self.last_data = data
                    return data
                except (ValueError, IndexError) as e:
                    logger.error(f"Ошибка парсинга данных: {e}, строка: {line}")
                    return None
        except Exception as e:
            logger.error(f"Ошибка чтения данных игры: {e}")
            return None


class ControlSender:
    """Отправляет команды управления в игру"""
    
    def __init__(self, command_file="bot_commands.txt"):
        self.command_file = command_file
        self.current_command = 0
        self.game_directory = self._find_game_directory()
    
    def _find_game_directory(self) -> Optional[Path]:
        """Пытается найти директорию игры"""
        possible_paths = [
            Path("C:/Program Files (x86)/Radic/RADMIR LAUNCHER/resources/projects/crmp"),
            Path("C:/Program Files (x86)/Rockstar Games/GTA San Andreas"),
            Path("C:/Games/GTA San Andreas"),
            Path("D:/Games/GTA San Andreas"),
            Path(os.getcwd()),
        ]
        
        for path in possible_paths:
            if path.exists():
                if (path / "moonloader").exists() or (path / "gta_sa.exe").exists():
                    return path
        
        return Path(os.getcwd())
    
    def send_command(self, enabled: bool, command: int):
        """
        Отправляет команду в игру через файл
        command: 0 = нет команды, 1 = вперед (W), 2 = влево (A), 3 = вправо (D)
        """
        try:
            # Пробуем несколько путей (включая путь пользователя)
            possible_files = [
                Path(self.command_file),  # Текущая директория
                self.game_directory / self.command_file,  # Директория игры
                Path("C:/Program Files (x86)/Radic/RADMIR LAUNCHER/resources/projects/crmp") / self.command_file,  # Путь пользователя
                Path(os.getcwd()) / self.command_file,  # Текущая рабочая директория
            ]
            
            # Пробуем создать файл в первом доступном месте
            command_file_path = None
            for path in possible_files:
                try:
                    # Пробуем создать файл для проверки доступа
                    path.parent.mkdir(parents=True, exist_ok=True)
                    command_file_path = path
                    break
                except:
                    continue
            
            # Если не удалось найти доступное место, используем текущую директорию
            if not command_file_path:
                command_file_path = Path(os.getcwd()) / self.command_file
            
            with open(command_file_path, 'w') as f:
                f.write(f"{1 if enabled else 0},{command}\n")
            self.current_command = command
        except Exception as e:
            logger.error(f"Ошибка отправки команды: {e}")
    
    def stop(self):
        """Останавливает бота"""
        self.send_command(False, 0)


class NavigationEngine:
    """Вычисляет направление к цели и управляет движением"""
    
    # Маппинг типов чекпоинтов
    CHECKPOINT_TYPE_MAP = {
        0: None,
        1: 'red',
        2: 'yellow',
        3: 'pink',
        4: 'green',
        5: 'white',
        6: 'orange',
        7: 'purple'
    }
    
    def __init__(self):
        self.state = 'Y1'  # Начальное состояние
        self.checkpoint_counter = None
        if CHECKPOINT_COUNTER_AVAILABLE:
            self.checkpoint_counter = CheckpointCounter()
            logger.info("Инициализирована система подсчета чекпоинтов")
    
    def calculate_angle_to_target(self, player_x: float, player_y: float, 
                                  player_angle: float, target_x: float, 
                                  target_y: float) -> float:
        """
        Вычисляет угол поворота к цели
        Возвращает разницу углов в градусах (-180 до 180)
        """
        # Вектор к цели
        dx = target_x - player_x
        dy = target_y - player_y
        
        # Угол к цели в радианах
        target_angle_rad = math.atan2(dy, dx)
        target_angle = math.degrees(target_angle_rad)
        
        # Нормализуем углы в диапазон 0-360
        target_angle = (target_angle + 360) % 360
        player_angle = (player_angle + 360) % 360
        
        # Разница углов
        angle_diff = target_angle - player_angle
        
        # Нормализуем в диапазон -180 до 180
        if angle_diff > 180:
            angle_diff -= 360
        elif angle_diff < -180:
            angle_diff += 360
        
        return angle_diff
    
    def get_target_for_state(self, checkpoint_type: int, 
                            checkpoint_distance: float) -> Optional[Dict]:
        """
        Определяет, является ли текущий чекпоинт целью для текущего состояния
        """
        if checkpoint_type == 0:
            return None
        
        target_color = self.CHECKPOINT_TYPE_MAP.get(checkpoint_type)
        if not target_color:
            return None
        
        # Проверяем, соответствует ли цель текущему состоянию
        # (логика как в оригинальном get_current_target)
        if self.state == 'Y1' and target_color == 'yellow':
            return {'color': 'yellow', 'distance': checkpoint_distance}
        elif self.state == 'P1' and target_color == 'pink':
            return {'color': 'pink', 'distance': checkpoint_distance}
        elif self.state == 'G1' and target_color == 'green':
            return {'color': 'green', 'distance': checkpoint_distance}
        elif self.state == 'RED_UNTIL_WHITE' and target_color == 'red':
            return {'color': 'red', 'distance': checkpoint_distance}
        elif self.state == 'W1' and target_color == 'white':
            return {'color': 'white', 'distance': checkpoint_distance}
        elif self.state == 'P2' and target_color == 'pink':
            return {'color': 'pink', 'distance': checkpoint_distance}
        elif self.state == 'O_BEFORE_FIRST' and target_color == 'orange':
            return {'color': 'orange', 'distance': checkpoint_distance}
        elif self.state == 'RED_1_7' and target_color == 'red':
            return {'color': 'red', 'distance': checkpoint_distance}
        elif self.state == 'GREEN_AFTER_7' and target_color == 'green':
            return {'color': 'green', 'distance': checkpoint_distance}
        elif self.state == 'RED_8' and target_color == 'red':
            return {'color': 'red', 'distance': checkpoint_distance}
        # ... добавьте остальные состояния
        
        return None
    
    def update_state(self, target_color: str, distance: float):
        """Обновляет состояние на основе достигнутых целей"""
        # Логика обновления состояния (как в оригинале)
        # ...
        pass


class BoatBotNative:
    """Главный класс бота, использующий нативные API"""
    
    def __init__(self):
        self.data_reader = GameDataReader()
        self.control_sender = ControlSender()
        self.navigation = NavigationEngine()
        self.running = False
        self.paused = False
        
        # Параметры управления
        self.turn_threshold = 3.0  # Градусы
        self.min_distance = 5.0    # Метры (в игровых единицах)
        self.close_distance_threshold = 10.0
        
        # История для отслеживания
        self.last_checkpoint_id = None
        self.last_checkpoint_time = 0
        self.checkpoint_cooldown = 1.5  # Секунды между чекпоинтами
        
        # Счетчики
        self.red_squares_collected = 0
        
        logger.info("Бот инициализирован (нативные API)")
        logger.info("Убедитесь, что MoonLoader скрипт загружен в игру!")
    
    def run(self):
        """Основной цикл бота"""
        logger.info("=" * 60)
        logger.info("Запуск бота (нативные API через MoonLoader)")
        logger.info("=" * 60)
        logger.info("Нажмите Ctrl+C для остановки")
        logger.info("Нажмите Insert в игре для паузы/возобновления")
        
        self.running = True
        self.control_sender.send_command(True, 0)  # Включаем бота в игре
        
        consecutive_errors = 0
        last_log_time = 0
        
        try:
            while self.running:
                frame_start = time.time()
                
                # Читаем данные из игры
                game_data = self.data_reader.read_game_data()
                
                if not game_data:
                    consecutive_errors += 1
                    if consecutive_errors % 10 == 0:
                        logger.warning(f"Не удалось прочитать данные игры ({consecutive_errors} раз). Проверьте MoonLoader скрипт.")
                    time.sleep(0.1)
                    continue
                
                consecutive_errors = 0
                
                # Проверяем, включен ли бот в игре
                if not game_data['bot_enabled']:
                    if not self.paused:
                        logger.info("Бот выключен в игре (Insert нажат)")
                        self.paused = True
                    self.control_sender.send_command(False, 0)
                    time.sleep(0.1)
                    continue
                
                if self.paused:
                    logger.info("Бот возобновлен")
                    self.paused = False
                
                # Получаем данные игрока
                player_x = game_data['player_x']
                player_y = game_data['player_y']
                player_angle = game_data['player_angle']
                
                # Получаем данные чекпоинта
                checkpoint_type = game_data['checkpoint_type']
                checkpoint_distance = game_data['checkpoint_distance']
                checkpoint_id = game_data['checkpoint_id']
                
                # Определяем цель
                target = self.navigation.get_target_for_state(
                    checkpoint_type, checkpoint_distance
                )
                
                if not target:
                    # Цель не найдена - продолжаем движение вперед
                    self.control_sender.send_command(True, 1)  # W
                    time.sleep(0.016)  # ~60 FPS
                    continue
                
                # Вычисляем угол к цели
                if checkpoint_type > 0:
                    checkpoint_x = game_data['checkpoint_x']
                    checkpoint_y = game_data['checkpoint_y']
                    
                    angle_diff = self.navigation.calculate_angle_to_target(
                        player_x, player_y, player_angle,
                        checkpoint_x, checkpoint_y
                    )
                    
                    # Управление
                    abs_angle_diff = abs(angle_diff)
                    
                    # Адаптивный порог для красных чекпоинтов
                    threshold = self.turn_threshold
                    if target['color'] == 'red':
                        threshold = 0.1  # Максимальная точность для красных
                    elif checkpoint_distance < self.close_distance_threshold:
                        threshold = 1.0  # Более точное наведение близко к цели
                    
                    if abs_angle_diff > threshold:
                        if angle_diff > 0:
                            # Поворот вправо (D)
                            self.control_sender.send_command(True, 3)
                        else:
                            # Поворот влево (A)
                            self.control_sender.send_command(True, 2)
                    else:
                        # Движение вперед (W)
                        self.control_sender.send_command(True, 1)
                    
                    # Логирование (периодически)
                    current_time = time.time()
                    if current_time - last_log_time >= 0.5:
                        action = "Прямо"
                        if abs_angle_diff > threshold:
                            action = "Вправо (D)" if angle_diff > 0 else "Влево (A)"
                        
                        logger.info(f"State: {self.navigation.state} | "
                                  f"Target: {target['color']} | "
                                  f"Angle: {angle_diff:.1f}° | "
                                  f"Distance: {checkpoint_distance:.2f}м | "
                                  f"{action}")
                        last_log_time = current_time
                    
                    # Проверка достижения цели
                    if checkpoint_distance < self.min_distance:
                        self.handle_checkpoint_reached(
                            checkpoint_type, checkpoint_id, checkpoint_distance, target
                        )
                
                # Поддерживаем ~60 FPS
                frame_time = time.time() - frame_start
                sleep_time = max(0, 0.016 - frame_time)
                time.sleep(sleep_time)
        
        except KeyboardInterrupt:
            logger.info("Остановка бота...")
        except Exception as e:
            logger.error(f"Критическая ошибка: {e}", exc_info=True)
        finally:
            self.control_sender.stop()
            logger.info("Бот остановлен")
    
    def handle_checkpoint_reached(self, checkpoint_type: int, checkpoint_id: int,
                                 distance: float, target: Dict):
        """Обрабатывает достижение чекпоинта"""
        current_time = time.time()
        
        # Защита от повторного засчитывания
        if checkpoint_id == self.last_checkpoint_id:
            return
        
        # Защита от слишком частых засчитываний
        if current_time - self.last_checkpoint_time < self.checkpoint_cooldown:
            return
        
        self.last_checkpoint_id = checkpoint_id
        self.last_checkpoint_time = current_time
        
        # Обработка красных чекпоинтов
        if checkpoint_type == 1:  # Красный
            if self.navigation.checkpoint_counter:
                internal, external = self.navigation.checkpoint_counter.add_checkpoint()
                self.red_squares_collected = external
                logger.info(f"✓ Чекпоинт достигнут: internal={internal}, "
                          f"external={external}, distance={distance:.2f}м")
            else:
                self.red_squares_collected += 1
                logger.info(f"✓ Чекпоинт #{self.red_squares_collected} достигнут "
                          f"(distance={distance:.2f}м)")
        
        # Обновление состояния
        self.navigation.update_state(target['color'], distance)


def main():
    """Точка входа"""
    print("=" * 60)
    print("Бот для автоматического плавания на лодке в GTA SAMP")
    print("Использует нативные API через MoonLoader")
    print("=" * 60)
    print("\nТребования:")
    print("1. MoonLoader должен быть установлен")
    print("2. SAMPFUNCS должен быть установлен")
    print("3. boat_bot_ml.lua должен быть загружен в игру")
    print("4. Игра должна быть запущена")
    print("\nУправление:")
    print("- Insert в игре: пауза/возобновление")
    print("- Ctrl+C: остановка бота")
    print("=" * 60)
    
    input("\nНажмите Enter для запуска бота...")
    
    bot = BoatBotNative()
    bot.run()


if __name__ == "__main__":
    main()

