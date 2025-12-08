import { notify } from './notifications'
import config from '../config.js'

class WebSocketService {
  constructor() {
    this.socket = null
    this.isConnected = false
    this.reconnectAttempts = 0
    this.maxReconnectAttempts = 5
    this.reconnectInterval = 3000
    this.listeners = new Map()
    this.pendingMessages = []
    this.heartbeatInterval = null
    this.userId = null
  }

  // Инициализация WebSocket
  init(userId, token = null) {
    this.userId = userId
    this.token = token

    // Определяем URL WebSocket (для разработки используем локальный)
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    let wsUrl = config.apiUrls.websocket || `${protocol}//localhost:6001`

    // Если VITE_WS_URL предоставлен, убедимся, что протокол правильный
    if (import.meta.env.VITE_WS_URL) {
      if (wsUrl.startsWith('http:')) {
        wsUrl = wsUrl.replace('http:', 'ws:')
      } else if (wsUrl.startsWith('https:')) {
        wsUrl = wsUrl.replace('https:', 'wss:')
      }
    }

    this.connect(wsUrl)
  }

  // Подключение к WebSocket
  connect(url) {
    try {
      console.log('Connecting to WebSocket:', url)
      this.socket = new WebSocket(url)

      this.socket.onopen = this.onOpen.bind(this)
      this.socket.onmessage = this.onMessage.bind(this)
      this.socket.onclose = this.onClose.bind(this)
      this.socket.onerror = this.onError.bind(this)

    } catch (error) {
      console.error('WebSocket connection error:', error)
      this.handleReconnect()
    }
  }

  // Обработчик открытия соединения
  onOpen(event) {
    console.log('WebSocket connected')
    this.isConnected = true
    this.reconnectAttempts = 0

    // Аутентификация пользователя
    this.authenticate()

    // Запуск heartbeat
    this.startHeartbeat()

    // Отправка ожидающих сообщений
    this.sendPendingMessages()

              // Уведомление о подключении
          try {
            notify.success('Подключение', 'Соединение установлено')
          } catch (error) {
            console.log('WebSocket connected successfully')
          }
  }

  // Обработчик входящих сообщений
  onMessage(event) {
    try {
      const data = JSON.parse(event.data)
      console.log('WebSocket message received:', data)

      this.handleMessage(data)
    } catch (error) {
      console.error('Error parsing WebSocket message:', error)
    }
  }

  // Обработчик закрытия соединения
  onClose(event) {
    console.log('WebSocket disconnected:', event.code, event.reason)
    this.isConnected = false
    this.stopHeartbeat()

    if (event.code !== 1000) { // Не нормальное закрытие
      this.handleReconnect()
    }
  }

  // Обработчик ошибок
  onError(error) {
    console.error('WebSocket error:', error)
  }

