<template>
  <div class="betting-interface">
    <!-- Header с навигацией -->
    <div class="interface-header">
      <div class="nav-tabs">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          @click="activeTab = tab.id"
          :class="['nav-tab', { active: activeTab === tab.id }]"
        >
          <i :class="tab.icon"></i>
          {{ tab.name }}
        </button>
      </div>

      <div class="header-actions">
        <button class="refresh-btn" @click="refreshData">
          <i class="fas fa-sync-alt"></i>
          Обновить
        </button>
        <div class="time-display">
          <i class="fas fa-clock"></i>
          {{ currentTime }}
        </div>
      </div>
    </div>

    <!-- Основной контент -->
    <div class="interface-content">
      <!-- Фильтры -->
      <div class="filters-panel">
        <div class="filter-group">
          <label>Вид спорта:</label>
          <select v-model="selectedSport" @change="applyFilters">
            <option value="all">Все виды спорта</option>
            <option value="football">⚽ Футбол</option>
            <option value="basketball">🏀 Баскетбол</option>
            <option value="tennis">🎾 Теннис</option>
            <option value="hockey">🏒 Хоккей</option>
            <option value="baseball">⚾ Бейсбол</option>
            <option value="csgo">🎮 CS:GO</option>
            <option value="dota2">🎯 Dota 2</option>
          </select>
        </div>

        <div class="filter-group">
          <label>Время:</label>
          <select v-model="timeFilter" @change="applyFilters">
            <option value="all">Все время</option>
            <option value="today">Сегодня</option>
            <option value="tomorrow">Завтра</option>
            <option value="week">На этой неделе</option>
            <option value="live">🔴 Live матчи</option>
          </select>
        </div>

        <div class="filter-group">
          <label>Сортировка:</label>
          <select v-model="sortBy" @change="applyFilters">
            <option value="time">По времени</option>
            <option value="popularity">По популярности</option>
            <option value="odds">По коэффициентам</option>
            <option value="league">По лиге</option>
          </select>
        </div>
      </div>

      <!-- Список событий -->
      <div class="events-list">
        <div v-if="loading" class="loading-state">
          <div class="spinner"></div>
          <p>Загрузка событий...</p>
        </div>

        <div v-else-if="events.length === 0" class="empty-state">
          <i class="fas fa-calendar-times"></i>
          <h3>События не найдены</h3>
          <p>Попробуйте изменить фильтры</p>
        </div>

        <div v-else class="events-container">
          <div
            v-for="event in events"
            :key="event.id"
            :class="['event-card', event.importance, { live: event.is_live }]"
          >
            <!-- Заголовок события -->
            <div class="event-header">
              <div class="event-info">
                <span class="league-name">{{ event.league }}</span>
                <span class="event-time">{{ formatTime(event.start_time) }}</span>
              </div>
              <div class="event-badges">
                <span v-if="event.is_live" class="badge live">🔴 LIVE</span>
                <span v-if="event.importance === 'high'" class="badge vip">⭐ VIP</span>
                <span v-if="event.has_stream" class="badge stream">📺 Прямая трансляция</span>
              </div>
            </div>

            <!-- Команды и счет -->
            <div class="event-main">
              <div class="team home">
                <div class="team-info">
                  <span class="team-name">{{ event.home_team }}</span>
                  <span v-if="event.is_live" class="live-score">{{ event.current_score?.home || 0 }}</span>
                </div>
              </div>

              <div class="vs-section">
                <div v-if="event.is_live" class="live-info">
                  <div class="match-time">{{ event.minute }}'</div>
                  <div class="period">{{ getPeriodText(event) }}</div>
                </div>
                <div v-else class="vs">VS</div>
              </div>

              <div class="team away">
                <div class="team-info">
                  <span class="team-name">{{ event.away_team }}</span>
                  <span v-if="event.is_live" class="live-score">{{ event.current_score?.away || 0 }}</span>
                </div>
              </div>
            </div>

            <!-- Коэффициенты -->
            <div class="odds-section">
              <div class="odds-group">
                <div class="odd-item" @click="placeBet(event, 'home', event.odds.home)">
                  <span class="odd-label">П1</span>
                  <span class="odd-value">{{ event.odds.home }}</span>
                </div>
                <div v-if="event.sport === 'football'" class="odd-item" @click="placeBet(event, 'draw', event.odds.draw)">
                  <span class="odd-label">X</span>
                  <span class="odd-value">{{ event.odds.draw }}</span>
                </div>
                <div class="odd-item" @click="placeBet(event, 'away', event.odds.away)">
                  <span class="odd-label">П2</span>
                  <span class="odd-value">{{ event.odds.away }}</span>
                </div>
              </div>

              <div class="additional-odds">
                <button class="expand-btn" @click="toggleExpanded(event)">
                  <i :class="event.expanded ? 'fas fa-chevron-up' : 'fas fa-chevron-down'"></i>
                  {{ event.expanded ? 'Скрыть' : 'Больше ставок' }}
                </button>
              </div>
            </div>

            <!-- Расширенные ставки -->
            <div v-if="event.expanded" class="expanded-odds">
              <div class="odds-categories">
                <div class="odds-category">
                  <h4>Тоталы</h4>
                  <div class="odd-grid">
                    <div class="odd-item" @click="placeBet(event, 'over_2_5', event.odds.over_2_5)">
                      <span class="odd-label">Больше 2.5</span>
                      <span class="odd-value">{{ event.odds.over_2_5 }}</span>
                    </div>
                    <div class="odd-item" @click="placeBet(event, 'under_2_5', event.odds.under_2_5)">
                      <span class="odd-label">Меньше 2.5</span>
                      <span class="odd-value">{{ event.odds.under_2_5 }}</span>
                    </div>
                  </div>
                </div>

                <div class="odds-category">
                  <h4>Обе забьют</h4>
                  <div class="odd-grid">
                    <div class="odd-item" @click="placeBet(event, 'btts_yes', event.odds.btts_yes)">
                      <span class="odd-label">Да</span>
                      <span class="odd-value">{{ event.odds.btts_yes }}</span>
                    </div>
                    <div class="odd-item" @click="placeBet(event, 'btts_no', event.odds.btts_no)">
                      <span class="odd-label">Нет</span>
                      <span class="odd-value">{{ event.odds.btts_no }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Корзина ставок -->
    <div v-if="betSlip.length > 0" class="bet-slip-panel">
      <div class="bet-slip-header">
        <h3>Корзина ставок ({{ betSlip.length }})</h3>
        <button class="close-btn" @click="toggleBetSlip">
          <i class="fas fa-times"></i>
        </button>
      </div>

      <div class="bet-slip-items">
        <div v-for="bet in betSlip" :key="bet.id" class="bet-item">
          <div class="bet-info">
            <span class="bet-event">{{ bet.event.home_team }} vs {{ bet.event.away_team }}</span>
            <span class="bet-type">{{ getBetTypeName(bet.type) }}</span>
          </div>
          <div class="bet-odds">{{ bet.odds }}</div>
          <button class="remove-bet" @click="removeBet(bet.id)">
            <i class="fas fa-trash"></i>
          </button>
        </div>
      </div>

      <div class="bet-slip-footer">
        <div class="total-odds">
          <span>Общий коэффициент:</span>
          <span class="total-value">{{ calculateTotalOdds() }}</span>
        </div>
        <button class="place-bets-btn" @click="placeBets">
          Сделать ставки
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'BettingInterface',
  data() {
    return {
      activeTab: 'all',
      selectedSport: 'all',
      timeFilter: 'all',
      sortBy: 'time',
      events: [],
      betSlip: [],
      loading: false,
      tabs: [
        { id: 'all', name: 'Все ставки', icon: 'fas fa-list' },
        { id: 'live', name: 'Live', icon: 'fas fa-play-circle' },
        { id: 'today', name: 'Сегодня', icon: 'fas fa-calendar-day' },
        { id: 'football', name: 'Футбол', icon: 'fas fa-futbol' },
        { id: 'basketball', name: 'Баскетбол', icon: 'fas fa-basketball-ball' },
        { id: 'tennis', name: 'Теннис', icon: 'fas fa-table-tennis' }
      ]
    }
  },
  computed: {
    currentTime() {
      return new Date().toLocaleTimeString('ru-RU', {
        hour: '2-digit',
        minute: '2-digit'
      })
    }
  },
  methods: {
    async loadEvents() {
      this.loading = true
      try {
        const { getSportsEvents } = await import('../api/endpoints.js')
        const events = await getSportsEvents(this.selectedSport)
        this.events = events.map(event => ({
          ...event,
          expanded: false
        }))
      } catch (error) {
        console.error('Error loading events:', error)
      } finally {
        this.loading = false
      }
    },

    applyFilters() {
      this.loadEvents()
    },

    formatTime(dateString) {
      const date = new Date(dateString)
      return date.toLocaleString('ru-RU', {
        day: '2-digit',
        month: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      })
    },

    getPeriodText(event) {
      if (event.sport === 'football') {
        if (event.minute <= 45) return '1-й тайм'
        return '2-й тайм'
      }
      if (event.sport === 'basketball') {
        return `${event.quarter || 1}-я четверть`
      }
      return ''
    },

    toggleExpanded(event) {
      event.expanded = !event.expanded
    },

    placeBet(event, type, odds) {
      const bet = {
        id: Date.now(),
        event: event,
        type: type,
        odds: odds,
        amount: 0
      }
      this.betSlip.push(bet)
    },

    removeBet(betId) {
      this.betSlip = this.betSlip.filter(bet => bet.id !== betId)
    },

    getBetTypeName(type) {
      const types = {
        home: 'Победа 1-й команды',
        draw: 'Ничья',
        away: 'Победа 2-й команды',
        over_2_5: 'Тотал больше 2.5',
        under_2_5: 'Тотал меньше 2.5',
        btts_yes: 'Обе забьют - Да',
        btts_no: 'Обе забьют - Нет'
      }
      return types[type] || type
    },

    calculateTotalOdds() {
      if (this.betSlip.length === 0) return 1
      return this.betSlip.reduce((total, bet) => total * bet.odds, 1).toFixed(2)
    },

    placeBets() {
      // Реализация ставки
      console.log('Placing bets:', this.betSlip)
    },

    toggleBetSlip() {
      // Toggle bet slip visibility
    },

    refreshData() {
      this.loadEvents()
    }
  },

  mounted() {
    this.loadEvents()
  }
}
</script>

