<template>
  <div class="min-h-screen flex items-center justify-center bg-azot-gradient relative overflow-hidden py-12 px-4 sm:px-8">
    <!-- SVG animated background -->
    <svg class="absolute top-0 left-0 w-full h-full opacity-10 pointer-events-none select-none animate-svg-wave" viewBox="0 0 1440 320" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path :d="svgWavePath" fill="#0070e0" fill-opacity="0.3" />
    </svg>
    <div class="absolute top-0 left-0 w-full h-full pointer-events-none select-none z-0">
      <img src="/images/lazot.png" class="absolute right-10 top-10 w-40 opacity-10 animate-spin-slow" alt="bg-logo" />
    </div>
    <transition name="fade" mode="out-in">
      <div v-if="user" key="profile" class="relative z-10 w-full max-w-lg animate-wow-fade-in">
        <div class="bg-white/90 dark:bg-industrial-900/90 rounded-wow shadow-glow-azot p-10 flex flex-col items-center card-3d" @mousemove="handleCardMouseMove($event)" @mouseleave="resetCard3D" :style="card3DStyle">
          <img :src="user.avatar_url || '/images/lazot.png'" class="w-28 h-28 rounded-full border-4 border-azot-100 dark:border-industrial-700 mb-4 shadow-glow-azot animate-wow-bounce" alt="avatar" />
          <h2 class="text-2xl font-bold text-azot-700 dark:text-azot-200 mb-2">{{ user.name }}</h2>
          <p class="text-industrial-600 dark:text-industrial-300 mb-1">{{ user.email }}</p>
          <span class="text-xs text-azot-600 dark:text-azot-300 mb-4">{{ user.role?.name }}</span>
          <input type="file" @change="onAvatarChange" accept="image/*" class="block mt-2 mb-4" />
          <div class="w-full mt-4">
            <label class="block text-sm font-medium mb-1 text-industrial-700 dark:text-industrial-200">Сменить пароль</label>
            <input v-model="password.old" type="password" placeholder="Старый пароль" class="input mb-2" />
            <input v-model="password.new" type="password" placeholder="Новый пароль" class="input mb-2" />
            <input v-model="password.confirm" type="password" placeholder="Повторите новый пароль" class="input mb-2" />
            <button @click="changePassword" class="btn-primary w-full mt-2">Сменить пароль</button>
          </div>
          <div class="w-full mt-6">
            <label class="block text-sm font-medium mb-1 text-industrial-700 dark:text-industrial-200">Настройки</label>
            <label class="flex items-center gap-2">
              <input type="checkbox" :checked="user.settings?.darkMode" @change="e => updateDarkMode(e.target.checked)" /> Тёмная тема
            </label>
          </div>
        </div>
      </div>
      <div v-else key="loader" class="flex flex-col items-center justify-center min-h-[60vh] w-full animate-wow-fade-in">
        <img src="/images/lazot.png" class="w-24 h-24 mb-6 animate-spin-slow" alt="loader-logo" />
        <div class="loader-azot"></div>
        <span class="mt-4 text-azot-600 text-lg font-semibold animate-wow-bounce">Загрузка профиля...</span>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const user = ref(null);
const password = ref({ old: '', new: '', confirm: '' });
const card3DStyle = ref({});

// SVG wave animation
const svgWavePath = ref('M0,160L60,170.7C120,181,240,203,360,197.3C480,192,600,160,720,133.3C840,107,960,85,1080,101.3C1200,117,1320,171,1380,197.3L1440,224L1440,320L1380,320C1320,320,1200,320,1080,320C960,320,840,320,720,320C600,320,480,320,360,320C240,320,120,320,60,320L0,320Z');
let wavePhase = 0;
function animateWave() {
  wavePhase += 0.03;
  const amplitude = 20;
  const frequency = 0.5;
  let path = 'M0,160';
  for (let x = 0; x <= 1440; x += 60) {
    const y = 160 + Math.sin((x / 1440) * Math.PI * 2 * frequency + wavePhase) * amplitude;
    path += `L${x},${y}`;
  }
  path += 'L1440,320L0,320Z';
  svgWavePath.value = path;
  requestAnimationFrame(animateWave);
}

