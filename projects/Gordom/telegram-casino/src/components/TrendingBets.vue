<template>
  <div class="trending-bets">
    <div class="trending-header">
      <h2 class="trending-title">🔥 Популярные ставки</h2>
      <p class="trending-subtitle">Что выбирают другие игроки</p>
    </div>

    <div class="trending-grid">
      <div
        v-for="trend in trendingBets"
        :key="trend.id"
        class="trend-card"
        :class="trend.trend"
        @click="handleTrendClick(trend)"
      >
        <div class="trend-header">
          <div class="trend-sport">
            <span class="sport-icon">{{ trend.sportIcon }}</span>
            <span class="sport-name">{{ trend.sportName }}</span>
          </div>
          <div class="trend-popularity">
            <span class="popularity-badge" :class="trend.trend">
              {{ trend.popularity }}%
            </span>
          </div>
        </div>

        <div class="trend-content">
          <div class="event-name">{{ trend.eventName }}</div>
          <div class="bet-recommendation">
            <span class="rec-label">Популярный выбор:</span>
            <span class="rec-value">{{ trend.recommendation }}</span>
          </div>
          <div class="odds-info">
            <span class="current-odds">Коэф: {{ trend.odds }}</span>
            <span class="trend-indicator" :class="trend.trend">
              <span v-if="trend.trend === 'up'">📈</span>
              <span v-else-if="trend.trend === 'hot'">🔥</span>
              <span v-else>📊</span>
            </span>
          </div>
        </div>

        <div class="trend-footer">
          <div class="participants">
            <span class="participants-count">{{ trend.participants }} участников</span>
          </div>
          <div class="trend-action">
            <button class="follow-trend-btn" @click.stop="followTrend(trend)">
              <span>📈</span>
              <span>Следовать</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Статистика трендов -->
    <div class="trends-stats">
      <div class="stat-item">
        <div class="stat-icon">🎯</div>
        <div class="stat-info">
          <div class="stat-number">{{ totalParticipants }}</div>
          <div class="stat-label">Активных участников</div>
        </div>
      </div>

      <div class="stat-item">
        <div class="stat-icon">💰</div>
        <div class="stat-info">
          <div class="stat-number">{{ totalVolume.toLocaleString() }}₽</div>
          <div class="stat-label">Объем ставок</div>
        </div>
      </div>

      <div class="stat-item">
        <div class="stat-icon">🏆</div>
        <div class="stat-info">
          <div class="stat-number">{{ avgWinRate }}%</div>
          <div class="stat-label">Средний win rate</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TrendingBets',
  data() {
    return {
      trendingBets: [
        {
          id: 1,
          sportName: 'CS:GO',
          sportIcon: '🎮',
          eventName: 'FaZe Clan vs NaVi',
          recommendation: 'Победа NaVi',
          odds: '1.85',
          popularity: 78,
          trend: 'hot',
          participants: 1250,
          volume: 250000
        },
        {
          id: 2,
          sportName: 'Футбол',
          sportIcon: '⚽',
          eventName: 'Барселона vs Реал Мадрид',
          recommendation: 'Ничья',
          odds: '3.40',
          popularity: 65,
          trend: 'up',
          participants: 980,
          volume: 180000
        },
        {
          id: 3,
          sportName: 'Dota 2',
          sportIcon: '🎯',
          eventName: 'Team Spirit vs Team Liquid',
          recommendation: 'Победа Team Spirit',
          odds: '1.75',
          popularity: 72,
          trend: 'hot',
          participants: 890,
          volume: 145000
        },
        {
          id: 4,
          sportName: 'League of Legends',
          sportIcon: '🏆',
          eventName: 'T1 vs Gen.G',
          recommendation: 'Победа T1',
          odds: '1.65',
          popularity: 58,
          trend: 'steady',
          participants: 750,
          volume: 120000
        }
      ]
    }
  },
  computed: {
    totalParticipants() {
      return this.trendingBets.reduce((sum, trend) => sum + trend.participants, 0)
    },

    totalVolume() {
      return this.trendingBets.reduce((sum, trend) => sum + trend.volume, 0)
    },

    avgWinRate() {
      const avg = this.trendingBets.reduce((sum, trend) => sum + trend.popularity, 0) / this.trendingBets.length
      return Math.round(avg)
    }
  },
  methods: {
    handleTrendClick(trend) {
      // Переход к соответствующему событию
      this.$router.push({
        path: '/sports',
        query: {
          sport: trend.sportName.toLowerCase(),
          event: trend.eventName
        }
      })
    },

    followTrend(trend) {
      // Имитация следования тренду
      this.$emit('follow-trend', {
        trend: trend,
        action: 'follow'
      })

      // Показываем уведомление
      this.$emit('show-notification', {
        type: 'success',
        title: 'Тренд добавлен!',
        message: `Вы подписались на тренд: ${trend.recommendation}`
      })
    }
  }
}
</script>

