class LocalizationService {
  constructor() {
    this.currentLocale = 'ru'
    this.fallbackLocale = 'ru'
    this.translations = {}
    this.listeners = []
  }

  // Инициализация сервиса локализации
  async init() {
    await this.loadTranslations(this.currentLocale)
    this.setupLocaleDetection()
  }

  // Загрузка переводов
  async loadTranslations(locale) {
    try {
      const translations = await this.fetchTranslations(locale)
      this.translations = { ...this.translations, ...translations }
      this.notifyListeners()
    } catch (error) {
      console.error('Failed to load translations:', error)
      // Fallback к встроенным переводам
      this.translations = this.getFallbackTranslations()
    }
  }

  // Получение переводов (в реальном приложении это будет API запрос)
  async fetchTranslations(locale) {
    // Имитация загрузки переводов
    return new Promise(resolve => {
      setTimeout(() => {
        resolve(this.getFallbackTranslations())
      }, 100)
    })
  }

  // Встроенные переводы для fallback
  getFallbackTranslations() {
    return {
      // Общие
      'app.title': 'TREASURE Casino',
      'app.description': 'Современное казино в Telegram',
      'common.loading': 'Загрузка...',
      'common.error': 'Ошибка',
      'common.success': 'Успех',
      'common.cancel': 'Отмена',
      'common.confirm': 'Подтвердить',
      'common.yes': 'Да',
      'common.no': 'Нет',
      'common.ok': 'OK',
      'common.save': 'Сохранить',
      'common.delete': 'Удалить',
      'common.edit': 'Редактировать',
      'common.back': 'Назад',
      'common.next': 'Далее',
      'common.previous': 'Назад',
      'common.close': 'Закрыть',
      'common.open': 'Открыть',
      'common.send': 'Отправить',
      'common.receive': 'Получить',
      'common.copy': 'Копировать',
      'common.paste': 'Вставить',
      'common.share': 'Поделиться',
      'common.download': 'Скачать',
      'common.upload': 'Загрузить',
      'common.refresh': 'Обновить',
      'common.retry': 'Повторить',

      // Навигация
      'nav.home': 'Главная',
      'nav.dice': 'Dice',
      'nav.wheel': 'Wheel',
      'nav.bonus': 'Бонусы',
      'nav.profile': 'Профиль',
      'nav.history': 'История',
      'nav.settings': 'Настройки',
      'nav.help': 'Помощь',
      'nav.about': 'О нас',

      // Игры
      'games.dice.title': 'Dice - игра в кости',
      'games.dice.description': 'Угадай число и увеличь свой депозит!',
      'games.wheel.title': 'Wheel - колесо фортуны',
      'games.wheel.description': 'Колесо фортуны с большими выигрышами!',
      'games.mines.title': 'Mines - сапер',
      'games.mines.description': 'Найди все сокровища, избегая мин!',
      'games.slots.title': 'Slots - слоты',
      'games.slots.description': 'Классические слоты с джекпотом!',

      // Кнопки ставок
      'bet.min': 'Min',
      'bet.max': 'Max',
      'bet.double': 'x2',
      'bet.half': '1/2',
      'bet.play': 'Играть',
      'bet.cashout': 'Забрать',
      'bet.place': 'Ставка',
      'bet.amount': 'Сумма ставки',

      // Результаты
      'result.win': 'Победа!',
      'result.loss': 'Проигрыш',
      'result.tie': 'Ничья',
      'result.jackpot': 'ДЖЕКПОТ!',
      'result.bonus': 'Бонус!',

      // Валюта и деньги
      'currency.rub': '₽',
      'currency.usd': '$',
      'currency.eur': '€',
      'money.balance': 'Баланс',
      'money.deposit': 'Пополнить',
      'money.withdraw': 'Вывести',
      'money.profit': 'Прибыль',
      'money.loss': 'Убыток',
      'money.winnings': 'Выигрыш',
      'money.bet': 'Ставка',

      // Пользователь
      'user.name': 'Имя',
      'user.email': 'Email',
      'user.phone': 'Телефон',
      'user.avatar': 'Аватар',
      'user.level': 'Уровень',
      'user.rank': 'Ранг',
      'user.score': 'Очки',
      'user.achievement': 'Достижение',
      'user.badge': 'Значок',

      // Время
      'time.now': 'сейчас',
      'time.second': 'секунду',
      'time.seconds': 'секунд',
      'time.minute': 'минуту',
      'time.minutes': 'минут',
      'time.hour': 'час',
      'time.hours': 'часов',
      'time.day': 'день',
      'time.days': 'дней',
      'time.week': 'неделю',
      'time.weeks': 'недель',
      'time.month': 'месяц',
      'time.months': 'месяцев',
      'time.ago': 'назад',
      'time.left': 'осталось',

      // Ошибки
      'error.network': 'Ошибка сети',
      'error.server': 'Ошибка сервера',
      'error.timeout': 'Время ожидания истекло',
      'error.unauthorized': 'Не авторизован',
      'error.forbidden': 'Доступ запрещен',
      'error.not_found': 'Не найдено',
      'error.validation': 'Ошибка валидации',
      'error.insufficient_funds': 'Недостаточно средств',
      'error.game_unavailable': 'Игра недоступна',
      'error.session_expired': 'Сессия истекла',
      'error.try_again': 'Попробуйте еще раз',

      // Уведомления
      'notification.welcome': 'Добро пожаловать!',
      'notification.win': 'Поздравляем с победой!',
      'notification.loss': 'Неудача, попробуйте еще раз',
      'notification.bonus': 'Вы получили бонус!',
      'notification.level_up': 'Уровень повышен!',
      'notification.achievement': 'Новое достижение!',
      'notification.daily_bonus': 'Ежедневный бонус доступен',

      // Бонусы
      'bonus.daily': 'Ежедневный бонус',
      'bonus.wheel': 'Колесо фортуны',
      'bonus.promo': 'Промокод',
      'bonus.free_spins': 'Бесплатные вращения',
      'bonus.deposit_bonus': 'Бонус на депозит',
      'bonus.referral': 'Реферальный бонус',
      'bonus.vip': 'VIP бонус',

      // Турниры
      'tournament.active': 'Активные турниры',
      'tournament.upcoming': 'Предстоящие турниры',
      'tournament.my': 'Мои турниры',
      'tournament.join': 'Присоединиться',
      'tournament.leave': 'Покинуть',
      'tournament.leaderboard': 'Таблица лидеров',
      'tournament.prize': 'Приз',
      'tournament.participants': 'Участники',
      'tournament.winner': 'Победитель',

      // Достижения
      'achievement.new': 'Новое достижение!',
      'achievement.progress': 'Прогресс',
      'achievement.completed': 'Завершено',
      'achievement.reward': 'Награда',
      'achievement.unlocked': 'Разблокировано',

      // Социальные функции
      'social.friends': 'Друзья',
      'social.invite': 'Пригласить',
      'social.share': 'Поделиться',
      'social.chat': 'Чат',
      'social.online': 'онлайн',
      'social.offline': 'офлайн',

      // Настройки
      'settings.language': 'Язык',
      'settings.theme': 'Тема',
      'settings.sound': 'Звук',
      'settings.notifications': 'Уведомления',
      'settings.privacy': 'Приватность',
      'settings.security': 'Безопасность',

      // Помощь
      'help.faq': 'Часто задаваемые вопросы',
      'help.support': 'Поддержка',
      'help.contact': 'Контакты',
      'help.rules': 'Правила',
      'help.terms': 'Условия использования',
      'help.privacy': 'Политика конфиденциальности',

      // Статусы
      'status.loading': 'Загрузка...',
      'status.processing': 'Обработка...',
      'status.connecting': 'Подключение...',
      'status.connected': 'Подключено',
      'status.disconnected': 'Отключено',
      'status.error': 'Ошибка',

      // Подтверждения
      'confirm.logout': 'Вы уверены, что хотите выйти?',
      'confirm.delete': 'Вы уверены, что хотите удалить?',
      'confirm.reset': 'Вы уверены, что хотите сбросить?',
      'confirm.purchase': 'Подтвердить покупку?',
      'confirm.bet': 'Подтвердить ставку?',

      // Математика и числа
      'math.multiplier': 'Множитель',
      'math.chance': 'Шанс',
      'math.percentage': 'Процент',
      'math.ratio': 'Коэффициент',
      'math.probability': 'Вероятность',

      // Специальные символы и эмодзи
      'emoji.win': '🎉',
      'emoji.loss': '😔',
      'emoji.jackpot': '💎',
      'emoji.bonus': '🎁',
      'emoji.level': '⭐',
      'emoji.achievement': '🏆',
      'emoji.money': '💰',
      'emoji.game': '🎮',
      'emoji.trophy': '🏅',
      'emoji.star': '⭐'
    }
  }

