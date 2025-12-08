"""
Тестовый скрипт для проверки чистой версии
"""
import sys
import ctypes
from radmir_launcher_clean import RadmirAutomation


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if __name__ == "__main__":
    if not is_admin():
        print("ОШИБКА: Нужны права администратора!")
        input()
        sys.exit(1)
    
    print("="*60)
    print("Тест чистой версии автоматизации")
    print("="*60)
    print()
    
    automation = RadmirAutomation()
    
    for i, acc in enumerate(automation.config["accounts"]):
        print(f"{i}: {acc['nickname']} - {acc['sandbox']} - {acc['server']}")
    
    print()
    index = int(input("Номер аккаунта: "))
    
    print()
    print("ВАЖНО: НЕ ТРОГАЙТЕ мышь/клавиатуру!")
    print()
    input("Enter для старта...")
    
    automation.run(start_index=index, end_index=index+1)
    
    print()
    print("Готово!")
    input("Enter...")

