import { ref, computed, onMounted, onUnmounted } from 'vue'
import localizationService, { i18n } from '../services/localization'

export function useI18n() {
  const currentLocale = ref(localizationService.getCurrentLocale())
  const localeInfo = ref(localizationService.getLocaleInfo())
  const unsubscribe = ref(null)

  // Вычисляемые значения
  const availableLocales = computed(() => localizationService.getAvailableLocales())
  const textDirection = computed(() => localeInfo.value.direction)
  const isRTL = computed(() => textDirection.value === 'rtl')

  // Методы локализации
  const t = (key, params = {}) => {
    return localizationService.t(key, params)
  }

  const tc = (key, count, params = {}) => {
    return localizationService.tc(key, count, params)
  }

  const n = (number, options = {}) => {
    return localizationService.n(number, options)
  }

  const c = (amount, currency = 'RUB') => {
    return localizationService.c(amount, currency)
  }

  const d = (date, options = {}) => {
    return localizationService.d(date, options)
  }

  const dt = (date, options = {}) => {
    return localizationService.dt(date, options)
  }

  // Изменение локали
  const setLocale = async (locale) => {
    await localizationService.setLocale(locale)
    currentLocale.value = locale
    localeInfo.value = localizationService.getLocaleInfo()
  }

  // Форматирование времени с учетом локали
  const formatTime = (timestamp, options = {}) => {
    const date = new Date(timestamp)
    return localizationService.d(date, {
      hour: '2-digit',
      minute: '2-digit',
      ...options
    })
  }

  // Форматирование даты с учетом локали
  const formatDate = (timestamp, options = {}) => {
    const date = new Date(timestamp)
    return localizationService.d(date, {
      day: 'numeric',
      month: 'short',
      year: 'numeric',
      ...options
    })
  }

  // Форматирование относительного времени
  const formatRelativeTime = (timestamp) => {
    const now = new Date()
    const date = new Date(timestamp)
    const diff = now - date

    if (diff < 60000) return t('time.now')
    if (diff < 3600000) {
      const minutes = Math.floor(diff / 60000)
      return `${minutes} ${tc('time.minute', minutes)} ${t('time.ago')}`
    }
    if (diff < 86400000) {
      const hours = Math.floor(diff / 3600000)
      return `${hours} ${tc('time.hour', hours)} ${t('time.ago')}`
    }
    if (diff < 604800000) {
      const days = Math.floor(diff / 86400000)
      return `${days} ${tc('time.day', days)} ${t('time.ago')}`
    }

    return formatDate(timestamp)
  }

  // Форматирование оставшегося времени
  const formatRemainingTime = (timestamp) => {
    const now = new Date()
    const date = new Date(timestamp)
    const diff = date - now

    if (diff <= 0) return t('time.now')

    if (diff < 60000) {
      const seconds = Math.floor(diff / 1000)
      return `${seconds} ${tc('time.second', seconds)} ${t('time.left')}`
    }
    if (diff < 3600000) {
      const minutes = Math.floor(diff / 60000)
      return `${minutes} ${tc('time.minute', minutes)} ${t('time.left')}`
    }
    if (diff < 86400000) {
      const hours = Math.floor(diff / 3600000)
      return `${hours} ${tc('time.hour', hours)} ${t('time.left')}`
    }
    if (diff < 604800000) {
      const days = Math.floor(diff / 86400000)
      return `${days} ${tc('time.day', days)} ${t('time.left')}`
    }

    return formatDate(timestamp)
  }

  // Форматирование чисел с разделителями
  const formatNumber = (number, options = {}) => {
    return localizationService.n(number, {
      minimumFractionDigits: 0,
      maximumFractionDigits: 2,
      ...options
    })
  }

  // Форматирование процентов
  const formatPercentage = (value, decimals = 1) => {
    return localizationService.n(value, {
      style: 'percent',
      minimumFractionDigits: decimals,
      maximumFractionDigits: decimals
    })
  }

  // Форматирование валюты
  const formatCurrency = (amount, currency = 'RUB', options = {}) => {
    return localizationService.c(amount, currency, options)
  }

  // Форматирование файла
  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 B'

    const k = 1024
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))

    return `${parseFloat((bytes / Math.pow(k, i)).toFixed(2))} ${sizes[i]}`
  }

  // Уведомления об ошибках с локализацией
  const getErrorMessage = (errorType, params = {}) => {
    return t(`error.${errorType}`, params)
  }

  // Уведомления об успехе с локализацией
  const getSuccessMessage = (successType, params = {}) => {
    return t(`notification.${successType}`, params)
  }

  // Названия месяцев
  const getMonthName = (monthIndex, format = 'long') => {
    const date = new Date(2000, monthIndex, 1)
    return localizationService.d(date, {
      month: format
    })
  }

  // Названия дней недели
  const getDayName = (dayIndex, format = 'long') => {
    const date = new Date(2000, 0, dayIndex + 1) // Понедельник = 1
    return localizationService.d(date, {
      weekday: format
    })
  }

  onMounted(() => {
    // Подписываемся на изменения локали
    unsubscribe.value = localizationService.subscribe((locale, translations) => {
      currentLocale.value = locale
      localeInfo.value = localizationService.getLocaleInfo()
    })
  })

  onUnmounted(() => {
    if (unsubscribe.value) {
      unsubscribe.value()
    }
  })

  return {
    // Основные функции
    t,
    tc,
    n,
    c,
    d,
    dt,

    // Текущая локаль
    currentLocale,
    localeInfo,
    availableLocales,
    textDirection,
    isRTL,

    // Методы
    setLocale,
    formatTime,
    formatDate,
    formatRelativeTime,
    formatRemainingTime,
    formatNumber,
    formatPercentage,
    formatCurrency,
    formatFileSize,
    getErrorMessage,
    getSuccessMessage,
    getMonthName,
    getDayName
  }
}

// Экспорт для использования в шаблонах
export { i18n }