  // Перевод текста
  t(key, params = {}) {
    let text = this.translations[key] || key

    // Замена параметров
    Object.keys(params).forEach(param => {
      const placeholder = `{${param}}`
      text = text.replace(new RegExp(placeholder, 'g'), params[param])
    })

    return text
  }

  // Перевод с множественным числом
  tc(key, count, params = {}) {
    const pluralKey = `${key}_${this.getPluralForm(count)}`
    return this.t(pluralKey, { ...params, count })
  }

  // Получение формы множественного числа для русского языка
  getPluralForm(count) {
    if (count % 10 === 1 && count % 100 !== 11) return 'one'
    if (count % 10 >= 2 && count % 10 <= 4 && (count % 100 < 10 || count % 100 >= 20)) return 'few'
    return 'many'
  }

  // Форматирование чисел
  n(number, options = {}) {
    return new Intl.NumberFormat(this.currentLocale, options).format(number)
  }

  // Форматирование валюты
  c(amount, currency = 'RUB') {
    return new Intl.NumberFormat(this.currentLocale, {
      style: 'currency',
      currency: currency
    }).format(amount)
  }

  // Форматирование даты
  d(date, options = {}) {
    return new Intl.DateTimeFormat(this.currentLocale, options).format(new Date(date))
  }

  // Форматирование времени
  dt(date, options = {}) {
    return new Intl.DateTimeFormat(this.currentLocale, {
      ...options,
      timeStyle: 'short'
    }).format(new Date(date))
  }

