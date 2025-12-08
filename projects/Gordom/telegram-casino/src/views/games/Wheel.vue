<template>
  <div class="flex flex-col space-y-6">
    <!-- Заголовок игры -->
    <div class="text-center">
      <div class="flex items-center justify-center gap-6">
        <div class="shrink-0 relative select-none group">
          <div class="absolute left-0 -top-[5px] w-full h-full flex items-center justify-center z-[1]">
            <span class="font-deftone text-grayLight text-4xl tracking-[1px] group-hover:text-violet transition-colors">Wheel</span>
          </div>
          <div class="w-32 h-32 bg-gradient-to-br from-purple/20 to-pink/20 rounded-xl flex items-center justify-center group-hover:scale-105 transition-transform duration-300 shadow-lg">
            <span class="text-6xl filter drop-shadow-lg animate-pulse">🎡</span>
          </div>
          <!-- Декоративные элементы -->
          <div class="absolute -top-2 -right-2 text-lg animate-bounce">✨</div>
          <div class="absolute -bottom-2 -left-2 text-lg animate-ping">💫</div>
        </div>
      </div>
    </div>

    <!-- Игровое поле -->
    <div class="bg-gradient-to-br from-[#202024] to-[#2c2c31] rounded-xl p-6 space-y-6 shadow-xl">
      <!-- Описание игры -->
      <div class="flex flex-col items-center space-y-4">
        <div class="w-16 h-16 bg-gradient-to-br from-violet/20 to-purple/20 rounded-xl flex items-center justify-center group hover:scale-110 transition-transform">
          <span class="text-2xl animate-pulse">🎯</span>
        </div>
        <p class="uppercase text-grayLight text-sm font-medium text-center">Колесо фортуны с большими выигрышами!</p>
      </div>

      <!-- Колесо -->
      <div class="flex flex-col items-center space-y-6">
        <!-- Таймер -->
        <div class="flex flex-col items-center space-y-2">
          <span class="text-grayLight text-sm font-semibold">До начала игры</span>
          <b class="text-violet text-3xl font-rubik font-semibold">{{ wheelTimer }}</b>
        </div>

        <!-- Колесо -->
        <div class="relative">
          <div class="w-64 h-64 relative">
            <!-- Колесо -->
            <div 
              ref="wheel"
              class="w-full h-full rounded-full border-4 border-violet/30 transition-transform duration-5000 ease-out overflow-hidden"
              :style="{ transform: `rotate(${wheelRotation}deg)` }"
            >
              <!-- SVG колесо с правильными секторами -->
              <svg class="w-full h-full" viewBox="0 0 256 256">
                <defs>
                  <clipPath id="wheel-clip">
                    <circle cx="128" cy="128" r="120"/>
                  </clipPath>
                </defs>
                
                <!-- Секторы колеса -->
                <g clip-path="url(#wheel-clip)">
                  <path 
                    v-for="(sector, index) in sectors" 
                    :key="index"
                    :d="getSectorPath(index)"
                    :fill="sector.hexColor"
                    stroke="#1a1a1a"
                    stroke-width="2"
                  />
                  
                  <!-- Текст множителей -->
                  <text
                    v-for="(sector, index) in sectors" 
                    :key="`text-${index}`"
                    :x="getTextX(index)"
                    :y="getTextY(index)"
                    :transform="`rotate(${index * 60 + 30}, ${getTextX(index)}, ${getTextY(index)})`"
                    class="text-white font-bold text-lg"
                    text-anchor="middle"
                    dominant-baseline="middle"
                    fill="white"
                    stroke="#000"
                    stroke-width="0.5"
                    font-size="14"
                    font-weight="bold"
                  >
                    x{{ sector.multiplier }}
                  </text>
                </g>
              </svg>
            </div>
            
            <!-- Центр колеса -->
            <div class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-12 h-12 bg-white rounded-full border-4 border-violet shadow-lg z-10"></div>
            
            <!-- Указатель -->
            <div class="absolute top-0 left-1/2 transform -translate-x-1/2 -translate-y-2 w-0 h-0 border-l-[16px] border-l-transparent border-r-[16px] border-r-transparent border-b-[32px] border-b-violet z-20 drop-shadow-lg"></div>
          </div>
        </div>

        <!-- История -->
        <div class="w-full">
          <h3 class="text-white font-semibold text-lg mb-4">История</h3>
          <div class="flex items-center space-x-3 overflow-x-auto pb-2">
            <div 
              v-for="item in history" 
              :key="item.id" 
              :class="getHistoryColor(item.multiplier)"
              class="min-w-[44px] min-h-[44px] border flex items-center justify-center rounded-xl font-rubik font-medium text-xs select-none flex-shrink-0 hover:scale-110 transition-transform"
            >
              x{{ item.multiplier }}
            </div>
          </div>
        </div>

        <!-- Текущие ставки -->
        <div v-if="currentBets.length > 0" class="w-full">
          <h3 class="text-white font-semibold text-lg mb-4">Ваши ставки:</h3>
          <div class="flex flex-wrap gap-2">
            <div 
              v-for="bet in currentBets" 
              :key="bet.color"
              class="px-3 py-2 bg-violet/20 border border-violet/30 rounded-lg text-violet font-medium text-sm flex items-center space-x-2"
            >
              <span>{{ bet.color }}</span>
              <span class="text-white">{{ bet.amount }}₽</span>
              <span class="text-violet">x{{ bet.sector.multiplier }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Ставки -->
      <div class="space-y-4">
        <h3 class="text-white font-semibold text-lg">Ваша ставка:</h3>
        
        <!-- Быстрые кнопки -->
        <div class="grid grid-cols-4 gap-2">
          <button 
            @click="maxBet"
            class="w-11 h-11 bg-gradient-to-br from-green/20 to-emerald/20 hover:from-green/30 hover:to-emerald/30 flex items-center justify-center rounded-xl font-rubik font-medium text-xs transition-all duration-200 hover:scale-105 border border-green/20"
          >
            Max
          </button>
          <button 
            @click="minBet"
            class="w-11 h-11 bg-gradient-to-br from-red/20 to-pink/20 hover:from-red/30 hover:to-pink/30 flex items-center justify-center rounded-xl font-rubik font-medium text-xs transition-all duration-200 hover:scale-105 border border-red/20"
          >
            Min
          </button>
          <button 
            @click="doubleBet"
            class="w-11 h-11 bg-gradient-to-br from-blue/20 to-cyan/20 hover:from-blue/30 hover:to-cyan/30 flex items-center justify-center rounded-xl font-rubik font-medium text-xs transition-all duration-200 hover:scale-105 border border-blue/20"
          >
            x2
          </button>
          <button 
            @click="halfBet"
            class="w-11 h-11 bg-gradient-to-br from-orange/20 to-yellow/20 hover:from-orange/30 hover:to-yellow/30 flex items-center justify-center rounded-xl font-rubik font-medium text-xs transition-all duration-200 hover:scale-105 border border-orange/20"
          >
            1/2
          </button>
        </div>

        <!-- Поле ввода ставки -->
        <div class="relative">
          <input
            v-model="betAmount"
            type="number"
            placeholder="Введите сумму"
            class="w-full p-4 bg-[#1b1c20] rounded-xl text-white placeholder-gray focus:outline-none focus:ring-2 focus:ring-violet border border-gray/20"
          />
          <div class="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray">₽</div>
        </div>

        <!-- Кнопки ставок -->
        <div class="grid grid-cols-6 gap-2">
          <button
            v-for="sector in sectors"
            :key="sector.id"
            @click="placeBet(sector.color)"
            :disabled="!canBet || loading || gameInProgress"
            :class="[
              sector.buttonClass,
              currentBets.find(bet => bet.color === sector.color) ? 'ring-2 ring-green-400 ring-opacity-50' : ''
            ]"
            class="h-16 px-3 rounded-xl text-white font-semibold transition-all duration-200 hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed flex flex-col items-center justify-center space-y-1 relative"
          >
            <span class="text-xs font-medium">{{ sector.color }}</span>
            <span class="text-lg font-rubik">x{{ sector.multiplier }}</span>
            <span class="text-xs opacity-75">{{ currentBets.find(bet => bet.color === sector.color) ? 'Поставлено' : 'Ставка' }}</span>
            <div v-if="currentBets.find(bet => bet.color === sector.color)" class="absolute -top-1 -right-1 w-4 h-4 bg-green-500 rounded-full flex items-center justify-center">
              <span class="text-white text-xs">✓</span>
            </div>
          </button>
        </div>
      </div>
    </div>

    <!-- Уведомление о результате -->
    <div v-if="resultMessage" class="fixed top-4 left-4 right-4 z-50">
      <div :class="isWin ? 'bg-green/90' : 'bg-red/90'" class="backdrop-blur-sm rounded-xl p-4 text-white text-center animate-bounce">
        {{ resultMessage }}
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useUserStore } from '../../stores/user'
import { postBet } from '../../api/endpoints'
import { notify } from '../../services/notifications'

