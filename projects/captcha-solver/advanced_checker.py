"""
Продвинутый параллельный чекер ГИБДД с кэшированием и аналитикой
"""

import multiprocessing
import json
import time
import hashlib
import pickle
import os
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from collections import defaultdict
import sqlite3
from contextlib import contextmanager

from parallel_checker import ParallelGibddChecker, CheckType, CheckResult
from config import CheckerConfig, DEFAULT_CONFIG

@dataclass
class CheckStatistics:
    """Статистика проверок"""
    total_checks: int = 0
    successful_checks: int = 0
    failed_checks: int = 0
    captcha_success_rate: float = 0.0
    average_check_time: float = 0.0
    cache_hits: int = 0
    cache_misses: int = 0
    last_updated: str = ""

class CacheManager:
    """Менеджер кэша для результатов"""
    
    def __init__(self, config: CheckerConfig):
        self.config = config
        self.cache_dir = "cache"
        os.makedirs(self.cache_dir, exist_ok=True)
        self.stats = {"hits": 0, "misses": 0}
    
    def _get_cache_key(self, vin: str) -> str:
        """Генерация ключа для кэша"""
        return hashlib.md5(vin.encode()).hexdigest()
    
    def _get_cache_path(self, cache_key: str) -> str:
        """Путь к файлу кэша"""
        return os.path.join(self.cache_dir, f"{cache_key}.pkl")
    
    def _is_cache_valid(self, cache_path: str) -> bool:
        """Проверка актуальности кэша"""
        if not os.path.exists(cache_path):
            return False
        
        file_time = datetime.fromtimestamp(os.path.getmtime(cache_path))
        expire_time = datetime.now() - timedelta(hours=self.config.cache_duration_hours)
        
        return file_time > expire_time
    
    def get(self, vin: str) -> Optional[Dict]:
        """Получение данных из кэша"""
        if not self.config.enable_cache:
            return None
            
        cache_key = self._get_cache_key(vin)
        cache_path = self._get_cache_path(cache_key)
        
        if self._is_cache_valid(cache_path):
            try:
                with open(cache_path, 'rb') as f:
                    data = pickle.load(f)
                    self.stats["hits"] += 1
                    return data
            except Exception:
                pass
                
        self.stats["misses"] += 1
        return None
    
    def set(self, vin: str, data: Dict):
        """Сохранение данных в кэш"""
        if not self.config.enable_cache:
            return
            
        cache_key = self._get_cache_key(vin)
        cache_path = self._get_cache_path(cache_key)
        
        try:
            with open(cache_path, 'wb') as f:
                pickle.dump(data, f)
        except Exception:
            pass
    
    def cleanup_old_cache(self):
        """Очистка старого кэша"""
        if not self.config.cleanup_old_files:
            return
            
        expire_time = datetime.now() - timedelta(hours=self.config.max_file_age_hours)
        
        for filename in os.listdir(self.cache_dir):
            file_path = os.path.join(self.cache_dir, filename)
            if os.path.isfile(file_path):
                file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                if file_time < expire_time:
                    try:
                        os.remove(file_path)
                    except Exception:
                        pass

