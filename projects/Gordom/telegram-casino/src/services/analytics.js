// Убираем импорт store - будем получать его динамически
import { notify } from './notifications'

class AnalyticsService {
  constructor() {
    this.userStore = null // Будет установлен позже
    this.sessionId = this.generateSessionId()
    this.sessionStart = Date.now()
    this.events = []
    this.isEnabled = true
    this.batchSize = 10
    this.flushInterval = 30000 // 30 секунд
    this.autoFlushTimer = null
  }

  // Установка userStore после инициализации Pinia
  setUserStore(userStore) {
    this.userStore = userStore
  }

  // Инициализация аналитики
  init() {
    if (!this.isEnabled) return

    // Временно отключаем аналитику в dev режиме для избежания ошибок
    if (process.env.NODE_ENV === 'development') {
      console.log('Analytics service disabled in development mode')
      return
    }

    this.trackEvent('app_start', {
      userAgent: navigator.userAgent,
      platform: navigator.platform,
      language: navigator.language,
      screenSize: `${screen.width}x${screen.height}`,
      viewportSize: `${window.innerWidth}x${window.innerHeight}`,
      referrer: document.referrer,
      timezone: Intl.DateTimeFormat().resolvedOptions().timeZone
    })

    this.setupAutoFlush()
    this.setupEventListeners()
    this.setupGameTracking()
    this.setupPerformanceTracking()
  }

  // Генерация ID сессии
  generateSessionId() {
    return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9)
  }

  // Отслеживание событий
  trackEvent(eventName, eventData = {}) {
    if (!this.isEnabled) return

    const event = {
      sessionId: this.sessionId,
      userId: this.userStore?.user?.id || null,
      eventName,
      eventData,
      timestamp: Date.now(),
      url: window.location.href,
      userAgent: navigator.userAgent
    }

    this.events.push(event)

    // Отправка события в режиме реального времени для важных событий
    if (this.isRealtimeEvent(eventName)) {
      this.sendEvent(event)
    }

    // Пакетная отправка при достижении размера батча
    if (this.events.length >= this.batchSize) {
      this.flush()
    }
  }

  // Проверка, является ли событие требующим отправки в реальном времени
  isRealtimeEvent(eventName) {
    const realtimeEvents = [
      'app_start',
      'user_login',
      'game_start',
      'game_end',
      'purchase',
      'error',
      'crash'
    ]
    return realtimeEvents.includes(eventName)
  }

  // Отправка одиночного события
  async sendEvent(event) {
    try {
      await fetch('/api/analytics/event', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(event)
      })
    } catch (error) {
      console.error('Failed to send analytics event:', error)
    }
  }

  // Отправка пакета событий
  async flush() {
    if (this.events.length === 0) return

    const events = [...this.events]
    this.events = []

    try {
      const response = await fetch('/api/analytics/batch', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ events })
      })

      if (response.ok) {
        console.log('Analytics batch sent successfully')
      } else {
        // Восстановление событий при ошибке
        this.events.unshift(...events)
        console.error('Failed to send analytics batch')
      }
    } catch (error) {
      // Восстановление событий при ошибке
      this.events.unshift(...events)
      console.error('Failed to send analytics batch:', error)
    }
  }

  // Настройка автоматической отправки
  setupAutoFlush() {
    this.autoFlushTimer = setInterval(() => {
      this.flush()
    }, this.flushInterval)
  }

  // Настройка прослушивателей событий
  setupEventListeners() {
    // Отслеживание кликов
    document.addEventListener('click', (e) => {
      const target = e.target.closest('[data-track]')
      if (target) {
        const eventName = target.dataset.track
        const eventData = target.dataset.trackData ? JSON.parse(target.dataset.trackData) : {}
        this.trackEvent(eventName, {
          ...eventData,
          element: target.tagName.toLowerCase(),
          text: target.textContent?.trim()
        })
      }
    })

    // Отслеживание навигации
    window.addEventListener('popstate', () => {
      this.trackEvent('page_view', {
        page: window.location.pathname,
        title: document.title
      })
    })

    // Отслеживание ошибок JavaScript
    window.addEventListener('error', (event) => {
      this.trackEvent('javascript_error', {
        message: event.message,
        filename: event.filename,
        lineno: event.lineno,
        colno: event.colno,
        error: event.error?.stack
      })
    })

    // Отслеживание необработанных обещаний
    window.addEventListener('unhandledrejection', (event) => {
      this.trackEvent('unhandled_promise_rejection', {
        reason: event.reason?.message || event.reason,
        stack: event.reason?.stack
      })
    })

    // Отслеживание видимости страницы
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) {
        this.trackEvent('page_hidden', {
          timeSpent: Date.now() - this.sessionStart
        })
      } else {
        this.trackEvent('page_visible')
      }
    })

    // Отслеживание ухода со страницы
    window.addEventListener('beforeunload', () => {
      this.trackEvent('page_unload', {
        timeSpent: Date.now() - this.sessionStart
      })
      this.flush() // Синхронная отправка
    })
  }

  // Настройка отслеживания игр
  setupGameTracking() {
    // Отслеживание начала игры
    this.trackGameEvent = (gameName, action, data = {}) => {
      this.trackEvent('game_action', {
        game: gameName,
        action,
        ...data
      })
    }

    // Отслеживание результатов игры
    this.trackGameResult = (gameName, result, bet, win, multiplier) => {
      this.trackEvent('game_result', {
        game: gameName,
        result,
        bet,
        win,
        multiplier,
        profit: win - bet
      })
    }

    // Отслеживание ставок
    this.trackBet = (gameName, amount, type) => {
      this.trackEvent('bet_placed', {
        game: gameName,
        amount,
        type
      })
    }
  }

  // Настройка отслеживания производительности
  setupPerformanceTracking() {
    // Отслеживание загрузки ресурсов
    const observer = new PerformanceObserver((list) => {
      list.getEntries().forEach(entry => {
        if (entry.duration > 1000) {
          this.trackEvent('slow_resource', {
            resource: entry.name,
            duration: entry.duration,
            type: entry.initiatorType
          })
        }
      })
    })

    try {
      observer.observe({ entryTypes: ['resource'] })
    } catch (error) {
      console.error('Performance observer error:', error)
    }
  }

  // Отслеживание пользовательских действий
  trackUserAction(action, data = {}) {
    this.trackEvent('user_action', {
      action,
      ...data
    })
  }

  // Отслеживание покупок
  trackPurchase(item, amount, currency = 'RUB') {
    this.trackEvent('purchase', {
      item,
      amount,
      currency
    })
  }

  // Отслеживание использования бонусов
  trackBonusUsage(bonusType, amount) {
    this.trackEvent('bonus_usage', {
      bonusType,
      amount
    })
  }

  // Отслеживание достижений
  trackAchievement(achievementName, reward) {
    this.trackEvent('achievement_unlocked', {
      achievement: achievementName,
      reward
    })
  }

  // Отслеживание ошибок API
  trackApiError(endpoint, error, statusCode) {
    this.trackEvent('api_error', {
      endpoint,
      error: error.message || error,
      statusCode
    })
  }

  // Отслеживание времени взаимодействия
  startTiming(label) {
    this.timings = this.timings || {}
    this.timings[label] = Date.now()
  }

  endTiming(label) {
    if (this.timings && this.timings[label]) {
      const duration = Date.now() - this.timings[label]
      this.trackEvent('timing', {
        label,
        duration
      })
      delete this.timings[label]
    }
  }

  // Отслеживание пути пользователя
  trackUserFlow(step, data = {}) {
    this.trackEvent('user_flow', {
      step,
      ...data
    })
  }

  // Отслеживание A/B тестов
  trackABTest(testName, variant, data = {}) {
    this.trackEvent('ab_test', {
      testName,
      variant,
      ...data
    })
  }

  // Отслеживание вовлеченности
  trackEngagement(action, data = {}) {
    this.trackEvent('engagement', {
      action,
      ...data
    })
  }

  // Получение статистики сессии
  getSessionStats() {
    return {
      sessionId: this.sessionId,
      sessionDuration: Date.now() - this.sessionStart,
      eventsCount: this.events.length,
      userId: this.userStore?.user?.id || null
    }
  }

  // Экспорт данных для отладки
  exportDebugData() {
    return {
      session: this.getSessionStats(),
      recentEvents: this.events.slice(-10),
      pendingEvents: this.events.length
    }
  }

  // Остановка аналитики
  disable() {
    this.isEnabled = false
    if (this.autoFlushTimer) {
      clearInterval(this.autoFlushTimer)
    }
  }

  // Возобновление аналитики
  enable() {
    this.isEnabled = true
    this.setupAutoFlush()
  }

  // Очистка всех данных
  clear() {
    this.events = []
    this.sessionId = this.generateSessionId()
    this.sessionStart = Date.now()
  }

  // Уничтожение сервиса
  destroy() {
    this.disable()
    this.events = []
    this.timings = {}
  }
}

