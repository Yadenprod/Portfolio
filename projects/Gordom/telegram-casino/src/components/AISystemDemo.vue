<template>
  <div class="ai-system-demo">
    <div class="demo-header">
      <h2 class="demo-title">🤖 Как работает AI система прогнозов</h2>
      <p class="demo-subtitle">Реальная система анализа спортивных событий</p>
    </div>

    <div class="demo-sections">
      <!-- Источники данных -->
      <div class="demo-section">
        <div class="section-header">
          <div class="section-icon">📡</div>
          <div class="section-title">Источники данных</div>
        </div>
        <div class="section-content">
          <div class="data-sources-grid">
            <div class="data-source-card">
              <div class="source-icon">🏆</div>
              <div class="source-info">
                <div class="source-name">Sportradar API</div>
                <div class="source-description">Профессиональные спортивные данные</div>
                <div class="source-status active">Активен</div>
              </div>
            </div>

            <div class="data-source-card">
              <div class="source-icon">🧠</div>
              <div class="source-info">
                <div class="source-name">OpenAI GPT-4</div>
                <div class="source-description">AI анализ и прогнозы</div>
                <div class="source-status active">Активен</div>
              </div>
            </div>

            <div class="data-source-card">
              <div class="source-icon">💾</div>
              <div class="source-info">
                <div class="source-name">IndexedDB</div>
                <div class="source-description">Локальное хранение данных</div>
                <div class="source-status active">Активен</div>
              </div>
            </div>

            <div class="data-source-card">
              <div class="source-icon">📈</div>
              <div class="source-info">
                <div class="source-name">Историческая статистика</div>
                <div class="source-description">Анализ прошлых матчей</div>
                <div class="source-status active">Активен</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Процесс анализа -->
      <div class="demo-section">
        <div class="section-header">
          <div class="section-icon">⚙️</div>
          <div class="section-title">Процесс AI анализа</div>
        </div>
        <div class="section-content">
          <div class="analysis-steps">
            <div class="step">
              <div class="step-number">1</div>
              <div class="step-content">
                <div class="step-title">Сбор данных</div>
                <div class="step-description">Получение информации о командах, статистике, погоде</div>
              </div>
            </div>

            <div class="step">
              <div class="step-number">2</div>
              <div class="step-content">
                <div class="step-title">AI обработка</div>
                <div class="step-description">Анализ через GPT-4 с учетом всех факторов</div>
              </div>
            </div>

            <div class="step">
              <div class="step-number">3</div>
              <div class="step-content">
                <div class="step-title">Расчет уверенности</div>
                <div class="step-description">Определение уровня достоверности прогноза</div>
              </div>
            </div>

            <div class="step">
              <div class="step-number">4</div>
              <div class="step-content">
                <div class="step-title">Рекомендация</div>
                <div class="step-description">Формирование финального прогноза</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Пример анализа -->
      <div class="demo-section">
        <div class="section-header">
          <div class="section-icon">🎯</div>
          <div class="section-title">Пример AI анализа</div>
        </div>
        <div class="section-content">
          <div class="analysis-example">
            <div class="example-event">
              <div class="event-teams">Манчестер Сити vs Ливерпуль</div>
              <div class="event-league">Премьер-лига • 20 января 2024</div>
            </div>

            <div class="analysis-breakdown">
              <div class="breakdown-item">
                <div class="breakdown-label">Форма команды</div>
                <div class="breakdown-value positive">+ М. Сити: 8 побед подряд</div>
              </div>

              <div class="breakdown-item">
                <div class="breakdown-label">Исторические встречи</div>
                <div class="breakdown-value neutral">5:3 в пользу М. Сити</div>
              </div>

              <div class="breakdown-item">
                <div class="breakdown-label">Домашнее преимущество</div>
                <div class="breakdown-value positive">+ М. Сити выиграл 12 из 15</div>
              </div>

              <div class="breakdown-item">
                <div class="breakdown-label">Травмы/дисквалификации</div>
                <div class="breakdown-value neutral">Без серьезных потерь</div>
              </div>
            </div>

            <div class="analysis-result">
              <div class="result-prediction">
                <div class="prediction-text">🎯 AI рекомендует: Победа Манчестер Сити</div>
                <div class="prediction-confidence">Уверенность: 78%</div>
              </div>

              <div class="result-reasoning">
                <div class="reasoning-title">Обоснование:</div>
                <div class="reasoning-text">
                  Отличная форма команды, преимущество домашнего поля и статистическое превосходство
                  над соперником делают победу Манчестер Сити наиболее вероятным исходом.
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Статистика системы -->
      <div class="demo-section">
        <div class="section-header">
          <div class="section-icon">📊</div>
          <div class="section-title">Статистика AI системы</div>
        </div>
        <div class="section-content">
          <div class="stats-grid">
            <div class="stat-card">
              <div class="stat-icon">🎯</div>
              <div class="stat-info">
                <div class="stat-value">76.5%</div>
                <div class="stat-label">Общая точность</div>
              </div>
            </div>

            <div class="stat-card">
              <div class="stat-icon">⚡</div>
              <div class="stat-info">
                <div class="stat-value">2.3 сек</div>
                <div class="stat-label">Среднее время анализа</div>
              </div>
            </div>

            <div class="stat-card">
              <div class="stat-icon">🔥</div>
              <div class="stat-info">
                <div class="stat-value">1,247</div>
                <div class="stat-label">Прогнозов за месяц</div>
              </div>
            </div>

            <div class="stat-card">
              <div class="stat-icon">👥</div>
              <div class="stat-info">
                <div class="stat-value">89%</div>
                <div class="stat-label">Доверие пользователей</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Технологии -->
      <div class="demo-section">
        <div class="section-header">
          <div class="section-icon">💻</div>
          <div class="section-title">Технологии</div>
        </div>
        <div class="section-content">
          <div class="tech-stack">
            <div class="tech-category">
              <div class="category-name">AI & Machine Learning</div>
              <div class="tech-list">
                <span class="tech-item">OpenAI GPT-4</span>
                <span class="tech-item">TensorFlow.js</span>
                <span class="tech-item">Scikit-learn</span>
              </div>
            </div>

            <div class="tech-category">
              <div class="category-name">Data Sources</div>
              <div class="tech-list">
                <span class="tech-item">Sportradar API</span>
                <span class="tech-item">OddsPortal API</span>
                <span class="tech-item">Weather API</span>
              </div>
            </div>

            <div class="tech-category">
              <div class="category-name">Frontend</div>
              <div class="tech-list">
                <span class="tech-item">Vue 3</span>
                <span class="tech-item">Pinia</span>
                <span class="tech-item">WebSocket</span>
              </div>
            </div>

            <div class="tech-category">
              <div class="category-name">Storage</div>
              <div class="tech-list">
                <span class="tech-item">IndexedDB</span>
                <span class="tech-item">LocalStorage</span>
                <span class="tech-item">Service Worker</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="demo-footer">
      <div class="footer-note">
        <div class="note-icon">ℹ️</div>
        <div class="note-text">
          <strong>Важно:</strong> AI прогнозы носят рекомендательный характер.
          Всегда делайте ставки осознанно и в рамках своих финансовых возможностей.
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AISystemDemo'
}
</script>

