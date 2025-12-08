import { defineStore } from 'pinia'
import { getMe } from '../api/endpoints'
import { initTelegram } from '../telegram'

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null,
    balance: 1000,
    loading: false,
    referralCode: null,
    achievements: [],
    rank: 0,
    totalGames: 0,
    winRate: 0,
    totalWinnings: 0,
  }),
  getters: {
    formattedBalance: (state) => `${state.balance.toFixed(2)}₽`,
    isAuth: (state) => Boolean(state.user),
    formattedWinRate: (state) => `${(state.winRate * 100).toFixed(1)}%`,
    formattedRank: (state) => `#${state.rank}`,
  },
  actions: {
    async initFromTelegram() {
      const tg = initTelegram()
      // read start_param (referrals)
      const startParam = tg?.initDataUnsafe?.start_param
      if (startParam) {
        this.referralCode = startParam
        localStorage.setItem('ref', startParam)
      }

      if (!tg?.initData) return
      try {
        this.loading = true
        const data = await getMe()
        this.user = data?.user || null
        if (typeof data?.balance === 'number') this.balance = data.balance
        if (data?.rank) this.rank = data.rank
        if (data?.totalGames) this.totalGames = data.totalGames
        if (data?.winRate) this.winRate = data.winRate
        if (data?.totalWinnings) this.totalWinnings = data.totalWinnings
      } catch (e) {
        console.error('Failed to initialize user:', e)
        // fallback to guest
      } finally {
        this.loading = false
      }
    },

    async fetchProfile() {
      try {
        this.loading = true
        const data = await getMe()
        this.user = data?.user || this.user
        if (typeof data?.balance === 'number') this.balance = data.balance
        if (data?.rank) this.rank = data.rank
        if (data?.totalGames) this.totalGames = data.totalGames
        if (data?.winRate) this.winRate = data.winRate
        if (data?.totalWinnings) this.totalWinnings = data.totalWinnings
      } finally {
        this.loading = false
      }
    },

    updateBalance(delta) {
      const next = this.balance + Number(delta || 0)
      this.balance = Math.max(0, next)
    },

    setUserStats(stats) {
      if (stats.rank) this.rank = stats.rank
      if (stats.totalGames) this.totalGames = stats.totalGames
      if (stats.winRate) this.winRate = stats.winRate
      if (stats.totalWinnings) this.totalWinnings = stats.totalWinnings
    },

    addAchievement(achievement) {
      this.achievements.unshift(achievement)
      if (this.achievements.length > 10) {
        this.achievements = this.achievements.slice(0, 10)
      }
    },
  }
})
