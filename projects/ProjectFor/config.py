import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys (получить можно бесплатно)
    SPORTMONKS_API_KEY = os.getenv('SPORTMONKS_API_KEY', '')
    ODDS_API_KEY = os.getenv('ODDS_API_KEY', '')
    
    # Database
    DATABASE_URL = "sqlite:///betting_system.db"
    
    # Betting Settings
    INITIAL_BANKROLL = 50000  # Начальный банкролл в рублях
    MIN_BET = 1000  # Минимальная ставка
    MAX_BET = 10000  # Максимальная ставка
    
    # Martingale Settings
    MARTINGALE_MULTIPLIER = 2.0
    MAX_MARTINGALE_STEPS = 5  # Максимум удвоений подряд
    
    # Confidence Thresholds
    MIN_CONFIDENCE = 0.65  # Минимальная уверенность для ставки
    HIGH_CONFIDENCE = 0.80  # Высокая уверенность
    
    # Sports Focus
    SUPPORTED_SPORTS = ['football', 'basketball', 'tennis', 'esports']
    
    # API URLs
    FOOTBALL_DATA_URL = "https://v3.football.api-sports.io"
    ESPORTS_DATA_URL = "https://api.pandascore.co"
    
    # Logging
    LOG_LEVEL = "INFO"
    LOG_FILE = "betting_system.log" 