// Админ сервис для управления платформой
import config from '../config.js'

class AdminService {
  constructor() {
    this.baseURL = config.apiUrls.admin;
    this.token = localStorage.getItem('admin_token');
  }

  // Аутентификация администратора
  async login(password) {
    try {
      const response = await fetch(`${this.baseURL}/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ password })
      });

      if (!response.ok) {
        throw new Error('Неверный пароль');
      }

      const data = await response.json();
      this.token = data.token;
      localStorage.setItem('admin_token', this.token);
      localStorage.setItem('admin_auth', 'true');

      return { success: true, token: data.token };
    } catch (error) {
      console.error('Admin login error:', error);
      return { success: false, error: error.message };
    }
  }

  // Проверка прав администратора
  async checkAuth() {
    if (!this.token) return false;

    try {
      const response = await fetch(`${this.baseURL}/verify`, {
        headers: {
          'Authorization': `Bearer ${this.token}`
        }
      });

      return response.ok;
    } catch (error) {
      return false;
    }
  }

  // Управление событиями
  async createEvent(eventData) {
    return this.makeRequest('/events', 'POST', eventData);
  }

  async updateEvent(eventId, eventData) {
    return this.makeRequest(`/events/${eventId}`, 'PUT', eventData);
  }

  async deleteEvent(eventId) {
    return this.makeRequest(`/events/${eventId}`, 'DELETE');
  }

  async getEvents(filters = {}) {
    const queryString = new URLSearchParams(filters).toString();
    return this.makeRequest(`/events?${queryString}`, 'GET');
  }

  // Управление коэффициентами
  async updateOdds(eventId, oddsData) {
    return this.makeRequest(`/events/${eventId}/odds`, 'PUT', oddsData);
  }

  async getOddsHistory(eventId) {
    return this.makeRequest(`/events/${eventId}/odds/history`, 'GET');
  }

  // Управление пользователями
  async getUsers(filters = {}) {
    const queryString = new URLSearchParams(filters).toString();
    return this.makeRequest(`/users?${queryString}`, 'GET');
  }

  async updateUser(userId, userData) {
    return this.makeRequest(`/users/${userId}`, 'PUT', userData);
  }

  async blockUser(userId, reason = '') {
    return this.makeRequest(`/users/${userId}/block`, 'POST', { reason });
  }

  async unblockUser(userId) {
    return this.makeRequest(`/users/${userId}/unblock`, 'POST');
  }

  async updateUserBalance(userId, amount, reason = '') {
    return this.makeRequest(`/users/${userId}/balance`, 'PUT', { amount, reason });
  }

  // Управление ставками
  async getBets(filters = {}) {
    const queryString = new URLSearchParams(filters).toString();
    return this.makeRequest(`/bets?${queryString}`, 'GET');
  }

  async settleBet(betId, result, adminNote = '') {
    return this.makeRequest(`/bets/${betId}/settle`, 'POST', { result, adminNote });
  }

  async deleteBet(betId, reason = '') {
    return this.makeRequest(`/bets/${betId}`, 'DELETE', { reason });
  }

  // Статистика
  async getStatistics(period = 'all') {
    return this.makeRequest(`/statistics?period=${period}`, 'GET');
  }

  async getDashboardStats() {
    return this.makeRequest('/dashboard/stats', 'GET');
  }

  // Система уведомлений
  async sendNotification(userId, notification) {
    if (userId === 'all') {
      return this.makeRequest('/notifications/broadcast', 'POST', notification);
    }
    return this.makeRequest(`/notifications/${userId}`, 'POST', notification);
  }

  // Настройки платформы
  async getSettings() {
    return this.makeRequest('/settings', 'GET');
  }

  async updateSettings(settings) {
    return this.makeRequest('/settings', 'PUT', settings);
  }

  // Логи действий
  async getActionLogs(filters = {}) {
    const queryString = new URLSearchParams(filters).toString();
    return this.makeRequest(`/logs?${queryString}`, 'GET');
  }

  // Вспомогательный метод для запросов
  async makeRequest(endpoint, method = 'GET', data = null) {
    if (!this.token && endpoint !== '/login') {
      throw new Error('Не авторизован');
    }

    const config = {
      method,
      headers: {
        'Content-Type': 'application/json'
      }
    };

    if (this.token) {
      config.headers['Authorization'] = `Bearer ${this.token}`;
    }

    if (data && (method === 'POST' || method === 'PUT')) {
      config.body = JSON.stringify(data);
    }

    try {
      const response = await fetch(`${this.baseURL}${endpoint}`, config);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.message || `HTTP ${response.status}`);
      }

      const result = await response.json();
      return { success: true, data: result };
    } catch (error) {
      console.error(`Admin API Error (${endpoint}):`, error);
      return { success: false, error: error.message };
    }
  }

  // Выход из системы
  logout() {
    this.token = null;
    localStorage.removeItem('admin_token');
    localStorage.removeItem('admin_auth');
    localStorage.removeItem('admin_login_time');
  }

  // Проверка сессии
  async checkSession() {
    const loginTime = localStorage.getItem('admin_login_time');
    if (!loginTime) return false;

    const hoursAgo = (Date.now() - new Date(loginTime)) / (1000 * 60 * 60);
    if (hoursAgo > 24) { // сессия истекает через 24 часа
      this.logout();
      return false;
    }

    return this.checkAuth();
  }
}

// Экспорт синглтона
export default new AdminService();
