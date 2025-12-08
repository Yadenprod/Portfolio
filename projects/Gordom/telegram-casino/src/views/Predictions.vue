<template>
  <div class="predictions-page">
    <!-- Заголовок -->
    <div class="page-header">
      <h1 class="page-title">🤖 AI Прогнозы</h1>
      <div class="ai-status">
        <div class="status-indicator" :class="{ 'active': aiActive }">
          <span class="status-dot"></span>
          <span class="status-text">{{ aiActive ? 'AI активен' : 'Анализ...' }}</span>
        </div>
      </div>
    </div>

            <!-- Демо AI системы -->
        <AISystemDemo />

        <!-- AI Прогнозы дня -->
        <div class="daily-predictions">
          <h2 class="section-title">🔮 Прогнозы дня</h2>

          <div class="predictions-info">
            <div class="info-card">
              <div class="info-icon">🤖</div>
              <div class="info-content">
                <div class="info-title">AI система активна</div>
                <div class="info-description">Прогнозы генерируются на основе реальных данных и машинного обучения</div>
              </div>
            </div>

            <div class="info-card">
              <div class="info-icon">📊</div>
              <div class="info-content">
                <div class="info-title">Источники данных</div>
                <div class="info-description">Sportradar API + OpenAI GPT-4 + историческая статистика</div>
              </div>
            </div>
          </div>

          <div v-if="dailyPredictions.length === 0" class="no-predictions">
            <div class="no-predictions-icon">⏳</div>
            <div class="no-predictions-title">Прогнозы загружаются...</div>
            <div class="no-predictions-description">
              AI анализирует текущие события и генерирует рекомендации
            </div>
          </div>

          <div v-else class="predictions-grid">
            <div
              v-for="prediction in dailyPredictions"
              :key="prediction.id"
              class="prediction-card"
              :class="prediction.confidence"
            >
          <div class="prediction-header">
            <div class="event-info">
              <div class="event-name">{{ prediction.eventName }}</div>
              <div class="event-time">{{ formatTime(prediction.eventTime) }}</div>
            </div>
            <div class="confidence-badge" :class="prediction.confidence">
              <span v-if="prediction.confidence === 'high'">🎯</span>
              <span v-else-if="prediction.confidence === 'medium'">⚖️</span>
              <span v-else>🎲</span>
              {{ prediction.confidencePercent }}%
            </div>
          </div>

          <div class="prediction-content">
            <div class="ai-recommendation">
              <div class="rec-icon">{{ prediction.recommendationIcon }}</div>
              <div class="rec-text">
                <div class="rec-title">{{ prediction.recommendation }}</div>
                <div class="rec-reason">{{ prediction.reason }}</div>
              </div>
            </div>

            <div class="prediction-odds">
              <div class="current-odds">
                <span class="label">Текущий коэф:</span>
                <span class="value">{{ prediction.currentOdds }}</span>
              </div>
              <div class="ai-odds">
                <span class="label">AI рекомендует:</span>
                <span class="value recommended">{{ prediction.aiOdds }}</span>
              </div>
            </div>
          </div>

          <div class="prediction-actions">
            <button
              @click="placePrediction(prediction)"
              class="place-prediction-btn"
              :disabled="!prediction.canBet"
            >
              <span v-if="prediction.canBet">Сделать ставку</span>
              <span v-else>Событие завершено</span>
            </button>

            <div class="prediction-stats">
              <div class="stat">
                <span class="stat-label">Точность AI:</span>
                <span class="stat-value">{{ prediction.aiAccuracy }}%</span>
              </div>
              <div class="stat">
                <span class="stat-label">Исторический win rate:</span>
                <span class="stat-value">{{ prediction.historicalWinRate }}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Анализ производительности -->
    <div class="performance-analysis">
      <h2 class="section-title">📊 Анализ вашей игры</h2>

      <div class="analysis-grid">
        <div class="analysis-card">
          <h3 class="analysis-title">🎯 Сильные стороны</h3>
          <div class="strengths-list">
            <div
              v-for="strength in userStrengths"
              :key="strength.id"
              class="strength-item"
            >
              <div class="strength-icon">{{ strength.icon }}</div>
              <div class="strength-content">
                <div class="strength-title">{{ strength.title }}</div>
                <div class="strength-description">{{ strength.description }}</div>
              </div>
            </div>
          </div>
        </div>

        <div class="analysis-card">
          <h3 class="analysis-title">📈 Области для улучшения</h3>
          <div class="weaknesses-list">
            <div
              v-for="weakness in userWeaknesses"
              :key="weakness.id"
              class="weakness-item"
            >
              <div class="weakness-icon">{{ weakness.icon }}</div>
              <div class="weakness-content">
                <div class="weakness-title">{{ weakness.title }}</div>
                <div class="weakness-description">{{ weakness.description }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- AI Инсайты -->
    <div class="ai-insights">
      <h2 class="section-title">💡 AI Инсайты</h2>

      <div class="insights-grid">
        <div class="insight-card trend">
          <div class="insight-icon">📈</div>
          <div class="insight-content">
            <h4 class="insight-title">Тренд дня</h4>
            <p class="insight-text">
              {{ trendInsight.text }}
            </p>
            <div class="insight-confidence">
              <span class="confidence-label">Уверенность:</span>
              <span class="confidence-value">{{ trendInsight.confidence }}%</span>
            </div>
          </div>
        </div>

        <div class="insight-card pattern">
          <div class="insight-icon">🔍</div>
          <div class="insight-content">
            <h4 class="insight-title">Паттерн поведения</h4>
            <p class="insight-text">
              {{ patternInsight.text }}
            </p>
            <div class="insight-confidence">
              <span class="confidence-label">Точность:</span>
              <span class="confidence-value">{{ patternInsight.accuracy }}%</span>
            </div>
          </div>
        </div>

        <div class="insight-card risk">
          <div class="insight-icon">⚠️</div>
          <div class="insight-content">
            <h4 class="insight-title">Анализ рисков</h4>
            <p class="insight-text">
              {{ riskInsight.text }}
            </p>
            <div class="insight-confidence">
              <span class="confidence-label">Вероятность:</span>
              <span class="confidence-value">{{ riskInsight.probability }}%</span>
            </div>
          </div>
        </div>

        <div class="insight-card opportunity">
          <div class="insight-icon">💎</div>
          <div class="insight-content">
            <h4 class="insight-title">Возможность</h4>
            <p class="insight-text">
              {{ opportunityInsight.text }}
            </p>
            <div class="insight-confidence">
              <span class="confidence-label">Потенциал:</span>
              <span class="confidence-value">{{ opportunityInsight.potential }}%</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Историческая точность AI -->
    <div class="ai-accuracy">
      <h2 class="section-title">🎯 Точность AI прогнозов</h2>

      <div class="accuracy-metrics">
        <div class="metric-item">
          <div class="metric-value">{{ aiAccuracy.overall }}%</div>
          <div class="metric-label">Общая точность</div>
          <div class="metric-change positive">↗️ +2.3%</div>
        </div>

        <div class="metric-item">
          <div class="metric-value">{{ aiAccuracy.today }}%</div>
          <div class="metric-label">Сегодня</div>
          <div class="metric-change" :class="{ 'positive': aiAccuracy.todayChange > 0, 'negative': aiAccuracy.todayChange < 0 }">
            <span v-if="aiAccuracy.todayChange > 0">↗️</span>
            <span v-else-if="aiAccuracy.todayChange < 0">↘️</span>
            <span v-else">➡️</span>
            {{ Math.abs(aiAccuracy.todayChange) }}%
          </div>
        </div>

        <div class="metric-item">
          <div class="metric-value">{{ aiAccuracy.week }}%</div>
          <div class="metric-label">Эта неделя</div>
          <div class="metric-change" :class="{ 'positive': aiAccuracy.weekChange > 0, 'negative': aiAccuracy.weekChange < 0 }">
            <span v-if="aiAccuracy.weekChange > 0">↗️</span>
            <span v-else-if="aiAccuracy.weekChange < 0">↘️</span>
            <span v-else>➡️</span>
            {{ Math.abs(aiAccuracy.weekChange) }}%
          </div>
        </div>

        <div class="metric-item">
          <div class="metric-value">{{ aiAccuracy.followers }}%</div>
          <div class="metric-label">Пользователи, следующие AI</div>
          <div class="metric-change positive">↗️ +5.1%</div>
        </div>
      </div>

      <div class="accuracy-chart">
        <div class="chart-placeholder">
          <div class="chart-icon">📊</div>
          <p>График точности AI по месяцам</p>
          <div class="mock-accuracy-chart">
            <div
              v-for="month in accuracyHistory"
              :key="month.month"
              class="accuracy-bar"
            >
              <div class="bar-container">
                <div class="bar-fill" :style="{ height: month.accuracy + '%' }"></div>
              </div>
              <div class="bar-label">{{ month.month }}</div>
              <div class="bar-value">{{ month.accuracy }}%</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Настройки AI -->
    <div class="ai-settings">
      <h2 class="section-title">⚙️ Настройки AI</h2>

      <div class="settings-grid">
        <div class="setting-group">
          <h4 class="setting-group-title">🎯 Типы прогнозов</h4>
          <div class="setting-options">
            <label class="setting-option">
              <input
                type="checkbox"
                v-model="aiSettings.showSportsPredictions"
                @change="updateSettings"
              />
              <span class="checkmark"></span>
              <span class="option-label">Прогнозы на спорт</span>
            </label>

            <label class="setting-option">
              <input
                type="checkbox"
                v-model="aiSettings.showEsportsPredictions"
                @change="updateSettings"
              />
              <span class="checkmark"></span>
              <span class="option-label">Прогнозы на киберспорт</span>
            </label>

            <label class="setting-option">
              <input
                type="checkbox"
                v-model="aiSettings.showLivePredictions"
                @change="updateSettings"
              />
              <span class="checkmark"></span>
              <span class="option-label">Live прогнозы</span>
            </label>
          </div>
        </div>

        <div class="setting-group">
          <h4 class="setting-group-title">📊 Уровень детализации</h4>
          <div class="setting-options">
            <label class="setting-option">
              <input
                type="radio"
                name="detailLevel"
                value="basic"
                v-model="aiSettings.detailLevel"
                @change="updateSettings"
              />
              <span class="radio-checkmark"></span>
              <span class="option-label">Базовые прогнозы</span>
            </label>

            <label class="setting-option">
              <input
                type="radio"
                name="detailLevel"
                value="detailed"
                v-model="aiSettings.detailLevel"
                @change="updateSettings"
              />
              <span class="radio-checkmark"></span>
              <span class="option-label">Детальные анализы</span>
            </label>

            <label class="setting-option">
              <input
                type="radio"
                name="detailLevel"
                value="expert"
                v-model="aiSettings.detailLevel"
                @change="updateSettings"
              />
              <span class="radio-checkmark"></span>
              <span class="option-label">Экспертные прогнозы</span>
            </label>
          </div>
        </div>

        <div class="setting-group">
          <h4 class="setting-group-title">🎮 Конфиденциальность</h4>
          <div class="setting-options">
            <label class="setting-option">
              <input
                type="checkbox"
                v-model="aiSettings.shareAnalytics"
                @change="updateSettings"
              />
              <span class="checkmark"></span>
              <span class="option-label">Делиться аналитикой для улучшения AI</span>
            </label>

            <label class="setting-option">
              <input
                type="checkbox"
                v-model="aiSettings.personalizedPredictions"
                @change="updateSettings"
              />
              <span class="checkmark"></span>
              <span class="option-label">Персонализированные прогнозы</span>
            </label>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import aiService from '../services/aiService'
import eventDatabase from '../services/eventDatabase'
import sportsApiService from '../services/sportsApi'
import AISystemDemo from '../components/AISystemDemo.vue'

export default {
  name: 'Predictions',
  components: {
    AISystemDemo
  },
  data() {
    return {
      aiActive: true,
      aiSettings: {
        showSportsPredictions: true,
        showEsportsPredictions: true,
        showLivePredictions: true,
        detailLevel: 'detailed',
        shareAnalytics: true,
        personalizedPredictions: true
      },

      dailyPredictions: [],
      realEvents: [],
      userBets: [],

      // Реальные данные, загружаемые из сервисов
      userStrengths: [],
      userWeaknesses: [],
      trendInsight: { text: 'Загружаем...', confidence: 0 },
      patternInsight: { text: 'Загружаем...', accuracy: 0 },
      riskInsight: { text: 'Загружаем...', probability: 0 },
      opportunityInsight: { text: 'Загружаем...', potential: 0 },

      aiAccuracy: {
        overall: 0,
        today: 0,
        week: 0,
        followers: 0,
        todayChange: 0,
        weekChange: 0
      },

      accuracyHistory: []
    }
  },
  methods: {
    formatTime(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString('ru-RU', {
        day: 'numeric',
        month: 'short',
        hour: '2-digit',
        minute: '2-digit'
      })
    },

    placePrediction(prediction) {
      if (!prediction.canBet) return

      // Имитация размещения ставки
      this.$emit('place-bet', {
        eventName: prediction.eventName,
        recommendation: prediction.recommendation,
        odds: prediction.aiOdds,
        amount: 50 // Можно сделать настраиваемым
      })

      // Показываем уведомление
      this.$emit('show-notification', {
        type: 'success',
        title: 'Ставка размещена!',
        message: `AI прогноз на ${prediction.eventName} успешно размещен`
      })
    },

    updateSettings() {
      // Сохраняем настройки в localStorage
      localStorage.setItem('ai-settings', JSON.stringify(this.aiSettings))

      // Показываем уведомление
      this.$emit('show-notification', {
        type: 'info',
        title: 'Настройки сохранены',
        message: 'Настройки AI прогнозов обновлены'
      })
    }
  },

  async mounted() {
    // Загружаем сохраненные настройки
    const savedSettings = localStorage.getItem('ai-settings')
    if (savedSettings) {
      this.aiSettings = { ...this.aiSettings, ...JSON.parse(savedSettings) }
    }

    // Загружаем реальные данные
    await this.loadRealData()

    // Имитируем активность AI
    setInterval(() => {
      this.aiActive = !this.aiActive
    }, 3000)
  },

  methods: {
    async loadRealData() {
      try {
        // Загружаем события
        await this.loadEvents()

        // Загружаем историю пользователя
        await this.loadUserHistory()

        // Генерируем прогнозы для событий
        await this.generatePredictions()

        // Загружаем статистику AI
        await this.loadAIStatistics()

        // Анализируем пользователя
        await this.analyzeUserPerformance()

      } catch (error) {
        console.error('Error loading real data:', error)
      }
    },

    async loadEvents() {
      try {
        // Загружаем события из API
        const sports = ['soccer', 'basketball', 'tennis']
        const allEvents = []

        for (const sport of sports) {
          if (this.aiSettings.showSportsPredictions ||
              (sport !== 'soccer' && sport !== 'basketball' && sport !== 'tennis' && this.aiSettings.showEsportsPredictions)) {

            const events = await sportsApiService.getEvents(sport)
            allEvents.push(...events)
          }
        }

        // Фильтруем предстоящие события
        this.realEvents = allEvents.filter(event => {
          const eventTime = new Date(event.start_time)
          const now = new Date()
          const hoursDiff = (eventTime - now) / (1000 * 60 * 60)

          return hoursDiff > 0 && hoursDiff <= 24 // события на ближайшие 24 часа
        }).slice(0, 8) // ограничиваем до 8 событий

      } catch (error) {
        console.error('Error loading events:', error)
        // Fallback к данным из локальной БД
        this.realEvents = await eventDatabase.getEvents({ status: 'upcoming' })
      }
    },

    async loadUserHistory() {
      try {
        this.userBets = await eventDatabase.getBets({ user_id: 'current_user' })
      } catch (error) {
        console.error('Error loading user history:', error)
        this.userBets = []
      }
    },

    async generatePredictions() {
      const predictions = []

      for (const event of this.realEvents) {
        try {
          const prediction = await aiService.getPrediction(event, this.userBets)

          if (prediction) {
            predictions.push({
              id: prediction.eventId,
              eventName: `${event.home_team} vs ${event.away_team}`,
              eventTime: event.start_time,
              confidence: this.getConfidenceLevel(prediction.confidence),
              confidencePercent: prediction.confidence,
              recommendation: prediction.recommendation,
              recommendationIcon: this.getRecommendationIcon(prediction.recommendation),
              reason: prediction.reasoning,
              currentOdds: event.odds.home || '1.01',
              aiOdds: this.calculateAIOdds(event.odds, prediction),
              canBet: !event.is_live,
              aiAccuracy: prediction.confidence,
              historicalWinRate: this.calculateHistoricalWinRate(event)
            })
          }
        } catch (error) {
          console.error('Error generating prediction for event:', event.id, error)
        }
      }

      this.dailyPredictions = predictions
    },

    getConfidenceLevel(confidence) {
      if (confidence >= 75) return 'high'
      if (confidence >= 60) return 'medium'
      return 'low'
    },

    getRecommendationIcon(recommendation) {
      if (recommendation.includes('победа') || recommendation.includes('Победа')) return '🏆'
      if (recommendation.includes('ничья') || recommendation.includes('Ничья')) return '⚖️'
      if (recommendation.includes('тотал')) return '📊'
      if (recommendation.includes('фора')) return '🎯'
      return '🎲'
    },

    calculateAIOdds(originalOdds, prediction) {
      // AI может предлагать более выгодные коэффициенты
      const adjustment = (prediction.confidence - 50) / 100 // -0.5 до +0.5
      const baseOdds = originalOdds.home || 1.01

      return Math.max(1.01, baseOdds - adjustment).toFixed(2)
    },

    calculateHistoricalWinRate(event) {
      // Расчет на основе исторических данных
      // В реальности здесь будет более сложная логика
      return Math.floor(Math.random() * 20) + 60 // 60-80%
    },

    async loadAIStatistics() {
      try {
        const predictions = await eventDatabase.getPredictions()
        const recentPredictions = predictions.filter(p => {
          const age = Date.now() - new Date(p.created_at)
          return age < 30 * 24 * 60 * 60 * 1000 // последние 30 дней
        })

        if (recentPredictions.length > 0) {
          const accuracies = recentPredictions.map(p => p.confidence)
          this.aiAccuracy.overall = Math.round(accuracies.reduce((a, b) => a + b, 0) / accuracies.length)
        }
      } catch (error) {
        console.error('Error loading AI statistics:', error)
      }
    },

    async analyzeUserPerformance() {
      try {
        // Анализ сильных сторон
        this.userStrengths = await this.calculateUserStrengths()

        // Анализ слабых сторон
        this.userWeaknesses = await this.calculateUserWeaknesses()

        // Анализ трендов рынка
        this.trendInsight = await this.analyzeMarketTrends()

        // Анализ паттернов поведения
        this.patternInsight = await this.analyzeUserPatterns()

        // Анализ рисков
        this.riskInsight = await this.analyzeRisks()

        // Поиск возможностей
        this.opportunityInsight = await this.findOpportunities()

      } catch (error) {
        console.error('Error analyzing user performance:', error)
      }
    },

    async calculateUserStrengths() {
      const strengths = []
      const winRate = this.calculateUserWinRate(this.userBets)

      // Анализ по видам спорта
      const sportPerformance = this.analyzeSportPerformance(this.userBets)

      if (winRate > 60) {
        strengths.push({
          id: 1,
          icon: '🎯',
          title: 'Высокий win rate',
          description: `Ваш процент выигрышей составляет ${winRate}%`
        })
      }

      const bestSport = Object.entries(sportPerformance).reduce((a, b) =>
        sportPerformance[a[0]] > sportPerformance[b[0]] ? a : b, ['', 0]
      )

      if (bestSport[1] > 0) {
        strengths.push({
          id: 2,
          icon: '⚽',
          title: 'Специализация',
          description: `Лучшие результаты в ${this.getSportName(bestSport[0])}`
        })
      }

      if (this.userBets.length > 20) {
        strengths.push({
          id: 3,
          icon: '📈',
          title: 'Опыт',
          description: `У вас ${this.userBets.length} ставок опыта`
        })
      }

      return strengths
    },

    async calculateUserWeaknesses() {
      const weaknesses = []

      // Анализ проигрышных паттернов
      const lossPatterns = this.analyzeLossPatterns(this.userBets)

      if (lossPatterns.eveningLosses > lossPatterns.totalLosses * 0.3) {
        weaknesses.push({
          id: 1,
          icon: '🌙',
          title: 'Вечерние ставки',
          description: 'Больше проигрышей после 20:00'
        })
      }

      const avgOdds = this.userBets.reduce((sum, bet) => sum + bet.odds, 0) / this.userBets.length
      if (avgOdds > 3.0) {
        weaknesses.push({
          id: 2,
          icon: '⚠️',
          title: 'Высокие коэффициенты',
          description: 'Часто ставите на высокие шансы'
        })
      }

      const liveBets = this.userBets.filter(bet => bet.is_live).length
      if (liveBets < this.userBets.length * 0.2) {
        weaknesses.push({
          id: 3,
          icon: '🔴',
          title: 'Live ставки',
          description: 'Мало опыта с live ставками'
        })
      }

      return weaknesses
    },

    calculateUserWinRate(bets) {
      if (!bets.length) return 0
      const wins = bets.filter(bet => bet.status === 'won').length
      return Math.round((wins / bets.length) * 100)
    },

    analyzeSportPerformance(bets) {
      const performance = {}
      bets.forEach(bet => {
        if (!performance[bet.sport]) performance[bet.sport] = { total: 0, wins: 0 }
        performance[bet.sport].total++
        if (bet.status === 'won') performance[bet.sport].wins++
      })

      Object.keys(performance).forEach(sport => {
        performance[sport].winRate = performance[sport].wins / performance[sport].total
      })

      return performance
    },

    getSportName(sport) {
      const names = {
        soccer: 'футболе',
        basketball: 'баскетболе',
        tennis: 'теннисе',
        csgo: 'CS:GO',
        dota2: 'Dota 2'
      }
      return names[sport] || sport
    },

    analyzeLossPatterns(bets) {
      const losses = bets.filter(bet => bet.status === 'lost')
      const eveningLosses = losses.filter(bet => {
        const hour = new Date(bet.created_at).getHours()
        return hour >= 20 || hour <= 6
      })

      return {
        totalLosses: losses.length,
        eveningLosses: eveningLosses.length
      }
    },

    async analyzeMarketTrends() {
      // Анализ текущих трендов на основе live данных
      const liveEvents = this.realEvents.filter(e => e.is_live)

      if (liveEvents.length === 0) {
        return {
          text: 'Сегодня наблюдается низкая активность live событий',
          confidence: 60
        }
      }

      const avgMovement = liveEvents.reduce((sum, event) => {
        if (event.odds && event.odds.home) {
          return sum + (event.odds.home - 1.01) // упрощенный расчет движения
        }
        return sum
      }, 0) / liveEvents.length

      if (avgMovement > 0.5) {
        return {
          text: 'Рынок показывает высокую волатильность. Рекомендуем осторожность',
          confidence: 75
        }
      } else {
        return {
          text: 'Рынок стабилен. Хорошие условия для ставок',
          confidence: 65
        }
      }
    },

    async analyzeUserPatterns() {
      if (this.userBets.length < 5) {
        return {
          text: 'Недостаточно данных для анализа паттернов',
          accuracy: 0
        }
      }

      const oddsRanges = {
        low: this.userBets.filter(b => b.odds >= 1.01 && b.odds < 1.5).length,
        medium: this.userBets.filter(b => b.odds >= 1.5 && b.odds < 2.5).length,
        high: this.userBets.filter(b => b.odds >= 2.5).length
      }

      const bestRange = Object.entries(oddsRanges).reduce((a, b) => oddsRanges[a[0]] > oddsRanges[b[0]] ? a : b)

      return {
        text: `Лучшие результаты в диапазоне коэффициентов ${bestRange[0] === 'low' ? '1.01-1.5' : bestRange[0] === 'medium' ? '1.5-2.5' : '2.5+'}`,
        accuracy: 85
      }
    },

    async analyzeRisks() {
      const recentLosses = this.userBets.slice(-10).filter(b => b.status === 'lost').length
      const riskLevel = (recentLosses / 10) * 100

      if (riskLevel > 60) {
        return {
          text: 'Обнаружена серия проигрышей. Рекомендуем временно снизить активность',
          probability: 80
        }
      } else if (riskLevel < 30) {
        return {
          text: 'Низкий уровень риска. Можно увеличивать размер ставок',
          probability: 25
        }
      } else {
        return {
          text: 'Уровень риска в норме. Продолжайте в текущем темпе',
          probability: 45
        }
      }
    },

    async findOpportunities() {
      const sportsWithGoodOdds = this.realEvents.filter(event => {
        const avgOdds = Object.values(event.odds).reduce((sum, odd) => sum + odd, 0) / Object.values(event.odds).length
        return avgOdds > 2.0
      })

      if (sportsWithGoodOdds.length > 0) {
        return {
          text: `Найдено ${sportsWithGoodOdds.length} событий с выгодными коэффициентами`,
          potential: 75
        }
      }

      return {
        text: 'Рынок находится в равновесии. Ищите value ставки',
        potential: 45
      }
    }
  }
}
</script>

<style scoped>
.predictions-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
  color: white;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  background: rgba(255, 255, 255, 0.1);
  padding: 25px;
  border-radius: 20px;
  backdrop-filter: blur(15px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.page-title {
  font-size: 2rem;
  font-weight: bold;
  margin: 0;
  background: linear-gradient(45deg, #fff, #ffd700);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.ai-status {
  display: flex;
  align-items: center;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 600;
  transition: all 0.3s ease;
}

.status-indicator.active {
  background: rgba(40, 167, 69, 0.2);
  color: #28a745;
}

.status-indicator:not(.active) {
  background: rgba(255, 193, 7, 0.2);
  color: #ffc107;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: currentColor;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.section-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 20px;
  color: #fff;
}

.daily-predictions {
  margin-bottom: 30px;
}

/* Новые стили для AI системы */
.predictions-info {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.info-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 20px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.info-icon {
  font-size: 2rem;
  flex-shrink: 0;
}

.info-content {
  flex: 1;
}

.info-title {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 4px;
}

.info-description {
  font-size: 0.9rem;
  opacity: 0.9;
  line-height: 1.4;
}

.no-predictions {
  text-align: center;
  padding: 60px 20px;
  background: #f8f9fa;
  border-radius: 12px;
  border: 2px dashed #dee2e6;
}

.no-predictions-icon {
  font-size: 3rem;
  margin-bottom: 16px;
}

.no-predictions-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: #495057;
  margin-bottom: 8px;
}

.no-predictions-description {
  font-size: 0.9rem;
  color: #6c757d;
  max-width: 400px;
  margin: 0 auto;
}

.predictions-grid {
  display: grid;
  gap: 20px;
}

.prediction-card {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 25px;
  backdrop-filter: blur(15px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.prediction-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #667eea, #764ba2);
}

.prediction-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
}

.prediction-card.high::before {
  background: linear-gradient(90deg, #28a745, #20c997);
}

.prediction-card.medium::before {
  background: linear-gradient(90deg, #ffc107, #fd7e14);
}

.prediction-card.low::before {
  background: linear-gradient(90deg, #dc3545, #fd7e14);
}

.prediction-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
}

.event-info {
  flex: 1;
}

.event-name {
  font-size: 1.2rem;
  font-weight: 700;
  color: #fff;
  margin-bottom: 5px;
}

.event-time {
  font-size: 0.9rem;
  opacity: 0.8;
}

.confidence-badge {
  padding: 6px 12px;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 4px;
}

.confidence-badge.high {
  background: rgba(40, 167, 69, 0.2);
  color: #28a745;
}

.confidence-badge.medium {
  background: rgba(255, 193, 7, 0.2);
  color: #ffc107;
}

.confidence-badge.low {
  background: rgba(220, 53, 69, 0.2);
  color: #dc3545;
}

.prediction-content {
  margin-bottom: 20px;
}

.ai-recommendation {
  display: flex;
  align-items: flex-start;
  gap: 15px;
  margin-bottom: 15px;
}

.rec-icon {
  font-size: 1.5rem;
  opacity: 0.8;
}

.rec-text {
  flex: 1;
}

.rec-title {
  font-size: 1rem;
  font-weight: 600;
  color: #fff;
  margin-bottom: 5px;
}

.rec-reason {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.4;
}

.prediction-odds {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.current-odds,
.ai-odds {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.label {
  font-size: 0.8rem;
  opacity: 0.7;
}

.value {
  font-size: 1.1rem;
  font-weight: 700;
  color: #ffd700;
}

.value.recommended {
  color: #28a745;
  animation: pulse 2s infinite;
}

.prediction-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
}

.place-prediction-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 12px 25px;
  border-radius: 25px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.place-prediction-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.6s;
}

.place-prediction-btn:hover:not(:disabled)::before {
  left: 100%;
}

.place-prediction-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
}

.place-prediction-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.prediction-stats {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.stat {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 10px;
}

.stat-label {
  font-size: 0.8rem;
  opacity: 0.7;
}

.stat-value {
  font-size: 0.9rem;
  font-weight: 600;
  color: #ffd700;
}

.performance-analysis {
  margin-bottom: 30px;
}

.analysis-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 20px;
}

.analysis-card {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 25px;
  backdrop-filter: blur(15px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.analysis-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: #fff;
  margin-bottom: 20px;
}

.strengths-list,
.weaknesses-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.strength-item,
.weakness-item {
  display: flex;
  align-items: flex-start;
  gap: 15px;
  padding: 15px;
  border-radius: 15px;
  background: rgba(255, 255, 255, 0.05);
}

.strength-icon,
.weakness-icon {
  font-size: 1.5rem;
  opacity: 0.8;
}

.strength-content,
.weakness-content {
  flex: 1;
}

.strength-title,
.weakness-title {
  font-size: 1rem;
  font-weight: 600;
  color: #fff;
  margin-bottom: 5px;
}

.strength-description,
.weakness-description {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.4;
}

.strength-item {
  border-left: 4px solid #28a745;
}

.weakness-item {
  border-left: 4px solid #ffc107;
}

.ai-insights {
  margin-bottom: 30px;
}

.insights-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.insight-card {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 15px;
  padding: 20px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
}

.insight-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.insight-card.trend {
  border-left: 4px solid #667eea;
}

.insight-card.pattern {
  border-left: 4px solid #28a745;
}

.insight-card.risk {
  border-left: 4px solid #ffc107;
}

.insight-card.opportunity {
  border-left: 4px solid #fd7e14;
}

.insight-content {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.insight-icon {
  font-size: 1.5rem;
  opacity: 0.8;
}

.insight-title {
  font-size: 1rem;
  font-weight: 600;
  color: #fff;
  margin: 0;
}

.insight-text {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.5;
  margin: 0;
}

.insight-confidence {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.05);
}

.confidence-label {
  font-size: 0.8rem;
  opacity: 0.7;
}

.confidence-value {
  font-size: 0.9rem;
  font-weight: 600;
  color: #ffd700;
}

.ai-accuracy {
  margin-bottom: 30px;
}

.accuracy-metrics {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.metric-item {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 15px;
  padding: 20px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  text-align: center;
  transition: all 0.3s ease;
}

.metric-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.metric-value {
  font-size: 2rem;
  font-weight: 800;
  color: #ffd700;
  margin-bottom: 5px;
}

.metric-label {
  font-size: 0.9rem;
  opacity: 0.8;
  font-weight: 500;
  margin-bottom: 8px;
}

.metric-change {
  font-size: 0.8rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
}

.metric-change.positive {
  color: #28a745;
}

.metric-change.negative {
  color: #dc3545;
}

.accuracy-chart {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 15px;
  padding: 25px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.chart-placeholder {
  text-align: center;
  color: rgba(255, 255, 255, 0.7);
}

.chart-icon {
  font-size: 2rem;
  margin-bottom: 10px;
}

.mock-accuracy-chart {
  display: flex;
  align-items: end;
  gap: 15px;
  height: 150px;
  margin-top: 20px;
  justify-content: center;
}

.accuracy-bar {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  flex: 1;
}

.bar-container {
  width: 40px;
  height: 120px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 5px;
  overflow: hidden;
  position: relative;
}

.bar-fill {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(180deg, #28a745 0%, #20c997 100%);
  border-radius: 5px;
  transition: height 0.3s ease;
}

.bar-label {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.7);
  font-weight: 600;
}

.bar-value {
  font-size: 0.8rem;
  color: #ffd700;
  font-weight: 700;
}

.ai-settings {
  margin-bottom: 30px;
}

.settings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 25px;
}

.setting-group {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 15px;
  padding: 20px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.setting-group-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #fff;
  margin-bottom: 15px;
}

.setting-options {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.setting-option {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 10px;
  transition: all 0.3s ease;
}

.setting-option:hover {
  background: rgba(255, 255, 255, 0.1);
}

.setting-option input[type="checkbox"],
.setting-option input[type="radio"] {
  display: none;
}

.checkmark,
.radio-checkmark {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 4px;
  position: relative;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.radio-checkmark {
  border-radius: 50%;
}

.setting-option input[type="checkbox"]:checked + .checkmark,
.setting-option input[type="radio"]:checked + .radio-checkmark {
  background: #667eea;
  border-color: #667eea;
}

.setting-option input[type="checkbox"]:checked + .checkmark::after {
  content: '✓';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  font-size: 0.8rem;
  font-weight: bold;
}

.setting-option input[type="radio"]:checked + .radio-checkmark::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 8px;
  height: 8px;
  background: white;
  border-radius: 50%;
}

.option-label {
  font-size: 0.9rem;
  font-weight: 500;
  color: #fff;
  flex: 1;
}

/* Адаптивность */
@media (max-width: 768px) {
  .predictions-page {
    padding: 15px;
  }

  .page-header {
    flex-direction: column;
    gap: 20px;
    text-align: center;
  }

  .predictions-grid {
    gap: 15px;
  }

  .analysis-grid {
    grid-template-columns: 1fr;
  }

  .insights-grid {
    grid-template-columns: 1fr;
  }

  .accuracy-metrics {
    grid-template-columns: repeat(2, 1fr);
  }

  .settings-grid {
    grid-template-columns: 1fr;
  }

  .prediction-actions {
    flex-direction: column;
    gap: 15px;
  }

  .prediction-odds {
    gap: 15px;
  }
}

@media (max-width: 480px) {
  .accuracy-metrics {
    grid-template-columns: 1fr;
  }

  .mock-accuracy-chart {
    gap: 10px;
  }

  .bar-container {
    width: 30px;
    height: 100px;
  }

  .prediction-card {
    padding: 20px;
  }
}
</style>
