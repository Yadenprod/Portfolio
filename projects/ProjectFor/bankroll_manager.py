import math
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from enum import Enum
import json

class BettingStrategy(Enum):
    FLAT = "flat"
    MARTINGALE = "martingale"
    FIBONACCI = "fibonacci"
    KELLY = "kelly"
    DALEMBERT = "dalembert"

class BankrollManager:
    def __init__(self, initial_bankroll: float, strategy: BettingStrategy = BettingStrategy.MARTINGALE):
        self.initial_bankroll = initial_bankroll
        self.current_bankroll = initial_bankroll
        self.strategy = strategy
        self.bet_history: List[Dict] = []
        self.consecutive_losses = 0
        self.fibonacci_sequence = [1, 1]
        self.base_bet = initial_bankroll * 0.02  # 2% от банка
        
    def calculate_bet_size(self, confidence: float, odds: float) -> float:
        """Рассчитывает размер ставки на основе выбранной стратегии"""
        
        if self.strategy == BettingStrategy.FLAT:
            return self._flat_betting()
        
        elif self.strategy == BettingStrategy.MARTINGALE:
            return self._martingale_betting()
        
        elif self.strategy == BettingStrategy.FIBONACCI:
            return self._fibonacci_betting()
        
        elif self.strategy == BettingStrategy.KELLY:
            return self._kelly_criterion(confidence, odds)
        
        elif self.strategy == BettingStrategy.DALEMBERT:
            return self._dalembert_betting()
        
        return self.base_bet
    
    def _flat_betting(self) -> float:
        """Фиксированная ставка 2% от текущего банка"""
        return max(self.current_bankroll * 0.02, 1000)
    
    def _martingale_betting(self) -> float:
        """Система удвоения после проигрыша"""
        if self.consecutive_losses == 0:
            return self.base_bet
        
        # Ограничиваем количество удвоений
        max_steps = 5
        if self.consecutive_losses > max_steps:
            return self.base_bet
        
        multiplier = 2 ** self.consecutive_losses
        bet_size = self.base_bet * multiplier
        
        # Не ставим больше 20% от банка
        max_bet = self.current_bankroll * 0.2
        return min(bet_size, max_bet)
    
    def _fibonacci_betting(self) -> float:
        """Система Фибоначчи"""
        if self.consecutive_losses == 0:
            return self.base_bet
        
        # Расширяем последовательность Фибоначчи если нужно
        while len(self.fibonacci_sequence) <= self.consecutive_losses:
            next_fib = self.fibonacci_sequence[-1] + self.fibonacci_sequence[-2]
            self.fibonacci_sequence.append(next_fib)
        
        multiplier = self.fibonacci_sequence[min(self.consecutive_losses, len(self.fibonacci_sequence) - 1)]
        bet_size = self.base_bet * multiplier
        
        max_bet = self.current_bankroll * 0.15
        return min(bet_size, max_bet)
    
    def _kelly_criterion(self, confidence: float, odds: float) -> float:
        """Критерий Келли для оптимального размера ставки"""
        # Преобразуем confidence в вероятность выигрыша
        win_probability = confidence
        
        # Коэффициент букмекера в десятичном формате
        decimal_odds = odds
        
        # Формула Келли: f = (bp - q) / b
        # где b = decimal_odds - 1, p = win_probability, q = 1 - p
        b = decimal_odds - 1
        p = win_probability
        q = 1 - p
        
        if b <= 0 or p <= q/b:
            return 0  # Невыгодная ставка
        
        kelly_fraction = (b * p - q) / b
        
        # Ограничиваем долю банка (консервативный подход)
        kelly_fraction = min(kelly_fraction, 0.1)  # Максимум 10%
        kelly_fraction = max(kelly_fraction, 0.01)  # Минимум 1%
        
        return self.current_bankroll * kelly_fraction
    
    def _dalembert_betting(self) -> float:
        """Система Д'Аламбера: +1 единица после проигрыша, -1 после выигрыша"""
        unit_size = self.base_bet * 0.5
        bet_size = self.base_bet + (self.consecutive_losses * unit_size)
        
        max_bet = self.current_bankroll * 0.1
        return min(bet_size, max_bet)
    
    def place_bet(self, bet_size: float, confidence: float, odds: float, 
                  match_info: Dict, prediction: str) -> Dict:
        """Размещает ставку и обновляет банкролл"""
        
        if bet_size > self.current_bankroll:
            bet_size = self.current_bankroll * 0.5  # Ставим половину банка максимум
        
        bet_info = {
            'timestamp': datetime.now().isoformat(),
            'bet_size': bet_size,
            'confidence': confidence,
            'odds': odds,
            'match_info': match_info,
            'prediction': prediction,
            'bankroll_before': self.current_bankroll,
            'strategy': self.strategy.value,
            'consecutive_losses': self.consecutive_losses
        }
        
        self.current_bankroll -= bet_size
        self.bet_history.append(bet_info)
        
        return bet_info
    
    def resolve_bet(self, bet_id: int, won: bool) -> Dict:
        """Разрешает результат ставки и обновляет банкролл"""
        
        if bet_id >= len(self.bet_history):
            raise ValueError("Invalid bet ID")
        
        bet = self.bet_history[bet_id]
        
        if won:
            # Выигрыш
            winnings = bet['bet_size'] * bet['odds']
            self.current_bankroll += winnings
            self.consecutive_losses = 0
            
            # Сброс последовательности Фибоначчи при выигрыше
            if self.strategy == BettingStrategy.FIBONACCI:
                self.fibonacci_sequence = [1, 1]
                
        else:
            # Проигрыш
            self.consecutive_losses += 1
        
        bet['result'] = 'won' if won else 'lost'
        bet['bankroll_after'] = self.current_bankroll
        bet['resolved_at'] = datetime.now().isoformat()
        
        return bet
    
    def get_statistics(self) -> Dict:
        """Возвращает статистику ставок"""
        if not self.bet_history:
            return {}
        
        resolved_bets = [bet for bet in self.bet_history if 'result' in bet]
        
        if not resolved_bets:
            return {'total_bets': len(self.bet_history), 'resolved_bets': 0}
        
        wins = len([bet for bet in resolved_bets if bet['result'] == 'won'])
        losses = len([bet for bet in resolved_bets if bet['result'] == 'lost'])
        
        total_staked = sum(bet['bet_size'] for bet in resolved_bets)
        total_returned = sum(bet['bet_size'] * bet['odds'] for bet in resolved_bets if bet['result'] == 'won')
        
        profit_loss = total_returned - total_staked
        roi = (profit_loss / total_staked * 100) if total_staked > 0 else 0
        
        win_rate = (wins / len(resolved_bets) * 100) if resolved_bets else 0
        
        return {
            'total_bets': len(self.bet_history),
            'resolved_bets': len(resolved_bets),
            'wins': wins,
            'losses': losses,
            'win_rate': round(win_rate, 2),
            'total_staked': round(total_staked, 2),
            'total_returned': round(total_returned, 2),
            'profit_loss': round(profit_loss, 2),
            'roi': round(roi, 2),
            'current_bankroll': round(self.current_bankroll, 2),
            'bankroll_change': round(self.current_bankroll - self.initial_bankroll, 2),
            'consecutive_losses': self.consecutive_losses,
            'strategy': self.strategy.value
        }
    
    def save_to_file(self, filename: str = "bankroll_data.json"):
        """Сохраняет данные банкролла в файл"""
        data = {
            'initial_bankroll': self.initial_bankroll,
            'current_bankroll': self.current_bankroll,
            'strategy': self.strategy.value,
            'bet_history': self.bet_history,
            'consecutive_losses': self.consecutive_losses,
            'fibonacci_sequence': self.fibonacci_sequence,
            'base_bet': self.base_bet
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load_from_file(self, filename: str = "bankroll_data.json"):
        """Загружает данные банкролла из файла"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.initial_bankroll = data['initial_bankroll']
            self.current_bankroll = data['current_bankroll']
            self.strategy = BettingStrategy(data['strategy'])
            self.bet_history = data['bet_history']
            self.consecutive_losses = data['consecutive_losses']
            self.fibonacci_sequence = data['fibonacci_sequence']
            self.base_bet = data['base_bet']
            
        except FileNotFoundError:
            print(f"File {filename} not found. Starting with fresh data.")
        except Exception as e:
            print(f"Error loading data: {e}")

# Пример использования
if __name__ == "__main__":
    # Создаем менеджер банкролла
    manager = BankrollManager(50000, BettingStrategy.MARTINGALE)
    
    # Рассчитываем размер ставки
    bet_size = manager.calculate_bet_size(confidence=0.75, odds=2.1)
    print(f"Рекомендуемая ставка: {bet_size:.2f} руб")
    
    # Размещаем ставку
    bet = manager.place_bet(
        bet_size=bet_size,
        confidence=0.75,
        odds=2.1,
        match_info={'team1': 'Real Madrid', 'team2': 'Barcelona'},
        prediction='Real Madrid'
    )
    
    # Статистика
    stats = manager.get_statistics()
    print(f"Статистика: {stats}") 