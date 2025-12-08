"""
Базовое тестирование компонентов NeiroComment
"""
import os
import sys

def test_file_structure():
    """Тестирование структуры файлов"""
    print("🔍 Проверка структуры файлов...")
    
    required_files = [
        "app/__init__.py",
        "app/main.py",
        "app/config.py",
        "app/database/__init__.py",
        "app/database/models.py",
        "app/database/connection.py",
        "app/telegram/__init__.py",
        "app/telegram/client.py",
        "app/telegram/monitor.py",
        "app/ai/__init__.py",
        "app/ai/generator.py",
        "app/ai/prompts.py",
        "app/web/__init__.py",
        "app/web/routes.py",
        "app/monitoring/__init__.py",
        "app/monitoring/logger.py",
        "app/monitoring/metrics.py",
        "requirements.txt",
        "README.md",
        "SETUP.md",
        "EXAMPLES.md",
        "Dockerfile",
        "docker-compose.yml"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Отсутствуют файлы: {missing_files}")
        return False
    else:
        print("✅ Все необходимые файлы присутствуют")
        return True

def test_imports():
    """Тестирование импортов"""
    print("\n📦 Проверка импортов...")
    
    try:
        # Добавляем путь к приложению
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        # Тестируем основные импорты
        from app.config import settings
        print("✅ app.config импортирован")
        
        from app.database.models import Channel, Post, Comment
        print("✅ app.database.models импортирован")
        
        from app.ai.prompts import CommentPrompts
        print("✅ app.ai.prompts импортирован")
        
        from app.monitoring.metrics import MetricsCollector
        print("✅ app.monitoring.metrics импортирован")
        
        return True
        
    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        return False
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")
        return False

def test_config():
    """Тестирование конфигурации"""
    print("\n⚙️ Проверка конфигурации...")
    
    try:
        from app.config import settings
        
        # Проверяем основные настройки
        if hasattr(settings, 'openai_model'):
            print(f"✅ OpenAI модель: {settings.openai_model}")
        else:
            print("❌ OpenAI модель не настроена")
            return False
        
        if hasattr(settings, 'max_comment_length'):
            print(f"✅ Максимальная длина комментария: {settings.max_comment_length}")
        else:
            print("❌ Максимальная длина не настроена")
            return False
        
        if hasattr(settings, 'comment_delay_min'):
            print(f"✅ Задержка между комментариями: {settings.comment_delay_min}-{settings.comment_delay_max}с")
        else:
            print("❌ Задержка не настроена")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка конфигурации: {e}")
        return False

def test_prompts():
    """Тестирование промптов"""
    print("\n📝 Проверка промптов...")
    
    try:
        from app.ai.prompts import CommentPrompts
        
        # Проверяем наличие промптов
        if hasattr(CommentPrompts, 'PROMPTS'):
            print(f"✅ Найдено {len(CommentPrompts.PROMPTS)} типов промптов")
        else:
            print("❌ Промпты не найдены")
            return False
        
        # Проверяем основные типы
        required_types = ['general', 'question', 'opinion', 'support', 'humor']
        for prompt_type in required_types:
            if prompt_type in CommentPrompts.PROMPTS:
                print(f"✅ Промпт '{prompt_type}' найден")
            else:
                print(f"❌ Промпт '{prompt_type}' отсутствует")
                return False
        
        # Тестируем генерацию промпта
        prompt = CommentPrompts.get_prompt(
            content="Тестовый контент",
            media_type="text",
            style="general",
            mood="neutral"
        )
        
        if prompt and "Тестовый контент" in prompt:
            print("✅ Генерация промпта работает")
        else:
            print("❌ Генерация промпта не работает")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка промптов: {e}")
        return False

def test_database_models():
    """Тестирование моделей базы данных"""
    print("\n🗄️ Проверка моделей базы данных...")
    
    try:
        from app.database.models import Channel, Post, Comment, Settings, Metrics
        
        # Проверяем, что модели определены
        models = [Channel, Post, Comment, Settings, Metrics]
        for model in models:
            if hasattr(model, '__tablename__'):
                print(f"✅ Модель {model.__name__} определена")
            else:
                print(f"❌ Модель {model.__name__} не определена")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка моделей БД: {e}")
        return False

def test_requirements():
    """Тестирование файла зависимостей"""
    print("\n📋 Проверка зависимостей...")
    
    try:
        with open('requirements.txt', 'r', encoding='utf-8') as f:
            requirements = f.read()
        
        # Проверяем основные зависимости
        required_packages = [
            'fastapi',
            'uvicorn',
            'python-telegram-bot',
            'sqlalchemy',
            'openai',
            'pydantic'
        ]
        
        missing_packages = []
        for package in required_packages:
            if package not in requirements:
                missing_packages.append(package)
        
        if missing_packages:
            print(f"❌ Отсутствуют зависимости: {missing_packages}")
            return False
        else:
            print("✅ Все основные зависимости присутствуют")
            return True
        
    except Exception as e:
        print(f"❌ Ошибка чтения requirements.txt: {e}")
        return False

def main():
    """Главная функция тестирования"""
    print("🚀 БАЗОВОЕ ТЕСТИРОВАНИЕ NEIROCOMMENT")
    print("="*60)
    
    tests = [
        ("Структура файлов", test_file_structure),
        ("Импорты", test_imports),
        ("Конфигурация", test_config),
        ("Промпты", test_prompts),
        ("Модели БД", test_database_models),
        ("Зависимости", test_requirements)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Ошибка в тесте '{test_name}': {e}")
            results.append((test_name, False))
    
    # Вывод сводки
    print("\n" + "="*60)
    print("📋 СВОДКА ТЕСТОВ")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\n📊 Результат: {passed}/{total} тестов пройдено ({(passed/total*100):.1f}%)")
    
    if passed == total:
        print("\n🎉 ВСЕ БАЗОВЫЕ ТЕСТЫ ПРОЙДЕНЫ!")
        print("💡 Система готова к настройке и запуску")
    else:
        print(f"\n⚠️  {total - passed} тестов провалено")
        print("🔧 Проверьте настройки и зависимости")

if __name__ == "__main__":
    main()
