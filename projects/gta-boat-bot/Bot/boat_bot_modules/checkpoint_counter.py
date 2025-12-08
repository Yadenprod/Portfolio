"""
Система подсчета чекпоинтов с надстройкой "по тройкам"
КОСТЫЛЬ: Из-за бага один физический чекпоинт засчитывается 3 раза.
Внутренний счетчик считает каждый вызов add_checkpoint() как +1.
Внешний счетчик считает каждые 3 внутренних = 1 внешний (компенсирует баг).

Маршрут зависит от внешнего счетчика (сколько раз набралось по 3).
"""

import logging
from typing import Optional, Tuple

logger = logging.getLogger(__name__)


class CheckpointCounter:
    """
    Система подсчета чекпоинтов с двойным счетом (КОСТЫЛЬ для бага):
    - Внутренний счетчик: считает каждый ВЫЗОВ add_checkpoint() как +1
      (из-за бага один физический чекпоинт вызывает add_checkpoint() 3 раза)
    - Внешний счетчик: считает тройки (каждые 3 внутренних = 1 внешний)
       Внутренний: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21
       Внешний:    0, 0, 0, 1, 1, 1, 2, 2, 2, 3,  3,  3,  4,  4,  4,  5,  5,  5,  6,  6,  6,  7
    
    Маршрут зависит от внешнего счетчика (это компенсирует баг троекратного засчитывания).
    """
    
    def __init__(self):
        """
        Инициализация счетчика
        """
        # Внутренний счетчик (считает каждый вызов add_checkpoint() как +1)
        # Из-за бага один физический чекпоинт вызывает add_checkpoint() 3 раза
        self.internal_counter = 0
        
        # Внешний счетчик (сколько раз набралось по 3 - для маршрута)
        # Вычисляется как internal_counter // 3
        # Компенсирует баг: каждые 3 вызова (1 физический чекпоинт) = 1 внешний
        self.external_counter = 0
        
        # История для отладки
        self.history = []
    
    def add_checkpoint(self) -> Tuple[int, int]:
        """
        Добавляет чекпоинт в счетчик (КОСТЫЛЬ: из-за бага вызывается 3 раза за 1 физический чекпоинт)
        
        Returns:
            (internal_counter, external_counter) - текущие значения счетчиков
        """
        # Внутренний счетчик: просто +1 за каждый вызов
        # (из-за бага один физический чекпоинт вызывает эту функцию 3 раза)
        old_internal = self.internal_counter
        self.internal_counter += 1
        
        # Вычисляем новый внешний счетчик (сколько полных троек набралось)
        # Каждые 3 вызова (1 физический чекпоинт) = 1 внешний
        new_external = self.internal_counter // 3
        
        # Если внешний счетчик изменился - это событие (собран 1 физический чекпоинт)
        external_changed = new_external > self.external_counter
        old_external = self.external_counter
        self.external_counter = new_external
        
        remainder = self.internal_counter % 3
        
        if external_changed:
            logger.info(f"[CHECKPOINT COUNTER] ✓ Внешний счетчик: {old_external} → {self.external_counter} "
                       f"(внутренний: {old_internal} → {self.internal_counter}, остаток: {remainder}/3) "
                       f"→ Собран 1 физический чекпоинт!")
        else:
            logger.debug(f"[CHECKPOINT COUNTER] Внутренний счетчик: {old_internal} → {self.internal_counter}, "
                        f"внешний: {self.external_counter} (остаток: {remainder}/3, нужно еще {3 - remainder} вызовов)")
        
        # Сохраняем в историю
        self.history.append({
            'internal': self.internal_counter,
            'external': self.external_counter,
            'changed': external_changed
        })
        if len(self.history) > 20:
            self.history.pop(0)
        
        return self.internal_counter, self.external_counter
    
    def get_external(self) -> int:
        """
        Возвращает внешний счетчик (для маршрута)
        Это количество "полных троек" - сколько раз набралось по 3
        """
        return self.external_counter
    
    def get_internal(self) -> int:
        """
        Возвращает внутренний счетчик
        Это количество вызовов add_checkpoint() (из-за бага один чекпоинт = 3 вызова)
        """
        return self.internal_counter
    
    def reset(self):
        """Сбрасывает оба счетчика"""
        old_internal = self.internal_counter
        old_external = self.external_counter
        self.internal_counter = 0
        self.external_counter = 0
        logger.info(f"[CHECKPOINT COUNTER] Счетчики сброшены (было: внутренний={old_internal}, внешний={old_external})")
        self.history.clear()
    
    def get_status_string(self) -> str:
        """Возвращает строку статуса для отображения"""
        remainder = self.internal_counter % 3
        return f"Внутренний: {self.internal_counter} (остаток: {remainder}/3), Внешний: {self.external_counter}"
    
    def check_threshold_external(self, threshold: int) -> bool:
        """
        Проверяет, достигнут ли порог по внешнему счетчику
        
        Args:
            threshold: Порог для внешнего счетчика (например, 7 для 7 внешних чекпоинтов)
        
        Returns:
            True если внешний счетчик >= threshold
        """
        return self.external_counter >= threshold
    
    def check_threshold_internal(self, threshold: int) -> bool:
        """
        Проверяет, достигнут ли порог по внутреннему счетчику
        
        Args:
            threshold: Порог для внутреннего счетчика (например, 21 для 7 внешних = 21 внутренний)
        
        Returns:
            True если внутренний счетчик >= threshold
        """
        return self.internal_counter >= threshold

