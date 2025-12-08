<template>
  <div
    v-if="isVisible"
    class="fixed bottom-4 left-4 right-4 z-50 bg-gradient-to-r from-orange/90 to-amber/90 backdrop-blur-md rounded-lg border border-orange/30 shadow-lg p-3"
  >
    <div class="flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <div class="w-8 h-8 bg-orange/20 rounded-full flex items-center justify-center">
          <span class="text-orange text-sm">🔄</span>
        </div>
        <div>
          <p class="text-white text-sm font-medium">Автономный режим</p>
          <p class="text-orange/80 text-xs">Приложение работает без подключения к серверу</p>
        </div>
      </div>
      <button
        @click="hide"
        class="w-6 h-6 bg-orange/20 rounded-full flex items-center justify-center hover:bg-orange/30 transition-colors"
      >
        <span class="text-white text-xs">×</span>
      </button>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { isStandaloneMode } from '../services/standalone'

export default {
  name: 'StandaloneIndicator',
  setup() {
    const isVisible = ref(false)

    const hide = () => {
      isVisible.value = false
      localStorage.setItem('standalone_indicator_hidden', 'true')
    }

    onMounted(() => {
      if (isStandaloneMode()) {
        const hidden = localStorage.getItem('standalone_indicator_hidden')
        if (!hidden) {
          // Показываем индикатор через 3 секунды после загрузки
          setTimeout(() => {
            isVisible.value = true
          }, 3000)

          // Автоматически скрываем через 10 секунд
          setTimeout(() => {
            if (isVisible.value) {
              hide()
            }
          }, 13000)
        }
      }
    })

    return {
      isVisible,
      hide
    }
  }
}
</script>
