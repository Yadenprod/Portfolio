<template>
  <div class="flex flex-col space-y-6">
    <div class="text-center">
      <h1 class="font-deftone text-3xl text-white mb-2">
        <span class="text-red">ВЫВОД</span>
      </h1>
    </div>
    
    <div class="bg-[#2c2c31] rounded-2xl p-6 space-y-6">
      <div class="space-y-4">
        <label class="text-sm font-medium text-grayLight">Сумма вывода:</label>
        <input
          v-model="amount"
          type="number"
          placeholder="Введите сумму"
          class="w-full p-4 bg-[#1b1c20] rounded-xl text-white placeholder-gray focus:outline-none focus:ring-2 focus:ring-red"
        />
      </div>
      
      <div class="grid grid-cols-3 gap-2">
        <button 
          @click="setAmount(100)"
          class="p-3 bg-[#1b1c20] rounded-lg text-sm font-medium text-grayLight hover:bg-[#35353c] transition-colors"
        >
          100₽
        </button>
        <button 
          @click="setAmount(500)"
          class="p-3 bg-[#1b1c20] rounded-lg text-sm font-medium text-grayLight hover:bg-[#35353c] transition-colors"
        >
          500₽
        </button>
        <button 
          @click="setAmount(1000)"
          class="p-3 bg-[#1b1c20] rounded-lg text-sm font-medium text-grayLight hover:bg-[#35353c] transition-colors"
        >
          1000₽
        </button>
      </div>
      
      <button
        @click="onWithdraw"
        :disabled="!canWithdraw || loading"
        class="w-full py-4 bg-red hover:bg-redHover disabled:opacity-50 disabled:cursor-not-allowed rounded-xl text-white font-semibold transition-all duration-200"
      >
        <span v-if="!loading">Вывести</span>
        <span v-else>Обработка...</span>
      </button>
    </div>
    
    <div class="bg-[#2c2c31] rounded-2xl p-6">
      <h3 class="text-lg font-semibold text-white mb-4">Доступные способы вывода:</h3>
      <div class="space-y-3">
        <div class="flex items-center justify-between p-3 bg-[#1b1c20] rounded-lg">
          <div class="flex items-center space-x-3">
            <div class="w-8 h-8 bg-blue/20 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-blue" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z"/>
              </svg>
            </div>
            <span class="text-white">Банковская карта</span>
          </div>
          <span class="text-gray text-sm">Комиссия 3%</span>
        </div>
        
        <div class="flex items-center justify-between p-3 bg-[#1b1c20] rounded-lg">
          <div class="flex items-center space-x-3">
            <div class="w-8 h-8 bg-green/20 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-green" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1"/>
              </svg>
            </div>
            <span class="text-white">QIWI</span>
          </div>
          <span class="text-gray text-sm">Комиссия 2%</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { useUserStore } from '../stores/user'
import { withdraw as apiWithdraw } from '../api/endpoints'

export default {
  name: 'Withdraw',
  setup() {
    const userStore = useUserStore()
    const amount = ref(100)
    const loading = ref(false)
    
    const canWithdraw = computed(() => {
      return amount.value >= 100 && amount.value <= userStore.balance
    })
    
    const setAmount = (value) => {
      amount.value = value
    }
    
    const onWithdraw = async () => {
      if (!canWithdraw.value || loading.value) return
      loading.value = true
      try {
        const res = await apiWithdraw(amount.value)
        const delta = Number(res?.balance_delta || -amount.value)
        userStore.updateBalance(delta)
        amount.value = 100
        alert('Заявка на вывод создана!')
      } catch (e) {
        alert(e.message)
      } finally {
        loading.value = false
      }
    }
    
    return {
      amount,
      loading,
      canWithdraw,
      setAmount,
      onWithdraw
    }
  }
}
</script>
