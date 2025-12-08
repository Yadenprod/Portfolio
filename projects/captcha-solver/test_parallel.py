#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from parallel_checker import check_vin_parallel

def test_parallel():
    """Тестирование параллельного чекера"""
    try:
        # VIN предоставленный пользователем
        test_vin = "WBAJC31010B050810"
        
        print(f"🚗 Тестирование параллельного ГИБДД чекера с VIN: {test_vin}")
        print("=" * 60)
        
        # Запускаем параллельную проверку
        print(f"\n🔍 Запускаем параллельную проверку всех секций для VIN: {test_vin}")
        result = check_vin_parallel(test_vin)
        
        # Проверяем наличие критической ошибки
        if "error" in result:
            print(f"\n❌ Критическая ошибка: {result['error']}")
            return
        
        # Выводим результаты
        print("\n📊 Результаты проверки:")
        print("=" * 60)
        
        success_count = sum(1 for r in result["results"] if r["success"])
        print(f"\n✅ Успешно выполнено: {success_count}/{len(result['results'])} проверок")
        
        for check_result in result["results"]:
            print(f"\n📋 Проверка: {check_result['type']}")
            print(f"✅ Успех: {check_result['success']}")
            print(f"🔒 CAPTCHA решена: {check_result['captcha_solved']}")
            print(f"📺 Реклама пройдена: {check_result['ad_waited']}")
            
            if check_result['success']:
                print("\n📝 Данные:")
                if check_result['type'] == 'registration':
                    for block in check_result['data']['data']:
                        if block['block'] == 'checkResult':
                            print("\nОсновная информация:")
                            print(block['text'])
                        elif block['block'] == 'ownershipPeriods':
                            print("\nПериоды владения:")
                            print(block['text'])
                elif check_result['type'] == 'accidents':
                    for block in check_result['data']['data']:
                        if block['block'] == 'checkResultScreenshot':
                            print(f"\nСкриншот сохранен: {block['screenshot_path']}")
                else:  # wanted или restrictions
                    for block in check_result['data']['data']:
                        if block['block'] == 'checkResult':
                            print("\nРезультат:")
                            print(block['text'])
            else:
                print(f"\n❌ Ошибка: {check_result['error']}")
                
        print("\n🔚 Тестирование завершено")
        
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {str(e)}")

if __name__ == "__main__":
    test_parallel() 