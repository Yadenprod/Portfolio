<template>
  <div class="notifications-center">
    <!-- Кнопка открытия центра уведомлений -->
    <button
      @click="toggleNotifications"
      class="notification-toggle"
      :class="{ 'has-unread': notificationsStore.hasUnread }"
    >
      <div class="bell-icon">
        <span class="bell">🔔</span>
        <span v-if="notificationsStore.hasUnread" class="unread-dot">
          {{ notificationsStore.unreadCount }}
        </span>
      </div>
    </button>

    <!-- Центр уведомлений -->
    <Transition name="slide-down">
      <div v-if="isOpen" class="notifications-panel" @click.stop>
        <div class="panel-header">
          <h3 class="panel-title">Уведомления</h3>
          <div class="panel-actions">
            <button @click="markAllAsRead" class="mark-read-btn" v-if="notificationsStore.hasUnread">
              <span>✓</span> Прочитать все
            </button>
            <button @click="clearAll" class="clear-btn">
              <span>🗑️</span> Очистить
            </button>
            <button @click="toggleNotifications" class="close-btn">
              <span>✕</span>
            </button>
          </div>
        </div>

        <div class="notifications-list">
          <div v-if="notificationsStore.allNotifications.length === 0" class="empty-state">
            <div class="empty-icon">📭</div>
            <p class="empty-message">У вас нет уведомлений</p>
            <p class="empty-subtitle">Новые уведомления появятся здесь</p>
          </div>

          <div v-else class="notifications-scroll">
            <div
              v-for="notification in notificationsStore.allNotifications"
              :key="notification.id"
              class="notification-item"
              :class="{
                'unread': !notification.read,
                [notification.type]: true
              }"
              @click="handleNotificationClick(notification)"
            >
              <div class="notification-icon">
                <span v-if="notification.type === 'success'">🎉</span>
                <span v-if="notification.type === 'error'">😞</span>
                <span v-if="notification.type === 'info'">💬</span>
                <span v-if="notification.type === 'promotion'">🎁</span>
                <span v-if="notification.type === 'warning'">⚠️</span>
              </div>

              <div class="notification-content">
                <div class="notification-header">
                  <h4 class="notification-title">{{ notification.title }}</h4>
                  <span class="notification-time">{{ formatTime(notification.created_at) }}</span>
                </div>
                <p class="notification-message">{{ notification.message }}</p>

                <!-- Дополнительная информация для ставок -->
                <div v-if="notification.data.bet" class="bet-info">
                  <div class="bet-details">
                    <span class="bet-event">{{ notification.data.bet.event_name }}</span>
                    <span class="bet-amount">{{ notification.data.bet.amount }}₽</span>
                    <span v-if="notification.data.result" class="bet-result" :class="{ 'positive': notification.data.result.profit > 0 }">
                      {{ notification.data.result.profit > 0 ? '+' : '' }}{{ notification.data.result.profit }}₽
                    </span>
                  </div>
                </div>
              </div>

              <div class="notification-actions">
                <button @click.stop="removeNotification(notification.id)" class="remove-btn">
                  <span>×</span>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Настройки уведомлений -->
        <div class="notifications-settings">
          <h4 class="settings-title">Настройки уведомлений</h4>
          <div class="settings-grid">
            <label class="setting-item">
              <input
                type="checkbox"
                v-model="notificationsStore.settings.betResults"
                @change="updateSettings"
              />
              <span class="checkmark"></span>
              <span class="setting-label">Результаты ставок</span>
            </label>

            <label class="setting-item">
              <input
                type="checkbox"
                v-model="notificationsStore.settings.liveEvents"
                @change="updateSettings"
              />
              <span class="checkmark"></span>
              <span class="setting-label">Live события</span>
            </label>

            <label class="setting-item">
              <input
                type="checkbox"
                v-model="notificationsStore.settings.promotions"
                @change="updateSettings"
              />
              <span class="checkmark"></span>
              <span class="setting-label">Акции и бонусы</span>
            </label>

            <label class="setting-item">
              <input
                type="checkbox"
                v-model="notificationsStore.settings.soundEnabled"
                @change="updateSettings"
              />
              <span class="checkmark"></span>
              <span class="setting-label">Звуковые уведомления</span>
            </label>

            <label class="setting-item">
              <input
                type="checkbox"
                v-model="notificationsStore.settings.pushEnabled"
                @change="togglePushNotifications"
              />
              <span class="checkmark"></span>
              <span class="setting-label">Push уведомления</span>
            </label>
          </div>
        </div>
      </div>
    </Transition>

    <!-- Затемнение фона -->
    <Transition name="fade">
      <div v-if="isOpen" class="notifications-overlay" @click="toggleNotifications"></div>
    </Transition>
  </div>
