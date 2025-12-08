"""
Скрипт для автоматической загрузки SOCKS5 прокси из GitHub каждые 5 минут
Источник: https://github.com/databay-labs/free-proxy-list/blob/master/socks5.txt
"""
import requests
import os
import time
import signal
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional, List

# Настройки
UPDATE_INTERVAL = 300  # 5 минут в секундах
PROXY_FILE = "RakLite/proxies.txt"
GITHUB_URL = "https://raw.githubusercontent.com/databay-labs/free-proxy-list/master/socks5.txt"
RUNNING = True

def signal_handler(sig, frame):
    """Обработчик сигнала для корректного завершения"""
    global RUNNING
    print("\n[INFO] Получен сигнал завершения, останавливаем обновление прокси...")
    RUNNING = False
    sys.exit(0)

def download_proxies() -> Optional[List[str]]:
    """Загружает список прокси с GitHub"""
    try:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Загрузка прокси с GitHub...")
        response = requests.get(GITHUB_URL, timeout=15)
        response.raise_for_status()
        
        # Парсим прокси
        proxies = []
        for line in response.text.strip().split('\n'):
            line = line.strip()
            # Проверяем формат ip:port
            if line and ':' in line:
                parts = line.split(':')
                if len(parts) == 2:
                    ip, port = parts[0].strip(), parts[1].strip()
                    # Базовая валидация IP и порта
                    if port.isdigit() and 1 <= int(port) <= 65535:
                        # Проверяем что это похоже на IP (простая проверка)
                        if '.' in ip and len(ip.split('.')) == 4:
                            proxies.append(f"{ip}:{port}")
        
        if proxies:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Загружено {len(proxies)} прокси")
        else:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ⚠️  Не найдено валидных прокси")
        
        return proxies if proxies else None
        
    except requests.exceptions.RequestException as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Ошибка при загрузке: {e}")
        return None
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Неожиданная ошибка: {e}")
        return None

def save_proxies(proxies: List[str], filepath: str = PROXY_FILE) -> bool:
    """Сохраняет прокси в файл"""
    try:
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        # Создаем временный файл для безопасной записи
        temp_file = filepath.with_suffix('.tmp')
        
        with open(temp_file, 'w', encoding='utf-8') as f:
            for proxy in proxies:
                f.write(proxy + '\n')
        
        # Атомарно заменяем старый файл новым
        if filepath.exists():
            filepath.unlink()
        temp_file.rename(filepath)
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 💾 Прокси сохранены в {filepath}")
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 📊 Всего: {len(proxies)} прокси")
        return True
        
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Ошибка при сохранении: {e}")
        return False

def update_proxies() -> bool:
    """Обновляет список прокси"""
    proxies = download_proxies()
    
    if proxies:
        if save_proxies(proxies):
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Обновление завершено успешно")
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Первые 5 прокси: {', '.join(proxies[:5])}")
            return True
        else:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Не удалось сохранить прокси")
            return False
    else:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ⚠️  Прокси не загружены, используем старый список")
        return False

def main_loop():
    """Основной цикл обновления прокси"""
    global RUNNING
    
    # Регистрируем обработчик сигналов
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print("=" * 60)
    print("🔄 АВТОМАТИЧЕСКОЕ ОБНОВЛЕНИЕ ПРОКСИ")
    print("=" * 60)
    print(f"Источник: {GITHUB_URL}")
    print(f"Файл: {PROXY_FILE}")
    print(f"Интервал обновления: {UPDATE_INTERVAL // 60} минут")
    print("=" * 60)
    
    # Первое обновление сразу при запуске
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 🚀 Первоначальная загрузка прокси...")
    update_proxies()
    
    # Основной цикл
    while RUNNING:
        try:
            # Ждем указанный интервал
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] ⏳ Следующее обновление через {UPDATE_INTERVAL // 60} минут...")
            
            # Ждем с проверкой каждую секунду (для возможности прервать)
            for _ in range(UPDATE_INTERVAL):
                if not RUNNING:
                    break
                time.sleep(1)
            
            if RUNNING:
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 🔄 Начало обновления прокси...")
                update_proxies()
                
        except KeyboardInterrupt:
            print("\n[INFO] Прервано пользователем")
            RUNNING = False
            break
        except Exception as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Ошибка в основном цикле: {e}")
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ⏳ Повтор через 60 секунд...")
            time.sleep(60)

def main():
    """Основная функция (одноразовое обновление)"""
    print("=" * 60)
    print("📥 ЗАГРУЗКА SOCKS5 ПРОКСИ")
    print("=" * 60)
    
    proxies = download_proxies()
    
    if proxies:
        if save_proxies(proxies):
            print("=" * 60)
            print("✅ ГОТОВО!")
            print("=" * 60)
            print(f"Первые 10 прокси:")
            for i, proxy in enumerate(proxies[:10], 1):
                print(f"  {i}. {proxy}")
        else:
            print("❌ Не удалось сохранить прокси")
    else:
        print("❌ Не удалось загрузить прокси")

if __name__ == "__main__":
    # Проверяем аргументы командной строки
    if len(sys.argv) > 1 and sys.argv[1] == "--daemon":
        # Режим демона - постоянное обновление
        main_loop()
    else:
        # Одноразовое обновление
        main()

