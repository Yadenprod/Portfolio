<template>
  <div class="sports-page">
    <!-- Admin Access (hidden but accessible) -->
    <div
      class="admin-access"
      @click="goToAdmin"
      title="Админ панель"
    >
      ⚙️
    </div>

    <!-- Hero Section -->
    <div class="hero-section">
      <div class="hero-content">
        <div class="hero-text">
          <h1 class="hero-title">
            <span class="gradient-text">Спортивные ставки</span>
          </h1>
          <p class="hero-subtitle">Делайте ставки на любимые виды спорта с лучшими коэффициентами</p>
        </div>
        <div class="hero-stats">
          <div class="stat-card">
            <div class="stat-number">{{ filteredEvents.length }}</div>
            <div class="stat-label">Активных событий</div>
          </div>
          <div class="stat-card">
            <div class="stat-number">{{ betsStore.liveEvents.length }}</div>
            <div class="stat-label">Live матчей</div>
          </div>
          <div class="stat-card">
            <div class="stat-number">{{ betsStore.availableSports.length }}</div>
            <div class="stat-label">Видов спорта</div>
          </div>
        </div>
      </div>
      <div class="hero-balance">
        <div class="balance-card">
          <div class="balance-label">Ваш баланс</div>
          <div class="balance-amount">{{ userStore.formattedBalance }}</div>
          <button class="deposit-btn">
            <span>💳 Пополнить</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="quick-actions">
      <button
        @click="setQuickFilter('live')"
        :class="['quick-action-btn', { 'active': statusFilter === 'live' }]"
      >
        <div class="action-icon">🔴</div>
        <div class="action-text">Live</div>
      </button>
      <button
        @click="setQuickFilter('football')"
        :class="['quick-action-btn', { 'active': betsStore.selectedSport === 'football' }]"
      >
        <div class="action-icon">⚽</div>
        <div class="action-text">Футбол</div>
      </button>
      <button
        @click="setQuickFilter('csgo')"
        :class="['quick-action-btn', { 'active': betsStore.selectedSport === 'csgo' }]"
      >
        <div class="action-icon">🎮</div>
        <div class="action-text">CS:GO</div>
      </button>
      <button
        @click="setQuickFilter('today')"
        :class="['quick-action-btn', { 'active': betsStore.selectedTimeframe === '24' }]"
      >
        <div class="action-icon">📅</div>
        <div class="action-text">Сегодня</div>
      </button>
    </div>

    <!-- Advanced Filters -->
    <div class="filters-section">
      <div class="filters-header">
        <h3 class="filters-title">Фильтры</h3>
        <button @click="resetFilters" class="reset-filters-btn">
          <span>🔄 Сбросить</span>
        </button>
      </div>

      <div class="filters-grid">
        <!-- Category Filter -->
        <div class="filter-card">
          <div class="filter-label">
            <span class="filter-icon">🎯</span>
            Категория
          </div>
          <div class="filter-options">
            <button
              v-for="category in betsStore.availableCategories"
              :key="category.value"
              @click="betsStore.selectedCategory = category.value; onCategoryFilterChange()"
              :class="['filter-option', { 'active': betsStore.selectedCategory === category.value }]"
            >
              {{ category.label }}
            </button>
          </div>
        </div>

        <!-- Sport Filter -->
        <div class="filter-card">
          <div class="filter-label">
            <span class="filter-icon">🏆</span>
            Вид спорта
          </div>
          <div class="filter-options">
            <button
              @click="betsStore.selectedSport = 'all'; onSportFilterChange()"
              :class="['filter-option', { 'active': betsStore.selectedSport === 'all' }]"
            >
              <span class="sport-icon">⚽</span>
              Все виды
            </button>
            <button
              v-for="sport in filteredSports.slice(0, 6)"
              :key="sport.value"
              @click="betsStore.selectedSport = sport.value; onSportFilterChange()"
              :class="['filter-option', { 'active': betsStore.selectedSport === sport.value }]"
            >
              <span class="sport-icon">{{ getSportIcon(sport.label) }}</span>
              {{ sport.label }}
            </button>
          </div>
        </div>

        <!-- Time Filter -->
        <div class="filter-card">
          <div class="filter-label">
            <span class="filter-icon">⏰</span>
            Время начала
          </div>
          <div class="filter-options">
            <button
              v-for="timeframe in timeframeOptions"
              :key="timeframe.value"
              @click="betsStore.selectedTimeframe = timeframe.value; onTimeframeFilterChange()"
              :class="['filter-option', { 'active': betsStore.selectedTimeframe === timeframe.value }]"
            >
              {{ timeframe.icon }} {{ timeframe.label }}
            </button>
          </div>
        </div>

        <!-- Status Filter -->
        <div class="filter-card">
          <div class="filter-label">
            <span class="filter-icon">🔥</span>
            Статус
          </div>
          <div class="filter-options">
            <button
              v-for="status in statusOptions"
              :key="status.value"
              @click="statusFilter = status.value; onStatusFilterChange()"
              :class="['filter-option', status.class, { 'active': statusFilter === status.value }]"
            >
              {{ status.icon }} {{ status.label }}
            </button>
          </div>
        </div>
      </div>

      <!-- Filter Actions -->
      <div class="filter-actions">
        <button
          @click="refreshEvents"
          :disabled="betsStore.loading"
          class="action-btn primary"
        >
          <span v-if="betsStore.loading" class="loading-spinner"></span>
          <span v-else>🔄</span>
          {{ betsStore.loading ? 'Загрузка...' : 'Обновить' }}
        </button>
        <div class="events-counter">
          <span class="counter-number">{{ filteredEvents.length }}</span>
          <span class="counter-label">событий найдено</span>
        </div>
      </div>
    </div>

    <!-- Live Events Section -->
    <div v-if="betsStore.liveEvents.length > 0" class="events-section">
      <div class="section-header">
        <div class="section-title">
          <div class="live-pulse"></div>
          <span>Live события</span>
          <span class="section-count">{{ betsStore.liveEvents.length }}</span>
        </div>
        <div class="section-subtitle">Матчи в прямом эфире</div>
      </div>

      <div class="events-container">
        <div class="events-scroll">
          <div
            v-for="event in betsStore.liveEvents"
            :key="event.id"
            class="event-card live-event"
          >
            <SportsEventCard
              :event="event"
              :is-live="true"
              @bet-added="onBetAdded"
            />
          </div>
        </div>
      </div>
    </div>

    <!-- Upcoming Events Section -->
    <div class="events-section">
      <div class="section-header">
        <div class="section-title">
          <span>Предстоящие события</span>
          <span class="section-count">{{ filteredEvents.length }}</span>
        </div>
        <div class="section-subtitle">Ближайшие матчи и турниры</div>
      </div>

      <!-- Loading State -->
      <div v-if="betsStore.loading" class="loading-container">
        <div class="loading-animation">
          <div class="loading-spinner-large"></div>
          <div class="loading-text">Загружаем события...</div>
          <div class="loading-subtext">Подбираем лучшие коэффициенты</div>
        </div>
      </div>

      <!-- Error State -->
      <div v-else-if="betsStore.error" class="error-container">
        <div class="error-icon">⚠️</div>
        <div class="error-title">Ошибка загрузки</div>
        <div class="error-message">{{ betsStore.error }}</div>
        <button @click="refreshEvents" class="error-retry-btn">
          <span>🔄 Попробовать снова</span>
        </button>
      </div>

      <!-- Empty State -->
      <div v-else-if="filteredEvents.length === 0" class="empty-container">
        <div class="empty-icon">🔍</div>
        <div class="empty-title">События не найдены</div>
        <div class="empty-message">Попробуйте изменить параметры фильтрации</div>
        <button @click="resetFilters" class="empty-reset-btn">
          <span>🔄 Сбросить фильтры</span>
        </button>
      </div>

      <!-- Events Grid -->
      <div v-else class="events-container">
        <div class="events-grid">
          <div
            v-for="event in filteredEvents"
            :key="event.id"
            class="event-card"
          >
            <SportsEventCard
              :event="event"
              :is-live="false"
              @bet-added="onBetAdded"
            />
          </div>
        </div>

        <!-- Load More Button -->
        <div v-if="filteredEvents.length >= 20" class="load-more-container">
          <button @click="loadMoreEvents" class="load-more-btn">
            <span>📥 Загрузить еще</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Корзина ставок -->
    <BetSlip
      v-if="betsStore.hasBetsInSlip"
      @bet-placed="onBetPlaced"
      @slip-cleared="onSlipCleared"
    />
  </div>
