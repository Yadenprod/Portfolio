<template>
  <div 
    class="fixed top-4 right-4 z-[100] flex flex-col space-y-4 w-96 animate-fade-in"
  >
    <TransitionGroup 
      enter-active-class="transition duration-500 ease-out animate-slide-right"
      enter-from-class="transform translate-x-full opacity-0"
      enter-to-class="transform translate-x-0 opacity-100"
      leave-active-class="transition duration-300 ease-in absolute"
      leave-from-class="opacity-100"
      leave-to-class="transform translate-x-full opacity-0"
      tag="div"
    >
      <div 
        v-for="toast in toasts" 
        :key="toast.id"
        :class="[
          'p-4 rounded-wow shadow-glow-azot border-l-4 relative overflow-hidden',
          typeClasses[toast.type],
          'bg-azot-gradient text-white',
          'animate-slide-right'
        ]"
      >
        <div class="flex items-start space-x-3">
          <div class="flex-shrink-0">
            <component 
              :is="iconMap[toast.type]" 
              class="w-6 h-6"
            />
          </div>
          <div class="flex-1">
            <h3 class="text-sm font-semibold">{{ toast.title }}</h3>
            <p class="text-xs text-white/80 mt-1">
              {{ toast.message }}
            </p>
          </div>
          <button 
            @click="removeToast(toast.id)"
            class="text-white/60 hover:text-white transition"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div 
          v-if="toast.duration" 
          class="absolute bottom-0 left-0 h-1 bg-chemical-500 rounded-full shadow-glow-chemical"
          :style="{
            width: `${(timeLeft[toast.id] / toast.duration) * 100}%`,
            transition: 'width 0.1s linear'
          }"
        ></div>
      </div>
    </TransitionGroup>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { 
  InformationCircleIcon, 
  CheckCircleIcon, 
  ExclamationTriangleIcon, 
  XCircleIcon 
} from '@heroicons/vue/24/outline'

const toasts = ref([])
const timeLeft = ref({})
const timers = ref({})

const iconMap = {
  info: InformationCircleIcon,
  success: CheckCircleIcon,
  warning: ExclamationTriangleIcon,
  error: XCircleIcon
}

const typeClasses = {
  info: 'bg-blue-50 dark:bg-blue-900 border-blue-500 text-blue-900 dark:text-blue-200',
  success: 'bg-green-50 dark:bg-green-900 border-green-500 text-green-900 dark:text-green-200',
  warning: 'bg-yellow-50 dark:bg-yellow-900 border-yellow-500 text-yellow-900 dark:text-yellow-200',
  error: 'bg-red-50 dark:bg-red-900 border-red-500 text-red-900 dark:text-red-200'
}

const addToast = (toast) => {
  const id = Date.now()
  const defaultToast = { 
    id, 
    type: 'info', 
    title: '', 
    message: '', 
    duration: 5000 
  }
  const newToast = { ...defaultToast, ...toast }
  
  toasts.value.push(newToast)
  timeLeft.value[id] = newToast.duration

  timers.value[id] = setInterval(() => {
    timeLeft.value[id] -= 100
    if (timeLeft.value[id] <= 0) {
      removeToast(id)
    }
  }, 100)
}

const removeToast = (id) => {
  clearInterval(timers.value[id])
  toasts.value = toasts.value.filter(t => t.id !== id)
  delete timeLeft.value[id]
  delete timers.value[id]
}

// Expose methods for global usage
const toast = {
  info: (message, title = '') => addToast({ type: 'info', message, title }),
  success: (message, title = '') => addToast({ type: 'success', message, title }),
  warning: (message, title = '') => addToast({ type: 'warning', message, title }),
  error: (message, title = '') => addToast({ type: 'error', message, title })
}

// Глобальная регистрация toast
onMounted(() => {
  window.$toast = toast
})

onUnmounted(() => {
  Object.values(timers.value).forEach(clearInterval)
})

defineExpose({ addToast, removeToast, toast })
</script>

<style scoped>
.v-enter-active,
.v-leave-active {
  transition: all 0.3s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
  transform: translateX(100%);
}
</style>
