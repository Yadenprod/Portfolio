"""
Модуль управления прокси
"""
import random
from typing import Dict, List, Optional
from pathlib import Path
import json
import requests
from datetime import datetime
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class ProxyManager:
    """Класс для управления прокси серверами"""
    
    def __init__(self, proxies_file: str = 'data/proxies.json'):
        """
        Инициализация менеджера прокси
        
        Args:
            proxies_file: Путь к файлу с прокси
        """
        self.proxies_file = Path(proxies_file)
        self.proxies_file.parent.mkdir(parents=True, exist_ok=True)
        self.proxies = self._load_proxies()
        self.used_proxies = set()
    
    def _load_proxies(self) -> List[Dict]:
        """Загружает прокси из файла"""
        if self.proxies_file.exists():
            try:
                with open(self.proxies_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Ошибка загрузки прокси: {e}")
                return []
        return []
    
    def _save_proxies(self):
        """Сохраняет прокси в файл"""
        try:
            with open(self.proxies_file, 'w', encoding='utf-8') as f:
                json.dump(self.proxies, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения прокси: {e}")
    
    def add_proxy(self, host: str, port: int, username: Optional[str] = None,
                  password: Optional[str] = None, proxy_type: str = 'http') -> Dict:
        """
        Добавляет прокси
        
        Args:
            host: Хост прокси
            port: Порт прокси
            username: Имя пользователя (опционально)
            password: Пароль (опционально)
            proxy_type: Тип прокси (http, socks4, socks5)
        
        Returns:
            Словарь с данными прокси
        """
        proxy = {
            'id': len(self.proxies) + 1,
            'host': host,
            'port': port,
            'username': username,
            'password': password,
            'type': proxy_type,
            'status': 'active',  # active, dead, testing
            'last_checked': None,
            'response_time': None
        }
        
        self.proxies.append(proxy)
        self._save_proxies()
        return proxy
    
    def get_proxy_dict(self, proxy: Dict) -> Dict[str, str]:
        """
        Преобразует прокси в формат для requests
        
        Args:
            proxy: Словарь с данными прокси
        
        Returns:
            Словарь в формате для requests
        """
        proxy_type = proxy.get('type', 'http').lower()
        host = proxy['host']
        port = proxy['port']
        username = proxy.get('username')
        password = proxy.get('password')
        
        if username and password:
            auth = f"{username}:{password}@"
        else:
            auth = ""
        
        if proxy_type == 'socks5':
            proxy_url = f"socks5://{auth}{host}:{port}"
        elif proxy_type == 'socks4':
            proxy_url = f"socks4://{auth}{host}:{port}"
        else:
            proxy_url = f"http://{auth}{host}:{port}"
        
        return {
            'http': proxy_url,
            'https': proxy_url
        }
    
    def get_random_proxy(self, exclude_used: bool = True) -> Optional[Dict]:
        """
        Получает случайный доступный прокси
        
        Args:
            exclude_used: Исключать ли уже использованные прокси
        
        Returns:
            Словарь с данными прокси или None
        """
        available = [p for p in self.proxies 
                    if p.get('status') == 'active' and 
                    (not exclude_used or p.get('id') not in self.used_proxies)]
        
        if not available:
            # Если все прокси использованы, сбрасываем список
            if exclude_used:
                self.used_proxies.clear()
                available = [p for p in self.proxies if p.get('status') == 'active']
        
        if available:
            proxy = random.choice(available)
            if exclude_used:
                self.used_proxies.add(proxy.get('id'))
            return proxy
        
        return None
    
    def test_proxy(self, proxy: Dict, timeout: int = 10) -> bool:
        """
        Тестирует работоспособность прокси
        
        Args:
            proxy: Словарь с данными прокси
            timeout: Таймаут в секундах
        
        Returns:
            True если прокси работает
        """
        try:
            proxies = self.get_proxy_dict(proxy)
            response = requests.get(
                'http://httpbin.org/ip',
                proxies=proxies,
                timeout=timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                proxy['last_checked'] = str(datetime.now())
                proxy['status'] = 'active'
                proxy['external_ip'] = data.get('origin')
                self._save_proxies()
                return True
        except Exception as e:
            print(f"Прокси {proxy.get('host')}:{proxy.get('port')} не работает: {e}")
            proxy['status'] = 'dead'
            self._save_proxies()
        
        return False
    
    def get_all_proxies(self) -> List[Dict]:
        """Возвращает все прокси"""
        return self.proxies
    
    def get_active_proxies(self) -> List[Dict]:
        """Возвращает только активные прокси"""
        return [p for p in self.proxies if p.get('status') == 'active']

