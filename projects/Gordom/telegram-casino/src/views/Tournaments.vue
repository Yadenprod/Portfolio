<template>
  <div class="flex flex-col space-y-6">
    <div class="text-center">
      <h1 class="font-deftone text-3xl text-white mb-2">
        <span class="text-violet">ТУРНИРЫ</span>
      </h1>
      <p class="text-grayLight text-sm">Соревнуйтесь с другими игроками и выигрывайте призы!</p>
    </div>

    <!-- Активные турниры -->
    <div v-if="activeTournaments.length > 0" class="space-y-4">
      <h3 class="text-lg font-semibold text-white">Активные турниры</h3>
      <div class="space-y-4">
        <div
          v-for="tournament in activeTournaments"
          :key="tournament.id"
          class="bg-gradient-to-br from-[#202024] to-[#2c2c31] rounded-2xl p-6"
        >
          <div class="flex items-center justify-between mb-4">
            <div class="flex items-center space-x-4">
              <div class="w-12 h-12 bg-violet/20 rounded-xl flex items-center justify-center">
                <span class="text-2xl">{{ tournament.icon }}</span>
              </div>
              <div>
                <h4 class="text-white font-semibold">{{ tournament.name }}</h4>
                <p class="text-xs text-grayLight">{{ tournament.description }}</p>
              </div>
            </div>
            <div class="text-right">
              <div class="text-lg font-bold text-green">{{ tournament.prize }}₽</div>
              <div class="text-xs text-grayLight">Приз</div>
            </div>
          </div>

          <div class="grid grid-cols-3 gap-4 mb-4">
            <div class="text-center">
              <div class="text-sm font-bold text-blue">{{ tournament.participants }}/10</div>
              <div class="text-xs text-gray">Участников</div>
            </div>
            <div class="text-center">
              <div class="text-sm font-bold text-orange">{{ formatTime(tournament.end_time) }}</div>
              <div class="text-xs text-gray">Осталось</div>
            </div>
            <div class="text-center">
              <div class="text-sm font-bold text-violet">{{ tournament.entry_fee }}₽</div>
              <div class="text-xs text-gray">Взнос</div>
            </div>
          </div>

          <button
            @click="joinTournament(tournament.id)"
            :disabled="!tournament.can_join || loading"
            class="w-full py-3 bg-violet hover:bg-violetHover disabled:opacity-50 disabled:cursor-not-allowed rounded-xl text-white font-semibold transition-all duration-200"
          >
            <span v-if="!loading">{{ tournament.can_join ? 'Присоединиться' : 'Уже участвуете' }}</span>
            <span v-else class="flex items-center justify-center space-x-2">
              <div class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
              <span>Присоединение...</span>
            </span>
          </button>
        </div>
      </div>
    </div>

    <!-- Ближайшие турниры -->
    <div v-if="upcomingTournaments.length > 0" class="space-y-4">
      <h3 class="text-lg font-semibold text-white">Ближайшие турниры</h3>
      <div class="space-y-4">
        <div
          v-for="tournament in upcomingTournaments"
          :key="tournament.id"
          class="bg-gradient-to-br from-[#1b1c20] to-[#2c2c31] rounded-xl p-4"
        >
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-3">
              <div class="w-10 h-10 bg-gray/20 rounded-lg flex items-center justify-center">
                <span class="text-xl">{{ tournament.icon }}</span>
              </div>
              <div>
                <h4 class="text-white font-semibold text-sm">{{ tournament.name }}</h4>
                <p class="text-xs text-grayLight">Старт: {{ formatDateTime(tournament.start_time) }}</p>
              </div>
            </div>
            <div class="text-right">
              <div class="text-sm font-bold text-green">{{ tournament.prize }}₽</div>
              <div class="text-xs text-grayLight">Приз</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Текущие участия -->
    <div v-if="myTournaments.length > 0" class="space-y-4">
      <h3 class="text-lg font-semibold text-white">Мои турниры</h3>
      <div class="space-y-4">
        <div
          v-for="tournament in myTournaments"
          :key="tournament.id"
          class="bg-gradient-to-br from-[#202024] to-[#2c2c31] rounded-xl p-4 border-2 border-green/30"
        >
          <div class="flex items-center justify-between mb-3">
            <div class="flex items-center space-x-3">
              <div class="w-10 h-10 bg-green/20 rounded-lg flex items-center justify-center">
                <span class="text-xl">{{ tournament.icon }}</span>
              </div>
              <div>
                <h4 class="text-white font-semibold">{{ tournament.name }}</h4>
                <p class="text-xs text-green">Вы участвуете</p>
              </div>
            </div>
            <div class="text-right">
              <div class="text-sm font-bold text-violet">{{ tournament.my_score || 0 }}</div>
              <div class="text-xs text-grayLight">Очки</div>
            </div>
          </div>

          <div class="grid grid-cols-3 gap-3 text-center text-xs">
            <div>
              <div class="font-bold text-blue">{{ tournament.position || '-' }}</div>
              <div class="text-grayLight">Позиция</div>
            </div>
            <div>
              <div class="font-bold text-orange">{{ tournament.participants }}/{{ tournament.max_participants }}</div>
              <div class="text-grayLight">Участников</div>
            </div>
            <div>
              <div class="font-bold text-green">{{ formatTime(tournament.end_time) }}</div>
              <div class="text-grayLight">Осталось</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Лидеры турнира -->
    <div v-if="selectedTournament" class="bg-gradient-to-br from-[#202024] to-[#2c2c31] rounded-2xl p-6">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-lg font-semibold text-white">Текущие лидеры</h3>
        <button @click="selectedTournament = null" class="text-gray hover:text-white">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>

      <div class="space-y-3">
        <div
          v-for="(leader, index) in selectedTournament.leaders"
          :key="leader.id"
          class="flex items-center justify-between p-3 bg-[#1b1c20] rounded-lg"
        >
          <div class="flex items-center space-x-3">
            <div class="w-8 h-8 rounded-full flex items-center justify-center text-white font-bold text-sm"
                 :class="{
                   'bg-yellow-500': index === 0,
                   'bg-gray-400': index === 1,
                   'bg-orange-400': index === 2,
                   'bg-violet': index > 2
                 }">
              {{ index + 1 }}
            </div>
            <div>
              <div class="text-white font-semibold">{{ leader.name }}</div>
              <div class="text-xs text-grayLight">{{ leader.score }} очков</div>
            </div>
          </div>
          <div v-if="leader.is_me" class="text-green font-bold">Вы</div>
        </div>
      </div>
    </div>

    <!-- Специальные события -->
    <div v-if="specialEvents.length > 0" class="space-y-4">
      <h3 class="text-lg font-semibold text-white">🎉 Специальные события</h3>
      <div class="space-y-4">
        <div
          v-for="event in specialEvents"
          :key="event.id"
          class="bg-gradient-to-br from-[#202024] to-[#2c2c31] rounded-2xl p-6 relative overflow-hidden"
          :class="event.bgClass"
        >
          <div class="absolute top-0 right-0 w-32 h-32 opacity-10">
            <div class="text-8xl">{{ event.icon }}</div>
          </div>

          <div class="relative z-10">
            <div class="flex items-center space-x-3 mb-3">
              <div class="w-12 h-12 rounded-xl flex items-center justify-center" :class="event.iconBg">
                <span class="text-2xl">{{ event.icon }}</span>
              </div>
              <div>
                <h4 class="text-white font-semibold">{{ event.name }}</h4>
                <p class="text-xs text-grayLight">{{ event.description }}</p>
              </div>
            </div>

            <div class="grid grid-cols-2 gap-4 mb-4">
              <div class="text-center">
                <div class="text-lg font-bold text-green">{{ event.reward }}</div>
                <div class="text-xs text-gray">Награда</div>
              </div>
              <div class="text-center">
                <div class="text-lg font-bold text-blue">{{ formatTime(event.end_time) }}</div>
                <div class="text-xs text-gray">Осталось</div>
              </div>
            </div>

            <button
              @click="participateInEvent(event.id)"
              :disabled="!event.can_participate || loading"
              class="w-full py-3 bg-white/20 hover:bg-white/30 disabled:opacity-50 disabled:cursor-not-allowed rounded-xl text-white font-semibold transition-all duration-200"
            >
              {{ event.can_participate ? 'Участвовать' : 'Уже участвуете' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Пустое состояние -->
    <div v-if="activeTournaments.length === 0 && upcomingTournaments.length === 0" class="text-center py-8">
      <div class="text-6xl mb-4">🏆</div>
      <p class="text-grayLight">Пока нет активных турниров</p>
      <p class="text-xs text-gray mt-2">Следите за обновлениями!</p>
    </div>

    <!-- Уведомление -->
    <div v-if="resultMessage" class="fixed top-4 left-4 right-4 z-50">
      <div :class="isSuccess ? 'bg-green/90' : 'bg-red/90'" class="backdrop-blur-sm rounded-xl p-4 text-white text-center animate-bounce">
        {{ resultMessage }}
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '../stores/user'
import { getActiveTournaments, joinTournament } from '../api/endpoints'
import { notify } from '../services/notifications'

export default {
  name: 'Tournaments',
  setup() {
    const userStore = useUserStore()

    const loading = ref(false)
    const resultMessage = ref('')
    const isSuccess = ref(false)
    const selectedTournament = ref(null)

    const activeTournaments = ref([])
    const upcomingTournaments = ref([])
    const myTournaments = ref([])
    const specialEvents = ref([])

    const formatTime = (timestamp) => {
      const date = new Date(timestamp)
      const now = new Date()
      const diff = date - now

      if (diff <= 0) return 'Завершен'

      const days = Math.floor(diff / (1000 * 60 * 60 * 24))
      const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
      const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60))

      if (days > 0) return `${days}д ${hours}ч`
      if (hours > 0) return `${hours}ч ${minutes}м`
      return `${minutes}м`
    }

    const formatDateTime = (timestamp) => {
      const date = new Date(timestamp)
      return date.toLocaleString('ru-RU', {
        day: 'numeric',
        month: 'short',
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    const showMessage = (message, success = true) => {
      resultMessage.value = message
      isSuccess.value = success
      setTimeout(() => {
        resultMessage.value = ''
      }, 3000)
    }

    const loadTournaments = async () => {
      try {
        loading.value = true
        const tournaments = await getActiveTournaments()

        // Разделяем турниры на активные и предстоящие
        const now = new Date()
        activeTournaments.value = tournaments.filter(t => new Date(t.end_time) > now)
        upcomingTournaments.value = tournaments.filter(t => new Date(t.start_time) > now)

        // Мои турниры (имитация)
        myTournaments.value = activeTournaments.value.slice(0, 2).map(t => ({
          ...t,
          my_score: Math.floor(Math.random() * 1000) + 100,
          position: Math.floor(Math.random() * 10) + 1
        }))

      } catch (error) {
        console.error('Failed to load tournaments:', error)
        // Mock data
        activeTournaments.value = [
          {
            id: 1,
            name: 'Dice Master',
            description: 'Соревнование в игре Dice',
            icon: '🎲',
            prize: 5000,
            participants: 8,
            entry_fee: 100,
            end_time: new Date(Date.now() + 3600000),
            can_join: true
          },
          {
            id: 2,
            name: 'Wheel Champion',
            description: 'Турнир колеса фортуны',
            icon: '🎡',
            prize: 10000,
            participants: 6,
            entry_fee: 200,
            end_time: new Date(Date.now() + 7200000),
            can_join: true
          }
        ]
      } finally {
        loading.value = false
      }
    }

    const joinTournament = async (tournamentId) => {
      loading.value = true
      try {
        const success = await joinTournament(tournamentId)
        if (success) {
          showMessage('Вы успешно присоединились к турниру!')
          notify.info('Турнир', 'Вы присоединились к новому турниру!')
          loadTournaments()
        } else {
          showMessage('Не удалось присоединиться к турниру', false)
        }
      } catch (error) {
        showMessage('Ошибка при присоединении к турниру', false)
      } finally {
        loading.value = false
      }
    }

    const participateInEvent = async (eventId) => {
      showMessage('Специальные события скоро будут доступны!')
    }

    // Загружаем специальные события
    const loadSpecialEvents = () => {
      specialEvents.value = [
        {
          id: 1,
          name: 'Золотая лихорадка',
          description: 'Удвоенные выигрыши в течение 24 часов',
          icon: '🥇',
          reward: 'x2',
          end_time: new Date(Date.now() + 86400000),
          can_participate: true,
          bgClass: 'bg-gradient-to-br from-yellow-900/20 to-orange-900/20',
          iconBg: 'bg-yellow/20'
        },
        {
          id: 2,
          name: 'Ночь бонусов',
          description: 'Каждые 10 минут бесплатный бонус',
          icon: '🌙',
          reward: '500₽',
          end_time: new Date(Date.now() + 43200000),
          can_participate: true,
          bgClass: 'bg-gradient-to-br from-purple-900/20 to-blue-900/20',
          iconBg: 'bg-purple/20'
        }
      ]
    }

    onMounted(() => {
      loadTournaments()
      loadSpecialEvents()
    })

    return {
      loading,
      resultMessage,
      isSuccess,
      activeTournaments,
      upcomingTournaments,
      myTournaments,
      specialEvents,
      selectedTournament,
      formatTime,
      formatDateTime,
      joinTournament,
      participateInEvent
    }
  }
}
</script>
