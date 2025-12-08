"""
Скрипт для удержания клавиш W и S
W - 5 секунд, пауза 20 секунд, S - 5 секунд, пауза 20 секунд
"""
import time
import keyboard
import sys
from colorama import init, Fore, Style

# Инициализация colorama для Windows
init(autoreset=True)

def hold_key(key: str, duration: float):
    """
    Удерживает клавишу в течение указанного времени
    
    Args:
        key: Клавиша для удержания
        duration: Длительность удержания в секундах
    """
    keyboard.press(key)
    time.sleep(duration)
    keyboard.release(key)

def wait_with_esc_check(duration: float, message: str = ""):
    """
    Ждет указанное время с проверкой ESC
    
    Args:
        duration: Длительность ожидания в секундах
        message: Сообщение для отображения
    """
    for i in range(int(duration)):
        if keyboard.is_pressed('esc'):
            return True
        time.sleep(1)
        if i % 5 == 0 and i > 0 and message:
            print(Fore.CYAN + f"  {message} Осталось: {int(duration) - i} сек")
    return False

def main():
    """Основная функция"""
    print(Fore.CYAN + "=" * 60)
    print(Fore.GREEN + "Скрипт удержания клавиш W и S")
    print(Fore.CYAN + "=" * 60)
    print(Fore.YELLOW + "W: удержание 5 сек → пауза 20 сек")
    print(Fore.YELLOW + "S: удержание 5 сек → пауза 20 сек")
    print(Fore.YELLOW + "Для остановки нажмите ESC")
    print(Fore.CYAN + "=" * 60)
    print()
    
    key_hold_duration = 5.0   # Удержание клавиши 5 секунд
    pause_duration = 20.0     # Пауза 20 секунд
    
    try:
        iteration = 0
        while True:
            iteration += 1
            
            # Проверяем, не нажата ли ESC
            if keyboard.is_pressed('esc'):
                print(Fore.RED + "\nОстановка по нажатию ESC...")
                break
            
            # Удерживаем W 5 секунд
            print(Fore.GREEN + f"[{iteration}] Удержание W ({key_hold_duration} сек)...")
            hold_key('w', key_hold_duration)
            print(Fore.GREEN + "W отпущена")
            
            # Пауза 20 секунд
            print(Fore.CYAN + f"Пауза {pause_duration} секунд...")
            if wait_with_esc_check(pause_duration, "Пауза"):
                print(Fore.RED + "\nОстановка по нажатию ESC...")
                break
            
            # Проверяем ESC снова
            if keyboard.is_pressed('esc'):
                print(Fore.RED + "\nОстановка по нажатию ESC...")
                break
            
            # Удерживаем S 5 секунд
            print(Fore.GREEN + f"[{iteration}] Удержание S ({key_hold_duration} сек)...")
            hold_key('s', key_hold_duration)
            print(Fore.GREEN + "S отпущена")
            
            # Пауза 20 секунд
            print(Fore.CYAN + f"Пауза {pause_duration} секунд...")
            if wait_with_esc_check(pause_duration, "Пауза"):
                print(Fore.RED + "\nОстановка по нажатию ESC...")
                break
            
    except KeyboardInterrupt:
        print(Fore.RED + "\n\nОстановка по Ctrl+C...")
    except Exception as e:
        print(Fore.RED + f"\nОшибка: {e}")
    finally:
        # Убеждаемся, что клавиши отпущены
        keyboard.release('w')
        keyboard.release('s')
        print(Fore.YELLOW + "\nСкрипт завершен.")

if __name__ == "__main__":
    main()

