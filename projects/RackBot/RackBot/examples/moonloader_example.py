"""
Пример использования Moonloader интеграции с RackBot
"""
from src.moonloader_integration import MoonloaderIntegration
from src.account_manager import AccountManager
from src.proxy_manager import ProxyManager

# Инициализация
ml = MoonloaderIntegration()
account_manager = AccountManager()
proxy_manager = ProxyManager()

# Создаем аккаунт
account = account_manager.create_account(
    username="test_user_123",
    password="secure_pass_456",
    email="test@example.com"
)

# Получаем прокси для аккаунта
proxy = proxy_manager.get_random_proxy()
if proxy:
    account_manager.update_account(account['id'], proxy=proxy)

# Генерируем Moonloader скрипт для регистрации
register_script = ml.generate_register_script(
    username=account['username'],
    password=account['password'],
    email=account['email']
)

print(f"Скрипт регистрации создан: {register_script}")
print(f"Скопируйте его в папку moonloader/ вашей игры")

# Генерируем скрипт для авторизации
login_script = ml.generate_login_script(
    username=account['username'],
    password=account['password']
)

print(f"Скрипт авторизации создан: {login_script}")

# Генерируем скрипт для прокачки
farm_script = ml.generate_farm_script(
    actions=['move_forward', 'jump', 'crouch', 'turn_left', 'turn_right']
)

print(f"Скрипт прокачки создан: {farm_script}")

# Проверяем результат выполнения (после запуска скрипта в игре)
result = ml.check_script_result("register_result.json")
if result:
    print(f"Результат регистрации: {result}")
    if result.get('status') == 'success':
        account_manager.update_account(account['id'], status='registered')
        print("Аккаунт успешно зарегистрирован!")

