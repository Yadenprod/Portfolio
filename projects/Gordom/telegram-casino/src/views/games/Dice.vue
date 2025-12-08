<template>
  <div class="flex flex-col space-y-6">
    <!-- Заголовок игры -->
    <div class="text-center">
      <div class="flex items-center justify-center gap-6">
        <div class="shrink-0 relative select-none group">
          <div class="absolute left-0 -top-[5px] w-full h-full flex items-center justify-center z-[1]">
            <span class="font-deftone text-grayLight text-4xl tracking-[1px] group-hover:text-violet transition-colors">Dice</span>
          </div>
          <div class="w-32 h-32 bg-gradient-to-br from-blue/20 to-cyan/20 rounded-xl flex items-center justify-center group-hover:scale-105 transition-transform duration-300 shadow-lg">
            <span class="text-6xl filter drop-shadow-lg animate-pulse">🎲</span>
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
        <p class="uppercase text-grayLight text-sm font-medium text-center">Угадай число и увеличь свой депозит!</p>
      </div>

      <!-- Слайдер шанса -->
      <div class="space-y-4">
        <div class="flex items-center text-sm text-gray justify-between font-medium font-rubik">
          <span class="w-7 text-center">0</span>
          <span class="w-7 text-center">30</span>
          <span class="w-7 text-center">50</span>
          <span class="w-7 text-center">70</span>
          <span class="w-7 text-center">100</span>
        </div>
        
        <div class="relative flex flex-col bg-gradient-to-r from-red/20 via-orange/20 to-green/20 px-4 py-5 rounded-xl border border-gray/20">
          <input
            v-model="sliderValue"
            type="range"
            min="1"
            max="95"
            step="1"
            class="w-full h-2 bg-gradient-to-r from-red via-orange to-green rounded-lg appearance-none cursor-pointer slider"
            @input="updateSlider"
          />
          
          <!-- Индикатор результата -->
          <div 
            v-if="showPicker"
            class="picker absolute top-1 w-4 h-4 rounded-full border-3 border-white shadow-lg transition-all duration-300 animate-pulse"
            :class="isWin ? 'win bg-green' : 'lose bg-red'"
            :style="{ left: pickerPosition + '%' }"
          ></div>
        </div>
      </div>

      <!-- История игр -->
      <div class="relative w-full overflow-hidden">
        <div class="flex items-center space-x-3 overflow-x-auto pb-2">
          <div 
            v-for="item in history" 
            :key="item.id" 
            :class="item.win ? 'text-green bg-green/10 border-green/20' : 'text-red bg-red/10 border-red/20'" 
            class="min-w-[44px] min-h-[44px] border flex items-center justify-center rounded-xl font-rubik font-medium text-xs select-none flex-shrink-0 hover:scale-110 transition-transform"
          >
            {{ item.percent }}
          </div>
        </div>
      </div>

      <!-- Ставка -->
      <div class="space-y-4">
        <div class="grid grid-cols-2 gap-4 text-sm bg-gradient-to-r from-violet/10 to-purple/10 py-3 px-4 rounded-xl text-gray border border-violet/20">
          <div class="flex justify-between">
            <span class="font-semibold">Коэффициент:</span>
            <b class="uppercase font-rubik font-medium text-grayLight text-base">x{{ parseFloat(100 / sliderValue).toFixed(2) }}</b>
          </div>
          <div class="flex justify-between">
            <span class="font-semibold">Шанс:</span>
            <b class="uppercase font-rubik font-medium text-grayLight text-base">{{ sliderValue }}%</b>
          </div>
        </div>

        <div class="space-y-4">
          <b class="text-grayLight font-semibold text-sm">Ваша ставка:</b>
          
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

          <!-- Кнопка игры -->
          <button
            @click="play"
            :disabled="!canPlay || loading"
            class="w-full py-4 bg-gradient-to-r from-violet to-purple hover:from-violetHover hover:to-purple/80 disabled:opacity-50 disabled:cursor-not-allowed rounded-xl text-white font-semibold transition-all duration-200 flex items-center justify-center space-x-2 hover:scale-105"
          >
            <span v-if="!loading">🎲</span>
            <span v-else class="animate-spin">⚡</span>
            <span>{{ loading ? 'Играем...' : 'Играть' }}</span>
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
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '../../stores/user'
import { postBet } from '../../api/endpoints'
import { notify } from '../../services/notifications'
import { analytics } from '../../services/analytics'

