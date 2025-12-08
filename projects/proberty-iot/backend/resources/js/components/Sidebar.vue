<template>
  <aside class="w-72 bg-azot-gradient dark:bg-industrial-900 border-r border-industrial-200 dark:border-industrial-700 flex-shrink-0 hidden md:flex flex-col min-h-screen shadow-glow-industrial rounded-wow animate-fade-in">
    <div class="h-20 flex items-center justify-center border-b border-industrial-200 dark:border-industrial-700 px-4 bg-white/80 dark:bg-industrial-800/80 rounded-t-wow">
      <div class="flex items-center gap-4">
        <img src="/images/lazot.png" alt="АЗОТ Логотип" class="w-12 h-12 object-contain rounded-industrial-md shadow-glow-azot">
        <span class="text-2xl font-bold text-azot-600 dark:text-azot-300 tracking-wide uppercase drop-shadow-lg">
          АЗОТ
        </span>
      </div>
    </div>
    <nav class="flex-1 px-4 py-6 space-y-2">
      <router-link 
        v-for="item in nav" 
        :key="item.to" 
        :to="item.to" 
        class="flex items-center px-4 py-2.5 rounded-industrial-md text-industrial-700 dark:text-industrial-200 hover:bg-white/40 dark:hover:bg-industrial-800/60 transition group font-semibold shadow-industrial-soft"
        active-class="bg-azot-100 dark:bg-industrial-700 text-azot-700 dark:text-azot-300 font-bold shadow-glow-azot"
      >
        <component 
          :is="item.icon" 
          class="w-6 h-6 mr-3 text-industrial-500 dark:text-industrial-300 group-hover:text-azot-600 dark:group-hover:text-azot-300 transition"
        />
        <span>{{ item.label }}</span>
      </router-link>
    </nav>
    <div class="p-4 border-t border-industrial-200 dark:border-industrial-700 bg-industrial-50/80 dark:bg-industrial-800/80 rounded-b-wow">
      <div class="bg-azot-100 dark:bg-industrial-900 rounded-industrial-lg p-3 text-center shadow-industrial-soft">
        <p class="text-sm text-industrial-600 dark:text-industrial-300 mb-1">
          Система мониторинга
        </p>
        <span class="text-xs font-technical text-azot-600 dark:text-azot-400">v1.0.0 Industrial</span>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { 
  HomeIcon, 
  CpuChipIcon, 
  ChartBarIcon, 
  ClipboardDocumentListIcon, 
  UserCircleIcon 
} from '@heroicons/vue/24/outline'

const nav = [
  { to: '/', label: 'Главная', icon: HomeIcon },
  { to: '/equipment', label: 'Оборудование', icon: CpuChipIcon },
  { to: '/sensors', label: 'Датчики', icon: ChartBarIcon },
  { to: '/maintenance', label: 'Заявки', icon: ClipboardDocumentListIcon },
  { to: '/profile', label: 'Профиль', icon: UserCircleIcon },
]
</script>

<style scoped>
.router-link-active {
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 112, 224, 0.1);
}
</style>
