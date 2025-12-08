#!/usr/bin/env python3
"""
CaptchaSolver - Мощная система распознавания капчи
Главный файл для запуска системы
"""

import sys
import argparse
import logging
from pathlib import Path

# Добавляем текущую директорию в путь для импорта
sys.path.append(str(Path(__file__).parent))

from captcha_solver import CaptchaSolver, create_app
from captcha_solver.api import run_server

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description='CaptchaSolver - Система распознавания капчи')
    
    subparsers = parser.add_subparsers(dest='command', help='Доступные команды')
    
    # Команда запуска веб-сервера
    server_parser = subparsers.add_parser('server', help='Запуск веб-сервера')
    server_parser.add_argument('--host', default='127.0.0.1', help='Хост для запуска сервера')
    server_parser.add_argument('--port', type=int, default=8000, help='Порт для запуска сервера')
    server_parser.add_argument('--debug', action='store_true', help='Режим отладки')
    
    # Команда решения одного изображения
    solve_parser = subparsers.add_parser('solve', help='Решить одну капчу')
    solve_parser.add_argument('image', help='Путь к изображению капчи')
    solve_parser.add_argument('--no-preprocessing', action='store_true', help='Отключить предобработку')
    solve_parser.add_argument('--show-steps', action='store_true', help='Показать этапы обработки')
    solve_parser.add_argument('--no-consensus', action='store_true', help='Не использовать консенсус')
    solve_parser.add_argument('--model-path', help='Путь к обученной модели')
    
    # Команда обучения модели
    train_parser = subparsers.add_parser('train', help='Обучить собственную модель')
    train_parser.add_argument('--epochs', type=int, default=50, help='Количество эпох')
    train_parser.add_argument('--model-path', default='models/captcha_model', help='Путь для сохранения модели')
    train_parser.add_argument('--no-synthetic', action='store_true', help='Не использовать синтетические данные')
    
    # Команда тестирования
    test_parser = subparsers.add_parser('test', help='Тестировать на наборе изображений')
    test_parser.add_argument('test_dir', help='Директория с тестовыми изображениями')
    test_parser.add_argument('--model-path', help='Путь к обученной модели')
    
    # Команда демонстрации
    demo_parser = subparsers.add_parser('demo', help='Демонстрация возможностей')
    demo_parser.add_argument('--create-sample', action='store_true', help='Создать образец для тестирования')
    
    args = parser.parse_args()
    
    if args.command == 'server':
        logger.info("🚀 Запуск веб-сервера...")
        run_server(host=args.host, port=args.port, debug=args.debug)
        
    elif args.command == 'solve':
        logger.info(f"🔍 Решаем капчу: {args.image}")
        
        # Создаем решатель
        solver = CaptchaSolver(model_path=args.model_path)
        
        # Решаем капчу
        result = solver.solve(
            args.image,
            use_preprocessing=not args.no_preprocessing,
            show_steps=args.show_steps,
            use_consensus=not args.no_consensus
        )
        
        # Выводим результаты
        print("\n" + "="*50)
        print(f"🎯 РЕЗУЛЬТАТ: {result['final_result']}")
        print("="*50)
        print(f"⏱️  Время обработки: {result['solve_time']:.2f} сек")
        print(f"🔧 Предобработка: {'включена' if result['preprocessed'] else 'выключена'}")
        print(f"🤝 Консенсус: {'использован' if result['consensus_used'] else 'не использован'}")
        
        print("\n📊 Результаты по методам:")
        for method, res in result['all_results'].items():
            success = "✅" if res == result['final_result'] else "❌"
            print(f"  {method}: {res or 'ошибка'} {success}")
            
        # Показываем статистику
        stats = solver.get_stats()
        if stats['total_solved'] > 0:
            print(f"\n📈 Общая статистика: {stats['total_solved']} капч решено")
            
    elif args.command == 'train':
        logger.info("🎓 Начинаем обучение модели...")
        
        # Создаем директорию для модели
        model_dir = Path(args.model_path).parent
        model_dir.mkdir(parents=True, exist_ok=True)
        
        # Создаем решатель
        solver = CaptchaSolver()
        
        # Обучаем модель
        solver.train_custom_model(
            epochs=args.epochs,
            use_synthetic=not args.no_synthetic
        )
        
        # Сохраняем модель
        solver.model.save_models(args.model_path)
        
        print(f"✅ Модель обучена и сохранена в: {args.model_path}")
        
    elif args.command == 'test':
        logger.info(f"🧪 Тестируем на директории: {args.test_dir}")
        
        test_dir = Path(args.test_dir)
        if not test_dir.exists():
            print(f"❌ Директория не найдена: {test_dir}")
            return
            
        # Находим все изображения
        image_files = []
        for ext in ['*.png', '*.jpg', '*.jpeg', '*.bmp', '*.gif']:
            image_files.extend(test_dir.glob(ext))
            
        if not image_files:
            print("❌ Изображения не найдены в директории")
            return
            
        print(f"📁 Найдено {len(image_files)} изображений")
        
        # Создаем решатель
        solver = CaptchaSolver(model_path=args.model_path)
        
        # Тестируем каждое изображение
        results = []
        for img_file in image_files:
            print(f"Обрабатываем: {img_file.name}...")
            result = solver.solve(str(img_file), show_steps=False)
            results.append({
                'file': img_file.name,
                'result': result['final_result'],
                'time': result['solve_time']
            })
            
        # Выводим сводку
        print("\n📊 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ:")
        print("-" * 60)
        for r in results:
            print(f"{r['file']:<30} | {r['result']:<10} | {r['time']:.2f}с")
            
        total_time = sum(r['time'] for r in results)
        avg_time = total_time / len(results)
        
        print("-" * 60)
        print(f"Всего обработано: {len(results)} изображений")
        print(f"Общее время: {total_time:.2f} сек")
        print(f"Среднее время: {avg_time:.2f} сек/изображение")
        
        # Показываем общую статистику
        stats = solver.get_stats()
        print(f"\n📈 Статистика решателя:")
        for key, value in stats.items():
            if 'percentage' in key:
                print(f"  {key}: {value}%")
                
    elif args.command == 'demo':
        if args.create_sample:
            logger.info("🎨 Создаем образцы для демонстрации...")
            create_demo_samples()
        else:
            logger.info("🎭 Запуск демонстрации...")
            run_demo()
            
    else:
        parser.print_help()

