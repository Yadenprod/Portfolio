<template>
  <div class="min-h-screen bg-azot-gradient flex flex-col items-center justify-start py-12 px-4 sm:px-8 relative overflow-hidden">
    <!-- SVG animated background -->
    <svg class="absolute top-0 left-0 w-full h-full opacity-10 pointer-events-none select-none animate-svg-wave" viewBox="0 0 1440 320" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path :d="svgWavePath" fill="#0070e0" fill-opacity="0.3" />
    </svg>
    <div class="absolute top-0 left-0 w-full h-full pointer-events-none select-none z-0">
      <img src="/images/lazot.png" class="absolute right-10 top-10 w-40 opacity-10 animate-spin-slow" alt="bg-logo" />
    </div>
    <transition name="fade" mode="out-in">
      <div v-if="!loading" key="sensors" class="relative z-10 w-full max-w-6xl animate-wow-fade-in">
        <div class="flex flex-col md:flex-row md:items-center md:justify-between mb-10 gap-6">
          <h1 class="text-4xl md:text-5xl font-extrabold text-azot-700 dark:text-azot-200 mb-2 tracking-tight animate-wow-fade-in">Датчики</h1>
          <button @click="openModal('create')" class="btn-primary">Добавить</button>
        </div>
        <div class="bg-white/90 dark:bg-industrial-900/90 rounded-wow shadow-glow-azot p-8 animate-wow-fade-in">
          <div class="mb-4 flex flex-col md:flex-row gap-2 md:gap-4 items-center">
            <input v-model="search" type="text" placeholder="Поиск по типу..." class="input" />
            <button @click="exportCSV" class="btn-primary">Экспорт CSV</button>
          </div>
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-industrial-200 dark:divide-industrial-700 rounded-xl overflow-hidden">
              <thead class="bg-industrial-50 dark:bg-industrial-900">
                <tr>
                  <th class="px-4 py-2 text-left text-xs font-medium text-industrial-500 dark:text-industrial-400 uppercase">Тип</th>
                  <th class="px-4 py-2 text-left text-xs font-medium text-industrial-500 dark:text-industrial-400 uppercase">Оборудование</th>
                  <th class="px-4 py-2 text-left text-xs font-medium text-industrial-500 dark:text-industrial-400 uppercase">Статус</th>
                  <th class="px-4 py-2"></th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in filteredSensors" :key="item?.id ?? Math.random()" class="hover:bg-azot-50 dark:hover:bg-industrial-800 transition animate-wow-fade-in">
                  <td class="px-4 py-2 text-industrial-900 dark:text-industrial-100 font-medium">{{ item?.type ?? '-' }}</td>
                  <td class="px-4 py-2 text-industrial-500 dark:text-industrial-300">{{ item?.equipment?.name ?? '-' }}</td>
                  <td class="px-4 py-2">
                    <span :class="getStatusClass(item?.status)">{{ item?.status ?? '-' }}</span>
                  </td>
                  <td class="px-4 py-2 flex gap-2">
                    <button @click="openModal('edit', item)" class="text-azot-600 hover:underline">Редактировать</button>
                    <button @click="remove(item?.id)" class="text-red-600 hover:underline">Удалить</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-if="!filteredSensors.length" class="text-center text-industrial-400 py-8">Нет датчиков</div>
          <div v-if="error" class="text-center text-red-500 py-4">{{ error }}</div>
        </div>
        <EntityModal :open="modalOpen" :title="modalMode === 'create' ? 'Добавить датчик' : 'Редактировать датчик'" :onClose="closeModal" :onSave="save">
          <form @submit.prevent="save">
            <div class="mb-4">
              <label class="block text-industrial-700 dark:text-industrial-200 mb-1">Тип</label>
              <input v-model="form.type" type="text" required class="input" />
            </div>
            <div class="mb-4">
              <label class="block text-industrial-700 dark:text-industrial-200 mb-1">Оборудование</label>
              <select v-model="form.equipment_id" required class="input">
                <option v-for="eq in equipment" :key="eq.id" :value="eq.id">{{ eq.name }}</option>
              </select>
            </div>
            <div class="mb-6">
              <label class="block text-industrial-700 dark:text-industrial-200 mb-1">Статус</label>
              <select v-model="form.status" required class="input">
                <option value="active">Активен</option>
                <option value="inactive">Неактивен</option>
                <option value="error">Ошибка</option>
              </select>
            </div>
          </form>
        </EntityModal>
      </div>
      <div v-else key="loader" class="flex flex-col items-center justify-center min-h-[60vh] w-full animate-wow-fade-in">
        <img src="/images/lazot.png" class="w-24 h-24 mb-6 animate-spin-slow" alt="loader-logo" />
        <div class="loader-azot"></div>
        <span class="mt-4 text-azot-600 text-lg font-semibold animate-wow-bounce">Загрузка датчиков...</span>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';
