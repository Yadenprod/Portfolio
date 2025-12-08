<template>
  <div class="analytics-container">
    <div class="text-center">
      <h1 class="font-deftone text-3xl text-white mb-2">
        <span class="text-violet">АНАЛИТИКА</span>
      </h1>
      <p class="text-grayLight text-sm">Статистика и аналитика вашего игрового процесса</p>
    </div>

    <!-- Общая статистика -->
    <div class="bg-gradient-to-br from-[#202024] to-[#2c2c31] rounded-2xl p-6">
      <h3 class="text-white font-semibold text-lg mb-4">Общая статистика</h3>
      <div class="grid grid-cols-2 gap-4">
        <div class="text-center">
          <div class="text-2xl font-bold text-green mb-1">{{ sessionStats.eventsCount || 0 }}</div>
          <div class="text-xs text-gray">Событий в сессии</div>
        </div>
        <div class="text-center">
          <div class="text-2xl font-bold text-blue mb-1">{{ formatTime(sessionStats.sessionDuration || 0) }}</div>
          <div class="text-xs text-gray">Время сессии</div>
        </div>
        <div class="text-center">
          <div class="text-2xl font-bold text-orange mb-1">{{ totalGames || 0 }}</div>
          <div class="text-xs text-gray">Всего игр</div>
        </div>
        <div class="text-center">
          <div class="text-2xl font-bold text-purple mb-1">{{ winRate || 0 }}%</div>
          <div class="text-xs text-gray">Процент побед</div>
        </div>
      </div>
    </div>

    <!-- Игровая активность -->
    <div class="bg-gradient-to-br from-[#202024] to-[#2c2c31] rounded-2xl p-6">
      <h3 class="text-white font-semibold text-lg mb-4">Игровая активность</h3>
      <div class="space-y-3">
        <div class="flex justify-between items-center">
          <span class="text-grayLight">Dice</span>
          <div class="flex items-center space-x-2">
            <span class="text-white">{{ gameStats.dice?.plays || 0 }}</span>
            <span class="text-green">{{ gameStats.dice?.wins || 0 }}W</span>
          </div>
        </div>
        <div class="flex justify-between items-center">
          <span class="text-grayLight">Wheel</span>
          <div class="flex items-center space-x-2">
            <span class="text-white">{{ gameStats.wheel?.plays || 0 }}</span>
            <span class="text-green">{{ gameStats.wheel?.wins || 0 }}W</span>
          </div>
        </div>
        <div class="flex justify-between items-center">
          <span class="text-grayLight">Mines</span>
          <div class="flex items-center space-x-2">
            <span class="text-white">{{ gameStats.mines?.plays || 0 }}</span>
            <span class="text-green">{{ gameStats.mines?.wins || 0 }}W</span>
          </div>
        </div>
        <div class="flex justify-between items-center">
          <span class="text-grayLight">Slots</span>
          <div class="flex items-center space-x-2">
            <span class="text-white">{{ gameStats.slots?.plays || 0 }}</span>
            <span class="text-green">{{ gameStats.slots?.wins || 0 }}W</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Финансовая статистика -->
    <div class="bg-gradient-to-br from-[#202024] to-[#2c2c31] rounded-2xl p-6">
      <h3 class="text-white font-semibold text-lg mb-4">Финансовая статистика</h3>
      <div class="grid grid-cols-2 gap-4">
        <div class="text-center">
          <div class="text-2xl font-bold text-green mb-1">+{{ totalWinnings || 0 }}₽</div>
          <div class="text-xs text-gray">Общий выигрыш</div>
        </div>
        <div class="text-center">
          <div class="text-2xl font-bold text-red mb-1">-{{ totalLosses || 0 }}₽</div>
          <div class="text-xs text-gray">Общий проигрыш</div>
        </div>
        <div class="text-center">
          <div class="text-2xl font-bold text-blue mb-1">{{ netProfit || 0 }}₽</div>
          <div class="text-xs text-gray">Чистая прибыль</div>
        </div>
        <div class="text-center">
          <div class="text-2xl font-bold text-purple mb-1">{{ roi || 0 }}%</div>
          <div class="text-xs text-gray">ROI</div>
        </div>
      </div>
    </div>

    <!-- График активности -->
    <div class="bg-gradient-to-br from-[#202024] to-[#2c2c31] rounded-2xl p-6">
      <h3 class="text-white font-semibold text-lg mb-4">Активность по дням</h3>
      <div class="space-y-2">
        <div
          v-for="day in activityChart"
          :key="day.date"
          class="flex items-center justify-between"
        >
          <span class="text-grayLight text-sm">{{ formatDate(day.date) }}</span>
          <div class="flex items-center space-x-2">
            <div class="w-16 h-2 bg-gray/20 rounded-full overflow-hidden">
              <div
                class="h-full bg-violet rounded-full transition-all duration-300"
                :style="{ width: `${Math.min(day.activity / 10, 100)}%` }"
              ></div>
            </div>
            <span class="text-white text-sm w-8 text-right">{{ day.activity }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Топ действий -->
    <div class="bg-gradient-to-br from-[#202024] to-[#2c2c31] rounded-2xl p-6">
      <h3 class="text-white font-semibold text-lg mb-4">Частые действия</h3>
      <div class="space-y-3">
        <div
          v-for="action in topActions"
          :key="action.name"
          class="flex items-center justify-between"
        >
          <span class="text-grayLight">{{ action.name }}</span>
          <div class="flex items-center space-x-2">
            <div class="w-12 h-2 bg-gray/20 rounded-full overflow-hidden">
              <div
                class="h-full bg-green rounded-full transition-all duration-300"
                :style="{ width: `${Math.min(action.count / 5, 100)}%` }"
              ></div>
            </div>
            <span class="text-white text-sm w-6 text-right">{{ action.count }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Производительность -->
    <div class="bg-gradient-to-br from-[#202024] to-[#2c2c31] rounded-2xl p-6">
      <h3 class="text-white font-semibold text-lg mb-4">Производительность</h3>
      <div class="space-y-3">
        <div class="flex justify-between items-center">
          <span class="text-grayLight">Время загрузки</span>
          <span class="text-white">{{ pageLoadTime || 0 }}ms</span>
        </div>
        <div class="flex justify-between items-center">
          <span class="text-grayLight">LCP (основной контент)</span>
          <span class="text-white">{{ lcpTime || 0 }}ms</span>
        </div>
        <div class="flex justify-between items-center">
          <span class="text-grayLight">FID (взаимодействие)</span>
          <span class="text-white">{{ fidTime || 0 }}ms</span>
        </div>
        <div class="flex justify-between items-center">
          <span class="text-grayLight">Использование памяти</span>
          <span class="text-white">{{ memoryUsage || 0 }}MB</span>
        </div>
      </div>
    </div>

    <!-- Отладочная информация -->
    <div v-if="debugMode" class="bg-gradient-to-br from-[#202024] to-[#2c2c31] rounded-2xl p-6">
      <h3 class="text-white font-semibold text-lg mb-4">Отладочная информация</h3>
      <div class="space-y-2 text-xs text-grayLight">
        <div><strong>Session ID:</strong> {{ sessionStats.sessionId }}</div>
        <div><strong>User ID:</strong> {{ sessionStats.userId || 'Guest' }}</div>
        <div><strong>Pending Events:</strong> {{ sessionStats.pendingEvents || 0 }}</div>
        <div><strong>Network Status:</strong> {{ networkStatus }}</div>
        <div><strong>WebSocket:</strong> {{ wsStatus }}</div>
      </div>

      <div class="mt-4 space-x-2">
        <button
          @click="exportDebugData"
          class="px-3 py-2 bg-violet rounded-lg text-white text-sm hover:bg-violetHover transition-colors"
        >
          Экспорт данных
        </button>
        <button
          @click="clearAnalytics"
          class="px-3 py-2 bg-red/20 rounded-lg text-red text-sm hover:bg-red/30 transition-colors"
        >
          Очистить
        </button>
      </div>
    </div>

    <!-- Кнопка включения отладки -->
    <button
      @click="debugMode = !debugMode"
      class="fixed bottom-4 right-4 w-12 h-12 bg-violet hover:bg-violetHover rounded-full shadow-lg flex items-center justify-center transition-all duration-300"
    >
      <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
      </svg>
    </button>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '../stores/user'
import analyticsService, { analytics } from '../services/analytics'
import wsService from '../services/websocket'

export default {
  name: 'Analytics',
  setup() {
    const userStore = useUserStore()
    const debugMode = ref(false)

    // Данные аналитики
    const sessionStats = ref({})
    const gameStats = ref({})
    const activityChart = ref([])
    const topActions = ref([])
    const performanceMetrics = ref({})

    // Вычисляемые значения
    const totalGames = computed(() => userStore.totalGames || 0)
    const winRate = computed(() => userStore.winRate || 0)
    const totalWinnings = computed(() => userStore.totalWinnings || 0)
    const totalLosses = computed(() => 0) // Нужно будет рассчитать из истории игр
    const netProfit = computed(() => totalWinnings.value - totalLosses.value)
    const roi = computed(() => totalLosses.value > 0 ? ((netProfit.value / totalLosses.value) * 100).toFixed(1) : 0)

    const pageLoadTime = computed(() => performanceMetrics.value.pageLoad || 0)
    const lcpTime = computed(() => performanceMetrics.value.lcp || 0)
    const fidTime = computed(() => performanceMetrics.value.fid || 0)
    const memoryUsage = computed(() => performanceMetrics.value.memory || 0)

    const networkStatus = computed(() => {
      const status = navigator.onLine ? 'Online' : 'Offline'
      const connection = navigator.connection?.effectiveType || 'unknown'
      return `${status} (${connection})`
    })

    const wsStatus = computed(() => wsService.getStatus().isConnected ? 'Connected' : 'Disconnected')

    const formatTime = (ms) => {
      const seconds = Math.floor(ms / 1000)
      const minutes = Math.floor(seconds / 60)
      const hours = Math.floor(minutes / 60)

      if (hours > 0) return `${hours}ч ${minutes % 60}м`
      if (minutes > 0) return `${minutes}м ${seconds % 60}с`
      return `${seconds}с`
    }

    const formatDate = (dateString) => {
      const date = new Date(dateString)
      return date.toLocaleDateString('ru-RU', { weekday: 'short', day: 'numeric' })
    }

    const exportDebugData = () => {
      const data = analytics.exportDebugData()
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `analytics-debug-${Date.now()}.json`
      a.click()
      URL.revokeObjectURL(url)
    }

    const clearAnalytics = () => {
      if (confirm('Вы уверены, что хотите очистить все аналитические данные?')) {
        analyticsService.clear()
        updateData()
      }
    }

    const updateData = () => {
      sessionStats.value = analytics.getSessionStats()

      // Имитация данных (в реальном приложении они будут приходить из API)
      gameStats.value = {
        dice: { plays: 25, wins: 12 },
        wheel: { plays: 18, wins: 8 },
        mines: { plays: 15, wins: 6 },
        slots: { plays: 22, wins: 4 }
      }

      activityChart.value = Array.from({ length: 7 }, (_, i) => {
        const date = new Date()
        date.setDate(date.getDate() - i)
        return {
          date: date.toISOString().split('T')[0],
          activity: Math.floor(Math.random() * 20) + 5
        }
      }).reverse()

      topActions.value = [
        { name: 'Ставки', count: 45 },
        { name: 'Игры', count: 32 },
        { name: 'Бонусы', count: 18 },
        { name: 'Чат', count: 12 }
      ]

      // Метрики производительности
      performanceMetrics.value = {
        pageLoad: 1250,
        lcp: 1800,
        fid: 45,
        memory: 25
      }
    }

    onMounted(() => {
      updateData()

      // Отслеживаем просмотр страницы аналитики
      analytics.trackEvent('analytics_page_view')
    })

    return {
      debugMode,
      sessionStats,
      gameStats,
      activityChart,
      topActions,
      performanceMetrics,
      totalGames,
      winRate,
      totalWinnings,
      totalLosses,
      netProfit,
      roi,
      pageLoadTime,
      lcpTime,
      fidTime,
      memoryUsage,
      networkStatus,
      wsStatus,
      formatTime,
      formatDate,
      exportDebugData,
      clearAnalytics
    }
  }
}
</script>
