import api from './index'
import { config } from '../config'

function mockDelay(result, ms = 500) {
  return new Promise((resolve) => setTimeout(() => resolve(result), ms))
}

// Получение событий созданных администратором
function getAdminEvents() {
  try {
    const savedEvents = localStorage.getItem('admin_events')
    if (savedEvents) {
      const events = JSON.parse(savedEvents)
      // Добавляем недостающие поля для совместимости
      return events.map(event => ({
        ...event,
        sport_name: event.sport_name || getSportDisplayName(event.sport),
        current_score: event.current_score || { home: 0, away: 0 },
        odds: event.odds || generateDefaultOdds(event.sport),
        venue: event.venue || 'Unknown Venue',
        attendance: event.attendance || 0,
        importance: event.importance || 'medium'
      }))
    }
  } catch (error) {
    console.error('Error loading admin events:', error)
  }
  return []
}

function getSportDisplayName(sport) {
  const names = {
    football: 'Футбол',
    basketball: 'Баскетбол',
    tennis: 'Теннис',
    hockey: 'Хоккей',
    csgo: 'CS:GO',
    dota2: 'Dota 2'
  }
  return names[sport] || sport
}

function generateDefaultOdds(sport) {
  const baseOdds = {
    football: {
      home: 2.10,
      draw: 3.40,
      away: 3.20,
      over_2_5: 1.85,
      under_2_5: 1.95,
      btts_yes: 1.65,
      btts_no: 2.20
    },
    basketball: {
      home: 1.75,
      away: 2.05,
      over_210_5: 1.90,
      under_210_5: 1.90
    },
    tennis: {
      home: 1.65,
      away: 2.20,
      over_22_5_games: 1.80,
      under_22_5_games: 2.00
    }
  }
  return baseOdds[sport] || baseOdds.football
}

export async function getMe() {
  const { data } = await api.get('/auth/telegram/me')
  if (!data.success) {
    throw new Error(data.message || 'Failed to get user data')
  }
  return {
    user: data.user,
    balance: data.user.balance
  }
}

export async function postBet(game, payload) {
  const { data } = await api.post(`/games/${game}/bet`, payload)
  if (!data.success) {
    throw new Error(data.message || 'Bet failed')
  }
  return data
}

export async function deposit(amount) {
  const { data } = await api.post('/wallet/deposit', { amount })
  if (!data.success) {
    throw new Error(data.message || 'Deposit failed')
  }
  return data
}

export async function withdraw(amount) {
  const { data } = await api.post('/wallet/withdraw', { amount })
  if (!data.success) {
    throw new Error(data.message || 'Withdraw failed')
  }
  return data
}

export async function activatePromo(code) {
  try {
    const { data } = await api.post('/promo/activate', { code })
    if (data.success) {
      return data
    }
    throw new Error(data.message || 'Promo activation failed')
  } catch (error) {
    console.error('API Error (activatePromo):', error)
    const reward = Math.floor(Math.random() * 100) + 10
    return mockDelay({
      success: true,
      reward: reward,
      message: `Промокод активирован! Получено ${reward}₽`
    })
  }
}

export async function getReferralStats() {
  try {
    const { data } = await api.get('/referrals/stats')
    if (data.success) {
      return data
    }
    throw new Error(data.message || 'Failed to get referral stats')
  } catch (error) {
    console.error('API Error (getReferralStats):', error)
    return mockDelay({
      success: true,
      invited: 12,
      earnings: 345.5,
      pending: 2
    })
  }
}

export async function getHistory(limit = 25) {
  const { data } = await api.get('/history', { params: { limit } })
  if (!data.success) {
    throw new Error(data.message || 'Failed to get history')
  }
  return data
}

// Новые API endpoints для улучшенной функциональности
export async function getChatMessages(limit = 50) {
  try {
    const { data } = await api.get('/chat/messages', { params: { limit } })
    return data.success ? data.messages : []
  } catch (error) {
    console.error('API Error (getChatMessages):', error)
    return []
  }
}