<style scoped>
.ai-system-demo {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
  background: #f8f9fa;
  min-height: 100vh;
}

.demo-header {
  text-align: center;
  margin-bottom: 40px;
}

.demo-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #212529;
  margin-bottom: 16px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.demo-subtitle {
  font-size: 1.1rem;
  color: #6c757d;
  max-width: 600px;
  margin: 0 auto;
}

.demo-sections {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.demo-section {
  background: white;
  border-radius: 16px;
  padding: 32px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid #e9ecef;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}

.section-icon {
  font-size: 2rem;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  color: white;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #212529;
}

.data-sources-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
}

.data-source-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 12px;
  border: 1px solid #dee2e6;
  transition: all 0.3s ease;
}

.data-source-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.source-icon {
  font-size: 1.5rem;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.source-info {
  flex: 1;
}

.source-name {
  font-size: 1rem;
  font-weight: 600;
  color: #212529;
  margin-bottom: 4px;
}

.source-description {
  font-size: 0.9rem;
  color: #6c757d;
  margin-bottom: 8px;
}

.source-status {
  font-size: 0.8rem;
  font-weight: 600;
  padding: 4px 8px;
  border-radius: 12px;
  width: fit-content;
}

.source-status.active {
  background: #d4edda;
  color: #155724;
}

.analysis-steps {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.step {
  display: flex;
  align-items: flex-start;
  gap: 16px;
}

.step-number {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #667eea;
  color: white;
  border-radius: 50%;
  font-size: 0.9rem;
  font-weight: 600;
  flex-shrink: 0;
}

.step-content {
  flex: 1;
}

.step-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #212529;
  margin-bottom: 4px;
}

.step-description {
  font-size: 0.9rem;
  color: #6c757d;
  line-height: 1.5;
}

.analysis-example {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 24px;
}

.example-event {
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid #dee2e6;
}

.event-teams {
  font-size: 1.3rem;
  font-weight: 600;
  color: #212529;
  margin-bottom: 8px;
}

.event-league {
  font-size: 0.9rem;
  color: #6c757d;
}

.analysis-breakdown {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 24px;
}

.breakdown-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: white;
  border-radius: 8px;
  border: 1px solid #dee2e6;
}

