"""
Главный файл для запуска полноценного автономного AI-ассистента
"""
import time
import cv2
from typing import Dict, Optional
from screen_capture import ScreenCapture
from vision import VisionProcessor
from decision_maker import DecisionMaker, Action
from controller import GameController
from state_machine import StateMachine, GameState
from navigation import NavigationSystem
from work_system import WorkSystem, WorkType
from human_behavior import HumanBehaviorSimulator
from autonomous_life import AutonomousLife
from auto_recovery import AutoRecovery
from learning_system import LearningSystem
from success_detector import SuccessDetector
from world_navigation import WorldNavigation
import keyboard
import random


class GTA_RP_AI:
    """Главный класс полноценного автономного AI-ассистента"""
    
    def __init__(self):
        """Инициализация всех компонентов"""
        print("=" * 50)
        print("Инициализация GTA RP AI - Автономный режим")
        print("=" * 50)
        
        # Основные компоненты
        self.screen_capture = ScreenCapture()
        self.vision = VisionProcessor()
        self.decision_maker = DecisionMaker()
        self.controller = GameController()
        
        # Новые системы
        self.state_machine = StateMachine()
        self.navigation = NavigationSystem()
        self.work_system = WorkSystem()
        self.human_behavior = HumanBehaviorSimulator()
        self.autonomous_life = AutonomousLife()
        self.auto_recovery = AutoRecovery()
        self.learning_system = LearningSystem()  # Система самообучения
        self.success_detector = SuccessDetector()  # Детектор успеха
        self.world_navigation = WorldNavigation()  # Навигация по открытому миру
        
        # Настройки
        self.running = False
        self.auto_start = True  # Автоматический запуск
        self.fps = 2  # Кадров в секунду для обработки (можно увеличить)
        self.last_frame_time = time.time()
        self.last_activity_decision = time.time()
        self.current_activity = None
        
        # Статистика
        self.stats = {
            'frames_processed': 0,
            'work_earnings': 0,
            'distance_traveled': 0,
            'session_start': time.time()
        }
        
        # Автономные настройки
        self.last_daily_reset = time.time()
        self.daily_reset_interval = 86400  # 24 часа в секундах
        
        # Настройки обучения
        self.last_learning_save = time.time()
        self.learning_save_interval = 300  # Сохраняем каждые 5 минут
        self.last_state = None  # Предыдущее состояние для обучения
        
        print("\n✓ Все системы инициализированы!")
        print("\n🤖 РЕЖИМ: ПОЛНАЯ АВТОНОМНОСТЬ + САМООБУЧЕНИЕ")
        print("   AI будет работать самостоятельно и УЧИТЬСЯ на опыте!")
        print("   Чем больше играет - тем лучше становится!")
        print("\nУправление:")
        print("  F9  - Запуск/остановка AI")
        print("  F10 - Выход из программы")
        print("  F11 - Показать статистику")
        print("\n" + "=" * 50)
        
        # Автоматический запуск через 5 секунд
        if self.auto_start:
            print("\n⏳ Автоматический запуск через 5 секунд...")
            print("   (Нажмите F9 для немедленного запуска или отмены)")
            time.sleep(5)
            if not self.running:  # Если не отменили
                self.toggle()
    
    def process_frame(self, frame: cv2.Mat) -> Dict:
        """
        Обрабатывает один кадр и принимает решения
        
        Args:
            frame: Изображение кадра
            
        Returns:
            Dict: Результаты обработки
        """
        self.stats['frames_processed'] += 1
        
        # Обработка изображения
        processed_frame = self.vision.preprocess_image(frame)
        
        # Извлечение данных из интерфейса
        minimap = self.vision.detect_minimap(processed_frame)
        minimap_data = self.navigation.extract_minimap_data(minimap)
        
        # Навигация по открытому миру
        player_pos = self.world_navigation.get_player_position(minimap)
        
        # Распознавание текста
        chat_text = self.vision.detect_chat_text(processed_frame)
        interface_text = self.vision.detect_text(processed_frame)
        
        # Определение состояния игры
        health = self.vision.detect_health_bar(processed_frame)
        in_vehicle = self.vision.detect_vehicle(processed_frame)
        has_interaction = self.vision.detect_interaction_prompt(processed_frame)
        has_work_marker = self.vision.detect_work_marker(processed_frame)
        players_nearby = self.vision.detect_players_nearby(processed_frame)
        
        # Создание game_state
        game_state = {
            'health': health,
            'in_vehicle': in_vehicle,
            'players_nearby': players_nearby,
            'has_police': False,  # TODO: реализовать детекцию полиции
            'position': player_pos,
            'frame': processed_frame,
        }
        
        # Формирование данных для принятия решений
        vision_data = {
            'text': interface_text + ' ' + chat_text,
            'chat_text': chat_text,
            'has_enemies': False,  # TODO: реализовать детекцию
            'has_obstacles': False,  # TODO: реализовать детекцию
            'on_road': self.navigation.is_on_road(minimap_data),
            'near_object': has_interaction,
            'has_work_marker': has_work_marker,
            'minimap_data': minimap_data,
            'minimap_image': minimap,  # Сохраняем изображение мини-карты
            'processed_frame': processed_frame,  # Сохраняем обработанный кадр
        }
        
        game_state = {
            'health': health,
            'in_vehicle': in_vehicle,
            'players_nearby': players_nearby,
            'has_police': False,  # TODO: реализовать детекцию полиции
            'frame': processed_frame,
        }
        
        # Проверка на ошибки и восстановление
        error_state = self.auto_recovery.detect_error_state(game_state, vision_data)
        if error_state:
            result = self.handle_recovery(error_state)
            return {
                'state': self.state_machine.current_state,
                'action': result,
                'processed_frame': processed_frame,
                'recovery_mode': True
            }
        
        # Автоматический сброс целей на новый день
        if time.time() - self.last_daily_reset > self.daily_reset_interval:
            self.autonomous_life.daily_plan.reset_daily_goals()
            self.last_daily_reset = time.time()
            self.auto_recovery.reset_error_count()
        
        # Автономное планирование активности с учетом обучения
        if time.time() - self.last_activity_decision > 30:  # Каждые 30 секунд
            # Получаем возможные активности
            possible_activities = [
                {'action': 'work', 'priority': 'normal', 'reason': 'daily_plan'},
                {'action': 'rest', 'duration': random.uniform(300, 900), 'reason': 'scheduled_rest'},
                {'action': 'explore', 'duration': random.uniform(600, 1800), 'reason': 'leisure'},
                {'action': 'walk_around', 'duration': random.uniform(300, 900), 'reason': 'free_time'},
                {'action': 'drive_around', 'duration': random.uniform(300, 900), 'reason': 'free_time'}
            ]
            
            # Используем обучение для выбора лучшей активности
            if self.learning_system.learning_stats['total_experiences'] > 10:
                # Если есть опыт - используем обучение
                learned_decision = self.learning_system.adapt_behavior(game_state, possible_activities)
                activity_decision = learned_decision
            else:
                # Если опыта мало - используем автономную систему
                activity_decision = self.autonomous_life.decide_next_activity(game_state)
            
            self.current_activity = activity_decision
            self.last_activity_decision = time.time()
            activity_name = activity_decision.get('action', 'unknown')
            reason = activity_decision.get('reason', '')
            learning_note = " (обучение)" if self.learning_system.learning_stats['total_experiences'] > 10 else ""
            print(f"📋 AI решил: {activity_name} ({reason}){learning_note}")
        
        # Проверка необходимости смены состояния
        new_state = self.state_machine.should_change_state(game_state)
        if new_state:
            self.state_machine.transition_to(new_state)
        
        # Обработка текущего состояния с учетом автономного планирования
        result = self.handle_current_state(vision_data, game_state, self.current_activity)
        
        # Обучение на основе опыта
        if self.last_state is not None and result.get('action'):
            # Убеждаемся, что action - это словарь
            action_for_learning = result.get('action', {})
            if isinstance(action_for_learning, str):
                action_for_learning = {'action': action_for_learning}
            elif not isinstance(action_for_learning, dict):
                action_for_learning = {'action': 'unknown'}
            
            # Определяем успешность действия через детектор
            learning_result = self.success_detector.detect_success(
                action_for_learning,
                game_state,
                vision_data
            )
            
            # Дополнительная информация из error_state (если была обнаружена ранее)
            if error_state:
                learning_result['error'] = True
                if error_state.get('reason') == 'stuck':
                    learning_result['stuck'] = True
                if error_state.get('reason') == 'death':
                    learning_result['death'] = True
            
            # Обучаемся на опыте (используем уже обработанный action_for_learning)
            self.learning_system.learn_from_experience(
                self.last_state,
                action_for_learning,
                learning_result,
                game_state
            )
            
            # Логируем результат для отладки (первые 50 опытов)
            if self.learning_system.learning_stats['total_experiences'] <= 50:
                action_name = action_for_learning.get('action', 'unknown')
                success = learning_result.get('success', False)
                reason = learning_result.get('reason', 'unknown')
                print(f"  📊 Опыт #{self.learning_system.learning_stats['total_experiences']}: "
                      f"{action_name} - {'✅' if success else '❌'} ({reason})")
        
        # Сохраняем текущее состояние для следующего цикла
        self.last_state = game_state.copy()
        
        # Периодическое сохранение данных обучения
        if time.time() - self.last_learning_save > self.learning_save_interval:
            self.learning_system.save_learning_data()
            self.last_learning_save = time.time()
        
        return {
            'state': self.state_machine.current_state,
            'action': result,  # result уже является словарем с действием
            'processed_frame': processed_frame
        }
    
    def handle_recovery(self, recovery_data: Dict) -> Dict:
        """
        Обрабатывает восстановление после ошибки
        
        Args:
            recovery_data: Данные для восстановления
            
        Returns:
            Dict: Действия для восстановления
        """
        recovery_action = recovery_data.get('recovery_action', {})
        action_type = recovery_action.get('action', 'wait')
        
        if action_type == 'move_backward':
            return {'action': 'move_backward', 'duration': recovery_action.get('duration', 2.0)}
        elif action_type == 'jump':
            count = recovery_action.get('count', 3)
            return {'action': 'jump_multiple', 'count': count}
        elif action_type == 'turn_around':
            return {'action': 'turn_around', 'angle': recovery_action.get('angle', 180)}
        elif action_type == 'wait_respawn':
            return {'action': 'wait', 'duration': recovery_action.get('duration', 10)}
        elif action_type == 'stop_vehicle':
            return {'action': 'stop_vehicle'}
        else:
            return {'action': 'wait', 'duration': 5}
    
    def handle_current_state(self, vision_data: Dict, game_state: Dict, 
                            activity_decision: Optional[Dict] = None) -> Dict:
        """
        Обрабатывает текущее состояние игры
        
        Args:
            vision_data: Данные от модуля зрения
            game_state: Состояние игры
            
        Returns:
            Dict: Команды для выполнения
        """
        current_state = self.state_machine.current_state
        
        if current_state == GameState.WORKING:
            return self.handle_working_state(vision_data, game_state)
        elif current_state == GameState.DRIVING:
            return self.handle_driving_state(vision_data, game_state)
        elif current_state == GameState.WALKING:
            return self.handle_walking_state(vision_data, game_state)
        elif current_state == GameState.EXPLORING:
            return self.handle_exploring_state(vision_data, game_state)
        elif current_state == GameState.IDLE:
            return self.handle_idle_state(vision_data, game_state)
        elif current_state == GameState.EMERGENCY:
            return self.handle_emergency_state(vision_data, game_state)
        else:
            return {'action': 'idle'}
    
    def handle_working_state(self, vision_data: Dict, game_state: Dict, 
                            activity_decision: Optional[Dict] = None) -> Dict:
        """Обработка состояния работы"""
        # Получаем мини-карту из vision_data или из game_state
        minimap = vision_data.get('minimap_image')
        if minimap is None:
            processed_frame = vision_data.get('processed_frame') or game_state.get('frame')
            if processed_frame is not None:
                minimap = self.vision.detect_minimap(processed_frame)
        
        # Проверка: есть ли уже работа
        if self.work_system.current_work != WorkType.NONE:
            # Уже работаем - обрабатываем текущую работу
            work_commands = self.work_system.process_work(vision_data, game_state)
            return work_commands
        
        # Ищем место работы на карте
        minimap_image = minimap if minimap is not None else game_state.get('frame')
        if minimap_image is not None:
            # Ищем все маркеры работы на карте
            all_work = self.world_navigation.find_all_work_markers(minimap_image)
            
            if all_work:
                # Нашли работу на карте - выбираем тип
                work_types_found = list(all_work.keys())
                preferred_work = self.work_system._select_work_by_preference()
                
                # Выбираем работу из найденных или предпочитаемую
                selected_work_type = None
                if preferred_work.value in work_types_found:
                    selected_work_type = preferred_work.value
                elif work_types_found:
                    selected_work_type = work_types_found[0]
                
                if selected_work_type:
                    # Находим позицию работы
                    work_positions = all_work[selected_work_type]
                    if work_positions:
                        work_pos = work_positions[0]  # Берем первую найденную
                        
                        # Проверяем, нужно ли ехать к месту работы
                        player_pos = self.world_navigation.get_player_position(minimap_image)
                        if player_pos:
                            nav_info = self.world_navigation.navigate_to_target(
                                minimap_image, work_pos
                            )
                            
                            if nav_info.get('action') == 'arrived':
                                # Достигли места работы - начинаем работу
                                work_type_enum = WorkType(selected_work_type)
                                self.work_system.start_work(work_type_enum)
                                # Запоминаем локацию
                                self.world_navigation.learn_location(
                                    f'work_{selected_work_type}', work_pos
                                )
                                return {'action': 'start_work_at_location'}
                            else:
                                # Нужно ехать к месту работы
                                return {
                                    'action': 'navigate_to_work',
                                    'target': work_pos,
                                    'work_type': selected_work_type,
                                    'navigation': nav_info
                                }
        
        # Если не нашли работу на карте - ищем в интерфейсе
        work_type = self.work_system.detect_work_opportunity(vision_data, game_state)
        if work_type:
            self.work_system.start_work(work_type)
            return {'action': 'work', 'work_type': work_type.value}
        
        # Если не нашли работу - ищем активнее
        return {'action': 'find_work', 'duration': 5}
        
        # Проверка на перерыв
        work_duration = time.time() - (self.work_system.work_start_time or time.time())
        if self.autonomous_life.should_take_break(work_duration):
            self.autonomous_life.schedule_break()
            self.work_system.stop_work()
            self.state_machine.transition_to(GameState.RESTING)
            return {'action': 'rest', 'duration': random.uniform(300, 600)}
        
        # Обработка текущей работы
        work_commands = self.work_system.process_work(vision_data, game_state)
        
        # Обновляем статистику работы и обучение
        if work_commands.get('sub_action') == 'deliver' and random.random() < 0.01:
            # Случайно завершаем задание (имитация)
            earnings = random.uniform(50, 200)
            self.work_system.complete_job(earnings)
            self.autonomous_life.daily_plan.update_earnings(earnings)
            self.autonomous_life.daily_plan.update_work_time(0.1)
            
            # Обновляем обучение - успешное завершение работы
            if self.last_state:
                learning_result = {
                    'success': True,
                    'earnings': earnings,
                    'job_completed': True,
                    'error': False
                }
                self.learning_system.learn_from_experience(
                    self.last_state,
                    {'action': 'work', 'work_type': self.work_system.current_work.value},
                    learning_result,
                    game_state
                )
        
        return work_commands
    
    def handle_driving_state(self, vision_data: Dict, game_state: Dict,
                            activity_decision: Optional[Dict] = None) -> Dict:
        """Обработка состояния вождения"""
        minimap_data = vision_data.get('minimap_data', {})
        
        # Получаем стиль вождения с человеческим фактором
        driving_style = self.human_behavior.adjust_driving_style()
        
        # Проверка наличия цели на карте
        targets = minimap_data.get('targets', [])
        if targets:
            # Едем к цели
            target = targets[0]
            return {
                'action': 'drive_to_target',
                'target': target,
                'style': driving_style
            }
        else:
            # Едем по дороге
            return {
                'action': 'follow_road',
                'style': driving_style
            }
    
    def handle_walking_state(self, vision_data: Dict, game_state: Dict,
                            activity_decision: Optional[Dict] = None) -> Dict:
        """Обработка состояния ходьбы"""
        # Проверка возможности взаимодействия
        if vision_data.get('near_object', False):
            return {'action': 'interact'}
        
        # Случайное движение
        if random.random() < 0.3:
            # Иногда осматриваемся
            look_around = self.human_behavior.random_look_around()
            return {'action': 'look_around', **look_around}
        
        # Обычное движение
        return {'action': 'walk_forward', 'duration': random.uniform(2, 5)}
    
    def handle_exploring_state(self, vision_data: Dict, game_state: Dict,
                              activity_decision: Optional[Dict] = None) -> Dict:
        """Обработка состояния исследования города"""
        minimap_data = vision_data.get('minimap_data', {})
        player_pos = minimap_data.get('player_position')
        
        if player_pos:
            # Находим ближайшую точку интереса
            landmark = self.navigation.find_nearest_landmark(player_pos)
            if landmark:
                return {
                    'action': 'move_to_landmark',
                    'landmark': landmark
                }
        
        # Случайное исследование
        return {
            'action': 'explore_random',
            'duration': random.uniform(30, 120)
        }
    
    def handle_idle_state(self, vision_data: Dict, game_state: Dict,
                         activity_decision: Optional[Dict] = None) -> Dict:
        """Обработка состояния бездействия"""
        # Используем решение автономной системы
        if activity_decision:
            activity = activity_decision.get('activity')
            
            if activity == 'work':
                self.state_machine.transition_to(GameState.WORKING)
                return {'action': 'find_work'}
            elif activity == 'rest':
                self.state_machine.transition_to(GameState.RESTING)
                return {'action': 'rest', 'duration': activity_decision.get('duration', 600)}
            elif activity == 'explore':
                self.state_machine.transition_to(GameState.EXPLORING)
                return {'action': 'explore_random', 'duration': activity_decision.get('duration', 600)}
            elif activity in ['walk_around', 'drive_around']:
                if activity == 'drive_around':
                    self.state_machine.transition_to(GameState.DRIVING)
                    return {'action': 'drive_random'}
                else:
                    self.state_machine.transition_to(GameState.WALKING)
                    return {'action': 'walk_forward', 'duration': activity_decision.get('duration', 300)}
        
        # Генерируем поведение бездействия
        idle_behavior = self.human_behavior.generate_idle_behavior()
        
        # Проверка возможности работы
        if vision_data.get('has_work_marker', False):
            self.state_machine.transition_to(GameState.WORKING)
            return {'action': 'start_work'}
        
        return idle_behavior
    
    def handle_emergency_state(self, vision_data: Dict, game_state: Dict,
                               activity_decision: Optional[Dict] = None) -> Dict:
        """Обработка экстренной ситуации"""
        # Низкое здоровье - ищем помощь
        if game_state.get('health', 100) < 20:
            return {'action': 'find_help', 'priority': 'high'}
        
        # Полиция - убегаем
        if game_state.get('has_police', False):
            return {'action': 'escape', 'priority': 'high'}
        
        # Выходим из экстренного режима
        self.state_machine.transition_to(GameState.IDLE)
        return {'action': 'idle'}
    
    def execute_action(self, action_data: Dict):
        """
        Выполняет действие с учетом человеческого поведения
        
        Args:
            action_data: Данные действия
        """
        if not self.controller.is_active:
            print(f"⚠️ Контроллер не активен! Действие не выполнено: {action_data.get('action', 'unknown')}")
            return
        
        if not action_data:
            return
        
        action = action_data.get('action', 'idle')
        
        # Логируем действие (первые 20 действий для отладки)
        if self.stats['frames_processed'] <= 20:
            print(f"🎮 Выполняю действие: {action}")
        
        # Добавляем человеческую задержку
        delay = self.human_behavior.add_human_delay()
        time.sleep(delay)
        
        # Проверка на ошибку (для реалистичности)
        if self.human_behavior.should_make_mistake():
            # Случайная ошибка - пропускаем действие или делаем неправильно
            if random.random() < 0.3:
                return
        
        # Выполнение действий
        if action == 'drive_to_target':
            self._execute_drive_to_target(action_data)
        elif action == 'follow_road':
            self._execute_follow_road(action_data)
        elif action == 'walk_forward':
            duration = action_data.get('duration', 2.0)
            if self.stats['frames_processed'] <= 20:
                print(f"  🚶 Иду вперед {duration:.1f} сек")
            self.controller.hold_key('w')
            time.sleep(duration)
            self.controller.release_key('w')
        elif action == 'interact':
            self.controller.press_key('e', 0.2)
        elif action == 'look_around':
            self._execute_look_around(action_data)
        elif action == 'start_work':
            self.controller.press_key('e', 0.2)  # Взаимодействие с работой
        elif action == 'idle':
            idle_duration = action_data.get('duration', random.uniform(2, 5))
            time.sleep(idle_duration)
        elif action == 'work':
            self._execute_work_action(action_data)
        elif action == 'navigate_to_work':
            self._execute_navigate_to_work(action_data)
        elif action == 'start_work_at_location':
            # Начало работы на локации
            if self.stats['frames_processed'] <= 20:
                print(f"  💼 Начинаю работу на локации")
            self.controller.press_key('e', 0.3)  # Взаимодействие с работой
            time.sleep(1.0)  # Ждем реакции игры
        elif action == 'find_work':
            # Поиск работы - просто ходим и ищем
            if self.stats['frames_processed'] <= 20:
                print(f"  🔍 Ищу работу...")
            self.controller.hold_key('w')
            time.sleep(3.0)  # Идем вперед
            self.controller.release_key('w')
            # Периодически поворачиваем
            if random.random() < 0.3:
                if random.random() < 0.5:
                    self.controller.turn_left(0.5)
                else:
                    self.controller.turn_right(0.5)
            # Ищем маркеры работы
            if random.random() < 0.2:
                self.controller.press_key('e', 0.3)  # Взаимодействие
                time.sleep(0.5)
        elif action == 'drive_random':
            # Случайная езда
            self.controller.hold_key('w')
            if random.random() < 0.2:
                if random.random() < 0.5:
                    self.controller.turn_left(0.3)
                else:
                    self.controller.turn_right(0.3)
            time.sleep(3.0)
            self.controller.release_key('w')
        elif action == 'move_backward':
            self.controller.move_backward(action_data.get('duration', 2.0))
        elif action == 'jump_multiple':
            count = action_data.get('count', 3)
            for _ in range(count):
                self.controller.press_key('space', 0.2)
                time.sleep(0.3)
        elif action == 'turn_around':
            angle = action_data.get('angle', 180)
            if angle > 0:
                self.controller.turn_right(angle / 90.0)
            else:
                self.controller.turn_left(abs(angle) / 90.0)
        elif action == 'stop_vehicle':
            self.controller.press_key('s', 1.0)  # Торможение
        elif action == 'explore_random':
            # Случайное исследование
            duration = action_data.get('duration', 5.0)
            if self.stats['frames_processed'] <= 20:
                print(f"  🗺️ Исследую {duration:.1f} сек")
            self.controller.hold_key('w')
            time.sleep(min(5.0, duration))
            self.controller.release_key('w')
            # Случайный поворот
            if random.random() < 0.3:
                if random.random() < 0.5:
                    self.controller.turn_left(random.uniform(0.3, 0.8))
                else:
                    self.controller.turn_right(random.uniform(0.3, 0.8))
        elif action == 'move_to_landmark':
            # Движение к точке интереса
            landmark = action_data.get('landmark')
            if landmark:
                if self.stats['frames_processed'] <= 20:
                    print(f"  📍 Иду к {landmark[0]}")
                self.controller.hold_key('w')
                time.sleep(3.0)
                self.controller.release_key('w')
        else:
            # Общие действия - по умолчанию просто идем вперед
            if 'move' in action or action == 'unknown' or not action:
                if self.stats['frames_processed'] <= 20:
                    print(f"  ⚠️ Неизвестное действие '{action}', просто иду вперед")
                self.controller.hold_key('w')
                time.sleep(2.0)
                self.controller.release_key('w')
            else:
                # Если действие не распознано - все равно двигаемся
                self.controller.hold_key('w')
                time.sleep(1.0)
                self.controller.release_key('w')
        
        # Микропауза между действиями
        pause = self.human_behavior.add_micro_pauses()
        time.sleep(pause)
    
    def _execute_drive_to_target(self, action_data: Dict):
        """Выполняет движение к цели"""
        style = action_data.get('style', {})
        speed_mult = style.get('speed_multiplier', 1.0)
        
        # Движение вперед с учетом стиля
        self.controller.hold_key('w')
        time.sleep(2.0 * speed_mult)
        self.controller.release_key('w')
    
    def _execute_navigate_to_work(self, action_data: Dict):
        """Выполняет навигацию к месту работы"""
        nav_info = action_data.get('navigation', {})
        target = action_data.get('target')
        
        # Если нет информации о навигации - просто идем вперед
        if not nav_info or not target:
            if self.stats['frames_processed'] <= 20:
                print(f"  ⚠️ Нет данных навигации, просто иду вперед")
            self.controller.hold_key('w')
            time.sleep(2.0)
            self.controller.release_key('w')
            return
        
        # Получаем команды навигации
        turn = nav_info.get('turn', {})
        move_forward = nav_info.get('move_forward', False)
        distance = nav_info.get('distance', 0)
        
        # Если очень близко - достигли
        if distance < 5:
            self.controller.press_key('e', 0.3)  # Взаимодействие с работой
            time.sleep(0.5)
            return
        
        # Поворачиваем если нужно
        if turn.get('direction') == 'right':
            self.controller.turn_right(turn.get('amount', 0.5))
        elif turn.get('direction') == 'left':
            self.controller.turn_left(turn.get('amount', 0.5))
        
        # Движемся вперед
        if move_forward:
            self.controller.hold_key('w')
            time.sleep(2.0)  # Увеличил время движения
            self.controller.release_key('w')
        else:
            # Если нет команды движения - все равно идем
            self.controller.hold_key('w')
            time.sleep(2.0)
            self.controller.release_key('w')
    
    def _execute_follow_road(self, action_data: Dict):
        """Выполняет движение по дороге"""
        style = action_data.get('style', {})
        speed_mult = style.get('speed_multiplier', 1.0)
        
        # Простое следование по дороге
        self.controller.hold_key('w')
        # Периодические корректировки
        if random.random() < 0.1:
            if random.random() < 0.5:
                self.controller.turn_left(0.2)
            else:
                self.controller.turn_right(0.2)
        time.sleep(1.0 * speed_mult)
        self.controller.release_key('w')
    
    def _execute_look_around(self, action_data: Dict):
        """Выполняет осмотр вокруг"""
        angle = action_data.get('angle', 30)
        duration = action_data.get('duration', 1.0)
        
        # Поворот камеры
        if angle > 0:
            self.controller.move_mouse(int(angle * 2), 0, relative=True)
        else:
            self.controller.move_mouse(int(angle * 2), 0, relative=True)
        time.sleep(duration)
    
    def _execute_work_action(self, action_data: Dict):
        """Выполняет действие работы"""
        work_type = action_data.get('work_type')
        sub_action = action_data.get('sub_action')
        
        # Логируем поддействие
        if self.stats['frames_processed'] <= 20:
            print(f"  💼 Работа: {work_type}, поддействие: {sub_action}")
        
        if sub_action == 'find_pickup':
            # Ищем точку приема заказа
            self.controller.move_forward(2.0)
        elif sub_action == 'deliver':
            # Доставляем заказ
            target = action_data.get('target')
            self.controller.move_forward(3.0)
            self.controller.press_key('e', 0.3)  # Взаимодействие
            time.sleep(0.5)
        elif sub_action == 'find_passenger':
            # Ищем пассажира
            self.controller.move_forward(2.0)
        elif sub_action == 'pickup_passenger':
            # Подбираем пассажира
            self.controller.press_key('e', 0.3)
            time.sleep(0.5)
        elif sub_action == 'drive_to_destination':
            # Едем к месту назначения
            self.controller.hold_key('w')
            time.sleep(5.0)
            self.controller.release_key('w')
        else:
            # По умолчанию - просто движение вперед
            self.controller.move_forward(1.0)
    
    def run(self):
        """Главный цикл работы AI"""
        print("\nОжидание запуска...")
        
        # Горячие клавиши
        keyboard.add_hotkey('f9', self.toggle)
        keyboard.add_hotkey('f10', self.stop)
        keyboard.add_hotkey('f11', self.show_stats)
        
        try:
            while True:
                if self.running:
                    # Захват экрана
                    frame = self.screen_capture.capture()
                    
                    # Обработка кадра
                    result = self.process_frame(frame)
                    
                    # Выполнение действия
                    action_data = result.get('action')
                    if action_data:
                        # Проверяем что контроллер активен
                        if not self.controller.is_active:
                            print("⚠️ ВНИМАНИЕ: Контроллер не активен! Активирую...")
                            self.controller.set_active(True)
                        
                        # Получаем game_state из result для отслеживания
                        game_state = {
                            'health': result.get('state', {}).value if hasattr(result.get('state'), 'value') else 100,
                            'position': result.get('position')
                        }
                        
                        # Начинаем отслеживание действия для определения успеха
                        self.success_detector.start_action(action_data, game_state)
                        
                        # Выполняем действие
                        self.execute_action(action_data)
                    else:
                        # Если нет действия - просто ждем
                        if self.stats['frames_processed'] <= 5:
                            print("  ⏸ Нет действия для выполнения")
                    
                    # Контроль FPS
                    elapsed = time.time() - self.last_frame_time
                    sleep_time = max(0, (1.0 / self.fps) - elapsed)
                    time.sleep(sleep_time)
                    self.last_frame_time = time.time()
                else:
                    time.sleep(0.1)
        
        except KeyboardInterrupt:
            print("\nОстановка AI...")
        finally:
            self.cleanup()
    
    def toggle(self):
        """Переключает состояние работы AI"""
        self.running = not self.running
        self.controller.set_active(self.running)
        
        if self.running:
            print("\n" + "=" * 50)
            print("🤖 AI ЗАПУЩЕН - Автономный режим активен")
            print("=" * 50)
            print(f"Текущее состояние: {self.state_machine.current_state.value}")
            print("AI будет работать, ездить и исследовать город самостоятельно")
            print("=" * 50 + "\n")
        else:
            print("\n⏸ AI ОСТАНОВЛЕН\n")
    
    def show_stats(self):
        """Показывает статистику работы"""
        session_time = time.time() - self.stats['session_start']
        stats = self.human_behavior.get_statistics()
        daily_stats = self.autonomous_life.get_daily_statistics()
        
        print("\n" + "=" * 50)
        print("📊 СТАТИСТИКА AI - АВТОНОМНЫЙ РЕЖИМ")
        print("=" * 50)
        print(f"Время работы: {session_time / 60:.1f} минут")
        print(f"Обработано кадров: {self.stats['frames_processed']}")
        print(f"Текущее состояние: {self.state_machine.current_state.value}")
        print(f"Текущая работа: {self.work_system.current_work.value}")
        print(f"\n📅 СТАТИСТИКА ЗА ДЕНЬ:")
        print(f"  Отработано часов: {daily_stats['work_hours']:.2f} / {daily_stats['work_target']:.2f}")
        print(f"  Заработано: ${daily_stats['earnings']:.2f} / ${daily_stats['earnings_target']:.2f}")
        print(f"  Завершено заданий: {self.work_system.completed_jobs}")
        print(f"  Активностей: {daily_stats['activities_count']}")
        print(f"\n🧠 ПОВЕДЕНИЕ:")
        print(f"  Среднее время реакции: {stats['avg_reaction_time']:.3f}с")
        print(f"  Паттерн: {stats['current_pattern']}")
        print(f"  Ошибок восстановлено: {self.auto_recovery.error_count}")
        
        # Статистика обучения
        learning_stats = self.learning_system.get_learning_statistics()
        print(f"\n🎓 ОБУЧЕНИЕ:")
        print(f"  Всего опытов: {learning_stats['total_experiences']}")
        print(f"  Успешных действий: {learning_stats['successful_actions']}")
        print(f"  Процент успеха: {learning_stats['success_rate']:.1f}%")
        print(f"  Исследование новых действий: {learning_stats['exploration_rate']*100:.1f}%")
        print(f"  Размер памяти: {learning_stats['memory_size']} опытов")
        print("=" * 50 + "\n")
    
    def stop(self):
        """Останавливает AI"""
        self.running = False
        self.controller.set_active(False)
        self.show_stats()
        print("Выход из программы...")
        exit(0)
    
    def cleanup(self):
        """Очистка ресурсов"""
        self.controller.set_active(False)
        self.work_system.stop_work()
        
        # Сохраняем данные обучения перед выходом
        print("\n💾 Сохранение данных обучения...")
        self.learning_system.save_learning_data()
        
        cv2.destroyAllWindows()
        print("Очистка завершена")


if __name__ == "__main__":
    ai = GTA_RP_AI()
    ai.run()
