<template>
  <div class="admin-event-manager">
    <div class="manager-header">
      <h2>📅 Управление событиями</h2>
      <button @click="createEvent" class="create-btn">
        <i class="fas fa-plus"></i>
        Создать событие
      </button>
    </div>

    <!-- Events List -->
    <div class="events-list">
      <div
        v-for="event in events"
        :key="event.id"
        :class="['event-card', event.importance, { live: event.is_live }]"
      >
        <div class="event-header">
          <div class="event-info">
            <h3>{{ event.home_team }} vs {{ event.away_team }}</h3>
            <p>{{ event.league }} • {{ formatTime(event.start_time) }}</p>
          </div>
          <div class="event-badges">
            <span v-if="event.is_live" class="badge live">🔴 LIVE</span>
            <span v-if="event.importance === 'high'" class="badge vip">⭐ VIP</span>
          </div>
        </div>

        <div class="event-odds">
          <div class="odds-grid">
            <div class="odd-item">
              <span class="odd-label">П1</span>
              <span class="odd-value">{{ event.odds?.home || 2.10 }}</span>
            </div>
            <div v-if="event.sport === 'football'" class="odd-item">
              <span class="odd-label">X</span>
              <span class="odd-value">{{ event.odds?.draw || 3.40 }}</span>
            </div>
            <div class="odd-item">
              <span class="odd-label">П2</span>
              <span class="odd-value">{{ event.odds?.away || 3.20 }}</span>
            </div>
          </div>
        </div>

        <div class="event-actions">
          <button @click="editEvent(event)" class="btn-edit">
            <i class="fas fa-edit"></i>
            Редактировать
          </button>
          <button @click="editOdds(event)" class="btn-odds">
            <i class="fas fa-coins"></i>
            Коэффициенты
          </button>
          <button @click="toggleLiveStatus(event)" :class="['btn-live', { active: event.is_live }]">
            <i class="fas fa-play"></i>
            {{ event.is_live ? 'Остановить' : 'Запустить Live' }}
          </button>
          <button @click="deleteEvent(event)" class="btn-delete">
            <i class="fas fa-trash"></i>
            Удалить
          </button>
        </div>
      </div>
    </div>

    <!-- Create/Edit Event Modal -->
    <div v-if="showModal" class="modal-overlay">
      <div class="modal">
        <div class="modal-header">
          <h3>{{ editingEvent ? 'Редактировать событие' : 'Создать событие' }}</h3>
          <button @click="closeModal" class="close-btn">
            <i class="fas fa-times"></i>
          </button>
        </div>

        <form @submit.prevent="saveEvent" class="event-form">
          <div class="form-row">
            <div class="form-group">
              <label>Вид спорта</label>
              <select v-model="eventForm.sport" required>
                <option value="football">⚽ Футбол</option>
                <option value="basketball">🏀 Баскетбол</option>
                <option value="tennis">🎾 Теннис</option>
                <option value="hockey">🏒 Хоккей</option>
                <option value="csgo">🎮 CS:GO</option>
                <option value="dota2">🎯 Dota 2</option>
              </select>
            </div>
            <div class="form-group">
              <label>Лига/Турнир</label>
              <input v-model="eventForm.league" type="text" required>
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Команда 1</label>
              <input v-model="eventForm.home_team" type="text" required>
            </div>
            <div class="form-group">
              <label>Команда 2</label>
              <input v-model="eventForm.away_team" type="text" required>
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Дата и время</label>
              <input v-model="eventForm.start_time" type="datetime-local" required>
            </div>
            <div class="form-group">
              <label>Стадион</label>
              <input v-model="eventForm.venue" type="text">
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Важность</label>
              <select v-model="eventForm.importance">
                <option value="low">Низкая</option>
                <option value="medium">Средняя</option>
                <option value="high">Высокая</option>
              </select>
            </div>
            <div class="form-group">
              <label>Статус</label>
              <select v-model="eventForm.status">
                <option value="upcoming">Предстоит</option>
                <option value="live">Live</option>
                <option value="finished">Завершен</option>
              </select>
            </div>
          </div>

          <div class="form-actions">
            <button type="button" @click="closeModal" class="btn-secondary">Отмена</button>
            <button type="submit" class="btn-primary">
              {{ editingEvent ? 'Сохранить' : 'Создать' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Odds Editor Modal -->
    <div v-if="showOddsModal" class="modal-overlay">
      <div class="modal">
        <div class="modal-header">
          <h3>Коэффициенты: {{ selectedEvent?.home_team }} vs {{ selectedEvent?.away_team }}</h3>
          <button @click="closeOddsModal" class="close-btn">
            <i class="fas fa-times"></i>
          </button>
        </div>

        <div class="odds-editor">
          <div class="odds-grid">
            <div class="odd-row">
              <label>Победа 1-й команды</label>
              <input v-model="selectedEvent.odds.home" type="number" step="0.01">
            </div>
            <div v-if="selectedEvent?.sport === 'football'" class="odd-row">
              <label>Ничья</label>
              <input v-model="selectedEvent.odds.draw" type="number" step="0.01">
            </div>
            <div class="odd-row">
              <label>Победа 2-й команды</label>
              <input v-model="selectedEvent.odds.away" type="number" step="0.01">
            </div>
            <div class="odd-row">
              <label>Тотал больше 2.5</label>
              <input v-model="selectedEvent.odds.over_2_5" type="number" step="0.01">
            </div>
            <div class="odd-row">
              <label>Тотал меньше 2.5</label>
              <input v-model="selectedEvent.odds.under_2_5" type="number" step="0.01">
            </div>
            <div v-if="selectedEvent?.sport === 'football'" class="odd-row">
              <label>Обе забьют - Да</label>
              <input v-model="selectedEvent.odds.btts_yes" type="number" step="0.01">
            </div>
            <div v-if="selectedEvent?.sport === 'football'" class="odd-row">
              <label>Обе забьют - Нет</label>
              <input v-model="selectedEvent.odds.btts_no" type="number" step="0.01">
            </div>
          </div>

          <div class="odds-actions">
            <button @click="resetOdds" class="btn-secondary">Сбросить</button>
            <button @click="saveOdds" class="btn-primary">Сохранить</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AdminEventManager',
  data() {
    return {
      events: [],
      showModal: false,
      showOddsModal: false,
      editingEvent: null,
      selectedEvent: null,
      eventForm: {
        sport: 'football',
        league: '',
        home_team: '',
        away_team: '',
        start_time: '',
        venue: '',
        importance: 'medium',
        status: 'upcoming'
      }
    }
  },
  methods: {
    loadEvents() {
      const savedEvents = localStorage.getItem('admin_events')
      if (savedEvents) {
        this.events = JSON.parse(savedEvents)
      }
    },

    saveEvents() {
      localStorage.setItem('admin_events', JSON.stringify(this.events))
      this.$emit('events-updated', this.events)
    },

    createEvent() {
      this.editingEvent = null
      this.eventForm = {
        sport: 'football',
        league: '',
        home_team: '',
        away_team: '',
        start_time: '',
        venue: '',
        importance: 'medium',
        status: 'upcoming'
      }
      this.showModal = true
    },

    editEvent(event) {
      this.editingEvent = event
      this.eventForm = { ...event }
      this.showModal = true
    },

    async saveEvent() {
      try {
        const eventData = {
          ...this.eventForm,
          id: this.editingEvent ? this.editingEvent.id : Date.now(),
          odds: this.generateDefaultOdds(this.eventForm.sport),
          is_live: this.eventForm.status === 'live',
          current_score: { home: 0, away: 0 },
          sport_name: this.getSportDisplayName(this.eventForm.sport)
        }

        if (this.editingEvent) {
          const index = this.events.findIndex(e => e.id === this.editingEvent.id)
          if (index !== -1) {
            this.events[index] = eventData
          }
        } else {
          this.events.push(eventData)
        }

        this.saveEvents()
        this.closeModal()

      } catch (error) {
        console.error('Error saving event:', error)
        alert('Ошибка при сохранении события')
      }
    },

    deleteEvent(event) {
      if (confirm(`Удалить событие "${event.home_team} vs ${event.away_team}"?`)) {
        this.events = this.events.filter(e => e.id !== event.id)
        this.saveEvents()
      }
    },

    toggleLiveStatus(event) {
      event.is_live = !event.is_live
      event.status = event.is_live ? 'live' : 'upcoming'
      this.saveEvents()
    },

    editOdds(event) {
      this.selectedEvent = event
      this.showOddsModal = true
    },

    saveOdds() {
      this.saveEvents()
      this.closeOddsModal()
    },

    resetOdds() {
      if (this.selectedEvent) {
        this.selectedEvent.odds = this.generateDefaultOdds(this.selectedEvent.sport)
      }
    },

    generateDefaultOdds(sport) {
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
    },

    getSportDisplayName(sport) {
      const names = {
        football: 'Футбол',
        basketball: 'Баскетбол',
        tennis: 'Теннис',
        hockey: 'Хоккей',
        csgo: 'CS:GO',
        dota2: 'Dota 2'
      }
      return names[sport] || sport
    },

    formatTime(dateString) {
      const date = new Date(dateString)
      return date.toLocaleString('ru-RU', {
        day: '2-digit',
        month: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      })
    },

    closeModal() {
      this.showModal = false
      this.editingEvent = null
    },

    closeOddsModal() {
      this.showOddsModal = false
      this.selectedEvent = null
    }
  },

  mounted() {
    this.loadEvents()
  }
}
</script>

<style scoped>
.admin-event-manager {
  padding: 30px;
  max-width: 1200px;
  margin: 0 auto;
}

.manager-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.manager-header h2 {
  margin: 0;
  font-size: 2rem;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.create-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
}

.create-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
}

