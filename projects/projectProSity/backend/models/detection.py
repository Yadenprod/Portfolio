import cv2
import numpy as np
import mediapipe as mp
import asyncio
import logging
from typing import List, Dict, Tuple, Optional
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class TheftDetectionSystem:
    """Основная система детекции краж"""
    
    def __init__(self):
        self.is_monitoring = False
        self.mp_pose = mp.solutions.pose
        self.mp_hands = mp.solutions.hands
        self.mp_face_detection = mp.solutions.face_detection
        
        # Инициализация MediaPipe
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.hands = self.mp_hands.Hands(
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5,
            max_num_hands=2
        )
        self.face_detection = self.mp_face_detection.FaceDetection(
            min_detection_confidence=0.5
        )
        
        # Параметры детекции
        self.suspicious_behavior_threshold = 0.7
        self.package_opening_threshold = 0.8
        self.exit_movement_threshold = 0.6
        
        # Статистика
        self.detection_stats = {
            "suspicious_events": 0,
            "package_openings": 0,
            "exit_movements": 0,
            "total_alerts": 0
        }
        
    async def initialize(self):
        """Инициализация системы"""
        logger.info("🔧 Инициализация системы детекции краж...")
        # Здесь можно загрузить предобученные модели
        logger.info("✅ Система детекции инициализирована")
        
    async def start_monitoring(self):
        """Запуск мониторинга"""
        self.is_monitoring = True
        logger.info("🚀 Запуск мониторинга системы детекции")
        
    async def stop_monitoring(self):
        """Остановка мониторинга"""
        self.is_monitoring = False
        logger.info("⏹️ Остановка мониторинга системы детекции")
        
    def analyze_suspicious_behavior(self, frame: np.ndarray) -> Dict:
        """Анализ подозрительного поведения"""
        results = {
            "suspicious_score": 0.0,
            "behaviors": [],
            "confidence": 0.0
        }
        
        try:
            # Конвертация в RGB для MediaPipe
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Анализ позы
            pose_results = self.pose.process(rgb_frame)
            if pose_results.pose_landmarks:
                # Анализ наклонов головы (попытка скрыть лицо)
                head_tilt = self._analyze_head_tilt(pose_results.pose_landmarks)
                if head_tilt > 0.6:
                    results["behaviors"].append("Скрытие лица")
                    results["suspicious_score"] += 0.3
                
                # Анализ движений рук
                hand_movements = self._analyze_hand_movements(pose_results.pose_landmarks)
                if hand_movements > 0.7:
                    results["behaviors"].append("Подозрительные движения рук")
                    results["suspicious_score"] += 0.4
            
            # Анализ рук
            hands_results = self.hands.process(rgb_frame)
            if hands_results.multi_hand_landmarks:
                for hand_landmarks in hands_results.multi_hand_landmarks:
                    # Детекция скрытия рук
                    hand_hiding = self._detect_hand_hiding(hand_landmarks)
                    if hand_hiding > 0.5:
                        results["behaviors"].append("Скрытие рук")
                        results["suspicious_score"] += 0.3
            
            # Анализ лица
            face_results = self.face_detection.process(rgb_frame)
            if face_results.detections:
                for detection in face_results.detections:
                    # Детекция избегания камер
                    face_avoidance = self._detect_face_avoidance(detection)
                    if face_avoidance > 0.6:
                        results["behaviors"].append("Избегание камер")
                        results["suspicious_score"] += 0.2
            
            # Нормализация score
            results["suspicious_score"] = min(results["suspicious_score"], 1.0)
            results["confidence"] = results["suspicious_score"]
            
        except Exception as e:
            logger.error(f"Ошибка анализа поведения: {e}")
            
        return results
    
    def detect_package_opening(self, frame: np.ndarray) -> Dict:
        """Детекция вскрытия упаковок"""
        results = {
            "opening_detected": False,
            "confidence": 0.0,
            "package_type": "unknown"
        }
        
        try:
            # Конвертация в RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Анализ рук для детекции движений вскрытия
            hands_results = self.hands.process(rgb_frame)
            if hands_results.multi_hand_landmarks:
                for hand_landmarks in hands_results.multi_hand_landmarks:
                    # Анализ движений пальцев
                    finger_movements = self._analyze_finger_movements(hand_landmarks)
                    if finger_movements > 0.7:
                        results["opening_detected"] = True
                        results["confidence"] = finger_movements
                        results["package_type"] = "small_package"
                        
            # Дополнительный анализ с помощью YOLO (если доступен)
            # Здесь можно добавить детекцию объектов упаковок
            
        except Exception as e:
            logger.error(f"Ошибка детекции вскрытия упаковок: {e}")
            
        return results
    
    def analyze_exit_movement(self, frame: np.ndarray, exit_zones: List[Dict]) -> Dict:
        """Анализ движения к выходам"""
        results = {
            "moving_to_exit": False,
            "exit_zone": None,
            "confidence": 0.0,
            "estimated_time": 0
        }
        
        try:
            # Конвертация в RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Анализ позы для определения направления движения
            pose_results = self.pose.process(rgb_frame)
            if pose_results.pose_landmarks:
                # Определение направления движения
                movement_direction = self._analyze_movement_direction(pose_results.pose_landmarks)
                
                # Проверка движения к выходам
                for zone in exit_zones:
                    if self._is_moving_towards_zone(movement_direction, zone):
                        results["moving_to_exit"] = True
                        results["exit_zone"] = zone["id"]
                        results["confidence"] = 0.8
                        results["estimated_time"] = self._estimate_time_to_exit(zone)
                        break
                        
        except Exception as e:
            logger.error(f"Ошибка анализа движения к выходам: {e}")
            
        return results
    
    def _analyze_head_tilt(self, landmarks) -> float:
        """Анализ наклона головы"""
        try:
            # Получение ключевых точек головы
            nose = landmarks.landmark[self.mp_pose.PoseLandmark.NOSE]
            left_ear = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_EAR]
            right_ear = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_EAR]
            
            # Расчет угла наклона
            head_angle = abs(left_ear.y - right_ear.y)
            return min(head_angle * 2, 1.0)
        except:
            return 0.0
    
    def _analyze_hand_movements(self, landmarks) -> float:
        """Анализ движений рук"""
        try:
            # Получение точек рук
            left_wrist = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_WRIST]
            right_wrist = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_WRIST]
            left_shoulder = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_SHOULDER]
            right_shoulder = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_SHOULDER]
            
            # Анализ положения рук относительно плеч
            left_hand_raised = left_wrist.y < left_shoulder.y
            right_hand_raised = right_wrist.y < right_shoulder.y
            
            # Подозрительные движения
            suspicious_movements = 0
            if left_hand_raised and right_hand_raised:
                suspicious_movements = 0.8
            elif left_hand_raised or right_hand_raised:
                suspicious_movements = 0.5
                
            return suspicious_movements
        except:
            return 0.0
    
    def _detect_hand_hiding(self, hand_landmarks) -> float:
        """Детекция скрытия рук"""
        try:
            # Анализ положения пальцев
            finger_tips = [8, 12, 16, 20]  # Кончики пальцев
            finger_mcp = [5, 9, 13, 17]    # Основания пальцев
            
            hidden_fingers = 0
            for tip, mcp in zip(finger_tips, finger_mcp):
                if hand_landmarks.landmark[tip].y > hand_landmarks.landmark[mcp].y:
                    hidden_fingers += 1
                    
            return hidden_fingers / len(finger_tips)
        except:
            return 0.0
    
    def _detect_face_avoidance(self, detection) -> float:
        """Детекция избегания камер"""
        try:
            # Анализ направления взгляда
            bbox = detection.location_data.relative_bounding_box
            center_x = bbox.xmin + bbox.width / 2
            
            # Если лицо смещено к краям кадра
            if center_x < 0.3 or center_x > 0.7:
                return 0.8
            elif center_x < 0.4 or center_x > 0.6:
                return 0.5
            else:
                return 0.2
        except:
            return 0.0
    
    def _analyze_finger_movements(self, hand_landmarks) -> float:
        """Анализ движений пальцев"""
        try:
            # Анализ движений пальцев для детекции вскрытия
            finger_tips = [8, 12, 16, 20]
            finger_pip = [6, 10, 14, 18]
            
            active_fingers = 0
            for tip, pip in zip(finger_tips, finger_pip):
                if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y:
                    active_fingers += 1
                    
            return active_fingers / len(finger_tips)
        except:
            return 0.0
    
    def _analyze_movement_direction(self, landmarks) -> Dict:
        """Анализ направления движения"""
        try:
            # Получение ключевых точек
            nose = landmarks.landmark[self.mp_pose.PoseLandmark.NOSE]
            left_hip = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_HIP]
            right_hip = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_HIP]
            
            # Определение направления
            center_x = (left_hip.x + right_hip.x) / 2
            center_y = (left_hip.y + right_hip.y) / 2
            
            return {
                "x": center_x,
                "y": center_y,
                "direction": "forward" if center_y < 0.5 else "backward"
            }
        except:
            return {"x": 0.5, "y": 0.5, "direction": "unknown"}
    
    def _is_moving_towards_zone(self, movement_direction: Dict, zone: Dict) -> bool:
        """Проверка движения к зоне"""
        try:
            zone_center_x = zone.get("center_x", 0.5)
            zone_center_y = zone.get("center_y", 0.5)
            
            # Простая проверка близости к зоне
            distance_x = abs(movement_direction["x"] - zone_center_x)
            distance_y = abs(movement_direction["y"] - zone_center_y)
            
            return distance_x < 0.2 and distance_y < 0.2
        except:
            return False
    
    def _estimate_time_to_exit(self, zone: Dict) -> int:
        """Оценка времени до выхода"""
        try:
            # Простая оценка на основе расстояния
            base_time = 30  # секунд
            return int(base_time * zone.get("distance_factor", 1.0))
        except:
            return 30
    
    async def process_frame(self, frame: np.ndarray, exit_zones: List[Dict] = None) -> Dict:
        """Обработка одного кадра"""
        if not self.is_monitoring:
            return {"status": "monitoring_disabled"}
            
        if exit_zones is None:
            exit_zones = []
            
        results = {
            "timestamp": datetime.now().isoformat(),
            "suspicious_behavior": self.analyze_suspicious_behavior(frame),
            "package_opening": self.detect_package_opening(frame),
            "exit_movement": self.analyze_exit_movement(frame, exit_zones),
            "alert_level": "none"
        }
        
        # Определение уровня тревоги
        alert_score = 0
        if results["suspicious_behavior"]["suspicious_score"] > self.suspicious_behavior_threshold:
            alert_score += 1
        if results["package_opening"]["opening_detected"]:
            alert_score += 2
        if results["exit_movement"]["moving_to_exit"]:
            alert_score += 1
            
        if alert_score >= 3:
            results["alert_level"] = "high"
            self.detection_stats["total_alerts"] += 1
        elif alert_score >= 2:
            results["alert_level"] = "medium"
        elif alert_score >= 1:
            results["alert_level"] = "low"
            
        return results
    
    def get_statistics(self) -> Dict:
        """Получение статистики детекции"""
        return {
            "monitoring_active": self.is_monitoring,
            "detection_stats": self.detection_stats,
            "thresholds": {
                "suspicious_behavior": self.suspicious_behavior_threshold,
                "package_opening": self.package_opening_threshold,
                "exit_movement": self.exit_movement_threshold
            }
        }
