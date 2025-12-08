"""
Готовые улучшения для boat_bot.py
Эти методы можно добавить в класс BoatBot для повышения стабильности
"""

import time
import math
import numpy as np
import cv2
import logging

logger = logging.getLogger(__name__)


class TargetStabilizer:
    """
    Стабилизатор обнаружения целей - предотвращает "мигание" целей
    """
    def __init__(self, history_size=5, confidence_threshold=0.6):
        self.history_size = history_size
        self.confidence_threshold = confidence_threshold
        self.target_history = []
    
    def stabilize(self, current_target):
        """
        Стабилизирует обнаружение цели через временное усреднение
        """
        if not current_target.get('found', False):
            # Если цель не найдена, проверяем историю
            if len(self.target_history) >= self.history_size:
                # Если в последних N кадрах цель была найдена в похожем месте - считаем что она есть
                recent_targets = [t for t in self.target_history[-self.history_size:] 
                                 if t.get('found', False)]
                
                if len(recent_targets) >= self.history_size * self.confidence_threshold:
                    # Усредняем позиции
                    centers = [t['center'] for t in recent_targets if 'center' in t]
                    if centers:
                        avg_center = (
                            int(sum(c[0] for c in centers) / len(centers)),
                            int(sum(c[1] for c in centers) / len(centers))
                        )
                        return {
                            'found': True,
                            'center': avg_center,
                            'type': recent_targets[0].get('type', 'square'),
                            'color': recent_targets[0].get('color', 'red'),
                            'confidence': len(recent_targets) / self.history_size,
                            'stabilized': True  # Флаг что это стабилизированная цель
                        }
            return current_target
        
        # Цель найдена - добавляем в историю
        self.target_history.append(current_target.copy())
        if len(self.target_history) > self.history_size * 2:
            self.target_history.pop(0)
        
        # Если цель найдена в текущем кадре, возвращаем её
        return current_target
    
    def reset(self):
        """Сбрасывает историю"""
        self.target_history = []


class StuckDetector:
    """
    Детектор застревания бота
    """
    def __init__(self, position_threshold=5, distance_threshold=20, history_size=10):
        self.position_threshold = position_threshold
        self.distance_threshold = distance_threshold
        self.history_size = history_size
        self.player_positions = []
        self.distances = []
        self.stuck_count = 0
    
    def add_frame(self, player_pos, distance_to_target):
        """
        Добавляет данные кадра для анализа
        """
        self.player_positions.append(player_pos)
        self.distances.append(distance_to_target)
        
        # Ограничиваем размер истории
        if len(self.player_positions) > self.history_size:
            self.player_positions.pop(0)
        if len(self.distances) > self.history_size:
            self.distances.pop(0)
    
    def is_stuck(self):
        """
        Проверяет, застрял ли бот
        """
        if len(self.player_positions) < 5 or len(self.distances) < 5:
            return False
        
        # Проверка 1: Игрок не двигается
        recent_positions = self.player_positions[-5:]
        position_variance = sum(
            (recent_positions[i][0] - recent_positions[i-1][0])**2 + 
            (recent_positions[i][1] - recent_positions[i-1][1])**2
            for i in range(1, len(recent_positions))
        )
        
        if position_variance < self.position_threshold:
            self.stuck_count += 1
            if self.stuck_count >= 3:  # Подтверждаем застревание после 3 кадров
                return True
        
        # Проверка 2: Расстояние до цели не уменьшается
        recent_distances = self.distances[-5:]
        if len(recent_distances) >= 3:
            # Проверяем, что расстояние не уменьшается
            distance_decreasing = any(
                recent_distances[i] < recent_distances[i-1] - 1 
                for i in range(1, len(recent_distances))
            )
            
            if not distance_decreasing and min(recent_distances) > self.distance_threshold:
                self.stuck_count += 1
                if self.stuck_count >= 5:
                    return True
        
        # Если не застряли - сбрасываем счетчик
        self.stuck_count = 0
        return False
    
    def reset(self):
        """Сбрасывает детектор"""
        self.player_positions = []
        self.distances = []
        self.stuck_count = 0


