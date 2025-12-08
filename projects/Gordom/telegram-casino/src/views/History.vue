<template>
  <div class="flex flex-col space-y-6">
    <div class="text-center">
      <h1 class="font-deftone text-3xl text-white mb-2">
        <span class="text-violet">ИСТОРИЯ</span>
      </h1>
    </div>
    
    <div class="bg-[#2c2c31] rounded-2xl p-6 space-y-4">
      <h3 class="text-lg font-semibold text-white">Последние игры:</h3>
      
      <div class="space-y-3">
        <div 
          v-for="game in games" 
          :key="game.id"
          class="flex items-center justify-between p-3 bg-[#1b1c20] rounded-lg"
        >
          <div class="flex items-center space-x-3">
            <div class="w-8 h-8 rounded-lg flex items-center justify-center" :class="game.win ? 'bg-green/20' : 'bg-red/20'">
              <svg class="w-4 h-4" :class="game.win ? 'text-green' : 'text-red'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 3H5a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2V5a2 2 0 00-2-2z"/>
              </svg>
            </div>
            <div>
              <div class="text-sm font-medium text-white">{{ game.game }}</div>
              <div class="text-xs text-gray">{{ game.time }}</div>
            </div>
          </div>
          <div class="text-right">
            <div class="text-sm font-medium" :class="game.win ? 'text-green' : 'text-red'">
              {{ game.win ? '+' : '-' }}{{ game.amount }}
            </div>
            <div class="text-xs text-gray">x{{ game.multiplier }}</div>
          </div>
        </div>
      </div>
      
      <div v-if="games.length === 0" class="text-center py-8">
        <p class="text-grayLight">История игр пуста</p>
        <p class="text-gray text-sm mt-2">Сыграйте в любую игру!</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { getHistory } from '../api/endpoints'

export default {
  name: 'History',
  setup() {
    const games = ref([])
    
    onMounted(async () => {
      try {
        const data = await getHistory(25)
        games.value = data.items || []
      } catch {
        games.value = []
      }
    })
    
    return {
      games
    }
  }
}
</script>
