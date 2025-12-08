import { notify } from './notifications'

class PerformanceService {
  constructor() {
    this.observers = new Map()
    this.metrics = new Map()
    this.isEnabled = true
  }

  // Инициализация сервиса производительности
  init() {
    this.setupPerformanceObserver()
    this.setupResourceHints()
    this.setupLazyLoading()
    this.setupImageOptimization()
    this.setupMemoryMonitoring()
  }

  // Настройка Performance Observer
  setupPerformanceObserver() {
    if (!this.isEnabled || !('PerformanceObserver' in window)) return

    try {
      // Наблюдение за Core Web Vitals
      this.observeCoreWebVitals()

      // Наблюдение за загрузкой ресурсов
      this.observeResourceTiming()

      // Наблюдение за навигацией
      this.observeNavigationTiming()

    } catch (error) {
      console.error('Performance Observer setup error:', error)
    }
  }

  // Наблюдение за Core Web Vitals
  observeCoreWebVitals() {
    // Largest Contentful Paint (LCP)
    const lcpObserver = new PerformanceObserver((list) => {
      const entries = list.getEntries()
      const lastEntry = entries[entries.length - 1]
      this.metrics.set('LCP', {
        value: lastEntry.startTime,
        rating: this.getRating('LCP', lastEntry.startTime)
      })
      console.log('LCP:', lastEntry.startTime + 'ms')
    })
    lcpObserver.observe({ entryTypes: ['largest-contentful-paint'] })

    // First Input Delay (FID)
    const fidObserver = new PerformanceObserver((list) => {
      const entries = list.getEntries()
      entries.forEach(entry => {
        this.metrics.set('FID', {
          value: entry.processingStart - entry.startTime,
          rating: this.getRating('FID', entry.processingStart - entry.startTime)
        })
        console.log('FID:', entry.processingStart - entry.startTime + 'ms')
      })
    })
    fidObserver.observe({ entryTypes: ['first-input'] })

    // Cumulative Layout Shift (CLS)
    let clsValue = 0
    const clsObserver = new PerformanceObserver((list) => {
      const entries = list.getEntries()
      entries.forEach(entry => {
        if (!entry.hadRecentInput) {
          clsValue += entry.value
        }
      })
      this.metrics.set('CLS', {
        value: clsValue,
        rating: this.getRating('CLS', clsValue)
      })
      console.log('CLS:', clsValue)
    })
    clsObserver.observe({ entryTypes: ['layout-shift'] })

    this.observers.set('LCP', lcpObserver)
    this.observers.set('FID', fidObserver)
    this.observers.set('CLS', clsObserver)
  }

  // Наблюдение за загрузкой ресурсов
  observeResourceTiming() {
    const resourceObserver = new PerformanceObserver((list) => {
      const entries = list.getEntries()
      entries.forEach(entry => {
        if (entry.duration > 1000) { // Ресурсы дольше 1 секунды
          console.warn('Slow resource:', entry.name, entry.duration + 'ms')
        }
      })
    })
    resourceObserver.observe({ entryTypes: ['resource'] })
    this.observers.set('resource', resourceObserver)
  }

  // Наблюдение за навигацией
  observeNavigationTiming() {
    const navObserver = new PerformanceObserver((list) => {
      const entries = list.getEntries()
      entries.forEach(entry => {
        const loadTime = entry.loadEventEnd - entry.navigationStart
        this.metrics.set('PageLoad', {
          value: loadTime,
          rating: this.getRating('PageLoad', loadTime)
        })
        console.log('Page Load Time:', loadTime + 'ms')
      })
    })
    navObserver.observe({ entryTypes: ['navigation'] })
    this.observers.set('navigation', navObserver)
  }

  // Получение рейтинга метрики
  getRating(metric, value) {
    const thresholds = {
      LCP: { good: 2500, needsImprovement: 4000 },
      FID: { good: 100, needsImprovement: 300 },
      CLS: { good: 0.1, needsImprovement: 0.25 },
      PageLoad: { good: 2000, needsImprovement: 4000 }
    }

    const threshold = thresholds[metric]
    if (!threshold) return 'unknown'

    if (value <= threshold.good) return 'good'
    if (value <= threshold.needsImprovement) return 'needs-improvement'
    return 'poor'
  }

