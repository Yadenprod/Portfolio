import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from typing import Dict, List, Tuple
import warnings
import json
import logging

logger = logging.getLogger(__name__)

class CSGOPredictionModel:
    """Модель прогнозирования матчей CS:GO"""
    
    def __init__(self):
        # Инициализируем модели
        self.random_forest = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.gradient_boost = GradientBoostingClassifier(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            random_state=42
        )
        self.logistic = LogisticRegression(
            random_state=42,
            max_iter=1000
        )
        
        # Загружаем исторические данные
        self.historical_data = self._load_historical_data()
        
        # Обучаем модели
        self._train_models()
        
    def _load_historical_data(self) -> List[Dict]:
        """Загружает исторические данные матчей"""
        try:
            with open('historical_csgo_matches.json', 'r') as f:
                data = json.load(f)
                return data.get('matches', [])
        except FileNotFoundError:
            print("⚠️ Файл с историческими данными не найден")
            return []
        except Exception as e:
            logger.error(f"Ошибка загрузки исторических данных: {e}")
            return []
            
    def _train_models(self):
        """Обучает модели на исторических данных"""
        if not self.historical_data:
            print("⚠️ Нет данных для обучения")
            return
            
        try:
            # Подготавливаем данные
            X = []
            y = []
            
            for match in self.historical_data:
                features = self._extract_features(
                    match['team1_stats'],
                    match['team2_stats'],
                    match['match_info']
                )
                X.append(features)
                y.append(1 if match['winner'] == 'team1' else 0)
            
            X = np.array(X)
            y = np.array(y)
            
            # Разделяем данные
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Обучаем модели
            print("🎮 Обучение CS:GO модели прогнозирования...")
            
            print("   Обучение random_forest...")
            self.random_forest.fit(X_train, y_train)
            rf_score = self.random_forest.score(X_test, y_test)
            print(f"   random_forest: точность {rf_score:.3f}")
            
            print("   Обучение gradient_boost...")
            self.gradient_boost.fit(X_train, y_train)
            gb_score = self.gradient_boost.score(X_test, y_test)
            print(f"   gradient_boost: точность {gb_score:.3f}")
            
            print("   Обучение logistic...")
            self.logistic.fit(X_train, y_train)
            log_score = self.logistic.score(X_test, y_test)
            print(f"   logistic: точность {log_score:.3f}")
            
            avg_score = (rf_score + gb_score + log_score) / 3
            print(f"✅ CS:GO модель обучена! Средняя точность: {avg_score:.3f}")
            
        except Exception as e:
            logger.error(f"Ошибка обучения моделей: {e}")
            
    def predict_cs_match(self, team1_stats: Dict, team2_stats: Dict, match: Dict) -> Dict:
        """Прогнозирует исход матча CS:GO"""
        try:
            # Извлекаем признаки
            features = self._extract_features(team1_stats, team2_stats, match)
            features = np.array([features])
            
            # Получаем предсказания от каждой модели
            rf_pred = self.random_forest.predict_proba(features)[0]
            gb_pred = self.gradient_boost.predict_proba(features)[0]
            log_pred = self.logistic.predict_proba(features)[0]
            
            # Усредняем вероятности
            team1_prob = (rf_pred[1] + gb_pred[1] + log_pred[1]) / 3
            team2_prob = 1 - team1_prob
            
            # Определяем победителя
            prediction = "Первая команда" if team1_prob > team2_prob else "Вторая команда"
            confidence = max(team1_prob, team2_prob)
            
            # Анализируем value
            value_bets = self._analyze_value_bets(
                team1_prob, team2_prob,
                match.get('odds', {'team1': 2.0, 'team2': 2.0})
            )
            
            # Показываем важные факторы
            self._show_important_features(team1_stats, team2_stats)
            
            return {
                'prediction': prediction,
                'confidence': confidence,
                'probabilities': {
                    'team1_win': team1_prob,
                    'team2_win': team2_prob
                },
                'value_bets': value_bets
            }
            
        except Exception as e:
            logger.error(f"Ошибка прогнозирования: {e}")
            return {
                'prediction': "Ошибка прогноза",
                'confidence': 0.0,
                'probabilities': {'team1_win': 0.5, 'team2_win': 0.5},
                'value_bets': []
            }
            
    def _extract_features(self, team1_stats: Dict, team2_stats: Dict, match: Dict) -> List[float]:
        """Извлекает признаки для прогнозирования"""
        features = []
        
        # Рейтинги команд
        features.append(team1_stats.get('rating', 1.0))
        features.append(team2_stats.get('rating', 1.0))
        features.append(team1_stats.get('rating', 1.0) - team2_stats.get('rating', 1.0))
        
        # Винрейты
        features.append(team1_stats.get('map_win_rate', 0.5))
        features.append(team2_stats.get('map_win_rate', 0.5))
        features.append(team1_stats.get('map_win_rate', 0.5) - team2_stats.get('map_win_rate', 0.5))
        
        # Пистолетные раунды
        features.append(team1_stats.get('pistol_win_rate', 0.5))
        features.append(team2_stats.get('pistol_win_rate', 0.5))
        features.append(team1_stats.get('pistol_win_rate', 0.5) - team2_stats.get('pistol_win_rate', 0.5))
        
        # Клатчи
        features.append(team1_stats.get('clutch_success', 0.4))
        features.append(team2_stats.get('clutch_success', 0.4))
        features.append(team1_stats.get('clutch_success', 0.4) - team2_stats.get('clutch_success', 0.4))
        
        # Форма команд
        team1_form = self._calculate_form_score(team1_stats.get('recent_form', []))
        team2_form = self._calculate_form_score(team2_stats.get('recent_form', []))
        features.append(team1_form)
        features.append(team2_form)
        features.append(team1_form - team2_form)
        
        # Тир команд
        features.append(float(team1_stats.get('tier', 3)))
        features.append(float(team2_stats.get('tier', 3)))
        
        # Формат матча
        format_weight = {
            'BO1': 1.0,
            'BO3': 2.0,
            'BO5': 3.0
        }
        features.append(format_weight.get(match.get('format', 'BO1'), 1.0))
        
        return features
        
    def _calculate_form_score(self, recent_form: List[str]) -> float:
        """Рассчитывает оценку формы команды"""
        if not recent_form:
            return 0.5
            
        weights = [1.0, 0.8, 0.6, 0.4, 0.2]  # Более недавние матчи важнее
        scores = {'W': 1.0, 'L': 0.0, 'D': 0.5}
        
        total_score = 0
        total_weight = 0
        
        for i, result in enumerate(recent_form[:5]):
            total_score += scores.get(result, 0.5) * weights[i]
            total_weight += weights[i]
            
        return total_score / total_weight if total_weight > 0 else 0.5
        
    def _analyze_value_bets(self, team1_prob: float, team2_prob: float, odds: Dict) -> List[Dict]:
        """Анализирует ценность ставок"""
        value_bets = []
        
        # Проверяем ставку на первую команду
        if team1_prob > 0:
            implied_prob = 1 / odds['team1']
            value = (team1_prob - implied_prob) * 100
            
            if value > 4.0:  # Минимальный порог value
                value_bets.append({
                    'team': 'team1',
                    'odds': odds['team1'],
                    'value': value,
                    'our_prob': team1_prob,
                    'bookie_prob': implied_prob
                })
                
        # Проверяем ставку на вторую команду
        if team2_prob > 0:
            implied_prob = 1 / odds['team2']
            value = (team2_prob - implied_prob) * 100
            
            if value > 4.0:
                value_bets.append({
                    'team': 'team2',
                    'odds': odds['team2'],
                    'value': value,
                    'our_prob': team2_prob,
                    'bookie_prob': implied_prob
                })
                
        return value_bets
        
    def _show_important_features(self, team1_stats: Dict, team2_stats: Dict):
        """Показывает важные факторы для прогноза"""
        try:
            feature_importance = self.random_forest.feature_importances_
            features = [
                'team1_overall_strength',
                'team1_clutch_success',
                'team1_map_winrate',
                'team2_clutch_success',
                'team1_pistol_winrate',
                'overall_strength_diff',
                'team2_rating',
                'map_winrate_diff',
                'clutch_advantage',
                'pistol_advantage'
            ]
            
            print("\n🎯 Топ-10 важных факторов для CS:GO:")
            for feature, importance in sorted(zip(features, feature_importance), key=lambda x: x[1], reverse=True)[:10]:
                print(f"   {feature}: {importance:.3f}")
                
        except Exception as e:
            logger.error(f"Ошибка отображения важных факторов: {e}")
            
    def save_match_result(self, match: Dict, actual_winner: str):
        """Сохраняет результат матча в исторические данные"""
        try:
            if not self.historical_data:
                self.historical_data = []
                
            match_data = {
                'match_info': match,
                'team1_stats': match.get('team1_stats', {}),
                'team2_stats': match.get('team2_stats', {}),
                'winner': actual_winner
            }
            
            self.historical_data.append(match_data)
            
            # Сохраняем в файл
            with open('historical_csgo_matches.json', 'w') as f:
                json.dump(self.historical_data, f, indent=2)
                
            # Переобучаем модели
            self._train_models()
            
        except Exception as e:
            logger.error(f"Ошибка сохранения результата: {e}") 