</template>

<script>
import { useUserStore } from '../stores/user'
import { useBetsStore } from '../stores/bets'
import SportsEventCard from '../components/sports/SportsEventCard.vue'
import BetSlip from '../components/sports/BetSlip.vue'

export default {
  name: 'Sports',
  components: {
    SportsEventCard,
    BetSlip
  },
  setup() {
    const userStore = useUserStore()
    const betsStore = useBetsStore()

    return {
      userStore,
      betsStore
    }
  },
  async mounted() {
    await this.loadData()
  },
  data() {
    return {
      statusFilter: 'all',
      timeframeOptions: [
        { value: 'all', label: 'Все матчи', icon: '📅' },
        { value: '1', label: '1 час', icon: '⏱️' },
        { value: '2', label: '2 часа', icon: '🕐' },
        { value: '6', label: '6 часов', icon: '🕕' },
        { value: '24', label: '24 часа', icon: '🌅' }
      ],
      statusOptions: [
        { value: 'all', label: 'Все', icon: '📊', class: 'all' },
        { value: 'upcoming', label: 'Предстоящие', icon: '⏳', class: 'upcoming' },
        { value: 'live', label: 'Live', icon: '🔴', class: 'live' }
      ]
    }
  },

  computed: {
    filteredSports() {
      if (this.betsStore.selectedCategory === 'all') {
        return this.betsStore.availableSports
      }
      return this.betsStore.availableSports.filter(sport =>
        sport.category === this.betsStore.selectedCategory
      )
    },

    filteredEvents() {
      let events = this.betsStore.filteredEvents

      if (this.statusFilter !== 'all') {
        if (this.statusFilter === 'live') {
          events = events.filter(event => event.is_live)
        } else if (this.statusFilter === 'upcoming') {
          events = events.filter(event => !event.is_live)
        }
      }

      return events
    }
  },

  methods: {
    async loadData() {
      await Promise.all([
        this.betsStore.loadEvents(),
        this.betsStore.loadUserBets()
      ])
    },

    async refreshEvents() {
      await this.betsStore.loadEvents()
    },

    onCategoryFilterChange() {
      // Фильтр обновится автоматически через getter
    },

    onSportFilterChange() {
      // Фильтр обновится автоматически через getter
    },

    goToAdmin() {
      // Проверяем, что пользователь администратор
      const isAdmin = localStorage.getItem('admin_logged_in')
      if (isAdmin) {
        this.$router.push('/admin')
      } else {
        // Если не админ, показываем форму входа
        if (confirm('Войти в админ панель?')) {
          const password = prompt('Введите пароль администратора:')
          if (password === 'admin123') {
            localStorage.setItem('admin_logged_in', 'true')
            this.$router.push('/admin')
          } else {
            alert('Неверный пароль!')
          }
        }
      }
    },

    onTimeframeFilterChange() {
      // Фильтр обновится автоматически через getter
    },

    onStatusFilterChange() {
      // Фильтр обновится автоматически через getter
    },

    onTimeframeFilterChange() {
      // Фильтр обновится автоматически через getter
    },

    // Quick Filter Methods
    setQuickFilter(type) {
      this.resetFilters()

      switch(type) {
        case 'live':
          this.statusFilter = 'live'
          this.onStatusFilterChange()
          break
        case 'football':
          this.betsStore.selectedSport = 'football'
          this.onSportFilterChange()
          break
        case 'csgo':
          this.betsStore.selectedSport = 'csgo'
          this.onSportFilterChange()
          break
        case 'today':
          this.betsStore.selectedTimeframe = '24'
          this.onTimeframeFilterChange()
          break
      }
    },

    // Reset all filters
    resetFilters() {
      this.betsStore.selectedCategory = 'all'
      this.betsStore.selectedSport = 'all'
      this.betsStore.selectedTimeframe = 'all'
      this.statusFilter = 'all'

      // Trigger filter updates
      this.onCategoryFilterChange()
      this.onSportFilterChange()
      this.onTimeframeFilterChange()
      this.onStatusFilterChange()
    },

    // Load more events (placeholder for pagination)
    loadMoreEvents() {
      // This would implement pagination in a real app
      console.log('Loading more events...')
    },

    getSportIcon(sportName) {
      const icons = {
        'Футбол': '⚽',
        'Баскетбол': '🏀',
        'Теннис': '🎾',
        'Волейбол': '🏐',
        'Хоккей': '🏒',
        'Бейсбол': '⚾',
        'Американский футбол': '🏈',
        'Регби': '🏉',
        'CS:GO': '🎮',
        'Dota 2': '🎯',
        'League of Legends': '🛡️',
        'Valorant': '🔫',
        'Apex Legends': '🦅',
        'Rainbow Six Siege': '🛡️'
      }
      return icons[sportName] || '🏆'
    },

    onBetAdded(bet) {
      // Ставка добавлена в корзину
      console.log('Bet added to slip:', bet)
    },

    onBetPlaced(results) {
      // Ставки сделаны
      console.log('Bets placed:', results)
      this.loadData() // Обновить данные
    },

    onSlipCleared() {
      // Корзина очищена
      console.log('Bet slip cleared')
    }
  }
}
</script>

