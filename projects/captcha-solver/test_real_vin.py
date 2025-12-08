#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
from gibdd_checker import GIBDDChecker, CheckType

async def test_real_vin():
    """Тестирование с реальным VIN"""
    # VIN предоставленный пользователем
    test_vin = "WBAJC31010B050810"
    
    print(f"🚗 Тестирование ГИБДД чекера с реальным VIN: {test_vin}")
    print("=" * 60)
    
    # Создаем чекер в видимом режиме для отладки
    checker = GIBDDChecker(headless=False)
    
    try:
        # Инициализация
        await checker.initialize()
        print("✅ Чекер инициализирован")
        
        # Вместо одиночной проверки вызываем check_vehicle для всех четырёх типов
        print(f"\n🔍 Проверяем все секции для VIN: {test_vin}")
        results = await checker.check_vehicle(test_vin, [
            CheckType.REGISTRATION,
            CheckType.ACCIDENTS,
            CheckType.WANTED,
            CheckType.RESTRICTIONS
        ])

        for result in results:
            print(f"\n📊 Результат проверки:")
            print(f"  Тип: {result.check_type.value}")
            print(f"  Успех: {result.success}")
            print(f"  CAPTCHA решена: {result.captcha_solved}")
            print(f"  Реклама пройдена: {result.ad_waited}")
            print(f"  Данные получены: {bool(result.data)}")
            if result.data:
                print(f"\n📋 Извлеченные данные:")
                if isinstance(result.data, dict):
                    print(f"  Тип: {result.data.get('type', 'N/A')}")
                    if 'data' in result.data:
                        for item in result.data['data']:
                            text = item.get('text', '')
                            # Убираем 'Скачать выписку' и лишние строки для registration
                            if result.data.get('type') == 'registration':
                                lines = [l for l in text.splitlines() if l.strip() and 'Скачать выписку' not in l and not l.startswith('Элемент')]
                                text = '\n'.join(lines)
                            # Для wanted/restrictions убираем служебные строки
                            if result.data.get('type') in ('wanted', 'restrictions'):
                                lines = [l for l in text.splitlines() if l.strip() and 'Выполняется запрос' not in l and not l.strip().startswith('запросить сведения')]
                                text = '\n'.join(lines)
                            print(f"{text}\n")
                else:
                    print(f"  Данные: {str(result.data)}\n")
            else:
                print(f"  Ошибка: {result.error}")
            
    except Exception as e:
        print(f"❌ Ошибка во время тестирования: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        # Закрываем чекер
        await checker.close()
        print("\n🔚 Тестирование завершено")

if __name__ == "__main__":
    asyncio.run(test_real_vin()) 