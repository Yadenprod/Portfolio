import { initTelegram } from '../telegram'

class NotificationService {
  constructor() {
    this.tg = initTelegram()
    this.notifications = []
    this.unreadCount = 0
    this.listeners = []
  }

  // Инициализация сервиса уведомлений
  init() {
    if (this.tg?.WebApp) {
      // Подписываемся на события Web App
      this.tg.WebApp.onEvent('notification', this.handleNotification.bind(this))
    }

    // Проверяем уведомления каждые 30 секунд
    setInterval(() => {
      this.checkForNotifications()
    }, 30000)

    // Загружаем существующие уведомления
    this.loadStoredNotifications()
  }

  // Обработка входящих уведомлений
  handleNotification(event) {
    const notification = {
      id: Date.now(),
      type: event.type || 'info',
      title: event.title || 'Уведомление',
      message: event.message || '',
      timestamp: new Date(),
      read: false,
      data: event.data || null
    }

    this.addNotification(notification)
    this.showToast(notification)
  }

  // Добавление уведомления
  addNotification(notification) {
    this.notifications.unshift(notification)
    this.unreadCount++

    // Ограничиваем количество уведомлений
    if (this.notifications.length > 50) {
      this.notifications = this.notifications.slice(0, 50)
    }

    // Сохраняем в localStorage
    this.saveNotifications()

    // Уведомляем слушателей
    this.notifyListeners()
  }

  // Показать toast уведомление
  showToast(notification) {
    // Создаем toast элемент
    const toast = document.createElement('div')
    toast.className = `fixed top-4 left-4 right-4 z-50 p-4 rounded-xl text-white text-center animate-bounce shadow-lg`
    toast.classList.add(this.getNotificationColor(notification.type))

    toast.innerHTML = `
      <div class="flex items-center justify-center space-x-2">
        <span>${this.getNotificationIcon(notification.type)}</span>
        <span>${notification.title}</span>
      </div>
      ${notification.message ? `<div class="text-sm mt-1">${notification.message}</div>` : ''}
    `

    document.body.appendChild(toast)

    // Автоматически скрываем через 5 секунд
    setTimeout(() => {
      toast.remove()
    }, 5000)
  }

  // Получить цвет уведомления
  getNotificationColor(type) {
    const colors = {
      success: 'bg-green/90',
      error: 'bg-red/90',
      warning: 'bg-yellow/90',
      info: 'bg-blue/90',
      game: 'bg-violet/90'
    }
    return colors[type] || colors.info
  }

  // Получить иконку уведомления
  getNotificationIcon(type) {
    const icons = {
      success: '✅',
      error: '❌',
      warning: '⚠️',
      info: 'ℹ️',
      game: '🎰'
    }
    return icons[type] || icons.info
  }

  // Отметить уведомление как прочитанное
  markAsRead(id) {
    const notification = this.notifications.find(n => n.id === id)
    if (notification && !notification.read) {
      notification.read = true
      this.unreadCount = Math.max(0, this.unreadCount - 1)
      this.saveNotifications()
      this.notifyListeners()
    }
  }

  // Отметить все уведомления как прочитанные
  markAllAsRead() {
    this.notifications.forEach(n => {
      n.read = true
    })
    this.unreadCount = 0
    this.saveNotifications()
    this.notifyListeners()
  }

  // Удалить уведомление
  removeNotification(id) {
    const index = this.notifications.findIndex(n => n.id === id)
    if (index !== -1) {
      const notification = this.notifications[index]
      if (!notification.read) {
        this.unreadCount = Math.max(0, this.unreadCount - 1)
      }
      this.notifications.splice(index, 1)
      this.saveNotifications()
      this.notifyListeners()
    }
  }

  // Проверка новых уведомлений
  async checkForNotifications() {
    try {
      // Здесь будет запрос к API для получения новых уведомлений
      // const response = await fetchNotifications()
      // response.forEach(notification => this.addNotification(notification))
    } catch (error) {
      console.error('Failed to check notifications:', error)
    }
  }

