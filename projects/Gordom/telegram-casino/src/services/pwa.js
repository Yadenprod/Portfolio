import { notify } from './notifications'

class PWAService {
  constructor() {
    this.deferredPrompt = null
    this.isInstallable = false
    this.isInstalled = false
    this.updateAvailable = false
    this.serviceWorker = null
  }

  // Инициализация PWA
  init() {
    this.checkInstallability()
    this.registerServiceWorker()
    this.setupInstallPrompt()
    this.setupUpdateHandling()
  }

  // Регистрация Service Worker
  async registerServiceWorker() {
    // Временно отключаем Service Worker в dev режиме
    if (process.env.NODE_ENV === 'development') {
      console.log('Service Worker disabled in development mode')
      return
    }

    if ('serviceWorker' in navigator) {
      try {
        this.serviceWorker = await navigator.serviceWorker.register('/sw.js', {
          scope: '/'
        })

        console.log('Service Worker registered:', this.serviceWorker)

        // Обработка обновлений
        this.serviceWorker.addEventListener('updatefound', () => {
          const newWorker = this.serviceWorker.installing
          newWorker.addEventListener('statechange', () => {
            if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
              this.updateAvailable = true
              this.showUpdateNotification()
            }
          })
        })

        // Обработка сообщений от Service Worker
        navigator.serviceWorker.addEventListener('message', (event) => {
          this.handleServiceWorkerMessage(event.data)
        })

      } catch (error) {
        console.error('Service Worker registration failed:', error)
      }
    }
  }

  // Проверка возможности установки
  checkInstallability() {
    if ('standalone' in window.navigator && window.navigator.standalone) {
      // iOS Safari в режиме standalone
      this.isInstalled = true
    }

    window.addEventListener('beforeinstallprompt', (event) => {
      event.preventDefault()
      this.deferredPrompt = event
      this.isInstallable = true
      this.showInstallPrompt()
    })

    window.addEventListener('appinstalled', (event) => {
      this.isInstalled = true
      this.isInstallable = false
      try {
        notify.success('Установка', 'Приложение успешно установлено!')
      } catch (error) {
        console.log('PWA installed successfully')
      }
    })
  }

  // Настройка промпта установки
  setupInstallPrompt() {
    // Показывать промпт через некоторое время использования
    setTimeout(() => {
      if (this.isInstallable && !this.isInstalled) {
        this.showInstallPrompt()
      }
    }, 30000) // 30 секунд
  }

  // Показать промпт установки
  showInstallPrompt() {
    try {
      notify.info(
        'Установить приложение',
        'Нажмите здесь, чтобы установить TREASURE Casino на ваше устройство',
        {
          action: {
            text: 'Установить',
            handler: () => this.installApp()
          }
        }
      )
    } catch (error) {
      console.log('PWA install prompt available')
    }
  }

  // Установка приложения
  async installApp() {
    if (!this.deferredPrompt) return

    try {
      await this.deferredPrompt.prompt()
      const { outcome } = await this.deferredPrompt.userChoice

      if (outcome === 'accepted') {
        console.log('User accepted the install prompt')
      } else {
        console.log('User dismissed the install prompt')
      }

      this.deferredPrompt = null
    } catch (error) {
      console.error('Install prompt error:', error)
    }
  }

  // Обработка обновлений
  setupUpdateHandling() {
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.addEventListener('controllerchange', () => {
        console.log('Service Worker updated, reloading page...')
        window.location.reload()
      })
    }
  }

  // Показать уведомление об обновлении
  showUpdateNotification() {
    try {
      notify.info(
        'Доступно обновление',
        'Новая версия приложения готова к установке',
        {
          action: {
            text: 'Обновить',
            handler: () => this.updateApp()
          }
        }
      )
    } catch (error) {
      console.log('PWA update available')
    }
  }

  // Обновление приложения
  async updateApp() {
    if (this.serviceWorker && this.updateAvailable) {
      const newWorker = this.serviceWorker.waiting
      if (newWorker) {
        newWorker.postMessage({ type: 'SKIP_WAITING' })
      }
    }
  }

  // Обработка сообщений от Service Worker
  handleServiceWorkerMessage(data) {
    switch (data.type) {
      case 'CACHE_UPDATED':
        try {
          notify.success('Кеш обновлен', 'Приложение готово к работе в офлайн режиме')
        } catch (error) {
          console.log('Cache updated')
        }
        break
      case 'OFFLINE_READY':
        try {
          notify.info('Офлайн режим', 'Приложение готово к работе без интернета')
        } catch (error) {
          console.log('Offline mode ready')
        }
        break
      default:
        console.log('Service Worker message:', data)
    }
  }

  // Очистка кеша
  async clearCache() {
    try {
      if ('caches' in window) {
        const cacheNames = await caches.keys()
        await Promise.all(
          cacheNames.map(cacheName => caches.delete(cacheName))
        )
        try {
          notify.success('Кеш очищен', 'Все данные кеша удалены')
        } catch (error) {
          console.log('Cache cleared successfully')
        }
      }
    } catch (error) {
      console.error('Cache clear error:', error)
      try {
        notify.error('Ошибка', 'Не удалось очистить кеш')
      } catch (notifyError) {
        console.error('Failed to show cache clear error')
      }
    }
  }

  // Получение информации о кеше
  async getCacheInfo() {
    try {
      if ('caches' in window) {
        const cacheNames = await caches.keys()
        const cacheInfo = {}

        for (const cacheName of cacheNames) {
          const cache = await caches.open(cacheName)
          const requests = await cache.keys()
          cacheInfo[cacheName] = {
            name: cacheName,
            size: requests.length,
            urls: requests.map(r => r.url)
          }
        }

        return cacheInfo
      }
      return {}
    } catch (error) {
      console.error('Cache info error:', error)
      return {}
    }
  }

  // Проверка состояния сети
  getNetworkStatus() {
    return {
      online: navigator.onLine,
      connection: navigator.connection?.effectiveType || 'unknown',
      saveData: navigator.connection?.saveData || false
    }
  }

  // Настройка для экономии данных
  setupDataSaving() {
    if ('connection' in navigator) {
      navigator.connection.addEventListener('change', () => {
        const connection = this.getNetworkStatus()

        if (connection.saveData) {
          // Включить режим экономии данных
          this.enableDataSaving()
        } else {
          // Отключить режим экономии данных
          this.disableDataSaving()
        }
      })
    }
  }

  // Включение режима экономии данных
  enableDataSaving() {
    document.documentElement.classList.add('data-saving')
    // Отключить анимации, автозагрузку и т.д.
    try {
      notify.info('Экономия данных', 'Включен режим экономии трафика')
    } catch (error) {
      console.log('Data saving mode enabled')
    }
  }

  // Отключение режима экономии данных
  disableDataSaving() {
    document.documentElement.classList.remove('data-saving')
    try {
      notify.info('Экономия данных', 'Режим экономии трафика отключен')
    } catch (error) {
      console.log('Data saving mode disabled')
    }
  }

  // Performance monitoring
  setupPerformanceMonitoring() {
    if ('performance' in window) {
      // Отслеживание Core Web Vitals
      this.observeCoreWebVitals()

      // Отслеживание загрузки страницы
      window.addEventListener('load', () => {
        const perfData = performance.timing
        const loadTime = perfData.loadEventEnd - perfData.navigationStart
        console.log('Page load time:', loadTime + 'ms')
      })
    }
  }

  // Наблюдение за Core Web Vitals
  observeCoreWebVitals() {
    if ('web-vitals' in window) {
      // Если используется web-vitals библиотека
      return
    }

    // Простое наблюдение за основными метриками
    const observer = new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        switch (entry.entryType) {
          case 'largest-contentful-paint':
            console.log('LCP:', entry.startTime + 'ms')
            break
          case 'first-input':
            console.log('FID:', entry.processingStart - entry.startTime + 'ms')
            break
          case 'layout-shift':
            if (!entry.hadRecentInput) {
              console.log('CLS:', entry.value)
            }
            break
        }
      }
    })

    observer.observe({ entryTypes: ['largest-contentful-paint', 'first-input', 'layout-shift'] })
  }

  // Предзагрузка критических ресурсов
  preloadCriticalResources() {
    const criticalResources = [
      '/images/logo.png',
      '/css/app.css'
    ]

    criticalResources.forEach(url => {
      const link = document.createElement('link')
      link.rel = 'preload'
      link.href = url
      link.as = this.getResourceType(url)
      document.head.appendChild(link)
    })
  }

  // Определение типа ресурса
  getResourceType(url) {
    if (url.endsWith('.css')) return 'style'
    if (url.endsWith('.js')) return 'script'
    if (/\.(png|jpg|jpeg|gif|svg)$/i.test(url)) return 'image'
    if (/\.(woff|woff2|ttf)$/i.test(url)) return 'font'
    return 'fetch'
  }

  // Lazy loading изображений
  setupLazyLoading() {
    const images = document.querySelectorAll('img[data-src]')

    const imageObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target
          img.src = img.dataset.src
          img.classList.remove('lazy')
          observer.unobserve(img)
        }
      })
    })

    images.forEach(img => {
      imageObserver.observe(img)
    })
  }

  // Получение статуса PWA
  getStatus() {
    return {
      isInstallable: this.isInstallable,
      isInstalled: this.isInstalled,
      updateAvailable: this.updateAvailable,
      networkStatus: this.getNetworkStatus(),
      serviceWorker: !!this.serviceWorker
    }
  }
}

// Создаем синглтон
const pwaService = new PWAService()

export default pwaService
