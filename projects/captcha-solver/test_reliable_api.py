"""
Тест надежного API с валидацией данных и повторными попытками
"""

import requests
import time
import json
from typing import Dict, Any

API_BASE_URL = "http://localhost:8000"  # Стандартный порт
API_TOKEN = "mobile_app_secret_token"

class ReliableVINCheckerClient:
    """Клиент для работы с надежным VIN Checker API"""
    
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
    
    def check_vin_reliable(self, vin: str, max_attempts: int = 3, min_quality_score: float = 60.0) -> Dict[str, Any]:
        """Надежная проверка VIN с настраиваемыми параметрами"""
        payload = {
            "vin": vin,
            "max_attempts": max_attempts,
            "min_quality_score": min_quality_score
        }
        response = requests.post(f"{self.base_url}/check/sync", 
                               json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def get_statistics(self) -> Dict[str, Any]:
        """Получить расширенную статистику"""
        response = requests.get(f"{self.base_url}/statistics", headers=self.headers)
        response.raise_for_status()
        return response.json()

def test_reliable_checking():
    """Демонстрация надежной проверки"""
    print("🎯 Тестирование надежного VIN Checker API")
    print("=" * 60)
    
    client = ReliableVINCheckerClient(API_BASE_URL, API_TOKEN)
    
    # Проверяем health
    try:
        health = client.health_check()
        print(f"📊 Статус API: {health['status']}")
        print(f"🔧 Версия: {health['version']}")
        print(f"⚡ Функции надежности: {health['system_stats'].get('reliability_features', False)}")
        print(f"🕐 Uptime: {health['uptime_seconds']:.1f} сек")
    except Exception as e:
        print(f"❌ Ошибка подключения к API: {e}")
        return
    
    # Тестовые VIN номера (система автоматически использует 3 попытки)
    test_cases = [
        {
            "vin": "WBAJC31010B050810",
            "description": "Стандартная надежная проверка (3 попытки)",
            "max_attempts": 3,  # Параметр игнорируется, всегда 3 попытки
            "min_quality_score": 60.0
        },
        {
            "vin": "WBAJC31010B050810", 
            "description": "Высокие требования к качеству (3 попытки)",
            "max_attempts": 3,  # Параметр игнорируется, всегда 3 попытки
            "min_quality_score": 80.0
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🔍 Тест {i}: {test_case['description']}")
        print("=" * 50)
        print(f"📋 VIN: {test_case['vin']}")
        print(f"🔄 Макс. попыток: {test_case['max_attempts']}")
        print(f"🎯 Мин. качество: {test_case['min_quality_score']}%")
        
        start_time = time.time()
        
        try:
            result = client.check_vin_reliable(
                vin=test_case['vin'],
                max_attempts=test_case['max_attempts'],
                min_quality_score=test_case['min_quality_score']
            )
            
            duration = time.time() - start_time
            
            print(f"⏱️ Время выполнения: {duration:.2f} сек")
            print(f"📋 Статус: {result['status']}")
            
            if result['status'] == 'completed':
                # Показываем сводную информацию
                summary = result.get('summary', {})
                if summary:
                    print(f"\n📊 СВОДКА:")
                    print(f"   ✅ Успешных секций: {summary.get('successful_sections', 0)}/{summary.get('total_sections', 0)}")
                    print(f"   🎯 Среднее качество: {summary.get('average_quality_score', 0):.1f}%")
                    print(f"   ⭐ Высококачественных: {summary.get('high_quality_sections', 0)}")
                
                # Детальная информация по секциям
                print(f"\n📋 ДЕТАЛИ ПО СЕКЦИЯМ:")
                for result_section in result.get('results', []):
                    section_name = result_section.get('type', 'unknown').upper()
                    success = result_section.get('success', False)
                    quality = result_section.get('quality_score', 0)
                    attempt = result_section.get('attempt_number', 1)
                    validation_errors = result_section.get('validation_errors', [])
                    
                    print(f"   📁 {section_name}:")
                    print(f"      ✅ Успех: {success}")
                    print(f"      🎯 Качество: {quality:.1f}%")
                    print(f"      🔄 Попытка: {attempt}")
                    
                    if validation_errors:
                        print(f"      ⚠️ Проблемы: {', '.join(validation_errors)}")
                    
                    # Специальная обработка для ДТП
                    if section_name == "ACCIDENTS" and success:
                        data = result_section.get('data', [])
                        for data_block in data:
                            if 'screenshot_path' in data_block:
                                print(f"      📸 Скриншот: {data_block['screenshot_path']}")
                            if 'text' in data_block:
                                text_preview = data_block['text'][:100]
                                print(f"      📝 Текст: {text_preview}...")
                
            else:
                print(f"❌ Ошибка: {result.get('error', 'Неизвестная ошибка')}")
                
        except Exception as e:
            print(f"❌ Исключение: {e}")
    
    # Показываем общую статистику
    print(f"\n📊 ОБЩАЯ СТАТИСТИКА СИСТЕМЫ")
    print("=" * 50)
    
    try:
        stats = client.get_statistics()
        print(f"📋 Всего проверок: {stats['total_checks']}")
        print(f"✅ Успешных: {stats['successful_checks']}")
        print(f"❌ Неудачных: {stats['failed_checks']}")
        print(f"⭐ Высококачественных: {stats['high_quality_checks']}")
        print(f"🔄 Использовано повторов: {stats['retries_used']}")
        print(f"🎯 Процент успеха: {stats['success_rate']:.1f}%")
        print(f"⭐ Процент высокого качества: {stats['high_quality_rate']:.1f}%")
        print(f"🔒 Успешность капчи: {stats['captcha_success_rate']:.1f}%")
        print(f"⏱️ Среднее время: {stats['average_check_time']:.2f} сек")
    except Exception as e:
        print(f"❌ Ошибка получения статистики: {e}")
    
    print(f"\n🎉 Тестирование завершено!")
    print("🔄 Система автоматически улучшает качество данных через повторные попытки")

if __name__ == "__main__":
    test_reliable_checking() 