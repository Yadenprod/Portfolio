import os
import sys
import json
import time
import random
import logging
import requests
import cloudscraper
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from fake_useragent import UserAgent
import re
import brotli
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

logger = logging.getLogger(__name__)

class HLTVParser:
    """Парсер матчей CS:GO с HLTV.org"""
    
    def __init__(self):
        self.base_url = "https://www.hltv.org"
        self.scraper = self._setup_scraper()
        self.team_cache = {}
        self.cache_ttl = 3600  # 1 час
        
    def _setup_scraper(self):
        """Настраивает scraper с правильными заголовками"""
        scraper = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'windows',
                'mobile': False
            }
        )
        
        scraper.headers.update({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache'
        })
        
        return scraper
        
    def get_upcoming_matches(self, days_ahead: int = 3) -> List[Dict]:
        """Получает предстоящие матчи CS:GO"""
        try:
            print("📡 Получение матчей CS:GO с HLTV.org...")
            
            # Создаем новую сессию для каждого запроса
            self.scraper = self._setup_scraper()
            
            # Добавляем случайную задержку
            time.sleep(random.uniform(2, 3))
            
            # Получаем страницу матчей
            response = self.scraper.get(f"{self.base_url}/matches")
            if response.status_code != 200:
                print(f"❌ Ошибка получения страницы: {response.status_code}")
                return []
                
            # Сохраняем HTML для отладки
            with open('debug_hltv.html', 'w', encoding='utf-8') as f:
                f.write(response.text)
                
            # Парсим HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Находим все блоки с матчами
            matches = []
            processed_urls = set()  # Для отслеживания уже обработанных матчей
            match_elements = soup.select('.match-wrapper')
            
            for match in match_elements:
                try:
                    # Получаем команды
                    teams = match.select('.match-team')
                    if len(teams) != 2:
                        continue
                        
                    # Получаем названия команд
                    team1_name = teams[0].select_one('.match-teamname')
                    team2_name = teams[1].select_one('.match-teamname')
                    
                    # Если нет имени команды, пробуем получить из .team
                    if not team1_name:
                        team1_name = teams[0].select_one('.team')
                    if not team2_name:
                        team2_name = teams[1].select_one('.team')
                        
                    if not team1_name or not team2_name:
                        continue
                        
                    team1 = team1_name.text.strip()
                    team2 = team2_name.text.strip()
                    
                    # Пропускаем матчи с неизвестными командами или победителями других матчей
                    if any(x in team1.lower() for x in ['tba', 'winner']) or any(x in team2.lower() for x in ['tba', 'winner']):
                        continue
                    
                    # Получаем время матча
                    time_element = match.select_one('.match-time')
                    if not time_element:
                        continue
                        
                    match_time = time_element.text.strip()
                    
                    # Получаем название турнира и стадию
                    event = match.select_one('.match-event')
                    if not event:
                        continue
                        
                    event_text = event.get_text(strip=True).split('\n')
                    event_name = event_text[0] if event_text else "Unknown Event"
                    
                    # Получаем стадию матча
                    stage_element = match.select_one('.match-stage')
                    stage = stage_element.text.strip() if stage_element else ""
                    
                    # Определяем формат матча
                    meta = match.select_one('.match-meta')
                    match_format = meta.text.strip().upper() if meta else "Unknown"
                    
                    # Получаем ссылку на матч
                    match_link = match.select_one('a.match-teams')
                    if not match_link or not match_link.has_attr('href'):
                        continue
                        
                    match_url = self.base_url + match_link['href']
                    
                    # Пропускаем дубликаты
                    if match_url in processed_urls:
                        continue
                    processed_urls.add(match_url)
                    
                    # Получаем дату из родительского контейнера
                    date_container = match.find_parent('div', {'class': 'matches-list-section'})
                    date = datetime.now()  # По умолчанию сегодня
                    
                    if date_container:
                        date_headline = date_container.select_one('.matches-list-headline')
                        if date_headline:
                            try:
                                # Формат: "Saturday - 2025-06-28"
                                date_str = date_headline.text.strip().split(' - ')[1]
                                date = datetime.strptime(date_str, '%Y-%m-%d')
                                
                                # Проверяем, что дата в пределах запрошенного периода
                                if date > datetime.now() + timedelta(days=days_ahead):
                                    continue
                            except Exception:
                                pass
                    
                    matches.append({
                        'id': f"hltv_{abs(hash(f'{team1}_{team2}_{event_name}_{match_time}'))}",
                        'team1': team1,
                        'team2': team2,
                        'date': f"{date.strftime('%Y-%m-%d')} {match_time}",
                        'tournament': event_name,
                        'stage': stage,
                        'format': match_format,
                        'url': match_url,
                        'sport': 'csgo',
                        'source': 'hltv'
                    })
                    
                except Exception as e:
                    print(f"⚠️ Ошибка при парсинге матча: {e}")
                    continue
            
            print(f"✅ Найдено матчей: {len(matches)}")
            return matches
            
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            return []
            
    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """Парсит дату из строки HLTV"""
        try:
            # Форматы даты: "Today", "Tomorrow", "Sunday 3rd of March 2024" и т.д.
            date_str = date_str.lower()
            
            if 'today' in date_str:
                return datetime.now()
            elif 'tomorrow' in date_str:
                return datetime.now() + timedelta(days=1)
            else:
                # Пытаемся распарсить полную дату
                date_parts = date_str.split()
                if len(date_parts) >= 4:
                    day = ''.join(filter(str.isdigit, date_parts[1]))
                    month = date_parts[3]
                    year = date_parts[4]
                    
                    return datetime.strptime(f"{day} {month} {year}", "%d %B %Y")
                    
            return None
            
        except Exception:
            return None
            
    def _get_match_format(self, stars: int) -> str:
        """Определяет формат матча по количеству звезд"""
        if stars == 1:
            return "BO1"
        elif stars == 2:
            return "BO3" 
        elif stars == 3:
            return "BO5"
        else:
            return "Unknown"
            
    def _parse_match_element(self, element, is_live: bool = False) -> Optional[Dict]:
        """Парсит элемент матча"""
        try:
            # Получаем команды
            teams = []
            team_elements = element.select('.matchTeam')
            
            for team in team_elements:
                team_name = team.select_one('.matchTeamName')
                if team_name:
                    team_name = team_name.get_text(strip=True)
                    if team_name and team_name not in teams:
                        teams.append(team_name)
            
            if len(teams) < 2:
                return None
            
            # Получаем турнир
            tournament = "Unknown Tournament"
            tournament_elem = element.select_one('.matchEventName')
            if tournament_elem:
                tournament = tournament_elem.get_text(strip=True)
            
            # Получаем время
            match_time = None
            time_elem = element.select_one('.matchTime')
            if time_elem:
                match_time = time_elem.get_text(strip=True)
                
            # Получаем формат матча (BO1, BO3, BO5)
            match_format = 'BO3'  # По умолчанию
            format_elem = element.select_one('.matchMeta')
            if format_elem:
                format_text = format_elem.get_text(strip=True).upper()
                if 'BO5' in format_text:
                    match_format = 'BO5'
                elif 'BO1' in format_text:
                    match_format = 'BO1'
            
            # Получаем ссылку на матч
            match_url = None
            match_link = element.select_one('a.match')
            if match_link:
                match_url = self.base_url + match_link['href']
            
            # Формируем данные матча
            match_data = {
                'id': f"{'live' if is_live else 'upcoming'}_{abs(hash(f'{teams[0]}_{teams[1]}_{tournament}_{match_time}'))}",
                'date': datetime.now().isoformat() if is_live else (match_time or datetime.now().isoformat()),
                'team1': teams[0],
                'team2': teams[1],
                'tournament': tournament,
                'format': match_format,
                'sport': 'csgo',
                'url': match_url,
                'status': 'live' if is_live else 'upcoming'
            }
            
            # Если есть URL матча, получаем дополнительную информацию
            if match_url and not is_live:
                extra_info = self._fetch_match_extra_info(match_url)
                if extra_info:
                    match_data.update(extra_info)
            
            print(f"✅ Добавлен {'LIVE' if is_live else 'предстоящий'} матч: {teams[0]} vs {teams[1]}")
            return match_data
            
        except Exception as e:
            logger.error(f"Ошибка парсинга элемента матча: {e}")
            return None
            
    def _fetch_match_extra_info(self, match_url: str) -> Optional[Dict]:
        """Получает дополнительную информацию о матче"""
        try:
            # Добавляем случайную задержку
            time.sleep(random.uniform(1, 2))
            
            # Получаем страницу матча
            response = self.scraper.get(match_url)
            if response.status_code != 200:
                return None
                
            soup = BeautifulSoup(response.text, 'html5lib')
            
            extra_info = {}
            
            # Получаем карты
            maps_container = soup.select_one('.maps')
            if maps_container:
                maps = [map_elem.get_text(strip=True) for map_elem in maps_container.select('.mapname')]
                extra_info['maps'] = maps
            
            # Получаем коэффициенты
            odds = {}
            team1_odds = soup.select_one('.team1-gradient .odds-cell')
            team2_odds = soup.select_one('.team2-gradient .odds-cell')
            
            if team1_odds:
                try:
                    odds['team1_win'] = float(team1_odds.get_text(strip=True))
                except:
                    pass
                    
            if team2_odds:
                try:
                    odds['team2_win'] = float(team2_odds.get_text(strip=True))
                except:
                    pass
                    
            if odds:
                extra_info['odds'] = odds
            
            return extra_info
            
        except Exception as e:
            logger.error(f"Ошибка получения доп. информации о матче: {e}")
            return None
    
    def _get_demo_matches(self) -> List[Dict]:
        """Возвращает демо-матчи для тестирования системы"""
        print("🎮 Генерируем демо-матчи CS:GO...")
        
        demo_teams = [
            ("NAVI", "FaZe"),
            ("G2", "Vitality"),
            ("Astralis", "Heroic"),
            ("Spirit", "Cloud9"),
            ("ENCE", "FURIA"),
            ("Liquid", "NIP"),
            ("Mouz", "Complexity"),
            ("Eternal Fire", "MIBR")
        ]
        
        matches = []
        for i, (team1, team2) in enumerate(demo_teams[:5]):
            match_id = f"demo_{i+1}"
            
            # Генерируем реалистичные коэффициенты
            odds = self._generate_cs_odds(team1, team2)
            
            match_data = {
                'id': match_id,
                'date': (datetime.now() + timedelta(hours=i+1)).isoformat(),
                'team1': team1,
                'team2': team2,
                'tournament': f"BLAST Premier Spring {2024}",
                'format': "BO3" if i % 2 == 0 else "BO1",
                'sport': 'csgo',
                'odds': odds,
                'source': 'demo'
            }
            matches.append(match_data)
            print(f"✅ Создан демо-матч: {team1} vs {team2}")
        
        print(f"🎮 Готово! Создано {len(matches)} демо-матчей")
        return matches
    
    def _parse_match_block(self, match_block) -> Optional[Dict]:
        """Парсит блок с информацией о матче"""
        try:
            # Получаем время матча
            match_time = None
            for time_class in ['matchTime', 'time', 'date-time', 'match-time']:
                time_elem = match_block.find(['div', 'span'], class_=time_class)
                if time_elem:
                    match_time = time_elem.get_text(strip=True)
                    break
            
            # Получаем команды
            team1 = None
            team2 = None
            
            # Пробуем разные структуры для команд
            team_containers = []
            
            # Структура 1: div с классом matchTeam/team
            if not team_containers:
                team_containers = match_block.find_all(['div', 'span'], class_=lambda x: x and ('matchTeam' in x or x == 'team'))
            
            # Структура 2: div внутри team-box
            if not team_containers:
                team_box = match_block.find(['div', 'section'], class_='team-box')
                if team_box:
                    team_containers = team_box.find_all(['div', 'span'], class_=lambda x: x and 'team' in x.lower())
            
            # Структура 3: прямой поиск названий команд
            if not team_containers:
                for team_class in ['team-name', 'teamName', 'team']:
                    teams = match_block.find_all(['div', 'span', 'a'], class_=team_class)
                    if len(teams) == 2:
                        team_containers = teams
                        break
            
            # Извлекаем названия команд
            if len(team_containers) >= 2:
                # Пробуем найти название в разных местах
                for container in team_containers[:2]:
                    team_name = None
                    
                    # Проверяем разные элементы с названием
                    for name_class in ['name', 'team-name', 'teamName']:
                        name_elem = container.find(['div', 'span', 'a'], class_=name_class)
                        if name_elem:
                            team_name = name_elem.get_text(strip=True)
                            break
                    
                    # Если не нашли через class, берем текст напрямую
                    if not team_name:
                        team_name = container.get_text(strip=True)
                    
                    # Очищаем название от мусора
                    if team_name:
                        team_name = re.sub(r'\([^)]*\)', '', team_name).strip()  # Убираем скобки и их содержимое
                        team_name = re.sub(r'[^\w\s-]', '', team_name).strip()   # Оставляем только буквы, цифры, пробелы и дефисы
                    
                    if not team1:
                        team1 = team_name
                    else:
                        team2 = team_name
            
            if not team1 or not team2:
                logger.warning("Не удалось найти обе команды в блоке матча")
                return None
            
            # Получаем событие/турнир
            event = None
            for event_class in ['matchEvent', 'event-name', 'tournament', 'match-tournament']:
                event_elem = match_block.find(['div', 'span'], class_=event_class)
                if event_elem:
                    event = event_elem.get_text(strip=True)
                    break
            
            if not event:
                event = "Unknown Tournament"
            
            # Получаем формат матча (BO1, BO3, BO5)
            match_format = "BO1"  # По умолчанию
            format_text = None
            
            # Ищем формат в разных местах
            for format_class in ['matchMeta', 'format', 'match-format', 'match-info']:
                format_elem = match_block.find(['div', 'span'], class_=format_class)
                if format_elem:
                    format_text = format_elem.get_text(strip=True).upper()
                    break
            
            # Если не нашли через классы, ищем в любом тексте блока
            if not format_text:
                format_text = match_block.get_text(strip=True).upper()
            
            # Определяем формат из текста
            if format_text:
                if "BO5" in format_text:
                    match_format = "BO5"
                elif "BO3" in format_text:
                    match_format = "BO3"
                elif "BO2" in format_text:
                    match_format = "BO2"
            
            # Генерируем ID матча
            match_id = f"hltv_{abs(hash(f'{team1}_{team2}_{event}_{match_time}'))}"
            
            # Получаем коэффициенты
            odds = self._generate_cs_odds(team1, team2)
            
            # Формируем дату матча
            try:
                if match_time:
                    match_date = datetime.strptime(match_time, "%Y-%m-%d %H:%M")
                else:
                    match_date = datetime.now() + timedelta(hours=2)
            except:
                match_date = datetime.now() + timedelta(hours=2)
            
            return {
                'id': match_id,
                'date': match_date.isoformat(),
                'team1': team1,
                'team2': team2,
                'tournament': event,
                'format': match_format,
                'sport': 'csgo',
                'odds': odds,
                'source': 'hltv'
            }
            
        except Exception as e:
            logger.error(f"Ошибка парсинга блока матча: {e}")
            return None
    
    def get_team_stats(self, team_name: str) -> Dict:
        """Получает статистику команды"""
        # Для демонстрации возвращаем фиктивные данные
        return {
            'rating': 1.1 + random.random() * 0.4,  # От 1.1 до 1.5
            'map_win_rate': 0.45 + random.random() * 0.3,  # От 45% до 75%
            'pistol_win_rate': 0.45 + random.random() * 0.2,  # От 45% до 65%
            'clutch_success': 0.35 + random.random() * 0.2,  # От 35% до 55%
            'recent_form': random.choices(['W', 'L'], k=5),  # 5 последних матчей
            'tier': random.randint(1, 3)  # Тир команды
        }
    
    def _fetch_team_stats_from_hltv(self, team_name: str) -> Optional[Dict]:
        """Получает статистику команды с HLTV"""
        try:
            # Создаем новую сессию для каждого запроса
            self.scraper = self._setup_scraper()
            
            # Формируем URL для поиска команды
            search_url = f"{self.base_url}/search?q={team_name}"
            
            # Добавляем случайную задержку
            time.sleep(random.uniform(2, 3))
            
            # Ищем команду
            response = self.scraper.get(search_url)
            if response.status_code != 200:
                return None
                
            soup = BeautifulSoup(response.text, 'html5lib')
            
            # Ищем ссылку на страницу команды
            team_links = soup.select('.table-header a')
            team_url = None
            
            for link in team_links:
                if '/team/' in link['href']:
                    team_url = self.base_url + link['href']
                    break
            
            if not team_url:
                return None
                
            # Добавляем случайную задержку
            time.sleep(random.uniform(2, 3))
            
            # Получаем страницу команды
            response = self.scraper.get(team_url)
            if response.status_code != 200:
                return None
                
            soup = BeautifulSoup(response.text, 'html5lib')
            
            # Парсим статистику
            stats = {
                'name': team_name,
                'world_rank': 999,  # По умолчанию
                'region': self._determine_team_region(team_url),
                'recent_form': [],
                'rating': 1.0,  # По умолчанию
                'map_win_rate': 0.5,  # По умолчанию
            }
            
            # Получаем ранк
            rank_elem = soup.select_one('.profile-team-stats-container .right')
            if rank_elem:
                try:
                    rank_text = rank_elem.get_text(strip=True).replace('#', '')
                    stats['world_rank'] = int(rank_text)
                except:
                    pass
            
            # Получаем рейтинг
            stats_container = soup.select('.profile-team-stats-container .stats-row')
            for stat_row in stats_container:
                stat_name = stat_row.select_one('.stat-name')
                stat_value = stat_row.select_one('.stat-value')
                
                if not stat_name or not stat_value:
                    continue
                    
                name = stat_name.get_text(strip=True).lower()
                value = stat_value.get_text(strip=True)
                
                if 'rating' in name:
                    try:
                        stats['rating'] = float(value)
                    except:
                        pass
                elif 'maps played' in name:
                    try:
                        stats['maps_played'] = int(value)
                    except:
                        pass
                elif 'win rate' in name:
                    try:
                        stats['map_win_rate'] = float(value.replace('%', '')) / 100
                    except:
                        pass
            
            # Получаем последние результаты
            results = soup.select('.profile-team-stats-container .result-row')
            for result in results[:5]:  # Берем последние 5 матчей
                result_text = result.get_text(strip=True).upper()
                if 'WIN' in result_text:
                    stats['recent_form'].append('W')
                elif 'LOSS' in result_text:
                    stats['recent_form'].append('L')
                else:
                    stats['recent_form'].append('D')
            
            # Если форма пустая, заполняем базовой
            if not stats['recent_form']:
                stats['recent_form'] = ['W', 'L', 'W', 'L', 'W']
            
            # Определяем тир команды на основе рейтинга
            stats['tier'] = self._determine_team_tier(stats['rating'])
            
            return stats
            
        except Exception as e:
            logger.error(f"Ошибка получения статистики {team_name} с HLTV: {e}")
            return None
    
    def _determine_team_tier(self, rating: float) -> int:
        """Определяет тир команды по рейтингу"""
        if rating >= 1.20:
            return 1
        elif rating >= 1.10:
            return 2
        else:
            return 3
            
    def _determine_team_region(self, team_url: str) -> str:
        """Определяет регион команды по URL"""
        regions = {
            'europe': 'Europe',
            'na': 'Americas',
            'sa': 'Americas',
            'asia': 'Asia',
            'oceania': 'Oceania'
        }
        
        for region_key, region_name in regions.items():
            if region_key in team_url.lower():
                return region_name
        return 'Unknown'
    
    def _get_cs_team_stats(self, team_name: str) -> Dict:
        """Генерирует базовую статистику команды"""
        # Базовые рейтинги для известных команд
        top_teams = {
            'NAVI': 1.22,
            'FaZe': 1.25,
            'Vitality': 1.20,
            'G2': 1.15,
            'Heroic': 1.14,
            'Cloud9': 1.10,
            'ENCE': 1.08,
            'Spirit': 1.16,
            'Astralis': 1.18,
            'FURIA': 1.12
        }
        
        # Определяем базовый рейтинг
        rating = top_teams.get(team_name, 1.0)
        
        # Генерируем реалистичную статистику
        stats = {
            'name': team_name,
            'rating': rating,
            'world_rank': list(top_teams.keys()).index(team_name) + 1 if team_name in top_teams else random.randint(10, 30),
            'map_win_rate': 0.5 + (rating - 1.0) * 0.3,  # Винрейт зависит от рейтинга
            'recent_form': ['W', 'L', 'W', 'L', 'W'],  # Базовая форма
            'region': 'EU' if team_name in ['G2', 'Vitality', 'Heroic', 'ENCE'] else 'CIS' if team_name in ['NAVI', 'Spirit', 'Cloud9'] else 'NA',
            'tier': 1 if rating >= 1.15 else 2,
            
            # Дополнительная статистика
            'pistol_win_rate': 0.48 + random.uniform(-0.05, 0.05),
            'clutch_success': 0.35 + random.uniform(-0.05, 0.05),
            'first_kill_rate': 0.51 + random.uniform(-0.03, 0.03),
            'flash_success': 0.72 + random.uniform(-0.05, 0.05),
            'avg_rounds_per_map': 26.5 + random.uniform(-2, 2)
        }
        
        return stats
    
    def _generate_cs_odds(self, team1: str, team2: str) -> Dict:
        """Генерирует коэффициенты на основе силы CS:GO команд"""
        team1_stats = self._get_cs_team_stats(team1)
        team2_stats = self._get_cs_team_stats(team2)
        
        # Рассчитываем силу команд
        team1_strength = (
            team1_stats['rating'] * 0.4 +
            team1_stats['map_win_rate'] * 0.3 +
            self._calculate_form_strength(team1_stats['recent_form']) * 0.2 +
            team1_stats['pistol_win_rate'] * 0.1
        )
        
        team2_strength = (
            team2_stats['rating'] * 0.4 +
            team2_stats['map_win_rate'] * 0.3 +
            self._calculate_form_strength(team2_stats['recent_form']) * 0.2 +
            team2_stats['pistol_win_rate'] * 0.1
        )
        
        # Нормализуем силу команд
        total_strength = team1_strength + team2_strength
        team1_prob = team1_strength / total_strength
        team2_prob = team2_strength / total_strength
        
        # Добавляем маржу букмекера (5%)
        margin = 0.05
        team1_odds = (1 / team1_prob) * (1 + margin)
        team2_odds = (1 / team2_prob) * (1 + margin)
        
        return {
            'team1': round(team1_odds, 2),
            'team2': round(team2_odds, 2)
        }
    
    def _calculate_form_strength(self, recent_form: List[str]) -> float:
        """Рассчитывает силу команды на основе последних результатов"""
        if not recent_form:
            return 0.5
        
        points = {'W': 1.0, 'L': 0.0, 'D': 0.5}
        total_points = sum(points.get(result, 0.5) for result in recent_form)
        return total_points / len(recent_form)
    
    def get_setup_instructions(self) -> str:
        """Возвращает инструкции по настройке парсера"""
        return """
🎮 НАСТРОЙКА CS:GO ПАРСЕРА:

📡 Источник данных: HLTV.org
• Автоматический парсинг предстоящих матчей
• Получение статистики команд  
• Генерация коэффициентов на основе силы команд

⚙️ Дополнительные настройки:
• Можно добавить прокси для обхода ограничений
• Настроить частоту обновления данных
• Добавить парсинг live результатов

🎯 ТЕКУЩИЙ СТАТУС: Работает с демо данными CS:GO матчей
""" 