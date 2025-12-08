"""
Тестирование системы NeiroComment
"""
import asyncio
import os
import sys
import tempfile
from datetime import datetime

# Добавляем путь к приложению
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.config import settings
from app.ai.generator import CommentGenerator
from app.ai.prompts import CommentPrompts
from app.monitoring.metrics import MetricsCollector, HealthChecker
from app.database.connection import init_db, SessionLocal
from app.database.models import Channel, Post, Comment


class TestNeiroComment:
    """Класс для тестирования системы"""
    
    def __init__(self):
        self.test_results = []
        self.generator = CommentGenerator()
        self.metrics_collector = MetricsCollector()
        self.health_checker = HealthChecker()
    
    def log_test(self, test_name: str, success: bool, message: str = ""):
        """Логирование результата теста"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        self.test_results.append({
            "test": test_name,
            "success": success,
            "message": message
        })
    
    async def test_ai_generator(self):
        """Тестирование AI генератора"""
        print("\n🤖 Тестирование AI генератора...")
        
        try:
            # Тест 1: Простая генерация
            comment = await self.generator.generate_comment(
                content="Новости о криптовалютах сегодня",
                media_type="text"
            )
            
            if comment and len(comment) > 0:
                self.log_test("AI Generator - Простая генерация", True, f"Сгенерирован комментарий: {comment[:50]}...")
            else:
                self.log_test("AI Generator - Простая генерация", False, "Не удалось сгенерировать комментарий")
            
            # Тест 2: Генерация с разными стилями
            styles = ["general", "opinion", "question", "humor"]
            for style in styles:
                comment = await self.generator.generate_comment(
                    content="Технологии искусственного интеллекта развиваются",
                    media_type="text",
                    style=style
                )
                
                if comment:
                    self.log_test(f"AI Generator - Стиль {style}", True, f"Комментарий: {comment[:30]}...")
                else:
                    self.log_test(f"AI Generator - Стиль {style}", False, "Не удалось сгенерировать")
            
            # Тест 3: Анализ типа контента
            content_type = await self.generator.analyze_content_type("Биткоин достиг новых высот")
            if content_type == "crypto":
                self.log_test("AI Generator - Анализ контента", True, f"Определен тип: {content_type}")
            else:
                self.log_test("AI Generator - Анализ контента", False, f"Ожидался 'crypto', получен '{content_type}'")
                
        except Exception as e:
            self.log_test("AI Generator - Общий тест", False, f"Ошибка: {str(e)}")
    
    def test_prompts(self):
        """Тестирование промптов"""
        print("\n📝 Тестирование промптов...")
        
        try:
            # Тест 1: Получение промпта
            prompt = CommentPrompts.get_prompt(
                content="Новости о технологиях",
                media_type="text",
                style="general",
                mood="positive"
            )
            
            if prompt and "Новости о технологиях" in prompt:
                self.log_test("Prompts - Получение промпта", True, "Промпт сгенерирован корректно")
            else:
                self.log_test("Prompts - Получение промпта", False, "Промпт не содержит ожидаемый контент")
            
            # Тест 2: Случайные стили
            random_style = CommentPrompts.get_random_style()
            if random_style in CommentPrompts.PROMPTS:
                self.log_test("Prompts - Случайный стиль", True, f"Получен стиль: {random_style}")
            else:
                self.log_test("Prompts - Случайный стиль", False, f"Неизвестный стиль: {random_style}")
            
            # Тест 3: Случайное настроение
            random_mood = CommentPrompts.get_random_mood()
            if random_mood in CommentPrompts.MOOD_PROMPTS:
                self.log_test("Prompts - Случайное настроение", True, f"Получено настроение: {random_mood}")
            else:
                self.log_test("Prompts - Случайное настроение", False, f"Неизвестное настроение: {random_mood}")
                
        except Exception as e:
            self.log_test("Prompts - Общий тест", False, f"Ошибка: {str(e)}")
    
    async def test_database(self):
        """Тестирование базы данных"""
        print("\n🗄️ Тестирование базы данных...")
        
        try:
            # Инициализация БД
            await init_db()
            self.log_test("Database - Инициализация", True, "База данных инициализирована")
            
            # Тест создания канала
            db = SessionLocal()
            test_channel = Channel(
                channel_id="test_channel_123",
                username="test_channel",
                title="Test Channel",
                description="Тестовый канал",
                is_active=True,
                comment_enabled=True
            )
            
            db.add(test_channel)
            db.commit()
            
            # Проверка создания
            created_channel = db.query(Channel).filter(Channel.channel_id == "test_channel_123").first()
            if created_channel:
                self.log_test("Database - Создание канала", True, f"Канал создан: {created_channel.title}")
            else:
                self.log_test("Database - Создание канала", False, "Канал не найден после создания")
            
            # Тест создания поста
            test_post = Post(
                post_id="test_post_456",
                channel_id="test_channel_123",
                content="Тестовый пост для проверки системы",
                media_type="text",
                published_at=datetime.now()
            )
            
            db.add(test_post)
            db.commit()
            
            # Проверка создания поста
            created_post = db.query(Post).filter(Post.post_id == "test_post_456").first()
            if created_post:
                self.log_test("Database - Создание поста", True, f"Пост создан: {created_post.content[:30]}...")
            else:
                self.log_test("Database - Создание поста", False, "Пост не найден после создания")
            
            # Тест создания комментария
            test_comment = Comment(
                channel_id="test_channel_123",
                post_id="test_post_456",
                content="Тестовый комментарий",
                ai_generated=True,
                status="sent",
                sent_at=datetime.now()
            )
            
            db.add(test_comment)
            db.commit()
            
            # Проверка создания комментария
            created_comment = db.query(Comment).filter(Comment.content == "Тестовый комментарий").first()
            if created_comment:
                self.log_test("Database - Создание комментария", True, f"Комментарий создан: {created_comment.content}")
            else:
                self.log_test("Database - Создание комментария", False, "Комментарий не найден после создания")
            
            # Очистка тестовых данных
            db.delete(created_comment)
            db.delete(created_post)
            db.delete(created_channel)
            db.commit()
            
            self.log_test("Database - Очистка данных", True, "Тестовые данные удалены")
            
        except Exception as e:
            self.log_test("Database - Общий тест", False, f"Ошибка: {str(e)}")
        finally:
            db.close()
    
    def test_metrics(self):
        """Тестирование метрик"""
        print("\n📊 Тестирование метрик...")
        
        try:
            # Тест сбора метрик
            metrics = self.metrics_collector.collect_metrics()
            
            if metrics and hasattr(metrics, 'total_channels'):
                self.log_test("Metrics - Сбор метрик", True, f"Метрики собраны: {metrics.total_channels} каналов")
            else:
                self.log_test("Metrics - Сбор метрик", False, "Не удалось собрать метрики")
            
            # Тест записи успеха
            self.metrics_collector.record_success()
            self.log_test("Metrics - Запись успеха", True, "Успех записан")
            
            # Тест записи ошибки
            self.metrics_collector.record_error()
            self.log_test("Metrics - Запись ошибки", True, "Ошибка записана")
            
            # Тест сводки метрик
            summary = self.metrics_collector.get_metrics_summary()
            if summary and 'timestamp' in summary:
                self.log_test("Metrics - Сводка метрик", True, "Сводка метрик получена")
            else:
                self.log_test("Metrics - Сводка метрик", False, "Не удалось получить сводку")
                
        except Exception as e:
            self.log_test("Metrics - Общий тест", False, f"Ошибка: {str(e)}")
    
    def test_health_check(self):
        """Тестирование проверки здоровья"""
        print("\n🏥 Тестирование проверки здоровья...")
        
        try:
            health = self.health_checker.check_health()
            
            if health and 'status' in health:
                self.log_test("Health Check - Проверка здоровья", True, f"Статус: {health['status']}")
                
                # Проверка отдельных компонентов
                if 'checks' in health:
                    for check_name, check_result in health['checks'].items():
                        if check_result['status'] == 'healthy':
                            self.log_test(f"Health Check - {check_name}", True, check_result['message'])
                        else:
                            self.log_test(f"Health Check - {check_name}", False, check_result['message'])
                else:
                    self.log_test("Health Check - Компоненты", False, "Информация о компонентах отсутствует")
            else:
                self.log_test("Health Check - Общий тест", False, "Не удалось получить статус здоровья")
                
        except Exception as e:
            self.log_test("Health Check - Общий тест", False, f"Ошибка: {str(e)}")
    
    def test_config(self):
        """Тестирование конфигурации"""
        print("\n⚙️ Тестирование конфигурации...")
        
        try:
            # Проверка основных настроек
            if hasattr(settings, 'openai_model'):
                self.log_test("Config - OpenAI модель", True, f"Модель: {settings.openai_model}")
            else:
                self.log_test("Config - OpenAI модель", False, "Модель не настроена")
            
            if hasattr(settings, 'max_comment_length'):
                self.log_test("Config - Максимальная длина", True, f"Длина: {settings.max_comment_length}")
            else:
                self.log_test("Config - Максимальная длина", False, "Длина не настроена")
            
            if hasattr(settings, 'comment_delay_min'):
                self.log_test("Config - Задержка", True, f"Задержка: {settings.comment_delay_min}-{settings.comment_delay_max}с")
            else:
                self.log_test("Config - Задержка", False, "Задержка не настроена")
                
        except Exception as e:
            self.log_test("Config - Общий тест", False, f"Ошибка: {str(e)}")
    
    def print_summary(self):
        """Вывод сводки тестов"""
        print("\n" + "="*60)
        print("📋 СВОДКА ТЕСТОВ")
        print("="*60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"Всего тестов: {total_tests}")
        print(f"✅ Пройдено: {passed_tests}")
        print(f"❌ Провалено: {failed_tests}")
        print(f"📊 Успешность: {(passed_tests/total_tests*100):.1f}%")
        
        if failed_tests > 0:
            print("\n❌ ПРОВАЛЕННЫЕ ТЕСТЫ:")
            for result in self.test_results:
                if not result['success']:
                    print(f"  - {result['test']}: {result['message']}")
        
        print("\n" + "="*60)
        
        if failed_tests == 0:
            print("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        else:
            print(f"⚠️  {failed_tests} тестов провалено. Проверьте настройки.")
    
    async def run_all_tests(self):
        """Запуск всех тестов"""
        print("🚀 ЗАПУСК ТЕСТИРОВАНИЯ NEIROCOMMENT")
        print("="*60)
        
        # Запуск тестов
        await self.test_ai_generator()
        self.test_prompts()
        await self.test_database()
        self.test_metrics()
        self.test_health_check()
        self.test_config()
        
        # Вывод сводки
        self.print_summary()


async def main():
    """Главная функция тестирования"""
    # Создаем временный файл .env для тестов
    test_env_content = """
# Test Configuration
TELEGRAM_BOT_TOKEN=test_token
TELEGRAM_API_ID=12345
TELEGRAM_API_HASH=test_hash
OPENAI_API_KEY=test_key
OPENAI_MODEL=gpt-3.5-turbo
DATABASE_URL=sqlite:///./test_neirocomment.db
SECRET_KEY=test_secret_key
DEBUG=True
HOST=0.0.0.0
PORT=8000
ENABLE_METRICS=True
LOG_LEVEL=INFO
MAX_COMMENT_LENGTH=200
COMMENT_DELAY_MIN=30
COMMENT_DELAY_MAX=300
MAX_COMMENTS_PER_HOUR=10
MAX_COMMENTS_PER_DAY=50
"""
    
    # Записываем тестовый .env файл
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(test_env_content)
    
    print("📝 Создан тестовый .env файл")
    
    # Запуск тестов
    tester = TestNeiroComment()
    await tester.run_all_tests()
    
    # Очистка тестового .env файла
    if os.path.exists('.env'):
        os.remove('.env')
        print("\n🧹 Тестовый .env файл удален")


if __name__ == "__main__":
    asyncio.run(main())
