<template>
  <div class="chat-container">
    <!-- Кнопка открытия чата -->
    <button
      @click="toggleChat"
      class="fixed bottom-20 right-4 z-40 w-14 h-14 bg-violet hover:bg-violetHover rounded-full shadow-lg flex items-center justify-center transition-all duration-300 hover:scale-110"
      :class="{ 'scale-110': showChat }"
    >
      <svg v-if="!showChat" class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/>
      </svg>
      <svg v-else class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
      </svg>
    </button>

    <!-- Индикатор новых сообщений -->
    <div
      v-if="unreadCount > 0 && !showChat"
      class="fixed bottom-32 right-2 z-50 w-6 h-6 bg-red rounded-full flex items-center justify-center text-white text-xs font-bold animate-bounce"
    >
      {{ unreadCount > 9 ? '9+' : unreadCount }}
    </div>

    <!-- Окно чата -->
    <Transition
      enter-active-class="transition-all duration-300 ease-out"
      enter-class="opacity-0 scale-95 translate-y-4"
      enter-to-class="opacity-100 scale-100 translate-y-0"
      leave-active-class="transition-all duration-200 ease-in"
      leave-class="opacity-100 scale-100 translate-y-0"
      leave-to-class="opacity-0 scale-95 translate-y-4"
    >
      <div
        v-if="showChat"
        class="fixed bottom-20 right-4 z-50 w-80 h-96 bg-gradient-to-br from-[#202024] to-[#2c2c31] rounded-2xl shadow-2xl border border-violet/20 flex flex-col"
      >
        <!-- Заголовок чата -->
        <div class="flex items-center justify-between p-4 border-b border-violet/20">
          <div class="flex items-center space-x-3">
            <div class="w-8 h-8 bg-violet/20 rounded-full flex items-center justify-center">
              <svg class="w-4 h-4 text-violet" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/>
              </svg>
            </div>
            <div>
              <h3 class="text-white font-semibold text-sm">Чат казино</h3>
              <p class="text-grayLight text-xs">{{ onlineCount }} онлайн</p>
            </div>
          </div>
          <button
            @click="toggleChat"
            class="w-6 h-6 text-gray hover:text-white transition-colors"
          >
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>

        <!-- Сообщения -->
        <div ref="messagesContainer" class="flex-1 p-4 space-y-3 overflow-y-auto">
          <div
            v-for="message in messages"
            :key="message.id"
            class="flex"
            :class="{ 'justify-end': message.isOwn }"
          >
            <div
              class="max-w-[70%] p-3 rounded-2xl text-sm"
              :class="message.isOwn ? 'bg-violet text-white' : 'bg-[#1b1c20] text-grayLight'"
            >
              <div v-if="!message.isOwn" class="text-xs text-violet font-medium mb-1">
                {{ message.user }}
              </div>
              <div class="break-words">{{ message.text }}</div>
              <div class="text-xs mt-1 opacity-70">
                {{ formatTime(message.timestamp) }}
              </div>
            </div>
          </div>

          <!-- Загрузка -->
          <div v-if="loading" class="flex justify-center py-4">
            <div class="w-6 h-6 border-2 border-violet border-t-transparent rounded-full animate-spin"></div>
          </div>
        </div>

        <!-- Форма отправки -->
        <div class="p-4 border-t border-violet/20">
          <form @submit.prevent="sendMessage" class="flex space-x-2">
            <input
              v-model="newMessage"
              type="text"
              placeholder="Введите сообщение..."
              class="flex-1 p-3 bg-[#1b1c20] rounded-xl text-white placeholder-gray focus:outline-none focus:ring-2 focus:ring-violet text-sm"
              maxlength="200"
              :disabled="sending"
            />
            <button
              type="submit"
              :disabled="!canSend || sending"
              class="w-12 h-12 bg-violet hover:bg-violetHover disabled:opacity-50 disabled:cursor-not-allowed rounded-xl flex items-center justify-center transition-all duration-200 hover:scale-105"
            >
              <svg v-if="!sending" class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"/>
              </svg>
              <div v-else class="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            </button>
          </form>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { useUserStore } from '../stores/user'
import { getChatMessages, sendChatMessage, getOnlinePlayers } from '../api/endpoints'
import wsService from '../services/websocket'

