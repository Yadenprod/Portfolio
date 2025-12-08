<template>
  <div class="flex flex-col space-y-6">
    <!-- Заголовок игры -->
    <div class="text-center">
      <h1 class="font-deftone text-3xl text-white mb-2">
        <span class="text-violet">SLOTS</span>
      </h1>
      <p class="text-grayLight text-sm">Классические слоты с джекпотом!</p>
    </div>

    <!-- Игровое поле -->
    <div class="bg-[#2c2c31] rounded-2xl p-6 space-y-6">
      <!-- Слоты -->
      <div class="flex justify-center">
        <div class="relative w-64 h-32 bg-[#1b1c20] rounded-xl overflow-hidden border-2 border-violet">
          <!-- Барабаны -->
          <div class="flex h-full">
            <div 
              v-for="(reel, reelIndex) in reels" 
              :key="reelIndex"
              class="flex-1 relative overflow-hidden"
            >
              <div 
                class="flex flex-col transition-transform duration-3000 ease-out"
                :style="{ transform: `translateY(${reel.offset}px)` }"
              >
                <div 
                  v-for="(symbol, symbolIndex) in reel.symbols" 
                  :key="symbolIndex"
                  class="h-32 flex items-center justify-center text-4xl"
                >
                  {{ symbol }}
                </div>
              </div>
            </div>
          </div>
          
          <!-- Линии выигрыша -->
          <div class="absolute inset-0 pointer-events-none">
            <div class="h-1/3 border-t border-b border-green/50"></div>
          </div>
        </div>
      </div>

      <!-- Линии выигрыша -->
      <div class="grid grid-cols-3 gap-2">
        <button 
          v-for="line in paylines" 
          :key="line.id"
          @click="selectPayline(line.id)"
          class="p-2 rounded-lg text-xs font-medium transition-colors"
          :class="selectedPayline === line.id ? 'bg-violet text-white' : 'bg-[#1b1c20] text-grayLight hover:bg-[#35353c]'"
        >
          Линия {{ line.id }}
        </button>
      </div>

      <!-- Ставка -->
      <div class="space-y-4">
        <label class="text-sm font-medium text-grayLight">Ваша ставка:</label>
        
        <!-- Быстрые кнопки -->
        <div class="grid grid-cols-4 gap-2">
          <button 
            @click="setBet(10)"
            class="p-2 bg-[#1b1c20] rounded-lg text-xs font-medium text-grayLight hover:bg-[#35353c] transition-colors"
          >
            Min
          </button>
          <button 
            @click="setBet(bet * 0.5)"
            class="p-2 bg-[#1b1c20] rounded-lg text-xs font-medium text-grayLight hover:bg-[#35353c] transition-colors"
          >
            1/2
          </button>
          <button 
            @click="setBet(bet * 2)"
            class="p-2 bg-[#1b1c20] rounded-lg text-xs font-medium text-grayLight hover:bg-[#35353c] transition-colors"
          >
            x2
          </button>
          <button 
            @click="setBet(1000)"
            class="p-2 bg-[#1b1c20] rounded-lg text-xs font-medium text-grayLight hover:bg-[#35353c] transition-colors"
          >
            Max
          </button>
        </div>
        
        <!-- Поле ввода -->
        <input
          v-model="bet"
          type="number"
          placeholder="Введите сумму"
          class="w-full p-4 bg-[#1b1c20] rounded-xl text-white placeholder-gray focus:outline-none focus:ring-2 focus:ring-violet"
          @input="validateBet"
        />
      </div>

      <!-- Кнопка игры -->
      <button
        @click="spin"
        :disabled="!canPlay || isSpinning"
        class="w-full py-4 bg-violet hover:bg-violetHover disabled:opacity-50 disabled:cursor-not-allowed rounded-xl text-white font-semibold transition-all duration-200"
      >
        <span v-if="!isSpinning">Крутить</span>
        <span v-else class="flex items-center justify-center space-x-2">
          <div class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
          <span>Крутим...</span>
        </span>
      </button>
    </div>

    <!-- История игр -->
    <div class="space-y-4">
      <h3 class="text-lg font-semibold text-white">История</h3>
      <div class="flex space-x-2 overflow-x-auto pb-2">
        <div 
          v-for="(result, index) in history" 
          :key="index"
          class="flex-shrink-0 w-12 h-12 rounded-lg flex items-center justify-center text-sm font-bold"
          :class="result.win ? 'bg-green/20 text-green' : 'bg-red/20 text-red'"
        >
          {{ result.multiplier }}x
        </div>
      </div>
    </div>

    <!-- Уведомление об ошибке -->
    <div v-if="resultMessage" class="fixed top-4 left-4 right-4 z-50">
      <div class="bg-red/90 backdrop-blur-sm rounded-xl p-4 text-white text-center animate-bounce">
        {{ resultMessage }}
      </div>
    </div>

    <!-- Результат игры -->
    <Transition
      enter-active-class="transition-all duration-300 ease-out"
      enter-class="opacity-0 scale-95"
      enter-to-class="opacity-100 scale-100"
      leave-active-class="transition-all duration-200 ease-in"
      leave-class="opacity-100 scale-100"
      leave-to-class="opacity-0 scale-95"
    >
      <div v-if="showResult" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
        <div class="bg-[#2c2c31] rounded-2xl p-8 mx-4 text-center">
          <div class="text-6xl mb-4" :class="gameResult.win ? 'text-green' : 'text-red'">
            {{ gameResult.win ? '🎉' : '😔' }}
          </div>
          <h3 class="text-xl font-bold text-white mb-2">
            {{ gameResult.win ? 'Победа!' : 'Проигрыш' }}
          </h3>
          <p class="text-grayLight mb-4">
            {{ gameResult.win ? `+${gameResult.winAmount}` : `-${bet}` }}
          </p>
          <button
            @click="closeResult"
            class="px-6 py-3 bg-violet hover:bg-violetHover rounded-xl text-white font-semibold transition-colors"
          >
            Продолжить
          </button>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '../../stores/user'
