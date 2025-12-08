<template>
  <div v-if="showInstall" class="fixed bottom-4 left-4 right-4 z-40">
    <div class="bg-gradient-to-br from-violet/90 to-purple/90 backdrop-blur-sm rounded-2xl p-4 shadow-lg border border-violet/20">
      <div class="flex items-center justify-between mb-3">
        <div class="flex items-center space-x-3">
          <div class="w-10 h-10 bg-violet/20 rounded-xl flex items-center justify-center">
            <svg class="w-6 h-6 text-violet" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
            </svg>
          </div>
          <div>
            <h4 class="text-white font-semibold">Установить приложение</h4>
            <p class="text-xs text-grayLight">Быстрый доступ к TREASURE Casino</p>
          </div>
        </div>
        <button
          @click="dismiss"
          class="w-6 h-6 text-gray hover:text-white transition-colors"
        >
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>

      <div class="flex space-x-2">
        <button
          @click="install"
          class="flex-1 py-3 bg-white/20 hover:bg-white/30 rounded-xl text-white font-semibold transition-all duration-200"
        >
          Установить
        </button>
        <button
          @click="dismiss"
          class="px-4 py-3 bg-gray/20 hover:bg-gray/30 rounded-xl text-grayLight font-medium transition-colors"
        >
          Позже
        </button>
      </div>

      <div class="mt-3 text-xs text-grayLight text-center">
        Установка занимает менее минуты
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import pwaService from '../services/pwa'

export default {
  name: 'PWAInstall',
  setup() {
    const showInstall = ref(false)
    const dismissed = ref(false)

    const pwaStatus = computed(() => pwaService.getStatus())

    const shouldShowInstall = computed(() => {
      return pwaStatus.value.isInstallable &&
             !pwaStatus.value.isInstalled &&
             !dismissed.value &&
             localStorage.getItem('pwa-install-dismissed') !== 'true'
    })

    const install = async () => {
      await pwaService.installApp()
      showInstall.value = false
    }

    const dismiss = () => {
      dismissed.value = true
      localStorage.setItem('pwa-install-dismissed', 'true')
      showInstall.value = false
    }

    // Показывать через 30 секунд использования
    onMounted(() => {
      setTimeout(() => {
        if (shouldShowInstall.value) {
          showInstall.value = true
        }
      }, 30000)
    })

    return {
      showInstall,
      install,
      dismiss
    }
  }
}
</script>
