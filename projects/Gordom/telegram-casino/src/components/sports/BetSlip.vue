<template>
  <div class="bet-slip">
    <div class="slip-header">
      <h3 class="slip-title">Корзина ставок</h3>
      <button @click="clearSlip" class="clear-btn">
        <span>✕</span>
      </button>
    </div>

    <div class="slip-content">
      <div class="bets-list">
        <div
          v-for="bet in betsStore.betSlip"
          :key="bet.id"
          class="bet-item"
        >
          <div class="bet-info">
            <div class="bet-event">{{ bet.event_name }}</div>
            <div class="bet-type">{{ getBetTypeName(bet.bet_type) || bet.bet_type_name }}</div>
            <div class="bet-odds">Коэф: {{ formatOdds(bet.odds) }}</div>
          </div>

          <div class="bet-amount">
            <input
              type="number"
              v-model.number="bet.amount"
              @input="onAmountChange(bet)"
              :min="minBetAmount"
              :max="userStore.balance"
              step="10"
              class="amount-input"
              placeholder="0"
            />
            <span class="currency">₽</span>
          </div>

          <div class="bet-potential">
            <div class="potential-win">
              ~{{ formatCurrency(bet.potential_win) }}
            </div>
          </div>

          <button @click="removeBet(bet)" class="remove-bet-btn">
            <span>×</span>
          </button>
        </div>
      </div>

      <div class="slip-footer">
        <div class="totals">
          <div class="total-stake">
            <span class="label">Общая ставка:</span>
            <span class="value">{{ formatCurrency(betsStore.totalStake) }}</span>
          </div>
          <div class="total-win">
            <span class="label">Возможный выигрыш:</span>
            <span class="value win">{{ formatCurrency(betsStore.potentialWin) }}</span>
          </div>
        </div>

        <div class="slip-actions">
          <button
            @click="placeAllBets"
            :disabled="!canPlaceBets"
            class="place-bets-btn"
          >
            <span v-if="placingBets">Размещение...</span>
            <span v-else>Сделать ставки</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useUserStore } from '../../stores/user'
import { useBetsStore } from '../../stores/bets'

export default {
  name: 'BetSlip',
  setup() {
    const userStore = useUserStore()
    const betsStore = useBetsStore()

    return {
      userStore,
      betsStore
    }
  },
  data() {
    return {
      placingBets: false,
      minBetAmount: 10
    }
  },
  computed: {
    canPlaceBets() {
      return this.betsStore.betSlip.length > 0 &&
             this.betsStore.betSlip.every(bet => bet.amount >= this.minBetAmount) &&
             this.betsStore.totalStake <= this.userStore.balance &&
             !this.placingBets
    }
  },
  methods: {
    onAmountChange(bet) {
      this.betsStore.updateBetAmount(bet.id, bet.amount)
    },

    removeBet(bet) {
      this.betsStore.removeFromBetSlip(bet)
    },

    clearSlip() {
      this.betsStore.clearBetSlip()
      this.$emit('slip-cleared')
    },

    async placeAllBets() {
      if (!this.canPlaceBets) return

      this.placingBets = true

      try {
        const results = await this.betsStore.placeAllBets()

        // Проверяем результаты
        const successful = results.filter(r => r.success)
        const failed = results.filter(r => !r.success)

        if (successful.length > 0) {
          this.showNotification(`Успешно размещено ${successful.length} ставок!`, 'success')
        }

        if (failed.length > 0) {
          this.showNotification(`Не удалось разместить ${failed.length} ставок`, 'error')
        }

        this.$emit('bet-placed', results)
      } catch (error) {
        console.error('Failed to place bets:', error)
        this.showNotification('Ошибка при размещении ставок', 'error')
      } finally {
        this.placingBets = false
      }
    },

    formatOdds(odds) {
      return Number(odds).toFixed(2)
    },

    formatCurrency(amount) {
      return Number(amount).toFixed(2) + ' ₽'
    },

    getBetTypeName(betType) {
      const betTypes = {
        // Основные исходы
        home: 'П1',
        draw: 'Ничья',
        away: 'П2',

        // Тоталы
        over_2_5: 'Тотал > 2.5',
        under_2_5: 'Тотал < 2.5',
        over_220_5: 'Тотал > 220.5',
        under_220_5: 'Тотал < 220.5',

        // CS:GO ставки
        map_handicap: 'Гандикап карт',
        total_maps: 'Тотал карт',
        next_round_home: 'След. раунд - хозяева',
        next_round_away: 'След. раунд - гости',

        // Dota 2 ставки
        first_blood_home: 'First Blood - хозяева',
        first_blood_away: 'First Blood - гости',
        total_kills_over_40: 'Убийств >40',
        total_kills_under_40: 'Убийств <40',
        next_kill_home: 'След. убийство - хозяева',
        next_kill_away: 'След. убийство - гости',

        // League of Legends ставки
        baron_control_home: 'Барон - хозяева',
        baron_control_away: 'Барон - гости',

        // Valorant ставки
        total_rounds_over_26: 'Раундов >26',
        total_rounds_under_26: 'Раундов <26',

        // PUBG ставки
        chicken_dinner_home: 'Победа - хозяева',
        chicken_dinner_away: 'Победа - гости',
        total_kills_over_25: 'Убийств >25',
        total_kills_under_25: 'Убийств <25',

        // Apex Legends ставки
        total_kills_over_30: 'Убийств >30',
        total_kills_under_30: 'Убийств <30',

        // Rainbow Six Siege ставки
        total_rounds_over_12: 'Раундов >12',
        total_rounds_under_12: 'Раундов <12'
      }

      return betTypes[betType]
    },

    showNotification(message, type) {
      // Здесь можно интегрировать с системой уведомлений приложения
      console.log(`[${type.toUpperCase()}] ${message}`)
      alert(message) // Временное решение
    }
  }
}
</script>

