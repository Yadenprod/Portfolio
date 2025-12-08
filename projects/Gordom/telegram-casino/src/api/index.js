import axios from 'axios'
import { initTelegram } from '../telegram'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

const tg = initTelegram()

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
})

api.interceptors.request.use((config) => {
  // Attach Telegram init data if available
  if (tg?.initData) {
    config.headers['X-Telegram-Init-Data'] = tg.initData
  }
  // Optional: forward user language and theme
  if (tg?.initDataUnsafe?.user?.language_code) {
    config.headers['X-User-Lang'] = tg.initDataUnsafe.user.language_code
  }
  if (tg?.colorScheme) {
    config.headers['X-Theme'] = tg.colorScheme
  }
  return config
})

api.interceptors.response.use(
  (r) => r,
  (error) => {
    const message = error?.response?.data?.message || error.message || 'Network error'
    return Promise.reject(new Error(message))
  }
)

export default api
