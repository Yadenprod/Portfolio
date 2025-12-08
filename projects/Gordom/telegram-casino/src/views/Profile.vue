<template>
  <div class="flex flex-col space-y-6">
    <div class="text-center">
      <h1 class="font-deftone text-3xl text-white mb-2">
        <span class="text-violet">ПРОФИЛЬ</span>
      </h1>
    </div>
    
    <div class="bg-[#2c2c31] rounded-2xl p-6 space-y-4">
      <div class="flex items-center space-x-4">
        <div class="w-16 h-16 bg-violet/20 rounded-full flex items-center justify-center">
          <svg class="w-8 h-8 text-violet" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
          </svg>
        </div>
        <div>
          <h3 class="text-lg font-semibold text-white">Пользователь</h3>
          <p class="text-grayLight text-sm">ID: 123456789</p>
        </div>
      </div>
      
      <div class="grid grid-cols-2 gap-4">
        <div class="bg-[#1b1c20] rounded-xl p-4 text-center">
          <div class="text-2xl font-bold text-green mb-1">{{ balance }}</div>
          <div class="text-xs text-gray">Баланс</div>
        </div>
        <div class="bg-[#1b1c20] rounded-xl p-4 text-center">
          <div class="text-2xl font-bold text-violet mb-1">0</div>
          <div class="text-xs text-gray">Рефералов</div>
        </div>
      </div>
    </div>
    
    <div class="space-y-4">
      <button 
        @click="$router.push('/deposit')"
        class="w-full p-4 bg-green/20 hover:bg-green/30 rounded-xl text-green font-semibold transition-colors"
      >
        Пополнить баланс
      </button>
      
      <button 
        @click="$router.push('/withdraw')"
        class="w-full p-4 bg-red/20 hover:bg-red/30 rounded-xl text-red font-semibold transition-colors"
      >
        Вывести средства
      </button>
      
      <button 
        @click="$router.push('/bonus')"
        class="w-full p-4 bg-violet/20 hover:bg-violet/30 rounded-xl text-violet font-semibold transition-colors"
      >
        Бонусы
      </button>
      
      <button 
        @click="$router.push('/referral')"
        class="w-full p-4 bg-blue/20 hover:bg-blue/30 rounded-xl text-blue font-semibold transition-colors"
      >
        Реферальная программа
      </button>
      
      <button
        @click="$router.push('/history')"
        class="w-full p-4 bg-gray/20 hover:bg-gray/30 rounded-xl text-grayLight font-semibold transition-colors"
      >
        История игр
      </button>

      <button
        @click="$router.push('/leaderboard')"
        class="w-full p-4 bg-yellow/20 hover:bg-yellow/30 rounded-xl text-yellow font-semibold transition-colors"
      >
        🏆 Рейтинг игроков
      </button>

      <button
        @click="$router.push('/achievements')"
        class="w-full p-4 bg-purple/20 hover:bg-purple/30 rounded-xl text-purple font-semibold transition-colors"
      >
        🏅 Достижения
      </button>

      <button
        @click="$router.push('/bonus')"
        class="w-full p-4 bg-pink/20 hover:bg-pink/30 rounded-xl text-pink font-semibold transition-colors"
      >
        🎁 Бонусы и промокоды
      </button>

      <button
        @click="$router.push('/tournaments')"
        class="w-full p-4 bg-orange/20 hover:bg-orange/30 rounded-xl text-orange font-semibold transition-colors"
      >
        🏆 Турниры и события
      </button>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useUserStore } from '../stores/user'

export default {
  name: 'Profile',
  setup() {
    let userStore = null

    // Безопасная инициализация userStore
    try {
      userStore = useUserStore()
    } catch (error) {
      console.warn('UserStore not available yet, using fallback')
      userStore = { formattedBalance: '0₽', user: null }
    }

    const balance = computed(() => {
      return userStore?.formattedBalance || '0₽'
    })
    
    return {
      balance
    }
  }
}
</script>
