"""
Система определения успешности действий AI
"""
import time
import re
from typing import Dict, Optional
from collections import deque


class SuccessDetector:
    """Определяет успешность действий на основе изменений в игре"""
    
    def __init__(self):
        """Инициализация детектора успеха"""
        self.state_history = deque(maxlen=10)  # История состояний
        self.last_money = 0
        self.last_health = 100.0  # Убеждаемся что это float
        self.last_position = None
        self.action_start_time = None
        self.current_action = None
        
        # Пороги для определения успеха
        self.money_threshold = 10  # Минимальное изменение денег
        self.health_threshold = 5  # Минимальное изменение здоровья
        self.timeout_threshold = 30  # Таймаут для действия (секунды)
    
    def start_action(self, action: Dict, game_state: Dict):
        """
        Начинает отслеживание действия
        
        Args:
            action: Выполняемое действие
            game_state: Текущее состояние игры
        """
        self.current_action = action
        self.action_start_time = time.time()
        
        # Сохраняем начальное состояние
        self.last_money = game_state.get('money', 0)
        self.last_health = game_state.get('health', 100)
        self.last_position = game_state.get('position')
    
    def detect_success(self, action: Dict, game_state: Dict, 
                      vision_data: Dict) -> Dict:
        """
        Определяет успешность действия
        
        Args:
            action: Выполненное действие
            game_state: Состояние игры после действия
            vision_data: Данные зрения
            
        Returns:
            Dict: Результат с информацией об успешности
        """
        result = {
            'success': False,
            'reason': 'unknown',
            'earnings': 0,
            'health_change': 0,
            'job_completed': False,
            'error': False,
            'stuck': False,
            'death': False,
            'timeout': False,
            'progress': False
        }
        
        # Проверка таймаута
        if self.action_start_time:
            action_duration = time.time() - self.action_start_time
            if action_duration > self.timeout_threshold:
                result['timeout'] = True
                result['success'] = False
                result['reason'] = 'timeout'
                return result
        
        # Определение типа действия
        # Проверяем, что action - это словарь
        if isinstance(action, str):
            action_type = action
            action = {'action': action}
        else:
            action_type = action.get('action', 'unknown')
        
        # Проверка смерти
        current_health = game_state.get('health', 100)
        if current_health <= 0:
            result['death'] = True
            result['success'] = False
            result['reason'] = 'death'
            return result
        
        # Проверка изменения здоровья
        # Убеждаемся что оба значения - числа
        try:
            current_health = float(current_health) if current_health is not None else 100.0
            last_health = float(self.last_health) if self.last_health is not None else 100.0
            health_change = current_health - last_health
        except (TypeError, ValueError):
            health_change = 0.0
        result['health_change'] = health_change
        
        if health_change < -20:  # Сильная потеря здоровья
            result['error'] = True
            result['success'] = False
            result['reason'] = 'health_loss'
            return result
        
        # Проверка застревания (если позиция не меняется)
        current_position = game_state.get('position')
        if current_position and self.last_position:
            if current_position == self.last_position:
                result['stuck'] = True
                result['success'] = False
                result['reason'] = 'stuck'
                # Но не возвращаем сразу - может быть нормально для некоторых действий
        
        # Определение успеха в зависимости от типа действия
        if action_type == 'work':
            result = self._detect_work_success(action, game_state, vision_data, result)
        elif action_type == 'drive_to_target':
            result = self._detect_driving_success(action, game_state, vision_data, result)
        elif action_type == 'interact':
            result = self._detect_interaction_success(action, game_state, vision_data, result)
        elif action_type == 'find_work':
            result = self._detect_find_work_success(action, game_state, vision_data, result)
        elif action_type == 'explore':
            result = self._detect_explore_success(action, game_state, vision_data, result)
        else:
            # Для неизвестных действий - проверяем общие признаки
            result = self._detect_general_success(action, game_state, vision_data, result)
        
        # Обновляем сохраненные значения
        self.last_money = game_state.get('money', self.last_money)
        # Убеждаемся что health - это число
        try:
            self.last_health = float(current_health) if current_health is not None else 100.0
        except (TypeError, ValueError):
            self.last_health = 100.0
        self.last_position = current_position
        
        return result
    
    def _detect_work_success(self, action: Dict, game_state: Dict,
                            vision_data: Dict, result: Dict) -> Dict:
        """Определяет успех работы"""
        # Проверяем текст на наличие признаков успеха
        text = vision_data.get('text', '').lower()
        
        # Признаки успешного завершения работы
        success_keywords = [
            'задание выполнено', 'job completed', 'заработано', 'earned',
            'оплата получена', 'payment received', 'успешно', 'success'
        ]
        
        # Признаки ошибки
        error_keywords = [
            'ошибка', 'error', 'не удалось', 'failed', 'провал', 'fail'
        ]
        
        # Проверка на успех
        if any(keyword in text for keyword in success_keywords):
            result['success'] = True
            result['job_completed'] = True
            result['reason'] = 'job_completed'
            
            # Пытаемся извлечь сумму заработка из текста
            # (упрощенная версия, можно улучшить)
            if 'заработано' in text or 'earned' in text:
                # Пытаемся найти число после ключевого слова
                numbers = re.findall(r'\d+', text)
                if numbers:
                    result['earnings'] = float(numbers[0])
        
        # Проверка на ошибку
        elif any(keyword in text for keyword in error_keywords):
            result['error'] = True
            result['success'] = False
            result['reason'] = 'work_error'
        
        # Если нет явных признаков - считаем успешным если нет ошибок
        elif not result.get('error') and not result.get('stuck'):
            result['success'] = True
            result['reason'] = 'work_in_progress'
        
        return result
    
    def _detect_driving_success(self, action: Dict, game_state: Dict,
                               vision_data: Dict, result: Dict) -> Dict:
        """Определяет успех вождения"""
        # Проверяем, достигли ли цели
        minimap_data = vision_data.get('minimap_data', {})
        targets = minimap_data.get('targets', [])
        
        # Если целей нет - возможно достигли
        if not targets:
            result['success'] = True
            result['reason'] = 'target_reached'
        # Если есть цели - движемся к ним (прогресс)
        elif targets:
            result['progress'] = True
            result['success'] = True  # Прогресс = успех
            result['reason'] = 'moving_to_target'
        # Если застряли
        elif result.get('stuck'):
            result['success'] = False
            result['reason'] = 'stuck_while_driving'
        
        return result
    
    def _detect_interaction_success(self, action: Dict, game_state: Dict,
                                    vision_data: Dict, result: Dict) -> Dict:
        """Определяет успех взаимодействия"""
        # Проверяем, появилось ли что-то после взаимодействия
        text = vision_data.get('text', '').lower()
        
        # Признаки успешного взаимодействия
        if any(keyword in text for keyword in ['открыто', 'opened', 'взаимодействие', 'interaction']):
            result['success'] = True
            result['reason'] = 'interaction_success'
        # Если нет признаков ошибки - считаем успешным
        elif not result.get('error'):
            result['success'] = True
            result['reason'] = 'interaction_completed'
        
        return result
    
    def _detect_find_work_success(self, action: Dict, game_state: Dict,
                                 vision_data: Dict, result: Dict) -> Dict:
        """Определяет успех поиска работы"""
        # Проверяем наличие маркеров работы
        has_work = vision_data.get('has_work_marker', False)
        text = vision_data.get('text', '').lower()
        
        # Признаки найденной работы
        work_keywords = ['работа', 'work', 'задание', 'job', 'доставка', 'delivery']
        
        if has_work or any(keyword in text for keyword in work_keywords):
            result['success'] = True
            result['reason'] = 'work_found'
        else:
            result['success'] = False
            result['reason'] = 'work_not_found'
        
        return result
    
    def _detect_explore_success(self, action: Dict, game_state: Dict,
                               vision_data: Dict, result: Dict) -> Dict:
        """Определяет успех исследования"""
        # Исследование успешно если:
        # - Не застряли
        # - Не умерли
        # - Позиция изменилась (двигаемся)
        
        current_position = game_state.get('position')
        if current_position and self.last_position:
            if current_position != self.last_position:
                result['success'] = True
                result['reason'] = 'exploring'
            else:
                result['success'] = False
                result['reason'] = 'not_moving'
        else:
            # Если нет данных о позиции - считаем успешным если нет ошибок
            if not result.get('error') and not result.get('stuck'):
                result['success'] = True
                result['reason'] = 'exploring'
        
        return result
    
    def _detect_general_success(self, action: Dict, game_state: Dict,
                               vision_data: Dict, result: Dict) -> Dict:
        """Определяет общий успех для неизвестных действий"""
        # Общие признаки успеха:
        # - Нет ошибок
        # - Нет застревания
        # - Здоровье не упало сильно
        # - Не умерли
        
        if (not result.get('error') and 
            not result.get('stuck') and 
            not result.get('death') and
            result.get('health_change', 0) > -10):
            result['success'] = True
            result['reason'] = 'no_errors'
        else:
            result['success'] = False
            result['reason'] = 'has_errors'
        
        return result

