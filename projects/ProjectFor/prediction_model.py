import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import pickle
from typing import Dict, Tuple

class SportsPredictionModel:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
        
    def prepare_features(self, match_data: Dict) -> pd.DataFrame:
        """Подготавливает фичи для модели"""
        features = {}
        
        # Основные статистики команд
        home_stats = match_data.get('home_stats', {})
        away_stats = match_data.get('away_stats', {})
        
        # Фичи домашней команды (используем те же названия что в generate_training_data)
        features['home_goals_scored'] = home_stats.get('goals_scored', 35)
        features['home_goals_conceded'] = home_stats.get('goals_conceded', 30)
        
        # Гостевая команда
        features['away_goals_scored'] = away_stats.get('goals_scored', 30)
        features['away_goals_conceded'] = away_stats.get('goals_conceded', 35)
        
        # Рассчитанные фичи (делаем это после основных)
        features['home_goal_diff'] = features['home_goals_scored'] - features['home_goals_conceded']
        features['away_goal_diff'] = features['away_goals_scored'] - features['away_goals_conceded']
        
        # Форма команд
        home_form = home_stats.get('recent_form', ['W', 'W', 'D'])
        features['home_wins_last_5'] = home_form.count('W') if home_form else 2
        
        away_form = away_stats.get('recent_form', ['W', 'D', 'L'])
        features['away_wins_last_5'] = away_form.count('W') if away_form else 1
        
        # H2H статистика
        h2h = match_data.get('h2h', {})
        features['h2h_home_wins'] = h2h.get('team1_wins', 3)
        features['h2h_away_wins'] = h2h.get('team2_wins', 2)
        
        # Коэффициенты
        odds = match_data.get('odds', {}).get('average_odds', {})
        features['odds_home'] = odds.get('home', 2.1)
        features['odds_away'] = odds.get('away', 2.8)
        
        # Рыночные данные
        market = match_data.get('market_data', {})
        features['home_percentage'] = market.get('home_percentage', 55)
        
        return pd.DataFrame([features])
    
    def generate_training_data(self, num_samples: int = 1000) -> Tuple[pd.DataFrame, pd.Series]:
        """Генерирует тренировочные данные"""
        np.random.seed(42)
        
        data = []
        labels = []
        
        for i in range(num_samples):
            sample = {
                'home_goals_scored': np.random.randint(20, 80),
                'home_goals_conceded': np.random.randint(15, 60),
                'away_goals_scored': np.random.randint(15, 70),
                'away_goals_conceded': np.random.randint(20, 65),
                'home_wins_last_5': np.random.randint(0, 6),
                'away_wins_last_5': np.random.randint(0, 6),
                'h2h_home_wins': np.random.randint(0, 10),
                'h2h_away_wins': np.random.randint(0, 10),
                'odds_home': np.random.uniform(1.2, 5.0),
                'odds_away': np.random.uniform(1.2, 5.0),
                'home_percentage': np.random.randint(20, 80)
            }
            
            # Рассчитанные фичи
            sample['home_goal_diff'] = sample['home_goals_scored'] - sample['home_goals_conceded']
            sample['away_goal_diff'] = sample['away_goals_scored'] - sample['away_goals_conceded']
            
            # Логичный исход
            home_strength = (
                (sample['home_goal_diff'] - sample['away_goal_diff']) * 0.3 +
                (sample['home_wins_last_5'] - sample['away_wins_last_5']) * 0.2 +
                (1 / sample['odds_home']) * 0.3 +
                sample['home_percentage'] / 100 * 0.2
            )
            
            if home_strength > 0.6:
                outcome = 'home_win'
            elif home_strength < 0.3:
                outcome = 'away_win'
            else:
                outcome = 'draw'
            
            data.append(sample)
            labels.append(outcome)
        
        return pd.DataFrame(data), pd.Series(labels)
    
    def train_model(self):
        """Обучает модель"""
        print("Генерируем тренировочные данные...")
        X, y = self.generate_training_data(1000)
        
        print("Обучение модели...")
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        self.model.fit(X_train, y_train)
        
        # Проверяем точность
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Точность модели: {accuracy:.3f}")
        
        self.is_trained = True
        return accuracy
    
    def predict_match(self, match_data: Dict) -> Dict:
        """Предсказывает исход матча"""
        if not self.is_trained:
            self.train_model()
        
        features = self.prepare_features(match_data)
        
        # Убеждаемся что порядок колонок правильный
        expected_columns = [
            'home_goals_scored', 'home_goals_conceded', 'away_goals_scored', 
            'away_goals_conceded', 'home_wins_last_5', 'away_wins_last_5',
            'h2h_home_wins', 'h2h_away_wins', 'odds_home', 'odds_away',
            'home_percentage', 'home_goal_diff', 'away_goal_diff'
        ]
        
        # Переупорядочиваем колонки в правильном порядке
        features = features[expected_columns]
        
        prediction = self.model.predict(features)[0]
        probabilities = self.model.predict_proba(features)[0]
        
        classes = self.model.classes_
        prob_dict = dict(zip(classes, probabilities))
        
        confidence = max(probabilities)
        
        return {
            'prediction': prediction,
            'confidence': confidence,
            'probabilities': prob_dict
        }
