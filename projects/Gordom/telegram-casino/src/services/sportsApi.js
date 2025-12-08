// Реальный API сервис для спортивных данных
import config from '../config.js'

class SportsAPIService {
  constructor() {
    this.baseURL = 'https://api.sportradar.com';
    this.apiKey = config.apiKeys.sportradar;
    this.cache = new Map();
    this.cacheTimeout = config.database.cacheTimeout;
  }

  // Получение событий из Sportradar API
  async getEvents(sport = 'soccer', date = new Date()) {
    const cacheKey = `${sport}_${date.toISOString().split('T')[0]}`;

    if (this.cache.has(cacheKey)) {
      const cached = this.cache.get(cacheKey);
      if (Date.now() - cached.timestamp < this.cacheTimeout) {
        return cached.data;
      }
    }

    try {
      const dateStr = date.toISOString().split('T')[0];
      const response = await fetch(
        `${this.baseURL}/${sport}/trial/v4/en/schedules/${dateStr}/schedule.json?api_key=${this.apiKey}`
      );

      if (!response.ok) {
        throw new Error(`API Error: ${response.status}`);
      }

      const data = await response.json();
      const events = this.transformEvents(data.sport_events || []);

      // Кешируем результат
      this.cache.set(cacheKey, {
        data: events,
        timestamp: Date.now()
      });

      return events;
    } catch (error) {
      console.error('Error fetching events:', error);
      // Fallback к локальным данным если API недоступен
      return this.getFallbackEvents(sport);
    }
  }

  // Получение live событий
  async getLiveEvents(sport = 'soccer') {
    try {
      const response = await fetch(
        `${this.baseURL}/${sport}/trial/v4/en/schedules/live/schedule.json?api_key=${this.apiKey}`
      );

      if (!response.ok) {
        throw new Error(`API Error: ${response.status}`);
      }

      const data = await response.json();
      return this.transformEvents(data.sport_events || []);
    } catch (error) {
      console.error('Error fetching live events:', error);
      return [];
    }
  }

  // Преобразование данных из API в наш формат
  transformEvents(apiEvents) {
    return apiEvents.map(event => ({
      id: event.id,
      sport: event.sport_event_context?.sport?.id || 'unknown',
      sport_name: event.sport_event_context?.sport?.name || 'Unknown',
      league: event.sport_event_context?.competition?.name || 'Unknown League',
      home_team: event.competitors?.find(c => c.qualifier === 'home')?.name || 'Home Team',
      away_team: event.competitors?.find(c => c.qualifier === 'away')?.name || 'Away Team',
      start_time: event.scheduled,
      status: event.event_status,
      is_live: event.event_status === 'live',
      venue: event.venue?.name,
      country: event.venue?.country_name,
      odds: {
        home: event.markets?.find(m => m.name === '2way')?.outcomes?.find(o => o.type === 'home')?.odds || 1.01,
        draw: event.markets?.find(m => m.name === '2way')?.outcomes?.find(o => o.type === 'draw')?.odds || 1.01,
        away: event.markets?.find(m => m.name === '2way')?.outcomes?.find(o => o.type === 'away')?.odds || 1.01
      },
      score: event.sport_event_status?.score,
      period_scores: event.sport_event_status?.period_scores,
      match_time: event.sport_event_status?.match_time,
      // Дополнительные данные для AI анализа
      home_team_stats: event.statistics?.find(s => s.type === 'team' && s.team === 'home'),
      away_team_stats: event.statistics?.find(s => s.type === 'team' && s.team === 'away'),
      lineups: event.lineups,
      injuries: event.injuries,
      weather: event.venue?.weather
    }));
  }

  // Fallback данные если API недоступен
  getFallbackEvents(sport) {
    const fallbacks = {
      soccer: [
        {
          id: 'fallback_1',
          sport: 'soccer',
          sport_name: 'Футбол',
          league: 'Премьер-лига',
          home_team: 'Манчестер Сити',
          away_team: 'Ливерпуль',
          start_time: new Date(Date.now() + 2 * 60 * 60 * 1000).toISOString(), // через 2 часа
          status: 'not_started',
          is_live: false,
          odds: { home: 1.85, draw: 3.40, away: 4.20 }
        },
        {
          id: 'fallback_2',
          sport: 'soccer',
          sport_name: 'Футбол',
          league: 'Ла Лига',
          home_team: 'Барселона',
          away_team: 'Реал Мадрид',
          start_time: new Date(Date.now() + 4 * 60 * 60 * 1000).toISOString(), // через 4 часа
          status: 'not_started',
          is_live: false,
          odds: { home: 2.10, draw: 3.60, away: 3.30 }
        }
      ],
      basketball: [
        {
          id: 'fallback_3',
          sport: 'basketball',
          sport_name: 'Баскетбол',
          league: 'NBA',
          home_team: 'Лейкерс',
          away_team: 'Уорриорз',
          start_time: new Date(Date.now() + 1 * 60 * 60 * 1000).toISOString(),
          status: 'not_started',
          is_live: false,
          odds: { home: 1.75, draw: null, away: 2.15 }
        }
      ]
    };

    return fallbacks[sport] || fallbacks.soccer;
  }

  // Получение коэффициентов от букмекеров
  async getOddsProviders(eventId) {
    try {
      const response = await fetch(
        `${this.baseURL}/oddscomparison/v1/en/eu/sport_events/${eventId}/odds.json?api_key=${this.apiKey}`
      );

      if (!response.ok) {
        throw new Error(`Odds API Error: ${response.status}`);
      }

      const data = await response.json();
      return data.odds_providers || [];
    } catch (error) {
      console.error('Error fetching odds:', error);
      return [];
    }
  }
}

// Экспорт синглтона
export default new SportsAPIService();
