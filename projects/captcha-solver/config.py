"""
Конфигурация для параллельного чекера ГИБДД
"""

import os
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class CheckerConfig:
    """Конфигурация чекера"""
    
    # Настройки браузера
    headless: bool = True
    window_size: str = "1920,1080"
    user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    
    # Таймауты
    wait_timeout: int = 20
    ad_timeout: int = 90
    captcha_wait_time: int = 30
    
    # Настройки капчи
    max_captcha_attempts: int = 10
    captcha_retry_delay: int = 1
    
    # Параллельность
    max_processes: int = 4
    
    # Пути и файлы
    temp_dir: str = "temp"
    screenshots_dir: str = "screenshots"
    logs_dir: str = "logs"
    
    # Очистка
    auto_cleanup: bool = True
    cleanup_old_files: bool = True
    max_file_age_hours: int = 24
    
    # Кэширование
    enable_cache: bool = False
    cache_duration_hours: int = 1
    
    # Уведомления
    enable_notifications: bool = False
    webhook_url: str = ""
    
    def __post_init__(self):
        """Создание директорий после инициализации"""
        self.create_directories()
    
    def create_directories(self):
        """Создание необходимых директорий"""
        for dir_path in [self.temp_dir, self.screenshots_dir, self.logs_dir]:
            os.makedirs(dir_path, exist_ok=True)
    
    def get_chrome_options(self) -> List[str]:
        """Получение опций Chrome"""
        options = [
            "--no-sandbox",
            "--disable-dev-shm-usage", 
            "--disable-gpu",
            f"--window-size={self.window_size}",
            f"--user-agent={self.user_agent}",
            "--mute-audio",
            "--disable-audio-output",
            "--disable-sound",
            "--autoplay-policy=no-user-gesture-required"
        ]
        
        if self.headless:
            options.append("--headless")
            
        return options
    
    def get_chrome_prefs(self) -> Dict:
        """Получение настроек Chrome"""
        return {
            "profile.managed_default_content_settings.images": 1,
            "profile.managed_default_content_settings.media_stream": 2,
            "profile.default_content_settings.popups": 0,
            "profile.content_settings.exceptions.automatic_downloads.*.setting": 1,
            "profile.default_content_setting_values.media_stream_mic": 2,
            "profile.default_content_setting_values.media_stream_camera": 2,
            "profile.default_content_setting_values.geolocation": 2,
            "profile.default_content_setting_values.notifications": 2
        }

# Экземпляр конфигурации по умолчанию
DEFAULT_CONFIG = CheckerConfig()

# Конфигурация для быстрого тестирования
FAST_CONFIG = CheckerConfig(
    headless=True,
    max_captcha_attempts=3,
    ad_timeout=30,
    enable_cache=False  # Кэширование отключено
)

# Конфигурация для продакшена
PRODUCTION_CONFIG = CheckerConfig(
    headless=True,
    max_captcha_attempts=15,
    ad_timeout=120,
    auto_cleanup=True,
    cleanup_old_files=True,
    enable_cache=False,  # Кэширование отключено
    cache_duration_hours=6
) 