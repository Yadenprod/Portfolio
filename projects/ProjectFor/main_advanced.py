#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time
from datetime import datetime
from typing import Dict, List

# Импортируем новые модули
from real_data_api import RealDataAPI
from advanced_prediction_model import AdvancedPredictionModel
from smart_bankroll_manager import SmartBankrollManager, BettingStrategy

class AdvancedBettingSystem:
    """Продвинутая система ставок с реальными данными и ИИ"""
    
    def __init__(self):
        print("🚀 Запуск продвинутой системы ставок...")
        
        # Инициализируем компоненты
        self.data_api = RealDataAPI()
        self.prediction_model = AdvancedPredictionModel()
        self.bankroll_manager = SmartBankrollManager(
            initial_bankroll=50000.0,
            strategy=BettingStrategy.KELLY_CRITERION
        )
        
        # Настройки системы
        self.min_confidence = 0.4  # Минимальная уверенность для ставки
        self.min_value = 0.02      # Минимальное value для ставки
        self.max_daily_bets = 5    # Максимум ставок в день
        
        print("✅ Система инициализирована")
    
    def run_analysis(self):
        """Запускает полный анализ и поиск ставок"""
        print("\n" + "="*60)
        print("🎯 СИСТЕМА СПОРТИВНЫХ СТАВОК С ИИ")
        print("="*60)
        
        # Показываем настройки API
        self._show_api_setup_info()
        
        # Получаем матчи
        print("\n📡 Получение актуальных матчей...")
        matches = self.data_api.get_live_matches()
        
        if not matches:
            print("❌ Не удалось получить данные о матчах")
            return
        
        print(f"✅ Найдено {len(matches)} матчей для анализа")
        
        # Анализируем каждый матч
        betting_opportunities = []
        
        for i, match in enumerate(matches, 1):
            print(f"\n🔍 Анализ матча {i}/{len(matches)}: {match['home_team']} vs {match['away_team']}")
            
            # Получаем детальную статистику команд
            home_stats = self.data_api.get_team_detailed_stats(match['home_team'])
            away_stats = self.data_api.get_team_detailed_stats(match['away_team'])
            
            # Делаем прогноз
            prediction = self.prediction_model.predict_match_advanced(
                home_stats, away_stats, match
            )
            
            # Рассчитываем рекомендуемую ставку
            bet_recommendation = self.bankroll_manager.calculate_bet_size(
                prediction, match['odds']
            )
            
            # Проверяем критерии для ставки
            if self._is_bet_worthy(prediction, bet_recommendation):
                opportunity = {
                    'match': match,
                    'prediction': prediction,
                    'bet_recommendation': bet_recommendation,
                    'home_stats': home_stats,
                    'away_stats': away_stats
                }
                betting_opportunities.append(opportunity)
                
                print(f"   ✅ Найдена ставка: {bet_recommendation['bet_type']} "
                      f"({bet_recommendation['recommended_bet']:.0f} руб)")
            else:
                print(f"   ❌ Ставка не рекомендуется")
        
        # Показываем результаты
        self._display_results(betting_opportunities)
        
        # Показываем статистику банкролла
        self._display_bankroll_stats()
        
        # Интерактивное меню
        self._interactive_menu(betting_opportunities)
    
    def _show_api_setup_info(self):
        """Показывает информацию о настройке API"""
        print("\n📋 НАСТРОЙКА ИСТОЧНИКОВ ДАННЫХ:")
        print(self.data_api.get_setup_instructions())
    
    def _is_bet_worthy(self, prediction: Dict, bet_recommendation: Dict) -> bool:
        """Проверяет, стоит ли делать ставку"""
        if bet_recommendation['recommended_bet'] <= 0:
            return False
        
        confidence = prediction.get('confidence', 0)
        value_bets = prediction.get('value_bets', {})
        
        # Минимальные требования
        if confidence < self.min_confidence:
            return False
        
        if not value_bets:
            return False
        
        # Проверяем наличие достаточного value
        max_value = max(bet['value'] for bet in value_bets.values())
        if max_value < self.min_value:
            return False
        
        return True
    
    def _display_results(self, opportunities: List[Dict]):
        """Отображает результаты анализа"""
        print("\n" + "="*60)
        print("📊 РЕЗУЛЬТАТЫ АНАЛИЗА")
        print("="*60)
        
        if not opportunities:
            print("❌ Выгодных ставок не найдено")
            print("\nВозможные причины:")
            print("- Низкая уверенность модели")
            print("- Недостаточное value")
            print("- Превышены дневные лимиты")
            print("- Активирован стоп-лосс")
            return
        
        print(f"🎯 Найдено {len(opportunities)} выгодных ставок:")
        
        total_recommended_amount = 0
        
        for i, opp in enumerate(opportunities, 1):
            match = opp['match']
            prediction = opp['prediction']
            bet_rec = opp['bet_recommendation']
            
            print(f"\n#{i}. {match['home_team']} vs {match['away_team']}")
            print(f"    🏆 {match['competition']}")
            print(f"    ⏰ {match['date']}")
            print(f"    🎯 Прогноз: {prediction['prediction']} ({prediction['confidence']:.1%})")
            print(f"    💰 Ставка: {bet_rec['recommended_bet']:.0f} руб на {bet_rec['bet_type']}")
            print(f"    📊 Коэффициент: {bet_rec['odds']:.2f}")
            print(f"    📈 Ожидаемый ROI: {bet_rec['expected_roi']:.1f}%")
            print(f"    ⚠️ Риск: {bet_rec['risk_level']}")
            print(f"    🔍 Value: {bet_rec['value']:.3f}")
            
            # Показываем анализ команд
            home_stats = opp['home_stats']
            away_stats = opp['away_stats']
            
            print(f"    📋 {match['home_team']}: {home_stats.get('goals_per_game', 0):.1f} голов/игру, "
                  f"форма: {''.join(home_stats.get('recent_form', []))}")
            print(f"    📋 {match['away_team']}: {away_stats.get('goals_per_game', 0):.1f} голов/игру, "
                  f"форма: {''.join(away_stats.get('recent_form', []))}")
            
            total_recommended_amount += bet_rec['recommended_bet']
        
        print(f"\n💼 Общая сумма рекомендуемых ставок: {total_recommended_amount:.0f} руб")
        
        # Проверяем лимиты
        current_bankroll = self.bankroll_manager.current_bankroll
        percentage_of_bankroll = (total_recommended_amount / current_bankroll) * 100
        
        print(f"📊 Это составляет {percentage_of_bankroll:.1f}% от текущего банкролла")
        
        if percentage_of_bankroll > 15:
            print("⚠️ ВНИМАНИЕ: Большой процент от банкролла! Рассмотрите уменьшение ставок.")
    
    def _display_bankroll_stats(self):
        """Отображает статистику банкролла"""
        print("\n" + "="*60)
        print("💰 СТАТИСТИКА БАНКРОЛЛА")
        print("="*60)
        
        stats = self.bankroll_manager.get_statistics()
        
        print(f"💼 Текущий банкролл: {stats['current_bankroll']:,.0f} руб")
        print(f"🎯 Изначальный банкролл: {stats['initial_bankroll']:,.0f} руб")
        print(f"📈 Прибыль/Убыток: {stats['profit_loss']:+,.0f} руб ({stats['roi_percent']:+.1f}%)")
        print(f"🎲 Всего ставок: {stats['total_bets']}")
        print(f"🏆 Выигрышных: {stats['winning_bets']} ({stats['win_rate']:.1f}%)")
        print(f"🔥 Текущая серия: {stats['current_streak']:+d}")
        print(f"📉 Максимальная просадка: {stats['max_drawdown']:.1f}%")
        print(f"⚙️ Стратегия: {stats['strategy']}")
        
        if stats['total_bets'] > 0:
            print(f"💸 Общая сумма ставок: {stats['total_staked']:,.0f} руб")
            print(f"💰 Общие выплаты: {stats['total_return']:,.0f} руб")
            print(f"📊 Средняя ставка: {stats['average_bet']:,.0f} руб")
        
        # Показываем рекомендации
        recommendations = self.bankroll_manager.get_recommendations()
        if recommendations:
            print("\n📋 РЕКОМЕНДАЦИИ:")
            for rec in recommendations:
                print(f"   {rec}")
    
    def _interactive_menu(self, opportunities: List[Dict]):
        """Интерактивное меню для управления системой"""
        while True:
            print("\n" + "="*60)
            print("🎮 МЕНЮ УПРАВЛЕНИЯ")
            print("="*60)
            print("1. Разместить рекомендованные ставки")
            print("2. Изменить стратегию банкролла")
            print("3. Разрешить результат ставки")
            print("4. Посмотреть историю ставок")
            print("5. Запустить новый анализ")
            print("0. Выход")
            
            try:
                choice = input("\nВыберите действие (0-5): ").strip()
                
                if choice == "0":
                    print("👋 До свидания!")
                    break
                elif choice == "1":
                    self._place_recommended_bets(opportunities)
                elif choice == "2":
                    self._change_strategy()
                elif choice == "3":
                    self._resolve_bet()
                elif choice == "4":
                    self._show_bet_history()
                elif choice == "5":
                    self.run_analysis()
                    break
                else:
                    print("❌ Неверный выбор. Попробуйте снова.")
                    
            except KeyboardInterrupt:
                print("\n👋 До свидания!")
                break
            except Exception as e:
                print(f"❌ Ошибка: {e}")
    
    def _place_recommended_bets(self, opportunities: List[Dict]):
        """Размещает рекомендованные ставки"""
        if not opportunities:
            print("❌ Нет доступных ставок")
            return
        
        print(f"\n🎯 Размещение {len(opportunities)} ставок...")
        
        for i, opp in enumerate(opportunities, 1):
            match = opp['match']
            bet_rec = opp['bet_recommendation']
            
            success = self.bankroll_manager.place_bet(
                amount=bet_rec['recommended_bet'],
                bet_type=bet_rec['bet_type'],
                odds=bet_rec['odds'],
                match_info={
                    'home_team': match['home_team'],
                    'away_team': match['away_team'],
                    'competition': match['competition'],
                    'date': match['date']
                }
            )
            
            if success:
                print(f"✅ Ставка #{i} размещена")
            else:
                print(f"❌ Не удалось разместить ставку #{i}")
    
    def _change_strategy(self):
        """Меняет стратегию банкролла"""
        print("\n📊 ДОСТУПНЫЕ СТРАТЕГИИ:")
        strategies = list(BettingStrategy)
        
        for i, strategy in enumerate(strategies, 1):
            current = " (текущая)" if strategy == self.bankroll_manager.strategy else ""
            print(f"{i}. {strategy.value}{current}")
        
        try:
            choice = int(input(f"\nВыберите стратегию (1-{len(strategies)}): "))
            if 1 <= choice <= len(strategies):
                new_strategy = strategies[choice - 1]
                self.bankroll_manager.change_strategy(new_strategy)
            else:
                print("❌ Неверный выбор")
        except ValueError:
            print("❌ Введите число")
    
    def _resolve_bet(self):
        """Разрешает результат ставки"""
        pending_bets = [
            i for i, bet in enumerate(self.bankroll_manager.bet_history)
            if bet['status'] == 'pending'
        ]
        
        if not pending_bets:
            print("❌ Нет неразрешенных ставок")
            return
        
        print("\n🎲 НЕРАЗРЕШЕННЫЕ СТАВКИ:")
        for i, bet_index in enumerate(pending_bets, 1):
            bet = self.bankroll_manager.bet_history[bet_index]
            match_info = bet['match_info']
            print(f"{i}. {match_info['home_team']} vs {match_info['away_team']} - "
                  f"{bet['amount']:.0f} руб на {bet['bet_type']}")
        
        try:
            choice = int(input(f"\nВыберите ставку (1-{len(pending_bets)}): "))
            if 1 <= choice <= len(pending_bets):
                bet_index = pending_bets[choice - 1]
                
                result = input("Результат (w/l): ").lower().strip()
                if result in ['w', 'win', 'выигрыш', 'в']:
                    self.bankroll_manager.resolve_bet(bet_index, True)
                elif result in ['l', 'loss', 'проигрыш', 'п']:
                    self.bankroll_manager.resolve_bet(bet_index, False)
                else:
                    print("❌ Неверный результат")
            else:
                print("❌ Неверный выбор")
        except ValueError:
            print("❌ Введите число")
    
    def _show_bet_history(self):
        """Показывает историю ставок"""
        if not self.bankroll_manager.bet_history:
            print("❌ История ставок пуста")
            return
        
        print("\n📜 ИСТОРИЯ СТАВОК:")
        print("-" * 80)
        
        for i, bet in enumerate(self.bankroll_manager.bet_history[-10:], 1):  # Последние 10
            match_info = bet['match_info']
            timestamp = datetime.fromisoformat(bet['timestamp']).strftime("%d.%m.%Y %H:%M")
            
            status_emoji = {"pending": "⏳", "won": "🎉", "lost": "😞"}
            status = status_emoji.get(bet['status'], "❓")
            
            profit_loss = ""
            if bet['status'] == 'won':
                profit_loss = f" (+{bet['payout'] - bet['amount']:.0f} руб)"
            elif bet['status'] == 'lost':
                profit_loss = f" (-{bet['amount']:.0f} руб)"
            
            print(f"{status} {timestamp} | {match_info['home_team']} vs {match_info['away_team']}")
            print(f"    {bet['amount']:.0f} руб на {bet['bet_type']}, коэф. {bet['odds']:.2f}{profit_loss}")
            print()

def main():
    """Главная функция"""
    try:
        system = AdvancedBettingSystem()
        system.run_analysis()
    except KeyboardInterrupt:
        print("\n👋 Программа завершена пользователем")
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 