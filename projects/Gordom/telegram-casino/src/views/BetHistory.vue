<template>
  <div class="bet-history-page">
    <!-- Заголовок -->
    <div class="page-header">
      <h1 class="page-title">История ставок</h1>
      <div class="balance-info">
        <span class="balance-label">Баланс:</span>
        <span class="balance-amount">{{ userStore.formattedBalance }}</span>
      </div>
    </div>

    <!-- Статистика -->
    <div v-if="betsStore.betStats" class="stats-section">
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-value">{{ betsStore.betStats.total_bets }}</div>
          <div class="stat-label">Всего ставок</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">{{ betsStore.winRate.toFixed(1) }}%</div>
          <div class="stat-label">Процент выигрышей</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">{{ betsStore.totalProfit.toFixed(2) }}₽</div>
          <div class="stat-label" :class="{ 'positive': betsStore.totalProfit > 0, 'negative': betsStore.totalProfit < 0 }">
            Общий профит
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-value">{{ betsStore.betStats.favorite_sport }}</div>
          <div class="stat-label">Любимый спорт</div>
        </div>
      </div>
    </div>

    <!-- Фильтры -->
    <div class="filters-section">
      <div class="filter-group">
        <label class="filter-label">Показать:</label>
        <select v-model="filterType" @change="applyFilters" class="filter-select">
          <option value="all">Все ставки</option>
          <option value="win">Выигрыши</option>
          <option value="lose">Проигрыши</option>
          <option value="active">Активные</option>
        </select>
      </div>

      <button @click="refreshHistory" :disabled="loading" class="refresh-btn">
        <span v-if="loading">Загрузка...</span>
        <span v-else>Обновить</span>
      </button>
    </div>

    <!-- История ставок -->
    <div class="history-section">
      <div v-if="loading" class="loading-state">
        <div class="loading-spinner"></div>
        <p>Загрузка истории...</p>
      </div>

      <div v-else-if="filteredHistory.length === 0" class="empty-state">
        <p>История ставок пуста</p>
        <p class="empty-subtitle">Сделайте свою первую ставку!</p>
        <router-link to="/sports" class="go-to-sports-btn">
          К спортивным ставкам
        </router-link>
      </div>

      <div v-else class="history-list">
        <div
          v-for="bet in filteredHistory"
          :key="bet.id"
          class="bet-item"
          :class="{ 'win': bet.result === 'win', 'lose': bet.result === 'lose', 'active': bet.status === 'active' }"
        >
          <div class="bet-header">
            <div class="event-name">{{ bet.event_name }}</div>
            <div class="bet-date">{{ formatDate(bet.created_at) }}</div>
          </div>

          <div class="bet-details">
            <div class="bet-info">
              <span class="bet-type">{{ bet.bet_type_name }}</span>
              <span class="bet-odds">×{{ bet.odds }}</span>
            </div>

            <div class="bet-amounts">
              <div class="stake">Ставка: {{ bet.amount }}₽</div>
              <div v-if="bet.result" class="result" :class="bet.result">
                {{ bet.result === 'win' ? '+' : '' }}{{ bet.profit.toFixed(2) }}₽
              </div>
              <div v-else class="potential">
                ~{{ (bet.amount * bet.odds).toFixed(2) }}₽
              </div>
            </div>
          </div>

          <div v-if="bet.status === 'active'" class="bet-status active">
            <span class="status-dot"></span>
            Активна
          </div>
          <div v-else-if="bet.result === 'win'" class="bet-status win">
            <span class="status-icon">✓</span>
            Выигрыш
          </div>
          <div v-else-if="bet.result === 'lose'" class="bet-status lose">
            <span class="status-icon">✕</span>
            Проигрыш
          </div>
        </div>
      </div>

      <!-- Загрузить еще -->
      <div v-if="hasMore && !loading" class="load-more-section">
        <button @click="loadMore" class="load-more-btn">
          Загрузить еще
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '../stores/user'
import { useBetsStore } from '../stores/bets'

export default {
  name: 'BetHistory',
  setup() {
    const userStore = useUserStore()
    const betsStore = useBetsStore()

    const loading = ref(false)
    const filterType = ref('all')
    const currentPage = ref(1)
    const hasMore = ref(true)

    const filteredHistory = computed(() => {
      let history = betsStore.betHistory

      switch (filterType.value) {
        case 'win':
          return history.filter(bet => bet.result === 'win')
        case 'lose':
          return history.filter(bet => bet.result === 'lose')
        case 'active':
          return betsStore.activeBets
        default:
          return history
      }
    })

    const loadHistory = async (append = false) => {
      loading.value = true
      try {
        const limit = 25
        await betsStore.loadUserBets()

        if (!append) {
          currentPage.value = 1
        }

        // Имитация пагинации
        const allHistory = await betsStore.getBetHistory(limit * currentPage.value)
        hasMore.value = allHistory.length >= limit * currentPage.value
      } catch (error) {
        console.error('Failed to load bet history:', error)
      } finally {
        loading.value = false
      }
    }

    const loadMore = async () => {
      currentPage.value++
      await loadHistory(true)
    }

    const refreshHistory = async () => {
      await loadHistory(false)
    }

    const applyFilters = () => {
      // Фильтры применяются автоматически через computed
    }

    const formatDate = (dateString) => {
      const date = new Date(dateString)
      const now = new Date()
      const diff = now - date

      if (diff < 60000) return 'Только что'
      if (diff < 3600000) return `${Math.floor(diff / 60000)} мин назад`
      if (diff < 86400000) return `${Math.floor(diff / 3600000)} ч назад`
      if (diff < 604800000) return `${Math.floor(diff / 86400000)} д назад`

      return date.toLocaleDateString('ru-RU')
    }

    onMounted(async () => {
      await loadHistory()
    })

    return {
      userStore,
      betsStore,
      loading,
      filterType,
      filteredHistory,
      hasMore,
      loadMore,
      refreshHistory,
      applyFilters,
      formatDate
    }
  }
}
</script>