<style scoped>
.trending-bets {
  margin: 30px 0;
}

.trending-header {
  text-align: center;
  margin-bottom: 30px;
}

.trending-title {
  font-size: 1.8rem;
  font-weight: 700;
  color: #fff;
  margin-bottom: 8px;
}

.trending-subtitle {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.7);
  margin: 0;
}

.trending-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.trend-card {
  background: linear-gradient(145deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%);
  border-radius: 20px;
  padding: 25px;
  backdrop-filter: blur(15px);
  border: 2px solid rgba(255, 255, 255, 0.2);
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.trend-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #667eea, #764ba2);
}

.trend-card.hot::before {
  background: linear-gradient(90deg, #ff6b6b, #ee5a24);
}

.trend-card.up::before {
  background: linear-gradient(90deg, #28a745, #20c997);
}

.trend-card:hover {
  transform: translateY(-5px) scale(1.02);
  box-shadow:
    0 20px 40px rgba(0, 0, 0, 0.15),
    0 8px 16px rgba(0, 0, 0, 0.1);
}

.trend-card.hot:hover {
  box-shadow:
    0 20px 40px rgba(255, 107, 107, 0.3),
    0 8px 16px rgba(255, 107, 107, 0.2);
}

.trend-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.trend-sport {
  display: flex;
  align-items: center;
  gap: 12px;
}

.sport-icon {
  font-size: 1.5rem;
  opacity: 0.8;
}

.sport-name {
  font-size: 1rem;
  font-weight: 600;
  color: #fff;
}

.trend-popularity {
  display: flex;
  align-items: center;
}

.popularity-badge {
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.popularity-badge.hot {
  background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
  color: white;
  animation: pulse 2s infinite;
}

.popularity-badge.up {
  background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
  color: white;
}

.popularity-badge.steady {
  background: linear-gradient(135deg, #6c757d 0%, #495057 100%);
  color: white;
}

.trend-content {
  margin-bottom: 20px;
}

.event-name {
  font-size: 1.1rem;
  font-weight: 600;
  color: #fff;
  margin-bottom: 12px;
  line-height: 1.3;
}

.bet-recommendation {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  padding: 10px 15px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 10px;
}

.rec-label {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.7);
  font-weight: 500;
}

.rec-value {
  font-size: 0.9rem;
  color: #ffd700;
  font-weight: 600;
}

.odds-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 15px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
}

.current-odds {
  font-size: 0.9rem;
  font-weight: 600;
  color: #fff;
}

.trend-indicator {
  font-size: 1.2rem;
  animation: bounce 1s infinite;
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
  40% { transform: translateY(-3px); }
  60% { transform: translateY(-1px); }
}

.trend-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 15px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.participants {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.7);
}

.follow-trend-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 5px;
}

.follow-trend-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.trends-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  padding: 25px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  backdrop-filter: blur(15px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 15px;
  text-align: center;
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

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

/* Адаптивность */
@media (max-width: 768px) {
  .trending-grid {
    grid-template-columns: 1fr;
  }

  .trends-stats {
    grid-template-columns: repeat(2, 1fr);
  }

  .trend-card {
    padding: 20px;
  }

  .trend-header {
    flex-direction: column;
    gap: 10px;
    align-items: flex-start;
  }

  .bet-recommendation,
  .odds-info {
    flex-direction: column;
    gap: 8px;
    align-items: flex-start;
  }
}

@media (max-width: 480px) {
  .trends-stats {
    grid-template-columns: 1fr;
  }

  .trending-title {
    font-size: 1.5rem;
  }

  .trend-card {
    padding: 15px;
  }
}
</style>
