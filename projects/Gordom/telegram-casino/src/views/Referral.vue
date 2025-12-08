<template>
  <div class="flex flex-col space-y-6">
    <div class="text-center">
      <h1 class="font-deftone text-3xl text-white mb-2">
        <span class="text-violet">РЕФЕРАЛЫ</span>
      </h1>
    </div>
    
    <div class="bg-[#2c2c31] rounded-2xl p-6 space-y-4">
      <h3 class="text-lg font-semibold text-white">Ваша реферальная ссылка:</h3>
      
      <div class="flex space-x-2">
        <input
          :value="referralLink"
          type="text"
          readonly
          class="flex-1 p-3 bg-[#1b1c20] rounded-lg text-white"
        />
        <button
          @click="copyLink"
          class="px-4 py-3 bg-violet hover:bg-violetHover rounded-lg text-white font-medium transition-colors"
        >
          Копировать
        </button>
      </div>
      
      <p class="text-grayLight text-sm">Приглашайте друзей и получайте 10% с их пополнений!</p>
    </div>
    
    <div class="bg-[#2c2c31] rounded-2xl p-6 space-y-4">
      <h3 class="text-lg font-semibold text-white">Статистика:</h3>
      
      <div class="grid grid-cols-2 gap-4">
        <div class="text-center p-4 bg-[#1b1c20] rounded-lg">
          <div class="text-2xl font-bold text-violet mb-1">{{ stats.invited }}</div>
          <div class="text-xs text-gray">Рефералов</div>
        </div>
        <div class="text-center p-4 bg-[#1b1c20] rounded-lg">
          <div class="text-2xl font-bold text-green mb-1">{{ stats.earnings }}₽</div>
          <div class="text-xs text-gray">Заработано</div>
        </div>
      </div>
    </div>
    
    <div class="bg-[#2c2c31] rounded-2xl p-6 space-y-4">
      <h3 class="text-lg font-semibold text-white">Ваши рефералы:</h3>
      
      <div class="text-center py-8">
        <p class="text-grayLight">У вас пока нет рефералов</p>
        <p class="text-gray text-sm mt-2">Поделитесь ссылкой с друзьями!</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '../stores/user'
import { getReferralStats } from '../api/endpoints'

export default {
  name: 'Referral',
  setup() {
    const userStore = useUserStore()
    const stats = ref({ invited: 0, earnings: 0 })

    const referralCode = computed(() => userStore.referralCode || localStorage.getItem('ref') || 'ref')
    const referralLink = computed(() => `https://t.me/your_bot?start=${referralCode.value}`)

    const copyLink = () => {
      navigator.clipboard.writeText(referralLink.value)
      alert('Ссылка скопирована!')
    }

    onMounted(async () => {
      try {
        const data = await getReferralStats()
        stats.value = { invited: data.invited || 0, earnings: data.earnings || 0 }
      } catch {}
    })

    return {
      referralLink,
      stats,
      copyLink
    }
  }
}
</script>
