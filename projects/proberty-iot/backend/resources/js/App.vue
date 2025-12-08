<template>
  <div :class="[$store.theme, 'min-h-screen flex bg-gray-50 dark:bg-gray-900']">
    <Sidebar v-if="!sidebarMobileOpen || isDesktop" />
    <transition name="fade">
      <div v-if="sidebarMobileOpen && !isDesktop" class="fixed inset-0 z-40 bg-black bg-opacity-40 md:hidden" @click="sidebarMobileOpen = false"></div>
    </transition>
    <transition name="slide">
      <Sidebar v-if="sidebarMobileOpen && !isDesktop" class="fixed z-50 top-0 left-0 h-full shadow-xl md:hidden" />
    </transition>
    <div class="flex-1 flex flex-col min-h-screen">
      <Topbar :theme="$store.theme" @toggleSidebar="sidebarMobileOpen = !sidebarMobileOpen" @toggleTheme="$store.toggleTheme()" @logout="logout" />
      <main class="flex-1 p-4 md:p-8 bg-gray-50 dark:bg-gray-900">
        <router-view />
      </main>
    </div>
    <ToastContainer />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import Sidebar from './components/Sidebar.vue';
import Topbar from './components/Topbar.vue';
import ToastContainer from './components/ToastContainer.vue';
const router = useRouter();
const sidebarMobileOpen = ref(false);
const isDesktop = computed(() => window.innerWidth >= 768);
const $store = reactive({
  theme: localStorage.getItem('theme') || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'),
  toggleTheme() {
    this.theme = this.theme === 'dark' ? 'light' : 'dark';
    document.documentElement.classList.toggle('dark', this.theme === 'dark');
    localStorage.setItem('theme', this.theme);
  }
});
onMounted(() => {
  document.documentElement.classList.toggle('dark', $store.theme === 'dark');
  window.addEventListener('resize', () => { if (isDesktop.value) sidebarMobileOpen.value = false; });
});
function logout() {
  localStorage.removeItem('token');
  localStorage.removeItem('role');
  router.push('/login');
}
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
.slide-enter-active, .slide-leave-active { transition: transform 0.2s; }
.slide-enter-from { transform: translateX(-100%); }
.slide-leave-to { transform: translateX(-100%); }
</style>
