"""
Упрощенная версия - удержание W и S
W - 5 секунд, пауза 20 секунд, S - 5 секунд, пауза 20 секунд
"""
import time
import keyboard

def main():
    print("Скрипт удержания W и S")
    print("W: 5 сек → пауза 20 сек → S: 5 сек → пауза 20 сек")
    print("Для остановки нажмите ESC")
    print("-" * 50)
    
    key_hold_duration = 5.0   # Удержание клавиши 5 секунд
    pause_duration = 20.0     # Пауза 20 секунд
    
    try:
        iteration = 0
        while True:
            iteration += 1
            
            # Проверка ESC
            if keyboard.is_pressed('esc'):
                print("\nОстановка...")
                break
            
            # Удерживаем W 5 секунд
            print(f"[{iteration}] Удержание W ({key_hold_duration} сек)...")
            keyboard.press('w')
            time.sleep(key_hold_duration)
            keyboard.release('w')
            print("W отпущена")
            
            # Пауза 20 секунд
            print(f"Пауза {pause_duration} секунд...")
            for i in range(int(pause_duration)):
                if keyboard.is_pressed('esc'):
                    print("\nОстановка...")
                    return
                time.sleep(1)
                if i % 5 == 0 and i > 0:
                    print(f"  Осталось: {int(pause_duration) - i} сек")
            
            # Проверка ESC
            if keyboard.is_pressed('esc'):
                print("\nОстановка...")
                break
            
            # Удерживаем S 5 секунд
            print(f"[{iteration}] Удержание S ({key_hold_duration} сек)...")
            keyboard.press('s')
            time.sleep(key_hold_duration)
            keyboard.release('s')
            print("S отпущена")
            
            # Пауза 20 секунд
            print(f"Пауза {pause_duration} секунд...")
            for i in range(int(pause_duration)):
                if keyboard.is_pressed('esc'):
                    print("\nОстановка...")
                    return
                time.sleep(1)
                if i % 5 == 0 and i > 0:
                    print(f"  Осталось: {int(pause_duration) - i} сек")
            
    except KeyboardInterrupt:
        print("\nОстановка...")
    finally:
        # Убеждаемся, что клавиши отпущены
        keyboard.release('w')
        keyboard.release('s')

if __name__ == "__main__":
    main()

