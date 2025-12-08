<template>
  <div id="app" class="tg-app min-h-screen">
    <!-- Лоадер при инициализации -->
    <div v-if="isLoading" class="fixed inset-0 z-50 flex items-center justify-center bg-gradient-to-br from-[#202024] to-[#2c2c31]">
      <div class="flex flex-col items-center space-y-6">
        <div class="relative">
          <div class="w-20 h-20 bg-gradient-to-br from-violet/20 to-purple/20 rounded-2xl flex items-center justify-center animate-pulse">
            <span class="text-3xl">🎰</span>
          </div>
          <!-- Декоративные элементы -->
          <div class="absolute -top-2 -right-2 text-lg animate-bounce">✨</div>
          <div class="absolute -bottom-2 -left-2 text-lg animate-ping">💫</div>
        </div>
        <div class="flex flex-col items-center space-y-2">
          <p class="text-grayLight text-lg font-semibold">TREASURE Casino</p>
          <p class="text-gray text-sm">Загрузка...</p>
        </div>
      </div>
    </div>

    <!-- Основной контент -->
    <Transition
      enter-active-class="transition-all duration-500 ease-out"
      enter-class="opacity-0 scale-95"
      enter-to-class="opacity-100 scale-100"
    >
      <div v-if="!isLoading" class="flex flex-col min-h-screen">
        <!-- Header -->
        <header class="sticky top-0 z-40 bg-gradient-to-r from-[#202024]/90 to-[#2c2c31]/90 backdrop-blur-md border-b border-[#2c2c31]/50 shadow-lg">
          <div class="flex items-center justify-between px-4 py-3">
            <div class="flex items-center space-x-3 group">
              <div class="w-10 h-10 bg-gradient-to-br from-violet/20 to-purple/20 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
                <span class="text-xl">💰</span>
              </div>
              <h1 class="font-deftone text-xl text-white group-hover:text-violet transition-colors">
                <span class="text-violet">TREASURE</span> Casino
              </h1>
            </div>
            <div class="flex items-center space-x-3">
              <!-- Баланс пользователя -->
              <div class="hidden sm:flex items-center space-x-2 bg-gradient-to-r from-green/10 to-emerald/10 px-3 py-1 rounded-lg border border-green/20">
                <span class="text-green text-sm font-semibold">{{ userBalance }}₽</span>
              </div>
                        <!-- Онлайн игроки -->
          <div class="flex items-center space-x-2 bg-gradient-to-r from-blue/10 to-cyan/10 px-3 py-1 rounded-lg border border-blue/20">
            <div class="w-2 h-2 bg-green rounded-full animate-pulse"></div>
            <span class="text-xs text-gray font-medium">{{ online }} онлайн</span>
          </div>
            </div>
          </div>
        </header>

        <!-- Основной контент -->
        <main class="flex-1 px-4 py-4 bg-gradient-to-br from-[#202024] to-[#1b1c20]">
          <router-view />
        </main>

        <!-- Нижняя навигация -->
        <nav class="sticky bottom-0 bg-gradient-to-r from-[#202024]/95 to-[#2c2c31]/95 backdrop-blur-md border-t border-[#2c2c31]/50 shadow-lg">
          <div class="flex items-center justify-around py-3">
            <router-link
              v-for="item in navigation"
              :key="item.path"
              :to="item.path"
              class="flex flex-col items-center space-y-1 p-2 rounded-xl transition-all duration-300 group relative"
              :class="[
                currentPath === item.path
                  ? 'text-violet bg-gradient-to-r from-violet/20 to-purple/20 scale-110'
                  : 'text-gray hover:text-grayLight hover:bg-[#2c2c31]/50'
              ]"
            >
              <!-- Декоративные элементы для активной вкладки -->
              <div v-if="currentPath === item.path" class="absolute -top-1 -right-1 w-2 h-2 bg-violet rounded-full animate-pulse"></div>
              
              <HomeIcon v-if="item.icon === 'HomeIcon'" class="w-6 h-6 group-hover:scale-110 transition-transform" />
              <DiceIcon v-else-if="item.icon === 'DiceIcon'" class="w-6 h-6 group-hover:scale-110 transition-transform" />
              <WheelIcon v-else-if="item.icon === 'WheelIcon'" class="w-6 h-6 group-hover:scale-110 transition-transform" />
              <SportsIcon v-else-if="item.icon === 'SportsIcon'" class="w-6 h-6 group-hover:scale-110 transition-transform" />
              <AnalyticsIcon v-else-if="item.icon === 'AnalyticsIcon'" class="w-6 h-6 group-hover:scale-110 transition-transform" />
              <PredictionsIcon v-else-if="item.icon === 'PredictionsIcon'" class="w-6 h-6 group-hover:scale-110 transition-transform" />
              <AchievementsIcon v-else-if="item.icon === 'AchievementsIcon'" class="w-6 h-6 group-hover:scale-110 transition-transform" />
              <BonusIcon v-else-if="item.icon === 'BonusIcon'" class="w-6 h-6 group-hover:scale-110 transition-transform" />
              <ProfileIcon v-else class="w-6 h-6 group-hover:scale-110 transition-transform" />
              <span class="text-xs font-medium">{{ item.name }}</span>
            </router-link>
          </div>
        </nav>
      </div>
    </Transition>

    <!-- Глобальные уведомления -->
    <div v-if="globalMessage" class="fixed top-20 left-4 right-4 z-50">
      <div class="bg-gradient-to-r from-green/90 to-emerald/90 backdrop-blur-sm rounded-xl p-4 text-white text-center animate-bounce shadow-lg">
        {{ globalMessage }}
      </div>
    </div>

    <!-- Временно отключаем компоненты для стабильности -->
    <!--
    <Chat />
    <Notifications />
    <ConnectionStatus />
    <PWAInstall />
    <div class="fixed top-4 left-4 z-40">
      <LanguageSwitcher />
    </div>
    -->
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useUserStore } from './stores/user'
import HomeIcon from './components/icons/HomeIcon.vue'
import DiceIcon from './components/icons/DiceIcon.vue'
import WheelIcon from './components/icons/WheelIcon.vue'
import BonusIcon from './components/icons/BonusIcon.vue'
import ProfileIcon from './components/icons/ProfileIcon.vue'
import SportsIcon from './components/icons/SportsIcon.vue'
import AnalyticsIcon from './components/icons/AnalyticsIcon.vue'
import PredictionsIcon from './components/icons/PredictionsIcon.vue'
import AchievementsIcon from './components/icons/AchievementsIcon.vue'
import Chat from './components/Chat.vue'
import Notifications from './components/Notifications.vue'
import ConnectionStatus from './components/ConnectionStatus.vue'
import PWAInstall from './components/PWAInstall.vue'
import LanguageSwitcher from './components/LanguageSwitcher.vue'
import wsService from './services/websocket'