export async function sendChatMessage(message) {
  try {
    const { data } = await api.post('/chat/send', { message })
    return data.success
  } catch (error) {
    console.error('API Error (sendChatMessage):', error)
    return false
  }
}

export async function getOnlinePlayers() {
  try {
    const { data } = await api.get('/players/online')
    return data.success ? data.count : 0
  } catch (error) {
    console.error('API Error (getOnlinePlayers):', error)
    return Math.floor(Math.random() * 200) + 50
  }
}

export async function getLeaderboard(limit = 10) {
  try {
    const { data } = await api.get('/leaderboard', { params: { limit } })
    return data.success ? data.players : []
  } catch (error) {
    console.error('API Error (getLeaderboard):', error)
    return Array.from({ length: limit }).map((_, i) => ({
      id: i + 1,
      name: `Player ${i + 1}`,
      balance: Math.floor(Math.random() * 10000) + 1000,
      rank: i + 1
    }))
  }
}

export async function getActiveTournaments() {
  try {
    const { data } = await api.get('/tournaments/active')
    return data.success ? data.tournaments : []
  } catch (error) {
    console.error('API Error (getActiveTournaments):', error)
    return []
  }
}

export async function joinTournament(tournamentId) {
  try {
    const { data } = await api.post('/tournaments/join', { tournament_id: tournamentId })
    return data.success
  } catch (error) {
    console.error('API Error (joinTournament):', error)
    return false
  }
}

export async function getUserAchievements() {
  try {
    const { data } = await api.get('/achievements')
    return data.success ? data.achievements : []
  } catch (error) {
    console.error('API Error (getUserAchievements):', error)
    return []
  }
}

// Новые API endpoints для бонусов и промокодов
export async function getAvailableBonuses() {
  try {
    const { data } = await api.get('/bonuses/available')
    return data.success ? data.bonuses : []
  } catch (error) {
    console.error('API Error (getAvailableBonuses):', error)
    return []
  }
}

export async function claimBonus(bonusId) {
  try {
    const { data } = await api.post('/bonuses/claim', { bonus_id: bonusId })
    if (data.success) {
      return data
    }
    throw new Error(data.message || 'Failed to claim bonus')
  } catch (error) {
    console.error('API Error (claimBonus):', error)
    return { success: false, message: 'Ошибка при получении бонуса' }
  }
}

export async function getDailyBonus() {
  try {
    const { data } = await api.get('/bonuses/daily')
    return data.success ? data : null
  } catch (error) {
    console.error('API Error (getDailyBonus):', error)
    return null
  }
}

export async function claimDailyBonus() {
  try {
    const { data } = await api.post('/bonuses/daily/claim')
    if (data.success) {
      return data
    }
    throw new Error(data.message || 'Failed to claim daily bonus')
  } catch (error) {
    console.error('API Error (claimDailyBonus):', error)
    return { success: false, message: 'Ошибка при получении ежедневного бонуса' }
  }
}

export async function getBonusHistory() {
  try {
    const { data } = await api.get('/bonuses/history')
    return data.success ? data.history : []
  } catch (error) {
    console.error('API Error (getBonusHistory):', error)
    return []
  }
}

export async function getActivePromocodes() {
  try {
    const { data } = await api.get('/promocodes/active')
    return data.success ? data.promocodes : []
  } catch (error) {
    console.error('API Error (getActivePromocodes):', error)
    return []
  }
}

export async function activatePromocode(code) {
  try {
    const { data } = await api.post('/promo/activate', { code })
    if (data.success) {
      return data
    }
    throw new Error(data.message || 'Failed to activate promocode')
  } catch (error) {
    console.error('API Error (activatePromocode):', error)
    return { success: false, message: 'Ошибка при активации промокода' }
  }
}

export async function getWheelOfFortune() {
  try {
    const { data } = await api.get('/bonuses/wheel')
    return data.success ? data : null
  } catch (error) {
    console.error('API Error (getWheelOfFortune):', error)
    return null
  }
}

export async function spinWheelOfFortune() {
  try {
    const { data } = await api.post('/bonuses/wheel/spin')
    if (data.success) {
      return data
    }
    throw new Error(data.message || 'Failed to spin wheel')
  } catch (error) {
    console.error('API Error (spinWheelOfFortune):', error)
    return { success: false, message: 'Ошибка при вращении колеса' }
  }
}

