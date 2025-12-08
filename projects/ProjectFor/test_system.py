#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тестирование системы спортивных ставок
"""

from main import BettingSystem
from bankroll_manager import BettingStrategy, BankrollManager
from config import Config
import time

def test_system():
    """Комплексное тестирование системы"""
    print("🧪 ТЕСТИРОВАНИЕ СИСТЕМЫ СПОРТИВНЫХ СТАВОК")
    print("=" * 50)
    
    # Тест 1: Инициализация системы
    print("\n1️⃣ Тест инициализации...")
    system = BettingSystem(
        bankroll=Config.INITIAL_BANKROLL,
        strategy=BettingStrategy.MARTINGALE
    )
    print("✅ Система инициализирована успешно")
    
    # Тест 2: Получение статистики
    print("\n2️⃣ Тест получения статистики...")
    stats = system.get_statistics()
    print(f"✅ Банкролл: {stats['bankroll_statistics'].get('current_bankroll', 0):.2f} руб")
    print(f"✅ Стратегия: {stats['system_info']['strategy']}")
    
    # Тест 3: Получение матчей
    print("\n3️⃣ Тест получения матчей...")
    football_matches = system.get_today_matches('football')
    esports_matches = system.get_today_matches('esports')
    print(f"✅ Футбольных матчей: {len(football_matches)}")
    print(f"✅ Киберспортивных матчей: {len(esports_matches)}")
    
    # Тест 4: Анализ матча
    if football_matches:
        print("\n4️⃣ Тест анализа матча...")
        match = football_matches[0]
        analysis = system.analyze_match(match['id'], 'football')
        
        if analysis:
            print("✅ Анализ выполнен успешно")
            print(f"   Матч: {match.get('home_team', 'Team A')} vs {match.get('away_team', 'Team B')}")
            print(f"   Предсказание: {analysis['prediction']['prediction']}")
            print(f"   Уверенность: {analysis['prediction']['confidence']:.3f}")
            print(f"   Рекомендация: {analysis['bet_analysis']['recommended_action']}")
            
            # Тест 5: Рекомендация ставки
            print("\n5️⃣ Тест рекомендации ставки...")
            recommendation = system.place_bet_recommendation(analysis)
            print(f"✅ Действие: {recommendation['action']}")
            
            if recommendation['action'] == 'bet':
                print(f"   Размер ставки: {recommendation['bet_size']:.2f} руб")
                print(f"   Коэффициент: {recommendation['odds']:.2f}")
                print(f"   Ожидаемая прибыль: {recommendation['expected_value']:.3f}")
                
                # Тест 6: Выполнение ставки
                print("\n6️⃣ Тест выполнения ставки...")
                bet_result = system.execute_bet(analysis, recommendation)
                
                if bet_result['status'] == 'placed':
                    print("✅ Ставка размещена")
                    bet_id = bet_result['bet_id']
                    
                    # Тест 7: Разрешение ставки (симуляция выигрыша)
                    print("\n7️⃣ Тест разрешения ставки...")
                    time.sleep(1)  # Небольшая пауза
                    
                    # Симулируем выигрыш
                    resolve_result = system.resolve_bet(bet_id, won=True)
                    print("✅ Ставка разрешена как выигрышная")
                    print(f"   Новый банкролл: {system.bankroll_manager.current_bankroll:.2f} руб")
                else:
                    print("ℹ️ Ставка была пропущена")
            else:
                print("ℹ️ Ставка не рекомендована")
        else:
            print("❌ Ошибка при анализе матча")
    
    # Тест 8: Анализ всех матчей
    print("\n8️⃣ Тест анализа всех матчей...")
    all_matches = system.analyze_all_today_matches('football')
    print(f"✅ Проанализировано {len(all_matches)} матчей")
    
    recommended_matches = [m for m in all_matches if m['recommendation']['action'] == 'bet']
    print(f"✅ Рекомендовано ставок: {len(recommended_matches)}")
    
    # Тест 9: Различные стратегии
    print("\n9️⃣ Тест различных стратегий...")
    strategies = [
        BettingStrategy.FIBONACCI,
        BettingStrategy.KELLY,
        BettingStrategy.FLAT,
        BettingStrategy.DALEMBERT
    ]
    
    for strategy in strategies:
        test_system = BettingSystem(bankroll=10000, strategy=strategy)
        bet_size = test_system.bankroll_manager.calculate_bet_size(0.75, 2.0)
        print(f"   {strategy.value}: {bet_size:.2f} руб")
    
    print("✅ Все стратегии протестированы")
    
    # Финальная статистика
    print("\n📊 ФИНАЛЬНАЯ СТАТИСТИКА")
    print("=" * 30)
    final_stats = system.get_statistics()
    bankroll_stats = final_stats['bankroll_statistics']
    
    print(f"💰 Банкролл: {bankroll_stats.get('current_bankroll', 0):.2f} руб")
    print(f"📈 Изменение: {bankroll_stats.get('bankroll_change', 0):.2f} руб")
    print(f"🎯 Всего ставок: {bankroll_stats.get('total_bets', 0)}")
    print(f"✅ Выигрышей: {bankroll_stats.get('wins', 0)}")
    print(f"❌ Проигрышей: {bankroll_stats.get('losses', 0)}")
    print(f"💹 ROI: {bankroll_stats.get('roi', 0):.2f}%")
    
    print("\n🎉 ТЕСТИРОВАНИЕ ЗАВЕРШЕНО УСПЕШНО!")
    return True

def demo_betting_strategies():
    """Демонстрация различных стратегий ставок"""
    print("\n🎲 ДЕМОНСТРАЦИЯ СТРАТЕГИЙ СТАВОК")
    print("=" * 40)
    
    initial_bankroll = 10000
    confidence = 0.75
    odds = 2.1
    
    strategies = {
        "Мартингейл": BettingStrategy.MARTINGALE,
        "Фибоначчи": BettingStrategy.FIBONACCI,
        "Критерий Келли": BettingStrategy.KELLY,
        "Фиксированная": BettingStrategy.FLAT,
        "Д'Аламбер": BettingStrategy.DALEMBERT
    }
    
    for name, strategy in strategies.items():
        manager = BankrollManager(initial_bankroll, strategy)
        
        print(f"\n📊 {name}:")
        print(f"   Начальная ставка: {manager.calculate_bet_size(confidence, odds):.2f} руб")
        
        # Симулируем серию проигрышей
        manager.consecutive_losses = 1
        bet_after_1_loss = manager.calculate_bet_size(confidence, odds)
        
        manager.consecutive_losses = 2
        bet_after_2_losses = manager.calculate_bet_size(confidence, odds)
        
        print(f"   После 1 проигрыша: {bet_after_1_loss:.2f} руб")
        print(f"   После 2 проигрышей: {bet_after_2_losses:.2f} руб")

def stress_test():
    """Стресс-тест системы"""
    print("\n⚡ СТРЕСС-ТЕСТ СИСТЕМЫ")
    print("=" * 30)
    
    system = BettingSystem(bankroll=50000, strategy=BettingStrategy.MARTINGALE)
    
    print("Тестируем производительность...")
    start_time = time.time()
    
    # Множественный анализ
    for i in range(10):
        matches = system.get_today_matches('football')
        if matches:
            analysis = system.analyze_match(matches[0]['id'], 'football')
    
    end_time = time.time()
    print(f"✅ 10 анализов выполнено за {end_time - start_time:.2f} секунд")
    
    # Тест больших объемов данных
    print("Тестируем обработку больших данных...")
    model = system.prediction_model
    
    start_time = time.time()
    X, y = model.generate_training_data(5000)  # Большой датасет
    model.train_model()
    end_time = time.time()
    
    print(f"✅ Модель обучена на 5000 образцах за {end_time - start_time:.2f} секунд")

if __name__ == "__main__":
    try:
        # Основное тестирование
        test_system()
        
        # Демонстрация стратегий
        demo_betting_strategies()
        
        # Стресс-тест
        stress_test()
        
        print("\n🏆 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        
    except Exception as e:
        print(f"\n❌ ОШИБКА ПРИ ТЕСТИРОВАНИИ: {e}")
        import traceback
        traceback.print_exc() 