def create_demo_samples():
    """Создание образцов для демонстрации"""
    from captcha_solver.models import CaptchaModel
    import cv2
    import os
    
    # Создаем директорию для образцов
    demo_dir = Path("demo_samples")
    demo_dir.mkdir(exist_ok=True)
    
    # Создаем модель для генерации
    model = CaptchaModel()
    
    # Генерируем несколько образцов
    samples = ['12345', '67890', '13579', '24680', '98765']
    
    print("Создаем образцы капчи...")
    for i, text in enumerate(samples):
        # Создаем изображение
        img = model._create_text_image(text)
        
        # Добавляем шум и искажения
        img_noisy = model._add_noise_and_distortions(img)
        
        # Сохраняем
        filename = demo_dir / f"sample_{i+1}_{text}.png"
        cv2.imwrite(str(filename), img_noisy)
        print(f"  ✅ {filename}")
        
    print(f"\n🎉 Создано {len(samples)} образцов в директории: {demo_dir}")
    print("Теперь вы можете протестировать их командой:")
    print(f"python main.py test {demo_dir}")

def run_demo():
    """Запуск интерактивной демонстрации"""
    print("🎭 ДЕМОНСТРАЦИЯ CaptchaSolver")
    print("=" * 50)
    
    # Проверяем наличие образцов
    demo_dir = Path("demo_samples")
    if not demo_dir.exists() or not list(demo_dir.glob("*.png")):
        print("📁 Образцы для демо не найдены.")
        print("Создаем их автоматически...")
        create_demo_samples()
        
    # Запускаем тестирование на образцах
    print("\n🧪 Тестируем на созданных образцах...")
    solver = CaptchaSolver()
    
    for sample_file in demo_dir.glob("*.png"):
        print(f"\n🔍 Обрабатываем: {sample_file.name}")
        
        # Извлекаем ожидаемый результат из имени файла
        expected = sample_file.stem.split('_')[-1]
        
        # Решаем
        result = solver.solve(str(sample_file), show_steps=False)
        
        # Сравниваем
        success = result['final_result'] == expected
        status = "✅ УСПЕХ" if success else "❌ ОШИБКА"
        
        print(f"  Ожидалось: {expected}")
        print(f"  Получено:  {result['final_result']}")
        print(f"  Время:     {result['solve_time']:.2f}с")
        print(f"  Статус:    {status}")
        
    print(f"\n🏁 Демонстрация завершена!")
    print("Для запуска веб-интерфейса используйте:")
    print("python main.py server")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Работа прервана пользователем")
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}")
        sys.exit(1) 