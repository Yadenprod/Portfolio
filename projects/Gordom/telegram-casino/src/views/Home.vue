<template>
  <div class="flex flex-col space-y-6">
    <!-- Приветственный блок -->
    <div class="flex flex-col space-y-4">
      <div class="flex flex-col [&_h1]:font-deftone [&_h1]:text-[26px] [&_h1>span]:text-violet font-semibold text-grayLight [&_p]:text-sm [&_p]:text-grayLight [&_p]:leading-[180%] space-y-2">
        <h1><span>TREASURE</span> Casino</h1>
        <p>Уникальные игры с выводом денег <br> и с большым шансом на победу</p>
      </div>
      
      <!-- Онлайн игроки -->
      <div class="flex flex-col space-y-2">
        <span class="text-sm text-gray font-semibold">Сейчас играют:</span>
        <div class="flex items-center space-x-3 font-rubik">
          <span class="flex relative h-2 w-2">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-green opacity-75"></span>
            <span class="relative inline-flex rounded-full h-2 w-2 bg-green"></span>
          </span>
          <b class="font-medium text-lg">{{ online || 0 }}</b>
        </div>
      </div>
    </div>

    <!-- Баннер турниров -->
    <div class="w-full grid before:pt-[30%] relative rounded-2xl overflow-hidden">
      <div class="absolute left-0 top-0 w-full h-full flex items-center justify-center z-[1]">
        <div class="flex flex-col items-center space-y-6">
          <div class="flex flex-col items-center space-y-1">
            <div class="uppercase text-6xl font-rubik font-medium select-none text-white leading-[100%]">Игры</div>
            <p class="text-sm font-semibold text-grayLight">выбери игру и начни играть</p>
          </div>
          <button 
            @click="claimJackpot"
            :disabled="jackpotLoading"
            class="px-6 py-3 bg-violet hover:bg-violetHover disabled:opacity-50 disabled:cursor-not-allowed rounded-xl text-white font-semibold transition-colors flex items-center space-x-2"
          >
            <span v-if="!jackpotLoading">🎮</span>
            <span v-else class="animate-spin">⚡</span>
            <span>{{ jackpotLoading ? 'Открываем...' : 'Играть сейчас!' }}</span>
          </button>
        </div>
      </div>
      <!-- Красивый градиентный фон -->
      <div class="absolute left-0 top-0 w-full h-full bg-gradient-to-br from-violet/30 via-purple/20 to-pink/30"></div>
      <!-- Декоративные элементы -->
      <div class="absolute top-4 right-4 text-2xl">🏆</div>
      <div class="absolute bottom-4 left-4 text-2xl">💎</div>
    </div>

    <!-- Быстрые действия -->
    <QuickActions />

    <!-- Популярные ставки -->
    <TrendingBets />

    <!-- Наши игры -->
    <div class="w-full flex flex-col space-y-6">
      <div class="flex items-center justify-between">
        <div class="flex items-center text-grayLight uppercase font-rubik font-medium text-sm space-x-2">
          <svg class="w-[18px] h-[18px]" fill="currentColor" viewBox="0 0 24 24">
            <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
          </svg>
          <span>Наши игры</span>
        </div>
      </div>

      <!-- Карточки игр -->
      <div class="grid grid-cols-2 gap-4">
        <div 
          v-for="game in games" 
          :key="game.id"
          @click="$router.push(game.path)"
          class="relative group cursor-pointer"
        >
          <div class="aspect-square bg-[#2c2c31] rounded-2xl overflow-hidden transition-all duration-200 group-hover:bg-[#35353c] group-hover:scale-105">
            <!-- Красивый градиентный фон для каждой игры -->
            <div class="absolute inset-0 bg-gradient-to-br" :class="game.gradient"></div>
            
            <div class="relative z-10 w-full h-full flex items-center justify-center">
              <span class="text-5xl filter drop-shadow-lg">{{ game.icon }}</span>
            </div>
            
            <!-- Анимированные частицы -->
            <div class="absolute inset-0 opacity-20">
              <div class="absolute top-2 left-2 text-sm animate-bounce">✨</div>
              <div class="absolute top-4 right-4 text-xs animate-pulse">⭐</div>
              <div class="absolute bottom-6 left-6 text-xs animate-ping">💫</div>
            </div>
            
            <div class="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent"></div>
            <div class="absolute bottom-4 left-4 right-4 z-20">
              <h3 class="text-white font-semibold text-lg drop-shadow-lg">{{ game.name }}</h3>
              <p class="text-grayLight text-sm drop-shadow-lg">{{ game.description }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Быстрые действия -->
    <div class="grid grid-cols-2 gap-4">
      <button 
        @click="$router.push('/deposit')"
        class="p-4 bg-green/20 hover:bg-green/30 rounded-xl text-green font-semibold transition-colors flex items-center justify-center space-x-2 group"
      >
        <span class="text-xl group-hover:scale-110 transition-transform">💰</span>
        <span>Пополнить</span>
      </button>
      <button 
        @click="$router.push('/withdraw')"
        class="p-4 bg-red/20 hover:bg-red/30 rounded-xl text-red font-semibold transition-colors flex items-center justify-center space-x-2 group"
      >
        <span class="text-xl group-hover:scale-110 transition-transform">💳</span>
        <span>Вывести</span>
      </button>
    </div>

    <!-- Уведомление о джекпоте -->
    <div v-if="jackpotMessage" class="fixed top-4 left-4 right-4 z-50">
      <div class="bg-green/90 backdrop-blur-sm rounded-xl p-4 text-white text-center animate-bounce">
        {{ jackpotMessage }}
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useUserStore } from '../stores/user'
import QuickActions from '../components/QuickActions.vue'
import TrendingBets from '../components/TrendingBets.vue'

