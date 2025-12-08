"""
Проверка окружения перед запуском
Проверяет все зависимости и настройки
"""
import os
import sys
import json
import subprocess
import ctypes


def check_admin():
    """Проверка прав администратора"""
    try:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        if is_admin:
            print("✓ Права администратора: ЕСТЬ")
            return True
        else:
            print("✗ Права администратора: НЕТ (требуется для изменения времени)")
            return False
    except:
        print("? Права администратора: НЕИЗВЕСТНО")
        return False


def check_python_version():
    """Проверка версии Python"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✓ Python версия: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"✗ Python версия: {version.major}.{version.minor}.{version.micro} (требуется 3.8+)")
        return False


def check_dependencies():
    """Проверка установленных зависимостей"""
    deps = {
        'pywinauto': 'pywinauto',
        'win32api': 'pywin32',
        'dateutil': 'python-dateutil'
    }
    
    all_ok = True
    for module, package in deps.items():
        try:
            __import__(module)
            print(f"✓ Зависимость '{package}': установлена")
        except ImportError:
            print(f"✗ Зависимость '{package}': НЕ УСТАНОВЛЕНА")
            all_ok = False
    
    return all_ok


def check_config():
    """Проверка конфигурационного файла"""
    if not os.path.exists('config.json'):
        print("✗ Файл config.json: НЕ НАЙДЕН")
        return False
    
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        print("✓ Файл config.json: найден и валиден")
        
        # Проверяем наличие обязательных полей
        required = ['launcher_path', 'sandboxie_start', 'common_password', 'accounts']
        for field in required:
            if field not in config:
                print(f"  ✗ Поле '{field}': отсутствует")
                return False
        
        print(f"  ✓ Количество аккаунтов: {len(config['accounts'])}")
        
        return True
    except Exception as e:
        print(f"✗ Файл config.json: ошибка чтения ({e})")
        return False


def check_paths():
    """Проверка путей из конфигурации"""
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Проверяем путь к лаунчеру
        launcher_path = config['launcher_path']
        if os.path.exists(launcher_path):
            print(f"✓ RADMIR Launcher: найден")
            print(f"  Путь: {launcher_path}")
        else:
            print(f"✗ RADMIR Launcher: НЕ НАЙДЕН")
            print(f"  Ожидаемый путь: {launcher_path}")
            return False
        
        # Проверяем путь к Sandboxie
        sandboxie_path = config['sandboxie_start']
        if os.path.exists(sandboxie_path):
            print(f"✓ Sandboxie Start.exe: найден")
            print(f"  Путь: {sandboxie_path}")
        else:
            print(f"✗ Sandboxie Start.exe: НЕ НАЙДЕН")
            print(f"  Ожидаемый путь: {sandboxie_path}")
            return False
        
        return True
    except Exception as e:
        print(f"✗ Ошибка проверки путей: {e}")
        return False


def check_sandboxie_boxes():
    """Проверка наличия песочниц в Sandboxie"""
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Для Sandboxie Classic проверяем конфигурационный файл
        sandboxie_ini_paths = [
            os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Sandboxie.ini'),
            'C:\\Windows\\Sandboxie.ini',
            os.path.join(os.environ.get('ProgramData', 'C:\\ProgramData'), 'Sandboxie\\Sandboxie.ini')
        ]
        
        sandboxie_ini = None
        for ini_path in sandboxie_ini_paths:
            if os.path.exists(ini_path):
                sandboxie_ini = ini_path
                break
        
        if sandboxie_ini:
            # Читаем конфигурацию Sandboxie
            try:
                with open(sandboxie_ini, 'r', encoding='utf-16') as f:
                    ini_content = f.read()
            except:
                try:
                    with open(sandboxie_ini, 'r', encoding='utf-8') as f:
                        ini_content = f.read()
                except:
                    with open(sandboxie_ini, 'r', encoding='cp1251') as f:
                        ini_content = f.read()
            
            # Ищем секции песочниц [BoxName]
            import re
            boxes = re.findall(r'^\[([^\]]+)\]', ini_content, re.MULTILINE)
            # Исключаем служебные секции
            boxes = [b for b in boxes if b not in ['GlobalSettings', 'UserSettings', 'Template']]
            
            if boxes:
                print(f"✓ Sandboxie: {len(boxes)} песочниц найдено")
                print(f"  Конфигурация: {sandboxie_ini}")
                
                # Проверяем наличие нужных песочниц
                required_boxes = [acc['sandbox'] for acc in config['accounts']]
                missing = []
                for box in required_boxes:
                    if box not in boxes:
                        missing.append(box)
                
                if missing:
                    print(f"  ✗ Отсутствуют песочницы: {', '.join(missing[:5])}")
                    if len(missing) > 5:
                        print(f"    ... и еще {len(missing) - 5}")
                    print(f"  ℹ Создайте их в Sandboxie Control")
                    return False
                else:
                    print(f"  ✓ Все необходимые песочницы присутствуют")
                    return True
            else:
                print("? Sandboxie: не найдено ни одной песочницы")
                print("  Создайте песочницы в Sandboxie Control")
                return False
        else:
            print("? Sandboxie: не найден конфигурационный файл")
            print("  Проверьте, что Sandboxie установлен и настроен")
            return None
            
    except Exception as e:
        print(f"? Sandboxie: ошибка проверки ({e})")
        return None


def check_time_sync():
    """Проверка синхронизации времени"""
    try:
        result = subprocess.run(
            ['w32tm', '/query', '/status'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if 'NoSync' in result.stdout or 'не синхрони' in result.stdout.lower():
            print("✓ Синхронизация времени: отключена (рекомендуется)")
            return True
        else:
            print("⚠ Синхронизация времени: включена")
            print("  Рекомендуется отключить для корректной работы")
            return False
            
    except Exception as e:
        print(f"? Синхронизация времени: не удалось проверить")
        return None


def main():
    """Главная функция проверки"""
    print("="*60)
    print("Проверка окружения для RADMIR Multi-Account Launcher")
    print("="*60)
    print()
    
    checks = {
        "Права администратора": check_admin(),
        "Версия Python": check_python_version(),
        "Зависимости Python": check_dependencies(),
        "Конфигурация": check_config(),
        "Пути к файлам": check_paths(),
        "Песочницы Sandboxie": check_sandboxie_boxes(),
        "Синхронизация времени": check_time_sync()
    }
    
    print()
    print("="*60)
    print("Результаты проверки:")
    print("="*60)
    
    passed = sum(1 for v in checks.values() if v is True)
    failed = sum(1 for v in checks.values() if v is False)
    unknown = sum(1 for v in checks.values() if v is None)
    
    print(f"✓ Пройдено: {passed}")
    print(f"✗ Не пройдено: {failed}")
    if unknown > 0:
        print(f"? Неизвестно: {unknown}")
    
    print()
    
    if failed == 0:
        print("✓ Все проверки пройдены! Можно запускать программу.")
    else:
        print("✗ Есть проблемы, которые нужно исправить перед запуском.")
        print()
        print("Рекомендации:")
        if not checks.get("Права администратора"):
            print("  - Запустите этот скрипт от имени администратора")
        if not checks.get("Зависимости Python"):
            print("  - Установите зависимости: pip install -r requirements.txt")
        if not checks.get("Конфигурация") or not checks.get("Пути к файлам"):
            print("  - Проверьте и исправьте config.json")
        if checks.get("Песочницы Sandboxie") is False:
            print("  - Создайте недостающие песочницы в Sandboxie-Plus")
        if checks.get("Синхронизация времени") is False:
            print("  - Отключите синхронизацию времени в настройках Windows")
    
    print()
    print("="*60)
    input("Нажмите Enter для выхода...")


if __name__ == "__main__":
    main()