  // Аутентификация пользователя
  authenticate() {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      const authMessage = {
        type: 'auth',
        user_id: this.userId,
        token: this.token
      }
      this.socket.send(JSON.stringify(authMessage))
    }
  }

  // Отправка сообщения
  send(type, payload = {}) {
    const message = {
      type,
      payload: {
        user_id: this.userId,
        ...payload
      },
      timestamp: Date.now()
    }

    if (this.isConnected && this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(JSON.stringify(message))
    } else {
      // Сохраняем для отправки после подключения
      this.pendingMessages.push(message)
    }
  }

  // Обработка входящих сообщений
  handleMessage(data) {
    const { type, payload } = data

    switch (type) {
      case 'auth_success':
        console.log('WebSocket authenticated successfully')
        break

      case 'chat_message':
        this.emit('chat_message', payload)
        break

      case 'notification':
        this.emit('notification', payload)
        this.handleNotification(payload)
        break

      case 'game_update':
        this.emit('game_update', payload)
        break

      case 'user_balance_update':
        this.emit('user_balance_update', payload)
        break

      case 'online_users':
        this.emit('online_users', payload)
        break

      case 'tournament_update':
        this.emit('tournament_update', payload)
        break

      case 'achievement_unlocked':
        this.emit('achievement_unlocked', payload)
        this.handleAchievement(payload)
        break

      case 'leaderboard_update':
        this.emit('leaderboard_update', payload)
        break

      case 'pong':
        // Heartbeat response
        break

      default:
        console.log('Unknown message type:', type)
    }
  }

  // Обработка уведомлений
  handleNotification(payload) {
    const { title, message, type = 'info' } = payload

    switch (type) {
      case 'success':
        notify.success(title, message)
        break
      case 'error':
        notify.error(title, message)
        break
      case 'warning':
        notify.warning(title, message)
        break
      case 'game':
        notify.info(title, message)
        break
      default:
        notify.info(title, message)
    }
  }

  // Обработка достижений
  handleAchievement(payload) {
    const { name, reward } = payload
    notify.achievement(name, reward)
  }

  // Отправка сообщения в чат
  sendChatMessage(message) {
    this.send('chat_message', { message })
  }

  // Присоединение к игре
  joinGame(gameType, gameId) {
    this.send('join_game', { game_type: gameType, game_id: gameId })
  }

  // Выход из игры
  leaveGame(gameType, gameId) {
    this.send('leave_game', { game_type: gameType, game_id: gameId })
  }

  // Обновление статуса игры
  updateGameStatus(gameType, gameId, status) {
    this.send('game_status_update', { game_type: gameType, game_id: gameId, status })
  }

  // Присоединение к турниру
  joinTournament(tournamentId) {
    this.send('join_tournament', { tournament_id: tournamentId })
  }

  // Heartbeat для поддержания соединения
  startHeartbeat() {
    this.heartbeatInterval = setInterval(() => {
      if (this.isConnected) {
        this.send('ping')
      }
    }, 30000) // Каждые 30 секунд
  }

  // Остановка heartbeat
  stopHeartbeat() {
    if (this.heartbeatInterval) {
      clearInterval(this.heartbeatInterval)
      this.heartbeatInterval = null
    }
  }

  // Обработка переподключения
  handleReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++
      const delay = this.reconnectInterval * this.reconnectAttempts

      console.log(`Attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts}) in ${delay}ms`)

      setTimeout(() => {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
        const wsUrl = config.apiUrls.websocket || `${protocol}//localhost:6001`
        this.connect(wsUrl)
      }, delay)
    } else {
      console.error('Max reconnection attempts reached')
      try {
        notify.error('Соединение', 'Не удалось восстановить соединение с сервером')
      } catch (error) {
        console.error('Failed to show connection error notification')
      }
    }
  }

  // Отправка ожидающих сообщений
  sendPendingMessages() {
    while (this.pendingMessages.length > 0) {
      const message = this.pendingMessages.shift()
      this.socket.send(JSON.stringify(message))
    }
  }

  // Подписка на события
  on(event, callback) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, [])
    }
    this.listeners.get(event).push(callback)
  }

  // Отписка от событий
  off(event, callback) {
    if (this.listeners.has(event)) {
      const callbacks = this.listeners.get(event)
      const index = callbacks.indexOf(callback)
      if (index !== -1) {
        callbacks.splice(index, 1)
      }
    }
  }

  // Генерация событий
  emit(event, data) {
    if (this.listeners.has(event)) {
      this.listeners.get(event).forEach(callback => {
        try {
          callback(data)
        } catch (error) {
          console.error('Error in WebSocket event listener:', error)
        }
      })
    }
  }

  // Отключение
  disconnect() {
    this.stopHeartbeat()
    if (this.socket) {
      this.socket.close(1000, 'Client disconnect')
      this.socket = null
    }
    this.isConnected = false
  }

  // Получение статуса соединения
  getStatus() {
    return {
      isConnected: this.isConnected,
      reconnectAttempts: this.reconnectAttempts,
      pendingMessages: this.pendingMessages.length
    }
  }
}

// Создаем синглтон
const wsService = new WebSocketService()

export default wsService
