"""
Тестовый скрипт для проверки работы с одним аккаунтом
Удобен для отладки и настройки
"""
import sys
import ctypes
import logging
from radmir_launcher import RadmirAutomation


def is_admin():
    """Проверка прав администратора"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def main():
    """Главная функция"""
    
    if not is_admin():
        print("ОШИБКА: Требуются права администратора!")
        input("Нажмите Enter для выхода...")
        sys.exit(1)
    
    print("="*60)
    print("Тестовый запуск одного аккаунта")
    print("="*60)
    print()
    
    try:
        automation = RadmirAutomation("config.json")
        
        # Показываем список аккаунтов
        print("Доступные аккаунты:")
        for i, acc in enumerate(automation.config["accounts"]):
            print(f"{i}: {acc['nickname']} - {acc['sandbox']} - {acc['server']}")
        
        print()
        index = int(input("Введите номер аккаунта для теста: "))
        
        if index < 0 or index >= len(automation.config["accounts"]):
            print("Неверный номер!")
            sys.exit(1)
        
        print()
        print("="*60)
        print(f"Запуск тестового аккаунта #{index}")
        print("="*60)
        print()
        
        # Запускаем один аккаунт
        automation.run(start_index=index, end_index=index+1)
        
        print()
        print("Тест завершен!")
        input("Нажмите Enter для выхода...")
        
    except Exception as e:
        print(f"Ошибка: {e}")
        logging.error(f"Ошибка в тесте: {e}", exc_info=True)
        input("Нажмите Enter для выхода...")
        sys.exit(1)


if __name__ == "__main__":
    main()

