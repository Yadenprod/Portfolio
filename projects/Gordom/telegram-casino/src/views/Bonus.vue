<template>
  <div class="flex flex-col space-y-6">
    <div class="text-center">
      <h1 class="font-deftone text-3xl text-white mb-2">
        <span class="text-violet">БОНУСЫ</span>
      </h1>
      <p class="text-grayLight text-sm">Получайте бонусы и активируйте промокоды</p>
    </div>

    <!-- Ежедневный бонус -->
    <div class="bg-gradient-to-br from-[#202024] to-[#2c2c31] rounded-2xl p-6">
      <div class="flex items-center space-x-4 mb-4">
        <div class="w-12 h-12 bg-green/20 rounded-xl flex items-center justify-center">
          <span class="text-2xl">🎁</span>
        </div>
        <div>
          <h3 class="text-white font-semibold">Ежедневный бонус</h3>
          <p class="text-xs text-grayLight">Получайте бонус каждый день!</p>
        </div>
      </div>

      <div class="space-y-4">
        <div class="text-center">
          <div class="text-3xl font-bold text-green mb-2">{{ dailyBonus?.amount || 50 }}₽</div>
          <p class="text-sm text-grayLight">{{ dailyBonus?.streak || 0 }} дней подряд</p>
        </div>

        <button
          @click="claimDailyBonus"
          :disabled="!dailyBonus?.available || loading"
          class="w-full py-3 bg-green hover:bg-greenHover disabled:opacity-50 disabled:cursor-not-allowed rounded-xl text-white font-semibold transition-all duration-200"
        >
          <span v-if="!loading">{{ dailyBonus?.available ? 'Получить бонус' : 'Уже получен сегодня' }}</span>
          <span v-else class="flex items-center justify-center space-x-2">
            <div class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            <span>Получение...</span>
          </span>
        </button>
      </div>
    </div>

    <!-- Колесо фортуны -->
    <div class="bg-gradient-to-br from-[#202024] to-[#2c2c31] rounded-2xl p-6">
      <div class="flex items-center space-x-4 mb-4">
        <div class="w-12 h-12 bg-violet/20 rounded-xl flex items-center justify-center">
          <span class="text-2xl">🎡</span>
        </div>
        <div>
          <h3 class="text-white font-semibold">Колесо фортуны</h3>
          <p class="text-xs text-grayLight">Крутите колесо и выигрывайте бонусы!</p>
        </div>
      </div>

      <div class="flex flex-col items-center space-y-4">
        <!-- Колесо -->
        <div class="relative">
          <div class="w-48 h-48 relative">
            <svg class="w-full h-full transform rotate-90" viewBox="0 0 200 200">
              <circle cx="100" cy="100" r="90" fill="none" stroke="#7c75d9" stroke-width="4"/>
              <!-- Секторы колеса -->
              <g v-for="(sector, index) in wheelSectors" :key="index">
                <path
                  :d="getSectorPath(index)"
                  :fill="sector.color"
                  stroke="#1b1c20"
                  stroke-width="1"
                />
                <text
                  :x="getTextX(index)"
                  :y="getTextY(index)"
                  :transform="`rotate(${index * 45 + 22.5}, ${getTextX(index)}, ${getTextY(index)})`"
                  class="text-white font-bold text-xs"
                  text-anchor="middle"
                  dominant-baseline="middle"
                >
                  {{ sector.label }}
                </text>
              </g>
              <!-- Центр колеса -->
              <circle cx="100" cy="100" r="30" fill="#1b1c20" stroke="#7c75d9" stroke-width="3"/>
              <!-- Указатель -->
              <polygon points="95,15 105,15 100,35" fill="#f24841"/>
            </svg>

            <!-- Анимация вращения -->
            <div
              v-if="wheelSpinning"
              class="absolute inset-0 w-full h-full animate-spin"
              :style="{ animationDuration: '3s' }"
            >
              <svg class="w-full h-full" viewBox="0 0 200 200">
                <g v-for="(sector, index) in wheelSectors" :key="index">
                  <path
                    :d="getSectorPath(index)"
                    :fill="sector.color"
                    stroke="#1b1c20"
                    stroke-width="1"
                  />
                </g>
              </svg>
            </div>
          </div>
        </div>

        <div class="text-center">
          <p class="text-sm text-grayLight mb-4">Осталось попыток: {{ wheelSpins || 0 }}</p>
          <button
            @click="spinWheel"
            :disabled="!wheelSpins || wheelSpinning || loading"
            class="px-6 py-3 bg-violet hover:bg-violetHover disabled:opacity-50 disabled:cursor-not-allowed rounded-xl text-white font-semibold transition-all duration-200"
          >
            <span v-if="!wheelSpinning">{{ wheelSpins > 0 ? 'Крутить колесо' : 'Нет попыток' }}</span>
            <span v-else>Крутится...</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Доступные бонусы -->
    <div v-if="availableBonuses.length > 0" class="space-y-4">
      <h3 class="text-lg font-semibold text-white">Доступные бонусы</h3>
      <div class="grid gap-4">
        <div
          v-for="bonus in availableBonuses"
          :key="bonus.id"
          class="bg-gradient-to-br from-[#202024] to-[#2c2c31] rounded-xl p-4 flex items-center space-x-4"
        >
          <div class="w-12 h-12 rounded-xl flex items-center justify-center" :class="bonus.iconBg">
            <span class="text-2xl">{{ bonus.icon }}</span>
          </div>
          <div class="flex-1">
            <h4 class="text-white font-semibold">{{ bonus.name }}</h4>
            <p class="text-xs text-grayLight">{{ bonus.description }}</p>
            <p class="text-sm font-bold text-green mt-1">+{{ bonus.reward }}₽</p>
          </div>
          <button
            @click="claimBonus(bonus.id)"
            :disabled="loading"
            class="px-4 py-2 bg-violet hover:bg-violetHover disabled:opacity-50 disabled:cursor-not-allowed rounded-lg text-white text-sm font-medium transition-colors"
          >
            Получить
          </button>
        </div>
      </div>
    </div>

    <!-- Промокоды -->
    <div class="bg-gradient-to-br from-[#202024] to-[#2c2c31] rounded-2xl p-6 space-y-4">
      <div class="flex items-center space-x-4 mb-4">
        <div class="w-12 h-12 bg-orange/20 rounded-xl flex items-center justify-center">
          <span class="text-2xl">🎫</span>
        </div>
        <div>
          <h3 class="text-white font-semibold">Активировать промокод</h3>
          <p class="text-xs text-grayLight">Введите код и получите бонус</p>
        </div>
      </div>

      <div class="space-y-4">
        <input
          v-model="promoCode"
          type="text"
          placeholder="Введите промокод"
          class="w-full p-4 bg-[#1b1c20] rounded-xl text-white placeholder-gray focus:outline-none focus:ring-2 focus:ring-violet text-center text-lg font-mono tracking-wider"
          maxlength="20"
          :disabled="loading"
        />

        <button
          @click="activatePromo"
          :disabled="!promoCode.trim() || loading"
          class="w-full py-3 bg-orange hover:bg-orangeHover disabled:opacity-50 disabled:cursor-not-allowed rounded-xl text-white font-semibold transition-all duration-200"
        >
          <span v-if="!loading">Активировать</span>
          <span v-else class="flex items-center justify-center space-x-2">
            <div class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            <span>Активация...</span>
          </span>
        </button>
      </div>
    </div>

    <!-- История бонусов -->
    <div v-if="bonusHistory.length > 0" class="space-y-4">
      <h3 class="text-lg font-semibold text-white">История бонусов</h3>
      <div class="space-y-2">
        <div
          v-for="item in bonusHistory.slice(0, 10)"
          :key="item.id"
          class="bg-gradient-to-br from-[#202024] to-[#2c2c31] rounded-xl p-4 flex items-center justify-between"
        >
          <div class="flex items-center space-x-3">
            <div class="w-8 h-8 rounded-lg flex items-center justify-center bg-green/20">
              <span class="text-lg">{{ item.type === 'daily' ? '🎁' : item.type === 'promo' ? '🎫' : '🎡' }}</span>
            </div>
            <div>
              <p class="text-white text-sm font-medium">{{ item.description }}</p>
              <p class="text-xs text-grayLight">{{ formatTime(item.created_at) }}</p>
            </div>
          </div>
          <div class="text-green font-bold">+{{ item.amount }}₽</div>
        </div>
      </div>
    </div>

    <!-- Уведомление о результате -->
    <div v-if="resultMessage" class="fixed top-4 left-4 right-4 z-50">
      <div :class="isSuccess ? 'bg-green/90' : 'bg-red/90'" class="backdrop-blur-sm rounded-xl p-4 text-white text-center animate-bounce">
        {{ resultMessage }}
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '../stores/user'
import {
  getDailyBonus,
  claimDailyBonus,
  getAvailableBonuses,
  claimBonus,
  getWheelOfFortune,
  spinWheelOfFortune,
  getBonusHistory,
  activatePromocode
} from '../api/endpoints'
import { notify } from '../services/notifications'