<style scoped>
.bet-slip {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(145deg, #ffffff 0%, #f8f9ff 100%);
  border-radius: 25px 25px 0 0;
  box-shadow:
    0 -8px 32px rgba(0, 0, 0, 0.15),
    0 -2px 8px rgba(0, 0, 0, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.8);
  z-index: 1000;
  max-height: 70vh;
  overflow: hidden;
  animation: slideUp 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

@keyframes slideUp {
  from {
    transform: translateY(100%);
  }
  to {
    transform: translateY(0);
  }
}

.slip-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 25px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  position: relative;
  overflow: hidden;
}

.slip-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
  animation: shimmer 2s infinite;
}

@keyframes shimmer {
  0% { left: -100%; }
  100% { left: 100%; }
}

.slip-title {
  font-size: 1.2rem;
  font-weight: bold;
  margin: 0;
}

.clear-btn {
  background: rgba(255, 255, 255, 0.2);
  border: 2px solid rgba(255, 255, 255, 0.3);
  color: white;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  backdrop-filter: blur(10px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.clear-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.5);
  transform: scale(1.1) rotate(90deg);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.slip-content {
  max-height: calc(70vh - 80px);
  overflow-y: auto;
}

.bets-list {
  padding: 0 20px;
}

.bet-item {
  display: grid;
  grid-template-columns: 1fr auto auto auto;
  gap: 15px;
  align-items: center;
  padding: 15px 0;
  border-bottom: 1px solid #e9ecef;
}

.bet-item:last-child {
  border-bottom: none;
}

.bet-info {
  min-width: 0;
}

.bet-event {
  font-weight: 600;
  color: #333;
  font-size: 0.9rem;
  margin-bottom: 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.bet-type {
  font-size: 0.8rem;
  color: #6c757d;
  margin-bottom: 2px;
}

.bet-odds {
  font-size: 0.8rem;
  color: #667eea;
  font-weight: 500;
}

.bet-amount {
  position: relative;
  width: 80px;
}

.amount-input {
  width: 100%;
  padding: 8px 25px 8px 10px;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 600;
  text-align: right;
  background: #f8f9fa;
  transition: all 0.3s ease;
}

.amount-input:focus {
  outline: none;
  border-color: #667eea;
  background: white;
}

.amount-input::placeholder {
  color: #adb5bd;
}

.currency {
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  color: #6c757d;
  font-size: 0.8rem;
  font-weight: 500;
  pointer-events: none;
}

.bet-potential {
  text-align: right;
  min-width: 80px;
}

.potential-win {
  font-size: 0.9rem;
  font-weight: 600;
  color: #28a745;
}

.remove-bet-btn {
  background: #dc3545;
  color: white;
  border: none;
  width: 25px;
  height: 25px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.remove-bet-btn:hover {
  background: #c82333;
  transform: scale(1.1);
}

.slip-footer {
  padding: 20px;
  background: #f8f9fa;
  border-top: 1px solid #e9ecef;
}

.totals {
  margin-bottom: 20px;
}

.total-stake,
.total-win {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  font-size: 0.9rem;
}

.total-stake:last-child,
.total-win:last-child {
  margin-bottom: 0;
}

.label {
  color: #6c757d;
}

.value {
  font-weight: 600;
}

.value.win {
  color: #28a745;
  font-size: 1.1rem;
}

.slip-actions {
  display: flex;
  justify-content: center;
}

.place-bets-btn {
  background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
  color: white;
  border: none;
  padding: 18px 35px;
  border-radius: 30px;
  font-size: 1.1rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  min-width: 220px;
  position: relative;
  overflow: hidden;
  text-transform: uppercase;
  letter-spacing: 1px;
  box-shadow:
    0 4px 15px rgba(40, 167, 69, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.place-bets-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.6s;
}

.place-bets-btn:hover:not(:disabled)::before {
  left: 100%;
}

.place-bets-btn:hover:not(:disabled) {
  transform: translateY(-3px) scale(1.02);
  box-shadow:
    0 8px 25px rgba(40, 167, 69, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
}

.place-bets-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

/* Адаптивность */
@media (max-width: 768px) {
  .bet-item {
    grid-template-columns: 1fr;
    gap: 10px;
  }

  .bet-info,
  .bet-amount,
  .bet-potential {
    text-align: center;
  }

  .bet-amount,
  .bet-potential {
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .place-bets-btn {
    min-width: 150px;
    padding: 12px 24px;
  }
}

@media (max-width: 480px) {
  .bet-slip {
    max-height: 80vh;
  }

  .slip-header {
    padding: 15px;
  }

  .bets-list,
  .slip-footer {
    padding: 0 15px;
  }

  .bet-item {
    padding: 10px 0;
  }

  .amount-input {
    padding: 6px 20px 6px 8px;
  }
}
</style>
