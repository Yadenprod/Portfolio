<template>
  <div class="notifications-container">
    <!-- Кнопка уведомлений -->
    <button
      @click="toggleNotifications"
      class="fixed top-4 right-4 z-40 w-12 h-12 bg-violet hover:bg-violetHover rounded-full shadow-lg flex items-center justify-center transition-all duration-300 hover:scale-110"
      :class="{ 'scale-110': showNotifications }"
    >
      <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/>
      </svg>
    </button>

    <!-- Индикатор новых уведомлений -->
    <div
      v-if="unreadCount > 0 && !showNotifications"
      class="fixed top-2 right-2 z-50 w-6 h-6 bg-red rounded-full flex items-center justify-center text-white text-xs font-bold animate-bounce"
    >
      {{ unreadCount > 9 ? '9+' : unreadCount }}
    </div>

    <!-- Панель уведомлений -->
    <Transition
      enter-active-class="transition-all duration-300 ease-out"
      enter-class="opacity-0 scale-95 translate-x-full"
      enter-to-class="opacity-100 scale-100 translate-x-0"
      leave-active-class="transition-all duration-200 ease-in"
      leave-class="opacity-100 scale-100 translate-x-0"
      leave-to-class="opacity-0 scale-95 translate-x-full"
    >
      <div
        v-if="showNotifications"
        class="fixed top-0 right-0 z-50 w-full max-w-sm h-full bg-gradient-to-br from-[#202024] to-[#2c2c31] shadow-2xl flex flex-col"
      >
        <!-- Заголовок -->
        <div class="flex items-center justify-between p-4 border-b border-violet/20">
          <div class="flex items-center space-x-3">
            <div class="w-8 h-8 bg-violet/20 rounded-full flex items-center justify-center">
              <svg class="w-4 h-4 text-violet" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/>
              </svg>
            </div>
            <div>
              <h3 class="text-white font-semibold text-sm">Уведомления</h3>
              <p class="text-xs text-grayLight">{{ unreadCount }} новых</p>
            </div>
          </div>
          <div class="flex items-center space-x-2">
            <button
              v-if="unreadCount > 0"
              @click="markAllAsRead"
              class="text-xs text-violet hover:text-white transition-colors"
            >
              Прочитать все
            </button>
            <button
              @click="toggleNotifications"
              class="w-6 h-6 text-gray hover:text-white transition-colors"
            >
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>
        </div>

        <!-- Список уведомлений -->
        <div ref="notificationsContainer" class="flex-1 p-4 space-y-3 overflow-y-auto">
          <div
            v-for="notification in notifications"
            :key="notification.id"
            @click="handleNotificationClick(notification)"
            class="bg-[#1b1c20] rounded-xl p-4 cursor-pointer transition-all duration-200 hover:scale-105"
            :class="{
              'ring-2 ring-violet/50': !notification.read,
              'opacity-75': notification.read
            }"
          >
            <div class="flex items-start space-x-3">
              <!-- Иконка -->
              <div
                class="w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0"
                :class="getNotificationColor(notification.type)"
              >
                <span class="text-lg">{{ getNotificationIcon(notification.type) }}</span>
              </div>

              <!-- Содержание -->
              <div class="flex-1 min-w-0">
                <div class="flex items-center justify-between">
                  <h4 class="text-white font-semibold text-sm truncate">{{ notification.title }}</h4>
                  <span
                    v-if="!notification.read"
                    class="w-2 h-2 bg-violet rounded-full flex-shrink-0"
                  ></span>
                </div>
                <p v-if="notification.message" class="text-xs text-grayLight mt-1">{{ notification.message }}</p>
                <p class="text-xs text-gray mt-2">{{ formatTime(notification.timestamp) }}</p>
              </div>

              <!-- Кнопка удаления -->
              <button
                @click.stop="removeNotification(notification.id)"
                class="w-6 h-6 text-gray hover:text-red transition-colors flex-shrink-0"
              >
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                </svg>
              </button>
            </div>
          </div>

          <!-- Загрузка -->
          <div v-if="loading" class="flex justify-center py-4">
            <div class="w-6 h-6 border-2 border-violet border-t-transparent rounded-full animate-spin"></div>
          </div>

          <!-- Пустое состояние -->
          <div v-if="!loading && notifications.length === 0" class="text-center py-8">
            <div class="text-4xl mb-4">🔔</div>
            <p class="text-grayLight text-sm">У вас пока нет уведомлений</p>
          </div>
        </div>

        <!-- Футер -->
        <div class="p-4 border-t border-violet/20">
          <button
            @click="clearAllNotifications"
            class="w-full py-2 text-xs text-red hover:text-white transition-colors"
          >
            Очистить все уведомления
          </button>
        </div>
      </div>
    </Transition>

    <!-- Затемнение фона -->
    <div
      v-if="showNotifications"
      @click="toggleNotifications"
      class="fixed inset-0 z-40 bg-black/50"
    ></div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import notificationService from '../services/notifications'
