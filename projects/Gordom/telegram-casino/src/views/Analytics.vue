<template>
  <div class="analytics-page">
    <!-- Заголовок -->
    <div class="page-header">
      <h1 class="page-title">📊 Аналитика и статистика</h1>
      <div class="balance-info">
        <span class="balance-label">Баланс:</span>
        <span class="balance-amount">{{ userStore.formattedBalance }}</span>
      </div>
    </div>

    <!-- Основные метрики -->
    <div class="metrics-grid">
      <div class="metric-card primary">
        <div class="metric-icon">💰</div>
        <div class="metric-content">
          <div class="metric-value">{{ formatCurrency(betsStore.betStats?.total_profit || 0) }}</div>
          <div class="metric-label">Общий профит</div>
          <div class="metric-change" :class="{ 'positive': (betsStore.betStats?.total_profit || 0) > 0 }">
            <span v-if="(betsStore.betStats?.total_profit || 0) > 0">↗️</span>
            <span v-else-if="(betsStore.betStats?.total_profit || 0) < 0">↘️</span>
            <span v-else>➡️</span>
            {{ Math.abs(betsStore.betStats?.total_profit || 0) }}₽
          </div>
        </div>
      </div>

      <div class="metric-card success">
        <div class="metric-icon">🎯</div>
        <div class="metric-content">
          <div class="metric-value">{{ betsStore.winRate.toFixed(1) }}%</div>
          <div class="metric-label">Процент выигрышей</div>
          <div class="metric-change" :class="{ 'positive': betsStore.winRate > 50 }">
            <span v-if="betsStore.winRate > 50">🎉</span>
            <span v-else-if="betsStore.winRate < 50">😞</span>
            <span v-else>⚖️</span>
            {{ betsStore.winRate > 50 ? 'Выше среднего' : betsStore.winRate < 50 ? 'Ниже среднего' : 'Средний' }}
          </div>
        </div>
      </div>

      <div class="metric-card info">
        <div class="metric-icon">📈</div>
        <div class="metric-content">
          <div class="metric-value">{{ betsStore.betStats?.total_bets || 0 }}</div>
          <div class="metric-label">Всего ставок</div>
          <div class="metric-change">
            <span>📊</span>
            Активность
          </div>
        </div>
      </div>

      <div class="metric-card warning">
        <div class="metric-icon">🏆</div>
        <div class="metric-content">
          <div class="metric-value">{{ betsStore.betStats?.favorite_sport || 'Не определен' }}</div>
          <div class="metric-label">Любимый спорт</div>
          <div class="metric-change">
            <span>⭐</span>
            Предпочтение
          </div>
        </div>
      </div>
    </div>

    <!-- Графики и диаграммы -->
    <div class="charts-section">
      <div class="chart-card">
        <h3 class="chart-title">📊 Динамика профита</h3>
        <div class="chart-container">
          <div class="profit-chart">
            <div class="chart-placeholder">
              <div class="chart-icon">📈</div>
              <p>График профита по месяцам</p>
              <div class="mock-chart">
                <div
                  v-for="month in betsStore.betStats?.monthly_stats || []"
                  :key="month.month"
                  class="chart-bar"
                  :style="{ height: Math.max(20, (month.profit + 200) * 0.5) + 'px' }"
                  :class="{ 'positive': month.profit > 0, 'negative': month.profit < 0 }"
                >
                  <span class="bar-value">{{ month.profit }}₽</span>
                  <span class="bar-label">{{ month.month }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="chart-card">
        <h3 class="chart-title">🎯 Распределение ставок</h3>
        <div class="chart-container">
          <div class="pie-chart">
            <div class="pie-placeholder">
              <div class="pie-icon">🥧</div>
              <p>Распределение по видам спорта</p>
              <div class="mock-pie">
                <div class="pie-segment segment-1">
                  <span class="segment-label">Футбол</span>
                  <span class="segment-value">45%</span>
                </div>
                <div class="pie-segment segment-2">
                  <span class="segment-label">CS:GO</span>
                  <span class="segment-value">30%</span>
                </div>
                <div class="pie-segment segment-3">
                  <span class="segment-label">Dota 2</span>
                  <span class="segment-value">15%</span>
                </div>
                <div class="pie-segment segment-4">
                  <span class="segment-label">Другое</span>
                  <span class="segment-value">10%</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Детальная статистика -->
    <div class="detailed-stats">
      <h2 class="section-title">📋 Детальная статистика</h2>

      <div class="stats-grid">
        <div class="stat-item">
          <div class="stat-icon">🎲</div>
          <div class="stat-info">
            <div class="stat-number">{{ betsStore.betStats?.total_bets || 0 }}</div>
            <div class="stat-label">Всего ставок</div>
          </div>
        </div>

        <div class="stat-item">
          <div class="stat-icon">✅</div>
          <div class="stat-info">
            <div class="stat-number">{{ betsStore.winningBets.length }}</div>
            <div class="stat-label">Выигрышные ставки</div>
          </div>
        </div>

        <div class="stat-item">
          <div class="stat-icon">❌</div>
          <div class="stat-info">
            <div class="stat-number">{{ betsStore.losingBets.length }}</div>
            <div class="stat-label">Проигрышные ставки</div>
          </div>
        </div>

        <div class="stat-item">
          <div class="stat-icon">💰</div>
          <div class="stat-info">
            <div class="stat-number">{{ formatCurrency(betsStore.betStats?.biggest_win || 0) }}</div>
            <div class="stat-label">Самый большой выигрыш</div>
          </div>
        </div>

        <div class="stat-item">
          <div class="stat-icon">📉</div>
          <div class="stat-info">
            <div class="stat-number">{{ formatCurrency(betsStore.betStats?.biggest_lose || 0) }}</div>
            <div class="stat-label">Самый большой проигрыш</div>
          </div>
        </div>

        <div class="stat-item">
          <div class="stat-icon">⏱️</div>
          <div class="stat-info">
            <div class="stat-number">{{ calculateAvgBetAmount() }}</div>
            <div class="stat-label">Средняя ставка</div>
          </div>
        </div>
      </div>
    </div>

    <!-- AI рекомендации -->
    <div class="ai-recommendations">
      <h2 class="section-title">🤖 AI Рекомендации</h2>

      <div class="recommendations-grid">
        <div class="recommendation-card">
          <div class="rec-icon">🎯</div>
          <div class="rec-content">
            <h4 class="rec-title">Оптимальный размер ставки</h4>
            <p class="rec-description">
              Рекомендуемый размер ставки: {{ calculateOptimalBetSize() }}₽
              ({{ Math.round(((betsStore.betStats?.total_profit || 0) / (betsStore.betStats?.total_bets || 1)) * 100) / 100 }}% от баланса)
            </p>
          </div>
        </div>

        <div class="recommendation-card">
          <div class="rec-icon">📊</div>
          <div class="rec-content">
            <h4 class="rec-title">Лучшее время для ставок</h4>
            <p class="rec-description">
              Ваша win rate выше в вечернее время (18:00-22:00).
              Рекомендуем ставить в этот период.
            </p>
          </div>
        </div>

        <div class="recommendation-card">
          <div class="rec-icon">⚠️</div>
          <div class="rec-content">
            <h4 class="rec-title">Предупреждение о рисках</h4>
            <p class="rec-description">
              {{ getRiskWarning() }}
            </p>
          </div>
        </div>

        <div class="recommendation-card">
          <div class="rec-icon">🎮</div>
          <div class="rec-content">
            <h4 class="rec-title">Рекомендуемый спорт</h4>
            <p class="rec-description">
              {{ getSportRecommendation() }}
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- История ставок с фильтрами -->
    <div class="recent-bets">
      <h2 class="section-title">🕐 Последние ставки</h2>

      <div class="bets-filter">
        <button
          v-for="filter in betFilters"
          :key="filter.value"
          @click="activeBetFilter = filter.value"
          class="filter-btn"
          :class="{ 'active': activeBetFilter === filter.value }"
        >
          {{ filter.label }}
        </button>
      </div>

      <div class="bets-list">
        <div
          v-for="bet in filteredRecentBets"
          :key="bet.id"
          class="bet-card"
          :class="{ 'win': bet.result === 'win', 'lose': bet.result === 'lose', 'pending': !bet.result }"
        >
          <div class="bet-header">
            <div class="bet-event">{{ bet.event_name }}</div>
            <div class="bet-time">{{ formatTime(bet.created_at) }}</div>
          </div>

          <div class="bet-details">
            <div class="bet-type">{{ bet.bet_type_name }}</div>
            <div class="bet-odds">×{{ bet.odds }}</div>
            <div class="bet-amount">{{ bet.amount }}₽</div>
            <div v-if="bet.result" class="bet-result" :class="bet.result">
              {{ bet.result === 'win' ? '+' : '' }}{{ bet.profit }}₽
            </div>
            <div v-else class="bet-potential">
              ~{{ (bet.amount * bet.odds).toFixed(2) }}₽
            </div>
          </div>

          <div class="bet-status" :class="{ 'active': !bet.result }">
            <span v-if="!bet.result">⏳</span>
            <span v-else-if="bet.result === 'win'">✅</span>
            <span v-else>❌</span>
            {{ !bet.result ? 'Активна' : bet.result === 'win' ? 'Выигрыш' : 'Проигрыш' }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useUserStore } from '../stores/user'
import { useBetsStore } from '../stores/bets'

export default {
  name: 'Analytics',
  setup() {
    const userStore = useUserStore()
    const betsStore = useBetsStore()

    return {
      userStore,
      betsStore
    }
  },
  data() {
    return {
      activeBetFilter: 'all',
      betFilters: [
        { value: 'all', label: 'Все' },
        { value: 'win', label: 'Выигрыши' },
        { value: 'lose', label: 'Проигрыши' },
        { value: 'pending', label: 'Активные' }
      ]
    }
  },
  computed: {
    filteredRecentBets() {
      const recentBets = this.betsStore.betHistory.slice(0, 10)

      switch (this.activeBetFilter) {
        case 'win':
          return recentBets.filter(bet => bet.result === 'win')
        case 'lose':
          return recentBets.filter(bet => bet.result === 'lose')
        case 'pending':
          return this.betsStore.activeBets.slice(0, 10)
        default:
          return recentBets
      }
    }
  },
  methods: {
    formatCurrency(amount) {
      return Number(amount).toFixed(2) + ' ₽'
    },

    formatTime(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString('ru-RU', {
        day: 'numeric',
        month: 'short',
        hour: '2-digit',
        minute: '2-digit'
      })
    },

    calculateAvgBetAmount() {
      const totalAmount = this.betsStore.betHistory.reduce((sum, bet) => sum + bet.amount, 0)
      const totalBets = this.betsStore.betHistory.length
      return totalBets > 0 ? this.formatCurrency(totalAmount / totalBets) : '0 ₽'
    },

    calculateOptimalBetSize() {
      const balance = this.userStore.balance
      const winRate = this.betsStore.winRate / 100
      const avgBet = this.betsStore.betHistory.length > 0
        ? this.betsStore.betHistory.reduce((sum, bet) => sum + bet.amount, 0) / this.betsStore.betHistory.length
        : 100

      // Простая формула Келли для расчета оптимального размера ставки
      const kellyMultiplier = winRate - ((1 - winRate) / (avgBet * 0.01))
      const optimalBet = Math.max(10, Math.min(balance * 0.1, kellyMultiplier * balance * 0.02))

      return Math.round(optimalBet)
    },

    getRiskWarning() {
      const winRate = this.betsStore.winRate
      const totalBets = this.betsStore.betStats?.total_bets || 0
      const profit = this.betsStore.betStats?.total_profit || 0

      if (winRate < 40 && totalBets > 10) {
        return "Ваш процент выигрышей ниже 40%. Рекомендуем пересмотреть стратегию ставок."
      } else if (profit < -1000) {
        return "Общий профит отрицательный. Возможно, стоит временно снизить активность."
      } else if (totalBets < 5) {
        return "У вас мало ставок для анализа. Продолжайте собирать статистику."
      } else {
        return "Ваша статистика выглядит хорошо! Продолжайте в том же духе."
      }
    },

    getSportRecommendation() {
      const favoriteSport = this.betsStore.betStats?.favorite_sport || 'Футбол'

      if (favoriteSport === 'CS:GO') {
        return "CS:GO - ваш любимый спорт. Рекомендуем сосредоточиться на ESL Pro League и Major турнирах."
      } else if (favoriteSport === 'Футбол') {
        return "Футбол - ваш выбор. Обращайте внимание на топовые лиги: Премьер-лига, Ла Лига, Бундеслига."
      } else if (favoriteSport === 'Dota 2') {
        return "Dota 2 - ваш спорт. The International и DPC - лучшие места для ставок."
      } else {
        return `Ваш любимый спорт - ${favoriteSport}. Фокусируйтесь на профессиональных турнирах.`
      }
    }
  }
}
</script>

<style scoped>
.analytics-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
  color: white;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  background: rgba(255, 255, 255, 0.1);
  padding: 20px;
  border-radius: 15px;
  backdrop-filter: blur(10px);
}

