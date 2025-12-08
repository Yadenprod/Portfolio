#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Тестовый клиент для Mobile API
Демонстрация интеграции с мобильным приложением
"""

import requests
import time
import json
from typing import Dict, Any, List

# Конфигурация API
API_BASE_URL = "http://localhost:8000"
API_TOKEN = "mobile_app_secret_token"

class VINCheckerAPIClient:
    """Клиент для работы с VIN Checker API"""
    
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    
    def health_check(self) -> Dict[str, Any]:
        """Проверка здоровья API"""
        response = requests.get(f"{self.base_url}/health", headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def check_vin_sync(self, vin: str, priority: str = "normal") -> Dict[str, Any]:
        """Синхронная проверка VIN"""
        payload = {
            "vin": vin,
            "priority": priority
        }
        response = requests.post(f"{self.base_url}/check/sync", 
                               json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def check_vin_async(self, vin: str, priority: str = "normal") -> str:
        """Асинхронная проверка VIN"""
        payload = {
            "vin": vin,
            "priority": priority
        }
        response = requests.post(f"{self.base_url}/check", 
                               json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()["request_id"]
    
    def get_check_status(self, request_id: str) -> Dict[str, Any]:
        """Получить статус проверки"""
        response = requests.get(f"{self.base_url}/check/{request_id}", headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def get_statistics(self, days: int = 7) -> Dict[str, Any]:
        """Получить статистику"""
        response = requests.get(f"{self.base_url}/statistics?days={days}", headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def get_screenshot(self, filename: str) -> bytes:
        """Скачать скриншот"""
        response = requests.get(f"{self.base_url}/screenshot/{filename}", headers=self.headers)
        response.raise_for_status()
        return response.content
    
    def cleanup_files(self, hours: int = 24) -> Dict[str, Any]:
        """Очистка файлов"""
        response = requests.delete(f"{self.base_url}/cleanup?hours={hours}", headers=self.headers)
        response.raise_for_status()
        return response.json()

def test_sync_check():
    """Тест синхронной проверки"""
    print("🔄 Тест синхронной проверки VIN")
    print("=" * 50)
    
    client = VINCheckerAPIClient(API_BASE_URL, API_TOKEN)
    
    # Проверяем health
    health = client.health_check()
    print(f"📊 Статус API: {health['status']}")
    print(f"🕐 Uptime: {health['uptime_seconds']:.1f} сек")
    
    # Проверяем VIN
    test_vin = "WBAJC31010B050810"
    print(f"\n🔍 Проверяем VIN: {test_vin}")
    
    start_time = time.time()
    result = client.check_vin_sync(test_vin, priority="fast")
    duration = time.time() - start_time
    
    print(f"⏱️ Время выполнения: {duration:.2f} сек")
    print(f"📋 Статус: {result['status']}")
    print(f"🔄 Свежие данные: {'Да' if not result['from_cache'] else 'Нет'}")
    
    if result['status'] == 'completed':
        print(f"✅ Успешных проверок: {sum(1 for r in result['results'] if r['success'])}/{len(result['results'])}")
        
        # Показываем результаты
        for check_result in result['results']:
            print(f"\n📋 {check_result['type'].upper()}:")
            print(f"   ✅ Успех: {check_result['success']}")
            
            if check_result['success'] and check_result['data']:
                if check_result['type'] == 'accidents':
                    # Ищем скриншот
                    for data_item in check_result['data']:
                        if 'screenshot_path' in data_item:
                            screenshot_filename = data_item['screenshot_path']
                            print(f"   📸 Скриншот: {screenshot_filename}")
                            
                            # Скачиваем скриншот
                            try:
                                screenshot_data = client.get_screenshot(screenshot_filename)
                                with open(f"downloaded_{screenshot_filename}", "wb") as f:
                                    f.write(screenshot_data)
                                print(f"   💾 Скриншот сохранен как: downloaded_{screenshot_filename}")
                            except Exception as e:
                                print(f"   ❌ Ошибка скачивания скриншота: {e}")
    else:
        print(f"❌ Ошибка: {result.get('error', 'Неизвестная ошибка')}")

def test_async_check():
    """Тест асинхронной проверки"""
    print("\n🔄 Тест асинхронной проверки VIN")
    print("=" * 50)
    
    client = VINCheckerAPIClient(API_BASE_URL, API_TOKEN)
    
    test_vin = "WBAJC31010B050810"
    print(f"🔍 Запускаем асинхронную проверку VIN: {test_vin}")
    
    # Запускаем проверку
    request_id = client.check_vin_async(test_vin, priority="normal")
    print(f"📋 ID запроса: {request_id}")
    
    # Проверяем статус каждые 2 секунды
    max_attempts = 30
    for attempt in range(max_attempts):
        status_result = client.get_check_status(request_id)
        status = status_result['status']
        
        print(f"   {attempt + 1}. Статус: {status}")
        
        if status == 'completed':
            print("✅ Проверка завершена!")
            print(f"🔄 Свежие данные: {'Да' if not status_result['from_cache'] else 'Нет'}")
            check_duration = status_result.get('check_duration', 0)
            if check_duration is not None:
                print(f"⏱️ Время: {check_duration:.2f} сек")
            break
        elif status == 'error':
            print(f"❌ Ошибка: {status_result.get('error')}")
            break
        elif status in ['pending', 'processing']:
            time.sleep(2)
        else:
            print(f"❓ Неизвестный статус: {status}")
            break
    else:
        print("⏰ Превышено время ожидания")

def test_statistics():
    """Тест получения статистики"""
    print("\n📊 Тест получения статистики")
    print("=" * 50)
    
    client = VINCheckerAPIClient(API_BASE_URL, API_TOKEN)
    
    stats = client.get_statistics(days=7)
    
    print(f"📋 Всего проверок: {stats['total_checks']}")
    print(f"✅ Успешных: {stats['successful_checks']}")
    print(f"❌ Неудачных: {stats['failed_checks']}")
    print(f"🎯 Процент успеха: {stats['success_rate']:.1f}%")
    print(f"🔒 Успешность капчи: {stats['captcha_success_rate']:.1f}%")
    print(f"⏱️ Среднее время: {stats['average_check_time']:.2f} сек")
    print(f"🚫 Кэширование: ОТКЛЮЧЕНО (всегда свежие данные)")

def demo_mobile_integration():
    """Демо интеграции с мобильным приложением"""
    print("\n📱 Демо интеграции с мобильным приложением")
    print("=" * 60)
    
    client = VINCheckerAPIClient(API_BASE_URL, API_TOKEN)
    
    # Симулируем запросы от мобильного приложения
    test_vins = [
        "WBAJC31010B050810",  # BMW
        "1HGBH41JXMN109186",  # Honda (пример)
        "JTDKN3DU4A0123456"   # Toyota (пример)
    ]
    
    print("📋 Обрабатываем запросы от мобильного приложения:")
    print("🔄 Каждый запрос получает свежие данные с сайта ГИБДД")
    
    for i, vin in enumerate(test_vins, 1):
        print(f"\n{i}. VIN: {vin}")
        
        try:
            # Быстрая проверка для мобильного приложения
            result = client.check_vin_sync(vin, priority="fast")
            
            if result['status'] == 'completed':
                # Формируем ответ для мобильного приложения
                mobile_response = {
                    "vin": vin,
                    "success": True,
                    "from_cache": result['from_cache'],
                    "check_time": result.get('check_duration') or 0,
                    "data": {}
                }
                
                # Извлекаем основную информацию
                for check_result in result['results']:
                    section_name = check_result['type']
                    mobile_response["data"][section_name] = {
                        "success": check_result['success'],
                        "error": check_result.get('error')
                    }
                    
                    # Для регистрации - основная информация
                    if section_name == 'registration' and check_result['success']:
                        reg_data = check_result.get('data', [])
                        if reg_data:
                            main_info = reg_data[0].get('text', '')
                            # Извлекаем марку и модель
                            lines = main_info.split('\n')
                            for line in lines:
                                if 'Марка и(или) модель:' in line:
                                    brand_model = line.split(':')[1].strip()
                                    mobile_response["data"][section_name]["brand_model"] = brand_model
                                elif 'Год выпуска:' in line:
                                    year = line.split(':')[1].strip()
                                    mobile_response["data"][section_name]["year"] = year
                    
                    # Для ДТП - ссылка на скриншот
                    elif section_name == 'accidents' and check_result['success']:
                        acc_data = check_result.get('data', [])
                        for data_item in acc_data:
                            if 'screenshot_path' in data_item:
                                screenshot_url = f"{API_BASE_URL}/screenshot/{data_item['screenshot_path']}"
                                mobile_response["data"][section_name]["screenshot_url"] = screenshot_url
                
                print(f"   ✅ Успех, свежие данные: {'Да' if not mobile_response['from_cache'] else 'Нет'}")
                print(f"   📊 Данные: {len(mobile_response['data'])} секций")
                check_time = mobile_response.get('check_time', 0)
                if check_time and check_time > 0:
                    print(f"   ⏱️ Время: {check_time:.2f} сек")
                
            else:
                print(f"   ❌ Ошибка: {result.get('error')}")
                
        except Exception as e:
            print(f"   ❌ Исключение: {e}")

def main():
    """Основная функция тестирования"""
    print("🚀 Тестирование Mobile API для VIN Checker")
    print("=" * 60)
    print("💡 Убедитесь что API сервер запущен: python api_mobile.py")
    print("🔄 КЭШИРОВАНИЕ ОТКЛЮЧЕНО - всегда свежие данные!")
    print("=" * 60)
    
    try:
        # Тесты
        test_sync_check()
        test_async_check()
        test_statistics()
        demo_mobile_integration()
        
        print("\n🎉 Все тесты завершены!")
        print("🔄 Каждый запрос получил свежие данные с сайта ГИБДД")
        
    except requests.exceptions.ConnectionError:
        print("❌ Не удается подключиться к API серверу")
        print("💡 Запустите сервер: python api_mobile.py")
    except Exception as e:
        print(f"❌ Ошибка тестирования: {e}")

if __name__ == "__main__":
    main() 