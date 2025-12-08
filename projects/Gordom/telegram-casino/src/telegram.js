// Lightweight wrapper around Telegram WebApp SDK
// Safely handles absence of Telegram environment during local dev

export function initTelegram() {
  const tg = window?.Telegram?.WebApp
  if (!tg) {
    return {
      isAvailable: false,
      colorScheme: 'dark',
      themeParams: {},
      initData: '',
      initDataUnsafe: {},
      onEvent: () => {},
      offEvent: () => {},
      MainButton: { show: () => {}, hide: () => {}, setText: () => {} },
    }
  }

  try {
    tg.ready()
    tg.expand()
  } catch {}

  return {
    isAvailable: true,
    colorScheme: tg.colorScheme,
    themeParams: tg.themeParams || {},
    initData: tg.initData || '',
    initDataUnsafe: tg.initDataUnsafe || {},
    onEvent: tg.onEvent?.bind(tg) || (() => {}),
    offEvent: tg.offEvent?.bind(tg) || (() => {}),
    MainButton: tg.MainButton,
  }
}

export function applyTelegramTheme(root = document.documentElement) {
  const tg = window?.Telegram?.WebApp
  if (!tg || !tg.themeParams) return
  const p = tg.themeParams
  const set = (k, v) => root.style.setProperty(k, v)
  set('--tg-theme-bg-color', p.bg_color || '#202024')
  set('--tg-theme-text-color', p.text_color || '#cfcde9')
  set('--tg-theme-hint-color', p.hint_color || '#6a6a7a')
  set('--tg-theme-link-color', p.link_color || '#7c75d9')
  set('--tg-theme-button-color', p.button_color || '#7c75d9')
  set('--tg-theme-button-text-color', p.button_text_color || '#ffffff')
}