</template>

<script>
import { useNotificationsStore } from '../stores/notifications'

export default {
  name: 'NotificationsCenter',
  setup() {
    const notificationsStore = useNotificationsStore()
    return { notificationsStore }
  },
  data() {
    return {
      isOpen: false
    }
  },
  methods: {
    toggleNotifications() {
      this.isOpen = !this.isOpen
      if (this.isOpen) {
        // Пометить все как прочитанные при открытии
        setTimeout(() => {
          this.notificationsStore.markAllAsRead()
        }, 1000)
      }
    },

    handleNotificationClick(notification) {
      if (!notification.read) {
        this.notificationsStore.markAsRead(notification.id)
      }

      // Обработка клика по уведомлению
      if (notification.data.event) {
        this.$router.push(`/sports`)
      } else if (notification.data.bet) {
        this.$router.push(`/sports/history`)
      }
    },

    removeNotification(id) {
      this.notificationsStore.removeNotification(id)
    },

    markAllAsRead() {
      this.notificationsStore.markAllAsRead()
    },

    clearAll() {
      if (confirm('Вы уверены, что хотите удалить все уведомления?')) {
        this.notificationsStore.clearAllNotifications()
      }
    },

    updateSettings() {
      // Настройки обновляются автоматически через v-model
    },

    async togglePushNotifications() {
      if (this.notificationsStore.settings.pushEnabled) {
        const success = await this.notificationsStore.initPushNotifications()
        if (!success) {
          this.notificationsStore.settings.pushEnabled = false
        }
      }
    },

    formatTime(dateString) {
      const date = new Date(dateString)
      const now = new Date()
      const diff = now - date

      if (diff < 60000) return 'только что'
      if (diff < 3600000) return `${Math.floor(diff / 60000)} мин назад`
      if (diff < 86400000) return `${Math.floor(diff / 3600000)} ч назад`
      if (diff < 604800000) return `${Math.floor(diff / 86400000)} д назад`

      return date.toLocaleDateString('ru-RU')
    }
  }
}
</script>

<style scoped>
.notifications-center {
  position: relative;
  z-index: 1000;
}

.notification-toggle {
  position: relative;
  background: rgba(255, 255, 255, 0.1);
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  width: 48px;
  height: 48px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  backdrop-filter: blur(10px);
  display: flex;
  align-items: center;
  justify-content: center;
}

.notification-toggle:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.4);
  transform: scale(1.1);
}

.notification-toggle.has-unread {
  animation: bellShake 0.5s ease-in-out;
  animation-iteration-count: 3;
}

@keyframes bellShake {
  0%, 100% { transform: rotate(0deg); }
  25% { transform: rotate(5deg); }
  75% { transform: rotate(-5deg); }
}

.bell-icon {
  position: relative;
}

.bell {
  font-size: 1.5rem;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3));
}

