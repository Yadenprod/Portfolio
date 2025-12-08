"""
Система самообучения AI - учится на опыте и улучшает свои действия
"""
import json
import time
import random
import numpy as np
from typing import Dict, List, Optional, Tuple
from collections import defaultdict
from datetime import datetime
import os


class ExperienceMemory:
    """Память опыта для обучения"""
    
    def __init__(self, max_size: int = 10000):
        """
        Инициализация памяти
        
        Args:
            max_size: Максимальный размер памяти
        """
        self.memory = []
        self.max_size = max_size
        self.successful_actions = defaultdict(list)
        self.failed_actions = defaultdict(list)
    
    def add_experience(self, state: Dict, action: Dict, reward: float, 
                      next_state: Dict, success: bool):
        """
        Добавляет опыт в память
        
        Args:
            state: Состояние до действия
            action: Выполненное действие
            reward: Награда за действие
            next_state: Состояние после действия
            success: Успешно ли выполнено действие
        """
        experience = {
            'timestamp': time.time(),
            'state': state,
            'action': action,
            'reward': reward,
            'next_state': next_state,
            'success': success
        }
        
        self.memory.append(experience)
        
        # Сохраняем успешные и неуспешные действия
        # Убеждаемся что action - словарь
        if isinstance(action, dict):
            action_key = f"{action.get('action', 'unknown')}"
        else:
            action_key = str(action) if action else 'unknown'
        if success:
            self.successful_actions[action_key].append(experience)
        else:
            self.failed_actions[action_key].append(experience)
        
        # Ограничиваем размер памяти
        if len(self.memory) > self.max_size:
            self.memory.pop(0)
        
        # Ограничиваем размер списков успешных/неуспешных действий
        for key in self.successful_actions:
            if len(self.successful_actions[key]) > 1000:
                self.successful_actions[key] = self.successful_actions[key][-1000:]
        for key in self.failed_actions:
            if len(self.failed_actions[key]) > 1000:
                self.failed_actions[key] = self.failed_actions[key][-1000:]
    
    def get_successful_patterns(self, action_type: str) -> List[Dict]:
        """
        Возвращает успешные паттерны для действия
        
        Args:
            action_type: Тип действия
            
        Returns:
            List[Dict]: Список успешных опытов
        """
        return self.successful_actions.get(action_type, [])
    
    def get_failed_patterns(self, action_type: str) -> List[Dict]:
        """
        Возвращает неуспешные паттерны для действия
        
        Args:
            action_type: Тип действия
            
        Returns:
            List[Dict]: Список неуспешных опытов
        """
        return self.failed_actions.get(action_type, [])


