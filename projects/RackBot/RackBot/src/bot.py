"""
Главный модуль RackBot - Headless бот для Radmir RP
"""
import time
import sys
import asyncio
from pathlib import Path
from typing import List, Dict, Optional

# Добавляем корневую директорию в путь
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils import load_config, validate_config, format_time
from src.logger import BotLogger
from src.account_manager import AccountManager
from src.proxy_manager import ProxyManager
from src.mac_changer import MACChanger
from src.samp_client import SAMPClient, ConnectionState
from src.moonloader_integration import MoonloaderIntegration
from src.web_api import RadmirWebAPI


class RackBot:
    """Главный класс headless бота для Radmir RP"""
    
    def __init__(self, config_path: str = 'config/config.json'):
        """
        Инициализация бота
        
        Args:
            config_path: Путь к файлу конфигурации
        """
        # Загрузка конфигурации
        self.config = load_config(config_path)
        validate_config(self.config)
        
        # Инициализация логирования
        log_config = self.config.get('logging', {})
        logger_manager = BotLogger(log_config)
        self.logger = logger_manager.get_logger()
        
        # Инициализация менеджеров
        self.account_manager = AccountManager(
            self.config.get('accounts_file', 'data/accounts.json')
        )
        self.proxy_manager = ProxyManager(
            self.config.get('proxies_file', 'data/proxies.json')
        )
        self.mac_changer = MACChanger()
        
        # Интеграция с Moonloader
        self.moonloader = MoonloaderIntegration(
            self.config.get('moonloader_dir', 'moonloader')
        )
        
        # Веб-API (если есть)
        web_api_config = self.config.get('web_api', {})
        if web_api_config.get('enabled', False):
            self.web_api = RadmirWebAPI(
                base_url=web_api_config.get('base_url', 'https://radmir-rp.com'),
                proxy=None  # Прокси будет устанавливаться для каждого аккаунта
            )
        else:
            self.web_api = None
        
        # Настройки сервера
        self.server_config = self.config.get('server', {})
        self.server_ip = self.server_config.get('ip', '127.0.0.1')
        self.server_port = self.server_config.get('port', 7777)
        
        # Настройки бота
        self.bot_config = self.config.get('bot', {})
        self.farming_config = self.config.get('farming', {})
        
        # Состояние
        self.running = False
        self.active_clients: List[SAMPClient] = []
        self.start_time = None
        
        self.logger.info(f"Инициализирован {self.bot_config.get('name', 'RackBot')} v{self.bot_config.get('version', '1.0')}")
    
    def start(self):
        """Запускает бота"""
        if not self.bot_config.get('enabled', True):
            self.logger.warning("Бот отключен в конфигурации")
            return
        
        self.running = True
        self.start_time = time.time()
        
        self.logger.info("=" * 50)
        self.logger.info("Запуск RackBot (Headless)")
        self.logger.info("=" * 50)
        self.logger.info("⚠️  ВАЖНО: Убедитесь, что использование бота разрешено правилами сервера!")
        self.logger.info("Для остановки нажмите Ctrl+C")
        self.logger.info("=" * 50)
        
        try:
            self._main_loop()
        except KeyboardInterrupt:
            self.logger.info("Получен сигнал остановки (Ctrl+C)")
        except Exception as e:
            self.logger.error(f"Критическая ошибка: {e}", exc_info=True)
        finally:
            self.stop()
    
    def stop(self):
        """Останавливает бота"""
        self.running = False
        
        # Отключаем все клиенты
        for client in self.active_clients:
            client.disconnect()
        
        if self.start_time:
            runtime = time.time() - self.start_time
            self.logger.info("=" * 50)
            self.logger.info(f"Бот остановлен")
            self.logger.info(f"Время работы: {format_time(runtime)}")
            self.logger.info(f"Активных аккаунтов: {len(self.active_clients)}")
            self.logger.info("=" * 50)
    
    def _main_loop(self):
        """Главный цикл работы бота"""
        max_accounts = self.bot_config.get('max_accounts', 10)
        check_interval = self.bot_config.get('check_interval_seconds', 60)
        
        while self.running:
            try:
                # Получаем аккаунты для работы
                accounts_to_process = self.account_manager.get_accounts_by_status('created')
                accounts_to_farm = self.account_manager.get_accounts_by_status('registered')
                
                # Регистрируем новые аккаунты
                if len(self.active_clients) < max_accounts:
                    for account in accounts_to_process[:max_accounts - len(self.active_clients)]:
                        self._register_account(account)
                
                # Прокачиваем зарегистрированные аккаунты
                for account in accounts_to_farm:
                    self._farm_account(account)
                
                # Проверяем состояние активных клиентов
                self._check_clients()
                
                # Ожидание перед следующей проверкой
                time.sleep(check_interval)
                
            except Exception as e:
                self.logger.error(f"Ошибка в главном цикле: {e}", exc_info=True)
                error_delay = self.config.get('delays', {}).get('error_retry_delay', 10.0)
                time.sleep(error_delay)
    
    def _register_account(self, account: Dict) -> bool:
        """Регистрирует аккаунт на сервере"""
        try:
            self.logger.info(f"Регистрация аккаунта: {account.get('username')}")
            
            # Получаем прокси для аккаунта
            proxy = None
            if not account.get('proxy'):
                proxy = self.proxy_manager.get_random_proxy()
                if proxy:
                    self.account_manager.update_account(
                        account['id'],
                        proxy=proxy
                    )
                    account['proxy'] = proxy
            else:
                proxy = account.get('proxy')
            
            # Подменяем MAC адрес если нужно
            if self.config.get('change_mac', True):
                interface = self.config.get('network_interface', 'Ethernet')
                new_mac = self.mac_changer.generate_random_mac()
                if self.mac_changer.change_mac(interface, new_mac):
                    self.account_manager.update_account(
                        account['id'],
                        mac_address=new_mac
                    )
                    self.logger.info(f"MAC адрес изменен: {new_mac}")
            
            # Создаем клиент
            client = SAMPClient(self.server_ip, self.server_port, proxy)
            
            # Подключаемся
            if not client.connect():
                self.logger.error(f"Не удалось подключиться для аккаунта {account.get('username')}")
                self.account_manager.update_account(account['id'], status='error')
                return False
            
            # Регистрируем
            if client.register_account(
                account['username'],
                account['password'],
                account['email']
            ):
                self.account_manager.update_account(account['id'], status='registered')
                self.active_clients.append(client)
                self.logger.info(f"Аккаунт {account.get('username')} успешно зарегистрирован")
                return True
            else:
                self.account_manager.update_account(account['id'], status='error')
                return False
                
        except Exception as e:
            self.logger.error(f"Ошибка регистрации аккаунта: {e}", exc_info=True)
            self.account_manager.update_account(account['id'], status='error')
            return False
    
    def _farm_account(self, account: Dict) -> bool:
        """Прокачивает аккаунт"""
        try:
            # Находим клиент для этого аккаунта или создаем новый
            client = None
            for c in self.active_clients:
                # Здесь нужно связать клиент с аккаунтом
                # Упрощенная версия
                pass
            
            if not client:
                # Создаем новый клиент
                proxy = account.get('proxy', {})
                client = SAMPClient(self.server_ip, self.server_port, proxy)
                
                if not client.connect():
                    return False
                
                if not client.login(account['username'], account['password']):
                    return False
                
                self.active_clients.append(client)
            
            # Качаем опыт
            if client.is_connected():
                client.farm_experience()
                self.account_manager.update_account(
                    account['id'],
                    status='active',
                    last_login=time.time()
                )
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Ошибка прокачки аккаунта: {e}", exc_info=True)
            return False
    
    def _check_clients(self):
        """Проверяет состояние активных клиентов"""
        disconnected = []
        for i, client in enumerate(self.active_clients):
            if not client.is_connected():
                disconnected.append(i)
                client.disconnect()
        
        # Удаляем отключенные клиенты
        for i in reversed(disconnected):
            self.active_clients.pop(i)
    
    def create_accounts_batch(self, count: int):
        """Создает несколько аккаунтов"""
        self.logger.info(f"Создание {count} аккаунтов...")
        
        for _ in range(count):
            proxy = self.proxy_manager.get_random_proxy()
            account = self.account_manager.create_account(proxy=proxy)
            self.logger.info(f"Создан аккаунт: {account['username']}")


def main():
    """Точка входа"""
    try:
        bot = RackBot()
        bot.start()
    except Exception as e:
        print(f"Ошибка запуска бота: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
