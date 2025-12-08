import requests
import time
import json
from typing import Optional

class GIBDDApiClient:
    """Клиент для работы с ГИБДД API"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip('/')
        
    def check_vehicle(self, vin: str, check_types: Optional[list] = None) -> dict:
        """Отправка запроса на проверку автомобиля"""
        if check_types is None:
            check_types = ["registration", "accidents"]
            
        url = f"{self.base_url}/api/v1/check"
        payload = {
            "vin": vin,
            "check_types": check_types
        }
        
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    
    def get_status(self, request_id: str) -> dict:
        """Получение статуса запроса"""
        url = f"{self.base_url}/api/v1/status/{request_id}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    
    def get_results(self, request_id: str) -> dict:
        """Получение результатов проверки"""
        url = f"{self.base_url}/api/v1/result/{request_id}"
        response = requests.get(url)
        return response.json()
    
    def wait_for_completion(self, request_id: str, timeout: int = 300, check_interval: int = 10) -> dict:
        """Ожидание завершения обработки запроса"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                status = self.get_status(request_id)
                print(f"📊 Статус: {status['status']}")
                
                if status['status'] in ['completed', 'failed', 'cancelled']:
                    if status['status'] == 'completed':
                        return self.get_results(request_id)
                    else:
                        return status
                        
                time.sleep(check_interval)
                
            except Exception as e:
                print(f"❌ Ошибка проверки статуса: {e}")
                time.sleep(check_interval)
                
        raise TimeoutError(f"Превышен таймаут ожидания ({timeout} сек)")

def main():
    """Тестирование API"""
    print("🚀 Тестирование ГИБДД API клиента...")
    
    # Создаем клиент
    client = GIBDDApiClient()
    
    # Проверяем доступность API
    try:
        response = requests.get(f"{client.base_url}/health")
        if response.status_code == 200:
            print("✅ API доступен")
        else:
            print("❌ API недоступен")
            return
    except Exception as e:
        print(f"❌ Ошибка подключения к API: {e}")
        return
    
    # Тестовый VIN (можно заменить на реальный)
    test_vin = "WVWZZZ1JZYW386752"
    print(f"🔍 Тестируем VIN: {test_vin}")
    
    try:
        # Отправляем запрос на проверку
        print("\n1️⃣ Отправляем запрос на проверку...")
        check_response = client.check_vehicle(test_vin, ["registration", "accidents"])
        request_id = check_response["request_id"]
        
        print(f"✅ Запрос создан:")
        print(f"   ID: {request_id}")
        print(f"   VIN: {check_response['vin']}")
        print(f"   Статус: {check_response['status']}")
        print(f"   Ожидаемое время: {check_response['estimated_completion']}")
        
        # Ждем завершения обработки
        print(f"\n2️⃣ Ожидаем завершения обработки...")
        results = client.wait_for_completion(request_id)
        
        # Выводим результаты
        print(f"\n3️⃣ Результаты проверки:")
        print(f"{'='*60}")
        print(f"Request ID: {results['request_id']}")
        print(f"VIN: {results['vin']}")
        print(f"Всего проверок: {results['total_checks']}")
        print(f"Успешных: {results['successful_checks']}")
        print(f"Время обработки: {results['processing_time']:.2f} сек")
        print(f"Завершено: {results['completed_at']}")
        
        print(f"\n📋 Детальные результаты:")
        for i, result in enumerate(results['results'], 1):
            print(f"\n{i}. Проверка: {result['check_type']}")
            print(f"   ✅ Успех: {result['success']}")
            if result['success']:
                print(f"   🔐 CAPTCHA решена: {result['captcha_solved']}")
                print(f"   📺 Реклама пройдена: {result['ad_waited']}")
                if result['data']:
                    print(f"   📊 Данные получены: {len(str(result['data']))} символов")
            else:
                print(f"   ❌ Ошибка: {result['error']}")
                
    except Exception as e:
        print(f"❌ Ошибка тестирования: {e}")

if __name__ == "__main__":
    main() 