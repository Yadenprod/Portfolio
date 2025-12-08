<template>
  <div class="min-h-screen flex items-center justify-center bg-azot-gradient relative overflow-hidden">
    <!-- SVG background -->
    <svg class="absolute top-0 left-0 w-full h-full opacity-10 pointer-events-none select-none" viewBox="0 0 1440 320" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path fill="#0070e0" fill-opacity="0.3" d="M0,160L60,170.7C120,181,240,203,360,197.3C480,192,600,160,720,133.3C840,107,960,85,1080,101.3C1200,117,1320,171,1380,197.3L1440,224L1440,320L1380,320C1320,320,1200,320,1080,320C960,320,840,320,720,320C600,320,480,320,360,320C240,320,120,320,60,320L0,320Z" />
    </svg>
    <div class="relative z-10 w-full max-w-md p-8 bg-white/90 dark:bg-industrial-900/90 rounded-wow shadow-glow-azot flex flex-col items-center animate-wow-fade-in">
      <img src="/images/lazot.png" alt="КАО Азот" class="w-20 h-20 mb-6 drop-shadow-xl animate-wow-bounce" />
      <h2 class="text-3xl font-extrabold text-azot-700 dark:text-azot-200 mb-6 tracking-tight">Вход в систему</h2>
      <form @submit.prevent="login" class="w-full flex flex-col gap-4">
        <input 
          type="email" 
          v-model="email" 
          placeholder="Email" 
          required
          class="w-full px-4 py-3 rounded-xl border border-industrial-200 dark:border-industrial-700 bg-industrial-50 dark:bg-industrial-900 text-industrial-900 dark:text-industrial-100 focus:outline-none focus:ring-2 focus:ring-azot-500 transition"
        >
        <input 
          type="password" 
          v-model="password" 
          placeholder="Пароль" 
          required
          class="w-full px-4 py-3 rounded-xl border border-industrial-200 dark:border-industrial-700 bg-industrial-50 dark:bg-industrial-900 text-industrial-900 dark:text-industrial-100 focus:outline-none focus:ring-2 focus:ring-azot-500 transition"
        >
        <button type="submit" class="btn-primary w-full mt-2">Войти</button>
        <p v-if="error" class="text-red-600 text-center mt-2">{{ error }}</p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const email = ref('');
const password = ref('');
const error = ref(null);
const router = useRouter();

const login = async () => {
  try {
    const response = await axios.post('/api/login', {
      email: email.value,
      password: password.value
    });
    localStorage.setItem('token', response.data.token);
    localStorage.setItem('role', response.data.user.role?.name || 'operator');
    axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.token}`;
    router.push('/');
  } catch (e) {
    error.value = 'Неверный email или пароль';
  }
};
</script>

<style scoped>
.btn-primary {
  background: linear-gradient(120deg, #0070e0, #7a4ebf);
  color: #fff;
  padding: 0.9rem 1.2rem;
  border-radius: 1.5rem;
  font-weight: 600;
  box-shadow: 0 0 16px 4px #0070e0;
  transition: background 0.2s, box-shadow 0.2s, transform 0.2s;
}
.btn-primary:hover {
  background: linear-gradient(120deg, #7a4ebf, #0070e0);
  box-shadow: 0 0 32px 8px #7a4ebf;
  transform: scale(1.04);
}
</style>
