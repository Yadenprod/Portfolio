<template>
  <button 
    :type="type" 
    :disabled="disabled"
    :class="[
      'relative inline-flex items-center justify-center overflow-hidden',
      'transition-all duration-300 ease-in-out',
      'rounded-wow font-medium text-center',
      'focus:outline-none focus:ring-2 focus:ring-offset-2',
      variantClasses,
      sizeClasses,
      { 'opacity-50 cursor-not-allowed': disabled },
      { 'animate-pulse': loading },
      'shadow-glow-azot',
      'bg-azot-gradient text-white',
    ]"
    @click="handleClick"
  >
    <span 
      v-if="loading" 
      class="absolute inset-0 flex items-center justify-center"
    >
      <svg 
        class="animate-spin h-5 w-5 text-white" 
        xmlns="http://www.w3.org/2000/svg" 
        fill="none" 
        viewBox="0 0 24 24"
      >
        <circle 
          class="opacity-25" 
          cx="12" 
          cy="12" 
          r="10" 
          stroke="currentColor" 
          stroke-width="4"
        ></circle>
        <path 
          class="opacity-75" 
          fill="currentColor" 
          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
        ></path>
      </svg>
    </span>
    <span 
      :class="{ 'invisible': loading }"
      class="flex items-center justify-center space-x-2"
    >
      <slot name="icon" v-if="$slots.icon"></slot>
      <slot></slot>
    </span>
    <span 
      v-if="badge" 
      class="absolute -top-2 -right-2 bg-chemical-500 text-white text-xs rounded-full px-2 py-0.5 shadow-glow-chemical"
    >
      {{ badge }}
    </span>
  </button>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  type: {
    type: String,
    default: 'button',
    validator: (value) => ['button', 'submit', 'reset'].includes(value)
  },
  variant: {
    type: String,
    default: 'primary',
    validator: (value) => [
      'primary', 'secondary', 'outline', 'ghost', 
      'danger', 'success', 'warning'
    ].includes(value)
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['xs', 'sm', 'md', 'lg', 'xl'].includes(value)
  },
  disabled: {
    type: Boolean,
    default: false
  },
  loading: {
    type: Boolean,
    default: false
  },
  badge: {
    type: [String, Number],
    default: null
  }
})

const emit = defineEmits(['click'])

const variantClasses = computed(() => {
  const baseClasses = 'shadow-md hover:shadow-lg'
  switch (props.variant) {
    case 'primary':
      return `${baseClasses} bg-primary-600 text-white hover:bg-primary-700 focus:ring-primary-500`
    case 'secondary':
      return `${baseClasses} bg-secondary-600 text-white hover:bg-secondary-700 focus:ring-secondary-500`
    case 'outline':
      return `${baseClasses} border-2 border-primary-500 text-primary-600 bg-transparent hover:bg-primary-50 focus:ring-primary-300`
    case 'ghost':
      return 'bg-transparent text-gray-700 hover:bg-gray-100 focus:ring-gray-300'
    case 'danger':
      return `${baseClasses} bg-red-600 text-white hover:bg-red-700 focus:ring-red-500`
    case 'success':
      return `${baseClasses} bg-green-600 text-white hover:bg-green-700 focus:ring-green-500`
    case 'warning':
      return `${baseClasses} bg-yellow-600 text-white hover:bg-yellow-700 focus:ring-yellow-500`
    default:
      return baseClasses
  }
})

const sizeClasses = computed(() => {
  switch (props.size) {
    case 'xs': return 'px-2 py-1 text-xs'
    case 'sm': return 'px-3 py-1.5 text-sm'
    case 'md': return 'px-4 py-2 text-base'
    case 'lg': return 'px-5 py-2.5 text-lg'
    case 'xl': return 'px-6 py-3 text-xl'
    default: return 'px-4 py-2 text-base'
  }
})

const handleClick = (event) => {
  if (!props.disabled && !props.loading) {
    emit('click', event)
  }
}
</script>

<style scoped>
button {
  position: relative;
  overflow: hidden;
  box-shadow: 0 0 16px 4px #0070e0;
}
button::after {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(120deg, transparent, rgba(255,255,255,0.3), transparent);
  transition: all 0.5s ease;
}
button:hover::after {
  left: 100%;
}
button:hover {
  filter: brightness(1.08) drop-shadow(0 0 16px #0070e0);
  transform: scale(1.04);
}
</style>
