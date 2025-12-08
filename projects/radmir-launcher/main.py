"""
RADMIR Multi-Account Launcher через Sandboxie
Главный файл запуска

ВАЖНО: Запускать с правами администратора!
"""
import sys
import ctypes
import logging
from radmir_launcher import RadmirAutomation


def is_admin():
    """Проверка, запущен ли скрипт с правами администратора"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def main():
    """Главная функция"""
    
    # Проверка прав администратора
    if not is_admin():
        print("="*60)
        print("ОШИБКА: Требуются права администратора!")
        print("="*60)
        print("Для изменения системного времени необходимо запустить")
        print("скрипт от имени администратора.")
        print("")
        print("Нажмите Enter для выхода...")
        input()
        sys.exit(1)
    
    print("="*60)
    print("RADMIR Multi-Account Launcher")
    print("="*60)
    print("")
    
    try:
        # Создаём экземпляр автоматизации
        automation = RadmirAutomation("config.json")
        
        # Спрашиваем пользователя, какие аккаунты обработать
        total_accounts = len(automation.config["accounts"])
        print(f"Всего аккаунтов в конфигурации: {total_accounts}")
        print("")
        print("Выберите режим:")
        print("1 - Запустить все аккаунты")
        print("2 - Запустить определенный диапазон")
        print("3 - Запустить один аккаунт")
        print("")
        
        choice = input("Ваш выбор (1/2/3): ").strip()
        
        if choice == "1":
            # Все аккаунты
            automation.run()
            
        elif choice == "2":
            # Диапазон
            start = int(input(f"С какого аккаунта начать (0-{total_accounts-1}): "))
            end = int(input(f"На каком аккаунте закончить (1-{total_accounts}): "))
            automation.run(start_index=start, end_index=end)
            
        elif choice == "3":
            # Один аккаунт
            index = int(input(f"Номер аккаунта (0-{total_accounts-1}): "))
            automation.run(start_index=index, end_index=index+1)
            
        else:
            print("Неверный выбор!")
            sys.exit(1)
        
        print("")
        print("Работа завершена! Нажмите Enter для выхода...")
        input()
        
    except KeyboardInterrupt:
        print("\n\nПрервано пользователем!")
        logging.info("Работа прервана пользователем")
        
    except Exception as e:
        print(f"\n\nКритическая ошибка: {e}")
        logging.error(f"Критическая ошибка: {e}", exc_info=True)
        print("\nНажмите Enter для выхода...")
        input()
        sys.exit(1)


if __name__ == "__main__":
    main()

