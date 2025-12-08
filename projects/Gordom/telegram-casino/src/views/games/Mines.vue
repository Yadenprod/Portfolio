<template>
  <div class="flex flex-col space-y-6">
    <!-- Заголовок игры -->
    <div class="text-center">
      <h1 class="font-deftone text-3xl text-white mb-2">
        <span class="text-violet">MINES</span>
      </h1>
      <p class="text-grayLight text-sm">Найди все сокровища, избегая мин!</p>
    </div>

    <!-- Игровое поле -->
    <div class="bg-[#2c2c31] rounded-2xl p-6 space-y-6">
      <!-- Настройки игры -->
      <div class="grid grid-cols-2 gap-4">
        <div class="space-y-2">
          <label class="text-sm font-medium text-grayLight">Количество мин:</label>
          <select 
            v-model="minesCount" 
            class="w-full p-3 bg-[#1b1c20] rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-violet"
            :disabled="gameStarted"
          >
            <option value="3">3 мины</option>
            <option value="5">5 мин</option>
            <option value="10">10 мин</option>
            <option value="15">15 мин</option>
            <option value="20">20 мин</option>
          </select>
        </div>
        
        <div class="space-y-2">
          <label class="text-sm font-medium text-grayLight">Множитель:</label>
          <div class="p-3 bg-[#1b1c20] rounded-lg text-center">
            <span class="text-xl font-bold text-violet">{{ currentMultiplier }}x</span>
          </div>
        </div>
      </div>

      <!-- Сетка игры -->
      <div class="flex justify-center">
        <div class="grid grid-cols-5 gap-1">
          <div 
            v-for="(cell, index) in gameGrid" 
            :key="index"
            @click="openCell(index)"
            class="w-12 h-12 rounded-lg flex items-center justify-center text-white font-bold cursor-pointer transition-all duration-200"
            :class="getCellClass(cell)"
          >
            <span v-if="cell.isRevealed">
              <span v-if="cell.isMine" class="text-red">💣</span>
              <span v-else-if="cell.isGem" class="text-green">💎</span>
              <span v-else class="text-grayLight">{{ cell.neighborMines || '' }}</span>
            </span>
            <span v-else-if="cell.isFlagged" class="text-yellow">🚩</span>
            <span v-else class="text-grayLight">?</span>
          </div>
        </div>
      </div>

      <!-- Статистика -->
      <div class="grid grid-cols-3 gap-4 text-center">
        <div class="p-3 bg-[#1b1c20] rounded-lg">
          <div class="text-sm text-gray">Открыто</div>
          <div class="text-lg font-bold text-white">{{ openedCells }}</div>
        </div>
        <div class="p-3 bg-[#1b1c20] rounded-lg">
          <div class="text-sm text-gray">Мин</div>
          <div class="text-lg font-bold text-red">{{ minesCount }}</div>
        </div>
        <div class="p-3 bg-[#1b1c20] rounded-lg">
          <div class="text-sm text-gray">Выигрыш</div>
          <div class="text-lg font-bold text-green">{{ potentialWin }}</div>
        </div>
      </div>

      <!-- Ставка -->
      <div class="space-y-4">
        <label class="text-sm font-medium text-grayLight">Ваша ставка:</label>
        
        <!-- Быстрые кнопки -->
        <div class="grid grid-cols-4 gap-2">
          <button 
            @click="setBet(10)"
            class="p-2 bg-[#1b1c20] rounded-lg text-xs font-medium text-grayLight hover:bg-[#35353c] transition-colors"
            :disabled="gameStarted"
          >
            Min
          </button>
          <button 
            @click="setBet(bet * 0.5)"
            class="p-2 bg-[#1b1c20] rounded-lg text-xs font-medium text-grayLight hover:bg-[#35353c] transition-colors"
            :disabled="gameStarted"
          >
            1/2
          </button>
          <button 
            @click="setBet(bet * 2)"
            class="p-2 bg-[#1b1c20] rounded-lg text-xs font-medium text-grayLight hover:bg-[#35353c] transition-colors"
            :disabled="gameStarted"
          >
            x2
          </button>
          <button 
            @click="setBet(1000)"
            class="p-2 bg-[#1b1c20] rounded-lg text-xs font-medium text-grayLight hover:bg-[#35353c] transition-colors"
            :disabled="gameStarted"
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
          :disabled="gameStarted"
        />
      </div>

      <!-- Кнопки управления -->
      <div class="grid grid-cols-2 gap-4">
        <button
          @click="startGame"
          :disabled="!canStart || gameStarted"
          class="py-3 bg-green hover:bg-greenHover disabled:opacity-50 disabled:cursor-not-allowed rounded-xl text-white font-semibold transition-all duration-200"
        >
          Начать игру
        </button>
        
        <button
          @click="cashOut"
          :disabled="!canCashOut"
          class="py-3 bg-violet hover:bg-violetHover disabled:opacity-50 disabled:cursor-not-allowed rounded-xl text-white font-semibold transition-all duration-200"
        >
          Забрать {{ potentialWin }}
        </button>
      </div>
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
            {{ gameResult.win ? '💎' : '💣' }}
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
  name: 'Mines',
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
    const minesCount = ref(5)
    const gameStarted = ref(false)
    const gameGrid = ref([])
    const showResult = ref(false)
    const gameResult = ref({})
    const history = ref([])

    const GRID_SIZE = 25 // 5x5 сетка

    const currentMultiplier = computed(() => {
      if (openedCells.value === 0) return 1
      return (1 + (openedCells.value * 0.1)).toFixed(2)
    })

    const openedCells = computed(() => {
      return gameGrid.value.filter(cell => cell.isRevealed && !cell.isMine).length
    })

    const potentialWin = computed(() => {
      return (bet.value * parseFloat(currentMultiplier.value)).toFixed(2)
    })

    const canStart = computed(() => {
      return bet.value > 0 && bet.value <= userStore.balance && !gameStarted.value
    })

    const canCashOut = computed(() => {
      return gameStarted.value && openedCells.value > 0
    })

    const initializeGrid = () => {
      gameGrid.value = Array(GRID_SIZE).fill(null).map(() => ({
        isRevealed: false,
        isMine: false,
        isGem: false,
        isFlagged: false,
        neighborMines: 0
      }))
    }

    const placeMines = () => {
      const minePositions = []
      while (minePositions.length < minesCount.value) {
        const pos = Math.floor(Math.random() * GRID_SIZE)
        if (!minePositions.includes(pos)) {
          minePositions.push(pos)
        }
      }
      
      minePositions.forEach(pos => {
        gameGrid.value[pos].isMine = true
      })
    }

    const calculateNeighborMines = (index) => {
      const row = Math.floor(index / 5)
      const col = index % 5
      let count = 0
      
      for (let i = -1; i <= 1; i++) {
        for (let j = -1; j <= 1; j++) {
          const newRow = row + i
          const newCol = col + j
          const newIndex = newRow * 5 + newCol
          
          if (newRow >= 0 && newRow < 5 && newCol >= 0 && newCol < 5 && newIndex !== index) {
            if (gameGrid.value[newIndex].isMine) {
              count++
            }
          }
        }
      }
      
      return count
    }

    const setBet = (amount) => {
      bet.value = Math.max(1, Math.min(amount, userStore.balance))
    }

    const validateBet = () => {
      if (bet.value < 1) bet.value = 1
      if (bet.value > userStore.balance) bet.value = userStore.balance
    }

    const startGame = async () => {
      if (!canStart.value) return

      try {
        // Отправляем запрос на начало игры через API
        const response = await postBet('mines', {
          amount: bet.value,
          action: 'start',
          mines_count: minesCount.value
        })

        if (response.success) {
          gameStarted.value = true

          // Инициализируем сетку с данными от сервера
          if (response.grid) {
            gameGrid.value = response.grid.map(cell => ({
              isRevealed: cell.is_revealed || false,
              isMine: cell.is_mine || false,
              isGem: cell.is_gem || false,
              isFlagged: false,
              neighborMines: cell.neighbor_mines || 0
            }))
          } else {
            initializeGrid()
          }

          // Списываем ставку
          userStore.updateBalance(-bet.value)
        }
      } catch (error) {
        resultMessage.value = '❌ Ошибка при начале игры'
        setTimeout(() => {
          resultMessage.value = ''
        }, 3000)
      }
    }

    const openCell = async (index) => {
      if (!gameStarted.value || gameGrid.value[index].isRevealed || gameGrid.value[index].isFlagged) {
        return
      }

      try {
        // Отправляем действие через API
        const response = await postBet('mines', {
          amount: bet.value,
          action: 'open',
          position: index,
          mines_count: minesCount.value
        })

        if (response.success) {
          // Обновляем состояние игры
          gameGrid.value[index].isRevealed = true
          gameGrid.value[index].isMine = response.cell.is_mine
          gameGrid.value[index].isGem = response.cell.is_gem

          if (response.cell.is_mine) {
            // Показываем все мины
            response.grid.forEach((cell, idx) => {
              gameGrid.value[idx].isMine = cell.is_mine
              gameGrid.value[idx].isRevealed = true
            })
            endGame(false)
          } else if (response.game_ended) {
            // Игра завершена успешно
            endGame(true)
          }

          // Обновляем баланс
          userStore.updateBalance(response.balance_delta)
        }
      } catch (error) {
        resultMessage.value = '❌ Ошибка при открытии клетки'
        setTimeout(() => {
          resultMessage.value = ''
        }, 3000)
      }
    }

    const cashOut = async () => {
      if (!canCashOut.value) return

      try {
        const response = await postBet('mines', {
          amount: bet.value,
          action: 'cashout'
        })

        if (response.success) {
          endGame(true, response)
        }
      } catch (error) {
        resultMessage.value = '❌ Ошибка при выводе средств'
        setTimeout(() => {
          resultMessage.value = ''
        }, 3000)
      }
    }

    const endGame = (win, apiResponse = null) => {
      gameStarted.value = false

      let winAmount = 0
      let multiplier = 1

      if (apiResponse) {
        winAmount = apiResponse.win_amount || 0
        multiplier = apiResponse.multiplier || 1
        userStore.updateBalance(apiResponse.balance_delta || 0)
      } else {
        winAmount = win ? parseFloat(potentialWin.value) : 0
        multiplier = parseFloat(currentMultiplier.value)

        // Обновление баланса
        if (win) {
          userStore.updateBalance(winAmount - bet.value)
        } else {
          userStore.updateBalance(-bet.value)
        }
      }

      // Добавление в историю
      history.value.unshift({
        multiplier: multiplier,
        win: win
      })

      // Ограничение истории
      if (history.value.length > 10) {
        history.value = history.value.slice(0, 10)
      }

      // Показ результата
      gameResult.value = {
        win: win,
        winAmount: winAmount.toFixed(2)
      }

      // Отправляем уведомление
      if (win) {
        notify.win(winAmount, 'Mines')
      } else {
        notify.loss(bet.value, 'Mines')
      }

      showResult.value = true
    }

    const getCellClass = (cell) => {
      if (cell.isFlagged) {
        return 'bg-yellow/20 hover:bg-yellow/30'
      }
      if (cell.isRevealed) {
        if (cell.isMine) {
          return 'bg-red/20'
        }
        return 'bg-green/20'
      }
      return 'bg-[#1b1c20] hover:bg-[#35353c]'
    }

    const closeResult = () => {
      showResult.value = false
      initializeGrid()
    }

    onMounted(() => {
      initializeGrid()
      
      // Инициализация истории
      for (let i = 0; i < 5; i++) {
        history.value.push({
          multiplier: (1 + Math.random() * 2).toFixed(2),
          win: Math.random() > 0.5
        })
      }
    })

    return {
      bet,
      minesCount,
      gameStarted,
      gameGrid,
      showResult,
      gameResult,
      history,
      resultMessage,
      currentMultiplier,
      openedCells,
      potentialWin,
      canStart,
      canCashOut,
      setBet,
      validateBet,
      startGame,
      openCell,
      cashOut,
      getCellClass,
      closeResult
    }
  }
}
</script>