.breakdown-label {
  font-size: 0.9rem;
  font-weight: 600;
  color: #495057;
}

.breakdown-value {
  font-size: 0.9rem;
  font-weight: 500;
}

.breakdown-value.positive {
  color: #28a745;
}

.breakdown-value.negative {
  color: #dc3545;
}

.breakdown-value.neutral {
  color: #6c757d;
}

.analysis-result {
  background: white;
  border-radius: 12px;
  padding: 20px;
  border: 1px solid #667eea;
}

.result-prediction {
  margin-bottom: 16px;
}

.prediction-text {
  font-size: 1.2rem;
  font-weight: 600;
  color: #212529;
  margin-bottom: 8px;
}

.prediction-confidence {
  font-size: 0.9rem;
  color: #28a745;
  font-weight: 600;
}

.result-reasoning {
  padding-top: 16px;
  border-top: 1px solid #e9ecef;
}

.reasoning-title {
  font-size: 0.9rem;
  font-weight: 600;
  color: #495057;
  margin-bottom: 8px;
}

.reasoning-text {
  font-size: 0.9rem;
  color: #6c757d;
  line-height: 1.5;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.stat-card {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 20px;
  text-align: center;
  border: 1px solid #dee2e6;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  font-size: 2rem;
  margin-bottom: 12px;
}

.stat-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #212529;
}

.stat-label {
  font-size: 0.9rem;
  color: #6c757d;
  font-weight: 500;
}

.tech-stack {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.tech-category {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.category-name {
  font-size: 1rem;
  font-weight: 600;
  color: #495057;
}

.tech-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tech-item {
  padding: 6px 12px;
  background: #e9ecef;
  color: #495057;
  border-radius: 16px;
  font-size: 0.8rem;
  font-weight: 600;
}

.demo-footer {
  margin-top: 40px;
  padding: 24px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.footer-note {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.note-icon {
  font-size: 1.2rem;
  flex-shrink: 0;
}

.note-text {
  font-size: 0.9rem;
  color: #6c757d;
  line-height: 1.5;
}

.note-text strong {
  color: #495057;
}

/* Адаптивность */
@media (max-width: 768px) {
  .ai-system-demo {
    padding: 20px 15px;
  }

  .demo-title {
    font-size: 2rem;
  }

  .demo-sections {
    gap: 24px;
  }

  .demo-section {
    padding: 24px;
  }

  .data-sources-grid {
    grid-template-columns: 1fr;
  }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .step {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .breakdown-item {
    flex-direction: column;
    gap: 8px;
    align-items: flex-start;
  }
}

@media (max-width: 480px) {
  .demo-title {
    font-size: 1.5rem;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .tech-list {
    justify-content: center;
  }
}
</style>