class LearningSystem:
    """Система обучения AI на основе опыта"""
    
    def __init__(self, memory_path: str = "learning_data"):
        """
        Инициализация системы обучения
        
        Args:
            memory_path: Путь для сохранения данных обучения
        """
        self.memory = ExperienceMemory()
        self.memory_path = memory_path
        self.learning_stats = {
            'total_experiences': 0,
            'successful_actions': 0,
            'failed_actions': 0,
            'learning_rate': 0.1,
            'exploration_rate': 0.3,  # Начальная вероятность исследования
            'min_exploration_rate': 0.05,
            'exploration_decay': 0.995
        }
        
        # Статистика по типам действий
        self.action_stats = defaultdict(lambda: {
            'success_count': 0,
            'fail_count': 0,
            'total_reward': 0.0,
            'avg_reward': 0.0
        })
        
        # Загружаем сохраненные данные
        self.load_learning_data()
    
    def calculate_reward(self, action: Dict, result: Dict, 
                        game_state: Dict) -> float:
        """
        Вычисляет награду за действие
        
        Args:
            action: Выполненное действие
            result: Результат действия
            game_state: Состояние игры
            
        Returns:
            float: Награда (-1.0 до 1.0)
        """
        reward = 0.0
        
        # Убеждаемся что action - словарь
        if isinstance(action, str):
            action = {'action': action}
        elif not isinstance(action, dict):
            action = {'action': 'unknown'}
        
        # Награда за успешное выполнение
        if result.get('success', False):
            reward += 0.5
        
        # Награда за заработок
        if result.get('earnings', 0) > 0:
            reward += min(0.3, result['earnings'] / 1000.0)
        
        # Награда за завершение задания
        if result.get('job_completed', False):
            reward += 0.4
        
        # Штраф за ошибки
        if result.get('error', False):
            reward -= 0.3
        
        # Штраф за застревание
        if result.get('stuck', False):
            reward -= 0.5
        
        # Штраф за смерть
        if result.get('death', False):
            reward -= 1.0
        
        # Награда за улучшение здоровья
        health_change = result.get('health_change', 0)
        if health_change > 0:
            reward += 0.1
        
        # Награда за исследование
        if action.get('action') == 'explore':
            reward += 0.1
        
        return max(-1.0, min(1.0, reward))
    
    def learn_from_experience(self, state: Dict, action: Dict, 
                            result: Dict, next_state: Dict):
        """
        Обучается на опыте
        
        Args:
            state: Состояние до действия
            action: Выполненное действие
            result: Результат действия
            next_state: Состояние после действия
        """
        # Убеждаемся что action - словарь
        if isinstance(action, str):
            action = {'action': action}
        elif not isinstance(action, dict):
            action = {'action': 'unknown'}
        
        # Вычисляем награду
        reward = self.calculate_reward(action, result, next_state)
        
        # Определяем успешность
        success = reward > 0.2
        
        # Добавляем опыт в память
        self.memory.add_experience(state, action, reward, next_state, success)
        
        # Обновляем статистику
        self.learning_stats['total_experiences'] += 1
        if success:
            self.learning_stats['successful_actions'] += 1
        else:
            self.learning_stats['failed_actions'] += 1
        
        # Обновляем статистику по типу действия
        action_type = action.get('action', 'unknown')
        stats = self.action_stats[action_type]
        if success:
            stats['success_count'] += 1
        else:
            stats['fail_count'] += 1
        stats['total_reward'] += reward
        stats['avg_reward'] = stats['total_reward'] / (
            stats['success_count'] + stats['fail_count']
        )
        
        # Уменьшаем exploration rate (меньше исследования со временем)
        if self.learning_stats['exploration_rate'] > self.learning_stats['min_exploration_rate']:
            self.learning_stats['exploration_rate'] *= self.learning_stats['exploration_decay']
    
    def should_explore(self) -> bool:
        """
        Определяет, нужно ли исследовать новые действия
        
        Returns:
            bool: True если нужно исследовать
        """
        return random.random() < self.learning_stats['exploration_rate']
    
    def get_best_action(self, state: Dict, possible_actions: List[Dict]) -> Optional[Dict]:
        """
        Возвращает лучшее действие на основе опыта
        
        Args:
            state: Текущее состояние
            possible_actions: Возможные действия
            
        Returns:
            Optional[Dict]: Лучшее действие или None
        """
        if not possible_actions:
            return None
        
        # Если нужно исследовать - случайное действие
        if self.should_explore():
            return random.choice(possible_actions)
        
        # Выбираем действие на основе опыта
        best_action = None
        best_score = float('-inf')
        
        for action in possible_actions:
            # Убеждаемся что action - словарь
            if isinstance(action, str):
                action = {'action': action}
            elif not isinstance(action, dict):
                action = {'action': 'unknown'}
            
            action_type = action.get('action', 'unknown')
            stats = self.action_stats[action_type]
            
            # Вычисляем score на основе успешности
            total_attempts = stats['success_count'] + stats['fail_count']
            if total_attempts > 0:
                success_rate = stats['success_count'] / total_attempts
                score = success_rate * 0.6 + stats['avg_reward'] * 0.4
            else:
                # Если нет опыта - средний score для исследования
                score = 0.3
            
            if score > best_score:
                best_score = score
                best_action = action
        
        return best_action or random.choice(possible_actions)
    
    def improve_strategy(self, action_type: str) -> Dict:
        """
        Улучшает стратегию для типа действия на основе опыта
        
        Args:
            action_type: Тип действия
            
        Returns:
            Dict: Улучшенная стратегия
        """
        successful_patterns = self.memory.get_successful_patterns(action_type)
        failed_patterns = self.memory.get_failed_patterns(action_type)
        
        if not successful_patterns:
            return {}
        
        # Анализируем успешные паттерны
        successful_states = [exp['state'] for exp in successful_patterns]
        successful_actions = [exp['action'] for exp in successful_patterns]
        
        # Находим общие черты успешных действий
        strategy = {
            'preferred_conditions': {},
            'avoid_conditions': {},
            'optimal_timing': None,
            'success_rate': len(successful_patterns) / (
                len(successful_patterns) + len(failed_patterns) + 1
            )
        }
        
        # Анализируем условия успеха
        if successful_states:
            # Пример: если успешно работали утром - предпочитаем утро
            # Это упрощенный пример, можно расширить
            pass  # TODO: Реализовать анализ условий успеха
        
        return strategy
    
    def adapt_behavior(self, current_state: Dict, 
                      available_actions: List[Dict]) -> Dict:
        """
        Адаптирует поведение на основе опыта
        
        Args:
            current_state: Текущее состояние
            available_actions: Доступные действия
            
        Returns:
            Dict: Адаптированное действие
        """
        # Получаем лучшее действие на основе опыта
        best_action = self.get_best_action(current_state, available_actions)
        
        if best_action:
            # Убеждаемся что best_action - словарь
            if isinstance(best_action, str):
                best_action = {'action': best_action}
            elif not isinstance(best_action, dict):
                best_action = {'action': 'unknown'}
            
            # Применяем улучшенную стратегию
            strategy = self.improve_strategy(best_action.get('action', 'unknown'))
            
            # Модифицируем действие на основе стратегии
            if strategy:
                best_action = best_action.copy()
                # Добавляем информацию из стратегии
                best_action['strategy'] = strategy
        
        return best_action or random.choice(available_actions)
    
    def save_learning_data(self):
        """Сохраняет данные обучения"""
        if not os.path.exists(self.memory_path):
            os.makedirs(self.memory_path)
        
        # Сохраняем статистику
        stats_file = os.path.join(self.memory_path, 'learning_stats.json')
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump({
                'learning_stats': self.learning_stats,
                'action_stats': dict(self.action_stats)
            }, f, indent=2, ensure_ascii=False)
        
        # Сохраняем последние опыты (для анализа)
        recent_experiences = self.memory.memory[-1000:]  # Последние 1000
        experiences_file = os.path.join(self.memory_path, 'recent_experiences.json')
        with open(experiences_file, 'w', encoding='utf-8') as f:
            json.dump(recent_experiences, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"💾 Данные обучения сохранены: {len(self.memory.memory)} опытов")
    
    def load_learning_data(self):
        """Загружает сохраненные данные обучения"""
        stats_file = os.path.join(self.memory_path, 'learning_stats.json')
        
        if os.path.exists(stats_file):
            try:
                with open(stats_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.learning_stats.update(data.get('learning_stats', {}))
                    self.action_stats = defaultdict(
                        lambda: {
                            'success_count': 0,
                            'fail_count': 0,
                            'total_reward': 0.0,
                            'avg_reward': 0.0
                        },
                        data.get('action_stats', {})
                    )
                print(f"📚 Загружены данные обучения: {self.learning_stats['total_experiences']} опытов")
            except Exception as e:
                print(f"⚠️ Ошибка загрузки данных обучения: {e}")
        else:
            print("📝 Начинаем обучение с нуля...")
    
    def get_learning_statistics(self) -> Dict:
        """
        Возвращает статистику обучения
        
        Returns:
            Dict: Статистика
        """
        total = self.learning_stats['total_experiences']
        success = self.learning_stats['successful_actions']
        fail = self.learning_stats['failed_actions']
        
        success_rate = (success / total * 100) if total > 0 else 0
        
        return {
            'total_experiences': total,
            'successful_actions': success,
            'failed_actions': fail,
            'success_rate': success_rate,
            'exploration_rate': self.learning_stats['exploration_rate'],
            'action_stats': dict(self.action_stats),
            'memory_size': len(self.memory.memory)
        }

