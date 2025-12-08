#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Тест для проверки автоматической очистки скриншотов
"""

import os
import time
import requests
import json
from datetime import datetime

def test_auto_cleanup():
    """Тест автоматической очистки скриншотов"""
    print("🧪 ТЕСТИРОВАНИЕ АВТООЧИСТКИ СКРИНШОТОВ")
    print("=" * 60)
    
    # Настройки API
    api_base_url = "http://localhost:8000"
    api_token = "mobile_app_secret_token"
    
    # Тестовый VIN
    test_vin = "WBAJC31010B050810"
    
    print(f"🔍 Проверка VIN: {test_vin}")
    print(f"⏰ Время начала: {datetime.now().strftime('%H:%M:%S')}")
    
    # Список скриншотов до проверки
    screenshots_before = [f for f in os.listdir('.') if f.startswith('dtp_block_') and f.endswith('.png')]
    print(f"📸 Скриншотов до проверки: {len(screenshots_before)}")
    
    try:
        # Отправляем запрос с коротким временем автоочистки (30 секунд)
        request_data = {
            "vin": test_vin,
            "auto_cleanup_delay": 30  # 30 секунд для быстрого тестирования
        }
        
        print(f"📤 Отправляем запрос с auto_cleanup_delay=30 секунд...")
        
        response = requests.post(
            f"{api_base_url}/check/sync", 
            json=request_data,
            headers={"Authorization": f"Bearer {api_token}"},
            timeout=300
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ API проверка завершена за {result.get('check_duration', 0):.1f} сек")
            
            # Собираем скриншоты из результата
            screenshot_files = []
            for section in result.get('results', []):
                if section.get('type') == 'accidents' and section.get('success'):
                    for data_block in section.get('data', []):
                        if 'screenshot_path' in data_block:
                            screenshot_files.append(data_block['screenshot_path'])
            
            print(f"📸 Создано скриншотов: {len(screenshot_files)}")
            for i, screenshot in enumerate(screenshot_files, 1):
                if os.path.exists(screenshot):
                    file_size = os.path.getsize(screenshot)
                    print(f"   {i}. {screenshot} ({file_size} байт)")
                else:
                    print(f"   {i}. {screenshot} (НЕ НАЙДЕН)")
            
            if screenshot_files:
                print(f"\n⏳ Ждем 35 секунд для автоочистки...")
                print(f"⏰ Автоочистка должна сработать в {(datetime.now().timestamp() + 30):.0f}")
                
                # Проверяем наличие файлов каждые 5 секунд
                for i in range(7):  # 7 проверок по 5 секунд = 35 секунд
                    time.sleep(5)
                    existing_files = []
                    for screenshot in screenshot_files:
                        if os.path.exists(screenshot):
                            existing_files.append(screenshot)
                    
                    elapsed = (i + 1) * 5
                    print(f"   ⏰ {elapsed}s: осталось файлов {len(existing_files)}/{len(screenshot_files)}")
                    
                    if len(existing_files) == 0:
                        print(f"✅ Все скриншоты удалены через {elapsed} секунд!")
                        break
                
                # Финальная проверка
                remaining_files = []
                for screenshot in screenshot_files:
                    if os.path.exists(screenshot):
                        remaining_files.append(screenshot)
                
                if remaining_files:
                    print(f"⚠️ Остались неудаленные файлы: {remaining_files}")
                else:
                    print(f"🎉 Автоочистка работает идеально!")
            
            else:
                print(f"⚠️ Не найдено скриншотов для тестирования")
        
        else:
            print(f"❌ Ошибка API: {response.status_code} - {response.text}")
    
    except Exception as e:
        print(f"❌ Ошибка теста: {e}")

def test_manual_cleanup():
    """Тест ручной очистки через endpoint скриншота"""
    print(f"\n🧪 ТЕСТИРОВАНИЕ РУЧНОЙ ОЧИСТКИ")
    print("=" * 60)
    
    # Настройки API
    api_base_url = "http://localhost:8000"
    api_token = "mobile_app_secret_token"
    
    # Найдем первый доступный скриншот
    screenshot_files = [f for f in os.listdir('.') if f.startswith('dtp_block_') and f.endswith('.png')]
    
    if not screenshot_files:
        print("⚠️ Нет скриншотов для тестирования ручной очистки")
        return
    
    test_screenshot = screenshot_files[0]
    print(f"📸 Тестируем с файлом: {test_screenshot}")
    
    if os.path.exists(test_screenshot):
        file_size = os.path.getsize(test_screenshot)
        print(f"📏 Размер файла: {file_size} байт")
        
        try:
            # Запрашиваем скриншот с автоудалением
            response = requests.get(
                f"{api_base_url}/screenshot/{test_screenshot}?delete_after_send=true",
                headers={"Authorization": f"Bearer {api_token}"}
            )
            
            if response.status_code == 200:
                print(f"✅ Скриншот получен: {len(response.content)} байт")
                
                # Ждем немного и проверяем удаление
                time.sleep(3)
                
                if os.path.exists(test_screenshot):
                    print(f"⚠️ Файл все еще существует после запроса на удаление")
                else:
                    print(f"🗑️ Файл успешно удален после отправки!")
            else:
                print(f"❌ Ошибка получения скриншота: {response.status_code}")
        
        except Exception as e:
            print(f"❌ Ошибка теста ручной очистки: {e}")
    else:
        print(f"❌ Файл не найден: {test_screenshot}")

if __name__ == "__main__":
    print("🧪 ЗАПУСК ТЕСТОВ АВТООЧИСТКИ СКРИНШОТОВ")
    print("=" * 60)
    print("📋 Убедитесь что API сервер запущен: python api_mobile_reliable.py")
    print("=" * 60)
    
    test_auto_cleanup()
    test_manual_cleanup()
    
    print("\n✅ Тестирование завершено!") 