class TargetValidator:
    """
    Валидатор целей - проверяет что цель действительно правильная
    """
    def __init__(self, minimap_size=(300, 300)):
        self.minimap_size = minimap_size
        self.max_target_area = 500  # Максимальная площадь цели
        self.max_distance = 250  # Максимальное расстояние до цели
        self.min_distance = 15  # Минимальное расстояние (чтобы не путать с игроком)
    
    def validate(self, target, player_pos, minimap=None, hsv=None):
        """
        Валидирует цель через несколько проверок
        """
        if not target.get('found', False):
            return False, "Цель не найдена"
        
        # Проверка 1: Размер цели
        area = target.get('area', 0)
        if area > self.max_target_area:
            return False, f"Цель слишком большая (площадь: {area})"
        
        if area < 10:
            return False, f"Цель слишком маленькая (площадь: {area})"
        
        # Проверка 2: Расстояние до цели
        if 'center' not in target:
            return False, "Цель не имеет центра"
        
        center = target['center']
        dx = center[0] - player_pos[0]
        dy = center[1] - player_pos[1]
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > self.max_distance:
            return False, f"Цель слишком далеко ({distance:.1f}px)"
        
        if distance < self.min_distance:
            return False, f"Цель слишком близко к игроку ({distance:.1f}px)"
        
        # Проверка 3: Цель не должна быть на краю миникарты (может быть обрезана)
        margin = 20
        if (center[0] < margin or center[0] > self.minimap_size[0] - margin or
            center[1] < margin or center[1] > self.minimap_size[1] - margin):
            return False, f"Цель слишком близко к краю миникарты"
        
        return True, "OK"
    
    def check_surrounding(self, minimap, hsv, center, radius=15):
        """
        Проверяет окружение цели (для водных чекпоинтов)
        """
        if minimap is None or hsv is None:
            return True  # Пропускаем проверку если нет данных
        
        h, w = minimap.shape[:2]
        cx, cy = int(center[0]), int(center[1])
        
        # Проверяем область вокруг цели
        x1 = max(0, cx - radius)
        y1 = max(0, cy - radius)
        x2 = min(w, cx + radius)
        y2 = min(h, cy + radius)
        
        if x2 <= x1 or y2 <= y1:
            return True  # Пропускаем если область некорректна
        
        roi_hsv = hsv[y1:y2, x1:x2]
        
        # Проверяем на черный цвет (суша)
        black_lower = np.array([0, 0, 0])
        black_upper = np.array([180, 255, 50])
        black_mask = cv2.inRange(roi_hsv, black_lower, black_upper)
        black_ratio = np.sum(black_mask > 0) / (roi_hsv.shape[0] * roi_hsv.shape[1])
        
        # Если более 30% области - черное (суша), это не наша цель
        if black_ratio > 0.3:
            return False
        
        return True