<style scoped>
/* Основные стили интерфейса */
.betting-interface {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
  color: white;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Header */
.interface-header {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding: 20px 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-tabs {
  display: flex;
  gap: 5px;
  overflow-x: auto;
}

.nav-tab {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.7);
  padding: 12px 20px;
  border-radius: 25px;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
  font-size: 0.9rem;
  font-weight: 500;
}

.nav-tab:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  transform: translateY(-1px);
}

.nav-tab.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-color: rgba(102, 126, 234, 0.5);
  box-shadow: 0 0 20px rgba(102, 126, 234, 0.3);
}

.header-actions {
  display: flex;
  gap: 15px;
  align-items: center;
}

.refresh-btn, .time-display {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  padding: 10px 15px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.9rem;
}

.refresh-btn:hover {
  background: rgba(255, 255, 255, 0.15);
  transform: translateY(-1px);
}

/* Фильтры */
.filters-panel {
  background: rgba(255, 255, 255, 0.03);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding: 20px 30px;
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.filter-group label {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.8);
  font-weight: 500;
}

.filter-group select {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  padding: 10px 15px;
  border-radius: 10px;
  font-size: 0.9rem;
  cursor: pointer;
}

.filter-group select:focus {
  outline: none;
  border-color: rgba(102, 126, 234, 0.5);
  box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
}