<style scoped>
.sports-page {
  min-height: 100vh;
  background:
    radial-gradient(ellipse at top, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
    radial-gradient(ellipse at bottom, rgba(255, 119, 198, 0.3) 0%, transparent 50%),
    linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
  padding: 0;
  color: white;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  position: relative;
}

/* Admin Access */
.admin-access {
  position: fixed;
  top: 20px;
  right: 20px;
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  z-index: 1000;
  font-size: 1.2rem;
}

.admin-access:hover {
  background: rgba(102, 126, 234, 0.3);
  border-color: rgba(102, 126, 234, 0.5);
  transform: scale(1.1);
}

/* Hero Section */
.hero-section {
  background:
    linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%),
    radial-gradient(ellipse at 20% 30%, rgba(102, 126, 234, 0.8) 0%, transparent 60%),
    radial-gradient(ellipse at 80% 70%, rgba(255, 119, 198, 0.7) 0%, transparent 60%),
    radial-gradient(ellipse at 60% 10%, rgba(120, 119, 198, 0.6) 0%, transparent 50%),
    radial-gradient(circle at 40% 50%, rgba(255, 215, 0, 0.3) 0%, transparent 40%);
  padding: 60px 30px;
  margin-bottom: 40px;
  border-radius: 0 0 40px 40px;
  backdrop-filter: blur(30px);
  border-bottom: 3px solid rgba(255, 255, 255, 0.2);
  position: relative;
  overflow: hidden;
  box-shadow:
    0 25px 80px rgba(0, 0, 0, 0.2),
    0 0 0 1px rgba(255, 255, 255, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.hero-section::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background:
    linear-gradient(45deg, transparent 30%, rgba(102, 126, 234, 0.1) 50%, transparent 70%),
    linear-gradient(-45deg, transparent 30%, rgba(255, 119, 198, 0.1) 50%, transparent 70%);
  animation: heroRotate 25s linear infinite;
  opacity: 0.6;
  pointer-events: none;
}

@keyframes heroRotate {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}



.hero-content {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 40px;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

.hero-text {
  animation: fadeInUp 0.8s ease-out;
}

.hero-title {
  font-size: 3.2rem;
  font-weight: 900;
  margin: 0 0 18px 0;
  line-height: 1.05;
  letter-spacing: -0.02em;
  text-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  animation: float 6s ease-in-out infinite;
}

.gradient-text {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 30%, #f093fb 60%, #ff6b6b 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  display: block;
  animation: gradientShift 8s ease-in-out infinite;
}

@keyframes gradientShift {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

.hero-subtitle {
  font-size: 1.1rem;
  color: rgba(255, 255, 255, 0.8);
  margin: 0;
  font-weight: 400;
}

.hero-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.stat-card {
  background: rgba(255, 255, 255, 0.1);
  padding: 20px;
  border-radius: 15px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  text-align: center;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  background: rgba(255, 255, 255, 0.15);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.stat-number {
  font-size: 2rem;
  font-weight: 800;
  color: #667eea;
  margin-bottom: 5px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.stat-label {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.7);
  font-weight: 500;
}

.hero-balance {
  animation: fadeInUp 0.8s ease-out 0.2s both;
}

.balance-card {
  background: linear-gradient(135deg, rgba(255, 215, 0, 0.2) 0%, rgba(255, 215, 0, 0.1) 100%);
  padding: 25px;
  border-radius: 20px;
  backdrop-filter: blur(15px);
  border: 1px solid rgba(255, 215, 0, 0.3);
  text-align: center;
  min-width: 200px;
  box-shadow: 0 10px 30px rgba(255, 215, 0, 0.2);
}

.balance-label {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 10px;
  font-weight: 500;
}

.balance-amount {
  font-size: 1.8rem;
  font-weight: 800;
  color: #ffd700;
  margin-bottom: 15px;
  text-shadow: 0 2px 10px rgba(255, 215, 0, 0.3);
}

.deposit-btn {
  background: linear-gradient(135deg, #ffd700 0%, #ffb347 100%);
  color: #000;
  border: none;
  padding: 12px 20px;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
}

.deposit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 215, 0, 0.4);
}

/* Quick Actions */
.quick-actions {
  padding: 0 25px;
  margin-bottom: 35px;
}

.quick-actions {
  display: flex;
  gap: 18px;
  overflow-x: auto;
  padding-bottom: 15px;
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.quick-actions::-webkit-scrollbar {
  display: none;
}

.quick-action-btn {
  background:
    linear-gradient(145deg, rgba(255, 255, 255, 0.15) 0%, rgba(255, 255, 255, 0.08) 100%),
    radial-gradient(circle at 30% 20%, rgba(102, 126, 234, 0.2) 0%, transparent 50%);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 24px;
  padding: 20px 22px;
  min-width: 115px;
  cursor: pointer;
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  backdrop-filter: blur(20px);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  flex-shrink: 0;
  position: relative;
  overflow: hidden;
  box-shadow:
    0 8px 25px rgba(0, 0, 0, 0.15),
    0 0 0 1px rgba(255, 255, 255, 0.1);
}

.quick-action-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background:
    linear-gradient(90deg,
      transparent 0%,
      rgba(255, 255, 255, 0.25) 50%,
      transparent 100%);
  transition: left 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}

.quick-action-btn::after {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background:
    radial-gradient(circle at 30% 30%, rgba(102, 126, 234, 0.3) 0%, transparent 50%),
    radial-gradient(circle at 70% 70%, rgba(255, 119, 198, 0.3) 0%, transparent 50%);
  opacity: 0;
  transition: opacity 0.4s ease;
  pointer-events: none;
}

.quick-action-btn:hover::before {
  left: 100%;
}

.quick-action-btn:hover::after {
  opacity: 1;
}

.quick-action-btn:hover {
  background:
    linear-gradient(145deg, rgba(255, 255, 255, 0.22) 0%, rgba(255, 255, 255, 0.12) 100%),
    radial-gradient(circle at 30% 20%, rgba(102, 126, 234, 0.4) 0%, transparent 60%);
  transform: translateY(-6px) scale(1.03);
  box-shadow:
    0 20px 45px rgba(0, 0, 0, 0.3),
    0 8px 25px rgba(102, 126, 234, 0.2),
    0 0 0 1px rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.4);
}

.quick-action-btn.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
  border-color: rgba(102, 126, 234, 0.6);
  box-shadow:
    0 15px 35px rgba(102, 126, 234, 0.4),
    0 0 0 1px rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
  animation: glowPulse 3s ease-in-out infinite;
}

.quick-action-btn.active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 30px;
  height: 3px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 2px;
}

