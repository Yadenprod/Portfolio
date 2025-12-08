import json
import math
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class BettingStrategy(Enum):
    KELLY_CRITERION = "kelly"
    FIXED_PERCENTAGE = "fixed_percent" 
    VALUE_BETTING = "value"
    PROGRESSIVE = "progressive"
    CONSERVATIVE = "conservative"

class SmartBankrollManager:
    """Умный менеджер банкролла с продвинутыми стратегиями"""
    
    def __init__(self, initial_bankroll: float = 50000.0, strategy: BettingStrategy = BettingStrategy.KELLY_CRITERION):
        self.initial_bankroll = initial_bankroll
        self.current_bankroll = initial_bankroll
        self.strategy = strategy
        self.bet_history: List[Dict] = []
        self.daily_limit_percent = 0.1  # Максимум 10% банкролла в день
        self.single_bet_max_percent = 0.05  # Максимум 5% на одну ставку
        self.min_bet = 100.0  # Минимальная ставка
        self.stop_loss_percent = 0.3  # Стоп-лосс на 30% от изначального банкролла
        self.target_profit_percent = 2.0  # Цель 200% прибыли
        
        # Статистика
        self.total_bets = 0
        self.winning_bets = 0
        self.current_streak = 0
        self.max_drawdown = 0.0
        self.peak_bankroll = initial_bankroll
        
        # Настройки стратегий
        self.kelly_multiplier = 0.25  # Консервативный келли (25% от полного)
        self.fixed_percent = 0.02  # 2% банкролла на фиксированной стратегии
        self.value_threshold = 0.05  # Минимальное value для ставки
        
        self.load_data()
    
    def calculate_bet_size(self, prediction_data: Dict, match_odds: Dict) -> Dict:
        """Рассчитывает оптимальный размер ставки"""
        
        # Проверяем лимиты
        if not self._check_daily_limits():
            return {"recommended_bet": 0, "reason": "Превышен дневной лимит ставок"}
        
        if self.current_bankroll <= self.initial_bankroll * (1 - self.stop_loss_percent):
            return {"recommended_bet": 0, "reason": "Активирован стоп-лосс"}
        
        value_bets = prediction_data.get('value_bets', {})
        if not value_bets:
            return {"recommended_bet": 0, "reason": "Нет value ставок"}
        
        # Находим лучшую value ставку
        best_value_bet = max(value_bets.items(), key=lambda x: x[1]['value'])
        bet_type, bet_info = best_value_bet
        
        if bet_info['value'] < self.value_threshold:
            return {"recommended_bet": 0, "reason": f"Value слишком низкое: {bet_info['value']:.3f}"}
        
        # Рассчитываем размер ставки по выбранной стратегии
        bet_size = self._calculate_by_strategy(bet_info, prediction_data)
        
        # Применяем лимиты
        bet_size = self._apply_limits(bet_size)
        
        # Дополнительная информация
        roi_expectation = bet_info['value'] * 100
        risk_level = self._assess_risk_level(bet_info, prediction_data)
        
        return {
            "recommended_bet": bet_size,
            "bet_type": bet_type,
            "odds": bet_info['odds'],
            "our_probability": bet_info['our_probability'],
            "bookmaker_probability": bet_info['bookmaker_probability'],
            "value": bet_info['value'],
            "expected_roi": roi_expectation,
            "risk_level": risk_level,
            "confidence": prediction_data.get('confidence', 0),
            "reason": f"Value ставка с ROI {roi_expectation:.1f}%"
        }
    
    def _calculate_by_strategy(self, bet_info: Dict, prediction_data: Dict) -> float:
        """Рассчитывает размер ставки по выбранной стратегии"""
        
        if self.strategy == BettingStrategy.KELLY_CRITERION:
            return self._kelly_bet_size(bet_info)
        
        elif self.strategy == BettingStrategy.FIXED_PERCENTAGE:
            return self.current_bankroll * self.fixed_percent
        
        elif self.strategy == BettingStrategy.VALUE_BETTING:
            return self._value_bet_size(bet_info)
        
        elif self.strategy == BettingStrategy.PROGRESSIVE:
            return self._progressive_bet_size(bet_info)
        
        elif self.strategy == BettingStrategy.CONSERVATIVE:
            return self._conservative_bet_size(bet_info, prediction_data)
        
        else:
            return self.current_bankroll * 0.02  # Fallback
    
    def _kelly_bet_size(self, bet_info: Dict) -> float:
        """Рассчитывает размер ставки по критерию Келли"""
        probability = bet_info['our_probability']
        odds = bet_info['odds']
        
        # Критерий Келли: f = (bp - q) / b
        # где b = odds - 1, p = вероятность выигрыша, q = вероятность проигрыша
        b = odds - 1
        p = probability
        q = 1 - probability
        
        kelly_fraction = (b * p - q) / b
        kelly_fraction = max(0, kelly_fraction)  # Не ставим при отрицательном Келли
        
        # Применяем консервативный множитель
        kelly_fraction *= self.kelly_multiplier
        
        return self.current_bankroll * kelly_fraction
    
    def _value_bet_size(self, bet_info: Dict) -> float:
        """Размер ставки пропорционален value"""
        value = bet_info['value']
        base_percentage = 0.01  # 1% базовый
        value_multiplier = min(value * 10, 0.04)  # Максимум 4% при value 0.4+
        
        return self.current_bankroll * (base_percentage + value_multiplier)
    
    def _progressive_bet_size(self, bet_info: Dict) -> float:
        """Прогрессивная система с учетом streaks"""
        base_bet = self.current_bankroll * 0.02
        
        # Увеличиваем ставку при победной серии
        if self.current_streak > 0:
            streak_multiplier = 1 + (self.current_streak * 0.1)
            streak_multiplier = min(streak_multiplier, 2.0)  # Максимум x2
            base_bet *= streak_multiplier
        
        # Уменьшаем при проигрышной серии
        elif self.current_streak < 0:
            loss_multiplier = 1 / (1 + abs(self.current_streak) * 0.1)
            loss_multiplier = max(loss_multiplier, 0.5)  # Минимум x0.5
            base_bet *= loss_multiplier
        
        return base_bet
    
    def _conservative_bet_size(self, bet_info: Dict, prediction_data: Dict) -> float:
        """Консервативная стратегия с акцентом на сохранение капитала"""
        confidence = prediction_data.get('confidence', 0.5)
        value = bet_info['value']
        
        # Базовая ставка только при высокой уверенности
        if confidence < 0.7:
            return 0
        
        # Очень маленькие ставки при низком value
        if value < 0.1:
            return self.current_bankroll * 0.005
        
        # Умеренные ставки при хорошем value и высокой уверенности
        return self.current_bankroll * min(0.015, value * 0.1)
    
    def _apply_limits(self, bet_size: float) -> float:
        """Применяет лимиты к размеру ставки"""
        # Минимальная ставка
        if bet_size < self.min_bet:
            return 0
        
        # Максимум от банкролла
        max_bet = self.current_bankroll * self.single_bet_max_percent
        bet_size = min(bet_size, max_bet)
        
        # Округляем до 100 рублей
        return round(bet_size / 100) * 100
    
    def _check_daily_limits(self) -> bool:
        """Проверяет дневные лимиты"""
        today = datetime.now().date()
        today_bets = [bet for bet in self.bet_history if 
                     datetime.fromisoformat(bet['timestamp']).date() == today]
        
        today_total = sum(bet['amount'] for bet in today_bets)
        daily_limit = self.current_bankroll * self.daily_limit_percent
        
        return today_total < daily_limit
    
    def _assess_risk_level(self, bet_info: Dict, prediction_data: Dict) -> str:
        """Оценивает уровень риска ставки"""
        confidence = prediction_data.get('confidence', 0.5)
        value = bet_info['value']
        model_agreement = prediction_data.get('model_agreement', False)
        
        risk_score = 0
        
        # Уверенность модели
        if confidence > 0.8:
            risk_score += 3
        elif confidence > 0.6:
            risk_score += 2
        else:
            risk_score += 1
        
        # Value ставки
        if value > 0.15:
            risk_score += 3
        elif value > 0.08:
            risk_score += 2
        else:
            risk_score += 1
        
        # Согласие моделей
        if model_agreement:
            risk_score += 2
        
        if risk_score >= 7:
            return "НИЗКИЙ"
        elif risk_score >= 5:
            return "СРЕДНИЙ"
        else:
            return "ВЫСОКИЙ"
    
    def place_bet(self, amount: float, bet_type: str, odds: float, match_info: Dict) -> bool:
        """Размещает ставку и обновляет банкролл"""
        if amount <= 0 or amount > self.current_bankroll:
            return False
        
        bet_record = {
            "timestamp": datetime.now().isoformat(),
            "amount": amount,
            "bet_type": bet_type,
            "odds": odds,
            "match_info": match_info,
            "bankroll_before": self.current_bankroll,
            "status": "pending"
        }
        
        self.current_bankroll -= amount
        self.total_bets += 1
        self.bet_history.append(bet_record)
        
        self.save_data()
        
        print(f"💰 Ставка размещена: {amount:.0f} руб на {bet_type}, коэф. {odds}")
        print(f"💼 Остаток банкролла: {self.current_bankroll:.0f} руб")
        
        return True
    
    def resolve_bet(self, bet_index: int, won: bool) -> Dict:
        """Разрешает результат ставки"""
        if bet_index >= len(self.bet_history):
            return {"error": "Ставка не найдена"}
        
        bet = self.bet_history[bet_index]
        if bet["status"] != "pending":
            return {"error": "Ставка уже разрешена"}
        
        if won:
            payout = bet["amount"] * bet["odds"]
            self.current_bankroll += payout
            bet["status"] = "won"
            bet["payout"] = payout
            self.winning_bets += 1
            self.current_streak = max(0, self.current_streak) + 1
            
            print(f"🎉 Ставка выиграла! Выплата: {payout:.0f} руб")
        else:
            bet["status"] = "lost"
            bet["payout"] = 0
            self.current_streak = min(0, self.current_streak) - 1
            
            print(f"😞 Ставка проиграла")
        
        # Обновляем статистику
        self.peak_bankroll = max(self.peak_bankroll, self.current_bankroll)
        drawdown = (self.peak_bankroll - self.current_bankroll) / self.peak_bankroll
        self.max_drawdown = max(self.max_drawdown, drawdown)
        
        self.save_data()
        
        return {
            "result": "won" if won else "lost",
            "new_bankroll": self.current_bankroll,
            "profit_loss": payout - bet["amount"] if won else -bet["amount"]
        }
    
    def get_statistics(self) -> Dict:
        """Возвращает детальную статистику"""
        if self.total_bets == 0:
            win_rate = 0
            avg_bet = 0
            total_staked = 0
            total_return = 0
        else:
            win_rate = (self.winning_bets / self.total_bets) * 100
            total_staked = sum(bet["amount"] for bet in self.bet_history)
            total_return = sum(bet.get("payout", 0) for bet in self.bet_history)
            avg_bet = total_staked / self.total_bets
        
        profit_loss = self.current_bankroll - self.initial_bankroll
        roi = (profit_loss / self.initial_bankroll) * 100
        
        return {
            "current_bankroll": self.current_bankroll,
            "initial_bankroll": self.initial_bankroll,
            "profit_loss": profit_loss,
            "roi_percent": roi,
            "total_bets": self.total_bets,
            "winning_bets": self.winning_bets,
            "win_rate": win_rate,
            "current_streak": self.current_streak,
            "max_drawdown": self.max_drawdown * 100,
            "total_staked": total_staked,
            "total_return": total_return,
            "average_bet": avg_bet,
            "strategy": self.strategy.value,
            "is_stop_loss_active": self.current_bankroll <= self.initial_bankroll * (1 - self.stop_loss_percent),
            "target_reached": profit_loss >= self.initial_bankroll * self.target_profit_percent
        }
    
    def get_recommendations(self) -> List[str]:
        """Возвращает рекомендации по управлению банкроллом"""
        recommendations = []
        stats = self.get_statistics()
        
        if stats["win_rate"] < 45:
            recommendations.append("⚠️ Низкий винрейт. Рассмотрите более консервативную стратегию")
        
        if stats["max_drawdown"] > 20:
            recommendations.append("⚠️ Высокая просадка. Уменьшите размеры ставок")
        
        if stats["current_streak"] < -3:
            recommendations.append("📉 Проигрышная серия. Возможно, стоит сделать перерыв")
        
        if stats["current_streak"] > 5:
            recommendations.append("📈 Отличная серия! Но не увлекайтесь размерами ставок")
        
        if stats["roi_percent"] > 20:
            recommendations.append("🎯 Отличная прибыльность! Рассмотрите увеличение банкролла")
        
        if stats["is_stop_loss_active"]:
            recommendations.append("🛑 Активирован стоп-лосс! Остановите ставки и пересмотрите стратегию")
        
        if stats["target_reached"]:
            recommendations.append("🎊 Цель достигнута! Рассмотрите вывод части прибыли")
        
        return recommendations
    
    def save_data(self):
        """Сохраняет данные в файл"""
        data = {
            "current_bankroll": self.current_bankroll,
            "initial_bankroll": self.initial_bankroll,
            "strategy": self.strategy.value,
            "bet_history": self.bet_history,
            "total_bets": self.total_bets,
            "winning_bets": self.winning_bets,
            "current_streak": self.current_streak,
            "max_drawdown": self.max_drawdown,
            "peak_bankroll": self.peak_bankroll,
            "last_updated": datetime.now().isoformat()
        }
        
        try:
            with open("smart_bankroll_data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Ошибка сохранения данных: {e}")
    
    def load_data(self):
        """Загружает данные из файла"""
        try:
            with open("smart_bankroll_data.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            
            self.current_bankroll = data.get("current_bankroll", self.initial_bankroll)
            self.bet_history = data.get("bet_history", [])
            self.total_bets = data.get("total_bets", 0)
            self.winning_bets = data.get("winning_bets", 0)
            self.current_streak = data.get("current_streak", 0)
            self.max_drawdown = data.get("max_drawdown", 0.0)
            self.peak_bankroll = data.get("peak_bankroll", self.initial_bankroll)
            
            # Обновляем стратегию если нужно
            saved_strategy = data.get("strategy", self.strategy.value)
            try:
                self.strategy = BettingStrategy(saved_strategy)
            except ValueError:
                logger.warning(f"Неизвестная стратегия: {saved_strategy}")
                
        except FileNotFoundError:
            # Создаем новый файл с базовыми данными
            self.save_data()
        except Exception as e:
            logger.error(f"Ошибка загрузки данных: {e}")
    
    def change_strategy(self, new_strategy: BettingStrategy):
        """Меняет стратегию управления банкроллом"""
        old_strategy = self.strategy
        self.strategy = new_strategy
        self.save_data()
        
        print(f"🔄 Стратегия изменена с {old_strategy.value} на {new_strategy.value}")
        
        # Даем рекомендации по новой стратегии
        strategy_info = {
            BettingStrategy.KELLY_CRITERION: "Математически оптимальные размеры ставок",
            BettingStrategy.FIXED_PERCENTAGE: "Фиксированный процент от банкролла",
            BettingStrategy.VALUE_BETTING: "Ставки пропорциональны найденному value",
            BettingStrategy.PROGRESSIVE: "Размер зависит от серий побед/поражений",
            BettingStrategy.CONSERVATIVE: "Минимальный риск, сохранение капитала"
        }
        
        print(f"📊 {strategy_info.get(new_strategy, 'Описание недоступно')}")
    
    def get_bankroll_info(self) -> Dict:
        """Возвращает информацию о банкролле (алиас для get_statistics)"""
        stats = self.get_statistics()
        return {
            'current_balance': stats['current_bankroll'],
            'initial_balance': stats['initial_bankroll'],
            'total_profit': stats['profit_loss'],
            'roi': stats['roi_percent'] / 100,
            'total_bets': stats['total_bets'],
            'winning_bets': stats['winning_bets'],
            'losing_bets': stats['total_bets'] - stats['winning_bets'],
            'win_rate': stats['win_rate'] / 100,
            'max_drawdown': stats['max_drawdown'] / 100,
            'current_streak': stats['current_streak']
        }
    
    def get_betting_history(self) -> List[Dict]:
        """Возвращает историю ставок"""
        return self.bet_history 