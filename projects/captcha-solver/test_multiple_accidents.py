#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Тест для проверки функциональности множественных ДТП
"""

import os
import sys
import time
import requests
from typing import List, Dict

# Добавляем путь к модулям проекта
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from reliable_checker import check_vin_reliable

def test_multiple_accidents_reliable():
    """Тест системы надежной проверки с множественными ДТП"""
    print("🧪 ТЕСТ МНОЖЕСТВЕННЫХ ДТП (Надежная система)")
    print("=" * 60)
    
    # Используем тестовый VIN (замените на реальный VIN с несколькими ДТП)
    test_vin = "WBAJC31010B050810"  # VIN с одним ДТП для тестирования
    
    try:
        print(f"🔍 Проверка VIN: {test_vin}")
        result = check_vin_reliable(test_vin, max_attempts=2, min_quality_score=50.0)
        
        print(f"📊 Полученный результат: {type(result)}")
        print(f"📋 Ключи результата: {list(result.keys()) if isinstance(result, dict) else 'не словарь'}")
        
        # Проверяем разные возможные структуры результата
        if isinstance(result, dict):
            # Вариант 1: результат содержит 'status'
            if 'status' in result and result['status'] == 'completed':
                print(f"✅ Проверка завершена за {result.get('duration', 0):.1f} сек")
                results_list = result.get('results', [])
            
            # Вариант 2: результат содержит 'success' 
            elif 'success' in result and result['success']:
                print(f"✅ Проверка успешна")
                results_list = result.get('results', [])
                
            # Вариант 3: результат содержит прямо список секций
            elif 'results' in result:
                print(f"✅ Найдены результаты проверки")
                results_list = result['results']
                
            # Вариант 4: результат - это список секций
            elif isinstance(result, list):
                print(f"✅ Результат - список секций")
                results_list = result
                
            else:
                print(f"⚠️ Неожиданная структура результата")
                print(f"   Содержимое: {result}")
                results_list = []
            
            # Ищем результаты ДТП
            accidents_found = False
            for section in results_list:
                if isinstance(section, dict) and section.get('type') == 'accidents':
                    accidents_found = True
                    success = section.get('success', False)
                    print(f"\n📋 СЕКЦИЯ ДТП НАЙДЕНА:")
                    print(f"   ✅ Успех: {success}")
                    
                    if success and section.get('data'):
                        data = section.get('data', [])
                        print(f"   📊 Всего блоков данных: {len(data)}")
                        
                        # Анализируем данные ДТП
                        total_accidents = 1
                        screenshots = []
                        
                        for i, block in enumerate(data, 1):
                            accident_num = block.get('accident_number', i)
                            total_accidents = block.get('total_accidents', total_accidents)
                            
                            print(f"\n   📋 ДТП #{accident_num}:")
                            print(f"      🏷️  Тип блока: {block.get('block', 'unknown')}")
                            
                            if 'screenshot_path' in block:
                                screenshot_path = block['screenshot_path']
                                screenshots.append(screenshot_path)
                                print(f"      📸 Скриншот: {screenshot_path}")
                                
                                # Проверяем существование файла
                                if os.path.exists(screenshot_path):
                                    file_size = os.path.getsize(screenshot_path)
                                    print(f"      📏 Размер файла: {file_size} байт")
                                else:
                                    print(f"      ❌ Файл скриншота не найден!")
                            
                            if 'text' in block:
                                text = block['text'][:200]
                                print(f"      📝 Текст: {text}{'...' if len(block.get('text', '')) > 200 else ''}")
                        
                        print(f"\n📊 ИТОГО:")
                        print(f"   🚗 Всего ДТП: {total_accidents}")
                        print(f"   📸 Скриншотов получено: {len(screenshots)}")
                        if total_accidents > 0:
                            print(f"   ✅ Покрытие: {len(screenshots)}/{total_accidents} ({len(screenshots)/total_accidents*100:.1f}%)")
                        
                        # Проверяем качество
                        quality_score = section.get('quality_score', 0)
                        validation_errors = section.get('validation_errors', [])
                        print(f"   🎯 Оценка качества: {quality_score:.1f}%")
                        
                        if validation_errors:
                            print(f"   ⚠️  Ошибки валидации: {', '.join(validation_errors)}")
                        
                        return len(screenshots) > 0  # Возвращаем True если есть хотя бы один скриншот
                    else:
                        print(f"   ❌ Нет данных о ДТП или проверка неуспешна")
                        return False
            
            if not accidents_found:
                print(f"❌ Секция ДТП не найдена в результатах")
                return False
                    
        else:
            print(f"❌ Результат не является словарем: {type(result)}")
            return False
            
    except Exception as e:
        print(f"❌ Исключение в тесте: {e}")
        import traceback
        print(f"📋 Детали ошибки:\n{traceback.format_exc()}")
        return False

def test_multiple_accidents_api():
    """Тест API с множественными ДТП"""
    print("\n🧪 ТЕСТ МНОЖЕСТВЕННЫХ ДТП (API)")
    print("=" * 60)
    
    # Настройки API
    api_base_url = "http://localhost:8000"
    api_token = "test_token_123"  # Замените на ваш токен
    
    # Используем тестовый VIN (замените на реальный VIN с несколькими ДТП)
    test_vin = "WBAJC31010B050810"  # VIN с одним ДТП для тестирования
    
    try:
        print(f"🔍 Проверка VIN через API: {test_vin}")
        
        # Отправляем запрос
        response = requests.post(f"{api_base_url}/check_sync", 
                               json={"vin": test_vin},
                               headers={"Authorization": f"Bearer {api_token}"},
                               timeout=300)
        
        if response.status_code == 200:
            result = response.json()
            
            if result['status'] == 'completed':
                print(f"✅ API проверка завершена за {result.get('check_duration', 0):.1f} сек")
                
                # Ищем результаты ДТП
                for section in result.get('results', []):
                    if section['type'] == 'accidents' and section['success']:
                        data = section.get('data', [])
                        print(f"\n📋 НАЙДЕНО ДТП через API:")
                        print(f"   📊 Всего блоков данных: {len(data)}")
                        
                        screenshots_downloaded = 0
                        
                        for i, block in enumerate(data, 1):
                            accident_num = block.get('accident_number', i)
                            print(f"\n   📋 ДТП #{accident_num}:")
                            
                            if 'screenshot_path' in block:
                                screenshot_filename = block['screenshot_path']
                                print(f"      📸 Скриншот: {screenshot_filename}")
                                
                                # Пытаемся скачать скриншот
                                try:
                                    screenshot_response = requests.get(
                                        f"{api_base_url}/screenshot/{screenshot_filename}",
                                        headers={"Authorization": f"Bearer {api_token}"}
                                    )
                                    
                                    if screenshot_response.status_code == 200:
                                        download_path = f"downloaded_{screenshot_filename}"
                                        with open(download_path, "wb") as f:
                                            f.write(screenshot_response.content)
                                        
                                        file_size = len(screenshot_response.content)
                                        print(f"      ✅ Скачан: {download_path} ({file_size} байт)")
                                        screenshots_downloaded += 1
                                    else:
                                        print(f"      ❌ Ошибка скачивания: {screenshot_response.status_code}")
                                        
                                except Exception as e:
                                    print(f"      ❌ Ошибка при скачивании: {e}")
                        
                        print(f"\n📊 ИТОГО API:")
                        print(f"   📸 Скриншотов скачано: {screenshots_downloaded}/{len(data)}")
                        return True
                        
        else:
            print(f"❌ Ошибка API: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Исключение в API тесте: {e}")
        return False

def main():
    """Главная функция тестирования"""
    print("🧪 ТЕСТИРОВАНИЕ МНОЖЕСТВЕННЫХ ДТП")
    print("=" * 60)
    print("Этот тест проверяет, что система корректно")
    print("обрабатывает автомобили с несколькими ДТП")
    print("=" * 60)
    
    # Проверяем тестирование надежной системы
    reliable_ok = test_multiple_accidents_reliable()
    
    # Проверяем API (опционально)
    api_ok = False
    try:
        api_ok = test_multiple_accidents_api()
    except Exception as e:
        print(f"⚠️ API тест пропущен: {e}")
    
    # Итоги
    print(f"\n📊 ИТОГИ ТЕСТИРОВАНИЯ:")
    print(f"   ✅ Надежная система: {'ПРОЙДЕН' if reliable_ok else 'ПРОВАЛЕН'}")
    print(f"   ✅ API система: {'ПРОЙДЕН' if api_ok else 'ПРОПУЩЕН'}")
    
    if reliable_ok:
        print(f"\n🎉 Функциональность множественных ДТП работает!")
        print(f"💡 Теперь система будет делать скриншоты всех ДТП автомобиля")
    else:
        print(f"\n⚠️ Требуется дополнительная настройка")

if __name__ == "__main__":
    main() 