// === БУКМЕКЕРСКИЕ СТАВКИ API ===

// Получить список доступных спортивных событий
export async function getSportsEvents(sport = 'football') {
  try {
    const { data } = await api.get('/sports/events')
    if (data.success) {
      return data.events
    }
    throw new Error(data.message || 'Failed to get sports events')
  } catch (error) {
    console.error('API Error (getSportsEvents):', error)

    // Пытаемся получить реальные данные
    if (config.settings.useRealSportsData) {
      try {
        const realSportsApi = await import('../services/realSportsApi.js')
        const realEvents = await realSportsApi.default.getEvents(sport)
        if (realEvents && realEvents.length > 0) {
          console.log('✅ Using real sports data from API')
          return mockDelay(realEvents)
        }
      } catch (realApiError) {
        console.error('Real API Error:', realApiError)
      }
    }

    console.log('📊 Using mock data (fallback mode)')

    // Проверяем локальные события от админа
    const adminEvents = getAdminEvents()
    if (adminEvents.length > 0) {
      console.log('✅ Using admin-created events')
      return mockDelay(adminEvents.filter(e => e.sport === sport))
    }

    // Реалистичные данные для демонстрации
    return mockDelay([
      {
        id: 1,
        sport: 'football',
        sport_name: 'Футбол',
        league: 'Английская Премьер-лига',
        home_team: 'Манчестер Сити',
        away_team: 'Арсенал',
        start_time: new Date(Date.now() + 1800000).toISOString(), // через 30 мин
        status: 'upcoming',
        odds: {
          home: 2.10,
          draw: 3.40,
          away: 3.20,
          over_2_5: 1.85,
          under_2_5: 1.95,
          btts_yes: 1.65,
          btts_no: 2.20,
          home_minus_1_5: 3.20,
          away_plus_1_5: 1.35
        },
        is_live: false,
        venue: 'Этихад Стэдиум',
        attendance: 53000,
        importance: 'high'
      },
      {
        id: 2,
        sport: 'football',
        sport_name: 'Футбол',
        league: 'Итальянская Серия А',
        home_team: 'Интер Милан',
        away_team: 'Милан',
        start_time: new Date(Date.now() + 3600000).toISOString(), // через 1 час
        status: 'upcoming',
        odds: {
          home: 2.25,
          draw: 3.10,
          away: 3.00,
          over_2_5: 1.90,
          under_2_5: 1.90,
          btts_yes: 1.80,
          btts_no: 2.00,
          home_minus_0_5: 1.75,
          away_plus_0_5: 2.05
        },
        is_live: false,
        venue: 'Джузеппе Меацца',
        attendance: 75000,
        importance: 'high'
      },
      {
        id: 3,
        sport: 'basketball',
        sport_name: 'Баскетбол',
        league: 'NBA',
        home_team: 'Бостон Селтикс',
        away_team: 'Милуоки Бакс',
        start_time: new Date(Date.now() + 900000).toISOString(), // через 15 мин
        status: 'upcoming',
        odds: {
          home: 1.65,
          away: 2.20,
          over_218_5: 1.85,
          under_218_5: 1.95,
          home_spread_minus_4_5: 1.90,
          away_spread_plus_4_5: 1.90
        },
        is_live: false,
        arena: 'TD Garden'
      },
      {
        id: 4,
        sport: 'tennis',
        sport_name: 'Теннис',
        league: 'ATP Masters 1000',
        home_team: 'Карлос Алькарас',
        away_team: 'Даниил Медведев',
        start_time: new Date(Date.now() + 7200000).toISOString(), // через 2 часа
        status: 'upcoming',
        odds: {
          home: 1.45,
          away: 2.70,
          over_22_5_games: 1.60,
          under_22_5_games: 2.25,
          home_to_win_set: 1.35,
          away_to_win_set: 3.10
        },
        is_live: false,
        surface: 'Хард',
        tournament: 'Майами Опен'
      },
      {
        id: 5,
        sport: 'csgo',
        sport_name: 'CS:GO',
        league: 'ESL Pro League Season 18',
        home_team: 'Vitality',
        away_team: 'G2 Esports',
        start_time: new Date(Date.now() + 2400000).toISOString(), // через 40 мин
        status: 'upcoming',
        odds: {
          home: 1.85,
          away: 1.95,
          first_map_vitality: 1.60,
          first_map_g2: 2.25,
          total_maps_over_2_5: 1.75,
          total_maps_under_2_5: 2.05,
          home_minus_1_5_maps: 2.10,
          away_plus_1_5_maps: 1.70
        },
        is_live: false,
        game_type: 'bo3',
        tournament: 'ESL Pro League'
      },
      {
        id: 6,
        sport: 'dota2',
        sport_name: 'Dota 2',
        league: 'DPC EU Division I',
        home_team: 'Team Secret',
        away_team: 'OG',
        start_time: new Date(Date.now() + 4800000).toISOString(), // через 1.3 часа
        status: 'upcoming',
        odds: {
          home: 2.15,
          away: 1.70,
          first_blood_team_secret: 2.30,
          first_blood_og: 1.60,
          total_kills_over_42_5: 1.85,
          total_kills_under_42_5: 1.95,
          home_minus_8_5_kills: 2.05,
          away_plus_8_5_kills: 1.75
        },
        is_live: false,
        game_type: 'bo3',
        region: 'Европа'
      },
      {
        id: 7,
        sport: 'lol',
        sport_name: 'League of Legends',
        league: 'LCK Spring Split',
        home_team: 'T1',
        away_team: 'Gen.G',
        start_time: new Date(Date.now() + 900000).toISOString(), // через 15 мин
        status: 'upcoming',
        odds: {
          home: 1.40,
          away: 2.80,
          first_blood_home: 1.70,
          first_blood_away: 2.10,
          baron_control_home: 1.90,
          baron_control_away: 1.85
        },
        is_live: false,
        game_type: 'bo3'
      },
      {
        id: 9,
        sport: 'valorant',
        sport_name: 'Valorant',
        league: 'VCT Americas',
        home_team: 'Sentinels',
        away_team: 'LOUD',
        start_time: new Date(Date.now() + 2700000).toISOString(), // через 45 мин
        status: 'upcoming',
        odds: {
          home: 1.65,
          away: 2.20,
          first_blood_home: 1.75,
          first_blood_away: 2.05,
          total_rounds_over_26: 1.55,
          total_rounds_under_26: 2.40
        },
        is_live: false,
        game_type: 'bo3'
      },
      {
        id: 10,
        sport: 'pubg',
        sport_name: 'PUBG Mobile',
        league: 'PMPL',
        home_team: 'Nigma Galaxy',
        away_team: 'Regans Gaming',
        start_time: new Date(Date.now() + 5400000).toISOString(), // через 1.5 часа
        status: 'upcoming',
        odds: {
          home: 1.80,
          away: 1.95,
          chicken_dinner_home: 2.10,
          chicken_dinner_away: 1.70,
          total_kills_over_25: 1.45,
          total_kills_under_25: 2.65
        },
        is_live: false,
        game_type: 'bo4'
      },
      {
        id: 11,
        sport: 'apex',
        sport_name: 'Apex Legends',
        league: 'ALGS',
        home_team: 'TSM',
        away_team: 'NRG',
        start_time: new Date(Date.now() + 7200000).toISOString(), // через 2 часа
        status: 'upcoming',
        odds: {
          home: 1.55,
          away: 2.35,
          first_blood_home: 1.65,
          first_blood_away: 2.15,
          total_kills_over_30: 1.70,
          total_kills_under_30: 2.10
        },
        is_live: false,
        game_type: 'bo3'
      },
      {
        id: 12,
        sport: 'rainbow',
        sport_name: 'Rainbow Six Siege',
        league: 'Six Invitational',
        home_team: 'Team BDS',
        away_team: 'Team Liquid',
        start_time: new Date(Date.now() + 9000000).toISOString(), // через 2.5 часа
        status: 'upcoming',
        odds: {
          home: 1.75,
          away: 2.05,
          first_blood_home: 1.80,
          first_blood_away: 1.95,
          total_rounds_over_12: 1.60,
          total_rounds_under_12: 2.25
        },
        is_live: false,
        game_type: 'bo3'
      }
    ])
  }
}