export default {
  name: 'App',
  components: {
    HomeIcon,
    DiceIcon,
    WheelIcon,
    BonusIcon,
    ProfileIcon,
    SportsIcon,
    AnalyticsIcon,
    PredictionsIcon,
    AchievementsIcon,
    Chat,
    Notifications,
    ConnectionStatus,
    PWAInstall,
    LanguageSwitcher
  },
  setup() {
    const isLoading = ref(true)
    const online = ref(0)
    const globalMessage = ref('')
    const currentPath = ref('/')
    const userBalance = ref('0₽')

    let userStore

    const navigation = [
      { name: 'Главная', path: '/', icon: 'HomeIcon' },
      { name: 'Dice', path: '/dice', icon: 'DiceIcon' },
      { name: 'Wheel', path: '/wheel', icon: 'WheelIcon' },
      { name: 'Спорт', path: '/sports', icon: 'SportsIcon' },
      { name: 'Аналитика', path: '/analytics', icon: 'AnalyticsIcon' },
      { name: 'Бонусы', path: '/bonus', icon: 'BonusIcon' },
      { name: 'Профиль', path: '/profile', icon: 'ProfileIcon' }
    ]

    onMounted(async () => {
      try {
        // Инициализация Telegram Web App
        if (window.Telegram?.WebApp) {
          window.Telegram.WebApp.ready()
          window.Telegram.WebApp.expand()

          userStore = useUserStore()
          await userStore.initFromTelegram()
          userBalance.value = userStore.formattedBalance

          // Инициализация WebSocket сервиса
          wsService.init(userStore.user?.id, window.Telegram.WebApp.initData)

          // Применяем тему Telegram
          const themeParams = window.Telegram.WebApp.themeParams
          if (themeParams) {
            document.documentElement.style.setProperty('--tg-theme-bg-color', themeParams.bg_color || '#202024')
            document.documentElement.style.setProperty('--tg-theme-text-color', themeParams.text_color || '#cfcde9')
            document.documentElement.style.setProperty('--tg-theme-hint-color', themeParams.hint_color || '#6a6a7a')
            document.documentElement.style.setProperty('--tg-theme-link-color', themeParams.link_color || '#7c75d9')
            document.documentElement.style.setProperty('--tg-theme-button-color', themeParams.button_color || '#7c75d9')
            document.documentElement.style.setProperty('--tg-theme-button-text-color', themeParams.button_text_color || '#ffffff')
          }

          // Показываем приветственное сообщение
          const initDataUnsafe = window.Telegram.WebApp.initDataUnsafe
          if (initDataUnsafe?.user) {
            globalMessage.value = `🎉 Добро пожаловать, ${initDataUnsafe.user.first_name}!`
            setTimeout(() => {
              globalMessage.value = ''
            }, 3000)
          }
        }

        console.log('✅ Telegram Casino App initialized successfully!')

      } catch (error) {
        console.error('❌ Ошибка инициализации:', error)
        console.warn('UserStore not available yet, using fallback')
      }

      // Симуляция загрузки
      setTimeout(() => {
        isLoading.value = false
      }, 1500)

      // Обновляем количество онлайн игроков
      online.value = Math.floor(Math.random() * 200) + 50
      setInterval(() => {
        online.value = Math.floor(Math.random() * 200) + 50
      }, 30000)
    })

    return {
      isLoading,
      online,
      globalMessage,
      navigation,
      currentPath,
      userBalance
    }
  }
}
</script>

<style>
/* Глобальные стили */
.tg-app {
  background: linear-gradient(135deg, #202024 0%, #1b1c20 100%);
}

/* Анимации для лоадера */
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

/* Плавные переходы */
* {
  transition: all 0.2s ease-in-out;
}

/* Кастомный скроллбар */
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: #1b1c20;
}

::-webkit-scrollbar-thumb {
  background: #7c75d9;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: #8c84ec;
}
</style>
