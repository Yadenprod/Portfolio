<template>
  <div class="ai-prediction-card">
    <!-- Шапка с уровнем уверенности -->
    <div class="prediction-header">
      <div class="confidence-indicator" :class="getConfidenceLevel()">
        <div class="confidence-icon">{{ getConfidenceIcon() }}</div>
        <div class="confidence-info">
          <div class="confidence-level">{{ getConfidenceText() }}</div>
          <div class="confidence-percent">{{ prediction.confidence }}%</div>
        </div>
      </div>

      <div class="prediction-time">
        <div class="time-label">Анализ выполнен</div>
        <div class="time-value">{{ formatTime(prediction.timestamp) }}</div>
      </div>
    </div>

    <!-- Основная информация о прогнозе -->
    <div class="prediction-content">
      <div class="event-info">
        <div class="event-teams">
          <span class="home-team">{{ prediction.home_team }}</span>
          <span class="vs-indicator">vs</span>
          <span class="away-team">{{ prediction.away_team }}</span>
        </div>
        <div class="event-league">{{ prediction.league }}</div>
        <div class="event-time">{{ formatEventTime(prediction.event_time) }}</div>
      </div>

      <div class="prediction-recommendation">
        <div class="rec-icon">{{ getRecommendationIcon(prediction.recommendation) }}</div>
        <div class="rec-content">
          <div class="rec-title">AI рекомендует</div>
          <div class="rec-value">{{ prediction.recommendation }}</div>
        </div>
      </div>
    </div>

    <!-- Обоснование прогноза -->
    <div class="prediction-reasoning">
      <div class="reasoning-header">
        <div class="reasoning-icon">🧠</div>
        <div class="reasoning-title">Обоснование прогноза</div>
      </div>
      <div class="reasoning-text">{{ prediction.reasoning }}</div>
    </div>

    <!-- Факторы влияния -->
    <div class="prediction-factors" v-if="prediction.factors && prediction.factors.length">
      <div class="factors-header">
        <div class="factors-icon">📊</div>
        <div class="factors-title">Ключевые факторы</div>
      </div>
      <div class="factors-list">
        <div
          v-for="factor in prediction.factors"
          :key="factor"
          class="factor-item"
        >
          <span class="factor-bullet">•</span>
          <span class="factor-text">{{ factor }}</span>
        </div>
      </div>
    </div>

    <!-- Статистика точности -->
    <div class="prediction-accuracy">
      <div class="accuracy-metrics">
        <div class="accuracy-item">
          <div class="accuracy-label">Точность AI</div>
          <div class="accuracy-value">{{ prediction.confidence }}%</div>
        </div>
        <div class="accuracy-item">
          <div class="accuracy-label">Модель</div>
          <div class="accuracy-value">{{ prediction.model || 'GPT-4' }}</div>
        </div>
        <div class="accuracy-item">
          <div class="accuracy-label">Версия</div>
          <div class="accuracy-value">{{ prediction.version || '1.0' }}</div>
        </div>
      </div>
    </div>

    <!-- Действия -->
    <div class="prediction-actions">
      <button
        @click="placePrediction"
        :disabled="!canBet"
        class="place-bet-btn"
      >
        <span v-if="canBet">🎯 Сделать ставку</span>
        <span v-else="eventExpired">⏰ Событие завершено</span>
      </button>

      <button @click="sharePrediction" class="share-btn">
        <span>📤 Поделиться</span>
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AIPredictionCard',
  props: {
    prediction: {
      type: Object,
      required: true
    }
  },
  computed: {
    canBet() {
      const eventTime = new Date(this.prediction.event_time);
      const now = new Date();
      return eventTime > now;
    },

    eventExpired() {
      const eventTime = new Date(this.prediction.event_time);
      const now = new Date();
      return eventTime <= now;
    }
  },
  methods: {
    getConfidenceLevel() {
      const confidence = this.prediction.confidence;
      if (confidence >= 80) return 'excellent';
      if (confidence >= 70) return 'very-high';
      if (confidence >= 60) return 'high';
      if (confidence >= 50) return 'medium';
      if (confidence >= 40) return 'low';
      return 'very-low';
    },

    getConfidenceText() {
      const level = this.getConfidenceLevel();
      const texts = {
        excellent: 'Отличная уверенность',
        'very-high': 'Очень высокая',
        high: 'Высокая',
        medium: 'Средняя',
        low: 'Низкая',
        'very-low': 'Очень низкая'
      };
      return texts[level] || 'Неизвестно';
    },

    getConfidenceIcon() {
      const level = this.getConfidenceLevel();
      const icons = {
        excellent: '🎯',
        'very-high': '⭐',
        high: '✅',
        medium: '⚠️',
        low: '❌',
        'very-low': '🚫'
      };
      return icons[level] || '❓';
    },

    getRecommendationIcon(recommendation) {
      if (recommendation.includes('победа') || recommendation.includes('Победа')) {
        return '🏆';
      }
      if (recommendation.includes('ничья') || recommendation.includes('Ничья')) {
        return '🤝';
      }
      if (recommendation.includes('тотал')) {
        return '📊';
      }
      if (recommendation.includes('фора')) {
        return '🎯';
      }
      return '🎲';
    },

    formatTime(timestamp) {
      const date = new Date(timestamp);
      return date.toLocaleString('ru-RU', {
        day: 'numeric',
        month: 'short',
        hour: '2-digit',
        minute: '2-digit'
      });
    },

    formatEventTime(eventTime) {
      const date = new Date(eventTime);
      return date.toLocaleString('ru-RU', {
        day: 'numeric',
        month: 'long',
        hour: '2-digit',
        minute: '2-digit'
      });
    },

    placePrediction() {
      if (!this.canBet) return;

      this.$emit('place-bet', {
        prediction: this.prediction,
        amount: 100 // Можно сделать настраиваемым
      });

      this.$emit('show-notification', {
        type: 'success',
        title: 'AI ставка размещена!',
        message: `Прогноз на ${this.prediction.home_team} vs ${this.prediction.away_team} успешно размещен`
      });
    },

    sharePrediction() {
      const shareText = `🤖 AI прогноз: ${this.prediction.recommendation} для ${this.prediction.home_team} vs ${this.prediction.away_team}. Уверенность: ${this.prediction.confidence}%`;

      if (navigator.share) {
        navigator.share({
          title: 'AI прогноз',
          text: shareText
        });
      } else {
        navigator.clipboard.writeText(shareText);
        this.$emit('show-notification', {
          type: 'info',
          title: 'Скопировано!',
          message: 'Прогноз скопирован в буфер обмена'
        });
      }
    }
  }
}
</script>