class DatabaseManager:
    """Менеджер базы данных для статистики"""
    
    def __init__(self):
        self.db_path = "gibdd_stats.db"
        self.init_database()
    
    @contextmanager
    def get_connection(self):
        """Контекстный менеджер для подключения к БД"""
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()
    
    def init_database(self):
        """Инициализация базы данных"""
        with self.get_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS check_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    vin TEXT NOT NULL,
                    check_type TEXT NOT NULL,
                    success BOOLEAN NOT NULL,
                    error_message TEXT,
                    captcha_solved BOOLEAN,
                    check_duration REAL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS daily_stats (
                    date DATE PRIMARY KEY,
                    total_checks INTEGER DEFAULT 0,
                    successful_checks INTEGER DEFAULT 0,
                    failed_checks INTEGER DEFAULT 0,
                    avg_duration REAL DEFAULT 0.0
                )
            ''')
            conn.commit()
    
    def save_result(self, vin: str, result: CheckResult, duration: float):
        """Сохранение результата проверки"""
        with self.get_connection() as conn:
            conn.execute('''
                INSERT INTO check_results 
                (vin, check_type, success, error_message, captcha_solved, check_duration)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                vin, 
                result.check_type.value, 
                result.success, 
                result.error, 
                result.captcha_solved, 
                duration
            ))
            conn.commit()
    
    def get_statistics(self, days: int = 7) -> CheckStatistics:
        """Получение статистики за период"""
        with self.get_connection() as conn:
            cursor = conn.execute('''
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successful,
                    AVG(check_duration) as avg_duration,
                    AVG(CASE WHEN captcha_solved = 1 THEN 1.0 ELSE 0.0 END) as captcha_rate
                FROM check_results 
                WHERE timestamp > datetime('now', '-{} days')
            '''.format(days))
            
            row = cursor.fetchone()
            
            if row and row[0] > 0:
                total, successful, avg_duration, captcha_rate = row
                return CheckStatistics(
                    total_checks=total,
                    successful_checks=successful,
                    failed_checks=total - successful,
                    average_check_time=avg_duration or 0.0,
                    captcha_success_rate=captcha_rate or 0.0,
                    last_updated=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
            
            return CheckStatistics()

class AdvancedGibddChecker:
    """Продвинутый чекер с кэшированием и аналитикой"""
    
    def __init__(self, config: CheckerConfig = None):
        self.config = config or DEFAULT_CONFIG
        self.cache_manager = CacheManager(self.config)
        self.db_manager = DatabaseManager()
        
    def check_vin_cached(self, vin: str) -> Dict[str, Any]:
        """Проверка VIN с кэшированием"""
        # Проверяем кэш
        cached_result = self.cache_manager.get(vin)
        if cached_result:
            cached_result["from_cache"] = True
            return cached_result
        
        # Выполняем проверку
        start_time = time.time()
        result = self._check_vin_parallel_with_stats(vin)
        duration = time.time() - start_time
        
        # Сохраняем в кэш если успешно
        if result and "error" not in result:
            self.cache_manager.set(vin, result)
        
        result["from_cache"] = False
        result["check_duration"] = duration
        
        return result
    
    def _check_vin_parallel_with_stats(self, vin: str) -> Dict[str, Any]:
        """Параллельная проверка с сохранением статистики"""
        sections = [CheckType.REGISTRATION, CheckType.ACCIDENTS, CheckType.WANTED, CheckType.RESTRICTIONS]
        
        try:
            with multiprocessing.Pool(processes=self.config.max_processes) as pool:
                checkers = [ParallelGibddChecker() for _ in range(4)]
                args = [(checker, vin, section) for checker, section in zip(checkers, sections)]
                results = pool.map(self._check_section_wrapper_with_stats, args)
            
            # Сохраняем статистику
            for result in results:
                if isinstance(result, tuple):
                    check_result, duration = result
                    self.db_manager.save_result(vin, check_result, duration)
            
            # Формируем итоговый результат
            final_results = [r[0] if isinstance(r, tuple) else r for r in results]
            
            return {
                "vin": vin,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "results": [
                    {
                        "type": result.check_type.value,
                        "success": result.success,
                        "data": result.data,
                        "error": result.error,
                        "captcha_solved": result.captcha_solved,
                        "ad_waited": result.ad_waited
                    }
                    for result in final_results
                ],
                "cache_stats": self.cache_manager.stats
            }
            
        except Exception as e:
            return {
                "vin": vin,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "error": str(e),
                "results": []
            }
    
    def _check_section_wrapper_with_stats(self, args):
        """Обертка с измерением времени"""
        start_time = time.time()
        try:
            checker, vin, section = args
            result = checker.check_section(vin, section)
            duration = time.time() - start_time
            return (result, duration)
        except Exception as e:
            duration = time.time() - start_time
            error_result = CheckResult(section, False, error=str(e))
            return (error_result, duration)
    
    def get_statistics(self, days: int = 7) -> CheckStatistics:
        """Получение статистики"""
        stats = self.db_manager.get_statistics(days)
        stats.cache_hits = self.cache_manager.stats["hits"]
        stats.cache_misses = self.cache_manager.stats["misses"]
        return stats
    
    def cleanup(self):
        """Очистка временных файлов и кэша"""
        if self.config.auto_cleanup:
            self.cache_manager.cleanup_old_cache()
            self._cleanup_temp_files()
    
    def _cleanup_temp_files(self):
        """Очистка временных файлов"""
        temp_patterns = ["temp_captcha_*.png", "dtp_block_*.png"]
        
        for pattern in temp_patterns:
            for filename in os.listdir("."):
                if filename.startswith(pattern.replace("*", "").replace(".png", "")):
                    try:
                        file_time = datetime.fromtimestamp(os.path.getmtime(filename))
                        expire_time = datetime.now() - timedelta(hours=self.config.max_file_age_hours)
                        
                        if file_time < expire_time:
                            os.remove(filename)
                    except Exception:
                        pass

# Функции для совместимости
def check_vin_advanced(vin: str, config: CheckerConfig = None) -> Dict[str, Any]:
    """Улучшенная проверка VIN"""
    checker = AdvancedGibddChecker(config)
    result = checker.check_vin_cached(vin)
    checker.cleanup()
    return result

def get_checker_statistics(days: int = 7) -> CheckStatistics:
    """Получение статистики чекера"""
    checker = AdvancedGibddChecker()
    return checker.get_statistics(days) 