export default {
  name: 'Chat',
  setup() {
    let userStore = useUserStore()

    const showChat = ref(false)
    const messages = ref([])
    const newMessage = ref('')
    const loading = ref(false)
    const sending = ref(false)
    const unreadCount = ref(0)
    const onlineCount = ref(0)
    const messagesContainer = ref(null)

    const canSend = computed(() => {
      return newMessage.value.trim().length > 0 && newMessage.value.trim().length <= 200 && !sending.value
    })

    const toggleChat = async () => {
      showChat.value = !showChat.value
      if (showChat.value) {
        unreadCount.value = 0
        await loadMessages()
        await loadOnlineCount()
      }
    }

    const loadMessages = async () => {
      if (loading.value) return

      try {
        loading.value = true
        const data = await getChatMessages(50)
        messages.value = data.map(msg => ({
          id: msg.id,
          user: msg.user_name,
          text: msg.message,
          timestamp: new Date(msg.created_at),
          isOwn: msg.user_id === userStore.user?.id
        }))
        await scrollToBottom()
      } catch (error) {
        console.error('Failed to load chat messages:', error)
      } finally {
        loading.value = false
      }
    }

    const loadOnlineCount = async () => {
      try {
        onlineCount.value = await getOnlinePlayers()
      } catch (error) {
        console.error('Failed to load online count:', error)
      }
    }

    const sendMessage = async () => {
      if (!canSend.value) return

      const messageText = newMessage.value.trim()
      newMessage.value = ''

      try {
        sending.value = true

        // Добавляем сообщение локально для мгновенного отображения
        const localMessage = {
          id: Date.now(),
          user: userStore.user?.name || 'Вы',
          text: messageText,
          timestamp: new Date(),
          isOwn: true,
          isLocal: true
        }
        messages.value.push(localMessage)
        await scrollToBottom()

        // Отправляем через WebSocket если подключен
        if (wsService.getStatus().isConnected) {
          wsService.sendChatMessage(messageText)
        } else {
          // Fallback на API
          const success = await sendChatMessage(messageText)
          if (!success) {
            // Удаляем локальное сообщение при ошибке
            const index = messages.value.findIndex(m => m.id === localMessage.id)
            if (index !== -1) {
              messages.value.splice(index, 1)
            }
            newMessage.value = messageText
          }
        }
      } catch (error) {
        console.error('Failed to send message:', error)
        newMessage.value = messageText
      } finally {
        sending.value = false
      }
    }

    const scrollToBottom = async () => {
      await nextTick()
      if (messagesContainer.value) {
        messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
      }
    }

    const formatTime = (timestamp) => {
      const now = new Date()
      const diff = now - timestamp

      if (diff < 60000) { // Меньше минуты
        return 'только что'
      } else if (diff < 3600000) { // Меньше часа
        return `${Math.floor(diff / 60000)} мин назад`
      } else if (diff < 86400000) { // Меньше дня
        return `${Math.floor(diff / 3600000)} ч назад`
      } else {
        return timestamp.toLocaleDateString('ru-RU', {
          day: 'numeric',
          month: 'short',
          hour: '2-digit',
          minute: '2-digit'
        })
      }
    }

    // Обработчик входящих сообщений через WebSocket
    const handleChatMessage = (payload) => {
      if (payload.user_id !== userStore.user?.id) {
        const message = {
          id: payload.id || Date.now(),
          user: payload.user_name || payload.user,
          text: payload.message || payload.text,
          timestamp: new Date(payload.timestamp || Date.now()),
          isOwn: false
        }
        messages.value.push(message)
        scrollToBottom()

        // Уведомление о новом сообщении
        if (!showChat.value) {
          unreadCount.value++
        }
      }
    }

    // Обработчик обновления онлайн пользователей
    const handleOnlineUsers = (payload) => {
      onlineCount.value = payload.count || 0
    }

    // Автоматическое обновление
    let updateInterval
    let onlineInterval

    onMounted(() => {
      // Подписываемся на WebSocket события
      wsService.on('chat_message', handleChatMessage)
      wsService.on('online_users', handleOnlineUsers)

      // Обновляем онлайн счетчик каждые 30 секунд
      onlineInterval = setInterval(loadOnlineCount, 30000)

      // Обновляем сообщения каждые 10 секунд если чат открыт (как fallback)
      updateInterval = setInterval(() => {
        if (showChat.value && !wsService.getStatus().isConnected) {
          loadMessages()
        }
      }, 10000)
    })

    onUnmounted(() => {
      // Отписываемся от WebSocket событий
      wsService.off('chat_message', handleChatMessage)
      wsService.off('online_users', handleOnlineUsers)

      if (updateInterval) clearInterval(updateInterval)
      if (onlineInterval) clearInterval(onlineInterval)
    })

    return {
      showChat,
      messages,
      newMessage,
      loading,
      sending,
      unreadCount,
      onlineCount,
      messagesContainer,
      canSend,
      toggleChat,
      sendMessage,
      formatTime
    }
  }
}
</script>

<style scoped>
/* Кастомный скроллбар для чата */
.overflow-y-auto::-webkit-scrollbar {
  width: 4px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: #1b1c20;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #7c75d9;
  border-radius: 2px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #8c84ec;
}

/* Анимации для сообщений */
.message-enter-active {
  transition: all 0.3s ease-out;
}

.message-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.message-enter-to {
  opacity: 1;
  transform: translateY(0);
}
</style>