.action-icon {
  font-size: 1.8rem;
  transition: transform 0.3s ease;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
}

.quick-action-btn:hover .action-icon {
  transform: scale(1.1);
}

.action-text {
  font-size: 0.9rem;
  font-weight: 700;
  text-align: center;
  letter-spacing: 0.02em;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

/* Filters Section */
.filters-section {
  background:
    linear-gradient(145deg, rgba(255, 255, 255, 0.08) 0%, rgba(255, 255, 255, 0.04) 100%),
    radial-gradient(circle at 30% 20%, rgba(102, 126, 234, 0.1) 0%, transparent 50%);
  backdrop-filter: blur(25px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 25px;
  padding: 35px;
  margin: 0 25px 35px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.25);
  position: relative;
  overflow: hidden;
}

.filters-section::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: conic-gradient(from 0deg, transparent, rgba(102, 126, 234, 0.1), transparent, rgba(255, 119, 198, 0.1), transparent);
  animation: rotate 20s linear infinite;
  opacity: 0.5;
  pointer-events: none;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.filters-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
}

.filters-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0;
}

.reset-filters-btn {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  padding: 8px 16px;
  border-radius: 10px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.reset-filters-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-1px);
}

.filters-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
  margin-bottom: 25px;
}

.filter-card {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 18px;
  padding: 25px;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.filter-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(255, 119, 198, 0.1) 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.filter-card:hover::before {
  opacity: 1;
}

.filter-card:hover {
  background: rgba(255, 255, 255, 0.15);
  transform: translateY(-3px) scale(1.01);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.25);
  border-color: rgba(255, 255, 255, 0.3);
}