  // Изменение локали
  async setLocale(locale) {
    if (this.currentLocale === locale) return

    this.currentLocale = locale
    await this.loadTranslations(locale)
    this.notifyListeners()
  }

  // Получение текущей локали
  getCurrentLocale() {
    return this.currentLocale
  }

  // Определение локали браузера
  setupLocaleDetection() {
    const browserLocale = navigator.language || navigator.userLanguage
    if (browserLocale && browserLocale.startsWith('ru')) {
      this.setLocale('ru')
    }
  }

  // Подписка на изменения локали
  subscribe(callback) {
    this.listeners.push(callback)
    return () => {
      const index = this.listeners.indexOf(callback)
      if (index !== -1) {
        this.listeners.splice(index, 1)
      }
    }
  }

  // Уведомление слушателей
  notifyListeners() {
    this.listeners.forEach(callback => {
      try {
        callback(this.currentLocale, this.translations)
      } catch (error) {
        console.error('Error in locale listener:', error)
      }
    })
  }

  // Получение доступных локалей
  getAvailableLocales() {
    return [
      { code: 'ru', name: 'Русский', flag: '🇷🇺' },
      { code: 'en', name: 'English', flag: '🇺🇸' },
      { code: 'es', name: 'Español', flag: '🇪🇸' },
      { code: 'de', name: 'Deutsch', flag: '🇩🇪' },
      { code: 'fr', name: 'Français', flag: '🇫🇷' },
      { code: 'it', name: 'Italiano', flag: '🇮🇹' },
      { code: 'pt', name: 'Português', flag: '🇵🇹' },
      { code: 'zh', name: '中文', flag: '🇨🇳' },
      { code: 'ja', name: '日本語', flag: '🇯🇵' },
      { code: 'ko', name: '한국어', flag: '🇰🇷' }
    ]
  }

  // Проверка поддержки локали
  isLocaleSupported(locale) {
    try {
      new Intl.DateTimeFormat(locale)
      new Intl.NumberFormat(locale)
      return true
    } catch (error) {
      return false
    }
  }

  // Получение направления текста
  getTextDirection() {
    const rtlLocales = ['ar', 'he', 'fa', 'ur']
    return rtlLocales.includes(this.currentLocale) ? 'rtl' : 'ltr'
  }

  // Получение информации о локали
  getLocaleInfo() {
    return {
      code: this.currentLocale,
      direction: this.getTextDirection(),
      supported: this.isLocaleSupported(this.currentLocale)
    }
  }
}

// Создаем синглтон
const localizationService = new LocalizationService()

// Глобальные функции для удобства использования
export const i18n = {
  t: (key, params) => localizationService.t(key, params),
  tc: (key, count, params) => localizationService.tc(key, count, params),
  n: (number, options) => localizationService.n(number, options),
  c: (amount, currency) => localizationService.c(amount, currency),
  d: (date, options) => localizationService.d(date, options),
  dt: (date, options) => localizationService.dt(date, options),
  setLocale: (locale) => localizationService.setLocale(locale),
  getCurrentLocale: () => localizationService.getCurrentLocale(),
  getAvailableLocales: () => localizationService.getAvailableLocales(),
  getLocaleInfo: () => localizationService.getLocaleInfo(),
  subscribe: (callback) => localizationService.subscribe(callback)
}

export default localizationService
