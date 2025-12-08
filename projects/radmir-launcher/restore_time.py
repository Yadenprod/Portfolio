"""
Скрипт для восстановления системного времени
Синхронизирует время с интернетом

ВАЖНО: Запускать с правами администратора!
"""
import subprocess
import ctypes
import sys


def is_admin():
    """Проверка прав администратора"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def restore_time():
    """Восстановить системное время через синхронизацию с интернетом"""
    if not is_admin():
        print("ОШИБКА: Требуются права администратора!")
        print("Запустите этот скрипт от имени администратора.")
        input("\nНажмите Enter для выхода...")
        sys.exit(1)
    
    print("="*60)
    print("Восстановление системного времени")
    print("="*60)
    print()
    
    try:
        # Включаем службу времени Windows
        print("Запуск службы времени Windows...")
        subprocess.run(['net', 'start', 'w32time'], capture_output=True)
        
        # Настраиваем синхронизацию с time.windows.com
        print("Настройка сервера времени...")
        subprocess.run([
            'w32tm', '/config', 
            '/manualpeerlist:time.windows.com',
            '/syncfromflags:manual',
            '/update'
        ], capture_output=True)
        
        # Перезапускаем службу времени
        print("Перезапуск службы времени...")
        subprocess.run(['net', 'stop', 'w32time'], capture_output=True)
        subprocess.run(['net', 'start', 'w32time'], capture_output=True)
        
        # Принудительная синхронизация
        print("Синхронизация времени с интернетом...")
        result = subprocess.run(['w32tm', '/resync'], capture_output=True, text=True)
        
        if "successfully" in result.stdout.lower() or "успешно" in result.stdout.lower():
            print("\n✓ Время успешно синхронизировано!")
        else:
            print("\n⚠ Возможно, синхронизация не удалась.")
            print(f"Вывод команды: {result.stdout}")
            print(f"Ошибки: {result.stderr}")
        
        print("\nАльтернативный способ:")
        print("1. Откройте: Параметры → Время и язык → Дата и время")
        print("2. Нажмите 'Синхронизировать сейчас'")
        print("3. Или включите 'Установить время автоматически'")
        
    except Exception as e:
        print(f"\nОшибка: {e}")
        print("\nВосстановите время вручную:")
        print("1. Откройте: Панель управления → Дата и время")
        print("2. Вкладка 'Время по интернету' → Изменить параметры")
        print("3. Включите синхронизацию и нажмите 'Обновить сейчас'")
    
    print("\n" + "="*60)
    input("\nНажмите Enter для выхода...")


if __name__ == "__main__":
    restore_time()