import wsService from '../services/websocket'

export default {
  name: 'Notifications',
  setup() {
    const showNotifications = ref(false)
    const notifications = ref([])
    const unreadCount = ref(0)
    const loading = ref(false)
    const notificationsContainer = ref(null)

    const toggleNotifications = () => {
      showNotifications.value = !showNotifications.value
    }

    const markAllAsRead = () => {
      notificationService.markAllAsRead()
    }

    const removeNotification = (id) => {
      notificationService.removeNotification(id)
    }

    const clearAllNotifications = () => {
      if (confirm('Вы уверены, что хотите удалить все уведомления?')) {
        notifications.value.forEach(n => notificationService.removeNotification(n.id))
      }
    }

    const handleNotificationClick = (notification) => {
      if (!notification.read) {
        notificationService.markAsRead(notification.id)
      }

      // Обработка специальных типов уведомлений
      if (notification.data) {
        handleNotificationAction(notification)
      }
    }

    const handleNotificationAction = (notification) => {
      // Здесь можно добавить специальную логику для разных типов уведомлений
      switch (notification.type) {
        case 'game':
          // Перейти к игре
          break
        case 'achievement':
          // Показать достижения
          break
        case 'bonus':
          // Показать бонусы
          break
      }
    }

    const getNotificationColor = (type) => {
      const colors = {
        success: 'bg-green/20 text-green',
        error: 'bg-red/20 text-red',
        warning: 'bg-yellow/20 text-yellow',
        info: 'bg-blue/20 text-blue',
        game: 'bg-violet/20 text-violet'
      }
      return colors[type] || colors.info
    }

    const getNotificationIcon = (type) => {
      const icons = {
        success: '✅',
        error: '❌',
        warning: '⚠️',
        info: 'ℹ️',
        game: '🎰'
      }
      return icons[type] || icons.info
    }

    const formatTime = (timestamp) => {
      const now = new Date()
      const diff = now - timestamp

      if (diff < 60000) { // Меньше минуты
        return 'только что'
      } else if (diff < 3600000) { // Меньше часа
        return `${Math.floor(diff / 60000)} мин назад`
      } else if (diff < 86400000) { // Меньше дня
        return `${Math.floor(diff / 3600000)} ч назад`
      } else {
        return timestamp.toLocaleDateString('ru-RU', {
          day: 'numeric',
          month: 'short',
          hour: '2-digit',
          minute: '2-digit'
        })
      }
    }

    // Обработчик уведомлений через WebSocket
    const handleWebSocketNotification = (payload) => {
      const { title, message, type = 'info' } = payload
      notificationService.addNotification({
        id: Date.now(),
        type,
        title,
        message,
        timestamp: new Date(),
        read: false
      })
    }

    // Подписываемся на изменения уведомлений
    let unsubscribe

    onMounted(() => {
      // Подписываемся на WebSocket уведомления
      wsService.on('notification', handleWebSocketNotification)

      unsubscribe = notificationService.subscribe((data) => {
        notifications.value = data.notifications
        unreadCount.value = data.unreadCount
      })

      // Инициализируем сервис уведомлений
      notificationService.init()
    })

    onUnmounted(() => {
      // Отписываемся от WebSocket
      wsService.off('notification', handleWebSocketNotification)

      if (unsubscribe) {
        unsubscribe()
      }
    })

    return {
      showNotifications,
      notifications,
      unreadCount,
      loading,
      notificationsContainer,
      toggleNotifications,
      markAllAsRead,
      removeNotification,
      clearAllNotifications,
      handleNotificationClick,
      getNotificationColor,
      getNotificationIcon,
      formatTime
    }
  }
}
</script>

<style scoped>
/* Кастомный скроллбар для уведомлений */
.overflow-y-auto::-webkit-scrollbar {
  width: 4px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: #1b1c20;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #7c75d9;
  border-radius: 2px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #8c84ec;
}
</style>
