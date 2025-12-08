#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тест ограничения потоков для предотвращения перегрузки системы
"""

import requests
import time
import threading
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

API_URL = "http://localhost:8000"  # URL вашего API
TOKEN = "mobile_app_secret_token"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# Тестовые VIN номера
TEST_VINS = [
    "WBAJC31010B050810",
    "1HGBH41JXMN109186", 
    "JF1VA1H60M9016641",
    "1NXBR32E25Z461317",
    "5NPEB4AC9DH654321",
    "KMHD35LH3EU123456",
    "YV1CZ59H9X2123456",
    "WP0ZZZ99ZZS123456",
    "VF7RDHFU0CW123456",
    "SALGS2SE0EA123456"
]

def check_vin(vin, request_id):
    """Проверка одного VIN"""
    try:
        start_time = time.time()
        print(f"🔄 Запрос #{request_id}: Начинаем проверку VIN {vin}")
        
        # Проверяем нагрузку до запроса
        try:
            load_response = requests.get(f"{API_URL}/load-info", headers=HEADERS, timeout=5)
            if load_response.status_code == 200:
                load_data = load_response.json()
                print(f"📊 Запрос #{request_id}: Нагрузка до запроса - активных: {load_data.get('active_tasks', 'N/A')}, статус: {load_data.get('status', 'N/A')}")
        except Exception as e:
            print(f"⚠️ Запрос #{request_id}: Не удалось получить информацию о нагрузке: {e}")
        
        # Отправляем запрос на проверку VIN
        response = requests.post(
            f"{API_URL}/check/sync",
            headers=HEADERS,
            json={"vin": vin, "auto_cleanup_delay": 60},  # Автоочистка через 1 минуту
            timeout=300  # 5 минут таймаут
        )
        
        duration = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            status = data.get("status", "unknown")
            results_count = len(data.get("results", []))
            print(f"✅ Запрос #{request_id}: VIN {vin} проверен за {duration:.2f}с, статус: {status}, результатов: {results_count}")
            return {
                "request_id": request_id,
                "vin": vin,
                "success": True,
                "duration": duration,
                "status": status,
                "results_count": results_count
            }
        elif response.status_code == 503:
            print(f"🚫 Запрос #{request_id}: Сервер перегружен для VIN {vin} - {response.text}")
            return {
                "request_id": request_id,
                "vin": vin,
                "success": False,
                "duration": duration,
                "error": "Server overloaded",
                "status_code": 503
            }
        else:
            print(f"❌ Запрос #{request_id}: Ошибка {response.status_code} для VIN {vin}: {response.text}")
            return {
                "request_id": request_id,
                "vin": vin,
                "success": False,
                "duration": duration,
                "error": response.text,
                "status_code": response.status_code
            }
            
    except requests.exceptions.Timeout:
        duration = time.time() - start_time
        print(f"⏰ Запрос #{request_id}: Таймаут для VIN {vin} после {duration:.2f}с")
        return {
            "request_id": request_id,
            "vin": vin,
            "success": False,
            "duration": duration,
            "error": "Timeout"
        }
    except Exception as e:
        duration = time.time() - start_time
        print(f"❌ Запрос #{request_id}: Ошибка для VIN {vin}: {e}")
        return {
            "request_id": request_id,
            "vin": vin,
            "success": False,
            "duration": duration,
            "error": str(e)
        }

def test_thread_limits():
    """Тест ограничения потоков"""
    print("🚀 ТЕСТ ОГРАНИЧЕНИЯ ПОТОКОВ")
    print("="*60)
    
    # Проверяем статус API
    try:
        health_response = requests.get(f"{API_URL}/health", headers=HEADERS, timeout=10)
        if health_response.status_code == 200:
            health_data = health_response.json()
            print(f"✅ API доступен, версия: {health_data.get('version', 'N/A')}")
        else:
            print(f"❌ API недоступен: {health_response.status_code}")
            return
    except Exception as e:
        print(f"❌ Не удалось подключиться к API: {e}")
        return
    
    # Тест 1: Небольшая нагрузка (3 одновременных запроса)
    print(f"\n📋 ТЕСТ 1: Отправляем 3 одновременных запроса")
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = []
        for i in range(3):
            vin = TEST_VINS[i % len(TEST_VINS)]
            future = executor.submit(check_vin, vin, i+1)
            futures.append(future)
        
        results = []
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
    
    test1_duration = time.time() - start_time
    successful = sum(1 for r in results if r.get("success", False))
    print(f"📊 ТЕСТ 1 ЗАВЕРШЕН: {successful}/{len(results)} успешных за {test1_duration:.2f}с")
    
    # Ждем немного между тестами
    print("\n⏳ Ожидание 10 секунд между тестами...")
    time.sleep(10)
    
    # Тест 2: Высокая нагрузка (8 одновременных запросов)
    print(f"\n📋 ТЕСТ 2: Отправляем 8 одновременных запросов (должна сработать очередь)")
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = []
        for i in range(8):
            vin = TEST_VINS[i % len(TEST_VINS)]
            future = executor.submit(check_vin, vin, i+11)
            futures.append(future)
            time.sleep(0.5)  # Небольшая задержка между запросами
        
        results = []
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
    
    test2_duration = time.time() - start_time
    successful = sum(1 for r in results if r.get("success", False))
    overloaded = sum(1 for r in results if r.get("status_code") == 503)
    print(f"📊 ТЕСТ 2 ЗАВЕРШЕН: {successful}/{len(results)} успешных, {overloaded} отклонено (перегрузка) за {test2_duration:.2f}с")
    
    # Показываем финальную статистику
    print(f"\n📈 ИТОГОВАЯ СТАТИСТИКА:")
    try:
        stats_response = requests.get(f"{API_URL}/statistics", headers=HEADERS, timeout=10)
        if stats_response.status_code == 200:
            stats_data = stats_response.json()
            print(f"   Всего проверок: {stats_data.get('total_checks', 'N/A')}")
            print(f"   Успешных: {stats_data.get('successful_checks', 'N/A')}")
            print(f"   Неудачных: {stats_data.get('failed_checks', 'N/A')}")
            print(f"   Средняя длительность: {stats_data.get('average_check_time', 'N/A'):.2f}с")
    except Exception as e:
        print(f"   ⚠️ Не удалось получить статистику: {e}")
    
    print("="*60)
    print("✅ ТЕСТ ЗАВЕРШЕН")

if __name__ == "__main__":
    test_thread_limits() 