#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Быстрый тест нагрузки для проверки улучшений производительности
"""

import asyncio
import aiohttp
import time
import json

# Конфигурация
API_URL = "http://localhost:8000"
AUTH_TOKEN = "mobile_app_secret_token"

async def simple_load_test(concurrent_requests: int = 10):
    """Простой тест нагрузки"""
    print(f"🚀 Тестирование {concurrent_requests} одновременных запросов...")
    
    async def send_request(session, request_id):
        """Отправка одного запроса"""
        start_time = time.time()
        
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}",
            "Content-Type": "application/json"
        }
        
        # Используем реальный VIN с модификацией для избежания кэша
        vin = f"WBAJC31010B05{request_id:04d}"
        
        data = {
            "vin": vin,
            "priority": "normal",
            "auto_cleanup_delay": 0
        }
        
        try:
            async with session.post(
                f"{API_URL}/check/sync",
                headers=headers,
                json=data,
                timeout=aiohttp.ClientTimeout(total=180)
            ) as response:
                response_time = time.time() - start_time
                
                if response.status == 200:
                    result = await response.json()
                    return {
                        "id": request_id,
                        "success": True,
                        "time": response_time,
                        "status": response.status,
                        "from_cache": result.get("from_cache", False)
                    }
                else:
                    error_text = await response.text()
                    return {
                        "id": request_id,
                        "success": False,
                        "time": response_time,
                        "status": response.status,
                        "error": error_text[:100]
                    }
        except Exception as e:
            return {
                "id": request_id,
                "success": False,
                "time": time.time() - start_time,
                "status": None,
                "error": str(e)[:100]
            }
    
    async def get_load_info(session):
        """Получение информации о нагрузке"""
        try:
            headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
            async with session.get(f"{API_URL}/load-info", headers=headers) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return {"error": f"Status {response.status}"}
        except Exception as e:
            return {"error": str(e)}
    
    # Создаем сессию
    connector = aiohttp.TCPConnector(limit=100)
    async with aiohttp.ClientSession(connector=connector) as session:
        
        # Проверяем исходное состояние
        initial_load = await get_load_info(session)
        print(f"📊 Исходное состояние: {json.dumps(initial_load, ensure_ascii=False, indent=2)}")
        
        # Запускаем тесты
        start_time = time.time()
        tasks = [send_request(session, i) for i in range(1, concurrent_requests + 1)]
        results = await asyncio.gather(*tasks)
        total_time = time.time() - start_time
        
        # Финальное состояние
        final_load = await get_load_info(session)
        print(f"📊 Финальное состояние: {json.dumps(final_load, ensure_ascii=False, indent=2)}")
        
        # Анализ результатов
        successful = sum(1 for r in results if r["success"])
        failed = len(results) - successful
        avg_time = sum(r["time"] for r in results) / len(results)
        max_time = max(r["time"] for r in results)
        min_time = min(r["time"] for r in results)
        
        print(f"\n📈 РЕЗУЛЬТАТЫ:")
        print(f"   Всего запросов: {len(results)}")
        print(f"   Успешных: {successful}")
        print(f"   Неудачных: {failed}")
        print(f"   Процент успеха: {successful/len(results)*100:.1f}%")
        print(f"   Общее время: {total_time:.2f} сек")
        print(f"   Пропускная способность: {successful/total_time:.2f} req/s")
        print(f"   Время ответа - среднее: {avg_time:.2f}s, мин: {min_time:.2f}s, макс: {max_time:.2f}s")
        
        # Показываем ошибки
        errors = [r for r in results if not r["success"]]
        if errors:
            print(f"\n❌ Ошибки:")
            for error in errors[:5]:  # Показываем первые 5 ошибок
                print(f"   ID {error['id']}: {error.get('error', 'Unknown error')}")
        
        return {
            "total_requests": len(results),
            "successful": successful,
            "failed": failed,
            "success_rate": successful/len(results)*100,
            "total_time": total_time,
            "throughput": successful/total_time,
            "avg_response_time": avg_time
        }

async def main():
    """Основная функция"""
    print("🧪 БЫСТРЫЙ ТЕСТ ПРОИЗВОДИТЕЛЬНОСТИ")
    print("="*50)
    
    # Тестируем разные уровни нагрузки
    test_cases = [5, 10, 20, 30]
    
    for concurrent in test_cases:
        print(f"\n🎯 Тест с {concurrent} одновременными запросами")
        print("-" * 40)
        
        result = await simple_load_test(concurrent)
        
        # Небольшая пауза между тестами
        if concurrent != test_cases[-1]:
            print("\n⏸️ Пауза 10 секунд...")
            await asyncio.sleep(10)
    
    print("\n✅ Все тесты завершены!")

if __name__ == "__main__":
    asyncio.run(main()) 