import { notify } from '../../services/notifications'

export default {
  name: 'Slots',
  setup() {
    let userStore = null

    // Безопасная инициализация userStore
    try {
      userStore = useUserStore()
    } catch (error) {
      console.warn('UserStore not available yet, using fallback')
      userStore = { user: null, balance: 0, updateBalance: () => {} }
    }

    const bet = ref(10)
    const isSpinning = ref(false)
    const showResult = ref(false)
    const gameResult = ref({})
    const history = ref([])
    const selectedPayline = ref(1)
    const resultMessage = ref('')

    const symbols = ['🍎', '🍊', '🍇', '🍒', '💎', '7️⃣', '🎰', '⭐']
    const paylines = [
      { id: 1, positions: [1, 1, 1] }, // Средняя линия
      { id: 2, positions: [0, 0, 0] }, // Верхняя линия
      { id: 3, positions: [2, 2, 2] }  // Нижняя линия
    ]

    const reels = ref([
      { symbols: [], offset: 0 },
      { symbols: [], offset: 0 },
      { symbols: [], offset: 0 }
    ])

    const canPlay = computed(() => {
      return bet.value > 0 && bet.value <= userStore.balance && !isSpinning.value
    })

    const setBet = (amount) => {
      bet.value = Math.max(1, Math.min(amount, userStore.balance))
    }

    const validateBet = () => {
      if (bet.value < 1) bet.value = 1
      if (bet.value > userStore.balance) bet.value = userStore.balance
    }

    const selectPayline = (paylineId) => {
      selectedPayline.value = paylineId
    }

    const generateReel = () => {
      const reelSymbols = []
      for (let i = 0; i < 9; i++) { // 9 символов на барабан
        const randomSymbol = symbols[Math.floor(Math.random() * symbols.length)]
        reelSymbols.push(randomSymbol)
      }
      return reelSymbols
    }

    const initializeReels = () => {
      reels.value = reels.value.map(() => ({
        symbols: generateReel(),
        offset: 0
      }))
    }

    const getSymbolValue = (symbol) => {
      const values = {
        '🍎': 10,
        '🍊': 15,
        '🍇': 20,
        '🍒': 25,
        '💎': 50,
        '7️⃣': 100,
        '🎰': 200,
        '⭐': 500
      }
      return values[symbol] || 0
    }

    const checkWin = (reelResults) => {
      const payline = paylines.find(p => p.id === selectedPayline.value)
      const lineSymbols = payline.positions.map((pos, reelIndex) => 
        reelResults[reelIndex][pos]
      )
      
      // Проверяем на джекпот (три одинаковых символа)
      if (lineSymbols[0] === lineSymbols[1] && lineSymbols[1] === lineSymbols[2]) {
        const symbolValue = getSymbolValue(lineSymbols[0])
        return { win: true, multiplier: symbolValue / 10, amount: bet.value * (symbolValue / 10) }
      }
      
      // Проверяем на пару
      if (lineSymbols[0] === lineSymbols[1] || lineSymbols[1] === lineSymbols[2] || lineSymbols[0] === lineSymbols[2]) {
        const symbolValue = getSymbolValue(lineSymbols[1]) // берем средний символ
        return { win: true, multiplier: (symbolValue / 10) * 0.5, amount: bet.value * (symbolValue / 10) * 0.5 }
      }
      
      return { win: false, multiplier: 0, amount: 0 }
    }

    const spin = async () => {
      if (!canPlay.value) return

      isSpinning.value = true

      try {
        // Отправляем ставку через API
        const response = await postBet('slots', {
          amount: bet.value,
          payline: selectedPayline.value
        })

        if (response.success) {
          // Используем результаты от сервера
          const reelResults = response.reels || []

          // Анимация вращения
          const spinPromises = reels.value.map((reel, index) => {
            return new Promise(resolve => {
              const spins = 3 + Math.random() * 2 // 3-5 оборотов
              const targetOffset = -(Math.random() * 64) // случайная позиция
              const duration = 2000 + index * 500 // разная скорость для каждого барабана

              const startOffset = reel.offset
              const startTime = Date.now()

              const animate = () => {
                const elapsed = Date.now() - startTime
                const progress = Math.min(elapsed / duration, 1)

                // Easing функция
                const easeOut = 1 - Math.pow(1 - progress, 3)

                reel.offset = startOffset + (targetOffset * easeOut)

                if (progress < 1) {
                  requestAnimationFrame(animate)
                } else {
                  resolve()
                }
              }

              animate()
            })
          })

          // Ждем завершения анимации
          await Promise.all(spinPromises)

          // Обновляем баланс
          userStore.updateBalance(response.balance_delta)

          // Добавление в историю
          history.value.unshift({
            multiplier: response.multiplier || 0,
            win: response.status || false
          })

          // Ограничение истории
          if (history.value.length > 10) {
            history.value = history.value.slice(0, 10)
          }

          // Показ результата
          gameResult.value = {
            win: response.status || false,
            winAmount: response.win_amount ? response.win_amount.toFixed(2) : '0.00'
          }

          // Отправляем уведомление
          if (response.status && response.win_amount > 0) {
            notify.win(response.win_amount, 'Slots')
          } else {
            notify.loss(bet.value, 'Slots')
          }

          showResult.value = true

          // Обновляем символы на барабанах
          setTimeout(() => {
            if (reelResults.length > 0) {
              reels.value = reelResults.map(reel => ({
                symbols: reel,
                offset: 0
              }))
            } else {
              initializeReels()
            }
          }, 1000)
        }
      } catch (error) {
        console.error('Slots spin error:', error)
        resultMessage.value = '❌ Ошибка при игре'
        setTimeout(() => {
          resultMessage.value = ''
        }, 3000)

        // Fallback анимация
        const reelResults = reels.value.map(() => {
          const reel = []
          for (let i = 0; i < 3; i++) {
            reel.push(symbols[Math.floor(Math.random() * symbols.length)])
          }
          return reel
        })

        // Простая анимация для fallback
        setTimeout(() => {
          initializeReels()
          isSpinning.value = false
        }, 2000)
      }

      isSpinning.value = false
    }

    const closeResult = () => {
      showResult.value = false
    }

    onMounted(() => {
      initializeReels()
      
      // Инициализация истории
      for (let i = 0; i < 5; i++) {
        history.value.push({
          multiplier: (Math.random() * 5).toFixed(1),
          win: Math.random() > 0.7
        })
      }
    })

    return {
      bet,
      isSpinning,
      showResult,
      gameResult,
      history,
      reels,
      selectedPayline,
      paylines,
      resultMessage,
      canPlay,
      setBet,
      validateBet,
      selectPayline,
      spin,
      closeResult
    }
  }
}
</script>
