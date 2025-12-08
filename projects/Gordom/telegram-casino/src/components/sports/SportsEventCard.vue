<template>
  <div class="event-card">
    <!-- Заголовок события -->
    <div class="event-header">
      <div class="event-info">
        <div class="sport-badge">{{ event.sport_name }}</div>
        <div class="league-name">{{ event.league }}</div>
      </div>
      <div class="event-time">
        <div v-if="isLive" class="live-badge">
          <span class="live-dot"></span>
          <span v-if="event.sport === 'football' || event.sport === 'basketball'">
            {{ event.minute }}'
          </span>
          <span v-else-if="event.sport === 'csgo'">
            {{ event.round || 0 }} раунд
          </span>
          <span v-else-if="event.sport === 'dota2'">
            {{ event.kills ? (event.kills.home + event.kills.away) : 0 }} убийств
          </span>
          <span v-else-if="event.sport === 'valorant'">
            {{ event.round || 0 }} раунд
          </span>
          <span v-else-if="event.sport === 'pubg'">
            {{ event.players_alive || 0 }} игроков
          </span>
          <span v-else-if="event.sport === 'apex'">
            {{ event.kills ? (event.kills.home + event.kills.away) : 0 }} убийств
          </span>
          <span v-else-if="event.sport === 'lol'">
            {{ event.minute || 0 }} мин
          </span>
          <span v-else>
            Live
          </span>
        </div>
        <div v-else class="start-time">
          {{ formatTime(event.start_time) }}
        </div>
      </div>
    </div>

    <!-- Команды -->
    <div class="teams-section">
      <div class="team home-team">
        <div class="team-name">{{ event.home_team }}</div>
        <div v-if="isLive && event.current_score" class="team-score">
          <span v-if="['csgo', 'valorant'].includes(event.sport)">{{ event.current_score.home }}</span>
          <span v-else-if="['dota2', 'apex'].includes(event.sport) && event.kills">{{ event.kills.home }}</span>
          <span v-else-if="event.sport === 'pubg'">{{ event.current_score.home }}</span>
          <span v-else>{{ event.current_score.home }}</span>
        </div>
        <div v-if="isLive" class="game-info">
          <span v-if="event.sport === 'csgo' && event.current_map">{{ event.current_map }} ({{ event.map_score }})</span>
          <span v-else-if="event.sport === 'valorant' && event.current_map">{{ event.current_map }} ({{ event.map_score }})</span>
          <span v-else-if="event.sport === 'pubg' && event.current_map">{{ event.current_map }}</span>
          <span v-else-if="event.sport === 'apex' && event.current_zone">{{ event.current_zone }}</span>
        </div>
      </div>

      <div class="vs-indicator">
        <span v-if="isLive && event.current_score">VS</span>
        <span v-else>VS</span>
        <div v-if="event.game_type" class="game-type">{{ event.game_type.toUpperCase() }}</div>
      </div>

      <div class="team away-team">
        <div class="team-name">{{ event.away_team }}</div>
        <div v-if="isLive && event.current_score" class="team-score">
          <span v-if="event.sport === 'csgo' && event.map_score">{{ event.current_score.away }}</span>
          <span v-else-if="event.sport === 'dota2' && event.kills">{{ event.kills.away }}</span>
          <span v-else>{{ event.current_score.away }}</span>
        </div>
      </div>
    </div>

    <!-- Коэффициенты -->
    <div class="odds-section">
      <!-- Основные исходы -->
      <div class="odds-group">
        <h4 class="odds-title">Основные исходы</h4>
        <div class="odds-buttons">
          <button
            v-if="event.odds.home"
            @click="addBet('home', event.odds.home)"
            :class="['odds-btn', { selected: isBetSelected('home') }]"
          >
            <span class="bet-type">П1</span>
            <span class="odds-value">{{ formatOdds(event.odds.home) }}</span>
          </button>

          <button
            v-if="event.odds.draw"
            @click="addBet('draw', event.odds.draw)"
            :class="['odds-btn', { selected: isBetSelected('draw') }]"
          >
            <span class="bet-type">Н</span>
            <span class="odds-value">{{ formatOdds(event.odds.draw) }}</span>
          </button>

          <button
            v-if="event.odds.away"
            @click="addBet('away', event.odds.away)"
            :class="['odds-btn', { selected: isBetSelected('away') }]"
          >
            <span class="bet-type">П2</span>
            <span class="odds-value">{{ formatOdds(event.odds.away) }}</span>
          </button>
        </div>
      </div>

      <!-- Тоталы -->
      <div class="odds-group" v-if="event.odds.over_2_5 || event.odds.over_220_5">
        <h4 class="odds-title">Тоталы</h4>
        <div class="odds-buttons">
          <button
            v-if="event.odds.over_2_5"
            @click="addBet('over_2_5', event.odds.over_2_5)"
            :class="['odds-btn', { selected: isBetSelected('over_2_5') }]"
          >
            <span class="bet-type">>2.5</span>
            <span class="odds-value">{{ formatOdds(event.odds.over_2_5) }}</span>
          </button>

          <button
            v-if="event.odds.under_2_5"
            @click="addBet('under_2_5', event.odds.under_2_5)"
            :class="['odds-btn', { selected: isBetSelected('under_2_5') }]"
          >
            <span class="bet-type"><2.5</span>
            <span class="odds-value">{{ formatOdds(event.odds.under_2_5) }}</span>
          </button>

          <button
            v-if="event.odds.over_220_5"
            @click="addBet('over_220_5', event.odds.over_220_5)"
            :class="['odds-btn', { selected: isBetSelected('over_220_5') }]"
          >
            <span class="bet-type">>220.5</span>
            <span class="odds-value">{{ formatOdds(event.odds.over_220_5) }}</span>
          </button>

          <button
            v-if="event.odds.under_220_5"
            @click="addBet('under_220_5', event.odds.under_220_5)"
            :class="['odds-btn', { selected: isBetSelected('under_220_5') }]"
          >
            <span class="bet-type"><220.5</span>
            <span class="odds-value">{{ formatOdds(event.odds.under_220_5) }}</span>
          </button>
        </div>
      </div>

      <!-- CS:GO ставки -->
      <div class="odds-group" v-if="event.sport === 'csgo'">
        <h4 class="odds-title">CS:GO ставки</h4>
        <div class="odds-buttons">
          <button
            v-if="event.odds.map_handicap"
            @click="addBet('map_handicap', event.odds.map_handicap)"
            :class="['odds-btn', { selected: isBetSelected('map_handicap') }]"
          >
            <span class="bet-type">Гандикап карт</span>
            <span class="odds-value">{{ formatOdds(event.odds.map_handicap) }}</span>
          </button>

          <button
            v-if="event.odds.total_maps"
            @click="addBet('total_maps', event.odds.total_maps)"
            :class="['odds-btn', { selected: isBetSelected('total_maps') }]"
          >
            <span class="bet-type">Тотал карт</span>
            <span class="odds-value">{{ formatOdds(event.odds.total_maps) }}</span>
          </button>

          <button
            v-if="event.odds.next_round_home && isLive"
            @click="addBet('next_round_home', event.odds.next_round_home)"
            :class="['odds-btn', { selected: isBetSelected('next_round_home') }]"
          >
            <span class="bet-type">След. раунд {{ event.home_team.substring(0, 3).toUpperCase() }}</span>
            <span class="odds-value">{{ formatOdds(event.odds.next_round_home) }}</span>
          </button>
        </div>
      </div>

      <!-- Dota 2 ставки -->
      <div class="odds-group" v-if="event.sport === 'dota2'">
        <h4 class="odds-title">Dota 2 ставки</h4>
        <div class="odds-buttons">
          <button
            v-if="event.odds.first_blood_home"
            @click="addBet('first_blood_home', event.odds.first_blood_home)"
            :class="['odds-btn', { selected: isBetSelected('first_blood_home') }]"
          >
            <span class="bet-type">First Blood {{ event.home_team.substring(0, 3).toUpperCase() }}</span>
            <span class="odds-value">{{ formatOdds(event.odds.first_blood_home) }}</span>
          </button>

          <button
            v-if="event.odds.total_kills_over_40"
            @click="addBet('total_kills_over_40', event.odds.total_kills_over_40)"
            :class="['odds-btn', { selected: isBetSelected('total_kills_over_40') }]"
          >
            <span class="bet-type">Убийств >40</span>
            <span class="odds-value">{{ formatOdds(event.odds.total_kills_over_40) }}</span>
          </button>

          <button
            v-if="event.odds.next_kill_home && isLive"
            @click="addBet('next_kill_home', event.odds.next_kill_home)"
            :class="['odds-btn', { selected: isBetSelected('next_kill_home') }]"
          >
            <span class="bet-type">След. убийство {{ event.home_team.substring(0, 3).toUpperCase() }}</span>
            <span class="odds-value">{{ formatOdds(event.odds.next_kill_home) }}</span>
          </button>
        </div>
      </div>

      <!-- League of Legends ставки -->
      <div class="odds-group" v-if="event.sport === 'lol'">
        <h4 class="odds-title">LoL ставки</h4>
        <div class="odds-buttons">
          <button
            v-if="event.odds.first_blood_home"
            @click="addBet('first_blood_home', event.odds.first_blood_home)"
            :class="['odds-btn', { selected: isBetSelected('first_blood_home') }]"
          >
            <span class="bet-type">First Blood {{ event.home_team.substring(0, 3).toUpperCase() }}</span>
            <span class="odds-value">{{ formatOdds(event.odds.first_blood_home) }}</span>
          </button>

          <button
            v-if="event.odds.baron_control_home"
            @click="addBet('baron_control_home', event.odds.baron_control_home)"
            :class="['odds-btn', { selected: isBetSelected('baron_control_home') }]"
          >
            <span class="bet-type">Барон {{ event.home_team.substring(0, 3).toUpperCase() }}</span>
            <span class="odds-value">{{ formatOdds(event.odds.baron_control_home) }}</span>
          </button>
        </div>
      </div>

      <!-- Valorant ставки -->
      <div class="odds-group" v-if="event.sport === 'valorant'">
        <h4 class="odds-title">Valorant ставки</h4>
        <div class="odds-buttons">
          <button
            v-if="event.odds.first_blood_home"
            @click="addBet('first_blood_home', event.odds.first_blood_home)"
            :class="['odds-btn', { selected: isBetSelected('first_blood_home') }]"
          >
            <span class="bet-type">First Blood {{ event.home_team.substring(0, 3).toUpperCase() }}</span>
            <span class="odds-value">{{ formatOdds(event.odds.first_blood_home) }}</span>
          </button>

          <button
            v-if="event.odds.total_rounds_over_26"
            @click="addBet('total_rounds_over_26', event.odds.total_rounds_over_26)"
            :class="['odds-btn', { selected: isBetSelected('total_rounds_over_26') }]"
          >
            <span class="bet-type">Раундов >26</span>
            <span class="odds-value">{{ formatOdds(event.odds.total_rounds_over_26) }}</span>
          </button>

          <button
            v-if="event.odds.next_round_home && isLive"
            @click="addBet('next_round_home', event.odds.next_round_home)"
            :class="['odds-btn', { selected: isBetSelected('next_round_home') }]"
          >
            <span class="bet-type">След. раунд {{ event.home_team.substring(0, 3).toUpperCase() }}</span>
            <span class="odds-value">{{ formatOdds(event.odds.next_round_home) }}</span>
          </button>
        </div>
      </div>

      <!-- PUBG ставки -->
      <div class="odds-group" v-if="event.sport === 'pubg'">
        <h4 class="odds-title">PUBG ставки</h4>
        <div class="odds-buttons">
          <button
            v-if="event.odds.chicken_dinner_home"
            @click="addBet('chicken_dinner_home', event.odds.chicken_dinner_home)"
            :class="['odds-btn', { selected: isBetSelected('chicken_dinner_home') }]"
          >
            <span class="bet-type">Победа {{ event.home_team.substring(0, 3).toUpperCase() }}</span>
            <span class="odds-value">{{ formatOdds(event.odds.chicken_dinner_home) }}</span>
          </button>

          <button
            v-if="event.odds.total_kills_over_25"
            @click="addBet('total_kills_over_25', event.odds.total_kills_over_25)"
            :class="['odds-btn', { selected: isBetSelected('total_kills_over_25') }]"
          >
            <span class="bet-type">Убийств >25</span>
            <span class="odds-value">{{ formatOdds(event.odds.total_kills_over_25) }}</span>
          </button>

          <button
            v-if="event.odds.next_kill_home && isLive"
            @click="addBet('next_kill_home', event.odds.next_kill_home)"
            :class="['odds-btn', { selected: isBetSelected('next_kill_home') }]"
          >
            <span class="bet-type">След. убийство {{ event.home_team.substring(0, 3).toUpperCase() }}</span>
            <span class="odds-value">{{ formatOdds(event.odds.next_kill_home) }}</span>
          </button>
        </div>
      </div>

      <!-- Apex Legends ставки -->
      <div class="odds-group" v-if="event.sport === 'apex'">
        <h4 class="odds-title">Apex ставки</h4>
        <div class="odds-buttons">
          <button
            v-if="event.odds.first_blood_home"
            @click="addBet('first_blood_home', event.odds.first_blood_home)"
            :class="['odds-btn', { selected: isBetSelected('first_blood_home') }]"
          >
            <span class="bet-type">First Blood {{ event.home_team.substring(0, 3).toUpperCase() }}</span>
            <span class="odds-value">{{ formatOdds(event.odds.first_blood_home) }}</span>
          </button>

          <button
            v-if="event.odds.total_kills_over_30"
            @click="addBet('total_kills_over_30', event.odds.total_kills_over_30)"
            :class="['odds-btn', { selected: isBetSelected('total_kills_over_30') }]"
          >
            <span class="bet-type">Убийств >30</span>
            <span class="odds-value">{{ formatOdds(event.odds.total_kills_over_30) }}</span>
          </button>

          <button
            v-if="event.odds.next_kill_home && isLive"
            @click="addBet('next_kill_home', event.odds.next_kill_home)"
            :class="['odds-btn', { selected: isBetSelected('next_kill_home') }]"
          >
            <span class="bet-type">След. убийство {{ event.home_team.substring(0, 3).toUpperCase() }}</span>
            <span class="odds-value">{{ formatOdds(event.odds.next_kill_home) }}</span>
          </button>
        </div>
      </div>

      <!-- Rainbow Six Siege ставки -->
      <div class="odds-group" v-if="event.sport === 'rainbow'">
        <h4 class="odds-title">R6S ставки</h4>
        <div class="odds-buttons">
          <button
            v-if="event.odds.first_blood_home"
            @click="addBet('first_blood_home', event.odds.first_blood_home)"
            :class="['odds-btn', { selected: isBetSelected('first_blood_home') }]"
          >
            <span class="bet-type">First Kill {{ event.home_team.substring(0, 3).toUpperCase() }}</span>
            <span class="odds-value">{{ formatOdds(event.odds.first_blood_home) }}</span>
          </button>

          <button
            v-if="event.odds.total_rounds_over_12"
            @click="addBet('total_rounds_over_12', event.odds.total_rounds_over_12)"
            :class="['odds-btn', { selected: isBetSelected('total_rounds_over_12') }]"
          >
            <span class="bet-type">Раундов >12</span>
            <span class="odds-value">{{ formatOdds(event.odds.total_rounds_over_12) }}</span>
          </button>
        </div>
      </div>

      <!-- Live ставки (для традиционного спорта) -->
      <div class="odds-group" v-if="isLive && !['csgo', 'dota2', 'lol'].includes(event.sport) && (event.odds.next_goal_home || event.odds.next_goal_away)">
        <h4 class="odds-title">Следующий гол</h4>
        <div class="odds-buttons">
          <button
            v-if="event.odds.next_goal_home"
            @click="addBet('next_goal_home', event.odds.next_goal_home)"
            :class="['odds-btn', { selected: isBetSelected('next_goal_home') }]"
          >
            <span class="bet-type">{{ event.home_team.substring(0, 3).toUpperCase() }}</span>
            <span class="odds-value">{{ formatOdds(event.odds.next_goal_home) }}</span>
          </button>

          <button
            v-if="event.odds.next_goal_away"
            @click="addBet('next_goal_away', event.odds.next_goal_away)"
            :class="['odds-btn', { selected: isBetSelected('next_goal_away') }]"
          >
            <span class="bet-type">{{ event.away_team.substring(0, 3).toUpperCase() }}</span>
            <span class="odds-value">{{ formatOdds(event.odds.next_goal_away) }}</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useBetsStore } from '../../stores/bets'