function handleCardMouseMove(e) {
  const card = e.currentTarget;
  const rect = card.getBoundingClientRect();
  const x = e.clientX - rect.left;
  const y = e.clientY - rect.top;
  const centerX = rect.width / 2;
  const centerY = rect.height / 2;
  const rotateX = ((y - centerY) / centerY) * 10;
  const rotateY = ((x - centerX) / centerX) * 10;
  card3DStyle.value = {
    transform: `rotateX(${-rotateX}deg) rotateY(${rotateY}deg) scale(1.04)`,
    transition: 'transform 0.2s',
    'box-shadow': '0 8px 32px 0 rgba(0,112,224,0.25), 0 1.5px 8px 0 #7a4ebf44',
  };
}
function resetCard3D() {
  card3DStyle.value = {
    transform: 'rotateX(0deg) rotateY(0deg) scale(1)',
    transition: 'transform 0.4s',
  };
}

async function fetchUser() {
  try {
    const { data } = await axios.get('/api/me');
    user.value = data;
  } catch (e) {
    if (window.$toast) window.$toast({ message: 'Ошибка загрузки профиля', type: 'error' });
  }
}

async function onAvatarChange(e) {
  const file = e.target.files[0];
  if (!file) return;
  const formData = new FormData();
  formData.append('avatar', file);
  try {
    await axios.post('/api/profile/avatar', formData, { headers: { 'Content-Type': 'multipart/form-data' } });
    if (window.$toast) window.$toast({ message: 'Аватар обновлён', type: 'success' });
    fetchUser();
  } catch (e) {
    if (window.$toast) window.$toast({ message: 'Ошибка загрузки аватара', type: 'error' });
  }
}

async function changePassword() {
  if (password.value.new !== password.value.confirm) {
    if (window.$toast) window.$toast({ message: 'Пароли не совпадают', type: 'error' });
    return;
  }
  try {
    await axios.post('/api/profile/password', {
      old_password: password.value.old,
      new_password: password.value.new,
      new_password_confirmation: password.value.confirm
    });
    if (window.$toast) window.$toast({ message: 'Пароль изменён', type: 'success' });
    password.value = { old: '', new: '', confirm: '' };
  } catch (e) {
    if (window.$toast) window.$toast({ message: 'Ошибка смены пароля', type: 'error' });
  }
}

async function saveSettings() {
  try {
    await axios.post('/api/profile/settings', { settings: user.value.settings });
    if (window.$toast) window.$toast({ message: 'Настройки сохранены', type: 'success' });
  } catch (e) {
    if (window.$toast) window.$toast({ message: 'Ошибка сохранения настроек', type: 'error' });
  }
}

function updateDarkMode(val) {
  if (user.value.settings) user.value.settings.darkMode = val;
  saveSettings();
}

onMounted(() => {
  fetchUser();
  animateWave();
});
</script>

<style scoped>
.input {
  width: 100%;
  padding: 0.7rem;
  border: 1px solid #d1d5db;
  border-radius: 1rem;
  margin-bottom: 0.5rem;
  background: #f0f4f8;
  color: #003d80;
  font-size: 1rem;
  transition: border 0.2s, box-shadow 0.2s;
}
.input:focus {
  border-color: #0070e0;
  box-shadow: 0 0 0 2px #e6f2ff;
}
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
.card-3d {
  will-change: transform;
  perspective: 800px;
  transition: box-shadow 0.2s;
}
.animate-svg-wave {
  animation: svgWaveAnim 8s linear infinite alternate;
}
@keyframes svgWaveAnim {
  0% { opacity: 0.10; }
  100% { opacity: 0.18; }
}
.animate-spin-slow {
  animation: spin 8s linear infinite;
}
@keyframes spin {
  100% { transform: rotate(360deg); }
}
.loader-azot {
  width: 48px;
  height: 48px;
  border: 6px solid #e6f2ff;
  border-top: 6px solid #0070e0;
  border-radius: 50%;
  animation: spin 1.2s linear infinite;
  margin: 0 auto;
}
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