.page-title {
  font-size: 2rem;
  font-weight: bold;
  margin: 0;
  background: linear-gradient(45deg, #fff, #ffd700);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.balance-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.balance-label {
  font-size: 0.9rem;
  opacity: 0.8;
}

.balance-amount {
  font-size: 1.2rem;
  font-weight: bold;
  color: #ffd700;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.metric-card {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 25px;
  backdrop-filter: blur(15px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.metric-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #667eea, #764ba2);
}

.metric-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
}

.metric-card.primary::before {
  background: linear-gradient(90deg, #667eea, #764ba2);
}

.metric-card.success::before {
  background: linear-gradient(90deg, #28a745, #20c997);
}

.metric-card.info::before {
  background: linear-gradient(90deg, #17a2b8, #6f42c1);
}

.metric-card.warning::before {
  background: linear-gradient(90deg, #ffc107, #fd7e14);
}

.metric-content {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.metric-icon {
  font-size: 2rem;
  margin-bottom: 10px;
  opacity: 0.8;
}

.metric-value {
  font-size: 2rem;
  font-weight: 800;
  margin-bottom: 5px;
  background: linear-gradient(135deg, #fff, #ffd700);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.metric-label {
  font-size: 0.9rem;
  opacity: 0.8;
  font-weight: 500;
}

.metric-change {
  font-size: 0.8rem;
  font-weight: 600;
  padding: 4px 8px;
  border-radius: 10px;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  margin-top: 5px;
}

.metric-change.positive {
  background: rgba(40, 167, 69, 0.2);
  color: #28a745;
}

.charts-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.chart-card {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 25px;
  backdrop-filter: blur(15px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.chart-title {
  font-size: 1.2rem;
  font-weight: 700;
  margin-bottom: 20px;
  color: #fff;
}

.chart-container {
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chart-placeholder {
  text-align: center;
  color: rgba(255, 255, 255, 0.7);
}

.chart-icon {
  font-size: 2rem;
  margin-bottom: 10px;
}

.mock-chart {
  display: flex;
  align-items: end;
  gap: 10px;
  height: 120px;
  margin-top: 20px;
}

.chart-bar {
  flex: 1;
  background: linear-gradient(180deg, #667eea, #764ba2);
  border-radius: 5px 5px 0 0;
  position: relative;
  transition: all 0.3s ease;
  min-height: 20px;
}

.chart-bar:hover {
  opacity: 0.8;
  transform: scale(1.05);
}

.chart-bar.positive {
  background: linear-gradient(180deg, #28a745, #20c997);
}

.chart-bar.negative {
  background: linear-gradient(180deg, #dc3545, #fd7e14);
}

.bar-value {
  position: absolute;
  top: -25px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 0.7rem;
  font-weight: 600;
  color: #fff;
  background: rgba(0, 0, 0, 0.7);
  padding: 2px 6px;
  border-radius: 4px;
}

.bar-label {
  position: absolute;
  bottom: -20px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 0.7rem;
  color: rgba(255, 255, 255, 0.7);
}

.mock-pie {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 20px;
}

.pie-segment {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.1);
}

.segment-1 { border-left: 4px solid #667eea; }
.segment-2 { border-left: 4px solid #28a745; }
.segment-3 { border-left: 4px solid #dc3545; }
.segment-4 { border-left: 4px solid #ffc107; }

.segment-label {
  font-weight: 600;
  color: #fff;
}

.segment-value {
  font-weight: 700;
  color: rgba(255, 255, 255, 0.8);
}

.detailed-stats {
  margin-bottom: 30px;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 20px;
  color: #fff;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.stat-item {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 15px;
  padding: 20px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  gap: 15px;
  transition: all 0.3s ease;
}

.stat-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.stat-icon {
  font-size: 1.5rem;
  opacity: 0.8;
}

.stat-info {
  flex: 1;
}

.stat-number {
  font-size: 1.5rem;
  font-weight: 800;
  color: #ffd700;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 0.9rem;
  opacity: 0.8;
  font-weight: 500;
}

.ai-recommendations {
  margin-bottom: 30px;
}

.recommendations-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.recommendation-card {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 15px;
  padding: 20px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: flex-start;
  gap: 15px;
  transition: all 0.3s ease;
}

.recommendation-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.rec-icon {
  font-size: 1.5rem;
  opacity: 0.8;
  flex-shrink: 0;
}

.rec-content {
  flex: 1;
}

.rec-title {
  font-size: 1rem;
  font-weight: 600;
  color: #fff;
  margin-bottom: 8px;
}

.rec-description {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.5;
  margin: 0;
}

.recent-bets {
  margin-bottom: 30px;
}

.bets-filter {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.filter-btn {
  padding: 10px 20px;
  border-radius: 25px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.filter-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.5);
}

.filter-btn.active {
  background: #667eea;
  border-color: #667eea;
  color: #fff;
}

.bets-list {
  display: grid;
  gap: 15px;
}

.bet-card {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 15px;
  padding: 20px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
}

.bet-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.bet-card.win {
  border-left: 4px solid #28a745;
}

.bet-card.lose {
  border-left: 4px solid #dc3545;
}

.bet-card.pending {
  border-left: 4px solid #ffc107;
}

.bet-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.bet-event {
  font-weight: 600;
  color: #fff;
  font-size: 0.9rem;
}

.bet-time {
  font-size: 0.8rem;
  opacity: 0.7;
}

.bet-details {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
  gap: 15px;
  margin-bottom: 10px;
}

.bet-type,
.bet-odds,
.bet-amount,
.bet-result,
.bet-potential {
  text-align: center;
  font-size: 0.9rem;
  font-weight: 600;
}

.bet-result.win {
  color: #28a745;
}

.bet-result.lose {
  color: #dc3545;
}

.bet-potential {
  color: #007bff;
}

.bet-status {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 0.8rem;
  font-weight: 600;
  padding: 5px 10px;
  border-radius: 15px;
  width: fit-content;
}

.bet-status.active {
  background: rgba(255, 193, 7, 0.2);
  color: #ffc107;
}

/* Адаптивность */
@media (max-width: 768px) {
  .analytics-page {
    padding: 15px;
  }

  .metrics-grid {
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  }

  .charts-section {
    grid-template-columns: 1fr;
  }

  .stats-grid {
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  }

  .recommendations-grid {
    grid-template-columns: 1fr;
  }

  .bet-details {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 480px) {
  .metrics-grid {
    grid-template-columns: 1fr;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .bet-details {
    grid-template-columns: 1fr;
  }

  .bets-filter {
    gap: 8px;
  }

  .filter-btn {
    padding: 8px 16px;
    font-size: 0.8rem;
  }
}
</style>