import EntityModal from './partials/EntityModal.vue';

const sensors = ref([]);
const equipment = ref([]);
const search = ref('');
const modalOpen = ref(false);
const modalMode = ref('create');
const form = ref({ id: null, type: '', equipment_id: '', status: 'active' });
const loading = ref(true);
const error = ref('');

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

const fetchSensors = async () => {
  loading.value = true;
  error.value = '';
  try {
    const { data } = await axios.get('/api/sensors');
    sensors.value = data;
  } catch (e) {
    error.value = 'Ошибка загрузки датчиков';
    if (window.$toast) window.$toast({ message: error.value, type: 'error' });
    sensors.value = [];
  }
  loading.value = false;
};
const fetchEquipment = async () => {
  try {
    const { data } = await axios.get('/api/equipment');
    equipment.value = data;
  } catch (e) {
    if (window.$toast) window.$toast({ message: 'Ошибка загрузки оборудования', type: 'error' });
    equipment.value = [];
  }
};
const filteredSensors = computed(() => {
  if (!search.value) return sensors.value;
  return sensors.value.filter(s => s.type.toLowerCase().includes(search.value.toLowerCase()));
});
function openModal(mode, item = null) {
  modalMode.value = mode;
  if (mode === 'edit' && item) {
    form.value = { ...item };
  } else {
    form.value = { id: null, type: '', equipment_id: '', status: 'active' };
  }
  modalOpen.value = true;
}
function closeModal() {
  modalOpen.value = false;
}
async function save() {
  try {
    if (modalMode.value === 'create') {
      await axios.post('/api/sensors', form.value);
    } else {
      await axios.put(`/api/sensors/${form.value.id}`, form.value);
    }
    await fetchSensors();
    closeModal();
  } catch (e) {
    if (window.$toast) window.$toast({ message: 'Ошибка сохранения', type: 'error' });
  }
}
async function remove(id) {
  try {
    await axios.delete(`/api/sensors/${id}`);
    await fetchSensors();
  } catch (e) {
    if (window.$toast) window.$toast({ message: 'Ошибка удаления', type: 'error' });
  }
}
function getStatusClass(status) {
  return {
    'inline-block px-2 py-1 rounded text-xs font-semibold bg-green-100 text-green-700': status === 'active',
    'inline-block px-2 py-1 rounded text-xs font-semibold bg-yellow-100 text-yellow-700': status === 'inactive',
    'inline-block px-2 py-1 rounded text-xs font-semibold bg-red-100 text-red-700': status === 'error',
  };
}
function exportCSV() {
  const rows = [
    ['ID', 'Тип', 'Оборудование', 'Статус'],
    ...filteredSensors.value.map(s => [s.id, s.type, s.equipment?.name || '', s.status])
  ];
  const csv = rows.map(r => r.map(v => '"' + String(v).replace(/"/g, '""') + '"').join(',')).join('\n');
  const blob = new Blob([csv], { type: 'text/csv' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'sensors.csv';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}
onMounted(() => {
  fetchSensors();
  fetchEquipment();
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