<style scoped>
.ai-prediction-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid #e9ecef;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.ai-prediction-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
}

.ai-prediction-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #667eea, #764ba2);
}

.ai-prediction-card.excellent::before {
  background: linear-gradient(90deg, #28a745, #20c997);
}

.ai-prediction-card.very-high::before {
  background: linear-gradient(90deg, #007bff, #0056b3);
}

.ai-prediction-card.high::before {
  background: linear-gradient(90deg, #17a2b8, #138496);
}

.ai-prediction-card.medium::before {
  background: linear-gradient(90deg, #ffc107, #e0a800);
}

.ai-prediction-card.low::before {
  background: linear-gradient(90deg, #fd7e14, #e8680d);
}

.ai-prediction-card.very-low::before {
  background: linear-gradient(90deg, #dc3545, #c82333);
}

.prediction-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
}

.confidence-indicator {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: 12px;
  background: #f8f9fa;
  border: 1px solid #dee2e6;
}

.confidence-icon {
  font-size: 1.5rem;
}

.confidence-info {
  display: flex;
  flex-direction: column;
}

.confidence-level {
  font-size: 0.9rem;
  font-weight: 600;
  color: #495057;
}

.confidence-percent {
  font-size: 1.2rem;
  font-weight: 700;
  color: #667eea;
}

.confidence-indicator.excellent .confidence-percent {
  color: #28a745;
}

.confidence-indicator.very-high .confidence-percent {
  color: #007bff;
}

.confidence-indicator.high .confidence-percent {
  color: #17a2b8;
}

.confidence-indicator.medium .confidence-percent {
  color: #ffc107;
  color: #212529;
}

.confidence-indicator.low .confidence-percent {
  color: #fd7e14;
}

.confidence-indicator.very-low .confidence-percent {
  color: #dc3545;
}

.prediction-time {
  text-align: right;
  font-size: 0.8rem;
  color: #6c757d;
}

.time-label {
  font-weight: 600;
  margin-bottom: 2px;
}

.time-value {
  color: #495057;
}

.prediction-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 12px;
}

.event-info {
  flex: 1;
}

.event-teams {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 1.1rem;
  font-weight: 600;
  color: #212529;
  margin-bottom: 8px;
}

.home-team, .away-team {
  max-width: 150px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.vs-indicator {
  color: #6c757d;
  font-weight: 400;
}

.event-league {
  font-size: 0.9rem;
  color: #6c757d;
  margin-bottom: 4px;
}

.event-time {
  font-size: 0.9rem;
  color: #495057;
  font-weight: 500;
}

.prediction-recommendation {
  display: flex;
  align-items: center;
  gap: 12px;
}

.rec-icon {
  font-size: 2rem;
}

.rec-content {
  display: flex;
  flex-direction: column;
}

.rec-title {
  font-size: 0.8rem;
  color: #6c757d;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.rec-value {
  font-size: 1.1rem;
  font-weight: 700;
  color: #212529;
}

.prediction-reasoning {
  margin-bottom: 20px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 12px;
  border-left: 4px solid #667eea;
}

.reasoning-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}

.reasoning-icon {
  font-size: 1.2rem;
}

.reasoning-title {
  font-size: 0.9rem;
  font-weight: 600;
  color: #495057;
}

.reasoning-text {
  font-size: 0.9rem;
  color: #6c757d;
  line-height: 1.5;
}

.prediction-factors {
  margin-bottom: 20px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 12px;
  border-left: 4px solid #28a745;
}

.factors-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}

.factors-icon {
  font-size: 1.2rem;
}

.factors-title {
  font-size: 0.9rem;
  font-weight: 600;
  color: #495057;
}

.factors-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.factor-item {
  display: flex;
  align-items: flex-start;
  gap: 8px;
}

.factor-bullet {
  color: #28a745;
  font-weight: 600;
  margin-top: 2px;
}

.factor-text {
  font-size: 0.9rem;
  color: #6c757d;
  line-height: 1.4;
}

.prediction-accuracy {
  margin-bottom: 24px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 12px;
  border-left: 4px solid #17a2b8;
}

.accuracy-metrics {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 16px;
}

.accuracy-item {
  text-align: center;
}

.accuracy-label {
  font-size: 0.8rem;
  color: #6c757d;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 4px;
}

.accuracy-value {
  font-size: 1.1rem;
  font-weight: 700;
  color: #495057;
}

.prediction-actions {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 12px;
}

.place-bet-btn, .share-btn {
  padding: 12px 20px;
  border: none;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.place-bet-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.place-bet-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.place-bet-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.share-btn {
  background: #6c757d;
  color: white;
}

.share-btn:hover {
  background: #5a6268;
  transform: translateY(-1px);
}

/* Адаптивность */
@media (max-width: 768px) {
  .ai-prediction-card {
    padding: 20px;
  }

  .prediction-header {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }

  .prediction-time {
    text-align: left;
  }

  .prediction-content {
    flex-direction: column;
    gap: 16px;
    text-align: center;
  }

  .event-teams {
    justify-content: center;
  }

  .prediction-recommendation {
    justify-content: center;
  }

  .accuracy-metrics {
    grid-template-columns: repeat(2, 1fr);
  }

  .prediction-actions {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .ai-prediction-card {
    padding: 16px;
  }

  .accuracy-metrics {
    grid-template-columns: 1fr;
  }

  .event-teams {
    flex-direction: column;
    gap: 8px;
  }

  .home-team, .away-team {
    max-width: none;
  }
}
</style>
