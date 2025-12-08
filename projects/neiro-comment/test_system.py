#!/usr/bin/env python3
"""
Простой тест системы NeiroComment
"""
import sys
import os

def test_imports():
    """Тестирование импортов основных модулей"""
    print("🔍 Тестирование импортов...")
    
    try:
        # Добавляем путь к приложению
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        # Тестируем импорты
        print("  📦 Импорт app.config...")
        from app.config import settings
        print("  ✅ app.config импортирован успешно")
        
        print("  📦 Импорт app.database.models...")
        from app.database.models import Channel, Post, Comment
        print("  ✅ app.database.models импортирован успешно")
        
        print("  📦 Импорт app.ai.prompts...")
        from app.ai.prompts import CommentPrompts
        print("  ✅ app.ai.prompts импортирован успешно")
        
        print("  📦 Импорт app.monitoring.metrics...")
        from app.monitoring.metrics import MetricsCollector
        print("  ✅ app.monitoring.metrics импортирован успешно")
        
        return True
        
    except ImportError as e:
        print(f"  ❌ Ошибка импорта: {e}")
        return False
    except Exception as e:
        print(f"  ❌ Неожиданная ошибка: {e}")
        return False

def test_config():
    """Тестирование конфигурации"""
    print("\n⚙️ Тестирование конфигурации...")
    
    try:
        from app.config import settings
        
        print(f"  🤖 OpenAI модель: {settings.openai_model}")
        print(f"  📏 Максимальная длина: {settings.max_comment_length}")
        print(f"  ⏱️ Задержка: {settings.comment_delay_min}-{settings.comment_delay_max}с")
        print(f"  🚀 Хост: {settings.host}:{settings.port}")
        print(f"  🐛 Debug режим: {settings.debug}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Ошибка конфигурации: {e}")
        return False

def test_prompts():
    """Тестирование промптов"""
    print("\n📝 Тестирование промптов...")
    
    try:
        from app.ai.prompts import CommentPrompts
        
        # Проверяем количество промптов
        prompt_count = len(CommentPrompts.PROMPTS)
        print(f"  📊 Найдено {prompt_count} типов промптов")
        
        # Проверяем основные типы
        required_types = ['general', 'question', 'opinion', 'support', 'humor']
        for prompt_type in required_types:
            if prompt_type in CommentPrompts.PROMPTS:
                print(f"  ✅ Промпт '{prompt_type}' найден")
            else:
                print(f"  ❌ Промпт '{prompt_type}' отсутствует")
                return False
        
        # Тестируем генерацию промпта
        prompt = CommentPrompts.get_prompt(
            content="Тестовый контент для проверки",
            media_type="text",
            style="general",
            mood="positive"
        )
        
        if prompt and "Тестовый контент для проверки" in prompt:
            print("  ✅ Генерация промпта работает корректно")
        else:
            print("  ❌ Генерация промпта не работает")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ Ошибка промптов: {e}")
        return False

def test_database_models():
    """Тестирование моделей базы данных"""
    print("\n🗄️ Тестирование моделей базы данных...")
    
    try:
        from app.database.models import Channel, Post, Comment, Settings, Metrics
        
        # Проверяем модели
        models = [
            ("Channel", Channel),
            ("Post", Post),
            ("Comment", Comment),
            ("Settings", Settings),
            ("Metrics", Metrics)
        ]
        
        for model_name, model_class in models:
            if hasattr(model_class, '__tablename__'):
                print(f"  ✅ Модель {model_name} определена (таблица: {model_class.__tablename__})")
            else:
                print(f"  ❌ Модель {model_name} не определена")
                return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ Ошибка моделей БД: {e}")
        return False

def test_file_structure():
    """Тестирование структуры файлов"""
    print("\n📁 Тестирование структуры файлов...")
    
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
        "main.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path} - отсутствует")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"  ⚠️ Отсутствуют файлы: {len(missing_files)}")
        return False
    else:
        print(f"  ✅ Все {len(required_files)} файлов присутствуют")
        return True

def main():
    """Главная функция тестирования"""
    print("🚀 ТЕСТИРОВАНИЕ СИСТЕМЫ NEIROCOMMENT")
    print("=" * 60)
    
    tests = [
        ("Структура файлов", test_file_structure),
        ("Импорты модулей", test_imports),
        ("Конфигурация", test_config),
        ("Промпты AI", test_prompts),
        ("Модели БД", test_database_models)
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
    print("\n" + "=" * 60)
    print("📋 СВОДКА ТЕСТОВ")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\n📊 Результат: {passed}/{total} тестов пройдено ({(passed/total*100):.1f}%)")
    
    if passed == total:
        print("\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        print("💡 Система готова к настройке и запуску")
        print("\n🚀 Следующие шаги:")
        print("1. Настройте .env файл с реальными токенами")
        print("2. Установите зависимости: pip install -r requirements.txt")
        print("3. Запустите приложение: python main.py")
        print("4. Откройте веб-интерфейс: http://localhost:8000")
    else:
        print(f"\n⚠️ {total - passed} тестов провалено")
        print("🔧 Проверьте настройки и зависимости")

if __name__ == "__main__":
    main()
