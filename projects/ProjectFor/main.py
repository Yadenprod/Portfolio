#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Персональная система анализа спортивных ставок с ИИ
"""

import json
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List
import logging

# Импорты наших модулей
from config import Config
from data_collector import DataCollector
from prediction_model import SportsPredictionModel
from bankroll_manager import BankrollManager, BettingStrategy

# Настройка логирования
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Config.LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class BettingSystem:
    def __init__(self, bankroll: float = Config.INITIAL_BANKROLL, strategy: BettingStrategy = BettingStrategy.MARTINGALE):
        """Инициализация системы ставок"""
        self.data_collector = DataCollector()
        self.prediction_model = SportsPredictionModel()
        self.bankroll_manager = BankrollManager(bankroll, strategy)
        
        # Загружаем сохраненные данные
        self.bankroll_manager.load_from_file()
        
        logger.info(f"Система запущена. Банкролл: {self.bankroll_manager.current_bankroll:.2f} руб")
        logger.info(f"Стратегия: {strategy.value}")
    
    def analyze_match(self, match_id: str, sport: str = 'football') -> Dict:
        """Полный анализ матча"""
        logger.info(f"Анализируем матч {match_id} ({sport})")
        
        try:
            # Собираем данные о матче
            if sport == 'football':
                matches = self.data_collector.get_football_matches()
                match_data = next((m for m in matches if m['id'] == match_id), None)
            else:
                matches = self.data_collector.get_esports_matches()
                match_data = next((m for m in matches if m['id'] == match_id), None)
            
            if not match_data:
                logger.error(f"Матч {match_id} не найден")
                return {}
            
            # Собираем дополнительные данные
            home_team = match_data.get('home_team') or match_data.get('team1')
            away_team = match_data.get('away_team') or match_data.get('team2')
            
            analysis_data = {
                'match_info': match_data,
                'home_stats': self.data_collector.get_team_stats(home_team, sport),
                'away_stats': self.data_collector.get_team_stats(away_team, sport),
                'h2h': self.data_collector.get_head_to_head(home_team, away_team, sport),
                'odds': self.data_collector.get_odds_data(match_id, sport),
                'market_data': self.data_collector.get_market_data(match_id),
                'weather': self.data_collector.get_weather_data('Moscow', match_data['date'][:10]) if sport == 'football' else {}
            }
            
            # Получаем предсказание
            prediction = self.prediction_model.predict_match(analysis_data)
            
            # Анализируем ценность ставки
            bet_analysis = self._analyze_bet_value(prediction, analysis_data)
            
            result = {
                'match_data': analysis_data,
                'prediction': prediction,
                'bet_analysis': bet_analysis,
                'timestamp': datetime.now().isoformat()
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Ошибка при анализе матча {match_id}: {e}")
            return {}
    
    def _analyze_bet_value(self, prediction: Dict, match_data: Dict) -> Dict:
        """Анализирует ценность ставки"""
        confidence = prediction['confidence']
        predicted_outcome = prediction['prediction']
        probabilities = prediction['probabilities']
        
        odds = match_data['odds'].get('average_odds', {})
        
        # Маппинг исходов
        outcome_mapping = {
            'home_win': 'home',
            'away_win': 'away',
            'draw': 'draw'
        }
        
        analysis = {
            'recommended_action': 'skip',
            'reasoning': '',
            'value_bets': [],
            'confidence_level': 'low'
        }
        
        # Определяем уровень уверенности
        if confidence >= Config.HIGH_CONFIDENCE:
            analysis['confidence_level'] = 'high'
        elif confidence >= Config.MIN_CONFIDENCE:
            analysis['confidence_level'] = 'medium'
        
        # Проверяем value bets
        for outcome, prob in probabilities.items():
            odds_key = outcome_mapping.get(outcome, outcome)
            odds_value = odds.get(odds_key, 0)
            
            if odds_value > 0:
                implied_prob = 1 / odds_value
                expected_value = (prob * odds_value) - 1
                
                if expected_value > 0.05 and prob > implied_prob:  # Минимум 5% EV
                    analysis['value_bets'].append({
                        'outcome': outcome,
                        'our_probability': prob,
                        'implied_probability': implied_prob,
                        'odds': odds_value,
                        'expected_value': expected_value
                    })
        
        # Принимаем решение
        if confidence >= Config.MIN_CONFIDENCE and analysis['value_bets']:
            best_bet = max(analysis['value_bets'], key=lambda x: x['expected_value'])
            
            analysis['recommended_action'] = 'bet'
            analysis['recommended_outcome'] = best_bet['outcome']
            analysis['recommended_odds'] = best_bet['odds']
            analysis['reasoning'] = f"Высокая ценность ставки: EV={best_bet['expected_value']:.3f}"
        else:
            reasons = []
            if confidence < Config.MIN_CONFIDENCE:
                reasons.append(f"низкая уверенность ({confidence:.3f})")
            if not analysis['value_bets']:
                reasons.append("нет ценных ставок")
            
            analysis['reasoning'] = f"Пропуск: {', '.join(reasons)}"
        
        return analysis
    
    def place_bet_recommendation(self, match_analysis: Dict) -> Dict:
        """Рекомендует размер ставки"""
        bet_analysis = match_analysis['bet_analysis']
        
        if bet_analysis['recommended_action'] != 'bet':
            return {
                'action': 'skip',
                'reasoning': bet_analysis['reasoning']
            }
        
        # Рассчитываем размер ставки
        confidence = match_analysis['prediction']['confidence']
        odds = bet_analysis['recommended_odds']
        
        bet_size = self.bankroll_manager.calculate_bet_size(confidence, odds)
        
        # Проверяем лимиты
        if bet_size < Config.MIN_BET:
            bet_size = Config.MIN_BET
        elif bet_size > Config.MAX_BET:
            bet_size = Config.MAX_BET
        
        recommendation = {
            'action': 'bet',
            'outcome': bet_analysis['recommended_outcome'],
            'bet_size': bet_size,
            'odds': odds,
            'confidence': confidence,
            'expected_value': bet_analysis['value_bets'][0]['expected_value'],
            'bankroll_before': self.bankroll_manager.current_bankroll,
            'bet_percentage': (bet_size / self.bankroll_manager.current_bankroll) * 100,
            'strategy': self.bankroll_manager.strategy.value
        }
        
        return recommendation
    
    def execute_bet(self, match_analysis: Dict, bet_recommendation: Dict) -> Dict:
        """Выполняет ставку (сохраняет в истории)"""
        if bet_recommendation['action'] != 'bet':
            return {'status': 'skipped'}
        
        match_info = match_analysis['match_data']['match_info']
        
        bet_info = self.bankroll_manager.place_bet(
            bet_size=bet_recommendation['bet_size'],
            confidence=bet_recommendation['confidence'],
            odds=bet_recommendation['odds'],
            match_info=match_info,
            prediction=bet_recommendation['outcome']
        )
        
        # Сохраняем данные
        self.bankroll_manager.save_to_file()
        
        logger.info(f"Ставка размещена: {bet_info['bet_size']:.2f} руб на {bet_info['prediction']}")
        logger.info(f"Банкролл: {self.bankroll_manager.current_bankroll:.2f} руб")
        
        return {
            'status': 'placed',
            'bet_info': bet_info,
            'bet_id': len(self.bankroll_manager.bet_history) - 1
        }
    
    def resolve_bet(self, bet_id: int, won: bool) -> Dict:
        """Разрешает результат ставки"""
        try:
            result = self.bankroll_manager.resolve_bet(bet_id, won)
            self.bankroll_manager.save_to_file()
            
            logger.info(f"Ставка #{bet_id} {'выиграла' if won else 'проиграла'}")
            logger.info(f"Новый банкролл: {self.bankroll_manager.current_bankroll:.2f} руб")
            
            return result
            
        except Exception as e:
            logger.error(f"Ошибка при разрешении ставки #{bet_id}: {e}")
            return {}
    
    def get_today_matches(self, sport: str = 'football') -> List[Dict]:
        """Получает матчи на сегодня"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        if sport == 'football':
            matches = self.data_collector.get_football_matches(today)
        else:
            matches = self.data_collector.get_esports_matches()
        
        # Убеждаемся что возвращаем список, а не None
        return matches if matches is not None else []
    
    def analyze_all_today_matches(self, sport: str = 'football') -> List[Dict]:
        """Анализирует все матчи на сегодня"""
        matches = self.get_today_matches(sport)
        analyzed_matches = []
        
        # Убеждаемся что matches - это список
        if not matches:
            logger.info(f"Матчей для анализа не найдено ({sport})")
            return []
        
        for match in matches:
            match_id = match['id']
            analysis = self.analyze_match(match_id, sport)
            
            if analysis:
                recommendation = self.place_bet_recommendation(analysis)
                
                analyzed_matches.append({
                    'match': match,
                    'analysis': analysis,
                    'recommendation': recommendation
                })
        
        # Сортируем по ценности ставок
        analyzed_matches.sort(
            key=lambda x: x['recommendation'].get('expected_value', -1), 
            reverse=True
        )
        
        return analyzed_matches
    
    def get_statistics(self) -> Dict:
        """Возвращает статистику системы"""
        bankroll_stats = self.bankroll_manager.get_statistics()
        
        return {
            'bankroll_statistics': bankroll_stats,
            'system_info': {
                'strategy': self.bankroll_manager.strategy.value,
                'model_trained': self.prediction_model.is_trained,
                'last_updated': datetime.now().isoformat()
            }
        }
    
    def save_analysis_to_file(self, analysis: Dict, filename: str = None):
        """Сохраняет анализ в файл"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"analysis_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(analysis, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Анализ сохранен в {filename}")
        except Exception as e:
            logger.error(f"Ошибка при сохранении анализа: {e}")

def main():
    """Главная функция для демонстрации"""
    print("🎯 Персональная система спортивных ставок с ИИ")
    print("=" * 50)
    
    # Инициализируем систему
    system = BettingSystem(
        bankroll=Config.INITIAL_BANKROLL,
        strategy=BettingStrategy.MARTINGALE
    )
    
    print(f"💰 Текущий банкролл: {system.bankroll_manager.current_bankroll:.2f} руб")
    print(f"📊 Стратегия: {system.bankroll_manager.strategy.value}")
    print(f"🎯 Базовая ставка: {system.bankroll_manager.base_bet:.2f} руб")
    
    # Анализируем матчи на сегодня
    print("\n🔍 Анализ матчей на сегодня...")
    matches_analysis = system.analyze_all_today_matches('football')
    
    if matches_analysis:
        print(f"Найдено {len(matches_analysis)} матчей для анализа:")
        
        for i, match_data in enumerate(matches_analysis[:3], 1):  # Показываем топ-3
            match = match_data['match']
            recommendation = match_data['recommendation']
            
            print(f"\n{i}. {match.get('home_team', 'Team A')} vs {match.get('away_team', 'Team B')}")
            print(f"   Рекомендация: {recommendation['action']}")
            
            if recommendation['action'] == 'bet':
                print(f"   Ставка: {recommendation['bet_size']:.2f} руб на {recommendation['outcome']}")
                print(f"   Коэффициент: {recommendation['odds']:.2f}")
                print(f"   Ожидаемая прибыль: {recommendation['expected_value']:.3f}")
    else:
        print("Подходящих матчей не найдено.")
    
    print(f"\n📝 Логи сохраняются в {Config.LOG_FILE}")
    print("✅ Система готова к работе!")

if __name__ == "__main__":
    main() 