// Получить live события
export async function getLiveEvents(sport = 'football') {
  try {
    const { data } = await api.get('/sports/live')
    if (data.success) {
      return data.events
    }
    throw new Error(data.message || 'Failed to get live events')
  } catch (error) {
    console.error('API Error (getLiveEvents):', error)

    // Пытаемся получить реальные live данные
    if (config.settings.useRealSportsData) {
      try {
        const realSportsApi = await import('../services/realSportsApi.js')
        const allEvents = await realSportsApi.default.getEvents(sport)
        const liveEvents = allEvents.filter(event => event.is_live)
        if (liveEvents && liveEvents.length > 0) {
          console.log('✅ Using real live sports data from API')
          return mockDelay(liveEvents)
        }
      } catch (realApiError) {
        console.error('Real Live API Error:', realApiError)
      }
    }

    console.log('📊 Using mock live data (fallback mode)')

    // Проверяем локальные live события от админа
    const adminEvents = getAdminEvents()
    const adminLiveEvents = adminEvents.filter(e => e.is_live)
    if (adminLiveEvents.length > 0) {
      console.log('✅ Using admin-created live events')
      return mockDelay(adminLiveEvents)
    }

    return mockDelay([
      {
        id: 19,
        sport: 'football',
        sport_name: 'Футбол',
        league: 'Английская Премьер-лига',
        home_team: 'Ливерпуль',
        away_team: 'Манчестер Сити',
        start_time: new Date(Date.now() - 2700000).toISOString(), // начался 45 мин назад
        status: 'live',
        current_score: { home: 2, away: 1 },
        odds: {
          home: 2.10,
          draw: 3.40,
          away: 3.20,
          next_goal_home: 2.45,
          next_goal_away: 3.10,
          over_1_5: 1.15,
          under_1_5: 5.50
        },
        is_live: true,
        minute: 45,
        venue: 'Энфилд',
        attendance: 54000
      },
      {
        id: 20,
        sport: 'football',
        sport_name: 'Футбол',
        league: 'Ла Лига',
        home_team: 'Барселона',
        away_team: 'Реал Мадрид',
        start_time: new Date(Date.now() - 1500000).toISOString(), // начался 25 мин назад
        status: 'live',
        current_score: { home: 1, away: 1 },
        odds: {
          home: 2.25,
          draw: 3.20,
          away: 3.10,
          next_goal_home: 2.30,
          next_goal_away: 2.90,
          over_1_5: 1.20,
          under_1_5: 4.50
        },
        is_live: true,
        minute: 25,
        venue: 'Камп Ноу',
        attendance: 95000
      },
      {
        id: 21,
        sport: 'basketball',
        sport_name: 'Баскетбол',
        league: 'NBA',
        home_team: 'Бостон Селтикс',
        away_team: 'Голден Стейт Уорриорз',
        start_time: new Date(Date.now() - 1200000).toISOString(), // начался 20 мин назад
        status: 'live',
        current_score: { home: 78, away: 72 },
        odds: {
          home: 1.65,
          away: 2.20,
          next_point_home: 1.45,
          next_point_away: 2.65,
          over_200_5: 1.85,
          under_200_5: 1.95
        },
        is_live: true,
        quarter: 2,
        time_remaining: '8:32',
        arena: 'TD Garden'
      },
      {
        id: 22,
        sport: 'csgo',
        sport_name: 'CS:GO',
        league: 'ESL Pro League Season 20',
        home_team: 'Astralis',
        away_team: 'Natus Vincere',
        start_time: new Date(Date.now() - 1800000).toISOString(), // начался 30 мин назад
        status: 'live',
        current_score: { home: 14, away: 11 },
        odds: {
          home: 1.90,
          away: 1.90,
          next_round_home: 1.85,
          next_round_away: 1.95,
          map_handicap: 1.40,
          pistol_round_home: 2.40,
          pistol_round_away: 1.55
        },
        is_live: true,
        current_map: 'Dust2',
        map_score: '1-0',
        round: 25,
        tournament: 'ESL Pro League'
      },
      {
        id: 23,
        sport: 'dota2',
        sport_name: 'Dota 2',
        league: 'DPC EU Division I',
        home_team: 'Tundra Esports',
        away_team: 'Team Spirit',
        start_time: new Date(Date.now() - 2400000).toISOString(), // начался 40 мин назад
        status: 'live',
        current_score: { home: 18, away: 25 },
        odds: {
          home: 2.40,
          away: 1.55,
          first_blood_home: 2.60,
          first_blood_away: 1.45,
          next_kill_home: 2.10,
          next_kill_away: 1.70,
          total_kills_over_38_5: 1.75,
          total_kills_under_38_5: 2.05
        },
        is_live: true,
        current_map: 'Diretide',
        kills: { home: 32, away: 48 },
        net_worth: { home: 15000, away: 22000 }
      },
      {
        id: 24,
        sport: 'tennis',
        sport_name: 'Теннис',
        league: 'ATP Masters 1000',
        home_team: 'Карлос Алькарас',
        away_team: 'Новак Джокович',
        start_time: new Date(Date.now() - 2100000).toISOString(), // начался 35 мин назад
        status: 'live',
        current_score: { home: { sets: 1, games: 4 }, away: { sets: 1, games: 3 } },
        odds: {
          home: 1.75,
          away: 2.05,
          next_point_home: 1.45,
          next_point_away: 2.65,
          over_24_5_games: 1.80,
          under_24_5_games: 2.00
        },
        is_live: true,
        set_score: '1-1',
        current_game_points: '40-30',
        surface: 'Хард',
        tournament: 'Индиан Уэллс Мастерс'
      },
      {
        id: 14,
        sport: 'apex',
        sport_name: 'Apex Legends',
        league: 'ALGS Championship',
        home_team: 'Alliance',
        away_team: 'Complexity',
        start_time: new Date(Date.now() - 2400000).toISOString(), // начался 40 мин назад
        status: 'live',
        current_score: { home: 3, away: 1 },
        odds: {
          home: 1.35,
          away: 3.10,
          first_blood_home: 1.45,
          first_blood_away: 2.55,
          next_kill_home: 1.25,
          next_kill_away: 3.75
        },
        is_live: true,
        kills: { home: 25, away: 18 },
        current_zone: 'Phase 4'
      },
      {
        id: 15,
        sport: 'pubg',
        sport_name: 'PUBG Mobile',
        league: 'PMPL SEA',
        home_team: 'Team Secret',
        away_team: 'Aqua Esports',
        start_time: new Date(Date.now() - 1500000).toISOString(), // начался 25 мин назад
        status: 'live',
        current_score: { home: 2, away: 1 },
        odds: {
          home: 1.85,
          away: 1.90,
          chicken_dinner_home: 1.95,
          chicken_dinner_away: 1.80,
          next_kill_home: 1.40,
          next_kill_away: 2.80
        },
        is_live: true,
        kills: { home: 15, away: 12 },
        current_map: 'Erangel',
        players_alive: 18
      }
    ])
  }
}

