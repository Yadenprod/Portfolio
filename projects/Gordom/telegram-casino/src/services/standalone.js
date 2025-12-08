// Сервис для управления автономным режимом работы приложения

// Ключи для localStorage
const STORAGE_KEYS = {
  USER: 'telegram_casino_user',
  HISTORY: 'telegram_casino_history',
  PROMOCODES: 'telegram_casino_promocodes',
  BETS: 'telegram_casino_bets',
  BET_HISTORY: 'telegram_casino_bet_history',
  SETTINGS: 'telegram_casino_settings'
}

// Проверка доступности localStorage
function isStorageAvailable() {
  try {
    const test = '__storage_test__'
    localStorage.setItem(test, test)
    localStorage.removeItem(test)
    return true
  } catch (e) {
    return false
  }
}

// Получить данные из localStorage
export function getLocalData(key, defaultValue = null) {
  if (!isStorageAvailable()) {
    console.warn('localStorage not available')
    return defaultValue
  }

  try {
    const data = localStorage.getItem(key)
    return data ? JSON.parse(data) : defaultValue
  } catch (error) {
    console.error('Error reading from localStorage:', error)
    return defaultValue
  }
}

// Сохранить данные в localStorage
export function setLocalData(key, data) {
  if (!isStorageAvailable()) {
    console.warn('localStorage not available')
    return false
  }

  try {
    localStorage.setItem(key, JSON.stringify(data))
    return true
  } catch (error) {
    console.error('Error saving to localStorage:', error)
    return false
  }
}

// Получить или создать пользователя
export function getOrCreateUser() {
  let user = getLocalData(STORAGE_KEYS.USER)

  if (!user) {
    user = {
      id: Date.now(),
      telegram_id: Date.now().toString(),
      name: 'Test User',
      username: 'testuser',
      balance: 1000,
      achievements: [],
      rank: 1,
      totalGames: 0,
      winRate: 0,
      totalWinnings: 0,
      created_at: new Date().toISOString()
    }
    setLocalData(STORAGE_KEYS.USER, user)
  }

  return user
}

// Обновить баланс пользователя
export function updateUserBalance(delta) {
  const user = getOrCreateUser()
  user.balance = Math.max(0, user.balance + delta)
  setLocalData(STORAGE_KEYS.USER, user)
  return user
}

// Получить историю игр
export function getGameHistory() {
  return getLocalData(STORAGE_KEYS.HISTORY, [])
}

// Добавить игру в историю
export function addGameToHistory(gameData) {
  const history = getGameHistory()
  const gameEntry = {
    id: Date.now(),
    game: gameData.game || 'unknown',
    amount: gameData.amount || 0,
    win: gameData.win || false,
    multiplier: gameData.multiplier || 0,
    result: gameData.result || 0,
    chance: gameData.chance || 50,
    created_at: new Date().toISOString()
  }

  history.unshift(gameEntry) // Добавляем в начало
  if (history.length > 100) {
    history.splice(100) // Ограничиваем до 100 записей
  }

  setLocalData(STORAGE_KEYS.HISTORY, history)
  return gameEntry
}

// Проверить, работает ли приложение автономно
export function isStandaloneMode() {
  return !window.Telegram?.WebApp
}

// Получить статистику пользователя
export function getUserStats() {
  const user = getOrCreateUser()
  const history = getGameHistory()

  if (history.length === 0) {
    return {
      totalGames: 0,
      winRate: 0,
      totalWinnings: 0,
      biggestWin: 0,
      biggestLoss: 0
    }
  }

  const wins = history.filter(game => game.win).length
  const totalWinnings = history
    .filter(game => game.win)
    .reduce((sum, game) => sum + (game.amount * game.multiplier - game.amount), 0)

  const biggestWin = Math.max(...history
    .filter(game => game.win)
    .map(game => game.amount * game.multiplier - game.amount))

  const biggestLoss = Math.max(...history
    .filter(game => !game.win)
    .map(game => game.amount))

  return {
    totalGames: history.length,
    winRate: history.length > 0 ? (wins / history.length) * 100 : 0,
    totalWinnings: totalWinnings,
    biggestWin: biggestWin > 0 ? biggestWin : 0,
    biggestLoss: biggestLoss > 0 ? biggestLoss : 0
  }
}

// Очистить все данные (для отладки)
export function clearAllData() {
  if (isStorageAvailable()) {
    Object.values(STORAGE_KEYS).forEach(key => {
      localStorage.removeItem(key)
    })
  }
}

// Экспортировать все данные (для резервного копирования)
export function exportAllData() {
  const data = {}
  Object.keys(STORAGE_KEYS).forEach(key => {
    data[key] = getLocalData(STORAGE_KEYS[key])
  })
  return data
}

// Импортировать данные (для восстановления)
export function importData(data) {
  Object.keys(data).forEach(key => {
    if (STORAGE_KEYS[key]) {
      setLocalData(STORAGE_KEYS[key], data[key])
    }
  })
}
