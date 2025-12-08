const express = require('express');
const cors = require('cors');
const WebSocket = require('ws');
const http = require('http');

const app = express();
const port = 3001;

// Middleware
app.use(cors());
app.use(express.json());

// Mock данные для спортивных событий
const mockEvents = [
  {
    id: 'event_001',
    sport: 'soccer',
    sport_name: 'Футбол',
    league: 'Премьер-лига',
    home_team: 'Манчестер Сити',
    away_team: 'Ливерпуль',
    start_time: new Date(Date.now() + 2 * 60 * 60 * 1000).toISOString(),
    status: 'upcoming',
    is_live: false,
    odds: { home: 1.85, draw: 3.40, away: 4.20 },
    venue: 'Этихад Стэдиум',
    country: 'Англия',
    created_at: new Date().toISOString()
  },
  {
    id: 'event_002',
    sport: 'soccer',
    sport_name: 'Футбол',
    league: 'Ла Лига',
    home_team: 'Барселона',
    away_team: 'Реал Мадрид',
    start_time: new Date(Date.now() + 4 * 60 * 60 * 1000).toISOString(),
    status: 'upcoming',
    is_live: false,
    odds: { home: 2.10, draw: 3.60, away: 3.30 },
    venue: 'Камп Ноу',
    country: 'Испания',
    created_at: new Date().toISOString()
  },
  {
    id: 'event_003',
    sport: 'csgo',
    sport_name: 'CS:GO',
    league: 'ESL Pro League',
    home_team: 'FaZe Clan',
    away_team: 'NaVi',
    start_time: new Date(Date.now() + 1 * 60 * 60 * 1000).toISOString(),
    status: 'upcoming',
    is_live: false,
    odds: { home: 1.65, draw: 1.00, away: 2.40 },
    venue: 'Online',
    country: 'Международный',
    created_at: new Date().toISOString()
  },
  {
    id: 'event_004',
    sport: 'basketball',
    sport_name: 'Баскетбол',
    league: 'NBA',
    home_team: 'Лейкерс',
    away_team: 'Уорриорз',
    start_time: new Date(Date.now() + 3 * 60 * 60 * 1000).toISOString(),
    status: 'upcoming',
    is_live: false,
    odds: { home: 1.95, draw: 1.00, away: 1.85 },
    venue: 'Crypto.com Arena',
    country: 'США',
    created_at: new Date().toISOString()
  },
  {
    id: 'event_005',
    sport: 'tennis',
    sport_name: 'Теннис',
    league: 'ATP',
    home_team: 'Новак Джокович',
    away_team: 'Рафаэль Надаль',
    start_time: new Date(Date.now() + 5 * 60 * 60 * 1000).toISOString(),
    status: 'upcoming',
    is_live: false,
    odds: { home: 1.45, draw: 1.00, away: 2.80 },
    venue: 'Уимблдон',
    country: 'Великобритания',
    created_at: new Date().toISOString()
  }
];

// API endpoints
app.get('/api/sports/events', (req, res) => {
  res.json({
    success: true,
    data: mockEvents,
    total: mockEvents.length
  });
});

app.get('/api/sports/live', (req, res) => {
  const liveEvents = mockEvents.filter(event => event.is_live);
  res.json({
    success: true,
    data: liveEvents,
    total: liveEvents.length
  });
});

app.get('/api/sports/user-bets', (req, res) => {
  res.json({
    success: true,
    data: [],
    total: 0
  });
});

app.get('/api/sports/bet-history', (req, res) => {
  res.json({
    success: true,
    data: [],
    total: 0
  });
});

app.get('/api/sports/bet-stats', (req, res) => {
  res.json({
    success: true,
    data: {
      total_bets: 0,
      wins: 0,
      losses: 0,
      win_rate: 0,
      profit: 0
    }
  });
});

// CORS Proxy для внешних API
app.get('/api/proxy/*', async (req, res) => {
  try {
    const targetUrl = req.params[0] + (req.url.split('?')[1] ? '?' + req.url.split('?')[1] : '');

    const axios = require('axios');
    const response = await axios.get(targetUrl, {
      timeout: 10000,
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
      }
    });

    res.json(response.data);
  } catch (error) {
    console.error('CORS Proxy Error:', error.message);
    res.status(500).json({
      success: false,
      error: 'Failed to proxy request',
      details: error.message
    });
  }
});

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({
    status: 'ok',
    timestamp: new Date().toISOString(),
    services: {
      api: 'running',
      websocket: 'running',
      cors_proxy: 'running'
    }
  });
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error('API Error:', err);
  res.status(500).json({
    success: false,
    error: 'Internal server error'
  });
});

// Create HTTP server
const server = http.createServer(app);

// WebSocket server
const wss = new WebSocket.Server({ server, path: '/ws' });

wss.on('connection', (ws, req) => {
  console.log('Client connected to WebSocket');

  // Send welcome message
  ws.send(JSON.stringify({
    type: 'welcome',
    message: 'Connected to betting server',
    timestamp: new Date().toISOString()
  }));

  // Simulate live updates every 30 seconds
  const interval = setInterval(() => {
    if (ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({
        type: 'live_update',
        data: mockEvents[Math.floor(Math.random() * mockEvents.length)],
        timestamp: new Date().toISOString()
      }));
    }
  }, 30000);

  ws.on('message', (message) => {
    try {
      const data = JSON.parse(message.toString());
      console.log('Received:', data);

      // Echo back
      ws.send(JSON.stringify({
        type: 'echo',
        data: data,
        timestamp: new Date().toISOString()
      }));
    } catch (error) {
      console.error('WebSocket message error:', error);
    }
  });

  ws.on('close', () => {
    console.log('Client disconnected from WebSocket');
    clearInterval(interval);
  });

  ws.on('error', (error) => {
    console.error('WebSocket error:', error);
    clearInterval(interval);
  });
});

// Start server
server.listen(port, () => {
  console.log(`🚀 API Server running on http://localhost:${port}`);
  console.log(`📡 WebSocket server running on ws://localhost:${port}/ws`);
  console.log('📊 Available endpoints:');
  console.log('  GET /api/health');
  console.log('  GET /api/sports/events');
  console.log('  GET /api/sports/live');
  console.log('  GET /api/sports/user-bets');
  console.log('  GET /api/sports/bet-history');
  console.log('  GET /api/sports/bet-stats');
});

// Graceful shutdown
process.on('SIGINT', () => {
  console.log('\n🛑 Shutting down server...');
  server.close(() => {
    console.log('✅ Server closed');
    process.exit(0);
  });
});

module.exports = app;