export default {
  name: 'Dice',
  setup() {
    let userStore = null

    // Безопасная инициализация userStore
    try {
      userStore = useUserStore()
    } catch (error) {
      console.warn('UserStore not available yet, using fallback')
      userStore = { user: null, balance: 0, updateBalance: () => {} }
    }

    const sliderValue = ref(50)
    const betAmount = ref(100)
    const loading = ref(false)
    const showPicker = ref(false)
    const pickerPosition = ref(50)
    const isWin = ref(false)
    const resultMessage = ref('')
    
    const history = ref([
      { id: 1, percent: 75, win: true },
      { id: 2, percent: 30, win: false },
      { id: 3, percent: 60, win: true },
      { id: 4, percent: 45, win: false },
      { id: 5, percent: 80, win: true }
    ])

    const canPlay = computed(() => {
      return betAmount.value >= 1 && betAmount.value <= userStore.balance
    })

    const updateSlider = () => {
      pickerPosition.value = sliderValue.value
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

    const play = async () => {
      if (!canPlay.value || loading.value) return

      analytics.trackGameEvent('Dice', 'game_start', { bet: betAmount.value, chance: sliderValue.value })
      analytics.trackBet('Dice', betAmount.value, 'dice_bet')

      loading.value = true
      showPicker.value = false
      
      try {
        const response = await postBet('dice', {
          amount: betAmount.value,
          chance: sliderValue.value
        })
        
        // Обновляем баланс
        userStore.updateBalance(response.balance_delta)

        // Отслеживаем результат игры
        const winAmount = response.status ? response.balance_delta + betAmount.value : 0
        analytics.trackGameResult('Dice', response.status ? 'win' : 'loss', betAmount.value, winAmount, response.status ? (100 / sliderValue.value) : 0)

        // Показываем результат
        isWin.value = response.status
        showPicker.value = true
        pickerPosition.value = response.number
        
        // Добавляем в историю
        history.value.unshift({
          id: Date.now(),
          percent: response.number,
          win: response.status
        })
        
        // Ограничиваем историю
        if (history.value.length > 10) {
          history.value = history.value.slice(0, 10)
        }
        
        // Показываем сообщение и отправляем уведомление
        if (response.status) {
          const winAmount = response.balance_delta + betAmount.value
          resultMessage.value = `🎉 Победа! Выигрыш: ${winAmount}₽`
          notify.win(winAmount, 'Dice')
        } else {
          resultMessage.value = `😔 Проигрыш: -${betAmount.value}₽`
          notify.loss(betAmount.value, 'Dice')
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
        loading.value = false
      }
    }

    onMounted(() => {
      updateSlider()
    })

    return {
      sliderValue,
      betAmount,
      loading,
      showPicker,
      pickerPosition,
      isWin,
      resultMessage,
      history,
      canPlay,
      updateSlider,
      maxBet,
      minBet,
      doubleBet,
      halfBet,
      play
    }
  }
}
</script>

<style scoped>
.slider::-webkit-slider-thumb {
  appearance: none;
  height: 20px;
  width: 20px;
  border-radius: 50%;
  background: linear-gradient(45deg, #7c75d9, #8c84ec);
  cursor: pointer;
  box-shadow: 0 2px 6px rgba(0,0,0,0.3);
}

.slider::-moz-range-thumb {
  height: 20px;
  width: 20px;
  border-radius: 50%;
  background: linear-gradient(45deg, #7c75d9, #8c84ec);
  cursor: pointer;
  border: none;
  box-shadow: 0 2px 6px rgba(0,0,0,0.3);
}

.picker.win {
  box-shadow: 0 0 10px rgba(68, 194, 118, 0.8);
}

.picker.lose {
  box-shadow: 0 0 10px rgba(242, 72, 65, 0.8);
}
</style>
