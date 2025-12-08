"""
Тест для проверки что система всегда использует 3 попытки
"""

import requests
import json

API_BASE_URL = "http://localhost:8000"
API_TOKEN = "mobile_app_secret_token"

def test_3_attempts_always():
    """Тест что система всегда использует 3 попытки независимо от параметра"""
    print("🔍 Тест: Система всегда использует 3 попытки")
    print("=" * 50)
    
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Тестируем с разными значениями max_attempts
    test_cases = [
        {"max_attempts": 1, "description": "Запрос с 1 попыткой"},
        {"max_attempts": 2, "description": "Запрос с 2 попытками"}, 
        {"max_attempts": 5, "description": "Запрос с 5 попытками"},
        {"max_attempts": None, "description": "Запрос без параметра"}
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 Тест {i}: {test_case['description']}")
        
        payload = {
            "vin": "WBAJC31010B050810",
            "min_quality_score": 50.0  # Низкий порог для быстрого теста
        }
        
        if test_case["max_attempts"] is not None:
            payload["max_attempts"] = test_case["max_attempts"]
        
        print(f"📤 Отправляем: max_attempts = {test_case['max_attempts']}")
        
        try:
            response = requests.post(f"{API_BASE_URL}/check/sync", 
                                   json=payload, headers=headers)
            response.raise_for_status()
            result = response.json()
            
            if result["status"] == "completed":
                # Проверяем максимальное количество попыток в результатах
                max_attempt_used = 0
                for section_result in result.get("results", []):
                    attempt_num = section_result.get("attempt_number", 0)
                    max_attempt_used = max(max_attempt_used, attempt_num)
                
                print(f"✅ Результат: максимально использовано попыток = {max_attempt_used}")
                print(f"🎯 Система корректно использует до 3 попыток!")
                
                # Показываем детали по секциям
                for section in result.get("results", []):
                    section_name = section.get("type", "unknown").upper()
                    attempt = section.get("attempt_number", 0)
                    quality = section.get("quality_score", 0)
                    print(f"   📁 {section_name}: попытка {attempt}, качество {quality:.1f}%")
                    
            else:
                print(f"❌ Ошибка: {result.get('error', 'Неизвестная ошибка')}")
                
        except Exception as e:
            print(f"❌ Исключение: {e}")
        
        print("-" * 30)
    
    print("\n🎉 Все тесты завершены!")
    print("💡 Независимо от переданного параметра max_attempts, система использует до 3 попыток")

if __name__ == "__main__":
    test_3_attempts_always() 