  // Настройка Resource Hints - отключено для избежания 404 ошибок
  setupResourceHints() {
    // Resource hints отключены для предотвращения ошибок с несуществующими ресурсами
    console.log('Resource hints disabled to prevent 404 errors')
  }

  // Настройка Lazy Loading
  setupLazyLoading() {
    // Lazy loading изображений
    const images = document.querySelectorAll('img[data-src]')

    if ('IntersectionObserver' in window) {
      const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const img = entry.target
            img.src = img.dataset.src
            img.classList.remove('lazy')
            observer.unobserve(img)
          }
        })
      }, {
        rootMargin: '50px 0px'
      })

      images.forEach(img => imageObserver.observe(img))
    } else {
      // Fallback для браузеров без IntersectionObserver
      images.forEach(img => {
        img.src = img.dataset.src
      })
    }

    // Lazy loading компонентов Vue
    this.setupComponentLazyLoading()
  }

  // Lazy loading компонентов
  setupComponentLazyLoading() {
    // Отложенная загрузка тяжелых компонентов
    const lazyComponents = [
      { selector: '.heavy-component', delay: 1000 }
    ]

    lazyComponents.forEach(({ selector, delay }) => {
      setTimeout(() => {
        const elements = document.querySelectorAll(selector)
        elements.forEach(el => {
          el.style.opacity = '1'
        })
      }, delay)
    })
  }

  // Оптимизация изображений
  setupImageOptimization() {
    // WebP support detection
    const supportsWebP = () => {
      const canvas = document.createElement('canvas')
      return canvas.toDataURL('image/webp').indexOf('data:image/webp') === 0
    }

    if (supportsWebP()) {
      document.documentElement.classList.add('webp-supported')
    }

    // Responsive images
    this.setupResponsiveImages()
  }

  // Настройка responsive изображений
  setupResponsiveImages() {
    const images = document.querySelectorAll('img[data-responsive]')

    images.forEach(img => {
      const updateImage = () => {
        const width = img.clientWidth
        const srcset = img.dataset.srcset

        if (srcset) {
          const sources = srcset.split(',')
          let bestSource = sources[0].trim()

          for (const source of sources) {
            const [url, size] = source.trim().split(' ')
            if (size && width <= parseInt(size)) {
              bestSource = url
              break
            }
          }

          if (img.src !== bestSource) {
            img.src = bestSource
          }
        }
      }

      if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries) => {
          entries.forEach(entry => {
            if (entry.isIntersecting) {
              updateImage()
              observer.unobserve(img)
            }
          })
        })
        observer.observe(img)
      } else {
        updateImage()
      }
    })
  }

  // Мониторинг памяти
  setupMemoryMonitoring() {
    if ('memory' in performance) {
      setInterval(() => {
        const memInfo = performance.memory
        const memoryUsage = {
          used: Math.round(memInfo.usedJSHeapSize / 1024 / 1024),
          total: Math.round(memInfo.totalJSHeapSize / 1024 / 1024),
          limit: Math.round(memInfo.jsHeapSizeLimit / 1024 / 1024)
        }

        this.metrics.set('Memory', memoryUsage)

        // Предупреждение при высоком использовании памяти
        if (memoryUsage.used > memoryUsage.total * 0.8) {
          console.warn('High memory usage:', memoryUsage)
          this.optimizeMemory()
        }
      }, 10000)
    }
  }

  // Оптимизация памяти
  optimizeMemory() {
    // Очистка неиспользуемых объектов
    if (window.gc) {
      window.gc()
    }

    // Очистка кеша изображений
    const images = document.querySelectorAll('img')
    images.forEach(img => {
      if (img.complete && img.naturalHeight === 0) {
        img.remove()
      }
    })

    try {
      notify.info('Оптимизация', 'Выполнена очистка памяти')
    } catch (error) {
      console.log('Memory optimization completed')
    }
  }

  // Virtual scrolling для больших списков
  setupVirtualScrolling(container, itemHeight = 50) {
    return {
      render: (items, scrollTop) => {
        const start = Math.floor(scrollTop / itemHeight)
        const visibleCount = Math.ceil(container.clientHeight / itemHeight)
        const end = Math.min(start + visibleCount + 2, items.length)

        return items.slice(start, end).map((item, index) => ({
          ...item,
          index: start + index,
          top: (start + index) * itemHeight
        }))
      }
    }
  }

  // Оптимизация анимаций
  optimizeAnimations() {
    // Проверка поддержки will-change
    const supportsWillChange = CSS.supports('will-change', 'transform')

    if (supportsWillChange) {
      // Добавление will-change для анимированных элементов
      const animatedElements = document.querySelectorAll('.animate-pulse, .animate-bounce, .transition-all')

      animatedElements.forEach(el => {
        el.style.willChange = 'transform, opacity'
      })

      // Удаление will-change через некоторое время
      setTimeout(() => {
        animatedElements.forEach(el => {
          el.style.willChange = 'auto'
        })
      }, 1000)
    }
  }

  // Отсрочка выполнения тяжелых операций
  deferHeavyOperations() {
    // Использование requestIdleCallback для отложенных операций
    if ('requestIdleCallback' in window) {
      requestIdleCallback(() => {
        this.runDeferredTasks()
      }, { timeout: 5000 })
    } else {
      setTimeout(() => {
        this.runDeferredTasks()
      }, 1000)
    }
  }

  // Выполнение отложенных задач
  runDeferredTasks() {
    // Анализ производительности
    this.analyzePerformance()

    // Предзагрузка ресурсов
    this.preloadResources()

    // Очистка неиспользуемых ресурсов
    this.cleanupUnusedResources()
  }

  // Анализ производительности
  analyzePerformance() {
    const analysis = {
      metrics: Object.fromEntries(this.metrics),
      recommendations: []
    }

    // Анализ LCP
    const lcp = this.metrics.get('LCP')
    if (lcp && lcp.rating === 'poor') {
      analysis.recommendations.push('Оптимизируйте Largest Contentful Paint (LCP)')
    }

    // Анализ FID
    const fid = this.metrics.get('FID')
    if (fid && fid.rating === 'poor') {
      analysis.recommendations.push('Улучшите First Input Delay (FID)')
    }

    // Анализ CLS
    const cls = this.metrics.get('CLS')
    if (cls && cls.rating === 'poor') {
      analysis.recommendations.push('Исправьте Cumulative Layout Shift (CLS)')
    }

    console.log('Performance Analysis:', analysis)
    return analysis
  }

  // Предзагрузка ресурсов
  preloadResources() {
    const resources = [
      '/api/user/profile',
      '/images/dice-icon.png'
    ]

    resources.forEach(url => {
      const link = document.createElement('link')
      link.rel = 'preload'
      link.href = url
      link.as = 'fetch'
      document.head.appendChild(link)
    })
  }

  // Очистка неиспользуемых ресурсов
  cleanupUnusedResources() {
    // Очистка скрытых изображений
    const hiddenImages = document.querySelectorAll('img[style*="display: none"]')
    hiddenImages.forEach(img => {
      img.src = ''
    })

    // Очистка неиспользуемых компонентов
    const unusedComponents = document.querySelectorAll('.component-unused')
    unusedComponents.forEach(component => {
      component.remove()
    })
  }

  // Получение метрик производительности
  getMetrics() {
    return Object.fromEntries(this.metrics)
  }

  // Экспорт данных для аналитики
  exportMetrics() {
    const data = {
      timestamp: new Date().toISOString(),
      url: window.location.href,
      userAgent: navigator.userAgent,
      metrics: this.getMetrics()
    }

    return data
  }

  // Остановка наблюдения
  destroy() {
    this.observers.forEach(observer => {
      if (observer) {
        observer.disconnect()
      }
    })
    this.observers.clear()
    this.metrics.clear()
  }
}

// Создаем синглтон
const performanceService = new PerformanceService()

export default performanceService