/* События */
.events-list {
  padding: 30px;
}

.events-container {
  display: grid;
  gap: 20px;
}

.event-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 15px;
  padding: 20px;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.event-card:hover {
  background: rgba(255, 255, 255, 0.08);
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.event-card.live {
  border-color: #ff4757;
  box-shadow: 0 0 20px rgba(255, 71, 87, 0.3);
  animation: livePulse 2s infinite;
}

.event-card.high {
  border-left: 4px solid #ffd700;
}

@keyframes livePulse {
  0%, 100% { box-shadow: 0 0 20px rgba(255, 71, 87, 0.3); }
  50% { box-shadow: 0 0 30px rgba(255, 71, 87, 0.6); }
}

/* Заголовок события */
.event-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.event-info {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.league-name {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.7);
  font-weight: 500;
}

.event-time {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.5);
}

.event-badges {
  display: flex;
  gap: 8px;
}

.badge {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.7rem;
  font-weight: 600;
}

.badge.live {
  background: rgba(255, 71, 87, 0.3);
  color: #ff4757;
  border: 1px solid rgba(255, 71, 87, 0.5);
}

.badge.vip {
  background: rgba(255, 215, 0, 0.2);
  color: #ffd700;
  border: 1px solid rgba(255, 215, 0, 0.5);
}