/* Events List */
.events-list {
  display: grid;
  gap: 20px;
}

.event-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 15px;
  padding: 20px;
  transition: all 0.3s ease;
}

.event-card:hover {
  background: rgba(255, 255, 255, 0.08);
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.event-card.live {
  border-color: rgba(255, 71, 87, 0.5);
  box-shadow: 0 0 20px rgba(255, 71, 87, 0.3);
  animation: livePulse 2s infinite;
}

.event-card.high {
  border-left: 4px solid #ffd700;
}

@keyframes livePulse {
  0%, 100% { box-shadow: 0 0 20px rgba(255, 71, 87, 0.3); }
  50% { box-shadow: 0 0 30px rgba(255, 71, 87, 0.6); }
}

/* Event Header */
.event-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 15px;
}

.event-info h3 {
  margin: 0 0 8px 0;
  font-size: 1.2rem;
  font-weight: 600;
}

.event-info p {
  margin: 0;
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
}

.event-badges {
  display: flex;
  gap: 8px;
}

.badge {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.7rem;
  font-weight: 600;
}

.badge.live {
  background: rgba(255, 71, 87, 0.3);
  color: #ff4757;
  border: 1px solid rgba(255, 71, 87, 0.5);
}

.badge.vip {
  background: rgba(255, 215, 0, 0.2);
  color: #ffd700;
  border: 1px solid rgba(255, 215, 0, 0.5);
}

