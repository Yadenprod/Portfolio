import { defineStore } from 'pinia'
import {
  getSportsEvents,
  getLiveEvents,
  placeBet,
  getUserBets,
  getBetHistory,
  getBetStats
} from '../api/endpoints'

export const useBetsStore = defineStore('bets', {
  state: () => ({
    // Спортивные события
    events: [],
    liveEvents: [],
    loading: false,
    error: null,

    // Ставки пользователя
    userBets: [],
    betHistory: [],
    betStats: null,

    // Фильтры и настройки
    selectedSport: 'all',
    selectedTimeframe: 'all',
    selectedCategory: 'all', // traditional, esports

    // Корзина ставок
    betSlip: [],
    totalStake: 0,
    potentialWin: 0
  }),

  getters: {
    // Фильтрованные события
    filteredEvents: (state) => {
      let filtered = state.events

      // Фильтр по категории (традиционный спорт vs киберспорт)
      if (state.selectedCategory !== 'all') {
        if (state.selectedCategory === 'esports') {
          filtered = filtered.filter(event =>
            ['csgo', 'dota2', 'lol', 'valorant', 'pubg', 'apex', 'rainbow'].includes(event.sport)
          )
        } else if (state.selectedCategory === 'traditional') {
          filtered = filtered.filter(event =>
            !['csgo', 'dota2', 'lol', 'valorant', 'pubg', 'apex', 'rainbow'].includes(event.sport)
          )
        }
      }

      if (state.selectedSport !== 'all') {
        filtered = filtered.filter(event => event.sport === state.selectedSport)
      }

      if (state.selectedTimeframe !== 'all') {
        const now = new Date()
        const hours = parseInt(state.selectedTimeframe)
        const cutoff = new Date(now.getTime() + hours * 60 * 60 * 1000)

        filtered = filtered.filter(event => {
          const eventTime = new Date(event.start_time)
          return eventTime <= cutoff
        })
      }

      return filtered.sort((a, b) => new Date(a.start_time) - new Date(b.start_time))
    },

    // Активные ставки
    activeBets: (state) => state.userBets.filter(bet => bet.status === 'active'),

    // Завершенные ставки
    completedBets: (state) => state.betHistory.filter(bet => bet.result === 'win' || bet.result === 'lose'),

    // Выигрышные ставки
    winningBets: (state) => state.betHistory.filter(bet => bet.result === 'win'),

    // Проигрышные ставки
    losingBets: (state) => state.betHistory.filter(bet => bet.result === 'lose'),

    // Процент выигрышей
    winRate: (state) => {
      const total = state.completedBets.length
      if (total === 0) return 0
      return (state.winningBets.length / total) * 100
    },

    // Общий профит
    totalProfit: (state) => {
      return state.betHistory.reduce((sum, bet) => sum + bet.profit, 0)
    },

          // Доступные виды спорта
    availableSports: (state) => {
      const sports = new Set(state.events.map(event => event.sport))
      return Array.from(sports).map(sport => {
        const event = state.events.find(e => e.sport === sport)
        return {
          value: sport,
          label: event?.sport_name || sport,
          category: ['csgo', 'dota2', 'lol', 'valorant', 'pubg', 'apex', 'rainbow'].includes(sport) ? 'esports' : 'traditional'
        }
      })
    },

    // Доступные категории
    availableCategories: () => [
      { value: 'all', label: 'Все виды спорта' },
      { value: 'traditional', label: 'Традиционный спорт' },
      { value: 'esports', label: 'Киберспорт' }
    ],

    // Есть ли ставки в корзине
    hasBetsInSlip: (state) => state.betSlip.length > 0,

    // Минимальная ставка в корзине
    minStake: (state) => Math.min(...state.betSlip.map(bet => bet.amount || 0)),

    // Максимальная ставка в корзине
    maxStake: (state) => Math.max(...state.betSlip.map(bet => bet.amount || 0))
  },

  actions: {
    // Загрузить спортивные события
    async loadEvents() {
      this.loading = true
      this.error = null

      try {
        const [events, liveEvents] = await Promise.all([
          getSportsEvents(),
          getLiveEvents()
        ])

        this.events = events
        this.liveEvents = liveEvents
      } catch (error) {
        this.error = error.message
        console.error('Failed to load events:', error)
      } finally {
        this.loading = false
      }
    },

    // Загрузить ставки пользователя
    async loadUserBets() {
      try {
        const [bets, history, stats] = await Promise.all([
          getUserBets(),
          getBetHistory(),
          getBetStats()
        ])

        this.userBets = bets
        this.betHistory = history
        this.betStats = stats
      } catch (error) {
        console.error('Failed to load user bets:', error)
      }
    },

    // Сделать ставку
    async placeBet(eventId, betType, amount, odds) {
      try {
        const result = await placeBet(eventId, betType, amount, odds)

        if (result.success) {
          // Обновить баланс пользователя
          const userStore = useUserStore()
          userStore.updateBalance(-amount)

          // Добавить ставку в активные
          const newBet = {
            id: result.bet_id,
            event_id: eventId,
            bet_type: betType,
            amount: Number(amount),
            odds: Number(odds),
            potential_win: Number(amount) * Number(odds),
            status: 'active',
            created_at: new Date().toISOString()
          }

          this.userBets.unshift(newBet)

          // Очистить корзину ставок
          this.clearBetSlip()

          return result
        }
      } catch (error) {
        console.error('Failed to place bet:', error)
        throw error
      }
    },

    // Добавить ставку в корзину
    addToBetSlip(event, betType, odds) {
      const existingBet = this.betSlip.find(bet =>
        bet.event_id === event.id && bet.bet_type === betType
      )

      if (existingBet) {
        // Удалить если такая ставка уже есть
        this.removeFromBetSlip(existingBet)
      } else {
        // Добавить новую ставку
        const bet = {
          id: Date.now() + Math.random(),
          event_id: event.id,
          event_name: `${event.home_team} vs ${event.away_team}`,
          sport: event.sport,
          bet_type: betType,
          bet_type_name: this.getBetTypeName(betType),
          odds: Number(odds),
          amount: 0,
          potential_win: 0
        }

        this.betSlip.push(bet)
        this.calculateTotals()
      }
    },

    // Удалить ставку из корзины
    removeFromBetSlip(bet) {
      const index = this.betSlip.findIndex(b => b.id === bet.id)
      if (index > -1) {
        this.betSlip.splice(index, 1)
        this.calculateTotals()
      }
    },

    // Обновить сумму ставки в корзине
    updateBetAmount(betId, amount) {
      const bet = this.betSlip.find(b => b.id === betId)
      if (bet) {
        bet.amount = Number(amount) || 0
        bet.potential_win = bet.amount * bet.odds
        this.calculateTotals()
      }
    },

    // Рассчитать общие суммы
    calculateTotals() {
      this.totalStake = this.betSlip.reduce((sum, bet) => sum + (bet.amount || 0), 0)
      this.potentialWin = this.betSlip.reduce((sum, bet) => sum + (bet.potential_win || 0), 0)
    },

    // Очистить корзину ставок
    clearBetSlip() {
      this.betSlip = []
      this.totalStake = 0
      this.potentialWin = 0
    },

    // Сделать все ставки из корзины
    async placeAllBets() {
      if (this.betSlip.length === 0) return

      const results = []

      for (const bet of this.betSlip) {
        if (bet.amount > 0) {
          try {
            const result = await this.placeBet(bet.event_id, bet.bet_type, bet.amount, bet.odds)
            results.push(result)
          } catch (error) {
            console.error('Failed to place bet from slip:', error)
            results.push({ success: false, error: error.message })
          }
        }
      }

      return results
    },

    // Получить название типа ставки
    getBetTypeName(betType) {
      const betTypes = {
        home: 'П1',
        draw: 'Ничья',
        away: 'П2',
        over_2_5: 'Тотал > 2.5',
        under_2_5: 'Тотал < 2.5',
        over_220_5: 'Тотал > 220.5',
        under_220_5: 'Тотал < 220.5',
        next_goal_home: 'Следующий гол - хозяева',
        next_goal_away: 'Следующий гол - гости',
        both_teams_score_yes: 'Обе забьют - Да',
        both_teams_score_no: 'Обе забьют - Нет'
      }

      return betTypes[betType] || betType
    },

    // Установить фильтр по виду спорта
    setSportFilter(sport) {
      this.selectedSport = sport
    },

    // Установить фильтр по времени
    setTimeframeFilter(timeframe) {
      this.selectedTimeframe = timeframe
    },

    // Установить фильтр по категории
    setCategoryFilter(category) {
      this.selectedCategory = category
      // Сбрасываем фильтр по виду спорта при смене категории
      if (category !== 'all') {
        this.selectedSport = 'all'
      }
    },

    // Обновить статистику ставок
    updateBetStats(stats) {
      this.betStats = stats
    },

    // Добавить ставку в историю (для имитации результатов)
    addBetToHistory(bet) {
      this.betHistory.unshift(bet)

      // Удалить из активных ставок
      const activeIndex = this.userBets.findIndex(b => b.id === bet.id)
      if (activeIndex > -1) {
        this.userBets.splice(activeIndex, 1)
      }
    }
  }
})