class TrajectoryPredictor:
    """
    Предсказатель траектории цели
    """
    def __init__(self, history_size=5):
        self.history_size = history_size
        self.target_history = []
    
    def add_target(self, target):
        """
        Добавляет цель в историю
        """
        if target.get('found', False) and 'center' in target:
            self.target_history.append({
                'center': target['center'],
                'time': time.time()
            })
            
            if len(self.target_history) > self.history_size:
                self.target_history.pop(0)
    
    def predict_position(self, frames_ahead=2):
        """
        Предсказывает будущую позицию цели
        """
        if len(self.target_history) < 2:
            return None
        
        # Вычисляем скорость (пиксели на кадр)
        recent = self.target_history[-3:]
        if len(recent) < 2:
            return None
        
        velocities = []
        for i in range(1, len(recent)):
            dt = recent[i]['time'] - recent[i-1]['time']
            if dt > 0:
                dx = recent[i]['center'][0] - recent[i-1]['center'][0]
                dy = recent[i]['center'][1] - recent[i-1]['center'][1]
                # Нормализуем на время (скорость в пикселях в секунду)
                vx = dx / dt if dt > 0 else 0
                vy = dy / dt if dt > 0 else 0
                velocities.append((vx, vy))
        
        if not velocities:
            return None
        
        # Усредняем скорость
        avg_vx = sum(v[0] for v in velocities) / len(velocities)
        avg_vy = sum(v[1] for v in velocities) / len(velocities)
        
        # Предсказываем позицию
        last_center = recent[-1]['center']
        # Предполагаем ~60 FPS (0.016 сек на кадр)
        frame_time = 0.016
        predicted_x = int(last_center[0] + avg_vx * frame_time * frames_ahead)
        predicted_y = int(last_center[1] + avg_vy * frame_time * frames_ahead)
        
        return (predicted_x, predicted_y)
    
    def reset(self):
        """Сбрасывает историю"""
        self.target_history = []


class BotMetrics:
    """
    Сбор и анализ метрик работы бота
    """
    def __init__(self):
        self.metrics = {
            'targets_found': 0,
            'targets_lost': 0,
            'targets_validated': 0,
            'targets_rejected': 0,
            'stuck_events': 0,
            'recovery_actions': 0,
            'frame_times': [],
            'checkpoint_times': []
        }
        self.start_time = time.time()
    
    def log_target_found(self):
        self.metrics['targets_found'] += 1
    
    def log_target_lost(self):
        self.metrics['targets_lost'] += 1
    
    def log_target_validated(self, valid=True):
        if valid:
            self.metrics['targets_validated'] += 1
        else:
            self.metrics['targets_rejected'] += 1
    
    def log_stuck_event(self):
        self.metrics['stuck_events'] += 1
    
    def log_recovery_action(self):
        self.metrics['recovery_actions'] += 1
    
    def log_frame_time(self, frame_time):
        self.metrics['frame_times'].append(frame_time)
        if len(self.metrics['frame_times']) > 1000:
            self.metrics['frame_times'].pop(0)
    
    def log_checkpoint_time(self, checkpoint_time):
        self.metrics['checkpoint_times'].append(checkpoint_time)
        if len(self.metrics['checkpoint_times']) > 100:
            self.metrics['checkpoint_times'].pop(0)
    
    def get_statistics(self):
        """Возвращает статистику работы бота"""
        total_time = time.time() - self.start_time
        
        frame_times = self.metrics['frame_times']
        avg_frame_time = (sum(frame_times) / len(frame_times) 
                         if frame_times else 0)
        
        checkpoint_times = self.metrics['checkpoint_times']
        avg_checkpoint_time = (sum(checkpoint_times) / len(checkpoint_times)
                              if checkpoint_times else 0)
        
        total_targets = self.metrics['targets_found'] + self.metrics['targets_lost']
        detection_rate = (self.metrics['targets_found'] / total_targets 
                         if total_targets > 0 else 0)
        
        validation_rate = (self.metrics['targets_validated'] / 
                          (self.metrics['targets_validated'] + self.metrics['targets_rejected'])
                          if (self.metrics['targets_validated'] + self.metrics['targets_rejected']) > 0 else 0)
        
        return {
            'total_time_seconds': total_time,
            'targets_found': self.metrics['targets_found'],
            'targets_lost': self.metrics['targets_lost'],
            'targets_validated': self.metrics['targets_validated'],
            'targets_rejected': self.metrics['targets_rejected'],
            'detection_rate': detection_rate,
            'validation_rate': validation_rate,
            'average_frame_time_ms': avg_frame_time * 1000,
            'average_checkpoint_time_seconds': avg_checkpoint_time,
            'stuck_events': self.metrics['stuck_events'],
            'recovery_actions': self.metrics['recovery_actions'],
            'fps': 1.0 / avg_frame_time if avg_frame_time > 0 else 0
        }
    
    def print_statistics(self):
        """Выводит статистику в лог"""
        stats = self.get_statistics()
        logger.info("=" * 60)
        logger.info("СТАТИСТИКА РАБОТЫ БОТА:")
        logger.info(f"  Время работы: {stats['total_time_seconds']:.1f} сек")
        logger.info(f"  Целей найдено: {stats['targets_found']}")
        logger.info(f"  Целей потеряно: {stats['targets_lost']}")
        logger.info(f"  Процент обнаружения: {stats['detection_rate']*100:.1f}%")
        logger.info(f"  Целей валидировано: {stats['targets_validated']}")
        logger.info(f"  Целей отклонено: {stats['targets_rejected']}")
        logger.info(f"  Процент валидации: {stats['validation_rate']*100:.1f}%")
        logger.info(f"  Среднее время кадра: {stats['average_frame_time_ms']:.2f} мс")
        logger.info(f"  FPS: {stats['fps']:.1f}")
        logger.info(f"  Среднее время сбора чекпоинта: {stats['average_checkpoint_time_seconds']:.2f} сек")
        logger.info(f"  Событий застревания: {stats['stuck_events']}")
        logger.info(f"  Действий восстановления: {stats['recovery_actions']}")
        logger.info("=" * 60)
    
    def reset(self):
        """Сбрасывает метрики"""
        self.metrics = {
            'targets_found': 0,
            'targets_lost': 0,
            'targets_validated': 0,
            'targets_rejected': 0,
            'stuck_events': 0,
            'recovery_actions': 0,
            'frame_times': [],
            'checkpoint_times': []
        }
        self.start_time = time.time()


