"""
Модуль управления аккаунтами
"""
import json
import random
import string
from pathlib import Path
from typing import Dict, List, Optional
from faker import Faker
from datetime import datetime


class AccountManager:
    """Класс для управления аккаунтами"""
    
    def __init__(self, accounts_file: str = 'data/accounts.json'):
        """
        Инициализация менеджера аккаунтов
        
        Args:
            accounts_file: Путь к файлу с аккаунтами
        """
        self.accounts_file = Path(accounts_file)
        self.accounts_file.parent.mkdir(parents=True, exist_ok=True)
        self.faker = Faker('ru_RU')
        self.accounts = self._load_accounts()
    
    def _load_accounts(self) -> List[Dict]:
        """Загружает аккаунты из файла"""
        if self.accounts_file.exists():
            try:
                with open(self.accounts_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Ошибка загрузки аккаунтов: {e}")
                return []
        return []
    
    def _save_accounts(self):
        """Сохраняет аккаунты в файл"""
        try:
            with open(self.accounts_file, 'w', encoding='utf-8') as f:
                json.dump(self.accounts, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения аккаунтов: {e}")
    
    def generate_username(self) -> str:
        """Генерирует случайное имя пользователя"""
        # Комбинация случайных слов и чисел
        words = [
            self.faker.first_name().lower(),
            self.faker.last_name().lower(),
            ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
        ]
        return '_'.join(random.sample(words, 2))
    
    def generate_password(self, length: int = 12) -> str:
        """Генерирует случайный пароль"""
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(random.choices(chars, k=length))
    
    def generate_email(self) -> str:
        """Генерирует случайный email"""
        return self.faker.email()
    
    def create_account(self, username: Optional[str] = None, 
                      password: Optional[str] = None,
                      email: Optional[str] = None,
                      proxy: Optional[Dict] = None,
                      mac_address: Optional[str] = None) -> Dict:
        """
        Создает новый аккаунт
        
        Args:
            username: Имя пользователя (если None - генерируется)
            password: Пароль (если None - генерируется)
            email: Email (если None - генерируется)
            proxy: Настройки прокси
            mac_address: MAC адрес
        
        Returns:
            Словарь с данными аккаунта
        """
        account = {
            'id': len(self.accounts) + 1,
            'username': username or self.generate_username(),
            'password': password or self.generate_password(),
            'email': email or self.generate_email(),
            'proxy': proxy or {},
            'mac_address': mac_address or '',
            'created_at': datetime.now().isoformat(),
            'last_login': None,
            'level': 1,
            'experience': 0,
            'status': 'created',  # created, registered, active, banned, error
            'server': 'radmir',
            'notes': ''
        }
        
        self.accounts.append(account)
        self._save_accounts()
        return account
    
    def get_account(self, account_id: int) -> Optional[Dict]:
        """Получает аккаунт по ID"""
        for account in self.accounts:
            if account.get('id') == account_id:
                return account
        return None
    
    def get_accounts_by_status(self, status: str) -> List[Dict]:
        """Получает аккаунты по статусу"""
        return [acc for acc in self.accounts if acc.get('status') == status]
    
    def update_account(self, account_id: int, **kwargs) -> bool:
        """Обновляет данные аккаунта"""
        for account in self.accounts:
            if account.get('id') == account_id:
                account.update(kwargs)
                account['updated_at'] = datetime.now().isoformat()
                self._save_accounts()
                return True
        return False
    
    def get_all_accounts(self) -> List[Dict]:
        """Возвращает все аккаунты"""
        return self.accounts
    
    def delete_account(self, account_id: int) -> bool:
        """Удаляет аккаунт"""
        self.accounts = [acc for acc in self.accounts if acc.get('id') != account_id]
        self._save_accounts()
        return True

