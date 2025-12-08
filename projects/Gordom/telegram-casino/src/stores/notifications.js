import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useNotificationsStore = defineStore('notifications', {
  state: () => ({
    notifications: [],
    unreadCount: 0,
    settings: {
      betResults: true,
      liveEvents: true,
      promotions: true,
      soundEnabled: true,
      pushEnabled: false
    }
  }),

  getters: {
    allNotifications: (state) => state.notifications.sort((a, b) => new Date(b.created_at) - new Date(a.created_at)),
    unreadNotifications: (state) => state.notifications.filter(n => !n.read),
    recentNotifications: (state) => state.notifications.slice(0, 10),
    hasUnread: (state) => state.unreadCount > 0
  },

  actions: {
    // Добавление нового уведомления
    addNotification(notification) {
      const newNotification = {
        id: Date.now() + Math.random(),
        type: notification.type || 'info',
        title: notification.title,
        message: notification.message,
        data: notification.data || {},
        read: false,
        created_at: new Date().toISOString(),
        autoHide: notification.autoHide !== false
      }

      this.notifications.unshift(newNotification)
      this.unreadCount++

      // Ограничить количество уведомлений
      if (this.notifications.length > 100) {
        this.notifications = this.notifications.slice(0, 100)
      }

      // Показать toast уведомление
      if (this.settings.soundEnabled) {
        this.playNotificationSound(newNotification.type)
      }

      // Отправить push уведомление если включено
      if (this.settings.pushEnabled && 'serviceWorker' in navigator) {
        this.sendPushNotification(newNotification)
      }

      // Автоматически скрыть через 5 секунд для некоторых типов
      if (newNotification.autoHide) {
        setTimeout(() => {
          this.markAsRead(newNotification.id)
        }, 5000)
      }

      return newNotification.id
    },

    // Уведомления о результатах ставок
    addBetResultNotification(bet, result) {
      if (!this.settings.betResults) return

      const isWin = result.profit > 0
      const title = isWin ? '🎉 Ставка выиграла!' : '😞 Ставка проиграла'
      const message = isWin
        ? `Ваша ставка ${bet.amount}₽ принесла +${result.profit}₽`
        : `Ставка ${bet.amount}₽ проиграна`

      return this.addNotification({
        type: isWin ? 'success' : 'error',
        title,
        message,
        data: { bet, result },
        autoHide: true
      })
    },

    // Уведомления о live событиях
    addLiveEventNotification(event, updateType) {
      if (!this.settings.liveEvents) return

      let title = ''
      let message = ''

      switch (updateType) {
        case 'goal':
          title = '⚽️ Гол!'
          message = `${event.home_team} vs ${event.away_team} - ${event.current_score.home}:${event.current_score.away}`
          break
        case 'round':
          title = '🎮 Новый раунд'
          message = `${event.home_team} vs ${event.away_team} - Раунд ${event.round}`
          break
        case 'kill':
          title = '💀 Убийство'
          message = `${event.home_team} vs ${event.away_team} - Общее: ${event.kills?.home + event.kills?.away || 0}`
          break
        case 'event_start':
          title = '🏁 Событие началось!'
          message = `${event.home_team} vs ${event.away_team} - Live`
          break
      }

      return this.addNotification({
        type: 'info',
        title,
        message,
        data: { event, updateType },
        autoHide: true
      })
    },

    // Промо уведомления
    addPromotionNotification(promo) {
      if (!this.settings.promotions) return

      return this.addNotification({
        type: 'promotion',
        title: '🎁 Специальное предложение!',
        message: promo.message,
        data: { promo },
        autoHide: false
      })
    },

    // Системные уведомления
    addSystemNotification(message, type = 'info') {
      return this.addNotification({
        type,
        title: '💬 Система',
        message,
        autoHide: true
      })
    },

    // Отметить как прочитанное
    markAsRead(notificationId) {
      const notification = this.notifications.find(n => n.id === notificationId)
      if (notification && !notification.read) {
        notification.read = true
        this.unreadCount = Math.max(0, this.unreadCount - 1)
      }
    },

    // Отметить все как прочитанные
    markAllAsRead() {
      this.notifications.forEach(n => n.read = true)
      this.unreadCount = 0
    },

    // Удалить уведомление
    removeNotification(notificationId) {
      const index = this.notifications.findIndex(n => n.id === notificationId)
      if (index > -1) {
        const notification = this.notifications[index]
        if (!notification.read) {
          this.unreadCount = Math.max(0, this.unreadCount - 1)
        }
        this.notifications.splice(index, 1)
      }
    },

    // Очистить все уведомления
    clearAllNotifications() {
      this.notifications = []
      this.unreadCount = 0
    },

    // Обновить настройки
    updateSettings(newSettings) {
      this.settings = { ...this.settings, ...newSettings }
    },

    // Воспроизвести звук уведомления
    playNotificationSound(type) {
      try {
        const audioContext = new (window.AudioContext || window.webkitAudioContext)()
        const oscillator = audioContext.createOscillator()
        const gainNode = audioContext.createGain()

        oscillator.connect(gainNode)
        gainNode.connect(audioContext.destination)

        // Разные звуки для разных типов
        const frequencies = {
          success: 523.25, // C5
          error: 349.23,   // F4
          info: 440.00,    // A4
          promotion: 659.25 // E5
        }

        oscillator.frequency.setValueAtTime(frequencies[type] || 440, audioContext.currentTime)
        oscillator.type = 'sine'

        gainNode.gain.setValueAtTime(0, audioContext.currentTime)
        gainNode.gain.linearRampToValueAtTime(0.1, audioContext.currentTime + 0.01)
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.3)

        oscillator.start(audioContext.currentTime)
        oscillator.stop(audioContext.currentTime + 0.3)
      } catch (error) {
        console.warn('Audio playback failed:', error)
      }
    },

    // Отправить push уведомление
    async sendPushNotification(notification) {
      if (!('serviceWorker' in navigator) || !this.settings.pushEnabled) return

      try {
        const registration = await navigator.serviceWorker.ready
        await registration.showNotification(notification.title, {
          body: notification.message,
          icon: '/favicon.svg',
          badge: '/favicon.svg',
          tag: `notification-${notification.id}`,
          requireInteraction: !notification.autoHide,
          data: notification.data,
          actions: [
            {
              action: 'view',
              title: 'Посмотреть'
            },
            {
              action: 'dismiss',
              title: 'Закрыть'
            }
          ]
        })
      } catch (error) {
        console.warn('Push notification failed:', error)
      }
    },

    // Инициализация push уведомлений
    async initPushNotifications() {
      if (!('serviceWorker' in navigator) || !('PushManager' in window)) {
        console.warn('Push notifications not supported')
        return false
      }

      try {
        const registration = await navigator.serviceWorker.register('/sw.js')
        const permission = await Notification.requestPermission()

        if (permission === 'granted') {
          const subscription = await registration.pushManager.subscribe({
            userVisibleOnly: true,
            applicationServerKey: this.urlB64ToUint8Array('YOUR_PUBLIC_VAPID_KEY')
          })

          this.settings.pushEnabled = true
          return true
        }

        return false
      } catch (error) {
        console.error('Push notification init failed:', error)
        return false
      }
    },

    // Вспомогательная функция для VAPID ключа
    urlB64ToUint8Array(base64String) {
      const padding = '='.repeat((4 - base64String.length % 4) % 4)
      const base64 = (base64String + padding).replace(/-/g, '+').replace(/_/g, '/')
      const rawData = window.atob(base64)
      const outputArray = new Uint8Array(rawData.length)

      for (let i = 0; i < rawData.length; ++i) {
        outputArray[i] = rawData.charCodeAt(i)
      }

      return outputArray
    }
  }
})