export default {
  name: 'Wheel',
  setup() {
    let userStore = null

    // Безопасная инициализация userStore
    try {
      userStore = useUserStore()
    } catch (error) {
      console.warn('UserStore not available yet, using fallback')
      userStore = { user: null, balance: 0, updateBalance: () => {} }
    }

    const betAmount = ref(10)
    const loading = ref(false)
    const wheelRotation = ref(0)
    const wheelTimer = ref('00:20')
    const isWin = ref(false)
    const resultMessage = ref('')
    const gameInProgress = ref(false)
    const currentBets = ref([])
    const canPlaceBet = ref(true)
    
    const sectors = ref([
      { id: 0, color: 'green', multiplier: 3, hexColor: '#44c276', buttonClass: 'bg-green-600 hover:bg-green-500' },
      { id: 1, color: 'orange', multiplier: 5, hexColor: '#f08929', buttonClass: 'bg-orange-600 hover:bg-orange-500' },
      { id: 2, color: 'red', multiplier: 10, hexColor: '#f24841', buttonClass: 'bg-red-600 hover:bg-red-500' },
      { id: 3, color: 'pink', multiplier: 20, hexColor: '#d92c9f', buttonClass: 'bg-pink-600 hover:bg-pink-500' },
      { id: 4, color: 'violet', multiplier: 100, hexColor: '#7c75d9', buttonClass: 'bg-violet-600 hover:bg-violet-500' },
      { id: 5, color: 'black', multiplier: 2, hexColor: '#2c2c31', buttonClass: 'bg-gray-700 hover:bg-gray-600' }
    ])

    const history = ref([
      { id: 1, multiplier: 2, color: 'black' },
      { id: 2, multiplier: 3, color: 'green' },
      { id: 3, multiplier: 5, color: 'orange' },
      { id: 4, multiplier: 10, color: 'red' },
      { id: 5, multiplier: 20, color: 'pink' },
      { id: 6, multiplier: 100, color: 'violet' },
      { id: 7, multiplier: 2, color: 'black' },
      { id: 8, multiplier: 3, color: 'green' }
    ])

    const canBet = computed(() => {
      return betAmount.value >= 1 && betAmount.value <= userStore.balance && canPlaceBet.value && !gameInProgress.value
    })

    const getSectorPath = (index) => {
      const angle = index * 60;
      const startAngle = (angle - 30) * Math.PI / 180;
      const endAngle = (angle + 30) * Math.PI / 180;
      const radius = 120;
      const centerX = 128;
      const centerY = 128;
      
      const x1 = centerX + radius * Math.cos(startAngle);
      const y1 = centerY + radius * Math.sin(startAngle);
      const x2 = centerX + radius * Math.cos(endAngle);
      const y2 = centerY + radius * Math.sin(endAngle);
      
      const largeArcFlag = 0; // 0 for angles <= 180, 1 for angles > 180
      
      return `M ${centerX} ${centerY} L ${x1} ${y1} A ${radius} ${radius} 0 ${largeArcFlag} 1 ${x2} ${y2} Z`;
    };

    const getTextX = (index) => {
      // Центр каждого сектора (30 градусов от начала сектора)
      const angle = (index * 60 + 30) * Math.PI / 180;
      return 128 + 50 * Math.cos(angle);
    };

    const getTextY = (index) => {
      // Центр каждого сектора (30 градусов от начала сектора)
      const angle = (index * 60 + 30) * Math.PI / 180;
      return 128 + 50 * Math.sin(angle);
    };

    const getHistoryColor = (multiplier) => {
      const colors = {
        2: 'text-[#bec5da] bg-gray-600/10 border-gray-600/20',
        3: 'text-[#44c276] bg-green-600/10 border-green-600/20',
        5: 'text-[#f08929] bg-orange-600/10 border-orange-600/20',
        10: 'text-[#f24841] bg-red-600/10 border-red-600/20',
        20: 'text-[#d92c9f] bg-pink-600/10 border-pink-600/20',
        100: 'text-[#7c75d9] bg-violet-600/10 border-violet-600/20'
      }
      return colors[multiplier] || colors[2]
    }

    const maxBet = () => {
      betAmount.value = userStore.balance
    }

    const minBet = () => {
      betAmount.value = 1
    }

    const doubleBet = () => {
      betAmount.value = Math.min(betAmount.value * 2, userStore.balance)
    }

    const halfBet = () => {
      betAmount.value = Math.max(Math.floor(betAmount.value / 2), 1)
    }

    const placeBet = async (color) => {
      if (!canBet.value || loading.value) return
      
      // Проверяем, есть ли уже ставка на этот цвет
      const existingBet = currentBets.value.find(bet => bet.color === color)
      if (existingBet) {
        resultMessage.value = '❌ Вы уже поставили на этот цвет!'
        setTimeout(() => {
          resultMessage.value = ''
        }, 3000)
        return
      }
      
      loading.value = true
      
      try {
        // Добавляем ставку в список
        currentBets.value.push({
          color: color,
          amount: betAmount.value,
          sector: sectors.value.find(s => s.color === color)
        })
        
        resultMessage.value = `✅ Ставка ${betAmount.value}₽ на ${color} принята!`
        setTimeout(() => {
          resultMessage.value = ''
        }, 2000)
        
      } catch (error) {
        resultMessage.value = '❌ Ошибка при размещении ставки'
        setTimeout(() => {
          resultMessage.value = ''
        }, 3000)
      } finally {
        loading.value = false
      }
    }

    const startGame = async () => {
      if (currentBets.value.length === 0) {
        resultMessage.value = '❌ Нет активных ставок!'
        setTimeout(() => {
          resultMessage.value = ''
        }, 3000)
        return
      }
      
      gameInProgress.value = true
      canPlaceBet.value = false
      
      try {
        // Выбираем случайный сектор для выигрыша
        const winningSector = sectors.value[Math.floor(Math.random() * sectors.value.length)]
        const winningColor = winningSector.color
        
        // Анимация вращения колеса
        const targetRotation = Math.random() * 360
        wheelRotation.value += 360 * 5 + targetRotation
        
        // Ждем окончания анимации
        await new Promise(resolve => setTimeout(resolve, 5000))
        
        // Проверяем выигрышные ставки
        let totalWin = 0
        let hasWinningBet = false
        
        for (const bet of currentBets.value) {
          if (bet.color === winningColor) {
            const winAmount = bet.amount * bet.sector.multiplier
            totalWin += winAmount
            hasWinningBet = true
          }
        }
        
        // Обновляем баланс
        const totalBet = currentBets.value.reduce((sum, bet) => sum + bet.amount, 0)
        const balanceChange = hasWinningBet ? totalWin - totalBet : -totalBet
        userStore.updateBalance(balanceChange)
        
        // Показываем результат
        isWin.value = hasWinningBet
        
        if (hasWinningBet) {
          resultMessage.value = `🎉 Победа! Выигрыш: ${totalWin}₽ (x${winningSector.multiplier})`
          notify.win(totalWin, 'Wheel')
        } else {
          resultMessage.value = `😔 Проигрыш: -${totalBet}₽`
          notify.loss(totalBet, 'Wheel')
        }
        
        // Добавляем в историю
        history.value.unshift({
          id: Date.now(),
          multiplier: winningSector.multiplier,
          color: winningColor
        })
        
        // Ограничиваем историю
        if (history.value.length > 10) {
          history.value = history.value.slice(0, 10)
        }
        
        // Скрываем сообщение через 3 секунды
        setTimeout(() => {
          resultMessage.value = ''
        }, 3000)
        
      } catch (error) {
        resultMessage.value = '❌ Ошибка при игре'
        setTimeout(() => {
          resultMessage.value = ''
        }, 3000)
      } finally {
        // Очищаем ставки и готовимся к следующему раунду
        currentBets.value = []
        gameInProgress.value = false
        canPlaceBet.value = true
      }
    }

    let timerInterval
    let gameInterval

    onMounted(() => {
      // Симуляция таймера
      let seconds = 20
      timerInterval = setInterval(() => {
        seconds--
        if (seconds < 0) {
          seconds = 20
          // Запускаем игру когда таймер достигает 0
          startGame()
        }
        wheelTimer.value = `00:${seconds.toString().padStart(2, '0')}`
      }, 1000)
    })

    onUnmounted(() => {
      if (timerInterval) {
        clearInterval(timerInterval)
      }
      if (gameInterval) {
        clearInterval(gameInterval)
      }
    })

    return {
      betAmount,
      loading,
      wheelRotation,
      wheelTimer,
      isWin,
      resultMessage,
      sectors,
      history,
      currentBets,
      canBet,
      canPlaceBet,
      gameInProgress,
      getSectorPath,
      getTextX,
      getTextY,
      getHistoryColor,
      maxBet,
      minBet,
      doubleBet,
      halfBet,
      placeBet,
      startGame
    }
  }
}
</script>

<style scoped>
/* Анимации для колеса */
@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.wheel-spinning {
  animation: spin 5s cubic-bezier(0, 0.49, 0, 1) forwards;
}
</style>
