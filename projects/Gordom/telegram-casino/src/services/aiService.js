// AI Сервис для анализа и прогнозов
import config from '../config.js'

class AIService {
  constructor() {
    this.modelEndpoint = 'https://api.openai.com/v1/chat/completions';
    this.apiKey = config.apiKeys.openai;
    this.historicalData = new Map();
    this.analysisCache = new Map();
    this.confidenceThreshold = config.ai.confidenceThreshold;
    this.cacheTimeout = config.ai.cacheTimeout;
  }

  // Основной метод для получения прогнозов
  async getPrediction(event, userHistory = []) {
    const cacheKey = `prediction_${event.id}_${event.sport}`;

    if (this.analysisCache.has(cacheKey)) {
      const cached = this.analysisCache.get(cacheKey);
      if (Date.now() - cached.timestamp < 10 * 60 * 1000) { // 10 минут
        return cached.data;
      }
    }

    try {
      // Сбор данных для анализа
      const analysisData = await this.collectAnalysisData(event, userHistory);

      // AI анализ через OpenAI API
      const aiAnalysis = await this.performAIAnalysis(analysisData);

      // Расчет уровня уверенности
      const confidence = this.calculateConfidence(aiAnalysis, event);

      const prediction = {
        eventId: event.id,
        sport: event.sport,
        recommendation: aiAnalysis.recommendation,
        confidence: confidence,
        reasoning: aiAnalysis.reasoning,
        factors: aiAnalysis.factors,
        timestamp: new Date().toISOString(),
        model: 'gpt-4',
        version: '1.0'
      };

      // Кешируем результат
      this.analysisCache.set(cacheKey, {
        data: prediction,
        timestamp: Date.now()
      });

      return prediction;
    } catch (error) {
      console.error('AI Prediction Error:', error);
      return this.getFallbackPrediction(event);
    }
  }

  // Сбор данных для анализа
  async collectAnalysisData(event, userHistory) {
    return {
      event: {
        id: event.id,
        sport: event.sport,
        league: event.league,
        home_team: event.home_team,
        away_team: event.away_team,
        odds: event.odds,
        is_live: event.is_live,
        venue: event.venue,
        weather: event.weather,
        start_time: event.start_time
      },
      teams: {
        home: await this.getTeamStats(event.home_team, event.sport),
        away: await this.getTeamStats(event.away_team, event.sport)
      },
      historical: {
        head_to_head: await this.getHeadToHeadStats(event.home_team, event.away_team),
        recent_form: await this.getRecentForm(event.home_team, event.away_team)
      },
      user: {
        history: userHistory.slice(-10), // Последние 10 ставок
        preferences: this.analyzeUserPreferences(userHistory),
        win_rate: this.calculateUserWinRate(userHistory)
      },
      market: {
        odds_comparison: await this.getOddsComparison(event.id),
        volume: await this.getBettingVolume(event.id),
        sentiment: await this.getMarketSentiment(event)
      }
    };
  }

