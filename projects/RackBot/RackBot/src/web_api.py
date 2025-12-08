"""
Модуль для работы с веб-API Radmir RP (если есть)
"""
import requests
from typing import Optional, Dict
from urllib.parse import urljoin


class RadmirWebAPI:
    """Класс для работы с веб-API Radmir RP"""
    
    def __init__(self, base_url: str = "https://radmir-rp.com", proxy: Optional[Dict] = None):
        """
        Инициализация
        
        Args:
            base_url: Базовый URL сайта Radmir RP
            proxy: Настройки прокси
        """
        self.base_url = base_url.rstrip('/')
        self.proxy = proxy
        self.session = requests.Session()
        
        if proxy:
            self.session.proxies = self._format_proxy(proxy)
        
        # Заголовки для имитации браузера
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Content-Type': 'application/json'
        })
    
    def _format_proxy(self, proxy: Dict) -> Dict[str, str]:
        """Форматирует прокси для requests"""
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
    
    def register(self, username: str, password: str, email: str, 
                captcha: Optional[str] = None) -> Dict:
        """
        Регистрирует аккаунт через веб-API
        
        Args:
            username: Имя пользователя
            password: Пароль
            email: Email
            captcha: Решение капчи (если требуется)
        
        Returns:
            Словарь с результатом регистрации
        """
        # Возможные эндпоинты для регистрации
        endpoints = [
            '/api/register',
            '/register',
            '/api/auth/register',
            '/api/user/register'
        ]
        
        data = {
            'username': username,
            'password': password,
            'email': email
        }
        
        if captcha:
            data['captcha'] = captcha
        
        for endpoint in endpoints:
            try:
                url = urljoin(self.base_url, endpoint)
                response = self.session.post(url, json=data, timeout=10)
                
                if response.status_code == 200:
                    result = response.json()
                    return {
                        'success': True,
                        'data': result,
                        'message': 'Регистрация успешна'
                    }
                elif response.status_code in [400, 401, 403]:
                    result = response.json() if response.content else {}
                    return {
                        'success': False,
                        'error': result.get('message', 'Ошибка регистрации'),
                        'status_code': response.status_code
                    }
            except requests.exceptions.RequestException as e:
                continue
        
        return {
            'success': False,
            'error': 'Не удалось найти рабочий эндпоинт для регистрации'
        }
    
    def login(self, username: str, password: str) -> Dict:
        """
        Авторизуется через веб-API
        
        Args:
            username: Имя пользователя
            password: Пароль
        
        Returns:
            Словарь с результатом авторизации
        """
        endpoints = [
            '/api/login',
            '/login',
            '/api/auth/login',
            '/api/user/login'
        ]
        
        data = {
            'username': username,
            'password': password
        }
        
        for endpoint in endpoints:
            try:
                url = urljoin(self.base_url, endpoint)
                response = self.session.post(url, json=data, timeout=10)
                
                if response.status_code == 200:
                    result = response.json()
                    # Сохраняем токен/сессию если есть
                    if 'token' in result:
                        self.session.headers['Authorization'] = f"Bearer {result['token']}"
                    elif 'session' in result:
                        self.session.cookies.update(result['session'])
                    
                    return {
                        'success': True,
                        'data': result,
                        'message': 'Авторизация успешна'
                    }
            except requests.exceptions.RequestException:
                continue
        
        return {
            'success': False,
            'error': 'Не удалось найти рабочий эндпоинт для авторизации'
        }
    
    def check_account_exists(self, username: str) -> bool:
        """
        Проверяет существование аккаунта
        
        Args:
            username: Имя пользователя
        
        Returns:
            True если аккаунт существует
        """
        endpoints = [
            f'/api/user/check/{username}',
            f'/api/check/{username}',
            f'/check/{username}'
        ]
        
        for endpoint in endpoints:
            try:
                url = urljoin(self.base_url, endpoint)
                response = self.session.get(url, timeout=10)
                
                if response.status_code == 200:
                    result = response.json()
                    return result.get('exists', False)
            except requests.exceptions.RequestException:
                continue
        
        return False
    
    def get_server_info(self) -> Optional[Dict]:
        """Получает информацию о сервере"""
        endpoints = [
            '/api/server/info',
            '/api/info',
            '/server/info'
        ]
        
        for endpoint in endpoints:
            try:
                url = urljoin(self.base_url, endpoint)
                response = self.session.get(url, timeout=10)
                
                if response.status_code == 200:
                    return response.json()
            except requests.exceptions.RequestException:
                continue
        
        return None