  // Загрузка уведомлений из localStorage
  loadStoredNotifications() {
    try {
      const stored = localStorage.getItem('telegram_casino_notifications')
      if (stored) {
        this.notifications = JSON.parse(stored).map(n => ({
          ...n,
          timestamp: new Date(n.timestamp)
        }))
        this.unreadCount = this.notifications.filter(n => !n.read).length
      }
    } catch (error) {
      console.error('Failed to load stored notifications:', error)
    }
  }

  // Сохранение уведомлений в localStorage
  saveNotifications() {
    try {
      localStorage.setItem('telegram_casino_notifications', JSON.stringify(this.notifications))
    } catch (error) {
      console.error('Failed to save notifications:', error)
    }
  }

  // Подписка на изменения
  subscribe(callback) {
    this.listeners.push(callback)
    return () => {
      const index = this.listeners.indexOf(callback)
      if (index !== -1) {
        this.listeners.splice(index, 1)
      }
    }
  }

  // Уведомление слушателей
  notifyListeners() {
    this.listeners.forEach(callback => callback({
      notifications: this.notifications,
      unreadCount: this.unreadCount
    }))
  }

  // Отправка уведомления через Telegram
  sendTelegramNotification(title, message, type = 'info') {
    if (this.tg?.WebApp) {
      // Отправляем уведомление через Telegram Web App
      this.tg.WebApp.showAlert(`${title}: ${message}`)
    }
  }

  // Создание уведомления о выигрыше
  createWinNotification(amount, game) {
    this.addNotification({
      id: Date.now(),
      type: 'success',
      title: 'Поздравляем!',
      message: `Вы выиграли ${amount}₽ в ${game}!`,
      timestamp: new Date(),
      read: false,
      data: { amount, game }
    })
  }

  // Создание уведомления о проигрыше
  createLossNotification(amount, game) {
    this.addNotification({
      id: Date.now(),
      type: 'error',
      title: 'Неудача',
      message: `Проигрыш ${amount}₽ в ${game}`,
      timestamp: new Date(),
      read: false,
      data: { amount, game }
    })
  }

  // Создание уведомления о достижении
  createAchievementNotification(achievementName, reward) {
    this.addNotification({
      id: Date.now(),
      type: 'game',
      title: 'Новое достижение!',
      message: `${achievementName} (+${reward} очков)`,
      timestamp: new Date(),
      read: false,
      data: { achievement: achievementName, reward }
    })
  }

  // Создание уведомления о бонусе
  createBonusNotification(bonusType, amount) {
    this.addNotification({
      id: Date.now(),
      type: 'success',
      title: 'Бонус получен!',
      message: `${bonusType}: +${amount}₽`,
      timestamp: new Date(),
      read: false,
      data: { bonusType, amount }
    })
  }

  // Создание уведомления о новом уровне
  createLevelUpNotification(newLevel) {
    this.addNotification({
      id: Date.now(),
      type: 'game',
      title: 'Уровень повышен!',
      message: `Теперь у вас ${newLevel} уровень`,
      timestamp: new Date(),
      read: false,
      data: { level: newLevel }
    })
  }
}

// Создаем синглтон
const notificationService = new NotificationService()

export default notificationService

// Глобальная функция для быстрого доступа
export const notify = {
  success: (title, message) => notificationService.addNotification({
    id: Date.now(),
    type: 'success',
    title,
    message,
    timestamp: new Date(),
    read: false
  }),

  error: (title, message) => notificationService.addNotification({
    id: Date.now(),
    type: 'error',
    title,
    message,
    timestamp: new Date(),
    read: false
  }),

  warning: (title, message) => notificationService.addNotification({
    id: Date.now(),
    type: 'warning',
    title,
    message,
    timestamp: new Date(),
    read: false
  }),

  info: (title, message) => notificationService.addNotification({
    id: Date.now(),
    type: 'info',
    title,
    message,
    timestamp: new Date(),
    read: false
  }),

  win: (amount, game) => notificationService.createWinNotification(amount, game),
  loss: (amount, game) => notificationService.createLossNotification(amount, game),
  achievement: (name, reward) => notificationService.createAchievementNotification(name, reward),
  bonus: (type, amount) => notificationService.createBonusNotification(type, amount),
  levelUp: (level) => notificationService.createLevelUpNotification(level)
}