// Создаем синглтон
const analyticsService = new AnalyticsService()

// Глобальные функции для удобства использования
export const analytics = {
  trackEvent: (eventName, data) => analyticsService.trackEvent(eventName, data),
  trackUserAction: (action, data) => analyticsService.trackUserAction(action, data),
  trackPurchase: (item, amount) => analyticsService.trackPurchase(item, amount),
  trackGameEvent: (game, action, data) => analyticsService.trackGameEvent(game, action, data),
  trackGameResult: (game, result, bet, win, multiplier) => analyticsService.trackGameResult(game, result, bet, win, multiplier),
  trackBet: (game, amount, type) => analyticsService.trackBet(game, amount, type),
  trackApiError: (endpoint, error, status) => analyticsService.trackApiError(endpoint, error, status),
  startTiming: (label) => analyticsService.startTiming(label),
  endTiming: (label) => analyticsService.endTiming(label),
  trackUserFlow: (step, data) => analyticsService.trackUserFlow(step, data),
  trackABTest: (test, variant, data) => analyticsService.trackABTest(test, variant, data),
  trackEngagement: (action, data) => analyticsService.trackEngagement(action, data),
  trackBonusUsage: (type, amount) => analyticsService.trackBonusUsage(type, amount),
  trackAchievement: (name, reward) => analyticsService.trackAchievement(name, reward),
  getSessionStats: () => analyticsService.getSessionStats(),
  exportDebugData: () => analyticsService.exportDebugData()
}

export default analyticsService
