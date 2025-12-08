#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тестирование производительности API под нагрузкой
"""

import asyncio
import aiohttp
import time
import statistics
from typing import List, Dict, Any
import json

# Конфигурация
API_URL = "http://localhost:8000"
AUTH_TOKEN = "mobile_app_secret_token"
TEST_VINS = [
    "WBAJC31010B050810",  # BMW - реальный VIN
    "Z94K241CBLR147119",  # Skoda - реальный VIN с ДТП
    "WVWZZZ1JZYW386752",  # Volkswagen
    "TMBJF21Z040073067",  # Skoda
    "XTA211440E0123456",  # Lada
]

class PerformanceTester:
    def __init__(self):
        self.results: List[Dict[str, Any]] = []
        
    async def send_request(self, session: aiohttp.ClientSession, vin: str, request_id: int) -> Dict[str, Any]:
        """Отправка одного запроса"""
        start_time = time.time()
        
        try:
            headers = {
                "Authorization": f"Bearer {AUTH_TOKEN}",
                "Content-Type": "application/json"
            }
            
            data = {
                "vin": vin,
                "priority": "normal",
                "client_id": f"test_client_{request_id}",
                "auto_cleanup_delay": 0  # Отключаем автоочистку для тестов
            }
            
            async with session.post(
                f"{API_URL}/check/sync",
                headers=headers,
                json=data,
                timeout=aiohttp.ClientTimeout(total=300)  # 5 минут таймаут
            ) as response:
                response_time = time.time() - start_time
                
                if response.status == 200:
                    result = await response.json()
                    return {
                        "request_id": request_id,
                        "vin": vin,
                        "success": True,
                        "response_time": response_time,
                        "status_code": response.status,
                        "from_cache": result.get("from_cache", False),
                        "results_count": len(result.get("results", [])),
                        "error": None
                    }
                else:
                    error_text = await response.text()
                    return {
                        "request_id": request_id,
                        "vin": vin,
                        "success": False,
                        "response_time": response_time,
                        "status_code": response.status,
                        "from_cache": False,
                        "results_count": 0,
                        "error": error_text
                    }
                    
        except asyncio.TimeoutError:
            return {
                "request_id": request_id,
                "vin": vin,
                "success": False,
                "response_time": time.time() - start_time,
                "status_code": None,
                "from_cache": False,
                "results_count": 0,
                "error": "Timeout"
            }
        except Exception as e:
            return {
                "request_id": request_id,
                "vin": vin,
                "success": False,
                "response_time": time.time() - start_time,
                "status_code": None,
                "from_cache": False,
                "results_count": 0,
                "error": str(e)
            }

    async def get_server_load(self, session: aiohttp.ClientSession) -> Dict[str, Any]:
        """Получение информации о нагрузке сервера"""
        try:
            headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
            async with session.get(
                f"{API_URL}/load-info",
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return {"error": f"Status {response.status}"}
        except Exception as e:
            return {"error": str(e)}

    async def stress_test(self, concurrent_requests: int) -> Dict[str, Any]:
        """Стресс-тест с заданным количеством одновременных запросов"""
        print(f"\n🚀 Запуск стресс-теста: {concurrent_requests} одновременных запросов")
        
        # Создаем сессию
        connector = aiohttp.TCPConnector(limit=100, limit_per_host=100)
        async with aiohttp.ClientSession(connector=connector) as session:
            
            # Проверяем исходное состояние сервера
            initial_load = await self.get_server_load(session)
            print(f"📊 Исходное состояние сервера: {initial_load}")
            
            # Подготавливаем задачи
            tasks = []
            for i in range(concurrent_requests):
                vin = TEST_VINS[i % len(TEST_VINS)]
                # Добавляем номер к VIN чтобы избежать кэширования
                modified_vin = vin[:-3] + f"{i:03d}"
                task = self.send_request(session, modified_vin, i + 1)
                tasks.append(task)
            
            # Запускаем все задачи одновременно
            start_time = time.time()
            print(f"⏰ Начало выполнения: {time.strftime('%H:%M:%S')}")
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            total_time = time.time() - start_time
            print(f"⏰ Завершение: {time.strftime('%H:%M:%S')} (общее время: {total_time:.2f} сек)")
            
            # Обрабатываем результаты
            self.results = []
            exceptions_count = 0
            
            for result in results:
                if isinstance(result, Exception):
                    exceptions_count += 1
                    self.results.append({
                        "success": False,
                        "error": str(result),
                        "response_time": 0
                    })
                else:
                    self.results.append(result)
            
            # Финальное состояние сервера
            final_load = await self.get_server_load(session)
            print(f"📊 Финальное состояние сервера: {final_load}")
            
            return {
                "concurrent_requests": concurrent_requests,
                "total_time": total_time,
                "exceptions_count": exceptions_count,
                "initial_load": initial_load,
                "final_load": final_load
            }

    def analyze_results(self, test_info: Dict[str, Any]) -> Dict[str, Any]:
        """Анализ результатов тестирования"""
        if not self.results:
            return {"error": "Нет результатов для анализа"}
        
        # Базовая статистика
        total_requests = len(self.results)
        successful_requests = sum(1 for r in self.results if r.get("success", False))
        failed_requests = total_requests - successful_requests
        
        # Статистика времени ответа
        response_times = [r.get("response_time", 0) for r in self.results if r.get("response_time", 0) > 0]
        
        if response_times:
            avg_response_time = statistics.mean(response_times)
            median_response_time = statistics.median(response_times)
            min_response_time = min(response_times)
            max_response_time = max(response_times)
            p95_response_time = sorted(response_times)[int(len(response_times) * 0.95)] if len(response_times) > 1 else avg_response_time
        else:
            avg_response_time = median_response_time = min_response_time = max_response_time = p95_response_time = 0
        
        # Статистика по статус-кодам
        status_codes = {}
        for r in self.results:
            code = r.get("status_code", "None")
            status_codes[str(code)] = status_codes.get(str(code), 0) + 1
        
        # Статистика кэширования
        cached_requests = sum(1 for r in self.results if r.get("from_cache", False))
        
        # Пропускная способность
        total_time = test_info.get("total_time", 1)
        throughput = successful_requests / total_time  # успешных запросов в секунду
        
        # Типы ошибок
        error_types = {}
        for r in self.results:
            if not r.get("success", False) and r.get("error"):
                error = r["error"]
                if "Timeout" in error:
                    error_type = "Timeout"
                elif "503" in error or "overloaded" in error:
                    error_type = "Server Overload"
                elif "Connection" in error:
                    error_type = "Connection Error"
                else:
                    error_type = "Other"
                error_types[error_type] = error_types.get(error_type, 0) + 1
        
        return {
            "total_requests": total_requests,
            "successful_requests": successful_requests,
            "failed_requests": failed_requests,
            "success_rate": (successful_requests / total_requests * 100) if total_requests > 0 else 0,
            "cached_requests": cached_requests,
            "cache_rate": (cached_requests / total_requests * 100) if total_requests > 0 else 0,
            "response_time_stats": {
                "average": avg_response_time,
                "median": median_response_time,
                "min": min_response_time,
                "max": max_response_time,
                "p95": p95_response_time
            },
            "throughput_rps": throughput,
            "total_duration": total_time,
            "status_codes": status_codes,
            "error_types": error_types,
            "concurrent_requests": test_info.get("concurrent_requests", 0)
        }

    def print_report(self, analysis: Dict[str, Any]):
        """Вывод отчета о тестировании"""
        print("\n" + "="*80)
        print("📊 ОТЧЕТ О ТЕСТИРОВАНИИ ПРОИЗВОДИТЕЛЬНОСТИ")
        print("="*80)
        
        print(f"\n🎯 Общая статистика:")
        print(f"   Общее количество запросов: {analysis['total_requests']}")
        print(f"   Одновременных запросов: {analysis['concurrent_requests']}")
        print(f"   Успешных запросов: {analysis['successful_requests']}")
        print(f"   Неудачных запросов: {analysis['failed_requests']}")
        print(f"   Процент успеха: {analysis['success_rate']:.1f}%")
        print(f"   Общее время: {analysis['total_duration']:.2f} сек")
        
        print(f"\n⚡ Производительность:")
        print(f"   Пропускная способность: {analysis['throughput_rps']:.2f} запросов/сек")
        print(f"   Запросов из кэша: {analysis['cached_requests']} ({analysis['cache_rate']:.1f}%)")
        
        rt_stats = analysis['response_time_stats']
        print(f"\n⏱️ Время ответа:")
        print(f"   Среднее: {rt_stats['average']:.2f} сек")
        print(f"   Медиана: {rt_stats['median']:.2f} сек")
        print(f"   Минимум: {rt_stats['min']:.2f} сек")
        print(f"   Максимум: {rt_stats['max']:.2f} сек")
        print(f"   95-й процентиль: {rt_stats['p95']:.2f} сек")
        
        print(f"\n📈 Статус-коды:")
        for code, count in analysis['status_codes'].items():
            print(f"   {code}: {count} запросов")
        
        if analysis['error_types']:
            print(f"\n❌ Типы ошибок:")
            for error_type, count in analysis['error_types'].items():
                print(f"   {error_type}: {count} ошибок")
        
        # Рекомендации
        print(f"\n💡 Рекомендации:")
        
        if analysis['success_rate'] < 90:
            print("   ⚠️ Низкий процент успеха - нужно увеличить пул потоков или добавить защиту от перегрузки")
        
        if rt_stats['p95'] > 120:
            print("   ⚠️ Высокое время ответа (P95) - возможно сервер перегружен")
        
        if analysis['throughput_rps'] < 1:
            print("   ⚠️ Низкая пропускная способность - нужна оптимизация архитектуры")
        
        if "Timeout" in analysis['error_types']:
            print("   ⚠️ Много таймаутов - увеличьте время ожидания или количество воркеров")
            
        if "Server Overload" in analysis['error_types']:
            print("   ⚠️ Сервер перегружен - нужна защита от перегрузки")
        
        print("="*80)

async def main():
    """Основная функция тестирования"""
    tester = PerformanceTester()
    
    # Тесты с разной нагрузкой
    test_scenarios = [
        {"name": "Легкая нагрузка", "concurrent": 5},
        {"name": "Средняя нагрузка", "concurrent": 15},
        {"name": "Высокая нагрузка", "concurrent": 30},
        {"name": "Экстремальная нагрузка", "concurrent": 50},
    ]
    
    print("🧪 ТЕСТИРОВАНИЕ ПРОИЗВОДИТЕЛЬНОСТИ API")
    print("="*80)
    
    all_results = []
    
    for scenario in test_scenarios:
        print(f"\n🎬 Сценарий: {scenario['name']}")
        
        # Запускаем тест
        test_info = await tester.stress_test(scenario['concurrent'])
        
        # Анализируем результаты
        analysis = tester.analyze_results(test_info)
        analysis['scenario_name'] = scenario['name']
        all_results.append(analysis)
        
        # Выводим отчет
        tester.print_report(analysis)
        
        # Пауза между тестами
        if scenario != test_scenarios[-1]:
            print("\n⏸️ Пауза 30 секунд между тестами...")
            await asyncio.sleep(30)
    
    # Итоговая сводка
    print("\n" + "="*80)
    print("📋 ИТОГОВАЯ СВОДКА")
    print("="*80)
    
    for result in all_results:
        print(f"\n{result['scenario_name']}:")
        print(f"   Запросов: {result['concurrent_requests']}")
        print(f"   Успех: {result['success_rate']:.1f}%")
        print(f"   Пропускная способность: {result['throughput_rps']:.2f} req/s")
        print(f"   Среднее время: {result['response_time_stats']['average']:.2f}s")
    
    # Сохраняем результаты
    with open("performance_test_results.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Результаты сохранены в performance_test_results.json")

if __name__ == "__main__":
    asyncio.run(main()) 