import eventDatabase from '../../services/eventDatabase'
import sportsApiService from '../../services/sportsApi'
import aiService from '../../services/aiService'

export default {
  name: 'SportsEventCard',
  props: {
    event: {
      type: Object,
      required: true
    },
    isLive: {
      type: Boolean,
      default: false
    }
  },
  setup() {
    const betsStore = useBetsStore()

    return {
      betsStore,
      eventDatabase,
      sportsApiService,
      aiService
    }
  },

  async mounted() {
    await this.loadRealEventData()
    if (this.event.is_live) {
      this.startLiveUpdates()
    }
  },

  beforeUnmount() {
    if (this.liveTimer) {
      clearInterval(this.liveTimer)
    }
  },
  methods: {
    // Загрузка реальных данных события
    async loadRealEventData() {
      try {
        this.isLoadingData = true

        // Временно отключаем внешние API вызовы из-за CORS проблем
        // Используем только локальные данные
        console.log('Using local event data (external APIs disabled due to CORS)')

        // Загрузка AI прогноза
        await this.loadAIPrediction()

      } catch (error) {
        console.error('Error loading real event data:', error)
      } finally {
        this.isLoadingData = false
      }
    },

    // Загрузка AI прогноза
    async loadAIPrediction() {
      try {
        this.isLoadingPrediction = true

        // Получение истории пользователя для анализа
        const userBets = await this.eventDatabase.getBets({ user_id: 'current_user' })

        // Запрос AI прогноза
        const prediction = await this.aiService.getPrediction(this.event, userBets)

        if (prediction) {
          this.aiPrediction = prediction
          // Сохранение прогноза в БД
          await this.eventDatabase.savePrediction(prediction)
        }

      } catch (error) {
        console.error('Error loading AI prediction:', error)
      } finally {
        this.isLoadingPrediction = false
      }
    },

    // Запуск live обновлений
    startLiveUpdates() {
      // Временно отключаем live обновления из-за CORS проблем
      // Используем только локальные данные
      console.log('Live updates disabled (external APIs disabled due to CORS)')

      // Имитация обновления счета для демонстрации
      if (this.event.is_live) {
        this.liveTimer = setInterval(() => {
          // Имитация обновления времени/счета для live событий
          if (this.event.sport === 'football' && this.event.minute) {
            this.event.minute = Math.min(90, this.event.minute + 1)
          }
        }, 60000) // Обновление каждую минуту
      }
    },

    addBet(betType, odds) {
      this.betsStore.addToBetSlip(this.event, betType, odds)
      this.$emit('bet-added', {
        event_id: this.event.id,
        bet_type: betType,
        odds: odds
      })
    },

    isBetSelected(betType) {
      return this.betsStore.betSlip.some(bet =>
        bet.event_id === this.event.id && bet.bet_type === betType
      )
    },

    formatOdds(odds) {
      return Number(odds).toFixed(2)
    },

    formatTime(dateString) {
      const date = new Date(dateString)
      const now = new Date()
      const diff = date - now

      if (diff < 0) return 'Скоро'

      const hours = Math.floor(diff / (1000 * 60 * 60))
      const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60))

      if (hours > 24) {
        return date.toLocaleDateString('ru-RU', {
          month: 'short',
          day: 'numeric',
          hour: '2-digit',
          minute: '2-digit'
        })
      } else if (hours > 0) {
        return `Через ${hours}ч ${minutes}м`
      } else {
        return `Через ${minutes}м`
      }
    }
  }
}
</script>

