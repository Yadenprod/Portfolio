#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Отладочный скрипт для проверки автоочистки скриншотов
"""

import os
import time
import threading
from reliable_checker import check_vin_reliable

def debug_cleanup_function():
    """Тестируем логику автоочистки"""
    print("🔍 ОТЛАДКА АВТООЧИСТКИ")
    print("=" * 50)
    
    # Проверяем текущие скриншоты
    existing_screenshots = [f for f in os.listdir('.') if f.startswith('dtp_block_') and f.endswith('.png')]
    print(f"📸 Найдено скриншотов до теста: {len(existing_screenshots)}")
    for screenshot in existing_screenshots:
        print(f"   - {screenshot}")
    
    if not existing_screenshots:
        print("⚠️ Нет скриншотов для тестирования. Создаем тестовый...")
        # Запускаем проверку VIN чтобы создать скриншот
        try:
            result = check_vin_reliable("WBAJC31010B050810", max_attempts=1)
            print(f"✅ Создан тестовый результат")
            
            # Обновляем список скриншотов
            existing_screenshots = [f for f in os.listdir('.') if f.startswith('dtp_block_') and f.endswith('.png')]
            print(f"📸 Скриншотов после создания: {len(existing_screenshots)}")
        except Exception as e:
            print(f"❌ Ошибка создания тестового скриншота: {e}")
            return
    
    if not existing_screenshots:
        print("❌ Не удалось создать тестовые скриншоты")
        return
    
    # Имитируем структуру результатов API
    mock_results = [
        {
            'type': 'accidents',
            'success': True,
            'data': []
        }
    ]
    
    # Добавляем все найденные скриншоты в mock результаты
    for i, screenshot in enumerate(existing_screenshots, 1):
        mock_results[0]['data'].append({
            'screenshot_path': screenshot,
            'accident_number': i,
            'block': 'checkResultScreenshot'
        })
    
    print(f"\n🔧 ТЕСТИРУЕМ ФУНКЦИЮ АВТООЧИСТКИ")
    print(f"📋 Mock результаты содержат {len(mock_results[0]['data'])} скриншотов")
    
    # Копируем функцию автоочистки из API
    def test_cleanup_screenshots_after_check(results, delay_seconds=5):
        """Тестовая версия функции автоочистки с отладкой"""
        def delayed_cleanup():
            print(f"⏳ Ждем {delay_seconds} секунд перед очисткой...")
            time.sleep(delay_seconds)
            screenshot_files = []
            
            try:
                print(f"🔍 Анализируем результаты...")
                print(f"   Результатов: {len(results)}")
                
                # Собираем все пути к скриншотам из результатов
                for i, result in enumerate(results):
                    print(f"   Результат {i+1}: тип {type(result)}")
                    if isinstance(result, dict):
                        print(f"      Ключи: {list(result.keys())}")
                        if result.get('data'):
                            print(f"      Данных: {len(result['data'])}")
                            for j, data_block in enumerate(result['data']):
                                print(f"         Блок {j+1}: {type(data_block)}")
                                if isinstance(data_block, dict):
                                    print(f"            Ключи: {list(data_block.keys())}")
                                    if 'screenshot_path' in data_block:
                                        screenshot_path = data_block['screenshot_path']
                                        print(f"            Скриншот: {screenshot_path}")
                                        if os.path.exists(screenshot_path):
                                            screenshot_files.append(screenshot_path)
                                            print(f"            ✅ Файл существует")
                                        else:
                                            print(f"            ❌ Файл не найден")
                
                print(f"\n🗑️ Найдено {len(screenshot_files)} файлов для удаления:")
                for file_path in screenshot_files:
                    print(f"   - {file_path}")
                
                # Удаляем файлы
                deleted_count = 0
                for file_path in screenshot_files:
                    try:
                        os.remove(file_path)
                        deleted_count += 1
                        print(f"🗑️ Удален скриншот: {file_path}")
                    except Exception as e:
                        print(f"⚠️ Не удалось удалить скриншот {file_path}: {e}")
                
                if deleted_count > 0:
                    print(f"✅ Автоочистка завершена: удалено {deleted_count} скриншотов")
                else:
                    print(f"⚠️ Не удалось удалить ни одного файла")
            
            except Exception as e:
                print(f"❌ Ошибка в автоочистке скриншотов: {e}")
        
        # Запускаем очистку в фоне
        cleanup_thread = threading.Thread(target=delayed_cleanup, daemon=True)
        cleanup_thread.start()
        return cleanup_thread
    
    # Запускаем тест
    thread = test_cleanup_screenshots_after_check(mock_results, delay_seconds=5)
    
    # Ждем завершения
    thread.join(timeout=10)
    
    # Проверяем результат
    remaining_screenshots = [f for f in os.listdir('.') if f.startswith('dtp_block_') and f.endswith('.png')]
    print(f"\n📊 РЕЗУЛЬТАТ:")
    print(f"   Было: {len(existing_screenshots)} скриншотов")
    print(f"   Осталось: {len(remaining_screenshots)} скриншотов")
    print(f"   Удалено: {len(existing_screenshots) - len(remaining_screenshots)}")
    
    if len(remaining_screenshots) < len(existing_screenshots):
        print(f"✅ Автоочистка работает!")
    else:
        print(f"❌ Автоочистка не работает")

if __name__ == "__main__":
    debug_cleanup_function() 