export default {
  name: 'Home',
  components: {
    QuickActions,
    TrendingBets
  },
  setup() {
    let userStore = null

    // Безопасная инициализация userStore
    try {
      userStore = useUserStore()
    } catch (error) {
      console.warn('UserStore not available yet, using fallback')
      userStore = { user: null, balance: 0 }
    }

    const online = ref(0)
    const jackpotLoading = ref(false)
    const jackpotMessage = ref('')
    
    const games = [
      {
        id: 1,
        name: 'Dice',
        path: '/dice',
        icon: '🎲',
        description: 'Игра в кости',
        gradient: 'from-blue/20 to-cyan/20'
      },
      {
        id: 2,
        name: 'Wheel',
        path: '/wheel',
        icon: '🎡',
        description: 'Колесо фортуны',
        gradient: 'from-purple/20 to-pink/20'
      },
      {
        id: 3,
        name: 'Mines',
        path: '/mines',
        icon: '💣',
        description: 'Найди мины',
        gradient: 'from-red/20 to-orange/20'
      },
      {
        id: 4,
        name: 'Slots',
        path: '/slots',
        icon: '🎰',
        description: 'Классические слоты',
        gradient: 'from-green/20 to-emerald/20'
      }
    ]

    const claimJackpot = async () => {
      if (jackpotLoading.value) return
      
      jackpotLoading.value = true
      
      try {
        // Симуляция проверки джекпота
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        // Открываем случайную игру вместо проверки джекпота
        const gamePaths = ['/dice', '/wheel', '/mines', '/slots']
        const randomGame = gamePaths[Math.floor(Math.random() * gamePaths.length)]
        
        // Показываем сообщение о переходе в игру
        jackpotMessage.value = '🎮 Открываем игру для вас!'
        
        setTimeout(() => {
          // Переходим в случайную игру
          window.location.href = randomGame
        }, 1500)
        
      } catch (error) {
        jackpotMessage.value = '❌ Ошибка при открытии игры'
        setTimeout(() => {
          jackpotMessage.value = ''
        }, 3000)
      } finally {
        jackpotLoading.value = false
      }
    }

    onMounted(() => {
      // Симуляция получения количества онлайн игроков
      online.value = Math.floor(Math.random() * 200) + 50
      
      // Обновляем количество игроков каждые 30 секунд
      setInterval(() => {
        online.value = Math.floor(Math.random() * 200) + 50
      }, 30000)
    })

    return {
      online,
      games,
      jackpotLoading,
      jackpotMessage,
      claimJackpot
    }
  }
}
</script>