# Пример использования в классе BoatBot:
"""
# В __init__ добавить:
self.target_stabilizer = TargetStabilizer(history_size=5, confidence_threshold=0.6)
self.stuck_detector = StuckDetector()
self.target_validator = TargetValidator(minimap_size=(300, 300))
self.trajectory_predictor = TrajectoryPredictor()
self.metrics = BotMetrics()

# В методе run, после получения target:
# 1. Стабилизация
target = self.target_stabilizer.stabilize(target)

# 2. Валидация
if target['found']:
    player_pos = self.minimap_center
    if player.get('green_center'):
        player_pos = player['green_center']
    
    is_valid, reason = self.target_validator.validate(target, player_pos, minimap, hsv)
    if not is_valid:
        logger.debug(f"Цель отклонена: {reason}")
        self.metrics.log_target_validated(valid=False)
        target = {'found': False}
    else:
        self.metrics.log_target_validated(valid=True)
        
        # Проверка окружения для водных чекпоинтов
        if target.get('color') in ['red', 'yellow', 'pink']:
            if not self.target_validator.check_surrounding(minimap, hsv, target['center']):
                logger.debug("Цель отклонена: не на воде")
                target = {'found': False}

# 3. Предсказание траектории
if target['found']:
    self.trajectory_predictor.add_target(target)
    predicted_pos = self.trajectory_predictor.predict_position(frames_ahead=2)
    if predicted_pos:
        # Используем предсказанную позицию для более точного наведения
        target['center'] = predicted_pos

# 4. Обнаружение застревания
if target['found']:
    distance = math.sqrt((target['center'][0] - player_pos[0])**2 + 
                        (target['center'][1] - player_pos[1])**2)
    self.stuck_detector.add_frame(player_pos, distance)
    
    if self.stuck_detector.is_stuck():
        logger.warning("Обнаружено застревание! Применяю восстановление...")
        self.metrics.log_stuck_event()
        self.recover_from_stuck()
        self.metrics.log_recovery_action()
        self.stuck_detector.reset()

# 5. Логирование метрик
frame_time = time.time() - frame_start
self.metrics.log_frame_time(frame_time)
"""