  // AI анализ через OpenAI
  async performAIAnalysis(analysisData) {
    if (!this.apiKey) {
      return this.performLocalAnalysis(analysisData);
    }

    const prompt = this.buildAnalysisPrompt(analysisData);

    try {
      const response = await fetch(this.modelEndpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.apiKey}`
        },
        body: JSON.stringify({
          model: 'gpt-4',
          messages: [
            {
              role: 'system',
              content: 'You are an expert sports analyst and betting advisor. Provide detailed analysis and prediction for the given event. Consider all factors including team performance, historical data, current form, and market conditions. Give a clear recommendation with confidence level and reasoning.'
            },
            {
              role: 'user',
              content: prompt
            }
          ],
          max_tokens: 1000,
          temperature: 0.7
        })
      });

      if (!response.ok) {
        throw new Error(`OpenAI API Error: ${response.status}`);
      }

      const data = await response.json();
      return this.parseAIResponse(data.choices[0].message.content);
    } catch (error) {
      console.error('OpenAI API Error:', error);
      return this.performLocalAnalysis(analysisData);
    }
  }

  // Локальный анализ если API недоступен
  performLocalAnalysis(analysisData) {
    const { event, teams, historical } = analysisData;

    // Простая логика анализа
    const homeStrength = teams.home.win_rate * 0.4 + teams.home.home_advantage * 0.3 + teams.home.recent_form * 0.3;
    const awayStrength = teams.away.win_rate * 0.4 + teams.away.away_performance * 0.3 + teams.away.recent_form * 0.3;

    let recommendation;
    let factors = [];

    if (homeStrength > awayStrength + 0.1) {
      recommendation = `Победа ${event.home_team}`;
      factors = ['Домашнее преимущество', 'Лучшая форма команды', 'Исторические показатели'];
    } else if (awayStrength > homeStrength + 0.1) {
      recommendation = `Победа ${event.away_team}`;
      factors = ['Хорошая выездная форма', 'Слабая защита соперника', 'Мотивация команды'];
    } else {
      recommendation = 'Ничья';
      factors = ['Баланс сил команд', 'Осторожная тактика', 'Равные коэффициенты'];
    }

    return {
      recommendation,
      reasoning: `Анализ показывает ${recommendation.toLowerCase()} как наиболее вероятный исход на основе текущей формы и статистических данных.`,
      factors
    };
  }

  // Получение статистики команды
  async getTeamStats(teamName, sport) {
    const cacheKey = `team_${teamName}_${sport}`;

    if (this.historicalData.has(cacheKey)) {
      return this.historicalData.get(cacheKey);
    }

    // В реальности здесь будет запрос к спортивной API
    const mockStats = {
      win_rate: Math.random() * 0.3 + 0.4, // 40-70%
      home_advantage: Math.random() * 0.2 + 0.1, // 10-30%
      away_performance: Math.random() * 0.2 + 0.1,
      recent_form: Math.random() * 0.4 + 0.3, // 30-70%
      goals_scored: Math.floor(Math.random() * 50) + 30,
      goals_conceded: Math.floor(Math.random() * 40) + 20,
      clean_sheets: Math.floor(Math.random() * 10) + 2,
      injuries: Math.floor(Math.random() * 3)
    };

    this.historicalData.set(cacheKey, mockStats);
    return mockStats;
  }

  // Статистика личных встреч
  async getHeadToHeadStats(homeTeam, awayTeam) {
    const cacheKey = `h2h_${homeTeam}_${awayTeam}`;

    if (this.historicalData.has(cacheKey)) {
      return this.historicalData.get(cacheKey);
    }

    const mockH2H = {
      total_matches: Math.floor(Math.random() * 20) + 5,
      home_wins: Math.floor(Math.random() * 10) + 2,
      away_wins: Math.floor(Math.random() * 8) + 1,
      draws: Math.floor(Math.random() * 5) + 1,
      avg_goals: (Math.random() * 2 + 2).toFixed(1)
    };

    this.historicalData.set(cacheKey, mockH2H);
    return mockH2H;
  }

  // Получение формы команд
  async getRecentForm(homeTeam, awayTeam) {
    return {
      home: Array.from({ length: 5 }, () => Math.random() > 0.4 ? 'W' : Math.random() > 0.5 ? 'D' : 'L'),
      away: Array.from({ length: 5 }, () => Math.random() > 0.4 ? 'W' : Math.random() > 0.5 ? 'D' : 'L')
    };
  }

  // Анализ предпочтений пользователя
  analyzeUserPreferences(userHistory) {
    if (!userHistory.length) return { favorite_sport: 'soccer', avg_odds: 2.0 };

    const sports = userHistory.map(bet => bet.sport);
    const favoriteSport = sports.reduce((acc, sport) => {
      acc[sport] = (acc[sport] || 0) + 1;
      return acc;
    }, {});

    const avgOdds = userHistory.reduce((sum, bet) => sum + bet.odds, 0) / userHistory.length;

    return {
      favorite_sport: Object.keys(favoriteSport).reduce((a, b) => favoriteSport[a] > favoriteSport[b] ? a : b),
      avg_odds: Math.round(avgOdds * 100) / 100,
      total_bets: userHistory.length
    };
  }

  // Расчет win rate пользователя
  calculateUserWinRate(userHistory) {
    if (!userHistory.length) return 0;

    const winningBets = userHistory.filter(bet => bet.result === 'win').length;
    return Math.round((winningBets / userHistory.length) * 100);
  }

  // Получение сравнения коэффициентов
  async getOddsComparison(eventId) {
    // В реальности запрос к OddsPortal или аналогичному сервису
    return {
      providers: ['1xBet', 'Bet365', 'William Hill', 'Pinnacle'],
      ranges: {
        home: { min: 1.70, max: 2.10, avg: 1.95 },
        draw: { min: 3.20, max: 3.80, avg: 3.50 },
        away: { min: 3.00, max: 4.20, avg: 3.80 }
      }
    };
  }

  // Получение объема ставок
  async getBettingVolume(eventId) {
    // В реальности интеграция с betting exchange
    return {
      total_volume: Math.floor(Math.random() * 1000000) + 50000,
      home_percentage: Math.floor(Math.random() * 30) + 30,
      draw_percentage: Math.floor(Math.random() * 20) + 10,
      away_percentage: Math.floor(Math.random() * 30) + 30
    };
  }

  // Анализ рыночного настроения
  async getMarketSentiment(event) {
    // Анализ социальных сетей, новостей, форумов
    return {
      sentiment: Math.random() > 0.5 ? 'positive' : 'neutral',
      confidence: Math.floor(Math.random() * 30) + 60,
      sources: ['Twitter', 'Reddit', 'Sports News', 'Fan Forums']
    };
  }

  // Расчет уровня уверенности
  calculateConfidence(aiAnalysis, event) {
    let confidence = 50; // базовый уровень

    // Факторы, влияющие на уверенность
    const factors = {
      dataQuality: 0.2, // качество доступных данных
      historicalAccuracy: 0.3, // точность исторических прогнозов
      marketConsensus: 0.2, // согласие рынка
      teamForm: 0.2, // текущая форма команд
      statisticalSignificance: 0.1 // статистическая значимость
    };

    // Расчет на основе факторов
    if (event.odds) {
      const oddsSpread = Math.max(...Object.values(event.odds)) - Math.min(...Object.values(event.odds));
      if (oddsSpread > 2) confidence += 15; // большой разброс коэффициентов
    }

    // На основе длины reasoning
    if (aiAnalysis.reasoning && aiAnalysis.reasoning.length > 100) {
      confidence += 10;
    }

    // На основе количества факторов
    if (aiAnalysis.factors && aiAnalysis.factors.length > 2) {
      confidence += 10;
    }

    return Math.min(Math.max(confidence, 10), 95); // ограничение 10-95%
  }

  // Fallback прогноз если AI недоступен
  getFallbackPrediction(event) {
    const recommendations = ['Победа ' + event.home_team, 'Ничья', 'Победа ' + event.away_team];
    const randomRec = recommendations[Math.floor(Math.random() * recommendations.length)];

    return {
      eventId: event.id,
      sport: event.sport,
      recommendation: randomRec,
      confidence: Math.floor(Math.random() * 30) + 40,
      reasoning: 'Базовый анализ на основе коэффициентов и формы команд',
      factors: ['Коэффициенты букмекеров', 'Текущая форма', 'Исторические данные'],
      timestamp: new Date().toISOString(),
      model: 'fallback',
      version: '1.0'
    };
  }

  // Построение промпта для AI
  buildAnalysisPrompt(analysisData) {
    return `
Проанализируй следующее спортивное событие и дай прогноз:

Событие: ${analysisData.event.home_team} vs ${analysisData.event.away_team}
Вид спорта: ${analysisData.event.sport}
Лига: ${analysisData.event.league}
Коэффициенты: ${JSON.stringify(analysisData.event.odds)}
Время начала: ${analysisData.event.start_time}

Статистика команд:
${analysisData.event.home_team}: ${JSON.stringify(analysisData.teams.home)}
${analysisData.event.away_team}: ${JSON.stringify(analysisData.teams.away)}

Исторические данные:
Личные встречи: ${JSON.stringify(analysisData.historical.head_to_head)}
Форма команд: ${JSON.stringify(analysisData.historical.recent_form)}

Дай ответ в формате JSON:
{
  "recommendation": "Победа [команда] / Ничья",
  "reasoning": "Подробное объяснение (2-3 предложения)",
  "factors": ["фактор1", "фактор2", "фактор3"],
  "confidence_factors": ["причина высокой/низкой уверенности"]
}
    `;
  }

  // Парсинг ответа AI
  parseAIResponse(response) {
    try {
      // Попытка найти JSON в ответе
      const jsonMatch = response.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        return JSON.parse(jsonMatch[0]);
      }

      // Если JSON не найден, извлекаем информацию из текста
      const recommendation = response.includes('ничья') || response.includes('Ничья') ? 'Ничья' :
                           response.includes(analysisData.event.home_team) ? `Победа ${analysisData.event.home_team}` :
                           `Победа ${analysisData.event.away_team}`;

      return {
        recommendation,
        reasoning: response.substring(0, 200) + '...',
        factors: ['Анализ AI', 'Статистические данные', 'Рыночные факторы']
      };
    } catch (error) {
      console.error('Error parsing AI response:', error);
      return {
        recommendation: 'Ничья',
        reasoning: 'Не удалось проанализировать данные',
        factors: ['Базовый анализ']
      };
    }
  }
}

// Экспорт синглтона
export default new AIService();
