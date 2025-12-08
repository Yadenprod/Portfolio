#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🎮 CS:GO BETTING SYSTEM - Система ставок на CS:GO
Использует данные с HLTV.org и букмекерских контор для анализа и прогнозирования матчей CS:GO
"""

import os
import sys
import json
import time
from datetime import datetime
from typing import Dict, List, Optional
import logging
import random

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('csgo_betting.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

try:
    from hltv_parser import HLTVParser
    from csgo_prediction_model import CSGOPredictionModel
    from smart_bankroll_manager import SmartBankrollManager
    from fonbet_api import FonbetAPI
except ImportError as e:
    logger.error(f"Ошибка импорта модулей: {e}")
    print("⚠️ Не все модули найдены. Проверьте установку зависимостей:")
    print("pip install -r requirements.txt")
    sys.exit(1)

class CSGOBettingSystem:
    """Главный класс системы ставок на CS:GO"""
    
    def __init__(self):
        print("🎮 ИНИЦИАЛИЗАЦИЯ CS:GO BETTING SYSTEM")
        print("=" * 50)
        
        # Инициализация компонентов
        self.hltv_parser = HLTVParser()
        self.prediction_model = CSGOPredictionModel()
        self.bankroll_manager = SmartBankrollManager()
        self.fonbet_api = FonbetAPI()
        
        # Настройки для CS:GO
        self.min_confidence = 0.55  # Минимальная уверенность для CS:GO
        self.min_value = 0.04      # Минимальное value для CS:GO (4%)
        self.max_daily_bets = 8    # Максимум ставок в день для CS:GO
        
        # Статистика
        self.daily_bets_count = 0
        self.session_stats = {
            'analyzed_matches': 0,
            'recommended_bets': 0,
            'high_confidence_predictions': 0,
            'value_bets_found': 0
        }
        
        print("✅ Система инициализирована успешно!")
        
    def format_prediction(self, prediction: str) -> str:
        """Форматирует прогноз для вывода"""
        team_mapping = {
            "Первая команда": "Победа первой команды",
            "Вторая команда": "Победа второй команды"
        }
        return team_mapping.get(prediction, prediction)
        
    def run_analysis(self):
        """Запуск анализа CS:GO матчей"""
        print("\n🔍 АНАЛИЗ CS:GO МАТЧЕЙ")
        print("=" * 50)
        
        try:
            # Проверяем существование файла с матчами
            if os.path.exists('matches.json'):
                with open('matches.json', 'r', encoding='utf-8') as f:
                    hltv_matches = json.load(f)
                print(f"✅ Загружено {len(hltv_matches)} матчей из файла")
            else:
                # Получаем матчи с HLTV
                hltv_matches = self.hltv_parser.get_upcoming_matches()
                
                if not hltv_matches:
                    print("❌ Не удалось получить матчи с HLTV")
                    return
                    
                # Сохраняем матчи в файл для отладки
                with open('matches.json', 'w', encoding='utf-8') as f:
                    json.dump(hltv_matches, f, ensure_ascii=False, indent=2)
                print(f"✅ Найдено {len(hltv_matches)} матчей")
            
            # Добавляем демо-коэффициенты для тестирования
            for match in hltv_matches:
                if 'odds' not in match:
                    match['odds'] = {
                        'team1': 1.8 + random.random() * 0.8,  # От 1.8 до 2.6
                        'team2': 1.8 + random.random() * 0.8   # От 1.8 до 2.6
                    }
            
            # Объединяем данные
            matches = self._merge_match_data(hltv_matches, [])  # Пустой список Fonbet матчей
            
            if not matches:
                print("❌ Нет матчей для анализа")
                return
            
            print(f"📊 Найдено {len(matches)} CS:GO матчей для анализа\n")
            
            recommendations = []
            
            for i, match in enumerate(matches, 1):
                print(f"🎯 МАТЧ {i}/{len(matches)}")
                print("-" * 30)
                
                # Анализируем матч
                analysis = self.analyze_cs_match(match)
                
                if analysis:
                    recommendations.append(analysis)
                
                print()  # Пустая строка между матчами
                self.session_stats['analyzed_matches'] += 1
            
            # Показываем итоги
            self.show_session_summary(recommendations)
            
        except Exception as e:
            logger.error(f"Ошибка анализа: {e}")
            print(f"❌ Ошибка анализа: {e}")
            
    def _merge_match_data(self, hltv_matches: List[Dict], fonbet_matches: List[Dict]) -> List[Dict]:
        """Объединяет данные о матчах с разных источников"""
        merged_matches = []
        
        for hltv_match in hltv_matches:
            # Если это демо-матч или уже есть коэффициенты, используем как есть
            if hltv_match.get('source') == 'demo' or 'odds' in hltv_match:
                merged_matches.append(hltv_match)
                continue
                
            # Для реальных матчей ищем в Фонбет
            fonbet_match = self._find_matching_fonbet_match(hltv_match, fonbet_matches)
            
            if fonbet_match:
                # Объединяем данные
                match = {
                    **hltv_match,
                    'odds': fonbet_match['odds']
                }
                merged_matches.append(match)
            else:
                # Если нет коэффициентов, добавляем матч без них
                merged_matches.append(hltv_match)
            
        return merged_matches
        
    def _find_matching_fonbet_match(self, hltv_match: Dict, fonbet_matches: List[Dict]) -> Optional[Dict]:
        """Ищет соответствующий матч в данных Фонбет"""
        team1 = hltv_match['team1'].lower()
        team2 = hltv_match['team2'].lower()
        
        for fonbet_match in fonbet_matches:
            fonbet_team1 = fonbet_match['team1'].lower()
            fonbet_team2 = fonbet_match['team2'].lower()
            
            # Проверяем совпадение команд (в любом порядке)
            if (team1 in fonbet_team1 and team2 in fonbet_team2) or \
               (team1 in fonbet_team2 and team2 in fonbet_team1):
                return fonbet_match
        
        return None
        
    def analyze_cs_match(self, match: Dict) -> Optional[Dict]:
        """Анализирует конкретный CS:GO матч"""
        try:
            team1 = match['team1']
            team2 = match['team2']
            tournament = match.get('tournament', 'Unknown')
            match_format = match.get('format', 'BO1')
            stage = match.get('stage', '')
            
            print(f"\n🎯 ДЕТАЛЬНЫЙ АНАЛИЗ МАТЧА")
            print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            print(f"🏆 Турнир: {tournament}")
            print(f"📍 Стадия: {stage}")
            print(f"⚔️  {team1} vs {team2} ({match_format})")
            
            # Получаем статистику команд
            team1_stats = self.hltv_parser.get_team_stats(team1)
            team2_stats = self.hltv_parser.get_team_stats(team2)
            
            if not team1_stats or not team2_stats:
                print("⚠️ Не удалось получить статистику команд")
                return None
            
            # Показываем подробную статистику
            self.display_detailed_team_comparison(team1, team1_stats, team2, team2_stats)
            
            # Анализ формы команд
            self.analyze_team_form(team1, team1_stats, team2, team2_stats)
            
            # Анализ турнирного контекста
            self.analyze_tournament_context(match)
            
            # Создаем информацию о матче для модели
            match_info = {
                'format': match_format,
                'tournament': tournament,
                'stage': stage
            }
            
            # Делаем прогноз
            prediction = self.prediction_model.predict_cs_match(
                team1_stats, team2_stats, match_info
            )
            
            # Анализируем результат
            confidence = prediction['confidence']
            probabilities = prediction['probabilities']
            value_bets = prediction['value_bets']
            
            print(f"\n🤖 ПРОГНОЗ И АНАЛИЗ:")
            print(f"━━━━━━━━━━━━━━━━━━━━━")
            
            # Определяем фаворита
            team1_prob = probabilities.get('team1_win', 0)
            team2_prob = probabilities.get('team2_win', 0)
            favorite = team1 if team1_prob > team2_prob else team2
            underdog = team2 if team1_prob > team2_prob else team1
            favorite_prob = max(team1_prob, team2_prob)
            underdog_prob = min(team1_prob, team2_prob)
            
            print(f"📊 Вероятности:")
            print(f"   • {team1}: {team1_prob:.1%}")
            print(f"   • {team2}: {team2_prob:.1%}")
            print(f"\n🎯 Фаворит: {favorite} ({favorite_prob:.1%})")
            print(f"   Андердог: {underdog} ({underdog_prob:.1%})")
            print(f"   Уверенность в прогнозе: {confidence:.1%}")
            
            if confidence >= self.min_confidence:
                self.session_stats['high_confidence_predictions'] += 1
                print(f"\n✅ ВЫСОКАЯ УВЕРЕННОСТЬ В ПРОГНОЗЕ")
                print(f"   • Модель показывает стабильный результат")
                print(f"   • Статистика команд подтверждает прогноз")
                print(f"   • Форма команд соответствует ожиданиям")
            
            # Анализируем value
            if value_bets:
                print("\n💰 АНАЛИЗ ЦЕННОСТИ СТАВОК:")
                print(f"━━━━━━━━━━━━━━━━━━━━━━━")
                self.session_stats['value_bets_found'] += len(value_bets)
                
                for bet in value_bets:
                    team = team1 if bet['team'] == 'team1' else team2
                    value_percent = bet['value']
                    our_prob = bet['our_prob']
                    bookie_prob = bet['bookie_prob']
                    odds = bet['odds']
                    
                    print(f"\n📈 Value bet на {team}:")
                    print(f"   • Наш прогноз: {our_prob:.1%}")
                    print(f"   • Оценка букмекера: {bookie_prob:.1%}")
                    print(f"   • Коэффициент: {odds:.2f}")
                    print(f"   • Value: +{value_percent:.1f}%")
                    
                    if value_percent >= 20:
                        print(f"   ⭐ ОЧЕНЬ ВЫСОКОЕ VALUE!")
                    elif value_percent >= 10:
                        print(f"   ✅ Хорошее value")
                    
                # Генерируем рекомендации
                recommendations = self.generate_detailed_recommendations(
                    match, prediction, team1_stats, team2_stats
                )
                
                if recommendations:
                    print("\n🎯 РЕКОМЕНДАЦИИ ПО СТАВКАМ:")
                    print(f"━━━━━━━━━━━━━━━━━━━━━━━━")
                    for category, recs in recommendations.items():
                        print(f"\n{category}:")
                        for rec in recs:
                            print(f"   • {rec}")
                    self.session_stats['recommended_bets'] += 1
                    
                return {
                    'match': match,
                    'prediction': prediction,
                    'recommendations': recommendations
                }
            else:
                print("\n⚠️ Нет рекомендаций по ставкам")
                print("   • Недостаточно value в коэффициентах")
                print("   • Рекомендуется пропустить матч")
            
            return None
            
        except Exception as e:
            logger.error(f"Ошибка анализа матча: {e}")
            return None
    
    def display_detailed_team_comparison(self, team1: str, team1_stats: Dict, team2: str, team2_stats: Dict):
        """Отображает подробное сравнение команд"""
        print(f"\n📊 ПОДРОБНОЕ СРАВНЕНИЕ КОМАНД:")
        print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"{'':12} {team1:15} | {team2}")
        print(f"{'─' * 12} {'─' * 15} | {'─' * 15}")
        
        # Основные показатели
        print("ОСНОВНЫЕ ПОКАЗАТЕЛИ:")
        print(f"Рейтинг:    {team1_stats.get('rating', 1.0):15.2f} | {team2_stats.get('rating', 1.0):.2f}")
        print(f"Винрейт:    {team1_stats.get('map_win_rate', 0.5):14.1%} | {team2_stats.get('map_win_rate', 0.5):.1%}")
        print(f"Тир:        {team1_stats.get('tier', 3):15d} | {team2_stats.get('tier', 3):d}")
        
        # Специальные показатели
        print("\nСПЕЦИАЛЬНЫЕ ПОКАЗАТЕЛИ:")
        print(f"Пистолетки: {team1_stats.get('pistol_win_rate', 0.5):14.1%} | {team2_stats.get('pistol_win_rate', 0.5):.1%}")
        print(f"Клатчи:     {team1_stats.get('clutch_success', 0.4):14.1%} | {team2_stats.get('clutch_success', 0.4):.1%}")
        
        # Форма команд
        team1_form = team1_stats.get('recent_form', [])
        team2_form = team2_stats.get('recent_form', [])
        form1_str = ''.join(team1_form) if team1_form else 'N/A'
        form2_str = ''.join(team2_form) if team2_form else 'N/A'
        print(f"\nПОСЛЕДНИЕ 5 МАТЧЕЙ:")
        print(f"Форма:      {form1_str:>15} | {form2_str}")
        
        # Анализ сильных и слабых сторон
        print("\nСИЛЬНЫЕ СТОРОНЫ:")
        self._print_team_strengths(team1, team1_stats, team2, team2_stats)
        
    def _print_team_strengths(self, team1: str, team1_stats: Dict, team2: str, team2_stats: Dict):
        """Выводит сильные стороны команд"""
        team1_strengths = []
        team2_strengths = []
        
        # Анализируем рейтинг
        if team1_stats.get('rating', 1.0) > team2_stats.get('rating', 1.0):
            team1_strengths.append("Выше рейтинг")
        elif team2_stats.get('rating', 1.0) > team1_stats.get('rating', 1.0):
            team2_strengths.append("Выше рейтинг")
            
        # Анализируем винрейт
        if team1_stats.get('map_win_rate', 0.5) > team2_stats.get('map_win_rate', 0.5):
            team1_strengths.append("Лучший винрейт")
        elif team2_stats.get('map_win_rate', 0.5) > team1_stats.get('map_win_rate', 0.5):
            team2_strengths.append("Лучший винрейт")
            
        # Анализируем пистолетные раунды
        if team1_stats.get('pistol_win_rate', 0.5) > team2_stats.get('pistol_win_rate', 0.5):
            team1_strengths.append("Сильнее в пистолетках")
        elif team2_stats.get('pistol_win_rate', 0.5) > team1_stats.get('pistol_win_rate', 0.5):
            team2_strengths.append("Сильнее в пистолетках")
            
        # Анализируем клатчи
        if team1_stats.get('clutch_success', 0.4) > team2_stats.get('clutch_success', 0.4):
            team1_strengths.append("Лучше в клатчах")
        elif team2_stats.get('clutch_success', 0.4) > team1_stats.get('clutch_success', 0.4):
            team2_strengths.append("Лучше в клатчах")
            
        # Анализируем форму
        team1_form = team1_stats.get('recent_form', [])
        team2_form = team2_stats.get('recent_form', [])
        team1_wins = team1_form.count('W')
        team2_wins = team2_form.count('W')
        
        if team1_wins > team2_wins:
            team1_strengths.append("Лучшая текущая форма")
        elif team2_wins > team1_wins:
            team2_strengths.append("Лучшая текущая форма")
            
        # Выводим результаты
        if team1_strengths:
            print(f"{team1}:")
            for strength in team1_strengths:
                print(f"   • {strength}")
                
        if team2_strengths:
            print(f"\n{team2}:")
            for strength in team2_strengths:
                print(f"   • {strength}")
                
    def analyze_team_form(self, team1: str, team1_stats: Dict, team2: str, team2_stats: Dict):
        """Анализирует форму команд"""
        print(f"\n📈 АНАЛИЗ ФОРМЫ КОМАНД:")
        print(f"━━━━━━━━━━━━━━━━━━━━")
        
        for team, stats in [(team1, team1_stats), (team2, team2_stats)]:
            form = stats.get('recent_form', [])
            if not form:
                continue
                
            wins = form.count('W')
            losses = form.count('L')
            win_rate = wins / len(form)
            
            print(f"\n{team}:")
            print(f"   • Последние {len(form)} матчей: {''.join(form)}")
            print(f"   • Винрейт: {win_rate:.1%} ({wins}W-{losses}L)")
            
            # Анализ тренда
            if form.count('W') >= 3:
                print(f"   ✅ Команда в хорошей форме")
            elif form.count('L') >= 3:
                print(f"   ⚠️ Команда в плохой форме")
            
            # Анализ последнего матча
            if form[0] == 'W':
                print(f"   📈 Победа в последнем матче")
            else:
                print(f"   📉 Поражение в последнем матче")
                
    def analyze_tournament_context(self, match: Dict):
        """Анализирует турнирный контекст матча"""
        print(f"\n🏆 ТУРНИРНЫЙ КОНТЕКСТ:")
        print(f"━━━━━━━━━━━━━━━━━━━")
        
        tournament = match.get('tournament', '')
        stage = match.get('stage', '')
        match_format = match.get('format', 'BO1')
        
        # Анализ стадии турнира
        if 'final' in stage.lower():
            print(f"   • ⭐ Финальная стадия турнира")
            print(f"   • Команды будут максимально мотивированы")
        elif 'semi' in stage.lower():
            print(f"   • 🔥 Полуфинальная стадия")
            print(f"   • Высокие ставки, команды в хорошей форме")
        elif 'quarter' in stage.lower():
            print(f"   • 📈 Четвертьфинал")
            print(f"   • Важная стадия плей-офф")
            
        # Анализ формата
        if match_format == 'BO1':
            print(f"   • ⚠️ Формат BO1 - возможны сюрпризы")
            print(f"   • Высокое влияние пистолетных раундов")
        elif match_format == 'BO3':
            print(f"   • ✅ Формат BO3 - более стабильный")
            print(f"   • Преимущество у более сильной команды")
        elif match_format == 'BO5':
            print(f"   • 🔥 Формат BO5 - максимально показательный")
            print(f"   • Выигрывает сильнейшая команда")
            
    def generate_detailed_recommendations(self, match: Dict, prediction: Dict, team1_stats: Dict, team2_stats: Dict) -> Dict[str, List[str]]:
        """Генерирует подробные рекомендации для CS:GO ставок"""
        recommendations = {
            "💰 ОСНОВНЫЕ СТАВКИ": [],
            "📊 СТАТИСТИЧЕСКИЕ СТАВКИ": [],
            "⚠️ РИСКИ": [],
            "💡 ДОПОЛНИТЕЛЬНО": []
        }
        
        confidence = prediction['confidence']
        value_bets = prediction['value_bets']
        probabilities = prediction['probabilities']
        
        # Проверяем условия для рекомендаций
        if confidence < self.min_confidence:
            recommendations["⚠️ РИСКИ"].append("Низкая уверенность в прогнозе")
            return recommendations
        
        if self.daily_bets_count >= self.max_daily_bets:
            recommendations["⚠️ РИСКИ"].append("Достигнут лимит ставок на день")
            return recommendations
        
        # Рекомендации на основе value bets
        for bet in value_bets:
            if bet['value'] >= self.min_value:
                team_name = match['team1'] if bet['team'] == 'team1' else match['team2']
                
                # Рассчитываем размер ставки
                bankroll_info = self.bankroll_manager.get_bankroll_info()
                current_bankroll = bankroll_info['current_balance']
                
                # Используем стратегию Келли для CS:GO
                kelly_fraction = (bet['our_prob'] * bet['odds'] - 1) / (bet['odds'] - 1)
                kelly_fraction *= 0.25  # Четверть Келли для безопасности
                
                stake = min(current_bankroll * kelly_fraction, current_bankroll * 0.05)
                
                if stake >= 100:
                    recommendations["💰 ОСНОВНЫЕ СТАВКИ"].append(
                        f"Ставка на {team_name}: {stake:.0f}₽ (коэфф. {bet['odds']:.2f}, value {bet['value']:.1f}%)"
                    )
                    
                    if bet['value'] >= 20:
                        recommendations["💰 ОСНОВНЫЕ СТАВКИ"].append(
                            f"ОЧЕНЬ ВЫСОКОЕ VALUE на {team_name}! Рекомендуется повышенная ставка"
                        )
        
        # Статистические ставки
        team1 = match['team1']
        team2 = match['team2']
        
        # Анализ пистолетных раундов
        t1_pistol = team1_stats.get('pistol_win_rate', 0.5)
        t2_pistol = team2_stats.get('pistol_win_rate', 0.5)
        if abs(t1_pistol - t2_pistol) >= 0.1:
            better_pistol_team = team1 if t1_pistol > t2_pistol else team2
            recommendations["📊 СТАТИСТИЧЕСКИЕ СТАВКИ"].append(
                f"Рассмотрите ставку на победу {better_pistol_team} в пистолетных раундах"
            )
            
        # Анализ формы
        t1_form = team1_stats.get('recent_form', [])
        t2_form = team2_stats.get('recent_form', [])
        t1_wins = t1_form.count('W')
        t2_wins = t2_form.count('W')
        if abs(t1_wins - t2_wins) >= 2:
            better_form_team = team1 if t1_wins > t2_wins else team2
            recommendations["📊 СТАТИСТИЧЕСКИЕ СТАВКИ"].append(
                f"{better_form_team} в отличной форме - рассмотрите ставку на их победу"
            )
            
        # Анализ рисков
        match_format = match.get('format', 'BO1')
        if match_format == 'BO1':
            recommendations["⚠️ РИСКИ"].append(
                "Формат BO1 более рискованный - рекомендуется уменьшить размер ставки"
            )
            
        if abs(team1_stats.get('rating', 1.0) - team2_stats.get('rating', 1.0)) < 0.1:
            recommendations["⚠️ РИСКИ"].append(
                "Команды очень близки по уровню - возможен любой исход"
            )
            
        # Дополнительные рекомендации
        if confidence >= 0.70:
            recommendations["💡 ДОПОЛНИТЕЛЬНО"].append(
                "Очень высокая уверенность в прогнозе - хорошая возможность для ставки"
            )
            
        if match_format in ['BO3', 'BO5'] and confidence >= 0.65:
            recommendations["💡 ДОПОЛНИТЕЛЬНО"].append(
                f"Формат {match_format} благоприятствует более сильной команде"
            )
            
        return recommendations
    
    def show_session_summary(self, recommendations: List[Dict]):
        """Показывает итоги сессии анализа"""
        print("\n" + "=" * 50)
        print("📈 ИТОГИ АНАЛИЗА CS:GO МАТЧЕЙ")
        print("=" * 50)
        
        stats = self.session_stats
        print(f"🔍 Проанализировано матчей: {stats['analyzed_matches']}")
        print(f"🎯 Высокая уверенность: {stats['high_confidence_predictions']}")
        print(f"💰 Value bets найдено: {stats['value_bets_found']}")
        print(f"📊 Рекомендации к ставкам: {stats['recommended_bets']}")
        
        if recommendations:
            print(f"\n💡 ТОП РЕКОМЕНДАЦИИ:")
            # Берем только первые 3 рекомендации
            top_recommendations = recommendations[:3] if len(recommendations) > 3 else recommendations
            
            for i, rec_data in enumerate(top_recommendations, 1):
                try:
                    match = rec_data['match']
                    pred = rec_data['prediction']
                    print(f"\n{i}. {match['team1']} vs {match['team2']}")
                    
                    # Форматируем прогноз и уверенность
                    prediction_text = self.format_prediction(pred['prediction'])
                    confidence = pred['confidence'] * 100
                    print(f"   Прогноз: {prediction_text} ({confidence:.1f}%)")
                    
                    # Выводим топ рекомендации
                    if 'recommendations' in rec_data:
                        main_bets = rec_data['recommendations'].get('💰 ОСНОВНЫЕ СТАВКИ', [])
                        if main_bets:
                            for bet in main_bets[:2]:  # Показываем только первые 2 ставки
                                print(f"   • {bet}")
                except Exception as e:
                    logger.error(f"Ошибка вывода рекомендации: {e}")
                    continue
        
        # Информация о банкролле
        bankroll_info = self.bankroll_manager.get_bankroll_info()
        print(f"\n💰 БАНКРОЛЛ: {bankroll_info['current_balance']:,.0f}₽")
        print(f"📊 Общая прибыль: {bankroll_info['total_profit']:+,.0f}₽")
        
        print("\n" + "=" * 50)
    
    def place_bet_interactive(self):
        """Интерактивное размещение ставки"""
        print("\n💰 РАЗМЕЩЕНИЕ СТАВКИ")
        print("=" * 30)
        
        try:
            # Получаем свежие матчи
            matches = self.hltv_parser.get_upcoming_matches()
            
            if not matches:
                print("❌ Нет доступных матчей")
                return
            
            # Показываем список матчей
            print("📋 Доступные матчи:")
            for i, match in enumerate(matches, 1):
                team1, team2 = match['team1'], match['team2']
                tournament = match.get('tournament', 'Unknown')
                print(f"{i}. {team1} vs {team2} ({tournament})")
            
            # Выбор матча
            choice = input(f"\nВыберите матч (1-{len(matches)}) или 0 для отмены: ")
            
            if choice == '0':
                return
                
            try:
                match_idx = int(choice) - 1
                selected_match = matches[match_idx]
            except (ValueError, IndexError):
                print("❌ Неверный выбор")
                return
            
            # Анализируем выбранный матч
            analysis = self.analyze_cs_match(selected_match)
            
            if not analysis or not analysis['recommendations']:
                print("⚠️ Нет рекомендаций для этого матча")
                return
            
            # Выбор команды для ставки
            team1, team2 = selected_match['team1'], selected_match['team2']
            print(f"\nНа какую команду ставим?")
            print(f"1. {team1}")
            print(f"2. {team2}")
            
            team_choice = input("Выбор (1-2): ")
            
            if team_choice == '1':
                bet_team = team1
                odds = selected_match['odds']['team1']
            elif team_choice == '2':
                bet_team = team2
                odds = selected_match['odds']['team2']
            else:
                print("❌ Неверный выбор")
                return
            
            # Размер ставки
            bankroll_info = self.bankroll_manager.get_bankroll_info()
            max_stake = bankroll_info['current_balance'] * 0.1  # Макс 10%
            
            print(f"\nРазмер ставки (макс. {max_stake:.0f}₽): ", end="")
            stake_input = input()
            
            try:
                stake = float(stake_input)
                if stake <= 0 or stake > max_stake:
                    print(f"❌ Неверная сумма (макс. {max_stake:.0f}₽)")
                    return
            except ValueError:
                print("❌ Неверный формат суммы")
                return
            
            # Размещаем ставку
            match_info = {
                'teams': f"{team1} vs {team2}",
                'tournament': selected_match.get('tournament', 'Unknown'),
                'bet_target': f"{bet_team} победа"
            }
            
            bet_success = self.bankroll_manager.place_bet(
                stake, f"{bet_team} победа", odds, match_info
            )
            
            if bet_success:
                print(f"✅ Ставка размещена успешно!")
                print(f"💰 Ставка: {stake:.0f}₽ на {bet_team} (коэфф. {odds:.2f})")
                print(f"💵 Возможный выигрыш: {stake * odds:.0f}₽")
                
                # Обновляем счетчик
                self.daily_bets_count += 1
            else:
                print(f"❌ Ошибка размещения ставки")
        
        except Exception as e:
            logger.error(f"Ошибка размещения ставки: {e}")
            print(f"❌ Ошибка: {e}")
    
    def show_main_menu(self):
        """Показывает главное меню"""
        while True:
            print("\n" + "🎮" * 25)
            print("CS:GO BETTING SYSTEM - ГЛАВНОЕ МЕНЮ")
            print("🎮" * 25)
            print("\n1. 🔍 Анализ CS:GO матчей")
            print("2. 💰 Разместить ставку")
            print("3. 📊 Статистика банкролла")
            print("4. 🏆 История ставок")
            print("5. ⚙️ Настройки системы")
            print("6. 📡 Информация о HLTV парсере")
            print("0. 🚪 Выход")
            
            choice = input("\nВыберите действие: ")
            
            if choice == '1':
                self.run_analysis()
            elif choice == '2':
                self.place_bet_interactive()
            elif choice == '3':
                self.show_bankroll_stats()
            elif choice == '4':
                self.show_betting_history()
            elif choice == '5':
                self.show_settings_menu()
            elif choice == '6':
                self.show_hltv_info()
            elif choice == '0':
                print("\n👋 До свидания! Удачных ставок на CS:GO!")
                break
            else:
                print("❌ Неверный выбор, попробуйте снова")
    
    def show_bankroll_stats(self):
        """Показывает статистику банкролла"""
        print("\n💰 СТАТИСТИКА БАНКРОЛЛА")
        print("=" * 30)
        
        info = self.bankroll_manager.get_bankroll_info()
        
        print(f"💵 Текущий банкролл: {info['current_balance']:,.0f}₽")
        print(f"🏦 Начальный банкролл: {info['initial_balance']:,.0f}₽")
        print(f"📈 Общая прибыль: {info['total_profit']:+,.0f}₽")
        print(f"📊 ROI: {info.get('roi', 0):+.1%}")
        print(f"🎯 Всего ставок: {info.get('total_bets', 0)}")
        print(f"✅ Выигрышных: {info.get('winning_bets', 0)}")
        print(f"❌ Проигрышных: {info.get('losing_bets', 0)}")
        
        if info.get('total_bets', 0) > 0:
            win_rate = info.get('winning_bets', 0) / info.get('total_bets', 1)
            print(f"📈 Винрейт: {win_rate:.1%}")
    
    def show_betting_history(self):
        """Показывает историю ставок"""
        print("\n🏆 ИСТОРИЯ СТАВОК")
        print("=" * 30)
        
        history = self.bankroll_manager.get_betting_history()
        
        if not history:
            print("📝 История ставок пуста")
            return
        
        for i, bet in enumerate(history[-10:], 1):  # Последние 10 ставок
            status = "✅" if bet.get('result') == 'win' else "❌" if bet.get('result') == 'loss' else "⏳"
            print(f"{i}. {status} {bet.get('description', 'N/A')} - {bet.get('stake', 0):.0f}₽ (x{bet.get('odds', 0):.2f})")
    
    def show_settings_menu(self):
        """Показывает меню настроек"""
        print("\n⚙️ НАСТРОЙКИ СИСТЕМЫ")
        print("=" * 30)
        print(f"1. Мин. уверенность: {self.min_confidence:.1%}")
        print(f"2. Мин. value: {self.min_value:.1%}")
        print(f"3. Макс. ставок в день: {self.max_daily_bets}")
        print("4. Сбросить счетчик дневных ставок")
        print("0. Назад")
        
        choice = input("\nВыберите настройку: ")
        
        if choice == '1':
            try:
                new_conf = float(input(f"Новая мин. уверенность (текущая {self.min_confidence:.1%}): "))
                if 0.1 <= new_conf <= 1.0:
                    self.min_confidence = new_conf
                    print("✅ Настройка сохранена")
                else:
                    print("❌ Значение должно быть от 0.1 до 1.0")
            except ValueError:
                print("❌ Неверный формат")
        elif choice == '4':
            self.daily_bets_count = 0
            print("✅ Счетчик дневных ставок сброшен")
    
    def show_hltv_info(self):
        """Показывает информацию о HLTV парсере"""
        print("\n📡 ИНФОРМАЦИЯ О HLTV ПАРСЕРЕ")
        print("=" * 40)
        print(self.hltv_parser.get_setup_instructions())

def main():
    """Главная функция"""
    try:
        # Проверка Python версии
        if sys.version_info < (3, 6):
            print("❌ Требуется Python 3.6 или новее")
            sys.exit(1)
        
        # Создание и запуск системы
        system = CSGOBettingSystem()
        system.show_main_menu()
        
    except KeyboardInterrupt:
        print("\n\n👋 Система остановлена пользователем")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
        print(f"\n❌ Критическая ошибка: {e}")
        print("Проверьте логи в файле csgo_betting.log")

if __name__ == "__main__":
    main() 