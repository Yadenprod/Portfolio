// Конфигурация приложения
export const config = {
  // API Keys
  apiKeys: {
    sportradar: 'demo_key',
    openai: null, // Установите ваш API key
    telegramBot: null,

    // Реальные спортивные API
    sportsdata: 'YOUR_SPORTSDATA_API_KEY', // https://sportsdata.io
    rapidapi: 'YOUR_RAPIDAPI_KEY', // https://rapidapi.com
    oddsapi: 'YOUR_ODDS_API_KEY', // https://the-odds-api.com
    footballData: 'YOUR_FOOTBALL_DATA_KEY' // https://www.football-data.org
  },

  // API URLs
  apiUrls: {
    base: 'http://localhost:3001/api',
    admin: 'http://localhost:3000/api/admin',
    websocket: 'ws://localhost:3001/ws',

    // Реальные спортивные API endpoints
    sportsdata: {
      football: 'https://api.sportsdata.io/v3/soccer/scores/json',
      basketball: 'https://api.sportsdata.io/v3/nba/scores/json',
      tennis: 'https://api.sportsdata.io/v3/tennis/scores/json'
    },

    rapidapi: {
      football: 'https://api-football-v1.p.rapidapi.com/v3',
      basketball: 'https://api-basketball-v1.p.rapidapi.com/v2',
      odds: 'https://odds.p.rapidapi.com/v4'
    },

    oddsapi: {
      sports: 'https://api.the-odds-api.com/v4/sports',
      odds: 'https://api.the-odds-api.com/v4/sports'
    },

    footballData: 'https://api.football-data.org/v4'
  },

  // Настройки приложения
  settings: {
    environment: 'development',
    enableAI: true,
    enableRealTime: true,
    fallbackMode: true, // Включить fallback для локальных данных
    useRealSportsData: true, // Использовать реальные спортивные данные
    preferredSportsAPI: 'sportsdata', // sportsdata, rapidapi, oddsapi, footballData
    enableLiveUpdates: true, // Включить live обновления
    enableBettingOdds: true // Включить коэффициенты ставок
  },

  // Настройки AI
  ai: {
    confidenceThreshold: 60, // Минимальный уровень уверенности в %
    cacheTimeout: 10 * 60 * 1000, // 10 минут
    maxRetries: 3
  },

  // Настройки базы данных
  database: {
    name: 'SportsBettingDB',
    version: 1,
    cacheTimeout: 5 * 60 * 1000 // 5 минут
  }
}

// Экспорт для использования в компонентах
export default config
