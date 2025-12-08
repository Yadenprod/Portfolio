<template>
  <header class="h-16 flex items-center justify-between px-4 bg-azot-gradient dark:bg-industrial-900 border-b border-industrial-200 dark:border-industrial-700 shadow-glow-azot rounded-wow animate-fade-in">
    <div class="flex items-center gap-2 md:hidden">
      <button 
        @click="$emit('toggleSidebar')" 
        class="p-2 rounded-industrial-md text-industrial-500 dark:text-industrial-300 hover:bg-white/40 dark:hover:bg-industrial-800/60 focus:outline-none shadow-industrial-soft"
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
          <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
        </svg>
      </button>
    </div>
    <div class="flex-1 flex items-center gap-4">
      <span class="text-lg font-semibold text-industrial-800 dark:text-industrial-200 uppercase tracking-wide drop-shadow-lg">
        Система мониторинга АЗОТ
      </span>
    </div>
    <div class="flex items-center gap-4">
      <button 
        @click="$emit('toggleTheme')" 
        class="p-2 rounded-industrial-md text-industrial-500 dark:text-industrial-300 hover:bg-white/40 dark:hover:bg-industrial-800/60 focus:outline-none shadow-industrial-soft"
      >
        <svg v-if="theme === 'dark'" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 3v1.5m0 15V21m8.485-8.485h-1.5m-15 0H3m15.364-6.364l-1.06 1.06m-12.728 0l-1.06-1.06m12.728 12.728l-1.06-1.06m-12.728 0l-1.06 1.06" />
        </svg>
        <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
          <path stroke-linecap="round" stroke-linejoin="round" d="M21.752 15.002A9.718 9.718 0 0112 21.75c-5.385 0-9.75-4.365-9.75-9.75 0-4.502 3.003-8.29 7.25-9.418" />
        </svg>
      </button>
      <div class="relative">
        <button 
          @click="profileOpen = !profileOpen" 
          class="flex items-center gap-2 p-2 rounded-industrial-md text-industrial-700 dark:text-industrial-200 hover:bg-white/40 dark:hover:bg-industrial-800/60 focus:outline-none shadow-industrial-soft"
        >
          <div class="flex items-center gap-3">
            <img 
              :src="user.avatar" 
              alt="User Avatar" 
              class="w-9 h-9 rounded-full border-2 border-azot-200 dark:border-industrial-700 object-cover shadow-glow-azot"
            >
            <div class="text-left">
              <p class="text-sm font-semibold text-industrial-800 dark:text-industrial-200">{{ user.name }}</p>
              <p class="text-xs text-industrial-500 dark:text-industrial-400">{{ user.role }}</p>
            </div>
          </div>
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5 text-industrial-500 dark:text-industrial-300">
            <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 8.25l-7.5 7.5-7.5-7.5" />
          </svg>
        </button>
        <div 
          v-if="profileOpen" 
          class="absolute right-0 mt-2 w-64 bg-white/95 dark:bg-industrial-900/95 border border-industrial-200 dark:border-industrial-700 rounded-wow shadow-glow-industrial z-50 animate-wow-bounce"
        >
          <div class="p-4 border-b border-industrial-200 dark:border-industrial-700 flex items-center gap-3 bg-azot-gradient bg-clip-text text-transparent">
            <img 
              :src="user.avatar" 
              alt="User Avatar" 
              class="w-12 h-12 rounded-full border-2 border-azot-200 dark:border-industrial-700 object-cover shadow-glow-azot"
            >
            <div>
              <p class="text-sm font-semibold text-industrial-800 dark:text-industrial-200">{{ user.name }}</p>
              <p class="text-xs text-industrial-500 dark:text-industrial-400">{{ user.email }}</p>
            </div>
          </div>
          <div class="py-1">
            <router-link 
              to="/profile" 
              class="block px-4 py-2 text-sm text-industrial-700 dark:text-industrial-200 hover:bg-white/40 dark:hover:bg-industrial-800/60"
            >
              <UserCircleIcon class="w-5 h-5 inline-block mr-2 -mt-1 text-industrial-500 dark:text-industrial-300" />
              Профиль
            </router-link>
            <router-link 
              to="/settings" 
              class="block px-4 py-2 text-sm text-industrial-700 dark:text-industrial-200 hover:bg-white/40 dark:hover:bg-industrial-800/60"
            >
              <CogIcon class="w-5 h-5 inline-block mr-2 -mt-1 text-industrial-500 dark:text-industrial-300" />
              Настройки
            </router-link>
          </div>
          <div class="border-t border-industrial-200 dark:border-industrial-700 py-1">
            <button 
              @click="$emit('logout')" 
              class="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 dark:hover:bg-red-900"
            >
              <ArrowLeftStartOnRectangleIcon class="w-5 h-5 inline-block mr-2 -mt-1 text-red-500" />
              Выйти
            </button>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, watch, defineProps } from 'vue'
import { 
  UserCircleIcon, 
  CogIcon, 
  ArrowLeftStartOnRectangleIcon 
} from '@heroicons/vue/24/outline'

const props = defineProps({ 
  theme: String,
  user: {
    type: Object,
    default: () => ({
      name: 'Иван Петров',
      email: 'ivan.petrov@azot.ru',
      role: 'Инженер',
      avatar: '/default-avatar.png'
    })
  }
})

const profileOpen = ref(false)
</script>

<style scoped>
.router-link-active {
  background-color: #e6f2ff; /* Используем прямое значение цвета azot.50 */
}
</style>
