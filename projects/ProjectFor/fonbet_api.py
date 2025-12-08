#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Модуль для работы с Fonbet API
Получение матчей, коэффициентов и размещение ставок
"""

import requests
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging
from bs4 import BeautifulSoup
import re

logger = logging.getLogger(__name__)

class FonbetAPI:
    def __init__(self):
        # Используем альтернативные рабочие домены
        self.base_url = "https://www.fonbet.ru"
        self.public_api = "https://www.fonbet.ru/api/v1"
        
        # Fallback домены если основной не работает
        self.fallback_domains = [
            "https://fonbet1.com",
            "https://fonbet2.com", 
            "https://fonbet3.com"
        ]
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'ru-RU,ru;q=0.9,en;q=0.8',
            'Referer': 'https://www.fonbet.ru/',
            'Origin': 'https://www.fonbet.ru'
        })
        
        # Кэш для событий и коэффициентов
        self.events_cache = {}
        self.cache_timeout = 300  # 5 минут
        self.last_update = 0
        
    def get_sports_list(self) -> List[Dict]:
        """Получает список доступных видов спорта"""
        try:
            url = f"{self.public_api}/sports"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('sports', [])
            else:
                logger.error(f"Ошибка получения списка спортов: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Ошибка при получении списка спортов: {e}")
            return []
    
    def get_events(self, sport_id: int = 1, days: int = 1) -> List[Dict]:
        """Получает события по виду спорта"""
        try:
            # Проверяем кэш
            current_time = time.time()
            cache_key = f"{sport_id}_{days}"
            
            if (cache_key in self.events_cache and 
                current_time - self.last_update < self.cache_timeout):
                return self.events_cache[cache_key]
            
            # Получаем новые данные
            url = f"{self.public_api}/events"
            params = {
                'sportId': sport_id,
                'days': days,
                'lang': 'ru'
            }
            
            response = self.session.get(url, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                events = data.get('events', [])
                
                # Фильтруем активные события
                active_events = []
                for event in events:
                    if event.get('status') == 'STARTED' or event.get('status') == 'NOT_STARTED':
                        active_events.append(self._format_event(event))
                
                # Обновляем кэш
                self.events_cache[cache_key] = active_events
                self.last_update = current_time
                
                return active_events
            else:
                logger.error(f"Ошибка получения событий: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Ошибка при получении событий: {e}")
            
            # Возвращаем демо данные если API недоступен
            logger.warning("⚠️ Матчи с Fonbet не получены, используем демо данные")
            return self._get_demo_events()
    
    def _get_demo_events(self) -> List[Dict]:
        """Возвращает демо события для тестирования"""
        print("🎭 Используем демо данные для тестирования")
        
        demo_events = [
            {
                'id': 'demo_1',
                'date': (datetime.now() + timedelta(hours=2)).isoformat(),
                'home_team': 'Спартак',
                'away_team': 'ЦСКА',
                'competition': 'Российская Премьер-лига',
                'sport': 'football',
                'status': 'NOT_STARTED',
                'fonbet_id': 'demo_1'
            },
            {
                'id': 'demo_2', 
                'date': (datetime.now() + timedelta(hours=4)).isoformat(),
                'home_team': 'Зенит',
                'away_team': 'Динамо',
                'competition': 'Российская Премьер-лига',
                'sport': 'football',
                'status': 'NOT_STARTED',
                'fonbet_id': 'demo_2'
            },
            {
                'id': 'demo_3',
                'date': (datetime.now() + timedelta(hours=6)).isoformat(),
                'home_team': 'Краснодар',
                'away_team': 'Ростов',
                'competition': 'Российская Премьер-лига', 
                'sport': 'football',
                'status': 'NOT_STARTED',
                'fonbet_id': 'demo_3'
            }
        ]
        
        return demo_events
    
    def _format_event(self, event: Dict) -> Dict:
        """Форматирует событие в стандартный вид"""
        try:
            # Извлекаем основную информацию
            event_id = event.get('id')
            start_time = event.get('startTime')
            
            # Команды/участники
            team1 = event.get('team1', {}).get('name', 'Unknown')
            team2 = event.get('team2', {}).get('name', 'Unknown')
            
            # Турнир/лига
            competition = event.get('competitionName', 'Unknown Competition')
            sport_name = event.get('sportName', 'Unknown Sport')
            
            formatted_event = {
                'id': str(event_id),
                'date': start_time,
                'home_team': team1,
                'away_team': team2,
                'competition': competition,
                'sport': sport_name.lower(),
                'status': event.get('status', 'UNKNOWN'),
                'fonbet_id': event_id,
                'raw_data': event
            }
            
            return formatted_event
            
        except Exception as e:
            logger.error(f"Ошибка форматирования события: {e}")
            return {}
    
    def get_event_odds(self, event_id: int) -> Dict:
        """Получает коэффициенты для события"""
        try:
            url = f"{self.public_api}/events/{event_id}/odds"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return self._format_odds(data)
            else:
                logger.error(f"Ошибка получения коэффициентов для события {event_id}: {response.status_code}")
                return {}
                
        except Exception as e:
            logger.error(f"Ошибка при получении коэффициентов: {e}")
            return {}
    
    def _format_odds(self, odds_data: Dict) -> Dict:
        """Форматирует коэффициенты в стандартный вид"""
        try:
            markets = odds_data.get('markets', [])
            formatted_odds = {
                'main_odds': {},
                'additional_markets': {},
                'timestamp': datetime.now().isoformat()
            }
            
            for market in markets:
                market_name = market.get('name', '')
                market_type = market.get('type', '')
                
                # Основные рынки (1X2)
                if 'исход' in market_name.lower() or market_type == 'win':
                    outcomes = market.get('outcomes', [])
                    for outcome in outcomes:
                        outcome_name = outcome.get('name', '').lower()
                        coefficient = outcome.get('coefficient')
                        
                        if 'п1' in outcome_name or '1' == outcome_name:
                            formatted_odds['main_odds']['home'] = coefficient
                        elif 'п2' in outcome_name or '2' == outcome_name:
                            formatted_odds['main_odds']['away'] = coefficient
                        elif 'х' in outcome_name or 'draw' in outcome_name:
                            formatted_odds['main_odds']['draw'] = coefficient
                
                # Дополнительные рынки
                elif 'тотал' in market_name.lower():
                    formatted_odds['additional_markets'][market_name] = market
                elif 'фора' in market_name.lower():
                    formatted_odds['additional_markets'][market_name] = market
            
            return formatted_odds
            
        except Exception as e:
            logger.error(f"Ошибка форматирования коэффициентов: {e}")
            return {}
    
    def get_football_matches(self) -> List[Dict]:
        """Получает футбольные матчи"""
        return self.get_events(sport_id=1, days=1)  # 1 = футбол
    
    def get_tennis_matches(self) -> List[Dict]:
        """Получает теннисные матчи"""
        return self.get_events(sport_id=2, days=1)  # 2 = теннис
    
    def get_basketball_matches(self) -> List[Dict]:
        """Получает баскетбольные матчи"""
        return self.get_events(sport_id=3, days=1)  # 3 = баскетбол
    
    def get_esports_matches(self) -> List[Dict]:
        """Получает киберспортивные матчи"""
        return self.get_events(sport_id=31, days=1)  # 31 = киберспорт
    
    def search_events(self, query: str) -> List[Dict]:
        """Поиск событий по названию команд или турниру"""
        try:
            url = f"{self.public_api}/search"
            params = {
                'query': query,
                'lang': 'ru'
            }
            
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                events = data.get('events', [])
                return [self._format_event(event) for event in events]
            else:
                return []
                
        except Exception as e:
            logger.error(f"Ошибка поиска событий: {e}")
            return []
    
    def get_event_details(self, event_id: int) -> Dict:
        """Получает детальную информацию о событии"""
        try:
            url = f"{self.public_api}/events/{event_id}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Получаем коэффициенты
                odds = self.get_event_odds(event_id)
                
                # Формируем детальную информацию
                event_details = {
                    'event_info': data,
                    'odds': odds,
                    'analytics': self._analyze_event(data, odds),
                    'timestamp': datetime.now().isoformat()
                }
                
                return event_details
            else:
                return {}
                
        except Exception as e:
            logger.error(f"Ошибка получения деталей события: {e}")
            return {}
    
    def _analyze_event(self, event_data: Dict, odds_data: Dict) -> Dict:
        """Базовый анализ события"""
        try:
            analysis = {
                'value_bets': [],
                'risk_level': 'medium',
                'recommended_action': 'analyze',
                'notes': []
            }
            
            main_odds = odds_data.get('main_odds', {})
            
            if main_odds:
                # Анализ основных коэффициентов
                home_odds = main_odds.get('home', 0)
                away_odds = main_odds.get('away', 0)
                draw_odds = main_odds.get('draw', 0)
                
                # Расчет вероятностей букмекера
                if home_odds and away_odds:
                    total_prob = (1/home_odds + 1/away_odds + (1/draw_odds if draw_odds else 0))
                    margin = (total_prob - 1) * 100
                    
                    analysis['bookmaker_margin'] = round(margin, 2)
                    analysis['implied_probabilities'] = {
                        'home': round((1/home_odds) / total_prob * 100, 1) if home_odds else 0,
                        'away': round((1/away_odds) / total_prob * 100, 1) if away_odds else 0,
                        'draw': round((1/draw_odds) / total_prob * 100, 1) if draw_odds else 0
                    }
                
                # Поиск аномальных коэффициентов
                if home_odds > 10 or away_odds > 10:
                    analysis['notes'].append('Высокие коэффициенты - возможен андердог')
                    analysis['risk_level'] = 'high'
                elif home_odds < 1.3 or away_odds < 1.3:
                    analysis['notes'].append('Низкие коэффициенты - явный фаворит')
                    analysis['risk_level'] = 'low'
            
            return analysis
            
        except Exception as e:
            logger.error(f"Ошибка анализа события: {e}")
            return {}
    
    def get_live_events(self) -> List[Dict]:
        """Получает live события"""
        try:
            url = f"{self.public_api}/events/live"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                events = data.get('events', [])
                return [self._format_event(event) for event in events]
            else:
                return []
                
        except Exception as e:
            logger.error(f"Ошибка получения live событий: {e}")
            return []
    
    def simulate_bet_placement(self, event_id: int, bet_type: str, stake: float, odds: float) -> Dict:
        """Симуляция размещения ставки (для тестирования)"""
        try:
            # ЭТО ТОЛЬКО СИМУЛЯЦИЯ! Реальные ставки требуют авторизации и могут нарушать ToS
            bet_info = {
                'bet_id': f"sim_{int(time.time())}",
                'event_id': event_id,
                'bet_type': bet_type,
                'stake': stake,
                'odds': odds,
                'potential_payout': stake * odds,
                'status': 'simulated',
                'timestamp': datetime.now().isoformat(),
                'warning': 'ЭТО СИМУЛЯЦИЯ! Реальные ставки не размещены!'
            }
            
            logger.info(f"Симуляция ставки: {stake} руб на {bet_type} с коэф. {odds}")
            return bet_info
            
        except Exception as e:
            logger.error(f"Ошибка симуляции ставки: {e}")
            return {}
    
    def get_account_balance(self) -> Dict:
        """Получает баланс аккаунта (требует авторизации)"""
        # Заглушка - требует реальной авторизации
        return {
            'balance': 0,
            'currency': 'RUB',
            'status': 'unauthorized',
            'message': 'Требуется авторизация для получения баланса'
        }
    
    def get_bet_history(self) -> List[Dict]:
        """Получает историю ставок (требует авторизации)"""
        # Заглушка - требует реальной авторизации
        return []

    def get_csgo_matches(self) -> List[Dict]:
        """Получает матчи CS:GO"""
        try:
            response = self.session.get(f"{self.base_url}", params={'sport': 'csgo'}, timeout=10)
            
            if response.status_code != 200:
                print(f"⚠️ Ошибка API Фонбет: {response.status_code}")
                return []
                
            data = response.json()
            matches = []
            
            for event in data.get('events', []):
                if event.get('sport') == 'csgo':
                    match = self._parse_csgo_match(event)
                    if match:
                        matches.append(match)
            
            return matches
            
        except Exception as e:
            logger.error(f"Ошибка получения матчей CS:GO: {e}")
            return []
            
    def _parse_csgo_match(self, event: Dict) -> Optional[Dict]:
        """Парсит матч CS:GO из данных Фонбет"""
        try:
            team1 = event.get('team1', {}).get('name')
            team2 = event.get('team2', {}).get('name')
            
            if not team1 or not team2:
                return None
                
            # Получаем основные коэффициенты
            markets = event.get('markets', [])
            match_winner = next((m for m in markets if m.get('type') == 'match_winner'), None)
            
            if not match_winner:
                return None
                
            odds = {
                'team1': float(match_winner['odds'][0]),
                'team2': float(match_winner['odds'][1])
            }
            
            return {
                'id': str(event['id']),
                'date': datetime.fromtimestamp(event['startTime']).isoformat(),
                'team1': team1,
                'team2': team2,
                'tournament': event.get('league', {}).get('name', 'Unknown'),
                'format': self._determine_match_format(event),
                'sport': 'csgo',
                'odds': odds,
                'source': 'fonbet'
            }
            
        except Exception as e:
            logger.error(f"Ошибка парсинга матча CS:GO: {e}")
            return None
            
    def _determine_match_format(self, event: Dict) -> str:
        """Определяет формат матча CS:GO"""
        try:
            name = event.get('name', '').lower()
            if 'bo5' in name:
                return 'BO5'
            elif 'bo3' in name:
                return 'BO3'
            else:
                return 'BO1'
        except:
            return 'BO1'

# Пример использования
if __name__ == "__main__":
    # Тестирование API
    fonbet = FonbetAPI()
    
    print("🏈 Тестирование Fonbet API")
    print("=" * 30)
    
    # Получаем список спортов
    sports = fonbet.get_sports_list()
    print(f"Доступно видов спорта: {len(sports)}")
    
    # Получаем футбольные матчи
    football_matches = fonbet.get_football_matches()
    print(f"Футбольных матчей: {len(football_matches)}")
    
    if football_matches:
        match = football_matches[0]
        print(f"\nПример матча:")
        print(f"🏆 {match['competition']}")
        print(f"⚽ {match['home_team']} vs {match['away_team']}")
        print(f"📅 {match['date']}")
        
        # Получаем коэффициенты
        odds = fonbet.get_event_odds(int(match['fonbet_id']))
        if odds.get('main_odds'):
            main_odds = odds['main_odds']
            print(f"💰 П1: {main_odds.get('home', 'N/A')} | X: {main_odds.get('draw', 'N/A')} | П2: {main_odds.get('away', 'N/A')}") 