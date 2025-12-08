"""
Система работы для AI
"""
import random
import time
from typing import Dict, Optional, List
from enum import Enum


class WorkType(Enum):
    """Типы работы"""
    DELIVERY = "delivery"  # Доставка
    TAXI = "taxi"  # Такси
    TRUCKER = "trucker"  # Дальнобойщик
    MINER = "miner"  # Шахтер
    FISHER = "fisher"  # Рыбак
    MECHANIC = "mechanic"  # Механик
    NONE = "none"  # Без работы


class WorkSystem:
    """Система управления работой"""
    
    def __init__(self):
        """Инициализация системы работы"""
        self.current_work = WorkType.NONE
        self.work_start_time = None
        self.work_earnings = 0
        self.completed_jobs = 0
        self.current_job = None
        
        # Настройки работы
        self.work_preferences = {
            WorkType.DELIVERY: 0.3,
            WorkType.TAXI: 0.2,
            WorkType.TRUCKER: 0.15,
            WorkType.MINER: 0.1,
            WorkType.FISHER: 0.1,
            WorkType.MECHANIC: 0.15
        }
    
    def detect_work_opportunity(self, vision_data: Dict, game_data: Dict) -> Optional[WorkType]:
        """
        Определяет возможность работы на основе интерфейса
        
        Args:
            vision_data: Данные от модуля зрения
            game_data: Данные игры
            
        Returns:
            Optional[WorkType]: Тип доступной работы или None
        """
        text = vision_data.get('text', '').lower()
        
        # Поиск упоминаний работы в тексте
        work_keywords = {
            WorkType.DELIVERY: ['доставка', 'delivery', 'курьер', 'заказ'],
            WorkType.TAXI: ['такси', 'taxi', 'пассажир', 'поездка'],
            WorkType.TRUCKER: ['груз', 'trucker', 'фура', 'перевозка'],
            WorkType.MINER: ['шахта', 'miner', 'руда', 'копать'],
            WorkType.FISHER: ['рыбак', 'fisher', 'рыба', 'улов'],
            WorkType.MECHANIC: ['механик', 'mechanic', 'ремонт', 'машина']
        }
        
        for work_type, keywords in work_keywords.items():
            if any(keyword in text for keyword in keywords):
                return work_type
        
        # Проверка визуальных маркеров работы
        if vision_data.get('has_work_marker', False):
            # Выбираем случайную работу на основе предпочтений
            return self._select_work_by_preference()
        
        return None
    
    def _select_work_by_preference(self) -> WorkType:
        """
        Выбирает работу на основе предпочтений
        
        Returns:
            WorkType: Выбранный тип работы
        """
        works = list(self.work_preferences.keys())
        weights = list(self.work_preferences.values())
        return random.choices(works, weights=weights)[0]
    
    def start_work(self, work_type: WorkType):
        """
        Начинает работу
        
        Args:
            work_type: Тип работы
        """
        self.current_work = work_type
        self.work_start_time = time.time()
        self.current_job = {
            'type': work_type,
            'start_time': self.work_start_time,
            'target': None,
            'status': 'active'
        }
        print(f"Начата работа: {work_type.value}")
    
    def stop_work(self):
        """Останавливает работу"""
        if self.current_work != WorkType.NONE:
            duration = time.time() - self.work_start_time if self.work_start_time else 0
            print(f"Работа остановлена: {self.current_work.value}, длительность: {duration:.1f}с")
            self.current_work = WorkType.NONE
            self.work_start_time = None
            self.current_job = None
    
    def process_work(self, vision_data: Dict, game_data: Dict) -> Dict:
        """
        Обрабатывает текущую работу
        
        Args:
            vision_data: Данные от модуля зрения
            game_data: Данные игры
            
        Returns:
            Dict: Команды для выполнения работы
        """
        if self.current_work == WorkType.NONE:
            return {'action': 'idle'}
        
        commands = {
            'action': 'work',
            'work_type': self.current_work.value
        }
        
        if self.current_work == WorkType.DELIVERY:
            commands.update(self._process_delivery(vision_data, game_data))
        elif self.current_work == WorkType.TAXI:
            commands.update(self._process_taxi(vision_data, game_data))
        elif self.current_work == WorkType.TRUCKER:
            commands.update(self._process_trucker(vision_data, game_data))
        elif self.current_work == WorkType.MINER:
            commands.update(self._process_miner(vision_data, game_data))
        elif self.current_work == WorkType.FISHER:
            commands.update(self._process_fisher(vision_data, game_data))
        elif self.current_work == WorkType.MECHANIC:
            commands.update(self._process_mechanic(vision_data, game_data))
        
        return commands
    
    def _process_delivery(self, vision_data: Dict, game_data: Dict) -> Dict:
        """Обработка работы доставщика"""
        # Логика доставки
        # 1. Взять заказ
        # 2. Найти адрес доставки
        # 3. Доставить заказ
        # 4. Получить оплату
        
        if not self.current_job.get('target'):
            # Ищем точку приема заказа
            return {
                'sub_action': 'find_pickup',
                'move_to': 'work_location'
            }
        else:
            # Доставляем заказ
            return {
                'sub_action': 'deliver',
                'target': self.current_job['target']
            }
    
    def _process_taxi(self, vision_data: Dict, game_data: Dict) -> Dict:
        """Обработка работы таксиста"""
        # Логика такси
        # 1. Найти пассажира
        # 2. Подобрать пассажира
        # 3. Отвезти в пункт назначения
        # 4. Получить оплату
        
        if not self.current_job.get('passenger'):
            return {
                'sub_action': 'find_passenger',
                'move_to': 'taxi_stand'
            }
        elif not self.current_job.get('destination'):
            return {
                'sub_action': 'pickup_passenger'
            }
        else:
            return {
                'sub_action': 'drive_to_destination',
                'destination': self.current_job['destination']
            }
    
    def _process_trucker(self, vision_data: Dict, game_data: Dict) -> Dict:
        """Обработка работы дальнобойщика"""
        return {
            'sub_action': 'drive_route',
            'route': 'long_distance'
        }
    
    def _process_miner(self, vision_data: Dict, game_data: Dict) -> Dict:
        """Обработка работы шахтера"""
        return {
            'sub_action': 'mine_ore',
            'location': 'mine'
        }
    
    def _process_fisher(self, vision_data: Dict, game_data: Dict) -> Dict:
        """Обработка работы рыбака"""
        return {
            'sub_action': 'fish',
            'location': 'water'
        }
    
    def _process_mechanic(self, vision_data: Dict, game_data: Dict) -> Dict:
        """Обработка работы механика"""
        return {
            'sub_action': 'repair_vehicle',
            'location': 'garage'
        }
    
    def complete_job(self, earnings: float = 0):
        """
        Завершает задание
        
        Args:
            earnings: Заработанная сумма
        """
        if self.current_job:
            self.completed_jobs += 1
            self.work_earnings += earnings
            print(f"Задание завершено! Заработано: ${earnings:.2f}")
            self.current_job = None

