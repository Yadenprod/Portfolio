#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Расширенный анализатор ставок
Продвинутая логика анализа матчей и поиска ценных ставок
"""

import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging
from dataclasses import dataclass
import statistics

logger = logging.getLogger(__name__)

@dataclass
class ValueBet:
    """Класс для хранения информации о ценной ставке"""
    match_id: str
    outcome: str
    our_probability: float
    bookmaker_odds: float
    implied_probability: float
    expected_value: float
    confidence_level: str
    risk_assessment: str
    stake_recommendation: float
    reasoning: List[str]

@dataclass
class TeamForm:
    """Класс для хранения формы команды"""
    team_name: str
    recent_results: List[str]  # W, L, D
    goals_scored: int
    goals_conceded: int
    matches_played: int
    win_percentage: float
    goal_difference: int
    form_rating: float

class AdvancedBetAnalyzer:
    def __init__(self):
        self.min_value_threshold = 0.05  # Минимальный EV 5%
        self.high_confidence_threshold = 0.75
        self.medium_confidence_threshold = 0.60
        
        # Веса для различных факторов
        self.weights = {
            'form': 0.25,
            'head_to_head': 0.20,
            'home_advantage': 0.15,
            'goal_stats': 0.20,
            'injuries': 0.10,
            'motivation': 0.10
        }
        
    def analyze_match_comprehensive(self, match_data: Dict) -> Dict:
        """Комплексный анализ матча"""
        try:
            # Извлекаем данные
            match_info = match_data.get('match_info', {})
            home_stats = match_data.get('home_stats', {})
            away_stats = match_data.get('away_stats', {})
            h2h = match_data.get('h2h', {})
            odds = match_data.get('odds', {})
            
            home_team = match_info.get('home_team', 'Unknown')
            away_team = match_info.get('away_team', 'Unknown')
            
            # Анализируем форму команд
            home_form = self._analyze_team_form(home_stats, home_team)
            away_form = self._analyze_team_form(away_stats, away_team)
            
            # Анализируем личные встречи
            h2h_analysis = self._analyze_head_to_head(h2h, home_team, away_team)
            
            # Анализируем домашний фактор
            home_advantage = self._calculate_home_advantage(home_stats)
            
            # Анализируем голевую статистику
            goal_analysis = self._analyze_goal_statistics(home_stats, away_stats)
            
            # Анализируем травмы и мотивацию
            injury_impact = self._analyze_injuries(home_stats, away_stats)
            motivation_factor = self._analyze_motivation(match_info)
            
            # Рассчитываем вероятности
            probabilities = self._calculate_probabilities(
                home_form, away_form, h2h_analysis, home_advantage,
                goal_analysis, injury_impact, motivation_factor
            )
            
            # Ищем ценные ставки
            value_bets = self._find_value_bets(probabilities, odds)
            
            # Формируем итоговый анализ
            analysis = {
                'match_id': match_info.get('id', 'unknown'),
                'teams': f"{home_team} vs {away_team}",
                'competition': match_info.get('competition', 'Unknown'),
                'date': match_info.get('date', ''),
                'analysis_timestamp': datetime.now().isoformat(),
                
                'team_analysis': {
                    'home_form': home_form.__dict__,
                    'away_form': away_form.__dict__,
                    'form_advantage': home_form.form_rating - away_form.form_rating
                },
                
                'tactical_analysis': {
                    'h2h_summary': h2h_analysis,
                    'home_advantage': home_advantage,
                    'goal_analysis': goal_analysis,
                    'injury_impact': injury_impact,
                    'motivation_factor': motivation_factor
                },
                
                'predictions': {
                    'probabilities': probabilities,
                    'confidence_level': self._determine_confidence_level(probabilities),
                    'predicted_outcome': max(probabilities, key=probabilities.get)
                },
                
                'betting_analysis': {
                    'value_bets': [vb.__dict__ for vb in value_bets],
                    'best_bet': value_bets[0].__dict__ if value_bets else None,
                    'recommended_action': 'bet' if value_bets else 'skip',
                    'total_value_bets': len(value_bets)
                },
                
                'risk_assessment': {
                    'overall_risk': self._assess_overall_risk(probabilities, value_bets),
                    'variance': self._calculate_variance(probabilities),
                    'uncertainty_factors': self._identify_uncertainty_factors(match_data)
                }
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Ошибка при комплексном анализе матча: {e}")
            return {}
    
    def _analyze_team_form(self, team_stats: Dict, team_name: str) -> TeamForm:
        """Анализирует форму команды"""
        try:
            recent_form = team_stats.get('recent_form', ['W', 'W', 'D', 'L', 'W'])
            last_games = team_stats.get('last_5_games', [])
            
            # Подсчитываем статистику
            wins = recent_form.count('W')
            losses = recent_form.count('L')
            draws = recent_form.count('D')
            matches_played = len(recent_form)
            
            # Голы из последних игр
            goals_scored = 0
            goals_conceded = 0
            
            for game in last_games:
                result = game.get('result', '0-0')
                # Парсим результат типа "W 2-1" или "L 0-2"
                try:
                    score_part = result.split()[-1]  # Берем последнюю часть "2-1"
                    home_goals, away_goals = map(int, score_part.split('-'))
                    
                    if game.get('home', True):  # Если команда играла дома
                        goals_scored += home_goals
                        goals_conceded += away_goals
                    else:  # Если команда играла в гостях
                        goals_scored += away_goals
                        goals_conceded += home_goals
                        
                except ValueError:
                    continue
            
            # Рассчитываем рейтинг формы
            form_points = wins * 3 + draws * 1
            max_points = matches_played * 3
            form_rating = form_points / max_points if max_points > 0 else 0.5
            
            # Бонус за последние результаты (больший вес недавним играм)
            weights = [0.4, 0.3, 0.15, 0.1, 0.05]  # Последняя игра важнее
            weighted_form = 0
            for i, result in enumerate(recent_form[:5]):
                if result == 'W':
                    weighted_form += weights[i] * 1
                elif result == 'D':
                    weighted_form += weights[i] * 0.5
                # Поражения дают 0 очков
            
            form_rating = (form_rating + weighted_form) / 2
            
            return TeamForm(
                team_name=team_name,
                recent_results=recent_form,
                goals_scored=goals_scored,
                goals_conceded=goals_conceded,
                matches_played=matches_played,
                win_percentage=wins / matches_played if matches_played > 0 else 0,
                goal_difference=goals_scored - goals_conceded,
                form_rating=round(form_rating, 3)
            )
            
        except Exception as e:
            logger.error(f"Ошибка анализа формы команды {team_name}: {e}")
            return TeamForm(team_name, [], 0, 0, 0, 0, 0, 0.5)
    
    def _analyze_head_to_head(self, h2h: Dict, home_team: str, away_team: str) -> Dict:
        """Анализирует статистику личных встреч"""
        try:
            total_matches = h2h.get('total_matches', 0)
            team1_wins = h2h.get('team1_wins', 0)  # home team
            team2_wins = h2h.get('team2_wins', 0)  # away team
            draws = h2h.get('draws', 0)
            
            if total_matches == 0:
                return {
                    'total_matches': 0,
                    'home_win_percentage': 50,
                    'away_win_percentage': 50,
                    'draw_percentage': 0,
                    'h2h_advantage': 'neutral',
                    'avg_goals': 2.5,
                    'confidence': 'low'
                }
            
            home_win_pct = (team1_wins / total_matches) * 100
            away_win_pct = (team2_wins / total_matches) * 100
            draw_pct = (draws / total_matches) * 100
            
            # Определяем преимущество
            if home_win_pct > away_win_pct + 20:
                advantage = 'strong_home'
            elif away_win_pct > home_win_pct + 20:
                advantage = 'strong_away'
            elif abs(home_win_pct - away_win_pct) <= 10:
                advantage = 'balanced'
            else:
                advantage = 'slight_home' if home_win_pct > away_win_pct else 'slight_away'
            
            confidence = 'high' if total_matches >= 10 else 'medium' if total_matches >= 5 else 'low'
            
            return {
                'total_matches': total_matches,
                'home_win_percentage': round(home_win_pct, 1),
                'away_win_percentage': round(away_win_pct, 1),
                'draw_percentage': round(draw_pct, 1),
                'h2h_advantage': advantage,
                'avg_goals': h2h.get('avg_goals_per_game', 2.5),
                'confidence': confidence
            }
            
        except Exception as e:
            logger.error(f"Ошибка анализа H2H: {e}")
            return {'confidence': 'low'}
    
    def _calculate_home_advantage(self, home_stats: Dict) -> Dict:
        """Рассчитывает домашнее преимущество"""
        try:
            home_record = home_stats.get('home_record', {})
            home_wins = home_record.get('wins', 0)
            home_draws = home_record.get('draws', 0)
            home_losses = home_record.get('losses', 0)
            
            total_home_games = home_wins + home_draws + home_losses
            
            if total_home_games == 0:
                return {'advantage_factor': 1.1, 'strength': 'average'}
            
            home_points = home_wins * 3 + home_draws
            home_performance = home_points / (total_home_games * 3)
            
            # Стандартное домашнее преимущество около 55-60%
            if home_performance >= 0.75:
                advantage = {'factor': 1.25, 'strength': 'very_strong'}
            elif home_performance >= 0.65:
                advantage = {'factor': 1.15, 'strength': 'strong'}
            elif home_performance >= 0.45:
                advantage = {'factor': 1.08, 'strength': 'average'}
            else:
                advantage = {'factor': 1.0, 'strength': 'weak'}
            
            return {
                'advantage_factor': advantage['factor'],
                'strength': advantage['strength'],
                'home_performance': round(home_performance, 3),
                'home_points_per_game': round(home_points / total_home_games, 2) if total_home_games > 0 else 0
            }
            
        except Exception as e:
            logger.error(f"Ошибка расчета домашнего преимущества: {e}")
            return {'advantage_factor': 1.1, 'strength': 'average'}
    
    def _analyze_goal_statistics(self, home_stats: Dict, away_stats: Dict) -> Dict:
        """Анализирует голевую статистику команд"""
        try:
            # Домашняя команда
            home_scored = home_stats.get('goals_scored', 20)
            home_conceded = home_stats.get('goals_conceded', 15)
            home_avg_scored = home_stats.get('avg_goals_per_game', 1.5)
            
            # Гостевая команда
            away_scored = away_stats.get('goals_scored', 18)
            away_conceded = away_stats.get('goals_conceded', 20)
            away_avg_scored = away_stats.get('avg_goals_per_game', 1.3)
            
            # Прогноз голов
            predicted_home_goals = (home_avg_scored + (away_conceded / 15)) / 2
            predicted_away_goals = (away_avg_scored + (home_conceded / 15)) / 2
            
            total_predicted = predicted_home_goals + predicted_away_goals
            
            # Анализ тоталов
            over_under_analysis = {
                'total_predicted': round(total_predicted, 2),
                'over_2_5_probability': min(90, max(10, (total_predicted - 2.5) * 40 + 50)),
                'over_1_5_probability': min(95, max(20, (total_predicted - 1.5) * 35 + 70)),
                'under_2_5_probability': max(10, min(90, 100 - ((total_predicted - 2.5) * 40 + 50)))
            }
            
            # Обе забьют
            btts_probability = min(85, max(15, 
                (predicted_home_goals * predicted_away_goals * 25) + 
                (min(home_avg_scored, away_avg_scored) * 20)
            ))
            
            return {
                'home_attack_strength': round(home_avg_scored / 1.5, 2),  # Относительно среднего
                'home_defense_strength': round(1.5 / (home_conceded / 15), 2),
                'away_attack_strength': round(away_avg_scored / 1.5, 2),
                'away_defense_strength': round(1.5 / (away_conceded / 15), 2),
                'predicted_score': f"{predicted_home_goals:.1f}-{predicted_away_goals:.1f}",
                'goal_expectancy': total_predicted,
                'over_under_analysis': over_under_analysis,
                'btts_probability': round(btts_probability, 1)
            }
            
        except Exception as e:
            logger.error(f"Ошибка анализа голевой статистики: {e}")
            return {'goal_expectancy': 2.5}
    
    def _analyze_injuries(self, home_stats: Dict, away_stats: Dict) -> Dict:
        """Анализирует влияние травм"""
        try:
            home_injuries = home_stats.get('injuries', [])
            away_injuries = away_stats.get('injuries', [])
            
            # Простая оценка влияния травм
            home_impact = len(home_injuries) * 0.05  # 5% за каждого травмированного
            away_impact = len(away_injuries) * 0.05
            
            net_impact = away_impact - home_impact  # Положительное значение в пользу дома
            
            return {
                'home_injuries_count': len(home_injuries),
                'away_injuries_count': len(away_injuries),
                'home_impact_factor': 1 - home_impact,
                'away_impact_factor': 1 - away_impact,
                'net_advantage': 'home' if net_impact > 0.05 else 'away' if net_impact < -0.05 else 'neutral',
                'impact_magnitude': abs(net_impact)
            }
            
        except Exception as e:
            logger.error(f"Ошибка анализа травм: {e}")
            return {'net_advantage': 'neutral', 'impact_magnitude': 0}
    
    def _analyze_motivation(self, match_info: Dict) -> Dict:
        """Анализирует мотивационные факторы"""
        try:
            competition = match_info.get('competition', '').lower()
            
            # Оценка важности матча
            if any(word in competition for word in ['champions', 'cup', 'final', 'playoff']):
                importance = 'very_high'
                motivation_boost = 1.15
            elif any(word in competition for word in ['europa', 'conference', 'semi']):
                importance = 'high'
                motivation_boost = 1.08
            elif any(word in competition for word in ['league', 'championship']):
                importance = 'medium'
                motivation_boost = 1.03
            else:
                importance = 'low'
                motivation_boost = 1.0
            
            return {
                'match_importance': importance,
                'motivation_factor': motivation_boost,
                'competition_type': competition
            }
            
        except Exception as e:
            logger.error(f"Ошибка анализа мотивации: {e}")
            return {'motivation_factor': 1.0}
    
    def _calculate_probabilities(self, home_form: TeamForm, away_form: TeamForm,
                               h2h: Dict, home_adv: Dict, goals: Dict,
                               injuries: Dict, motivation: Dict) -> Dict:
        """Рассчитывает вероятности исходов матча"""
        try:
            # Базовые вероятности (равные шансы с домашним преимуществом)
            base_home = 40
            base_draw = 25
            base_away = 35
            
            # Корректировка на форму
            form_diff = home_form.form_rating - away_form.form_rating
            home_adjustment = form_diff * 30  # Максимум ±30%
            
            # Корректировка на H2H
            h2h_home_pct = h2h.get('home_win_percentage', 50)
            h2h_adjustment = (h2h_home_pct - 50) * 0.3
            
            # Корректировка на домашнее преимущество
            home_adv_factor = home_adv.get('advantage_factor', 1.1)
            home_advantage_boost = (home_adv_factor - 1) * 100
            
            # Корректировка на травмы
            injury_adjustment = 0
            if injuries.get('net_advantage') == 'home':
                injury_adjustment = injuries.get('impact_magnitude', 0) * 20
            elif injuries.get('net_advantage') == 'away':
                injury_adjustment = -injuries.get('impact_magnitude', 0) * 20
            
            # Корректировка на мотивацию
            motivation_boost = (motivation.get('motivation_factor', 1.0) - 1) * 5
            
            # Применяем все корректировки
            home_prob = base_home + home_adjustment + h2h_adjustment + home_advantage_boost + injury_adjustment + motivation_boost
            away_prob = base_away - home_adjustment - h2h_adjustment + injury_adjustment
            draw_prob = base_draw - (abs(home_adjustment) + abs(h2h_adjustment)) * 0.3
            
            # Нормализация
            total = home_prob + draw_prob + away_prob
            home_prob = max(5, min(85, home_prob / total * 100))
            away_prob = max(5, min(85, away_prob / total * 100))
            draw_prob = max(5, min(50, 100 - home_prob - away_prob))
            
            # Округление
            return {
                'home_win': round(home_prob / 100, 3),
                'draw': round(draw_prob / 100, 3),
                'away_win': round(away_prob / 100, 3)
            }
            
        except Exception as e:
            logger.error(f"Ошибка расчета вероятностей: {e}")
            return {'home_win': 0.4, 'draw': 0.25, 'away_win': 0.35}
    
    def _find_value_bets(self, probabilities: Dict, odds_data: Dict) -> List[ValueBet]:
        """Ищет ценные ставки"""
        try:
            value_bets = []
            average_odds = odds_data.get('average_odds', {})
            
            outcome_mapping = {
                'home_win': 'home',
                'draw': 'draw',
                'away_win': 'away'
            }
            
            for outcome, prob in probabilities.items():
                odds_key = outcome_mapping.get(outcome, outcome)
                odds = average_odds.get(odds_key)
                
                if not odds or odds <= 1:
                    continue
                
                implied_prob = 1 / odds
                expected_value = (prob * odds) - 1
                
                if expected_value >= self.min_value_threshold:
                    # Определяем уровень уверенности
                    if prob >= self.high_confidence_threshold:
                        confidence = 'high'
                        risk = 'low'
                    elif prob >= self.medium_confidence_threshold:
                        confidence = 'medium'
                        risk = 'medium'
                    else:
                        confidence = 'low'
                        risk = 'high'
                    
                    # Рекомендуемая ставка (процент от банкролла)
                    kelly_fraction = (prob * odds - 1) / (odds - 1)
                    stake_pct = min(5, max(0.5, kelly_fraction * 100))  # 0.5-5% от банкролла
                    
                    # Обоснование
                    reasoning = [
                        f"Наша оценка вероятности: {prob:.1%}",
                        f"Вероятность букмекера: {implied_prob:.1%}",
                        f"Ожидаемая прибыль: {expected_value:.1%}",
                        f"Коэффициент: {odds}"
                    ]
                    
                    value_bet = ValueBet(
                        match_id=odds_data.get('match_id', 'unknown'),
                        outcome=outcome,
                        our_probability=prob,
                        bookmaker_odds=odds,
                        implied_probability=implied_prob,
                        expected_value=expected_value,
                        confidence_level=confidence,
                        risk_assessment=risk,
                        stake_recommendation=stake_pct,
                        reasoning=reasoning
                    )
                    
                    value_bets.append(value_bet)
            
            # Сортируем по ожидаемой прибыли
            value_bets.sort(key=lambda x: x.expected_value, reverse=True)
            
            return value_bets
            
        except Exception as e:
            logger.error(f"Ошибка поиска ценных ставок: {e}")
            return []
    
    def _determine_confidence_level(self, probabilities: Dict) -> str:
        """Определяет общий уровень уверенности в прогнозе"""
        max_prob = max(probabilities.values())
        
        if max_prob >= 0.70:
            return 'very_high'
        elif max_prob >= 0.60:
            return 'high'
        elif max_prob >= 0.45:
            return 'medium'
        else:
            return 'low'
    
    def _assess_overall_risk(self, probabilities: Dict, value_bets: List[ValueBet]) -> str:
        """Оценивает общий риск ставок"""
        if not value_bets:
            return 'no_bets'
        
        # Анализ на основе разброса вероятностей
        prob_values = list(probabilities.values())
        variance = statistics.variance(prob_values) if len(prob_values) > 1 else 0
        
        # Анализ ценных ставок
        avg_ev = statistics.mean([vb.expected_value for vb in value_bets])
        high_risk_bets = sum(1 for vb in value_bets if vb.risk_assessment == 'high')
        
        if variance < 0.05 and avg_ev > 0.15 and high_risk_bets == 0:
            return 'low'
        elif variance < 0.1 and avg_ev > 0.08 and high_risk_bets <= 1:
            return 'medium'
        else:
            return 'high'
    
    def _calculate_variance(self, probabilities: Dict) -> float:
        """Рассчитывает дисперсию вероятностей"""
        prob_values = list(probabilities.values())
        return statistics.variance(prob_values) if len(prob_values) > 1 else 0
    
    def _identify_uncertainty_factors(self, match_data: Dict) -> List[str]:
        """Определяет факторы неопределенности"""
        factors = []
        
        h2h = match_data.get('h2h', {})
        if h2h.get('total_matches', 0) < 5:
            factors.append('Мало личных встреч')
        
        home_stats = match_data.get('home_stats', {})
        away_stats = match_data.get('away_stats', {})
        
        if len(home_stats.get('injuries', [])) > 3:
            factors.append('Много травм у домашней команды')
        if len(away_stats.get('injuries', [])) > 3:
            factors.append('Много травм у гостевой команды')
        
        match_info = match_data.get('match_info', {})
        competition = match_info.get('competition', '').lower()
        if any(word in competition for word in ['cup', 'friendly']):
            factors.append('Непредсказуемый формат турнира')
        
        return factors

# Пример использования
if __name__ == "__main__":
    analyzer = AdvancedBetAnalyzer()
    
    # Пример данных матча
    sample_match = {
        'match_info': {
            'id': 'test_1',
            'home_team': 'Real Madrid',
            'away_team': 'Barcelona',
            'competition': 'La Liga',
            'date': '2025-06-28'
        },
        'home_stats': {
            'recent_form': ['W', 'W', 'D', 'W', 'L'],
            'goals_scored': 35,
            'goals_conceded': 18,
            'avg_goals_per_game': 2.3,
            'home_record': {'wins': 8, 'draws': 3, 'losses': 2},
            'injuries': [{'player': 'Player A'}]
        },
        'away_stats': {
            'recent_form': ['L', 'W', 'W', 'D', 'W'],
            'goals_scored': 28,
            'goals_conceded': 22,
            'avg_goals_per_game': 1.9,
            'away_record': {'wins': 6, 'draws': 4, 'losses': 3},
            'injuries': []
        },
        'h2h': {
            'total_matches': 12,
            'team1_wins': 6,
            'team2_wins': 4,
            'draws': 2,
            'avg_goals_per_game': 2.8
        },
        'odds': {
            'average_odds': {'home': 1.85, 'draw': 3.40, 'away': 4.20}
        }
    }
    
    result = analyzer.analyze_match_comprehensive(sample_match)
    print(json.dumps(result, indent=2, ensure_ascii=False)) 