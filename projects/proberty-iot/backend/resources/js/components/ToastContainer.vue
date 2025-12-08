<template>
  <div class="fixed z-50 top-6 right-6 space-y-3 flex flex-col items-end">
    <transition-group name="toast-fade" tag="div">
      <div v-for="toast in toasts" :key="toast.id" :class="toastClass(toast)" class="w-80 shadow-lg rounded-lg px-4 py-3 flex items-center gap-3 animate-toast">
        <span v-if="toast.type === 'success'" class="text-green-500">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" /></svg>
        </span>
        <span v-else-if="toast.type === 'error'" class="text-red-500">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
        </span>
        <span v-else-if="toast.type === 'info'" class="text-blue-500">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01" /></svg>
        </span>
        <span v-else class="text-gray-500">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2" fill="none" /></svg>
        </span>
        <div class="flex-1 text-sm text-gray-900 dark:text-white">{{ toast.message }}</div>
        <button @click="removeToast(toast.id)" class="ml-2 text-gray-400 hover:text-gray-700 dark:hover:text-gray-200">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
        </button>
      </div>
    </transition-group>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const toasts = ref([]);

function showToast({ message, type = 'info', duration = 3500 }) {
  const id = Date.now() + Math.random();
  toasts.value.push({ id, message, type });
  setTimeout(() => removeToast(id), duration);
}

function removeToast(id) {
  toasts.value = toasts.value.filter(t => t.id !== id);
}

// Глобально доступно через window для простоты интеграции
onMounted(() => {
  window.$toast = showToast;
});

function toastClass(toast) {
  return [
    'bg-white dark:bg-gray-800',
    toast.type === 'success' && 'border-l-4 border-green-500',
    toast.type === 'error' && 'border-l-4 border-red-500',
    toast.type === 'info' && 'border-l-4 border-blue-500',
    toast.type === 'warning' && 'border-l-4 border-yellow-500',
  ];
}
</script>

<style scoped>
.toast-fade-enter-active, .toast-fade-leave-active {
  transition: all 0.3s cubic-bezier(0.4,0,0.2,1);
}
.toast-fade-enter-from, .toast-fade-leave-to {
  opacity: 0;
  transform: translateY(-20px) scale(0.95);
}
.animate-toast {
  animation: toastIn 0.4s cubic-bezier(0.4,0,0.2,1);
}
@keyframes toastIn {
  from { opacity: 0; transform: translateY(-20px) scale(0.95); }
  to { opacity: 1; transform: none; }
}
</style>