.badge.stream {
  background: rgba(0, 123, 255, 0.2);
  color: #007bff;
  border: 1px solid rgba(0, 123, 255, 0.5);
}

/* Основная часть события */
.event-main {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.team {
  flex: 1;
  text-align: center;
}

.team-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.team-name {
  font-size: 1.1rem;
  font-weight: 600;
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.live-score {
  font-size: 1.5rem;
  font-weight: 800;
  color: #ffd700;
}

.vs-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
  min-width: 80px;
}

.vs {
  font-size: 1.2rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.5);
}

.live-info {
  text-align: center;
}

.match-time {
  font-size: 1.2rem;
  font-weight: 800;
  color: #ff4757;
}

.period {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.7);
}

/* Коэффициенты */
.odds-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.odds-group {
  display: flex;
  gap: 10px;
}

.odd-item {
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 8px;
  padding: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
  min-width: 60px;
}

.odd-item:hover {
  background: rgba(255, 255, 255, 0.15);
  transform: translateY(-1px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.odd-label {
  display: block;
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 2px;
}

.odd-value {
  display: block;
  font-size: 1.1rem;
  font-weight: 700;
  color: #ffd700;
}

.expand-btn {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: rgba(255, 255, 255, 0.8);
  padding: 8px 12px;
  border-radius: 20px;
  cursor: pointer;
  font-size: 0.8rem;
  transition: all 0.3s ease;
}

.expand-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

/* Расширенные ставки */
.expanded-odds {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.odds-categories {
  display: grid;
  gap: 20px;
}

.odds-category h4 {
  font-size: 1rem;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 10px;
}

.odd-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

/* Корзина ставок */
.bet-slip-panel {
  position: fixed;
  right: 20px;
  top: 100px;
  width: 350px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 15px;
  padding: 20px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
}

.bet-slip-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.bet-slip-header h3 {
  margin: 0;
  font-size: 1.2rem;
}

.close-btn {
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.6);
  cursor: pointer;
  font-size: 1.2rem;
}

.bet-slip-items {
  max-height: 300px;
  overflow-y: auto;
  margin-bottom: 20px;
}

.bet-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  margin-bottom: 10px;
}

.bet-info {
  flex: 1;
}

.bet-event {
  display: block;
  font-size: 0.9rem;
  font-weight: 600;
  margin-bottom: 5px;
}

.bet-type {
  display: block;
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.7);
}

.bet-odds {
  font-weight: 700;
  color: #ffd700;
  margin: 0 10px;
}

.remove-bet {
  background: rgba(255, 71, 87, 0.2);
  border: none;
  color: #ff4757;
  padding: 5px;
  border-radius: 5px;
  cursor: pointer;
}

.bet-slip-footer {
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding-top: 15px;
}

.total-odds {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
  font-weight: 600;
}

.total-value {
  color: #ffd700;
}

.place-bets-btn {
  width: 100%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 15px;
  border-radius: 10px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
}

.place-bets-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
}

/* Loading и Empty states */
.loading-state, .empty-state {
  text-align: center;
  padding: 60px 20px;
  color: rgba(255, 255, 255, 0.6);
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(255, 255, 255, 0.1);
  border-top: 3px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

.empty-state i {
  font-size: 3rem;
  margin-bottom: 20px;
  opacity: 0.5;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Responsive */
@media (max-width: 768px) {
  .interface-header {
    flex-direction: column;
    gap: 15px;
  }

  .filters-panel {
    padding: 15px;
    flex-direction: column;
  }

  .event-main {
    flex-direction: column;
    gap: 15px;
  }

  .odds-group {
    flex-wrap: wrap;
    justify-content: center;
  }

  .bet-slip-panel {
    position: fixed;
    bottom: 0;
    right: 0;
    left: 0;
    top: auto;
    width: 100%;
    border-radius: 15px 15px 0 0;
  }
}
</style>