/* Event Odds */
.event-odds {
  margin-bottom: 15px;
}

.odds-grid {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.odd-item {
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 8px;
  padding: 8px 12px;
  text-align: center;
  min-width: 60px;
}

.odd-label {
  display: block;
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 2px;
}

.odd-value {
  display: block;
  font-size: 1.1rem;
  font-weight: 700;
  color: #ffd700;
}

/* Event Actions */
.event-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.btn-edit, .btn-odds, .btn-live, .btn-delete {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: rgba(255, 255, 255, 0.8);
  padding: 6px 12px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.8rem;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 5px;
}

.btn-edit:hover {
  background: rgba(0, 123, 255, 0.3);
  color: #007bff;
}

.btn-odds:hover {
  background: rgba(255, 193, 7, 0.3);
  color: #ffc107;
}

.btn-live:hover {
  background: rgba(255, 71, 87, 0.3);
  color: #ff4757;
}

.btn-live.active {
  background: rgba(255, 71, 87, 0.4);
  color: #ff4757;
  border-color: rgba(255, 71, 87, 0.6);
}

.btn-delete:hover {
  background: rgba(255, 71, 87, 0.3);
  color: #ff4757;
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 15px;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 25px 30px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.modal-header h3 {
  margin: 0;
  font-size: 1.3rem;
  font-weight: 600;
}

.close-btn {
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.6);
  font-size: 1.5rem;
  cursor: pointer;
  padding: 5px;
  border-radius: 5px;
  transition: all 0.3s ease;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

/* Form */
.event-form {
  padding: 30px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.8);
  font-weight: 500;
}

.form-group input,
.form-group select {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  padding: 12px 15px;
  border-radius: 8px;
  font-size: 0.9rem;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: rgba(102, 126, 234, 0.5);
  box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 15px;
  padding-top: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: rgba(255, 255, 255, 0.8);
  padding: 12px 24px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
}

.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
}

/* Odds Editor */
.odds-editor {
  padding: 30px;
}

.odds-grid {
  display: grid;
  gap: 15px;
  margin-bottom: 30px;
}

.odd-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
}

.odd-row label {
  font-weight: 500;
  color: rgba(255, 255, 255, 0.9);
}

.odd-row input {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  padding: 8px 12px;
  border-radius: 5px;
  text-align: center;
  width: 80px;
  font-weight: 600;
}

.odd-row input:focus {
  outline: none;
  border-color: rgba(102, 126, 234, 0.5);
}

.odds-actions {
  display: flex;
  justify-content: flex-end;
  gap: 15px;
}

/* Responsive */
@media (max-width: 768px) {
  .manager-header {
    flex-direction: column;
    gap: 15px;
    text-align: center;
  }

  .form-row {
    grid-template-columns: 1fr;
  }

  .event-actions {
    justify-content: center;
  }

  .odds-grid {
    grid-template-columns: 1fr;
  }

  .odd-row {
    flex-direction: column;
    gap: 10px;
    align-items: stretch;
  }
}
</style>
