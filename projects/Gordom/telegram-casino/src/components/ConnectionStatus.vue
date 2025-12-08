<template>
  <div v-if="showStatus" class="fixed top-16 right-4 z-40">
    <div
      class="bg-gradient-to-br from-[#202024] to-[#2c2c31] rounded-xl p-4 border shadow-lg min-w-[200px]"
      :class="statusBorderClass"
    >
      <div class="flex items-center space-x-3 mb-3">
        <div
          class="w-3 h-3 rounded-full animate-pulse"
          :class="statusColorClass"
        ></div>
        <div class="text-white font-semibold text-sm">Статус соединения</div>
      </div>

      <div class="space-y-2 text-xs text-grayLight">
        <div class="flex justify-between">
          <span>Статус:</span>
          <span :class="statusColorClass">{{ statusText }}</span>
        </div>
        <div class="flex justify-between">
          <span>Онлайн:</span>
          <span class="text-white">{{ onlineCount }}</span>
        </div>
        <div v-if="reconnectAttempts > 0" class="flex justify-between">
          <span>Попыток:</span>
          <span class="text-orange">{{ reconnectAttempts }}</span>
        </div>
        <div v-if="pendingMessages > 0" class="flex justify-between">
          <span>Ожидают:</span>
          <span class="text-yellow">{{ pendingMessages }}</span>
        </div>
      </div>

      <button
        @click="toggleStatus"
        class="w-full mt-3 py-2 text-xs text-gray hover:text-white transition-colors"
      >
        Скрыть
      </button>
    </div>
  </div>

  <!-- Кнопка показа статуса -->
  <button
    v-else
    @click="toggleStatus"
    class="fixed top-16 right-4 z-40 w-12 h-12 bg-violet hover:bg-violetHover rounded-full shadow-lg flex items-center justify-center transition-all duration-300"
    :class="statusButtonClass"
  >
    <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
    </svg>
  </button>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import wsService from '../services/websocket'

export default {
  name: 'ConnectionStatus',
  setup() {
    const showStatus = ref(false)

    const status = computed(() => wsService.getStatus())

    const onlineCount = ref(0)
    const reconnectAttempts = computed(() => status.value.reconnectAttempts)
    const pendingMessages = computed(() => status.value.pendingMessages)

    const statusText = computed(() => {
      if (status.value.isConnected) return 'Подключено'
      if (reconnectAttempts.value > 0) return 'Переподключение...'
      return 'Отключено'
    })

    const statusColorClass = computed(() => {
      if (status.value.isConnected) return 'bg-green'
      if (reconnectAttempts.value > 0) return 'bg-orange'
      return 'bg-red'
    })

    const statusBorderClass = computed(() => {
      if (status.value.isConnected) return 'border-green/20'
      if (reconnectAttempts.value > 0) return 'border-orange/20'
      return 'border-red/20'
    })

    const statusButtonClass = computed(() => {
      if (status.value.isConnected) return 'animate-pulse'
      return 'animate-bounce'
    })

    const toggleStatus = () => {
      showStatus.value = !showStatus.value
    }

    // Обновление количества онлайн пользователей
    const updateOnlineCount = (payload) => {
      onlineCount.value = payload.count || 0
    }

    onMounted(() => {
      wsService.on('online_users', updateOnlineCount)
    })

    onUnmounted(() => {
      wsService.off('online_users', updateOnlineCount)
    })

    return {
      showStatus,
      status,
      onlineCount,
      reconnectAttempts,
      pendingMessages,
      statusText,
      statusColorClass,
      statusBorderClass,
      statusButtonClass,
      toggleStatus
    }
  }
}
</script>