.unread-dot {
  position: absolute;
  top: -8px;
  right: -8px;
  background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
  color: white;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  font-size: 0.7rem;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(255, 107, 107, 0.4);
  border: 2px solid rgba(255, 255, 255, 0.8);
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

.notifications-panel {
  position: absolute;
  top: 60px;
  right: 0;
  width: 400px;
  max-width: 90vw;
  max-height: 70vh;
  background: linear-gradient(145deg, rgba(255, 255, 255, 0.98) 0%, rgba(248, 250, 252, 0.95) 100%);
  border-radius: 20px;
  box-shadow:
    0 20px 40px rgba(0, 0, 0, 0.15),
    0 8px 16px rgba(0, 0, 0, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  overflow: hidden;
  z-index: 1001;
}

.panel-header {
  padding: 20px 25px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.panel-title {
  font-size: 1.3rem;
  font-weight: 700;
  margin: 0;
}

.panel-actions {
  display: flex;
  gap: 10px;
}

.mark-read-btn,
.clear-btn,
.close-btn {
  background: rgba(255, 255, 255, 0.2);
  border: 2px solid rgba(255, 255, 255, 0.3);
  color: white;
  border-radius: 15px;
  padding: 8px 12px;
  cursor: pointer;
  font-size: 0.8rem;
  font-weight: 600;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.mark-read-btn:hover,
.clear-btn:hover,
.close-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.5);
  transform: translateY(-1px);
}

.notifications-list {
  max-height: 400px;
}

.notifications-scroll {
  max-height: 350px;
  overflow-y: auto;
}

.notification-item {
  padding: 15px 20px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  display: flex;
  gap: 15px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
}

.notification-item:hover {
  background: rgba(102, 126, 234, 0.05);
  transform: translateX(2px);
}

.notification-item.unread {
  background: linear-gradient(90deg, rgba(102, 126, 234, 0.1) 0%, transparent 100%);
  border-left: 4px solid #667eea;
}

.notification-item.success {
  border-left-color: #28a745;
}

.notification-item.error {
  border-left-color: #dc3545;
}

.notification-item.promotion {
  border-left-color: #ffc107;
}

.notification-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.notification-content {
  flex: 1;
  min-width: 0;
}

.notification-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 5px;
}

.notification-title {
  font-size: 1rem;
  font-weight: 600;
  color: #2c3e50;
  margin: 0;
}

.notification-time {
  font-size: 0.8rem;
  color: #6c757d;
  opacity: 0.8;
}

.notification-message {
  font-size: 0.9rem;
  color: #495057;
  margin: 0;
  line-height: 1.4;
}

.bet-info {
  margin-top: 10px;
  padding: 8px 12px;
  background: rgba(0, 0, 0, 0.05);
  border-radius: 8px;
}

.bet-details {
  display: flex;
  gap: 10px;
  align-items: center;
  flex-wrap: wrap;
}

.bet-event {
  font-size: 0.8rem;
  font-weight: 600;
  color: #495057;
}

.bet-amount {
  font-size: 0.8rem;
  color: #6c757d;
}

.bet-result {
  font-size: 0.9rem;
  font-weight: 700;
}

.bet-result.positive {
  color: #28a745;
}

.notification-actions {
  flex-shrink: 0;
}

.remove-btn {
  background: rgba(220, 53, 69, 0.1);
  color: #dc3545;
  border: 2px solid rgba(220, 53, 69, 0.2);
  border-radius: 50%;
  width: 25px;
  height: 25px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.remove-btn:hover {
  background: rgba(220, 53, 69, 0.2);
  border-color: rgba(220, 53, 69, 0.4);
  transform: scale(1.1);
}

.empty-state {
  padding: 60px 20px;
  text-align: center;
  color: #6c757d;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 15px;
  opacity: 0.5;
}

.empty-message {
  font-size: 1.1rem;
  font-weight: 600;
  margin: 0 0 5px 0;
}

.empty-subtitle {
  font-size: 0.9rem;
  opacity: 0.7;
  margin: 0;
}

.notifications-settings {
  padding: 20px 25px;
  border-top: 1px solid rgba(0, 0, 0, 0.05);
  background: rgba(248, 250, 252, 0.5);
}

.settings-title {
  font-size: 1rem;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 15px 0;
}

.settings-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.setting-item {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 10px;
  transition: all 0.3s ease;
}

.setting-item:hover {
  background: rgba(102, 126, 234, 0.1);
}

.setting-item input[type="checkbox"] {
  display: none;
}

.checkmark {
  width: 20px;
  height: 20px;
  border: 2px solid #e9ecef;
  border-radius: 4px;
  position: relative;
  transition: all 0.3s ease;
}

.setting-item input[type="checkbox"]:checked + .checkmark {
  background: #667eea;
  border-color: #667eea;
}

.setting-item input[type="checkbox"]:checked + .checkmark::after {
  content: '✓';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  font-size: 0.8rem;
  font-weight: bold;
}

.setting-label {
  font-size: 0.9rem;
  font-weight: 500;
  color: #495057;
}

.notifications-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(5px);
  z-index: 1000;
}

/* Анимации */
.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.slide-down-enter-from,
.slide-down-leave-to {
  opacity: 0;
  transform: translateY(-20px) scale(0.95);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Адаптивность */
@media (max-width: 480px) {
  .notifications-panel {
    width: 95vw;
    right: -5vw;
    max-height: 80vh;
  }

  .settings-grid {
    grid-template-columns: 1fr;
  }

  .panel-actions {
    flex-direction: column;
    gap: 5px;
  }

  .mark-read-btn,
  .clear-btn,
  .close-btn {
    padding: 6px 10px;
    font-size: 0.7rem;
  }
}
</style>