// Сделать ставку
export async function placeBet(eventId, betType, amount, odds) {
  try {
    const { data } = await api.post('/sports/bet', {
      event_id: eventId,
      bet_type: betType,
      amount: Number(amount),
      odds: Number(odds)
    })
    if (data.success) {
      return data
    }
    throw new Error(data.message || 'Failed to place bet')
  } catch (error) {
    console.error('API Error (placeBet):', error)
    // Mock для разработки
    const potentialWin = Number(amount) * Number(odds)
    return mockDelay({
      success: true,
      bet_id: Date.now(),
      amount: Number(amount),
      odds: Number(odds),
      potential_win: potentialWin,
      new_balance: 1000 - Number(amount),
      message: `Ставка принята! Возможный выигрыш: ${potentialWin.toFixed(2)}₽`
    })
  }
}

// Получить активные ставки пользователя
export async function getUserBets() {
  try {
    const { data } = await api.get('/sports/user-bets')
    if (data.success) {
      return data.bets
    }
    throw new Error(data.message || 'Failed to get user bets')
  } catch (error) {
    console.error('API Error (getUserBets):', error)
    return mockDelay([
      {
        id: 1001,
        event_id: 1,
        event_name: 'Манчестер Сити vs Арсенал',
        bet_type: 'home',
        bet_type_name: 'П1',
        amount: 50,
        odds: 2.10,
        potential_win: 105,
        status: 'active',
        created_at: new Date(Date.now() - 3600000).toISOString()
      },
      {
        id: 1002,
        event_id: 4,
        event_name: 'FaZe Clan vs NaVi',
        bet_type: 'home',
        bet_type_name: 'П1',
        amount: 100,
        odds: 1.85,
        potential_win: 185,
        status: 'active',
        created_at: new Date(Date.now() - 1800000).toISOString()
      },
      {
        id: 1003,
        event_id: 5,
        event_name: 'Team Spirit vs Team Liquid',
        bet_type: 'total_kills_over_40',
        bet_type_name: 'Убийств >40',
        amount: 75,
        odds: 1.60,
        potential_win: 120,
        status: 'active',
        created_at: new Date(Date.now() - 900000).toISOString()
      }
    ])
  }
}

