<template>
  <div class="language-switcher">
    <button
      @click="toggleDropdown"
      class="language-button flex items-center space-x-2 px-3 py-2 rounded-lg bg-[#1b1c20] hover:bg-[#2c2c31] transition-colors"
      :class="{ 'bg-violet/20': showDropdown }"
    >
      <span class="text-lg">{{ currentLocaleFlag }}</span>
      <span class="text-white text-sm hidden sm:block">{{ currentLocaleName }}</span>
      <svg
        class="w-4 h-4 text-gray transition-transform"
        :class="{ 'rotate-180': showDropdown }"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
      </svg>
    </button>

    <!-- Выпадающий список -->
    <Transition
      enter-active-class="transition-all duration-200 ease-out"
      enter-class="opacity-0 scale-95 translate-y-2"
      enter-to-class="opacity-100 scale-100 translate-y-0"
      leave-active-class="transition-all duration-150 ease-in"
      leave-class="opacity-100 scale-100 translate-y-0"
      leave-to-class="opacity-0 scale-95 translate-y-2"
    >
      <div
        v-if="showDropdown"
        class="absolute top-12 right-0 z-50 w-48 bg-[#202024] rounded-xl shadow-2xl border border-violet/20 py-2"
        @click.stop
      >
        <div
          v-for="locale in availableLocales"
          :key="locale.code"
          @click="selectLocale(locale.code)"
          class="flex items-center space-x-3 px-4 py-3 hover:bg-violet/10 cursor-pointer transition-colors"
          :class="{ 'bg-violet/20': locale.code === currentLocale }"
        >
          <span class="text-lg">{{ locale.flag }}</span>
          <span class="text-white flex-1">{{ locale.name }}</span>
          <div
            v-if="locale.code === currentLocale"
            class="w-2 h-2 bg-violet rounded-full"
          ></div>
        </div>
      </div>
    </Transition>

    <!-- Затемнение фона -->
    <div
      v-if="showDropdown"
      @click="toggleDropdown"
      class="fixed inset-0 z-40"
    ></div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import localizationService from '../services/localization'

export default {
  name: 'LanguageSwitcher',
  setup() {
    const showDropdown = ref(false)
    const currentLocale = ref(localizationService.getCurrentLocale())
    const unsubscribe = ref(null)

    const availableLocales = computed(() => localizationService.getAvailableLocales())

    const currentLocaleFlag = computed(() => {
      const locale = availableLocales.value.find(l => l.code === currentLocale.value)
      return locale ? locale.flag : '🌐'
    })

    const currentLocaleName = computed(() => {
      const locale = availableLocales.value.find(l => l.code === currentLocale.value)
      return locale ? locale.name : 'Unknown'
    })

    const toggleDropdown = () => {
      showDropdown.value = !showDropdown.value
    }

    const selectLocale = async (localeCode) => {
      if (localeCode === currentLocale.value) {
        showDropdown.value = false
        return
      }

      try {
        await localizationService.setLocale(localeCode)
        currentLocale.value = localeCode
        showDropdown.value = false

        // Сохраняем выбор пользователя
        localStorage.setItem('preferred_locale', localeCode)

        // Уведомление об изменении языка
        console.log(`Language changed to: ${localeCode}`)

      } catch (error) {
        console.error('Failed to change locale:', error)
      }
    }

    onMounted(() => {
      // Подписываемся на изменения локали
      unsubscribe.value = localizationService.subscribe((locale) => {
        currentLocale.value = locale
      })

      // Восстанавливаем сохраненный выбор
      const savedLocale = localStorage.getItem('preferred_locale')
      if (savedLocale && savedLocale !== currentLocale.value) {
        selectLocale(savedLocale)
      }
    })

    onUnmounted(() => {
      if (unsubscribe.value) {
        unsubscribe.value()
      }
    })

    return {
      showDropdown,
      currentLocale,
      availableLocales,
      currentLocaleFlag,
      currentLocaleName,
      toggleDropdown,
      selectLocale
    }
  }
}
</script>

<style scoped>
.language-button {
  position: relative;
}

.rotate-180 {
  transform: rotate(180deg);
}
</style>
