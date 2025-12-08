import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import joblib
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

class AdvancedPredictionModel:
    """Продвинутая модель прогнозирования с учетом множества факторов"""
    
    def __init__(self):
        # Ансамбль моделей для повышения точности
        self.models = {
            'random_forest': RandomForestClassifier(n_estimators=100, random_state=42),
            'gradient_boost': GradientBoostingClassifier(n_estimators=100, random_state=42),
            'logistic': LogisticRegression(random_state=42, max_iter=1000)
        }
        
        self.scaler = StandardScaler()
        self.is_trained = False
        self.feature_importance = {}
        self.model_weights = {'random_forest': 0.4, 'gradient_boost': 0.4, 'logistic': 0.2}
        
    def prepare_advanced_features(self, home_team_stats: Dict, away_team_stats: Dict, match_info: Dict) -> pd.DataFrame:
        """Подготавливает расширенный набор фичей"""
        features = {}
        
        # === ОСНОВНЫЕ СТАТИСТИКИ ===
        # Голы
        features['home_goals_per_game'] = home_team_stats.get('goals_per_game', 1.5)
        features['away_goals_per_game'] = away_team_stats.get('goals_per_game', 1.5)
        features['home_goals_against'] = home_team_stats.get('goals_against', 1.3)
        features['away_goals_against'] = away_team_stats.get('goals_against', 1.3)
        
        # Атакующая сила vs Защитная сила
        features['home_attack_vs_away_defense'] = features['home_goals_per_game'] / max(features['away_goals_against'], 0.5)
        features['away_attack_vs_home_defense'] = features['away_goals_per_game'] / max(features['home_goals_against'], 0.5)
        
        # === ФОРМА КОМАНД ===
        home_form = home_team_stats.get('recent_form', ['D', 'D', 'D', 'D', 'D'])
        away_form = away_team_stats.get('recent_form', ['D', 'D', 'D', 'D', 'D'])
        
        # Очки в последних играх (W=3, D=1, L=0)
        home_form_points = sum([3 if r == 'W' else 1 if r == 'D' else 0 for r in home_form])
        away_form_points = sum([3 if r == 'W' else 1 if r == 'D' else 0 for r in away_form])
        
        features['home_form_points'] = home_form_points
        features['away_form_points'] = away_form_points
        features['form_difference'] = home_form_points - away_form_points
        
        # === ДОМАШНИЕ/ВЫЕЗДНЫЕ РЕЗУЛЬТАТЫ ===
        home_record = home_team_stats.get('home_record', {'W': 5, 'D': 5, 'L': 5})
        away_record = away_team_stats.get('away_record', {'W': 5, 'D': 5, 'L': 5})
        
        home_home_games = sum(home_record.values())
        away_away_games = sum(away_record.values())
        
        features['home_home_win_rate'] = home_record['W'] / max(home_home_games, 1)
        features['away_away_win_rate'] = away_record['W'] / max(away_away_games, 1)
        
        # === ДОПОЛНИТЕЛЬНЫЕ СТАТИСТИКИ ===
        features['home_possession'] = home_team_stats.get('possession', 50.0)
        features['away_possession'] = away_team_stats.get('possession', 50.0)
        features['possession_difference'] = features['home_possession'] - features['away_possession']
        
        features['home_shots_per_game'] = home_team_stats.get('shots_per_game', 12.0)
        features['away_shots_per_game'] = away_team_stats.get('shots_per_game', 12.0)
        
        features['home_pass_accuracy'] = home_team_stats.get('pass_accuracy', 80.0)
        features['away_pass_accuracy'] = away_team_stats.get('pass_accuracy', 80.0)
        
        # === МОТИВАЦИЯ И ТРАВМЫ ===
        features['home_motivation'] = home_team_stats.get('motivation', 0.5)
        features['away_motivation'] = away_team_stats.get('motivation', 0.5)
        features['motivation_difference'] = features['home_motivation'] - features['away_motivation']
        
        home_injuries_data = home_team_stats.get('injuries', [])
        away_injuries_data = away_team_stats.get('injuries', [])
        
        # Проверяем тип данных о травмах
        if isinstance(home_injuries_data, list):
            home_injuries = len(home_injuries_data)
        else:
            home_injuries = int(home_injuries_data) if home_injuries_data else 0
            
        if isinstance(away_injuries_data, list):
            away_injuries = len(away_injuries_data)
        else:
            away_injuries = int(away_injuries_data) if away_injuries_data else 0
        
        features['home_injuries'] = home_injuries
        features['away_injuries'] = away_injuries
        features['injury_impact'] = away_injuries - home_injuries  # Положительное значение = преимущество дома
        
        # === КОЭФФИЦИЕНТЫ КАК ФИЧИ ===
        odds = match_info.get('odds', {'home': 2.0, 'draw': 3.0, 'away': 3.0})
        features['odds_home'] = odds.get('home', 2.0)
        features['odds_draw'] = odds.get('draw', 3.0)  
        features['odds_away'] = odds.get('away', 3.0)
        
        # Имплицитные вероятности от букмекеров
        total_prob = (1/features['odds_home']) + (1/features['odds_draw']) + (1/features['odds_away'])
        features['bookmaker_home_prob'] = (1/features['odds_home']) / total_prob
        features['bookmaker_away_prob'] = (1/features['odds_away']) / total_prob
        features['bookmaker_draw_prob'] = (1/features['odds_draw']) / total_prob
        
        # === КОМБИНИРОВАННЫЕ ИНДИКАТОРЫ ===
        # Общая сила команд
        features['home_team_strength'] = (
            features['home_goals_per_game'] * 0.3 +
            (2 - features['home_goals_against']) * 0.3 +
            features['home_form_points'] * 0.1 +
            features['home_home_win_rate'] * 0.2 +
            features['home_motivation'] * 0.1
        )
        
        features['away_team_strength'] = (
            features['away_goals_per_game'] * 0.3 +
            (2 - features['away_goals_against']) * 0.3 +
            features['away_form_points'] * 0.1 +
            features['away_away_win_rate'] * 0.2 +
            features['away_motivation'] * 0.1
        )
        
        features['strength_difference'] = features['home_team_strength'] - features['away_team_strength']
        
        # Преимущество дома (всегда +0.3 к силе домашней команды)
        features['home_advantage'] = 0.3
        features['adjusted_strength_diff'] = features['strength_difference'] + features['home_advantage']
        
        return pd.DataFrame([features])
    
    def generate_training_data(self, num_samples: int = 1000) -> Tuple[pd.DataFrame, np.array]:
        """Генерирует тренировочные данные на основе реалистичных сценариев"""
        np.random.seed(42)
        training_data = []
        labels = []
        
        for _ in range(num_samples):
            # Генерируем случайные, но реалистичные характеристики команд
            home_strength = np.random.normal(0.6, 0.2)  # 0.2 - 1.0
            away_strength = np.random.normal(0.5, 0.2)  # 0.1 - 0.9
            
            # Домашнее преимущество
            home_advantage = 0.3
            
            # Генерируем статистики на основе силы
            home_stats = {
                'goals_per_game': max(0.5, home_strength * 3 + np.random.normal(0, 0.3)),
                'goals_against': max(0.3, (1 - home_strength) * 2 + np.random.normal(0, 0.2)),
                'possession': max(30, min(70, home_strength * 100 + np.random.normal(0, 10))),
                'shots_per_game': max(5, home_strength * 20 + np.random.normal(0, 3)),
                'pass_accuracy': max(60, min(95, home_strength * 100 + np.random.normal(0, 5))),
                'recent_form': self._generate_form(home_strength),
                'home_record': self._generate_record(home_strength + home_advantage),
                'motivation': max(0.1, min(1.0, home_strength + np.random.normal(0, 0.2))),
                'injuries': np.random.poisson(1)
            }
            
            away_stats = {
                'goals_per_game': max(0.5, away_strength * 3 + np.random.normal(0, 0.3)),
                'goals_against': max(0.3, (1 - away_strength) * 2 + np.random.normal(0, 0.2)),
                'possession': max(30, min(70, away_strength * 100 + np.random.normal(0, 10))),
                'shots_per_game': max(5, away_strength * 20 + np.random.normal(0, 3)),
                'pass_accuracy': max(60, min(95, away_strength * 100 + np.random.normal(0, 5))),
                'recent_form': self._generate_form(away_strength),
                'away_record': self._generate_record(away_strength),
                'motivation': max(0.1, min(1.0, away_strength + np.random.normal(0, 0.2))),
                'injuries': np.random.poisson(1)
            }
            
            # Генерируем коэффициенты на основе силы команд
            strength_diff = (home_strength + home_advantage) - away_strength
            odds = self._generate_realistic_odds(strength_diff)
            
            match_info = {'odds': odds}
            
            # Создаем фичи
            features = self.prepare_advanced_features(home_stats, away_stats, match_info)
            training_data.append(features.iloc[0])
            
            # Определяем результат на основе силы команд и случайности
            total_strength = home_strength + home_advantage + away_strength
            home_win_prob = (home_strength + home_advantage) / total_strength
            away_win_prob = away_strength / total_strength
            draw_prob = 1 - home_win_prob - away_win_prob
            
            # Добавляем случайность
            rand = np.random.random()
            if rand < home_win_prob * 0.7:  # 70% от расчетной вероятности
                result = 'home_win'
            elif rand < home_win_prob * 0.7 + away_win_prob * 0.7:
                result = 'away_win'
            else:
                result = 'draw'
                
            labels.append(result)
        
        return pd.DataFrame(training_data), np.array(labels)
    
    def _generate_form(self, strength: float) -> List[str]:
        """Генерирует форму команды на основе её силы"""
        form = []
        for _ in range(5):
            rand = np.random.random()
            if rand < strength * 0.6:
                form.append('W')
            elif rand < strength * 0.6 + 0.25:
                form.append('D')
            else:
                form.append('L')
        return form
    
    def _generate_record(self, strength: float) -> Dict:
        """Генерирует домашний/выездной рекорд"""
        total_games = 15
        wins = int(strength * total_games * 0.8)
        losses = int((1 - strength) * total_games * 0.6)
        draws = total_games - wins - losses
        
        return {'W': max(0, wins), 'D': max(0, draws), 'L': max(0, losses)}
    
    def _generate_realistic_odds(self, strength_diff: float) -> Dict:
        """Генерирует реалистичные коэффициенты"""
        if strength_diff > 0.4:
            return {'home': 1.6, 'draw': 3.8, 'away': 4.5}
        elif strength_diff > 0.2:
            return {'home': 1.9, 'draw': 3.4, 'away': 3.8}
        elif strength_diff > 0:
            return {'home': 2.2, 'draw': 3.1, 'away': 3.2}
        elif strength_diff > -0.2:
            return {'home': 2.8, 'draw': 3.0, 'away': 2.4}
        elif strength_diff > -0.4:
            return {'home': 3.5, 'draw': 3.2, 'away': 1.9}
        else:
            return {'home': 4.2, 'draw': 3.6, 'away': 1.7}
    
    def train_models(self):
        """Обучает ансамбль моделей"""
        print("🤖 Обучение продвинутой модели прогнозирования...")
        
        # Генерируем тренировочные данные
        X, y = self.generate_training_data(2000)
        
        # Разделяем на тренировочную и тестовую выборки
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Масштабируем фичи
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Обучаем каждую модель
        model_scores = {}
        
        for name, model in self.models.items():
            print(f"   Обучение {name}...")
            
            if name == 'logistic':
                model.fit(X_train_scaled, y_train)
                y_pred = model.predict(X_test_scaled)
            else:
                model.fit(X_train, y_train) 
                y_pred = model.predict(X_test)
            
            accuracy = accuracy_score(y_test, y_pred)
            model_scores[name] = accuracy
            print(f"   {name}: точность {accuracy:.3f}")
            
            # Сохраняем важность фичей для Random Forest
            if name == 'random_forest':
                feature_names = X_train.columns
                importance = model.feature_importances_
                self.feature_importance = dict(zip(feature_names, importance))
        
        # Корректируем веса моделей на основе их производительности
        total_score = sum(model_scores.values())
        for name in self.model_weights:
            self.model_weights[name] = model_scores[name] / total_score
            
        self.is_trained = True
        
        avg_accuracy = np.mean(list(model_scores.values()))
        print(f"✅ Модель обучена! Средняя точность: {avg_accuracy:.3f}")
        
        # Выводим топ-10 важных фичей
        if self.feature_importance:
            sorted_features = sorted(self.feature_importance.items(), key=lambda x: x[1], reverse=True)
            print("\n📊 Топ-10 важных факторов:")
            for feature, importance in sorted_features[:10]:
                print(f"   {feature}: {importance:.3f}")
        
        return avg_accuracy
    
    def predict_match_advanced(self, home_team_stats: Dict, away_team_stats: Dict, match_info: Dict) -> Dict:
        """Делает продвинутый прогноз матча"""
        if not self.is_trained:
            self.train_models()
        
        # Подготавливаем фичи
        features = self.prepare_advanced_features(home_team_stats, away_team_stats, match_info)
        
        # Получаем предсказания от каждой модели
        predictions = {}
        probabilities = {}
        
        for name, model in self.models.items():
            if name == 'logistic':
                features_scaled = self.scaler.transform(features)
                pred = model.predict(features_scaled)[0]
                prob = model.predict_proba(features_scaled)[0]
            else:
                pred = model.predict(features)[0]
                prob = model.predict_proba(features)[0]
            
            predictions[name] = pred
            probabilities[name] = dict(zip(model.classes_, prob))
        
        # Взвешенное голосование
        final_probabilities = {'home_win': 0, 'draw': 0, 'away_win': 0}
        
        for name, weight in self.model_weights.items():
            model_probs = probabilities[name]
            for outcome in final_probabilities:
                if outcome in model_probs:
                    final_probabilities[outcome] += model_probs[outcome] * weight
        
        # Определяем финальный прогноз
        final_prediction = max(final_probabilities, key=final_probabilities.get)
        confidence = final_probabilities[final_prediction]
        
        # Рассчитываем value bet (математическое ожидание)
        odds = match_info.get('odds', {'home': 2.0, 'draw': 3.0, 'away': 3.0})
        
        value_bets = {}
        odds_mapping = {'home_win': 'home', 'draw': 'draw', 'away_win': 'away'}
        
        for outcome, prob in final_probabilities.items():
            odds_key = odds_mapping[outcome]
            if odds_key in odds:
                implied_prob = 1 / odds[odds_key]
                if prob > implied_prob * 1.05:  # 5% маржа
                    value = (prob * odds[odds_key]) - 1
                    if value > 0.05:  # Минимальное value 5%
                        value_bets[outcome] = {
                            'value': value,
                            'our_probability': prob,
                            'bookmaker_probability': implied_prob,
                            'odds': odds[odds_key]
                        }
        
        return {
            'prediction': final_prediction,
            'confidence': confidence,
            'probabilities': final_probabilities,
            'value_bets': value_bets,
            'model_agreement': len(set(predictions.values())) == 1,  # Согласны ли все модели
            'feature_analysis': self._analyze_key_factors(features.iloc[0])
        }
    
    def _analyze_key_factors(self, features: pd.Series) -> Dict:
        """Анализирует ключевые факторы матча"""
        analysis = {}
        
        # Сила команд
        strength_diff = features.get('adjusted_strength_diff', 0)
        if strength_diff > 0.3:
            analysis['strength'] = "Сильное преимущество дома"
        elif strength_diff > 0.1:
            analysis['strength'] = "Небольшое преимущество дома"
        elif strength_diff < -0.3:
            analysis['strength'] = "Сильное преимущество гостей"
        elif strength_diff < -0.1:
            analysis['strength'] = "Небольшое преимущество гостей"
        else:
            analysis['strength'] = "Равные силы"
        
        # Форма
        form_diff = features.get('form_difference', 0)
        if abs(form_diff) > 6:
            better_form = "дома" if form_diff > 0 else "у гостей"
            analysis['form'] = f"Значительно лучше форма {better_form}"
        
        # Мотивация
        motivation_diff = features.get('motivation_difference', 0)
        if abs(motivation_diff) > 0.2:
            higher_motivation = "у домашних" if motivation_diff > 0 else "у гостей"
            analysis['motivation'] = f"Выше мотивация {higher_motivation}"
        
        # Травмы
        injury_impact = features.get('injury_impact', 0)
        if injury_impact > 1:
            analysis['injuries'] = "Больше травм у гостей"
        elif injury_impact < -1:
            analysis['injuries'] = "Больше травм у хозяев"
        
        return analysis 