// Получить историю ставок
export async function getBetHistory(limit = 25) {
  try {
    const { data } = await api.get('/sports/bet-history', { params: { limit } })
    if (data.success) {
      return data.history
    }
    throw new Error(data.message || 'Failed to get bet history')
  } catch (error) {
    console.error('API Error (getBetHistory):', error)
    const items = Array.from({ length: 15 }).map((_, i) => {
      const isWin = Math.random() > 0.5
      const amount = Math.floor(Math.random() * 200) + 10
      const odds = +(Math.random() * 3 + 1).toFixed(2)
      const eventTypes = [
        { name: 'Ман Сити vs Арсенал', type: 'traditional' },
        { name: 'Лейкерс vs Уорриорз', type: 'traditional' },
        { name: 'Барса vs Реал', type: 'traditional' },
        { name: 'FaZe Clan vs NaVi', type: 'esports' },
        { name: 'Team Spirit vs Team Liquid', type: 'esports' },
        { name: 'T1 vs Gen.G', type: 'esports' },
        { name: 'Cloud9 vs Astralis', type: 'esports' }
      ]

      const event = eventTypes[Math.floor(Math.random() * eventTypes.length)]
      const betTypes = event.type === 'esports'
        ? ['П1', 'П2', 'Гандикап карт', 'Тотал карт', 'First Blood', 'Убийств >40']
        : ['П1', 'П2', 'Ничья', 'Тотал > 2.5', 'Тотал < 2.5']

      return {
        id: 2000 + i,
        event_name: event.name,
        bet_type_name: betTypes[Math.floor(Math.random() * betTypes.length)],
        amount: amount,
        odds: odds,
        result: isWin ? 'win' : 'lose',
        profit: isWin ? (amount * odds - amount) : -amount,
        created_at: new Date(Date.now() - i * 86400000).toISOString()
      }
    })
    return mockDelay(items)
  }
}

// Получить статистику ставок пользователя
export async function getBetStats() {
  try {
    const { data } = await api.get('/sports/bet-stats')
    if (data.success) {
      return data.stats
    }
    throw new Error(data.message || 'Failed to get bet stats')
  } catch (error) {
    console.error('API Error (getBetStats):', error)
    return mockDelay({
      total_bets: 67,
      win_rate: 0.58,
      total_profit: 2150.75,
      biggest_win: 750,
      biggest_lose: -150,
      favorite_sport: 'CS:GO',
      monthly_stats: [
        { month: 'Янв', profit: 250 },
        { month: 'Фев', profit: -75 },
        { month: 'Мар', profit: 450 },
        { month: 'Апр', profit: 350 },
        { month: 'Май', profit: 175 }
      ]
    })
  }
}