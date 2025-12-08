"""
Скрипт для тестирования восстановления времени
Восстанавливает актуальное время через синхронизацию с интернетом
"""
import subprocess
import time
import logging
from datetime import datetime

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('test_restore_time.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)


def check_admin():
    """Проверка прав администратора"""
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False


def restore_time():
    """Восстановить актуальное время через синхронизацию с интернетом"""
    print("="*60)
    print("ТЕСТ ВОССТАНОВЛЕНИЯ ВРЕМЕНИ")
    print("="*60)
    print()
    
    # Проверка прав администратора
    if not check_admin():
        print("ОШИБКА: Требуются права администратора!")
        print("Запустите этот скрипт от имени администратора.")
        input("\nНажмите Enter для выхода...")
        return False
    
    print("✓ Права администратора: ЕСТЬ")
    print()
    
    # Показываем текущее время ДО синхронизации
    current_time_before = datetime.now()
    print(f"Текущее время ДО синхронизации: {current_time_before}")
    print()
    
    try:
        logging.info("Синхронизация времени с интернетом...")
        
        # Шаг 1: Проверка и настройка службы времени
        print("Шаг 1: Проверка статуса службы времени Windows...")
        
        def check_service_status():
            """Проверить статус службы времени"""
            try:
                result = subprocess.run(
                    ['sc', 'query', 'w32time'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if 'RUNNING' in result.stdout:
                    return 'running'
                elif 'STOPPED' in result.stdout:
                    return 'stopped'
                else:
                    return 'unknown'
            except:
                return 'unknown'
        
        status = check_service_status()
        print(f"  Статус службы: {status}")
        
        # Устанавливаем службу на автоматический запуск
        print("Шаг 2: Настройка службы на автоматический запуск...")
        try:
            result = subprocess.run(
                ['sc', 'config', 'w32time', 'start=auto'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                print("  ✓ Служба настроена на автоматический запуск")
            else:
                print(f"  ℹ Результат: {result.stdout.strip()}")
        except Exception as e:
            print(f"  ⚠ Ошибка настройки: {e}")
        
        # Запускаем службу, если она не запущена
        print("Шаг 3: Запуск службы времени...")
        if status != 'running':
            try:
                result = subprocess.run(
                    ['sc', 'start', 'w32time'],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if result.returncode == 0:
                    print("  ✓ Служба запущена")
                    time.sleep(2)  # Даем время службе запуститься
                else:
                    print(f"  ⚠ Не удалось запустить службу: {result.stderr.strip()}")
                    print("  Пробуем через net start...")
                    subprocess.run(['net', 'start', 'w32time'], 
                                 capture_output=True, timeout=10)
                    time.sleep(2)
            except Exception as e:
                print(f"  ⚠ Ошибка запуска службы: {e}")
        else:
            print("  ✓ Служба уже запущена")
        
        # Проверяем статус еще раз
        status = check_service_status()
        if status != 'running':
            print()
            print("  ⚠ ВНИМАНИЕ: Служба времени не запущена!")
            print("  Попробуем продолжить, но синхронизация может не работать.")
        
        print()
        print("Шаг 4: Настройка синхронизации с time.windows.com...")
        
        # Настраиваем синхронизацию с time.windows.com
        try:
            result = subprocess.run([
                'w32tm', '/config', 
                '/manualpeerlist:time.windows.com',
                '/syncfromflags:manual',
                '/update'
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                print("  ✓ Настройка выполнена успешно")
            else:
                print(f"  ℹ Результат настройки: {result.stdout.strip()}")
                if result.stderr:
                    print(f"  Ошибки: {result.stderr.strip()}")
        except Exception as e:
            print(f"  ⚠ Ошибка настройки: {e}")
        
        print()
        print("Шаг 5: Перезапуск службы времени...")
        
        # Перезапускаем службу времени
        try:
            subprocess.run(['sc', 'stop', 'w32time'], 
                         capture_output=True, timeout=10)
            print("  ✓ Служба остановлена")
            time.sleep(2)
            subprocess.run(['sc', 'start', 'w32time'], 
                         capture_output=True, timeout=10)
            print("  ✓ Служба запущена")
            time.sleep(3)  # Увеличено время ожидания
            
            # Проверяем, что служба действительно запущена
            status = check_service_status()
            if status == 'running':
                print("  ✓ Служба успешно запущена и работает")
            else:
                print(f"  ⚠ Служба в статусе: {status}")
        except Exception as e:
            print(f"  ⚠ Ошибка перезапуска службы: {e}")
        
        print()
        print("Шаг 6: Принудительная синхронизация с интернетом...")
        print("  (это может занять несколько секунд)...")
        
        # Принудительная синхронизация с интернетом
        result = subprocess.run(
            ['w32tm', '/resync', '/force'],
            capture_output=True,
            text=True,
            timeout=15
        )
        
        print(f"  Код возврата: {result.returncode}")
        if result.stdout:
            print(f"  Вывод: {result.stdout.strip()}")
        if result.stderr:
            print(f"  Ошибки: {result.stderr.strip()}")
        
        if result.returncode == 0 or "successfully" in result.stdout.lower():
            # Получаем текущее время после синхронизации
            time.sleep(1)  # Небольшая задержка для применения изменений
            current_time_after = datetime.now()
            print()
            print("="*60)
            print("РЕЗУЛЬТАТ:")
            print("="*60)
            print(f"Время ДО синхронизации: {current_time_before}")
            print(f"Время ПОСЛЕ синхронизации: {current_time_after}")
            print()
            
            time_diff = (current_time_after - current_time_before).total_seconds()
            print(f"Разница: {time_diff:.1f} секунд")
            print()
            print("✓ Время успешно синхронизировано!")
            logging.info(f"✓ Время синхронизировано и восстановлено: {current_time_after}")
            return True
        else:
            # Если синхронизация не удалась, пробуем еще раз через другой сервер
            print()
            print("⚠ Синхронизация через time.windows.com не удалась")
            print("Пробуем альтернативный сервер pool.ntp.org...")
            print()
            
            try:
                print("Шаг 7: Настройка синхронизации с pool.ntp.org...")
                subprocess.run([
                    'w32tm', '/config', 
                    '/manualpeerlist:pool.ntp.org',
                    '/syncfromflags:manual',
                    '/update'
                ], capture_output=True, text=True, timeout=10)
                print("  ✓ Настройка выполнена")
                
                time.sleep(1)
                print("Шаг 8: Перезапуск службы...")
                subprocess.run(['sc', 'stop', 'w32time'], capture_output=True, timeout=10)
                time.sleep(2)
                subprocess.run(['sc', 'start', 'w32time'], capture_output=True, timeout=10)
                time.sleep(3)
                print("  ✓ Служба перезапущена")
                
                # Проверяем статус
                status = check_service_status()
                if status == 'running':
                    print("  ✓ Служба работает")
                else:
                    print(f"  ⚠ Служба в статусе: {status}")
                
                print()
                print("Шаг 9: Синхронизация с pool.ntp.org...")
                result2 = subprocess.run(
                    ['w32tm', '/resync', '/force'],
                    capture_output=True,
                    text=True,
                    timeout=15
                )
                
                print(f"  Код возврата: {result2.returncode}")
                if result2.stdout:
                    print(f"  Вывод: {result2.stdout.strip()}")
                
                if result2.returncode == 0 or "successfully" in result2.stdout.lower():
                    time.sleep(1)
                    current_time_after = datetime.now()
                    print()
                    print("="*60)
                    print("РЕЗУЛЬТАТ:")
                    print("="*60)
                    print(f"Время ДО синхронизации: {current_time_before}")
                    print(f"Время ПОСЛЕ синхронизации: {current_time_after}")
                    print()
                    print("✓ Время успешно синхронизировано через pool.ntp.org!")
                    logging.info(f"✓ Время синхронизировано через pool.ntp.org: {current_time_after}")
                    return True
                else:
                    print()
                    print("✗ Синхронизация не удалась через оба сервера")
                    current_time_after = datetime.now()
                    print(f"Текущее системное время: {current_time_after}")
                    print()
                    print("Возможные причины:")
                    print("  - Нет подключения к интернету")
                    print("  - Служба времени Windows отключена или заблокирована")
                    print("  - Брандмауэр блокирует NTP запросы")
                    print("  - Групповые политики блокируют изменение времени")
                    print()
                    print("РЕШЕНИЕ:")
                    print("1. Откройте services.msc (Win+R → services.msc)")
                    print("2. Найдите службу 'Служба времени Windows' (Windows Time)")
                    print("3. Щелкните правой кнопкой → Свойства")
                    print("4. Установите 'Тип запуска' на 'Автоматически'")
                    print("5. Нажмите 'Запустить'")
                    print("6. Затем попробуйте синхронизировать время через:")
                    print("   Настройки Windows → Время и язык → Дата и время")
                    print("   Или выполните: w32tm /resync")
                    print()
                    logging.warning(f"Не удалось синхронизировать время. Текущее время: {current_time_after}")
                    return False
                    
            except Exception as e:
                print(f"✗ Ошибка при попытке синхронизации через pool.ntp.org: {e}")
                logging.error(f"Ошибка восстановления времени: {e}")
                return False
                
    except Exception as e:
        print(f"✗ Ошибка: {e}")
        logging.error(f"Ошибка восстановления времени: {e}")
        return False


if __name__ == "__main__":
    print()
    print("ВАЖНО: Этот скрипт требует прав администратора!")
    print("Запустите его от имени администратора.")
    print()
    input("Нажмите Enter для продолжения...")
    print()
    
    success = restore_time()
    
    print()
    print("="*60)
    if success:
        print("ТЕСТ ЗАВЕРШЕН УСПЕШНО")
    else:
        print("ТЕСТ ЗАВЕРШЕН С ОШИБКАМИ")
    print("="*60)
    print()
    input("Нажмите Enter для выхода...")