<style scoped>
.event-card {
  background: #ffffff;
  border: 1px solid #e1e5e9;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  position: relative;
}

.event-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
  border-color: #667eea;
}

.event-card.live {
  border-left: 4px solid #ff4444;
  background: #fff8f8;
}

.event-card.live:hover {
  border-left-color: #ff6b6b;
}

.event-header {
  background: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
  padding: 12px 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.sport-badge {
  background: #6c757d;
  color: white;
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 600;
}

.league-name {
  font-size: 0.9rem;
  opacity: 0.9;
  margin-top: 5px;
}

.event-time {
  text-align: right;
}

.live-badge {
  background: #dc3545;
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 4px;
}

.live-dot {
  width: 6px;
  height: 6px;
  background: white;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.start-time {
  font-size: 1rem;
  font-weight: 500;
}

.teams-section {
  padding: 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
}

.team {
  flex: 1;
  text-align: center;
}

.home-team {
  text-align: right;
}

.team-name {
  font-size: 1rem;
  font-weight: 600;
  color: #212529;
  margin-bottom: 4px;
  text-align: center;
  line-height: 1.3;
}

.team-score {
  font-size: 1.2rem;
  font-weight: 700;
  color: #495057;
  background: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  padding: 2px 6px;
  display: inline-block;
}

.vs-indicator {
  font-size: 1rem;
  font-weight: 600;
  color: #6c757d;
  margin: 0 12px;
  min-width: 30px;
}

.game-type {
  font-size: 0.7rem;
  font-weight: 600;
  color: #495057;
  background: #e9ecef;
  padding: 2px 6px;
  border-radius: 4px;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.game-info {
  font-size: 0.75rem;
  color: #6c757d;
  font-weight: 600;
  margin-top: 4px;
  padding: 3px 6px;
  background: rgba(108, 117, 125, 0.1);
  border-radius: 6px;
  text-align: center;
  border: 1px solid rgba(108, 117, 125, 0.2);
  backdrop-filter: blur(5px);
}

.odds-section {
  padding: 20px;
}

.odds-group {
  margin-bottom: 20px;
}

.odds-group:last-child {
  margin-bottom: 0;
}

.odds-title {
  font-size: 0.85rem;
  font-weight: 700;
  color: #495057;
  margin-bottom: 12px;
  text-transform: uppercase;
  letter-spacing: 1px;
  text-align: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  position: relative;
}

.odds-title::after {
  content: '';
  position: absolute;
  bottom: -4px;
  left: 50%;
  transform: translateX(-50%);
  width: 30px;
  height: 2px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 1px;
}

.odds-buttons {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(80px, 1fr));
  gap: 10px;
}

.odds-btn {
  background: #f8f9fa;
  border: 2px solid #dee2e6;
  border-radius: 8px;
  padding: 12px 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  min-height: 60px;
  position: relative;
}

.odds-btn:hover {
  border-color: #007bff;
  background: #e3f2fd;
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 123, 255, 0.15);
}

.odds-btn.selected {
  background: #007bff;
  border-color: #007bff;
  color: white;
  box-shadow: 0 2px 8px rgba(0, 123, 255, 0.3);
}

.odds-btn.selected:hover {
  background: #0056b3;
  border-color: #0056b3;
  box-shadow: 0 4px 12px rgba(0, 123, 255, 0.4);
}

.odds-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.bet-type {
  font-size: 0.8rem;
  font-weight: 600;
  color: #6c757d;
  text-transform: uppercase;
  text-align: center;
  line-height: 1.2;
}

.odds-value {
  font-size: 1.2rem;
  font-weight: 700;
  color: #212529;
}

.odds-btn.selected .bet-type,
.odds-btn.selected .odds-value {
  color: white;
}

@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.5; }
  100% { opacity: 1; }
}

/* Адаптивность */
@media (max-width: 480px) {
  .event-header {
    flex-direction: column;
    gap: 10px;
    text-align: center;
  }

  .teams-section {
    flex-direction: column;
    gap: 15px;
  }

  .home-team,
  .away-team {
    text-align: center;
  }

  .vs-indicator {
    margin: 0;
  }

  .odds-buttons {
    grid-template-columns: repeat(3, 1fr);
  }

  .odds-btn {
    min-height: 50px;
    padding: 8px 4px;
  }
}
</style>
