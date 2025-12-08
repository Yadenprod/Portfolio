<template>
  <div class="flex flex-col space-y-6">
    <div class="text-center">
      <h1 class="font-deftone text-3xl text-white mb-2">
        <span class="text-violet">РЕЙТИНГ</span>
      </h1>
      <p class="text-grayLight text-sm">Топ игроков казино</p>
    </div>

    <!-- Статистика текущего пользователя -->
    <div v-if="userStats" class="bg-gradient-to-br from-[#202024] to-[#2c2c31] rounded-2xl p-6 space-y-4">
      <h3 class="text-white font-semibold text-lg mb-4">Ваша статистика</h3>
      <div class="grid grid-cols-4 gap-4">
        <div class="text-center">
          <div class="text-2xl font-bold text-violet mb-1">{{ userStats.rank }}</div>
          <div class="text-xs text-gray">Место</div>
        </div>
        <div class="text-center">
          <div class="text-2xl font-bold text-green mb-1">{{ userStats.totalGames }}</div>
          <div class="text-xs text-gray">Игр</div>
        </div>
        <div class="text-center">
          <div class="text-2xl font-bold text-blue mb-1">{{ userStats.winRate }}%</div>
          <div class="text-xs text-gray">Побед</div>
        </div>
        <div class="text-center">
          <div class="text-2xl font-bold text-orange mb-1">{{ userStats.totalWinnings }}</div>
          <div class="text-xs text-gray">Выигрыш</div>
        </div>
      </div>
    </div>

    <!-- Фильтры -->
    <div class="flex justify-center">
      <div class="bg-[#2c2c31] rounded-xl p-1 flex">
        <button
          v-for="filter in filters"
          :key="filter.key"
          @click="activeFilter = filter.key"
          class="px-4 py-2 rounded-lg text-sm font-medium transition-colors"
          :class="activeFilter === filter.key ? 'bg-violet text-white' : 'text-grayLight hover:text-white'"
        >
          {{ filter.name }}
        </button>
      </div>
    </div>

    <!-- Список лидеров -->
    <div class="space-y-3">
      <div
        v-for="(player, index) in filteredPlayers"
        :key="player.id"
        class="bg-gradient-to-br from-[#202024] to-[#2c2c31] rounded-xl p-4 flex items-center space-x-4 hover:scale-105 transition-transform duration-200"
        :class="{
          'ring-2 ring-violet': player.isCurrentUser,
          'ring-2 ring-yellow-400': index === 0,
          'ring-2 ring-gray-400': index === 1,
          'ring-2 ring-orange-400': index === 2
        }"
      >
        <!-- Место -->
        <div class="flex-shrink-0">
          <div
            class="w-10 h-10 rounded-full flex items-center justify-center text-white font-bold text-sm"
            :class="{
              'bg-yellow-500': index === 0,
              'bg-gray-400': index === 1,
              'bg-orange-400': index === 2,
              'bg-violet': index > 2 && player.isCurrentUser,
              'bg-[#1b1c20]': index > 2 && !player.isCurrentUser
            }"
          >
            {{ index + 1 }}
          </div>
        </div>

        <!-- Аватар и имя -->
        <div class="flex items-center space-x-3 flex-1">
          <div class="w-12 h-12 bg-gradient-to-br from-violet/20 to-purple/20 rounded-full flex items-center justify-center">
            <svg class="w-6 h-6 text-violet" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
            </svg>
          </div>
          <div>
            <div class="text-white font-semibold">{{ player.name }}</div>
            <div class="text-xs text-grayLight">{{ player.winRate }}% побед</div>
          </div>
        </div>

        <!-- Статистика -->
        <div class="text-right">
          <div class="text-white font-bold">{{ player.balance }}₽</div>
          <div class="text-xs text-grayLight">{{ player.totalGames }} игр</div>
        </div>
      </div>
    </div>

    <!-- Загрузка -->
    <div v-if="loading" class="flex justify-center py-8">
      <div class="w-8 h-8 border-4 border-violet border-t-transparent rounded-full animate-spin"></div>
    </div>

    <!-- Пустое состояние -->
    <div v-if="!loading && filteredPlayers.length === 0" class="text-center py-8">
      <div class="text-6xl mb-4">🏆</div>
      <p class="text-grayLight">Пока нет данных для отображения</p>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '../stores/user'
import { getLeaderboard } from '../api/endpoints'

export default {
  name: 'Leaderboard',
  setup() {
    const userStore = useUserStore()
    const players = ref([])
    const loading = ref(false)
    const activeFilter = ref('balance')

    const filters = [
      { key: 'balance', name: 'Баланс' },
      { key: 'games', name: 'Игры' },
      { key: 'winrate', name: 'Победы' },
      { key: 'winnings', name: 'Выигрыш' }
    ]

    const userStats = computed(() => {
      if (!userStore.user) return null
      return {
        rank: userStore.formattedRank,
        totalGames: userStore.totalGames,
        winRate: userStore.formattedWinRate,
        totalWinnings: userStore.totalWinnings
      }
    })

    const filteredPlayers = computed(() => {
      const sorted = [...players.value].sort((a, b) => {
        switch (activeFilter.value) {
          case 'balance':
            return b.balance - a.balance
          case 'games':
            return b.totalGames - a.totalGames
          case 'winrate':
            return b.winRate - a.winRate
          case 'winnings':
            return b.totalWinnings - a.totalWinnings
          default:
            return 0
        }
      })

      return sorted.map((player, index) => ({
        ...player,
        isCurrentUser: player.id === userStore.user?.id
      }))
    })

    const loadLeaderboard = async () => {
      try {
        loading.value = true
        const data = await getLeaderboard(50)
        players.value = data.map(player => ({
          id: player.id,
          name: player.name,
          balance: player.balance,
          totalGames: player.total_games || 0,
          winRate: player.win_rate || 0,
          totalWinnings: player.total_winnings || 0
        }))
      } catch (error) {
        console.error('Failed to load leaderboard:', error)
        // Fallback data
        players.value = Array.from({ length: 20 }).map((_, i) => ({
          id: i + 1,
          name: `Игрок ${i + 1}`,
          balance: Math.floor(Math.random() * 100000) + 1000,
          totalGames: Math.floor(Math.random() * 1000) + 10,
          winRate: Math.floor(Math.random() * 100),
          totalWinnings: Math.floor(Math.random() * 50000) + 1000
        }))
      } finally {
        loading.value = false
      }
    }

    onMounted(() => {
      loadLeaderboard()
    })

    return {
      players,
      loading,
      activeFilter,
      filters,
      userStats,
      filteredPlayers
    }
  }
}
</script>
