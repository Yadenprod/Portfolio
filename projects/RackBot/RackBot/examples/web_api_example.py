"""
Пример использования веб-API Radmir RP
"""
from src.web_api import RadmirWebAPI
from src.proxy_manager import ProxyManager

# Инициализация прокси менеджера
proxy_manager = ProxyManager()

# Получаем прокси
proxy = proxy_manager.get_random_proxy()

# Инициализация API (если есть веб-сайт)
# ВАЖНО: Замените base_url на реальный URL сайта Radmir RP
api = RadmirWebAPI(
    base_url="https://radmir-rp.com",  # Замените на реальный URL
    proxy=proxy
)

# Попытка регистрации
username = "test_user"
password = "test_password"
email = "test@example.com"

print("Попытка регистрации через веб-API...")
result = api.register(username, password, email)

if result['success']:
    print(f"✅ Регистрация успешна!")
    print(f"Данные: {result.get('data')}")
else:
    print(f"❌ Ошибка регистрации: {result.get('error')}")
    print(f"Статус код: {result.get('status_code')}")

# Попытка авторизации
print("\nПопытка авторизации через веб-API...")
login_result = api.login(username, password)

if login_result['success']:
    print(f"✅ Авторизация успешна!")
    print(f"Данные: {login_result.get('data')}")
else:
    print(f"❌ Ошибка авторизации: {login_result.get('error')}")

# Проверка существования аккаунта
print(f"\nПроверка существования аккаунта '{username}'...")
exists = api.check_account_exists(username)
print(f"Аккаунт существует: {exists}")

# Получение информации о сервере
print("\nПолучение информации о сервере...")
server_info = api.get_server_info()
if server_info:
    print(f"Информация о сервере: {server_info}")
else:
    print("Не удалось получить информацию о сервере")

