<template>
  <div class="quick-actions">
    <div class="actions-grid">
      <!-- Быстрый доступ к AI прогнозам -->
      <div class="action-card ai-predictions" @click="$router.push('/predictions')">
        <div class="action-icon">
          <span>🤖</span>
        </div>
        <div class="action-content">
          <h4 class="action-title">AI Прогнозы</h4>
          <p class="action-description">Умные рекомендации на основе анализа данных</p>
          <div class="action-stats">
            <span class="accuracy-badge">76% точность</span>
          </div>
        </div>
        <div class="action-arrow">
          <span>→</span>
        </div>
      </div>

      <!-- Быстрый доступ к достижениям -->
      <div class="action-card achievements" @click="$router.push('/achievements')">
        <div class="action-icon">
          <span>🏆</span>
        </div>
        <div class="action-content">
          <h4 class="action-title">Достижения</h4>
          <p class="action-description">Выполняйте квесты и получайте награды</p>
          <div class="action-stats">
            <span class="progress-badge">{{ userLevel }} уровень</span>
          </div>
        </div>
        <div class="action-arrow">
          <span>→</span>
        </div>
      </div>

      <!-- Быстрый доступ к live ставкам -->
      <div class="action-card live-bets" @click="$router.push('/sports')">
        <div class="action-icon">
          <span>🔥</span>
        </div>
        <div class="action-content">
          <h4 class="action-title">Live ставки</h4>
          <p class="action-description">Ставки на происходящие матчи</p>
          <div class="action-stats">
            <span class="live-badge">{{ liveEventsCount }} live</span>
          </div>
        </div>
        <div class="action-arrow">
          <span>→</span>
        </div>
      </div>

      <!-- Быстрый доступ к аналитике -->
              <div class="action-card analytics" @click="$router.push('/analytics')">
          <div class="action-icon">
            <span>📊</span>
          </div>
          <div class="action-content">
            <h4 class="action-title">Аналитика</h4>
            <p class="action-description">Статистика и инсайты по вашим ставкам</p>
            <div class="action-stats">
              <span class="profit-badge">{{ totalProfit }}₽</span>
            </div>
          </div>
          <div class="action-arrow">
            <span>→</span>
          </div>
        </div>

        <!-- Админ-панель (только для администраторов) -->
        <div v-if="isAdmin()" class="action-card admin" @click="openAdminPanel">
          <div class="action-icon">
            <span>⚙️</span>
          </div>
          <div class="action-content">
            <h4 class="action-title">Админ-панель</h4>
            <p class="action-description">Управление событиями и пользователями</p>
            <div class="action-stats">
              <span class="admin-badge">Админ</span>
            </div>
          </div>
          <div class="action-arrow">
            <span>→</span>
          </div>
        </div>
    </div>
  </div>
</template>

<script>
import { useBetsStore } from '../stores/bets'
import { useUserStore } from '../stores/user'

export default {
  name: 'QuickActions',
  setup() {
    const betsStore = useBetsStore()
    const userStore = useUserStore()

    return {
      betsStore,
      userStore
    }
  },
  data() {
    return {
      userLevel: 12,
      liveEventsCount: 8,
      totalProfit: 1250
    }
  },
  computed: {
    // Вычисляемые свойства для реальных данных
    realLiveEventsCount() {
      return this.betsStore.liveEvents?.length || 0
    },
    realUserLevel() {
      // Здесь можно взять из user store
      return this.userLevel
    },
    realTotalProfit() {
      return this.betsStore.betStats?.total_profit || 0
    }
  },

  methods: {
    openAdminPanel() {
      if (this.isAdmin()) {
        this.$router.push('/admin')
      } else {
        this.$emit('show-notification', {
          type: 'error',
          title: 'Доступ запрещен',
          message: 'У вас нет прав доступа к админ-панели'
        })
      }
    },

    // Проверка прав администратора
    isAdmin() {
      // В реальном приложении проверка будет через API
      // Для демонстрации используем localStorage
      return localStorage.getItem('admin_auth') === 'true'
    }
  }
}
</script>

<style scoped>
.quick-actions {
  margin: 30px 0;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
}

.action-card {
  background: linear-gradient(145deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%);
  border-radius: 20px;
  padding: 25px;
  backdrop-filter: blur(15px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  gap: 20px;
}

.action-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
  transition: left 0.5s;
}

.action-card:hover::before {
  left: 100%;
}

.action-card:hover {
  transform: translateY(-5px) scale(1.02);
  box-shadow:
    0 20px 40px rgba(0, 0, 0, 0.15),
    0 8px 16px rgba(0, 0, 0, 0.1);
}

.action-card.ai-predictions::before {
  background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.2), transparent);
}

.action-card.achievements::before {
  background: linear-gradient(90deg, transparent, rgba(255, 193, 7, 0.2), transparent);
}

.action-card.live-bets::before {
  background: linear-gradient(90deg, transparent, rgba(255, 107, 107, 0.2), transparent);
}

.action-card.analytics::before {
  background: linear-gradient(90deg, transparent, rgba(40, 167, 69, 0.2), transparent);
}

.action-card.ai-predictions:hover {
  border-color: rgba(102, 126, 234, 0.5);
  box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
}

.action-card.achievements:hover {
  border-color: rgba(255, 193, 7, 0.5);
  box-shadow: 0 20px 40px rgba(255, 193, 7, 0.3);
}

.action-card.live-bets:hover {
  border-color: rgba(255, 107, 107, 0.5);
  box-shadow: 0 20px 40px rgba(255, 107, 107, 0.3);
}

.action-card.analytics:hover {
  border-color: rgba(40, 167, 69, 0.5);
  box-shadow: 0 20px 40px rgba(40, 167, 69, 0.3);
}

.action-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.2) 0%, rgba(255, 255, 255, 0.1) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  backdrop-filter: blur(10px);
  border: 2px solid rgba(255, 255, 255, 0.3);
  flex-shrink: 0;
}

.action-content {
  flex: 1;
  min-width: 0;
}

.action-title {
  font-size: 1.2rem;
  font-weight: 700;
  color: #fff;
  margin: 0 0 8px 0;
}

.action-description {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.8);
  margin: 0 0 12px 0;
  line-height: 1.4;
}

.action-stats {
  display: flex;
  align-items: center;
}

.accuracy-badge,
.progress-badge,
.live-badge,
.profit-badge {
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.accuracy-badge {
  background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
  color: white;
}

.progress-badge {
  background: linear-gradient(135deg, #ffc107 0%, #fd7e14 100%);
  color: white;
}

.live-badge {
  background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
  color: white;
  animation: pulse 2s infinite;
}

.profit-badge {
  background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
  color: white;
}

.action-arrow {
  font-size: 1.5rem;
  color: rgba(255, 255, 255, 0.6);
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.action-card:hover .action-arrow {
  color: #fff;
  transform: translateX(5px);
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}

/* Адаптивность */
@media (max-width: 768px) {
  .actions-grid {
    grid-template-columns: 1fr;
    gap: 15px;
  }

  .action-card {
    padding: 20px;
    gap: 15px;
  }

  .action-icon {
    width: 50px;
    height: 50px;
    font-size: 1.3rem;
  }

  .action-title {
    font-size: 1.1rem;
  }

  .action-description {
    font-size: 0.85rem;
  }
}

@media (max-width: 480px) {
  .quick-actions {
    margin: 20px 0;
  }

  .action-card {
    padding: 15px;
    gap: 12px;
  }

  .action-icon {
    width: 45px;
    height: 45px;
    font-size: 1.1rem;
  }

  .action-title {
    font-size: 1rem;
  }
}
</style>
