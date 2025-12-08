// Локальная база данных для событий (IndexedDB)
class EventDatabase {
  constructor() {
    this.dbName = 'SportsBettingDB';
    this.version = 1;
    this.db = null;
    this.initPromise = this.init();
  }

  async init() {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open(this.dbName, this.version);

      request.onerror = () => {
        console.error('Error opening IndexedDB:', request.error);
        reject(request.error);
      };

      request.onsuccess = (event) => {
        this.db = event.target.result;
        console.log('IndexedDB initialized successfully');
        resolve(this.db);
      };

      request.onupgradeneeded = (event) => {
        const db = event.target.result;

        // Создание хранилищ
        if (!db.objectStoreNames.contains('events')) {
          const eventsStore = db.createObjectStore('events', { keyPath: 'id' });
          eventsStore.createIndex('sport', 'sport', { unique: false });
          eventsStore.createIndex('status', 'status', { unique: false });
          eventsStore.createIndex('start_time', 'start_time', { unique: false });
          eventsStore.createIndex('is_live', 'is_live', { unique: false });
        }

        if (!db.objectStoreNames.contains('bets')) {
          const betsStore = db.createObjectStore('bets', { keyPath: 'id' });
          betsStore.createIndex('user_id', 'user_id', { unique: false });
          betsStore.createIndex('event_id', 'event_id', { unique: false });
          betsStore.createIndex('status', 'status', { unique: false });
          betsStore.createIndex('created_at', 'created_at', { unique: false });
        }

        if (!db.objectStoreNames.contains('users')) {
          const usersStore = db.createObjectStore('users', { keyPath: 'id' });
          usersStore.createIndex('email', 'email', { unique: true });
          usersStore.createIndex('status', 'status', { unique: false });
        }

        if (!db.objectStoreNames.contains('predictions')) {
          const predictionsStore = db.createObjectStore('predictions', { keyPath: 'id' });
          predictionsStore.createIndex('event_id', 'event_id', { unique: false });
          predictionsStore.createIndex('user_id', 'user_id', { unique: false });
          predictionsStore.createIndex('created_at', 'created_at', { unique: false });
        }

        if (!db.objectStoreNames.contains('settings')) {
          db.createObjectStore('settings', { keyPath: 'key' });
        }

        // Инициализация начальными данными
        this.initializeDefaultData(db);
      };
    });
  }

  async initializeDefaultData(db) {
    // Добавление начальных событий
    const eventsTransaction = db.transaction(['events'], 'readwrite');
    const eventsStore = eventsTransaction.objectStore('events');

    const defaultEvents = [
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
        home_team: 'NaVi',
        away_team: 'FaZe Clan',
        start_time: new Date(Date.now() + 1 * 60 * 60 * 1000).toISOString(),
        status: 'live',
        is_live: true,
        odds: { home: 1.75, away: 2.15 },
        venue: 'Online',
        country: 'Международный',
        score: { home: 12, away: 8 },
        map: 'Dust2',
        round: 20,
        created_at: new Date().toISOString()
      }
    ];

    defaultEvents.forEach(event => {
      eventsStore.add(event);
    });

    // Добавление начальных пользователей
    const usersTransaction = db.transaction(['users'], 'readwrite');
    const usersStore = usersTransaction.objectStore('users');

    const defaultUsers = [
      {
        id: 'user_001',
        name: 'Иван Петров',
        email: 'ivan@example.com',
        balance: 1500.00,
        status: 'active',
        registration_date: new Date().toISOString(),
        total_bets: 25,
        winning_bets: 15,
        total_profit: 350.50
      },
      {
        id: 'user_002',
        name: 'Мария Иванова',
        email: 'maria@example.com',
        balance: 3200.50,
        status: 'active',
        registration_date: new Date().toISOString(),
        total_bets: 40,
        winning_bets: 28,
        total_profit: 850.75
      }
    ];

    defaultUsers.forEach(user => {
      usersStore.add(user);
    });
  }

  // Методы для работы с событиями
  async getEvents(filters = {}) {
    await this.initPromise;

    return new Promise((resolve, reject) => {
      const transaction = this.db.transaction(['events'], 'readonly');
      const store = transaction.objectStore('events');
      const request = store.getAll();

      request.onsuccess = () => {
        let events = request.result;

        // Применение фильтров
        if (filters.sport) {
          events = events.filter(event => event.sport === filters.sport);
        }

        if (filters.status) {
          events = events.filter(event => event.status === filters.status);
        }

        if (filters.is_live !== undefined) {
          events = events.filter(event => event.is_live === filters.is_live);
        }

        if (filters.date) {
          const filterDate = new Date(filters.date).toISOString().split('T')[0];
          events = events.filter(event => {
            const eventDate = new Date(event.start_time).toISOString().split('T')[0];
            return eventDate === filterDate;
          });
        }

        resolve(events);
      };

      request.onerror = () => reject(request.error);
    });
  }

  async getEvent(eventId) {
    await this.initPromise;

    return new Promise((resolve, reject) => {
      const transaction = this.db.transaction(['events'], 'readonly');
      const store = transaction.objectStore('events');
      const request = store.get(eventId);

      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });
  }

  async createEvent(eventData) {
    await this.initPromise;

    const event = {
      ...eventData,
      id: eventData.id || `event_${Date.now()}`,
      created_at: new Date().toISOString(),
      status: eventData.status || 'upcoming',
      is_live: eventData.is_live || false
    };

    return new Promise((resolve, reject) => {
      const transaction = this.db.transaction(['events'], 'readwrite');
      const store = transaction.objectStore('events');
      const request = store.add(event);

      request.onsuccess = () => resolve(event);
      request.onerror = () => reject(request.error);
    });
  }

  async updateEvent(eventId, updates) {
    await this.initPromise;

    return new Promise((resolve, reject) => {
      const transaction = this.db.transaction(['events'], 'readwrite');
      const store = transaction.objectStore('events');

      const getRequest = store.get(eventId);

      getRequest.onsuccess = () => {
        const event = getRequest.result;
        if (!event) {
          reject(new Error('Event not found'));
          return;
        }

        const updatedEvent = { ...event, ...updates, updated_at: new Date().toISOString() };
        const putRequest = store.put(updatedEvent);

        putRequest.onsuccess = () => resolve(updatedEvent);
        putRequest.onerror = () => reject(putRequest.error);
      };

      getRequest.onerror = () => reject(getRequest.error);
    });
  }

  async deleteEvent(eventId) {
    await this.initPromise;

    return new Promise((resolve, reject) => {
      const transaction = this.db.transaction(['events'], 'readwrite');
      const store = transaction.objectStore('events');
      const request = store.delete(eventId);

      request.onsuccess = () => resolve(true);
      request.onerror = () => reject(request.error);
    });
  }

  // Методы для работы со ставками
  async getBets(filters = {}) {
    await this.initPromise;

    return new Promise((resolve, reject) => {
      const transaction = this.db.transaction(['bets'], 'readonly');
      const store = transaction.objectStore('bets');
      const request = store.getAll();

      request.onsuccess = () => {
        let bets = request.result;

        // Применение фильтров
        if (filters.user_id) {
          bets = bets.filter(bet => bet.user_id === filters.user_id);
        }

        if (filters.event_id) {
          bets = bets.filter(bet => bet.event_id === filters.event_id);
        }

        if (filters.status) {
          bets = bets.filter(bet => bet.status === filters.status);
        }

        // Сортировка по дате (новые сначала)
        bets.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));

        resolve(bets);
      };

      request.onerror = () => reject(request.error);
    });
  }

  async createBet(betData) {
    await this.initPromise;

    const bet = {
      ...betData,
      id: betData.id || `bet_${Date.now()}`,
      created_at: new Date().toISOString(),
      status: betData.status || 'pending'
    };

    return new Promise((resolve, reject) => {
      const transaction = this.db.transaction(['bets'], 'readwrite');
      const store = transaction.objectStore('bets');
      const request = store.add(bet);

      request.onsuccess = () => resolve(bet);
      request.onerror = () => reject(request.error);
    });
  }

  async updateBet(betId, updates) {
    await this.initPromise;

    return new Promise((resolve, reject) => {
      const transaction = this.db.transaction(['bets'], 'readwrite');
      const store = transaction.objectStore('bets');

      const getRequest = store.get(betId);

      getRequest.onsuccess = () => {
        const bet = getRequest.result;
        if (!bet) {
          reject(new Error('Bet not found'));
          return;
        }

        const updatedBet = { ...bet, ...updates, updated_at: new Date().toISOString() };
        const putRequest = store.put(updatedBet);

        putRequest.onsuccess = () => resolve(updatedBet);
        putRequest.onerror = () => reject(putRequest.error);
      };

      getRequest.onerror = () => reject(getRequest.error);
    });
  }

  // Методы для работы с пользователями
  async getUsers(filters = {}) {
    await this.initPromise;

    return new Promise((resolve, reject) => {
      const transaction = this.db.transaction(['users'], 'readonly');
      const store = transaction.objectStore('users');
      const request = store.getAll();

      request.onsuccess = () => {
        let users = request.result;

        // Применение фильтров
        if (filters.status) {
          users = users.filter(user => user.status === filters.status);
        }

        if (filters.search) {
          const searchTerm = filters.search.toLowerCase();
          users = users.filter(user =>
            user.name.toLowerCase().includes(searchTerm) ||
            user.email.toLowerCase().includes(searchTerm)
          );
        }

        resolve(users);
      };

      request.onerror = () => reject(request.error);
    });
  }

  async getUser(userId) {
    await this.initPromise;

    return new Promise((resolve, reject) => {
      const transaction = this.db.transaction(['users'], 'readonly');
      const store = transaction.objectStore('users');
      const request = store.get(userId);

      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });
  }

  async updateUser(userId, updates) {
    await this.initPromise;

    return new Promise((resolve, reject) => {
      const transaction = this.db.transaction(['users'], 'readwrite');
      const store = transaction.objectStore('users');

      const getRequest = store.get(userId);

      getRequest.onsuccess = () => {
        const user = getRequest.result;
        if (!user) {
          reject(new Error('User not found'));
          return;
        }

        const updatedUser = { ...user, ...updates, updated_at: new Date().toISOString() };
        const putRequest = store.put(updatedUser);

        putRequest.onsuccess = () => resolve(updatedUser);
        putRequest.onerror = () => reject(putRequest.error);
      };

      getRequest.onerror = () => reject(getRequest.error);
    });
  }

  // Методы для работы с прогнозами
  async savePrediction(prediction) {
    await this.initPromise;

    const predictionData = {
      ...prediction,
      id: prediction.id || `pred_${Date.now()}`,
      created_at: new Date().toISOString()
    };

    return new Promise((resolve, reject) => {
      const transaction = this.db.transaction(['predictions'], 'readwrite');
      const store = transaction.objectStore('predictions');
      const request = store.put(predictionData); // Используем put вместо add для обновления существующих записей

      request.onsuccess = () => resolve(predictionData);
      request.onerror = () => reject(request.error);
    });
  }

  async getPredictions(filters = {}) {
    await this.initPromise;

    return new Promise((resolve, reject) => {
      const transaction = this.db.transaction(['predictions'], 'readonly');
      const store = transaction.objectStore('predictions');
      const request = store.getAll();

      request.onsuccess = () => {
        let predictions = request.result;

        // Применение фильтров
        if (filters.event_id) {
          predictions = predictions.filter(p => p.eventId === filters.event_id);
        }

        if (filters.user_id) {
          predictions = predictions.filter(p => p.user_id === filters.user_id);
        }

        resolve(predictions);
      };

      request.onerror = () => reject(request.error);
    });
  }

  // Методы для работы с настройками
  async getSetting(key) {
    await this.initPromise;

    return new Promise((resolve, reject) => {
      const transaction = this.db.transaction(['settings'], 'readonly');
      const store = transaction.objectStore('settings');
      const request = store.get(key);

      request.onsuccess = () => resolve(request.result?.value);
      request.onerror = () => reject(request.error);
    });
  }

  async setSetting(key, value) {
    await this.initPromise;

    return new Promise((resolve, reject) => {
      const transaction = this.db.transaction(['settings'], 'readwrite');
      const store = transaction.objectStore('settings');
      const request = store.put({ key, value, updated_at: new Date().toISOString() });

      request.onsuccess = () => resolve(true);
      request.onerror = () => reject(request.error);
    });
  }

  // Очистка базы данных
  async clearAll() {
    await this.initPromise;

    const stores = ['events', 'bets', 'users', 'predictions', 'settings'];

    for (const storeName of stores) {
      await new Promise((resolve, reject) => {
        const transaction = this.db.transaction([storeName], 'readwrite');
        const store = transaction.objectStore(storeName);
        const request = store.clear();

        request.onsuccess = () => resolve();
        request.onerror = () => reject(request.error);
      });
    }
  }

  // Экспорт данных
  async exportData() {
    const [events, bets, users, predictions, settings] = await Promise.all([
      this.getEvents(),
      this.getBets(),
      this.getUsers(),
      this.getPredictions(),
      this.getAllSettings()
    ]);

    return {
      events,
      bets,
      users,
      predictions,
      settings,
      exported_at: new Date().toISOString(),
      version: this.version
    };
  }

  async getAllSettings() {
    await this.initPromise;

    return new Promise((resolve, reject) => {
      const transaction = this.db.transaction(['settings'], 'readonly');
      const store = transaction.objectStore('settings');
      const request = store.getAll();

      request.onsuccess = () => {
        const settings = {};
        request.result.forEach(setting => {
          settings[setting.key] = setting.value;
        });
        resolve(settings);
      };
      request.onerror = () => reject(request.error);
    });
  }
}

// Экспорт синглтона
export default new EventDatabase();
