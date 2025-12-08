<template>
  <div 
    :class="[
      'bg-white/90 dark:bg-industrial-900/90 rounded-wow shadow-industrial-medium',
      'border border-industrial-200 dark:border-industrial-700',
      'transition-all duration-300 ease-in-out',
      'hover:shadow-glow-industrial hover:-translate-y-1',
      'backdrop-blur-lg',
      additionalClasses
    ]"
  >
    <div 
      v-if="$slots.header" 
      class="px-6 py-4 border-b border-industrial-200 dark:border-industrial-700 flex items-center justify-between bg-azot-gradient bg-clip-text text-transparent"
    >
      <slot name="header"></slot>
      <button 
        v-if="closable" 
        @click="$emit('close')" 
        class="text-industrial-400 hover:text-industrial-600 dark:hover:text-industrial-200 transition"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>
    <div 
      :class="[
        'p-6',
        { 'opacity-50 pointer-events-none': loading }
      ]"
    >
      <div v-if="loading" class="absolute inset-0 flex items-center justify-center">
        <div class="animate-spin w-8 h-8 border-4 border-azot-500 border-t-transparent rounded-full"></div>
      </div>
      <slot></slot>
    </div>
    <div 
      v-if="$slots.footer" 
      class="px-6 py-4 border-t border-industrial-200 dark:border-industrial-700 flex items-center justify-between"
    >
      <slot name="footer"></slot>
    </div>
    <div 
      v-if="badge" 
      class="absolute top-4 right-4 bg-chemical-500 text-white text-xs font-bold px-3 py-1 rounded-full shadow-glow-chemical"
    >
      {{ badge }}
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
  closable: {
    type: Boolean,
    default: false
  },
  loading: {
    type: Boolean,
    default: false
  },
  badge: {
    type: String,
    default: null
  },
  additionalClasses: {
    type: [String, Array, Object],
    default: ''
  }
})

const emit = defineEmits(['close'])
</script>

<style scoped>
.card-hover-effect {
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}
.card-hover-effect:hover {
  box-shadow: 0 14px 28px #627d98, 0 10px 10px #0070e0;
  transform: translateY(-5px) scale(1.03);
}
</style>
