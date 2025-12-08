#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import time
from advanced_checker import check_vin_advanced, get_checker_statistics
from config import FAST_CONFIG, PRODUCTION_CONFIG

def test_advanced_checker():
    """Тестирование продвинутого чекера"""
    print("🚀 Тестирование продвинутого ГИБДД чекера")
    print("=" * 60)
    
    # VIN для тестирования
    test_vin = "WBAJC31010B050810"
    
    print(f"\n🔍 Проверяем VIN: {test_vin}")
    print("=" * 40)
    
    # Первая проверка (без кэша)
    print("\n1️⃣ Первая проверка (создание кэша):")
    start_time = time.time()
    result1 = check_vin_advanced(test_vin, FAST_CONFIG)
    duration1 = time.time() - start_time
    
    print(f"⏱️ Время: {duration1:.2f} сек")
    print(f"💾 Из кэша: {result1.get('from_cache', False)}")
    print(f"✅ Успешно: {sum(1 for r in result1['results'] if r['success'])}/{len(result1['results'])}")
    
    # Вторая проверка (из кэша)
    print("\n2️⃣ Вторая проверка (из кэша):")
    start_time = time.time()
    result2 = check_vin_advanced(test_vin, FAST_CONFIG)
    duration2 = time.time() - start_time
    
    print(f"⏱️ Время: {duration2:.2f} сек")
    print(f"💾 Из кэша: {result2.get('from_cache', False)}")
    print(f"🚀 Ускорение: {duration1/duration2:.1f}x")
    
    # Показываем статистику
    print("\n📊 Статистика чекера:")
    print("=" * 40)
    stats = get_checker_statistics()
    
    print(f"📋 Всего проверок: {stats.total_checks}")
    print(f"✅ Успешных: {stats.successful_checks}")
    print(f"❌ Неудачных: {stats.failed_checks}")
    print(f"🎯 Успешность капчи: {stats.captcha_success_rate:.1%}")
    print(f"⏱️ Среднее время: {stats.average_check_time:.2f} сек")
    print(f"💾 Попаданий в кэш: {stats.cache_hits}")
    print(f"🔍 Промахов кэша: {stats.cache_misses}")
    print(f"🕐 Обновлено: {stats.last_updated}")
    
    # Показываем детали результата
    if "results" in result1:
        print("\n📋 Детали проверки:")
        print("=" * 40)
        
        for check_result in result1["results"]:
            print(f"\n🔍 {check_result['type'].upper()}:")
            print(f"   ✅ Успех: {check_result['success']}")
            print(f"   🔒 CAPTCHA: {check_result['captcha_solved']}")
            print(f"   📺 Реклама: {check_result['ad_waited']}")
            
            if not check_result['success']:
                print(f"   ❌ Ошибка: {check_result['error']}")
    
    print("\n🔚 Тестирование завершено")

def test_different_configs():
    """Тестирование разных конфигураций"""
    print("\n🔧 Тестирование конфигураций:")
    print("=" * 40)
    
    test_vin = "WBAJC31010B050810"
    
    configs = {
        "Быстрая": FAST_CONFIG,
        "Продакшн": PRODUCTION_CONFIG
    }
    
    for config_name, config in configs.items():
        print(f"\n📋 Конфигурация: {config_name}")
        print(f"   🖥️ Headless: {config.headless}")
        print(f"   💾 Кэш: {config.enable_cache}")
        print(f"   🔄 Попытки капчи: {config.max_captcha_attempts}")
        print(f"   ⏱️ Таймаут рекламы: {config.ad_timeout} сек")

if __name__ == "__main__":
    test_advanced_checker()
    test_different_configs() 