<style scoped>
.bet-history-page {
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

.stats-section {
  background: rgba(255, 255, 255, 0.1);
  padding: 20px;
  border-radius: 15px;
  margin-bottom: 30px;
  backdrop-filter: blur(10px);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.stat-card {
  text-align: center;
  padding: 15px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
}

.stat-value {
  font-size: 1.8rem;
  font-weight: bold;
  color: #ffd700;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 0.9rem;
  opacity: 0.8;
}

.stat-label.positive {
  color: #28a745;
}

.stat-label.negative {
  color: #dc3545;
}

.filters-section {
  background: rgba(255, 255, 255, 0.1);
  padding: 20px;
  border-radius: 15px;
  margin-bottom: 30px;
  backdrop-filter: blur(10px);
  display: flex;
  gap: 20px;
  align-items: center;
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.filter-label {
  font-size: 0.9rem;
  font-weight: 500;
}

.filter-select {
  padding: 10px 15px;
  border-radius: 10px;
  border: none;
  background: rgba(255, 255, 255, 0.9);
  color: #333;
  font-size: 0.9rem;
  min-width: 180px;
}

.refresh-btn {
  padding: 10px 20px;
  border-radius: 10px;
  border: none;
  background: #ffd700;
  color: #333;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}

.refresh-btn:hover:not(:disabled) {
  background: #ffed4e;
  transform: translateY(-2px);
}

.refresh-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.history-section {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 15px;
  backdrop-filter: blur(10px);
  overflow: hidden;
}

.loading-state,
.empty-state {
  text-align: center;
  padding: 60px 20px;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-top: 4px solid #ffd700;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-subtitle {
  opacity: 0.7;
  font-size: 0.9rem;
  margin-bottom: 20px;
}

.go-to-sports-btn {
  display: inline-block;
  padding: 12px 24px;
  border-radius: 25px;
  background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
  color: white;
  text-decoration: none;
  font-weight: bold;
  transition: all 0.3s ease;
}

.go-to-sports-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(40, 167, 69, 0.3);
}

.history-list {
  max-height: 60vh;
  overflow-y: auto;
}

.bet-item {
  padding: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.bet-item:hover {
  background: rgba(255, 255, 255, 0.05);
}

.bet-item:last-child {
  border-bottom: none;
}

.bet-item.active {
  border-left: 4px solid #007bff;
}

.bet-item.win {
  border-left: 4px solid #28a745;
}

.bet-item.lose {
  border-left: 4px solid #dc3545;
}

.bet-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.event-name {
  font-weight: 600;
  color: #fff;
}

.bet-date {
  font-size: 0.8rem;
  opacity: 0.7;
}

.bet-details {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.bet-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.bet-type {
  font-weight: 500;
  color: #ffd700;
}

.bet-odds {
  font-size: 0.9rem;
  opacity: 0.8;
}

.bet-amounts {
  text-align: right;
}

.stake {
  font-size: 0.9rem;
  opacity: 0.8;
  margin-bottom: 5px;
}

.result.win {
  font-size: 1.1rem;
  font-weight: bold;
  color: #28a745;
}

.result.lose {
  font-size: 1.1rem;
  font-weight: bold;
  color: #dc3545;
}

.potential {
  font-size: 1rem;
  color: #007bff;
}

.bet-status {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 0.8rem;
  font-weight: 500;
  padding: 4px 8px;
  border-radius: 10px;
  width: fit-content;
}

.bet-status.active {
  background: rgba(0, 123, 255, 0.2);
  color: #007bff;
}

.bet-status.win {
  background: rgba(40, 167, 69, 0.2);
  color: #28a745;
}

.bet-status.lose {
  background: rgba(220, 53, 69, 0.2);
  color: #dc3545;
}

.status-dot {
  width: 6px;
  height: 6px;
  background: currentColor;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

.status-icon {
  font-size: 0.9rem;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.load-more-section {
  padding: 20px;
  text-align: center;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.load-more-btn {
  padding: 12px 24px;
  border-radius: 25px;
  border: 2px solid #ffd700;
  background: transparent;
  color: #ffd700;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}

.load-more-btn:hover {
  background: #ffd700;
  color: #333;
}

/* Адаптивность */
@media (max-width: 768px) {
  .bet-history-page {
    padding: 15px;
  }

  .page-header {
    flex-direction: column;
    gap: 15px;
    text-align: center;
  }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .filters-section {
    flex-direction: column;
    align-items: stretch;
  }

  .filter-group {
    width: 100%;
  }

  .filter-select {
    min-width: auto;
    width: 100%;
  }

  .bet-details {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }

  .bet-amounts {
    text-align: left;
  }
}
</style>
