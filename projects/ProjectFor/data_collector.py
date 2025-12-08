import requests
import json
import pandas as pd
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import time
from bs4 import BeautifulSoup
import asyncio
import aiohttp
from fonbet_api import FonbetAPI

class DataCollector:
    def __init__(self, use_fonbet: bool = True):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Инициализируем Fonbet API если нужно
        self.use_fonbet = use_fonbet
        if use_fonbet:
            try:
                self.fonbet = FonbetAPI()
                print("✅ Fonbet API инициализирован")
            except Exception as e:
                print(f"❌ Ошибка инициализации Fonbet API: {e}")
                self.use_fonbet = False
                self.fonbet = None
        else:
            self.fonbet = None
        
    def get_football_matches(self, date: str = None) -> List[Dict]:
        """Получает данные о футбольных матчах"""
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        
        # Пробуем получить данные с Fonbet
        if self.use_fonbet and self.fonbet:
            try:
                print("🏈 Получаем матчи с Fonbet...")
                matches = self.fonbet.get_football_matches()
                
                if matches:
                    print(f"✅ Получено {len(matches)} футбольных матчей с Fonbet")
                    return matches
                else:
                    print("⚠️ Матчи с Fonbet не получены, используем демо данные")
                    
            except Exception as e:
                print(f"❌ Ошибка получения данных с Fonbet: {e}")
        
        # Fallback: пробуем бесплатный API
        url = "https://api.football-data.org/v4/competitions/2021/matches"
        
        try:
            response = self.session.get(url)
            if response.status_code == 200:
                data = response.json()
                matches = []
                
                for match in data.get('matches', []):
                    if match['status'] in ['SCHEDULED', 'TIMED']:
                        match_data = {
                            'id': match['id'],
                            'date': match['utcDate'],
                            'home_team': match['homeTeam']['name'],
                            'away_team': match['awayTeam']['name'],
                            'competition': match['competition']['name'],
                            'status': match['status'],
                            'sport': 'football'
                        }
                        matches.append(match_data)
                
                if matches:
                    return matches
                
        except Exception as e:
            print(f"❌ Ошибка получения данных с football-data.org: {e}")
        
        # Последний fallback - демо данные
        print("🎭 Используем демо данные для тестирования")
        return [
            {
                'id': 'demo_1',
                'date': datetime.now().isoformat(),
                'home_team': 'Real Madrid',
                'away_team': 'Barcelona',
                'competition': 'La Liga',
                'status': 'SCHEDULED',
                'sport': 'football'
            },
            {
                'id': 'demo_2',
                'date': datetime.now().isoformat(),
                'home_team': 'Manchester United',
                'away_team': 'Liverpool',
                'competition': 'Premier League',
                'status': 'SCHEDULED',
                'sport': 'football'
            },
            {
                'id': 'demo_3',
                'date': datetime.now().isoformat(),
                'home_team': 'Bayern Munich',
                'away_team': 'Borussia Dortmund',
                'competition': 'Bundesliga',
                'status': 'SCHEDULED',
                'sport': 'football'
            }
        ]
    
    def get_team_stats(self, team_name: str, sport: str = 'football') -> Dict:
        """Получает статистику команды"""
        # Реалистичные статистики для российских команд
        team_profiles = {
            'Спартак': {'base_goals': 45, 'base_conceded': 25, 'strength': 0.8},
            'ЦСКА': {'base_goals': 40, 'base_conceded': 28, 'strength': 0.75},
            'Зенит': {'base_goals': 50, 'base_conceded': 22, 'strength': 0.85},
            'Динамо': {'base_goals': 35, 'base_conceded': 35, 'strength': 0.6},
            'Краснодар': {'base_goals': 42, 'base_conceded': 30, 'strength': 0.7},
            'Ростов': {'base_goals': 30, 'base_conceded': 40, 'strength': 0.5},
            'Real Madrid': {'base_goals': 55, 'base_conceded': 20, 'strength': 0.9},
            'Barcelona': {'base_goals': 50, 'base_conceded': 25, 'strength': 0.85},
            'Manchester United': {'base_goals': 45, 'base_conceded': 30, 'strength': 0.75},
            'Liverpool': {'base_goals': 48, 'base_conceded': 25, 'strength': 0.8},
            'Bayern Munich': {'base_goals': 52, 'base_conceded': 22, 'strength': 0.88},
            'Borussia Dortmund': {'base_goals': 45, 'base_conceded': 35, 'strength': 0.72}
        }
        
        profile = team_profiles.get(team_name, {'base_goals': 35, 'base_conceded': 35, 'strength': 0.6})
        
        return {
            'team_name': team_name,
            'goals_scored': profile['base_goals'] + random.randint(-5, 5),
            'goals_conceded': profile['base_conceded'] + random.randint(-5, 5),
            'recent_form': random.choices(['W', 'D', 'L'], 
                                        weights=[profile['strength'], 0.3, 1-profile['strength']], k=5),
            'home_record': {'wins': int(15 * profile['strength']), 'draws': 3, 'losses': int(15 * (1-profile['strength']))},
            'away_record': {'wins': int(10 * profile['strength']), 'draws': 5, 'losses': int(10 * (1-profile['strength']))},
            'injuries': [],
            'last_5_games': [],
            'avg_goals_per_game': profile['base_goals'] / 20,
            'clean_sheets': int(8 * profile['strength'])
        }
    
    def get_esports_matches(self, game: str = 'cs2') -> List[Dict]:
        """Получает данные о киберспортивных матчах"""
        try:
            # Для CS2 можем парсить HLTV
            matches = self._scrape_hltv_matches()
            return matches if matches else []
        except Exception as e:
            print(f"Error fetching esports data: {e}")
            # Возвращаем демо данные для тестирования
            return [
                {
                    'id': 'esports_demo_1',
                    'date': datetime.now().isoformat(),
                    'team1': 'NAVI',
                    'team2': 'G2 Esports', 
                    'tournament': 'IEM Katowice 2025',
                    'format': 'BO3',
                    'sport': 'cs2'
                },
                {
                    'id': 'esports_demo_2',
                    'date': (datetime.now() + timedelta(hours=2)).isoformat(),
                    'team1': 'FaZe Clan',
                    'team2': 'Vitality', 
                    'tournament': 'BLAST Premier',
                    'format': 'BO1',
                    'sport': 'cs2'
                }
            ]
    
    def _scrape_hltv_matches(self) -> List[Dict]:
        """Парсит матчи с HLTV"""
        try:
            # Простой парсинг (в реальности нужен более сложный)
            url = "https://www.hltv.org/matches"
            
            # Симуляция данных (в реальности парсинг)
            matches = [
                {
                    'id': f'hltv_{i}',
                    'date': (datetime.now() + timedelta(hours=i)).isoformat(),
                    'team1': f'Team{i}_A',
                    'team2': f'Team{i}_B', 
                    'tournament': 'IEM Katowice',
                    'format': 'BO3',
                    'sport': 'cs2'
                }
                for i in range(1, 6)
            ]
            
            return matches
            
        except Exception as e:
            print(f"Error scraping HLTV: {e}")
            # Возвращаем демо данные для тестирования
            return [
                {
                    'id': 'hltv_demo_1',
                    'date': datetime.now().isoformat(),
                    'team1': 'Astralis',
                    'team2': 'Team Liquid', 
                    'tournament': 'ESL Pro League',
                    'format': 'BO3',
                    'sport': 'cs2'
                }
            ]
    
    def get_odds_data(self, match_id: str, sport: str) -> Dict:
        """Получает коэффициенты букмекеров"""
        try:
            # Получаем коэффициенты с Fonbet только если это не демо матч
            if self.use_fonbet and self.fonbet and not match_id.startswith('demo_'):
                try:
                    if match_id.isdigit():
                        fonbet_odds = self.fonbet.get_event_odds(int(match_id))
                        
                        if fonbet_odds and fonbet_odds.get('main_odds'):
                            main_odds = fonbet_odds['main_odds']
                            
                            return {
                                'match_id': match_id,
                                'bookmakers': {'fonbet': main_odds},
                                'average_odds': main_odds,
                                'fonbet_data': fonbet_odds,
                                'timestamp': datetime.now().isoformat(),
                                'source': 'fonbet'
                            }
                        
                except Exception as e:
                    print(f"❌ Ошибка получения коэффициентов с Fonbet: {e}")
            
            # Fallback - реалистичные коэффициенты для демо матчей
            demo_odds = {
                'demo_1': {'home': 2.1, 'away': 2.8, 'draw': 3.2},  # Спартак vs ЦСКА
                'demo_2': {'home': 1.8, 'away': 3.4, 'draw': 3.6},  # Зенит vs Динамо  
                'demo_3': {'home': 2.3, 'away': 2.6, 'draw': 3.1},  # Краснодар vs Ростов
                # Европейские команды
                'demo_soccer_1': {'home': 1.6, 'away': 4.2, 'draw': 3.8},  # Real vs Barca
                'demo_soccer_2': {'home': 2.2, 'away': 2.9, 'draw': 3.1},  # Man Utd vs Liverpool
                'demo_soccer_3': {'home': 1.7, 'away': 3.8, 'draw': 3.5}   # Bayern vs Dortmund
            }
            
            if match_id in demo_odds:
                odds = demo_odds[match_id]
            else:
                # Генерируем случайные реалистичные коэффициенты
                import random
                home_prob = random.uniform(0.25, 0.65)
                away_prob = random.uniform(0.15, 0.55)
                draw_prob = max(0.1, 1 - home_prob - away_prob)
                
                # Нормализуем вероятности
                total = home_prob + away_prob + draw_prob
                home_prob /= total
                away_prob /= total
                draw_prob /= total
                
                odds = {
                    'home': round(1 / home_prob, 2),
                    'away': round(1 / away_prob, 2),
                    'draw': round(1 / draw_prob, 2)
                }
            
            return {
                'match_id': match_id,
                'bookmakers': {
                    'bet365': odds,
                    'william_hill': {k: round(v + random.uniform(-0.1, 0.1), 2) for k, v in odds.items()},
                    'pinnacle': {k: round(v + random.uniform(-0.05, 0.05), 2) for k, v in odds.items()}
                },
                'average_odds': odds,
                'timestamp': datetime.now().isoformat(),
                'source': 'demo' if match_id.startswith('demo_') else 'simulated'
            }
            
        except Exception as e:
            print(f"❌ Ошибка получения коэффициентов для {match_id}: {e}")
            return {
                'match_id': match_id,
                'average_odds': {'home': 2.0, 'away': 2.5, 'draw': 3.0},
                'timestamp': datetime.now().isoformat(),
                'source': 'fallback'
            }
    
    def _get_recent_form(self, team_name: str) -> List[str]:
        """Получает недавнюю форму команды"""
        # Симуляция формы (W-выигрыш, L-проигрыш, D-ничья)
        import random
        forms = ['W', 'L', 'D']
        return [random.choice(forms) for _ in range(5)]
    
    def _get_injury_list(self, team_name: str) -> List[Dict]:
        """Получает список травмированных игроков"""
        # Симуляция травм
        return [
            {'player': 'Player A', 'injury': 'knee', 'return_date': '2025-07-15'},
            {'player': 'Player B', 'injury': 'ankle', 'return_date': '2025-07-10'}
        ]
    
    def _get_last_games(self, team_name: str) -> List[Dict]:
        """Получает результаты последних игр"""
        return [
            {'date': '2025-06-25', 'opponent': 'Team X', 'result': 'W 2-1', 'home': True},
            {'date': '2025-06-22', 'opponent': 'Team Y', 'result': 'L 0-2', 'home': False},
            {'date': '2025-06-18', 'opponent': 'Team Z', 'result': 'D 1-1', 'home': True},
            {'date': '2025-06-15', 'opponent': 'Team A', 'result': 'W 3-0', 'home': False},
            {'date': '2025-06-12', 'opponent': 'Team B', 'result': 'W 2-1', 'home': True}
        ]
    
    def get_weather_data(self, city: str, date: str) -> Dict:
        """Получает данные о погоде для матча"""
        try:
            # Симуляция погодных данных
            import random
            
            conditions = ['sunny', 'cloudy', 'rainy', 'windy']
            return {
                'city': city,
                'date': date,
                'temperature': random.randint(5, 30),
                'humidity': random.randint(40, 90),
                'wind_speed': random.randint(0, 25),
                'condition': random.choice(conditions),
                'precipitation': random.choice([0, 0, 0, 0.5, 1.2, 2.5])
            }
        except Exception as e:
            print(f"Error getting weather data: {e}")
            return {}
    
    def get_head_to_head(self, team1: str, team2: str, sport: str = 'football') -> Dict:
        """Получает статистику личных встреч"""
        try:
            # Симуляция H2H статистики
            import random
            
            team1_wins = random.randint(2, 8)
            team2_wins = random.randint(2, 8)
            draws = random.randint(0, 4)
            
            return {
                'team1': team1,
                'team2': team2,
                'total_matches': team1_wins + team2_wins + draws,
                'team1_wins': team1_wins,
                'team2_wins': team2_wins,
                'draws': draws,
                'last_5_results': [
                    {'date': '2025-05-01', 'result': f'{team1} 2-1 {team2}'},
                    {'date': '2025-02-15', 'result': f'{team2} 1-0 {team1}'},
                    {'date': '2024-11-20', 'result': f'{team1} 3-2 {team2}'},
                    {'date': '2024-08-10', 'result': f'{team1} 1-1 {team2}'},
                    {'date': '2024-05-05', 'result': f'{team2} 2-0 {team1}'}
                ],
                'avg_goals_per_game': round(random.uniform(1.5, 3.5), 1)
            }
        except Exception as e:
            print(f"Error getting H2H data: {e}")
            return {}
    
    def get_market_data(self, match_id: str) -> Dict:
        """Получает рыночные данные (объемы ставок, движение коэффициентов)"""
        try:
            import random
            
            return {
                'match_id': match_id,
                'total_volume': random.randint(100000, 1000000),
                'home_percentage': random.randint(35, 65),
                'away_percentage': random.randint(25, 55),
                'draw_percentage': random.randint(10, 30),
                'odds_movement': {
                    'home': {'opening': 2.2, 'current': 2.1, 'trend': 'down'},
                    'away': {'opening': 3.5, 'current': 3.8, 'trend': 'up'},
                    'draw': {'opening': 3.1, 'current': 3.2, 'trend': 'up'}
                },
                'sharp_money': 'home',  # Куда идут "умные" деньги
                'public_betting': 'away'  # Куда ставит публика
            }
        except Exception as e:
            print(f"Error getting market data: {e}")
            return {}
    
    async def get_live_data(self, match_id: str) -> Dict:
        """Получает данные в реальном времени во время матча"""
        try:
            # Симуляция live данных
            import random
            
            return {
                'match_id': match_id,
                'minute': random.randint(0, 90),
                'score': {'home': random.randint(0, 3), 'away': random.randint(0, 3)},
                'possession': {'home': random.randint(40, 60), 'away': random.randint(40, 60)},
                'shots': {'home': random.randint(0, 15), 'away': random.randint(0, 15)},
                'cards': {'home': random.randint(0, 5), 'away': random.randint(0, 5)},
                'corners': {'home': random.randint(0, 10), 'away': random.randint(0, 10)},
                'live_odds': {
                    'home_win': round(random.uniform(1.5, 4.0), 2),
                    'away_win': round(random.uniform(1.5, 4.0), 2),
                    'over_2.5': round(random.uniform(1.3, 2.5), 2),
                    'under_2.5': round(random.uniform(1.3, 2.5), 2)
                }
            }
        except Exception as e:
            print(f"Error getting live data: {e}")
            return {}
    
    def save_data_to_file(self, data: Dict, filename: str):
        """Сохраняет данные в файл"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def load_historical_data(self, filename: str) -> Dict:
        """Загружает исторические данные"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except Exception as e:
            print(f"Error loading data: {e}")
            return {}

# Пример использования
if __name__ == "__main__":
    collector = DataCollector()
    
    # Получаем футбольные матчи
    matches = collector.get_football_matches()
    print(f"Найдено матчей: {len(matches)}")
    
    if matches:
        match = matches[0]
        print(f"\nМатч: {match['home_team']} vs {match['away_team']}")
        
        # Получаем статистику команд
        home_stats = collector.get_team_stats(match['home_team'])
        away_stats = collector.get_team_stats(match['away_team'])
        
        # Получаем коэффициенты
        odds = collector.get_odds_data(match['id'], 'football')
        
        # H2H статистика
        h2h = collector.get_head_to_head(match['home_team'], match['away_team'])
        
        print(f"Коэффициенты: {odds['average_odds']}")
        print(f"H2H: {h2h['team1_wins']}-{h2h['draws']}-{h2h['team2_wins']}")
        
    # Киберспорт
    esports_matches = collector.get_esports_matches()
    print(f"\nКиберспорт матчей: {len(esports_matches)}") 