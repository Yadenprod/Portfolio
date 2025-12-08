<template>
  <Teleport to="body">
    <Transition 
      enter-active-class="duration-500 ease-out animate-fade-in"
      enter-from-class="opacity-0 scale-95"
      enter-to-class="opacity-100 scale-100"
      leave-active-class="duration-300 ease-in"
      leave-from-class="opacity-100 scale-100"
      leave-to-class="opacity-0 scale-95"
    >
      <div 
        v-if="modelValue" 
        class="fixed inset-0 z-50 flex items-center justify-center overflow-x-hidden overflow-y-auto outline-none focus:outline-none"
      >
        <div 
          class="fixed inset-0 bg-black opacity-50" 
          @click="closeModal"
        ></div>
        <div 
          :class="[
            'relative w-auto max-w-3xl mx-auto my-6',
            'transform transition-all duration-500 ease-in-out',
            'scale-95 hover:scale-100',
            sizeClasses
          ]"
        >
          <div 
            :class="[
              'bg-white/95 dark:bg-industrial-900/95 rounded-wow shadow-glow-industrial',
              'border border-industrial-200 dark:border-industrial-700',
              'flex flex-col backdrop-blur-xl'
            ]"
          >
            <!-- Заголовок -->
            <div 
              v-if="$slots.header" 
              class="flex items-center justify-between p-5 border-b border-industrial-200 dark:border-industrial-700 rounded-t-wow bg-azot-gradient bg-clip-text text-transparent"
            >
              <h3 class="text-xl font-semibold text-industrial-900 dark:text-white">
                <slot name="header"></slot>
              </h3>
              <button 
                @click="closeModal" 
                class="text-industrial-400 hover:text-industrial-600 dark:hover:text-industrial-200 transition"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <!-- Контент -->
            <div 
              :class="[
                'relative p-6 flex-auto',
                { 'opacity-50 pointer-events-none': loading }
              ]"
            >
              <div v-if="loading" class="absolute inset-0 flex items-center justify-center">
                <div class="animate-spin w-10 h-10 border-4 border-azot-500 border-t-transparent rounded-full"></div>
              </div>
              <slot></slot>
            </div>
            <!-- Футер -->
            <div 
              v-if="$slots.footer" 
              class="flex items-center justify-end p-5 border-t border-industrial-200 dark:border-industrial-700 rounded-b-wow space-x-3"
            >
              <slot name="footer"></slot>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { defineProps, defineEmits, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg', 'xl', 'full'].includes(value)
  },
  loading: {
    type: Boolean,
    default: false
  },
  closeOnBackdrop: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['update:modelValue', 'close'])

const sizeClasses = {
  sm: 'max-w-md w-full',
  md: 'max-w-2xl w-full',
  lg: 'max-w-4xl w-full',
  xl: 'max-w-6xl w-full',
  full: 'w-screen h-screen'
}

const closeModal = () => {
  if (props.closeOnBackdrop) {
    emit('update:modelValue', false)
    emit('close')
  }
}

// Блокировка скролла при открытом модальном окне
watch(() => props.modelValue, (newValue) => {
  if (newValue) {
    document.body.style.overflow = 'hidden'
  } else {
    document.body.style.overflow = 'auto'
  }
})
</script>

<style scoped>
.modal-backdrop {
  background-color: rgba(0, 0, 0, 0.5);
}
</style>