export default {
  name: 'Bonus',
  setup() {
    const userStore = useUserStore()

    const loading = ref(false)
    const promoCode = ref('')
    const resultMessage = ref('')
    const isSuccess = ref(false)

    const dailyBonus = ref(null)
    const availableBonuses = ref([])
    const wheelData = ref(null)
    const bonusHistory = ref([])
    const wheelSpinning = ref(false)

    const wheelSpins = computed(() => wheelData.value?.spins || 0)

    const wheelSectors = ref([
      { label: 'x2', color: '#f24841', multiplier: 2 },
      { label: '50₽', color: '#44c276', amount: 50 },
      { label: 'x5', color: '#7c75d9', multiplier: 5 },
      { label: '100₽', color: '#f08929', amount: 100 },
      { label: 'x10', color: '#d92c9f', multiplier: 10 },
      { label: '200₽', color: '#2c2c31', amount: 200 },
      { label: 'x3', color: '#44c276', multiplier: 3 },
      { label: '25₽', color: '#7c75d9', amount: 25 }
    ])

    const getSectorPath = (index) => {
      const angle = index * 45
      const startAngle = (angle - 22.5) * Math.PI / 180
      const endAngle = (angle + 22.5) * Math.PI / 180
      const radius = 90
      const centerX = 100
      const centerY = 100

      const x1 = centerX + radius * Math.cos(startAngle)
      const y1 = centerY + radius * Math.sin(startAngle)
      const x2 = centerX + radius * Math.cos(endAngle)
      const y2 = centerY + radius * Math.sin(endAngle)

      return `M ${centerX} ${centerY} L ${x1} ${y1} A ${radius} ${radius} 0 0 1 ${x2} ${y2} Z`
    }

    const getTextX = (index) => {
      const angle = (index * 45 + 22.5) * Math.PI / 180
      return 100 + 60 * Math.cos(angle)
    }

    const getTextY = (index) => {
      const angle = (index * 45 + 22.5) * Math.PI / 180
      return 100 + 60 * Math.sin(angle)
    }

    const formatTime = (timestamp) => {
      const date = new Date(timestamp)
      const now = new Date()
      const diff = now - date

      if (diff < 60000) return 'только что'
      if (diff < 3600000) return `${Math.floor(diff / 60000)} мин назад`
      if (diff < 86400000) return `${Math.floor(diff / 3600000)} ч назад`
      return date.toLocaleDateString('ru-RU', { day: 'numeric', month: 'short' })
    }

    const showMessage = (message, success = true) => {
      resultMessage.value = message
      isSuccess.value = success
      setTimeout(() => {
        resultMessage.value = ''
      }, 3000)
    }

    const loadDailyBonus = async () => {
      try {
        const data = await getDailyBonus()
        dailyBonus.value = data
      } catch (error) {
        console.error('Failed to load daily bonus:', error)
      }
    }

    const loadAvailableBonuses = async () => {
      try {
        const bonuses = await getAvailableBonuses()
        availableBonuses.value = bonuses.map(bonus => ({
          ...bonus,
          icon: bonus.type === 'deposit' ? '💳' : bonus.type === 'game' ? '🎮' : '🎁',
          iconBg: bonus.type === 'deposit' ? 'bg-blue/20' : bonus.type === 'game' ? 'bg-green/20' : 'bg-purple/20'
        }))
      } catch (error) {
        console.error('Failed to load bonuses:', error)
      }
    }

    const loadWheelData = async () => {
      try {
        const data = await getWheelOfFortune()
        wheelData.value = data
      } catch (error) {
        console.error('Failed to load wheel data:', error)
      }
    }

    const loadBonusHistory = async () => {
      try {
        const history = await getBonusHistory()
        bonusHistory.value = history
      } catch (error) {
        console.error('Failed to load bonus history:', error)
      }
    }

    const claimDailyBonus = async () => {
      if (!dailyBonus.value?.available) return

      loading.value = true
      try {
        const result = await claimDailyBonus()
        if (result.success) {
          userStore.updateBalance(result.balance_delta)
          dailyBonus.value.available = false
          showMessage(`Ежедневный бонус получен! +${result.reward}₽`)
          notify.bonus('Ежедневный бонус', result.reward)
          loadBonusHistory()
        } else {
          showMessage(result.message, false)
        }
      } catch (error) {
        showMessage('Ошибка при получении бонуса', false)
      } finally {
        loading.value = false
      }
    }

    const claimBonus = async (bonusId) => {
      loading.value = true
      try {
        const result = await claimBonus(bonusId)
        if (result.success) {
          userStore.updateBalance(result.balance_delta)
          showMessage(`Бонус получен! +${result.reward}₽`)
          notify.bonus('Бонус', result.reward)
          loadAvailableBonuses()
          loadBonusHistory()
        } else {
          showMessage(result.message, false)
        }
      } catch (error) {
        showMessage('Ошибка при получении бонуса', false)
      } finally {
        loading.value = false
      }
    }

    const spinWheel = async () => {
      if (!wheelSpins.value || wheelSpinning.value) return

      wheelSpinning.value = true
      loading.value = true

      try {
        const result = await spinWheelOfFortune()
        if (result.success) {
          // Анимация вращения
          await new Promise(resolve => setTimeout(resolve, 3000))

          userStore.updateBalance(result.balance_delta)
          wheelData.value.spins--
          showMessage(`Колесо фортуны: ${result.reward > 0 ? `+${result.reward}₽` : `x${result.multiplier}`}`)
          notify.bonus('Колесо фортуны', result.reward || (result.multiplier * 10))
          loadBonusHistory()
        } else {
          showMessage(result.message, false)
        }
      } catch (error) {
        showMessage('Ошибка при вращении колеса', false)
      } finally {
        wheelSpinning.value = false
        loading.value = false
      }
    }

    const activatePromo = async () => {
      if (!promoCode.value.trim()) return

      loading.value = true
      try {
        const result = await activatePromocode(promoCode.value.trim())
        if (result.success) {
          userStore.updateBalance(result.balance_delta)
          promoCode.value = ''
          showMessage(`Промокод активирован! +${result.reward}₽`)
          notify.bonus('Промокод', result.reward)
          loadBonusHistory()
        } else {
          showMessage(result.message, false)
        }
      } catch (error) {
        showMessage('Ошибка при активации промокода', false)
      } finally {
        loading.value = false
      }
    }

    onMounted(() => {
      loadDailyBonus()
      loadAvailableBonuses()
      loadWheelData()
      loadBonusHistory()
    })

    return {
      loading,
      promoCode,
      resultMessage,
      isSuccess,
      dailyBonus,
      availableBonuses,
      wheelData,
      bonusHistory,
      wheelSpinning,
      wheelSectors,
      wheelSpins,
      getSectorPath,
      getTextX,
      getTextY,
      formatTime,
      claimDailyBonus,
      claimBonus,
      spinWheel,
      activatePromo
    }
  }
}
</script>