.filter-label {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 15px;
  color: rgba(255, 255, 255, 0.9);
}

.filter-icon {
  font-size: 1.2rem;
}

.filter-options {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 10px;
}

.filter-option {
  background: rgba(255, 255, 255, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.25);
  color: white;
  padding: 12px 18px;
  border-radius: 12px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(10px);
}

.filter-option::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.15), transparent);
  transition: left 0.5s ease;
}

.filter-option:hover::before {
  left: 100%;
}

.filter-option:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px) scale(1.02);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.25);
  border-color: rgba(255, 255, 255, 0.4);
}

.filter-option.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
  border-color: rgba(102, 126, 234, 0.7);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
  transform: translateY(-1px);
  color: white;
}

.filter-option.active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 20px;
  height: 2px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 1px;
}

.filter-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.action-btn {
  background:
    linear-gradient(135deg, #667eea 0%, #764ba2 30%, #f093fb 70%, #ff6b6b 100%),
    linear-gradient(145deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%);
  color: white;
  border: none;
  padding: 16px 32px;
  border-radius: 18px;
  font-weight: 800;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  align-items: center;
  gap: 12px;
  box-shadow:
    0 8px 25px rgba(102, 126, 234, 0.4),
    0 0 0 1px rgba(255, 255, 255, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
  position: relative;
  overflow: hidden;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.action-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background:
    linear-gradient(90deg,
      transparent 0%,
      rgba(255, 255, 255, 0.3) 50%,
      transparent 100%);
  transition: left 0.7s cubic-bezier(0.4, 0, 0.2, 1);
}

.action-btn::after {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background:
    radial-gradient(circle at 30% 30%, rgba(255, 255, 255, 0.2) 0%, transparent 50%),
    radial-gradient(circle at 70% 70%, rgba(255, 215, 0, 0.3) 0%, transparent 50%);
  opacity: 0;
  transition: opacity 0.4s ease;
  pointer-events: none;
}

.action-btn:hover::before {
  left: 100%;
}

.action-btn:hover::after {
  opacity: 1;
}

.action-btn:hover {
  transform: translateY(-4px) scale(1.03);
  box-shadow:
    0 15px 40px rgba(102, 126, 234, 0.6),
    0 8px 25px rgba(255, 119, 198, 0.4),
    0 0 0 1px rgba(255, 255, 255, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
}

.action-btn:active {
  transform: translateY(-2px) scale(0.98);
  transition-duration: 0.1s;
}

.action-btn.primary {
  background:
    linear-gradient(135deg, #ffd700 0%, #ffb347 30%, #ff8c42 70%, #ff4757 100%),
    linear-gradient(145deg, rgba(255, 255, 255, 0.2) 0%, rgba(255, 255, 255, 0.1) 100%);
  color: #000;
  box-shadow:
    0 8px 25px rgba(255, 215, 0, 0.5),
    0 0 0 1px rgba(255, 215, 0, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.action-btn.primary:hover {
  background:
    linear-gradient(135deg, #ffe135 0%, #ffc107 30%, #ff9800 70%, #ff5722 100%),
    linear-gradient(145deg, rgba(255, 255, 255, 0.3) 0%, rgba(255, 255, 255, 0.15) 100%);
  box-shadow:
    0 15px 40px rgba(255, 215, 0, 0.7),
    0 8px 25px rgba(255, 136, 0, 0.5),
    0 0 0 1px rgba(255, 215, 0, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.4);
}

.loading-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.events-counter {
  text-align: center;
}

.counter-number {
  font-size: 1.5rem;
  font-weight: 800;
  color: #667eea;
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.counter-label {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.7);
  margin-top: 2px;
}

/* Events Section */
.events-section {
  margin-bottom: 40px;
}

.section-header {
  padding: 0 20px;
  margin-bottom: 25px;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 1.8rem;
  font-weight: 700;
  margin: 0 0 8px 0;
}

.section-count {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 600;
}

.live-pulse {
  width: 12px;
  height: 12px;
  background: #ff4757;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

.section-subtitle {
  color: rgba(255, 255, 255, 0.7);
  font-size: 1rem;
  margin: 0;
  font-weight: 400;
}

.events-container {
  padding: 0 20px;
}

.events-scroll {
  display: flex;
  gap: 20px;
  overflow-x: auto;
  padding-bottom: 10px;
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.events-scroll::-webkit-scrollbar {
  display: none;
}

.events-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 25px;
}

/* Loading States */
.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 60px 20px;
}

.loading-animation {
  text-align: center;
}

.loading-spinner-large {
  width: 60px;
  height: 60px;
  border: 4px solid rgba(255, 255, 255, 0.1);
  border-top: 4px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

.loading-text {
  font-size: 1.2rem;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 10px;
}

.loading-subtext {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.6);
}

/* Error States */
.error-container {
  text-align: center;
  padding: 60px 20px;
}

.error-icon {
  font-size: 4rem;
  margin-bottom: 20px;
  opacity: 0.7;
}

.error-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 10px;
}

.error-message {
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 25px;
  max-width: 400px;
  margin-left: auto;
  margin-right: auto;
}

.error-retry-btn {
  background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
}

.error-retry-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 107, 107, 0.4);
}

/* Empty States */
.empty-container {
  text-align: center;
  padding: 60px 20px;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 20px;
  opacity: 0.7;
}

.empty-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 10px;
}

.empty-message {
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 25px;
  max-width: 400px;
  margin-left: auto;
  margin-right: auto;
}

.empty-reset-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.empty-reset-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

/* Load More */
.load-more-container {
  text-align: center;
  margin-top: 30px;
}

.load-more-btn {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  padding: 15px 30px;
  border-radius: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.load-more-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
}

/* Animations */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes pulse {
  0% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.2);
    opacity: 0.7;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes gradientShift {
  0%, 100% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
  }
  33% {
    transform: translateY(-10px) rotate(1deg);
  }
  66% {
    transform: translateY(-5px) rotate(-1deg);
  }
}

@keyframes glowPulse {
  0%, 100% {
    box-shadow:
      0 0 20px rgba(102, 126, 234, 0.3),
      0 0 40px rgba(102, 126, 234, 0.1);
  }
  50% {
    box-shadow:
      0 0 30px rgba(102, 126, 234, 0.6),
      0 0 60px rgba(102, 126, 234, 0.2);
  }
}

@keyframes shimmer {
  0% {
    background-position: -200px 0;
  }
  100% {
    background-position: calc(200px + 100%) 0;
  }
}

@keyframes glow {
  0%, 100% {
    box-shadow: 0 0 20px rgba(102, 126, 234, 0.3);
  }
  50% {
    box-shadow: 0 0 30px rgba(102, 126, 234, 0.6);
  }
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-10px);
  }
  60% {
    transform: translateY(-5px);
  }
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes slideInLeft {
  from {
    opacity: 0;
    transform: translateX(-30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* Responsive Design */
@media (max-width: 768px) {
  .sports-page {
    padding: 0;
  }

  .hero-section {
    padding: 30px 15px;
    margin-bottom: 20px;
  }

  .hero-content {
    grid-template-columns: 1fr;
    gap: 30px;
    text-align: center;
  }

  .hero-title {
    font-size: 2.2rem;
  }

  .hero-stats {
    grid-template-columns: repeat(3, 1fr);
    gap: 15px;
  }

  .hero-balance {
    order: -1;
  }

  .quick-actions {
    padding: 0 15px;
  }

  .quick-action-btn {
    min-width: 80px;
    padding: 12px;
  }

  .filters-section {
    margin: 0 15px 20px;
    padding: 20px;
  }

  .filters-grid {
    grid-template-columns: 1fr;
    gap: 15px;
  }

  .filter-options {
    grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
  }

  .events-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .events-scroll {
    gap: 15px;
  }

  .section-header {
    padding: 0 15px;
  }

  .events-container {
    padding: 0 15px;
  }

  .action-btn {
    padding: 10px 20px;
    font-size: 0.9rem;
  }
}

@media (max-width: 480px) {
  .hero-title {
    font-size: 1.8rem;
  }

  .hero-stats {
    grid-template-columns: repeat(2, 1fr);
  }

  .quick-actions {
    gap: 10px;
  }

  .quick-action-btn {
    min-width: 70px;
    padding: 10px;
    font-size: 0.8rem;
  }

  .filter-options {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
