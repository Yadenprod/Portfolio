"""
Модуль логирования для RackBot
"""
import logging
import os
from datetime import datetime
from pathlib import Path
from colorama import Fore, Style, init

# Инициализация colorama для Windows
init(autoreset=True)


class ColoredFormatter(logging.Formatter):
    """Форматтер с цветным выводом для консоли"""
    
    COLORS = {
        'DEBUG': Fore.CYAN,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.RED + Style.BRIGHT
    }
    
    def format(self, record):
        log_color = self.COLORS.get(record.levelname, '')
        record.levelname = f"{log_color}{record.levelname}{Style.RESET_ALL}"
        return super().format(record)


class BotLogger:
    """Класс для настройки логирования бота"""
    
    def __init__(self, config: dict):
        self.config = config
        self.log_dir = Path(config.get('log_directory', 'logs'))
        self.log_dir.mkdir(exist_ok=True)
        
        self.logger = logging.getLogger('RackBot')
        self.logger.setLevel(getattr(logging, config.get('level', 'INFO')))
        
        # Очистка старых обработчиков
        self.logger.handlers.clear()
        
        # Формат логов
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        date_format = '%Y-%m-%d %H:%M:%S'
        
        # Консольный обработчик
        if config.get('console_enabled', True):
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            console_formatter = ColoredFormatter(log_format, date_format)
            console_handler.setFormatter(console_formatter)
            self.logger.addHandler(console_handler)
        
        # Файловый обработчик
        if config.get('file_enabled', True):
            log_file = self.log_dir / f"rackbot_{datetime.now().strftime('%Y%m%d')}.log"
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_formatter = logging.Formatter(log_format, date_format)
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)
    
    def get_logger(self):
        """Возвращает настроенный logger"""
        return self.logger

