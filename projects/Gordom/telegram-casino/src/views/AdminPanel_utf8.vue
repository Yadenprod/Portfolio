<template>
  <div class="admin-panel">
    <!-- Header -->
    <div class="admin-header">
      <div class="header-content">
        <h1>рџЋЇ РђРґРјРёРЅ РџР°РЅРµР»СЊ</h1>
        <p>РЈРїСЂР°РІР»РµРЅРёРµ СЃРїРѕСЂС‚РёРІРЅС‹РјРё СЃРѕР±С‹С‚РёСЏРјРё Рё СЃС‚Р°РІРєР°РјРё</p>
      </div>
      <button @click="logout" class="logout-btn">
        <i class="fas fa-sign-out-alt"></i>
        Р’С‹Р№С‚Рё
      </button>
    </div>

    <!-- Navigation Tabs -->
    <div class="admin-nav">
      <button
        v-for="tab in tabs"
        :key="tab.id"
        @click="activeTab = tab.id"
        :class="['nav-tab', { active: activeTab === tab.id }]"
      >
        <i :class="tab.icon"></i>
        {{ tab.name }}
      </button>
    </div>

    <!-- РЎРѕРґРµСЂР¶РёРјРѕРµ РІРєР»Р°РґРѕРє -->
    <div class="admin-content">
      <!-- РЎРѕР±С‹С‚РёСЏ -->
      <div v-if="activeTab === 'events'" class="events-tab">
        <div class="tab-header">
          <h2>РЈРїСЂР°РІР»РµРЅРёРµ СЃРѕР±С‹С‚РёСЏРјРё</h2>
          <button @click="showCreateEventModal = true" class="create-btn">
            вћ• РЎРѕР·РґР°С‚СЊ СЃРѕР±С‹С‚РёРµ
          </button>
        </div>

        <div class="events-list">
          <div
            v-for="event in events"
            :key="event.id"
            :class="['event-item', event.importance, { live: event.is_live }]"
          >
            <div class="event-header">
              <div class="event-info">
                <h3>{{ event.home_team }} vs {{ event.away_team }}</h3>
                <p>{{ event.league }} вЂў {{ formatTime(event.start_time) }}</p>
              </div>
              <div class="event-badges">
                <span v-if="event.is_live" class="badge live">Live</span>
                <span v-if="event.importance === 'high'" class="badge vip">VIP</span>
              </div>
            </div>

            <div class="event-odds">
              <div class="odds-group">
                <span class="odds-label">1:</span>
                <input
                  v-model.number="event.odds.home"
                  @change="updateEventOdds(event)"
                  type="number"
                  step="0.01"
                  min="1.01"
                  class="odds-input"
                />
              </div>
              <div class="odds-group">
                <span class="odds-label">X:</span>
                <input
                  v-if="event.odds.draw"
                  v-model.number="event.odds.draw"
                  @change="updateEventOdds(event)"
                  type="number"
                  step="0.01"
                  min="1.01"
                  class="odds-input"
                />
                <span v-else class="no-odds">-</span>
              </div>
              <div class="odds-group">
                <span class="odds-label">2:</span>
                <input
                  v-model.number="event.odds.away"
                  @change="updateEventOdds(event)"
                  type="number"
                  step="0.01"
                  min="1.01"
                  class="odds-input"
                />
              </div>
            </div>

            <div class="event-actions">
              <button @click="editEvent(event)" class="btn-edit">
                <i class="fas fa-edit"></i>
                Р РµРґР°РєС‚РёСЂРѕРІР°С‚СЊ
              </button>
              <button @click="editOdds(event)" class="btn-odds">
                <i class="fas fa-coins"></i>
                РљРѕСЌС„С„РёС†РёРµРЅС‚С‹
              </button>
              <button @click="toggleLiveStatus(event)" :class="['btn-live', { active: event.is_live }]">
                <i class="fas fa-play"></i>
                {{ event.is_live ? 'РћСЃС‚Р°РЅРѕРІРёС‚СЊ' : 'Р—Р°РїСѓСЃС‚РёС‚СЊ Live' }}
              </button>
              <button @click="deleteEvent(event)" class="btn-delete">
                <i class="fas fa-trash"></i>
                РЈРґР°Р»РёС‚СЊ
              </button>
            </div>
          </div>
        </div>

        <!-- Create Event Modal -->
        <div v-if="showCreateEventModal" class="modal-overlay">
          <div class="modal">
            <div class="modal-header">
              <h3>{{ editingEvent ? 'Р РµРґР°РєС‚РёСЂРѕРІР°С‚СЊ СЃРѕР±С‹С‚РёРµ' : 'РЎРѕР·РґР°С‚СЊ СЃРѕР±С‹С‚РёРµ' }}</h3>
              <button @click="closeModal" class="close-btn">
                <i class="fas fa-times"></i>
              </button>
            </div>

            <form @submit.prevent="saveEvent" class="event-form">
              <div class="form-row">
                <div class="form-group">
                  <label>Р’РёРґ СЃРїРѕСЂС‚Р°</label>
                  <select v-model="eventForm.sport" required>
                    <option value="football">вљЅ Р¤СѓС‚Р±РѕР»</option>
                    <option value="basketball">рџЏЂ Р‘Р°СЃРєРµС‚Р±РѕР»</option>
                    <option value="tennis">рџЋѕ РўРµРЅРЅРёСЃ</option>
                    <option value="hockey">рџЏ’ РҐРѕРєРєРµР№</option>
                    <option value="csgo">рџЋ® CS:GO</option>
                    <option value="dota2">рџЋЇ Dota 2</option>
                  </select>
                </div>
                <div class="form-group">
                  <label>Р›РёРіР°/РўСѓСЂРЅРёСЂ</label>
                  <input v-model="eventForm.league" type="text" required>
                </div>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label>РљРѕРјР°РЅРґР° 1</label>
                  <input v-model="eventForm.home_team" type="text" required>
                </div>
                <div class="form-group">
                  <label>РљРѕРјР°РЅРґР° 2</label>
                  <input v-model="eventForm.away_team" type="text" required>
                </div>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label>Р”Р°С‚Р° Рё РІСЂРµРјСЏ</label>
                  <input v-model="eventForm.start_time" type="datetime-local" required>
                </div>
                <div class="form-group">
                  <label>РЎС‚Р°РґРёРѕРЅ</label>
                  <input v-model="eventForm.venue" type="text">
                </div>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label>Р’Р°Р¶РЅРѕСЃС‚СЊ</label>
                  <select v-model="eventForm.importance">
                    <option value="low">РќРёР·РєР°СЏ</option>
                    <option value="medium">РЎСЂРµРґРЅСЏСЏ</option>
                    <option value="high">Р’С‹СЃРѕРєР°СЏ</option>
                  </select>
                </div>
                <div class="form-group">
                  <label>РЎС‚Р°С‚СѓСЃ</label>
                  <select v-model="eventForm.status">
                    <option value="upcoming">РџСЂРµРґСЃС‚РѕРёС‚</option>
                    <option value="live">Live</option>
                    <option value="finished">Р—Р°РІРµСЂС€РµРЅ</option>
                  </select>
                </div>
              </div>

              <div class="form-actions">
                <button type="button" @click="closeModal" class="btn-secondary">РћС‚РјРµРЅР°</button>
                <button type="submit" class="btn-primary">
                  {{ editingEvent ? 'РЎРѕС…СЂР°РЅРёС‚СЊ' : 'РЎРѕР·РґР°С‚СЊ' }}
                </button>
              </div>
            </form>
          </div>
        </div>

        <!-- Odds Edit Modal -->
        <div v-if="showOddsModal" class="modal-overlay">
          <div class="modal">
            <div class="modal-header">
              <h3>Р РµРґР°РєС‚РёСЂРѕРІР°РЅРёРµ РєРѕСЌС„С„РёС†РёРµРЅС‚РѕРІ</h3>
              <button @click="closeOddsModal" class="close-btn">
                <i class="fas fa-times"></i>
              </button>
            </div>

            <div class="odds-form">
              <h4>{{ selectedEvent?.home_team }} vs {{ selectedEvent?.away_team }}</h4>
              <div class="odds-grid">
                <div class="odds-item">
                  <label>Рџ1</label>
                  <input v-model.number="selectedEvent.odds.home" type="number" step="0.01" min="1.01">
                </div>
                <div class="odds-item">
                  <label>РҐ</label>
                  <input v-if="selectedEvent.odds.draw" v-model.number="selectedEvent.odds.draw" type="number" step="0.01" min="1.01">
                  <span v-else>-</span>
                </div>
                <div class="odds-item">
                  <label>Рџ2</label>
                  <input v-model.number="selectedEvent.odds.away" type="number" step="0.01" min="1.01">
                </div>
              </div>
              <div class="form-actions">
                <button @click="resetOdds" class="btn-secondary">РЎР±СЂРѕСЃРёС‚СЊ</button>
                <button @click="saveOdds" class="btn-primary">РЎРѕС…СЂР°РЅРёС‚СЊ</button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- РџРѕР»СЊР·РѕРІР°С‚РµР»Рё -->
      <div v-if="activeTab === 'users'" class="users-tab">
        <div class="tab-header">
          <h2>РЈРїСЂР°РІР»РµРЅРёРµ РїРѕР»СЊР·РѕРІР°С‚РµР»СЏРјРё</h2>
          <div class="search-box">
            <input
              v-model="userSearch"
              type="text"
              placeholder="РџРѕРёСЃРє РїРѕР»СЊР·РѕРІР°С‚РµР»РµР№..."
              class="search-input"
            />
          </div>
        </div>

        <div class="users-list">
          <div class="user-item user-header">
            <div class="user-info">РџРѕР»СЊР·РѕРІР°С‚РµР»СЊ</div>
            <div class="user-balance">Р‘Р°Р»Р°РЅСЃ</div>
            <div class="user-status">РЎС‚Р°С‚СѓСЃ</div>
            <div class="user-actions">Р”РµР№СЃС‚РІРёСЏ</div>
          </div>

          <div
            v-for="user in filteredUsers"
            :key="user.id"
            class="user-item"
          >
            <div class="user-info">
              <div class="user-avatar">{{ user.name.charAt(0) }}</div>
              <div class="user-details">
                <div class="user-name">{{ user.name }}</div>
                <div class="user-email">{{ user.email }}</div>
              </div>
            </div>
            <div class="user-balance">{{ user.balance }} в‚Ѕ</div>
            <div class="user-status">
              <span :class="['status-badge', user.status]">{{ user.status }}</span>
            </div>
            <div class="user-actions">
              <button @click="banUser(user)" class="btn-ban">Р—Р°Р±Р°РЅРёС‚СЊ</button>
              <button @click="resetUserBalance(user)" class="btn-reset">РЎР±СЂРѕСЃРёС‚СЊ Р±Р°Р»Р°РЅСЃ</button>
            </div>
          </div>
        </div>
      </div>

      <!-- РЎС‚Р°С‚РёСЃС‚РёРєР° -->
      <div v-if="activeTab === 'stats'" class="stats-tab">
        <div class="tab-header">
          <h2>РЎС‚Р°С‚РёСЃС‚РёРєР°</h2>
          <div class="date-filter">
            <input v-model="statsFromDate" type="date">
            <span>РґРѕ</span>
            <input v-model="statsToDate" type="date">
            <button @click="loadStats" class="btn-filter">РџСЂРёРјРµРЅРёС‚СЊ</button>
          </div>
        </div>

        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-icon">рџ“Љ</div>
            <div class="stat-info">
              <h3>Р’СЃРµРіРѕ СЃС‚Р°РІРѕРє</h3>
              <p class="stat-number">{{ stats.totalBets }}</p>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">рџ’°</div>
            <div class="stat-info">
              <h3>РћР±С‰РёР№ РѕР±РѕСЂРѕС‚</h3>
              <p class="stat-number">{{ stats.totalTurnover }} в‚Ѕ</p>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">рџЋЇ</div>
            <div class="stat-info">
              <h3>Р’С‹РёРіСЂС‹С€РЅС‹Рµ СЃС‚Р°РІРєРё</h3>
              <p class="stat-number">{{ stats.winningBets }}</p>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">рџ“€</div>
            <div class="stat-info">
              <h3>РџСЂРёР±С‹Р»СЊ</h3>
              <p class="stat-number">{{ stats.profit }} в‚Ѕ</p>
            </div>
          </div>
        </div>
      </div>

      <!-- РќР°СЃС‚СЂРѕР№РєРё -->
      <div v-if="activeTab === 'settings'" class="settings-tab">
        <div class="tab-header">
          <h2>РќР°СЃС‚СЂРѕР№РєРё СЃРёСЃС‚РµРјС‹</h2>
        </div>

        <div class="settings-form">
          <div class="setting-group">
            <h3>РћР±С‰РёРµ РЅР°СЃС‚СЂРѕР№РєРё</h3>
            <div class="setting-item">
              <label>РњР°РєСЃРёРјР°Р»СЊРЅР°СЏ СЃС‚Р°РІРєР°</label>
              <input v-model.number="settings.maxBet" type="number" min="1">
            </div>
            <div class="setting-item">
              <label>РњРёРЅРёРјР°Р»СЊРЅР°СЏ СЃС‚Р°РІРєР°</label>
              <input v-model.number="settings.minBet" type="number" min="1">
            </div>
            <div class="setting-item">
              <label>РљРѕРјРёСЃСЃРёСЏ (%)</label>
              <input v-model.number="settings.commission" type="number" min="0" max="100">
            </div>
          </div>

          <div class="setting-group">
            <h3>РЈРІРµРґРѕРјР»РµРЅРёСЏ</h3>
            <div class="setting-item">
              <label>
                <input v-model="settings.enableNotifications" type="checkbox">
                Р’РєР»СЋС‡РёС‚СЊ СѓРІРµРґРѕРјР»РµРЅРёСЏ
              </label>
            </div>
            <div class="setting-item">
              <label>
                <input v-model="settings.enableLiveUpdates" type="checkbox">
                Live РѕР±РЅРѕРІР»РµРЅРёСЏ
              </label>
            </div>
          </div>

          <div class="form-actions">
            <button @click="saveSettings" class="btn-primary">РЎРѕС…СЂР°РЅРёС‚СЊ РЅР°СЃС‚СЂРѕР№РєРё</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'AdminPanel',
  setup() {
    const router = useRouter()

    // Data
    const activeTab = ref('events')
    const events = ref([])
    const users = ref([
      { id: 1, name: 'РРІР°РЅ РџРµС‚СЂРѕРІ', email: 'ivan@example.com', balance: 1500, status: 'active' },
      { id: 2, name: 'РњР°СЂРёСЏ РРІР°РЅРѕРІР°', email: 'maria@example.com', balance: 2300, status: 'active' },
      { id: 3, name: 'РђР»РµРєСЃРµР№ РЎРёРґРѕСЂРѕРІ', email: 'alex@example.com', balance: 800, status: 'banned' },
    ])
    const userSearch = ref('')
    const statsFromDate = ref('')
    const statsToDate = ref('')
    const stats = ref({
      totalBets: 0,
      totalTurnover: 0,
      winningBets: 0,
      profit: 0
    })
    const settings = ref({
      maxBet: 10000,
      minBet: 10,
      commission: 5,
      enableNotifications: true,
      enableLiveUpdates: true
    })

    // Modal states
    const showCreateEventModal = ref(false)
    const showOddsModal = ref(false)
    const editingEvent = ref(null)
    const selectedEvent = ref(null)

    // Event form
    const eventForm = ref({
      sport: 'football',
      league: '',
      home_team: '',
      away_team: '',
      start_time: '',
      venue: '',
      importance: 'medium',
      status: 'upcoming'
    })

    // Navigation tabs
    const tabs = ref([
      { id: 'events', name: 'РЎРѕР±С‹С‚РёСЏ', icon: 'fas fa-calendar' },
      { id: 'users', name: 'РџРѕР»СЊР·РѕРІР°С‚РµР»Рё', icon: 'fas fa-users' },
      { id: 'stats', name: 'РЎС‚Р°С‚РёСЃС‚РёРєР°', icon: 'fas fa-chart-bar' },
      { id: 'settings', name: 'РќР°СЃС‚СЂРѕР№РєРё', icon: 'fas fa-cog' }
    ])

    // Computed
    const filteredUsers = computed(() => {
      if (!userSearch.value) return users.value
      return users.value.filter(user =>
        user.name.toLowerCase().includes(userSearch.value.toLowerCase()) ||
        user.email.toLowerCase().includes(userSearch.value.toLowerCase())
      )
    })

    // Methods
    const logout = () => {
      localStorage.removeItem('admin_logged_in')
      router.push('/sports')
    }

    const loadEvents = () => {
      const savedEvents = localStorage.getItem('admin_events')
      if (savedEvents) {
        events.value = JSON.parse(savedEvents)
      }
    }

    const saveEvents = () => {
      localStorage.setItem('admin_events', JSON.stringify(events.value))
    }

    const createEvent = () => {
      showCreateEventModal.value = true
      editingEvent.value = null
      resetEventForm()
    }

    const editEvent = (event) => {
      editingEvent.value = event
      eventForm.value = { ...event }
      showCreateEventModal.value = true
    }

    const editOdds = (event) => {
      selectedEvent.value = event
      showOddsModal.value = true
    }

    const saveEvent = () => {
      if (editingEvent.value) {
        // Update existing event
        const index = events.value.findIndex(e => e.id === editingEvent.value.id)
        if (index !== -1) {
          events.value[index] = {
            ...editingEvent.value,
            ...eventForm.value,
            odds: eventForm.value.odds || generateDefaultOdds(eventForm.value.sport)
          }
        }
      } else {
        // Create new event
        const newEvent = {
          id: Date.now(),
          ...eventForm.value,
          odds: generateDefaultOdds(eventForm.value.sport),
          is_live: eventForm.value.status === 'live'
        }
        events.value.push(newEvent)
      }

      saveEvents()
      closeModal()

      // Emit event to parent components
      window.dispatchEvent(new CustomEvent('events-updated'))
    }

    const deleteEvent = (event) => {
      if (confirm('Р’С‹ СѓРІРµСЂРµРЅС‹, С‡С‚Рѕ С…РѕС‚РёС‚Рµ СѓРґР°Р»РёС‚СЊ СЌС‚Рѕ СЃРѕР±С‹С‚РёРµ?')) {
        events.value = events.value.filter(e => e.id !== event.id)
        saveEvents()
        window.dispatchEvent(new CustomEvent('events-updated'))
      }
    }

    const toggleLiveStatus = (event) => {
      event.is_live = !event.is_live
      event.status = event.is_live ? 'live' : 'upcoming'
      saveEvents()
      window.dispatchEvent(new CustomEvent('events-updated'))
    }

    const updateEventOdds = (event) => {
      saveEvents()
      window.dispatchEvent(new CustomEvent('events-updated'))
    }

    const saveOdds = () => {
      saveEvents()
      closeOddsModal()
      window.dispatchEvent(new CustomEvent('events-updated'))
    }

    const resetOdds = () => {
      if (selectedEvent.value) {
        selectedEvent.value.odds = generateDefaultOdds(selectedEvent.value.sport)
      }
    }

    const generateDefaultOdds = (sport) => {
      const baseOdds = {
        football: { home: 2.10, draw: 3.20, away: 3.50 },
        basketball: { home: 1.85, away: 1.95 },
        tennis: { home: 1.75, away: 2.05 },
        hockey: { home: 2.00, draw: 3.80, away: 3.00 },
        csgo: { home: 1.90, away: 1.90 },
        dota2: { home: 1.85, away: 1.95 }
      }
      return baseOdds[sport] || { home: 2.00, away: 2.00 }
    }

    const resetEventForm = () => {
      eventForm.value = {
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

    const closeModal = () => {
      showCreateEventModal.value = false
      editingEvent.value = null
      resetEventForm()
    }

    const closeOddsModal = () => {
      showOddsModal.value = false
      selectedEvent.value = null
    }

    const banUser = (user) => {
      user.status = user.status === 'banned' ? 'active' : 'banned'
    }

    const resetUserBalance = (user) => {
      if (confirm('РЎР±СЂРѕСЃРёС‚СЊ Р±Р°Р»Р°РЅСЃ РїРѕР»СЊР·РѕРІР°С‚РµР»СЏ?')) {
        user.balance = 0
      }
    }

    const loadStats = () => {
      // Mock stats loading
      stats.value = {
        totalBets: Math.floor(Math.random() * 1000) + 100,
        totalTurnover: Math.floor(Math.random() * 50000) + 10000,
        winningBets: Math.floor(Math.random() * 500) + 50,
        profit: Math.floor(Math.random() * 10000) + 1000
      }
    }

    const saveSettings = () => {
      localStorage.setItem('admin_settings', JSON.stringify(settings.value))
      alert('РќР°СЃС‚СЂРѕР№РєРё СЃРѕС…СЂР°РЅРµРЅС‹!')
    }

    const formatTime = (dateString) => {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleString('ru-RU', {
        day: '2-digit',
        month: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    const formatDate = (dateString) => {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleDateString('ru-RU')
    }

    // Lifecycle
    onMounted(() => {
      loadEvents()
      loadStats()

      // Load settings
      const savedSettings = localStorage.getItem('admin_settings')
      if (savedSettings) {
        settings.value = { ...settings.value, ...JSON.parse(savedSettings) }
      }
    })

    return {
      activeTab,
      tabs,
      events,
      users,
      userSearch,
      filteredUsers,
      statsFromDate,
      statsToDate,
      stats,
      settings,
      showCreateEventModal,
      showOddsModal,
      editingEvent,
      selectedEvent,
      eventForm,
      logout,
      loadEvents,
      saveEvents,
      createEvent,
      editEvent,
      editOdds,
      saveEvent,
      deleteEvent,
      toggleLiveStatus,
      updateEventOdds,
      saveOdds,
      resetOdds,
      generateDefaultOdds,
      resetEventForm,
      closeModal,
      closeOddsModal,
      banUser,
      resetUserBalance,
      loadStats,
      saveSettings,
      formatTime,
      formatDate
    }
  }
}
</script>

<style scoped>
/* Admin Panel Styles */
.admin-panel {
  min-height: 100vh;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f0f23 100%);
  color: white;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Header */
.admin-header {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding: 20px 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.admin-header h1 {
  margin: 0;
  font-size: 2rem;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.admin-header p {
  margin: 5px 0 0 0;
  color: rgba(255, 255, 255, 0.7);
}

.logout-btn {
  background: rgba(255, 71, 87, 0.2);
  border: 1px solid rgba(255, 71, 87, 0.3);
  color: #ff4757;
  padding: 10px 15px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.logout-btn:hover {
  background: rgba(255, 71, 87, 0.3);
  transform: translateY(-1px);
}

/* Navigation */
.admin-nav {
  padding: 20px 30px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  gap: 10px;
  overflow-x: auto;
}

.nav-tab {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.7);
  padding: 12px 20px;
  border-radius: 25px;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
  font-weight: 500;
}

.nav-tab:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

.nav-tab.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-color: rgba(102, 126, 234, 0.5);
}

/* Content */
.admin-content {
  padding: 30px;
}

.tab-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.tab-header h2 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
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

.event-item {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 15px;
  padding: 20px;
  transition: all 0.3s ease;
}

.event-item:hover {
  background: rgba(255, 255, 255, 0.08);
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.event-item.live {
  border-color: rgba(255, 71, 87, 0.5);
  box-shadow: 0 0 20px rgba(255, 71, 87, 0.3);
  animation: livePulse 2s infinite;
}

.event-item.high {
  border-left: 4px solid #ffd700;
}

@keyframes livePulse {
  0%, 100% { box-shadow: 0 0 20px rgba(255, 71, 87, 0.3); }
  50% { box-shadow: 0 0 30px rgba(255, 71, 87, 0.6); }
}

/* Event Info */
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

.odds-group {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.odds-label {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.8rem;
  margin-bottom: 2px;
}

.odds-input {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  padding: 8px 10px;
  border-radius: 5px;
  text-align: center;
  width: 70px;
  font-weight: 600;
}

.odds-input:focus {
  outline: none;
  border-color: rgba(102, 126, 234, 0.5);
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

/* Responsive */
@media (max-width: 768px) {
  .admin-header {
    flex-direction: column;
    gap: 15px;
    text-align: center;
  }

  .admin-nav {
    padding: 15px;
    flex-wrap: wrap;
  }

  .tab-header {
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
}
</style>


