<template>
  <div class="min-h-screen bg-azot-gradient flex flex-col items-center justify-start py-12 px-4 sm:px-8 relative overflow-hidden">
    <!-- SVG animated background pattern -->
    <svg class="absolute top-0 left-0 w-full h-full opacity-10 pointer-events-none select-none animate-svg-wave" viewBox="0 0 1440 320" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path :d="svgWavePath" fill="#0070e0" fill-opacity="0.3" />
    </svg>
    <div class="absolute top-0 left-0 w-full h-full pointer-events-none select-none z-0">
      <img src="/images/lazot.png" class="absolute right-10 top-10 w-40 opacity-10 animate-spin-slow" alt="bg-logo" />
    </div>
    <transition name="fade" mode="out-in">
      <div v-if="!loading" key="dashboard" class="relative z-10 w-full max-w-7xl animate-wow-fade-in">
        <!-- Header -->
        <div class="flex flex-col md:flex-row md:items-center md:justify-between mb-10 gap-6">
          <div>
            <h1 class="text-4xl md:text-5xl font-extrabold text-azot-700 dark:text-azot-200 mb-2 tracking-tight animate-wow-fade-in">IIoT Dashboard</h1>
            <p class="text-lg md:text-2xl text-industrial-700 dark:text-industrial-200 animate-wow-fade-in">
              Корпоративная платформа мониторинга и управления для КАО «Азот»
            </p>
          </div>
          <img src="/images/lazot.png" alt="КАО Азот" class="w-28 h-28 md:w-36 md:h-36 drop-shadow-xl animate-wow-bounce" />
        </div>
        <!-- Statistic Cards -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mb-10">
          <div class="bg-white/90 dark:bg-industrial-900/90 rounded-wow shadow-glow-azot p-8 flex flex-col items-center wow-glow animate-wow-fade-in card-3d" @mousemove="handleCardMouseMove($event, 0)" @mouseleave="resetCard3D(0)" :style="card3DStyles[0]">
            <span class="text-4xl font-bold text-azot-600 dark:text-azot-200">{{ equipmentStats?.total ?? '-' }}</span>
            <span class="text-industrial-600 dark:text-industrial-300 mt-2">Всего оборудования</span>
          </div>
          <div class="bg-white/90 dark:bg-industrial-900/90 rounded-wow shadow-glow-industrial p-8 flex flex-col items-center wow-glow-industrial animate-wow-fade-in card-3d" @mousemove="handleCardMouseMove($event, 1)" @mouseleave="resetCard3D(1)" :style="card3DStyles[1]">
            <span class="text-4xl font-bold text-green-600">{{ equipmentStats?.working ?? '-' }}</span>
            <span class="text-industrial-600 dark:text-industrial-300 mt-2">Исправно</span>
          </div>
          <div class="bg-white/90 dark:bg-industrial-900/90 rounded-wow shadow-glow-chemical p-8 flex flex-col items-center wow-glow-chemical animate-wow-fade-in card-3d" @mousemove="handleCardMouseMove($event, 2)" @mouseleave="resetCard3D(2)" :style="card3DStyles[2]">
            <span class="text-4xl font-bold text-red-600">{{ equipmentStats?.critical ?? '-' }}</span>
            <span class="text-industrial-600 dark:text-industrial-300 mt-2">Критические</span>
          </div>
        </div>
        <!-- Charts -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-10">
          <div class="bg-white/90 dark:bg-industrial-900/90 rounded-wow shadow-glow-azot p-8 animate-wow-fade-in">
            <h2 class="text-xl font-semibold text-azot-700 dark:text-azot-200 mb-4">Статус оборудования</h2>
            <canvas ref="equipmentStatusChart" class="w-full h-64 animate-chart-fade"></canvas>
          </div>
          <div class="bg-white/90 dark:bg-industrial-900/90 rounded-wow shadow-glow-chemical p-8 animate-wow-fade-in">
            <h2 class="text-xl font-semibold text-azot-700 dark:text-azot-200 mb-4">Тренды датчиков</h2>
            <canvas ref="sensorTrendChart" class="w-full h-64 animate-chart-fade"></canvas>
          </div>
        </div>
        <!-- Weather & Simulated Sensor -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-10">
          <div class="bg-white/90 dark:bg-industrial-900/90 rounded-wow shadow-glow-industrial p-8 flex flex-col items-center animate-wow-fade-in">
            <span class="text-lg font-semibold text-industrial-900 dark:text-industrial-100 mb-2">Погода</span>
            <div v-if="weatherLoading" class="h-10 w-32 bg-industrial-100 dark:bg-industrial-800 rounded animate-skeleton mb-2"></div>
            <div v-else-if="weather">
              <span class="text-2xl font-bold">{{ weather.temperature }}°C</span>
              <span class="block text-industrial-600 dark:text-industrial-300">{{ weather.description }}</span>
            </div>
            <div v-else class="text-red-500">Ошибка загрузки погоды</div>
          </div>
          <div class="bg-white/90 dark:bg-industrial-900/90 rounded-wow shadow-glow-azot p-8 flex flex-col items-center animate-wow-fade-in">
            <span class="text-lg font-semibold text-industrial-900 dark:text-industrial-100 mb-2">Датчик (эмуляция)</span>
            <div v-if="simSensorLoading" class="h-10 w-32 bg-industrial-100 dark:bg-industrial-800 rounded animate-skeleton mb-2"></div>
            <div v-else-if="simSensor">
              <span class="text-2xl font-bold">{{ simSensor.value }} {{ simSensor.unit }}</span>
              <span class="block text-industrial-600 dark:text-industrial-300">Тип: {{ simSensor.type }}</span>
            </div>
            <div v-else class="text-red-500">Ошибка эмуляции датчика</div>
            <button @click="fetchSimSensor" class="mt-4 btn-primary">Обновить</button>
          </div>
        </div>
        <!-- Maintenance Requests Table -->
        <div class="bg-white/90 dark:bg-industrial-900/90 rounded-wow shadow-glow-industrial p-8 mt-6 animate-wow-fade-in">
          <h2 class="text-xl font-semibold text-azot-700 dark:text-azot-200 mb-4">Заявки на обслуживание</h2>
          <transition-group name="fade" tag="tbody">
            <table class="min-w-full divide-y divide-industrial-200 dark:divide-industrial-700 rounded-xl overflow-hidden">
              <thead class="bg-industrial-50 dark:bg-industrial-900">
                <tr>
                  <th class="px-4 py-2 text-left text-xs font-medium text-industrial-500 dark:text-industrial-400 uppercase">Оборудование</th>
                  <th class="px-4 py-2 text-left text-xs font-medium text-industrial-500 dark:text-industrial-400 uppercase">Статус</th>
                  <th class="px-4 py-2 text-left text-xs font-medium text-industrial-500 dark:text-industrial-400 uppercase">Дата</th>
                  <th class="px-4 py-2"></th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="request in maintenanceRequests" :key="request?.id ?? request?.equipment?.id ?? Math.random()" class="hover:bg-azot-50 dark:hover:bg-industrial-800 transition animate-wow-fade-in">
                  <td class="px-4 py-2 text-industrial-900 dark:text-industrial-100 font-medium">{{ request?.equipment?.name ?? '-' }}</td>
                  <td class="px-4 py-2">
                    <span :class="getStatusClass(request?.status)">{{ request?.status ?? '-' }}</span>
                  </td>
                  <td class="px-4 py-2 text-industrial-500 dark:text-industrial-300">{{ formatDate(request?.created_at) }}</td>
                  <td class="px-4 py-2">
                    <button class="text-azot-600 hover:underline">Подробнее</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </transition-group>
          <div v-if="!maintenanceRequests.length && !loading" class="text-center text-industrial-400 py-8">Нет заявок</div>
        </div>
      </div>
      <div v-else key="loader" class="flex flex-col items-center justify-center min-h-[60vh] w-full animate-wow-fade-in">
        <img src="/images/lazot.png" class="w-24 h-24 mb-6 animate-spin-slow" alt="loader-logo" />
        <div class="loader-azot"></div>
        <span class="mt-4 text-azot-600 text-lg font-semibold animate-wow-bounce">Загрузка данных...</span>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import axios from 'axios';
import Chart from 'chart.js/auto';

const equipmentStatusChart = ref(null);
const sensorTrendChart = ref(null);
const maintenanceRequests = ref([]);
const loading = ref(true);

const equipmentStats = ref({ total: 0, working: 0, critical: 0 });
const weather = ref(null);
const weatherLoading = ref(true);
const simSensor = ref(null);
const simSensorLoading = ref(true);

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

// 3D card hover effect
const card3DStyles = ref([{}, {}, {}]);
function handleCardMouseMove(e, idx) {
  const card = e.currentTarget;
  const rect = card.getBoundingClientRect();
  const x = e.clientX - rect.left;
  const y = e.clientY - rect.top;
  const centerX = rect.width / 2;
  const centerY = rect.height / 2;
  const rotateX = ((y - centerY) / centerY) * 10;
  const rotateY = ((x - centerX) / centerX) * 10;
  card3DStyles.value[idx] = {
    transform: `rotateX(${-rotateX}deg) rotateY(${rotateY}deg) scale(1.04)`,
    transition: 'transform 0.2s',
    'box-shadow': '0 8px 32px 0 rgba(0,112,224,0.25), 0 1.5px 8px 0 #7a4ebf44',
  };
}
function resetCard3D(idx) {
  card3DStyles.value[idx] = {
    transform: 'rotateX(0deg) rotateY(0deg) scale(1)',
    transition: 'transform 0.4s',
  };
}

const fetchMaintenanceRequests = async () => {
  loading.value = true;
  try {
    const response = await axios.get('/api/maintenance-requests');
    maintenanceRequests.value = response.data;
  } catch (error) {
    maintenanceRequests.value = [];
    if (window.$toast) window.$toast({ message: 'Ошибка загрузки заявок', type: 'error' });
  }
  loading.value = false;
};

const fetchEquipmentStats = async () => {
  equipmentStats.value = { total: 42, working: 36, critical: 2 };
};

const fetchWeather = async () => {
  weatherLoading.value = true;
  try {
    const { data } = await axios.get('/api/external/weather');
    if (data.current_weather) {
      weather.value = {
        temperature: data.current_weather.temperature,
        description: 'Ветер: ' + data.current_weather.windspeed + ' м/с',
      };
    } else {
      weather.value = { temperature: '-', description: 'Нет данных' };
    }
  } catch (e) {
    weather.value = null;
    if (window.$toast) window.$toast({ message: 'Ошибка загрузки погоды', type: 'error' });
  }
  weatherLoading.value = false;
};

const fetchSimSensor = async () => {
  simSensorLoading.value = true;
  try {
    const { data } = await axios.get('/api/external/simulate-sensor');
    simSensor.value = data;
  } catch (e) {
    simSensor.value = null;
    if (window.$toast) window.$toast({ message: 'Ошибка эмуляции датчика', type: 'error' });
  }
  simSensorLoading.value = false;
};

const renderEquipmentStatusChart = () => {
  new Chart(equipmentStatusChart.value, {
    type: 'pie',
    data: {
      labels: ['Исправное', 'Требует внимания', 'Критическое'],
      datasets: [{
        data: [36, 4, 2],
        backgroundColor: ['#22c55e', '#f59e42', '#ef4444'],
        borderWidth: 4,
        borderColor: '#fff',
        hoverOffset: 16,
        hoverBorderColor: '#0070e0',
        hoverBorderWidth: 6,
      }]
    },
    options: {
      responsive: true,
      animation: {
        animateRotate: true,
        animateScale: true,
        duration: 1800,
        easing: 'easeOutElastic',
      },
      plugins: {
        legend: { labels: { color: '#374151', font: { size: 16, weight: 'bold' } } }
      }
    }
  });
};

const renderSensorTrendChart = () => {
  new Chart(sensorTrendChart.value, {
    type: 'line',
    data: {
      labels: ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн'],
      datasets: [
        {
          label: 'Температура',
          data: [20, 22, 25, 23, 26, 24],
          borderColor: '#3b82f6',
          backgroundColor: 'rgba(59,130,246,0.1)',
          tension: 0.4,
          pointRadius: 6,
          pointHoverRadius: 12,
          pointBackgroundColor: '#0070e0',
          pointBorderColor: '#fff',
          fill: true,
        },
        {
          label: 'Давление',
          data: [980, 990, 1000, 1010, 1005, 1015],
          borderColor: '#ef4444',
          backgroundColor: 'rgba(239,68,68,0.1)',
          tension: 0.4,
          pointRadius: 6,
          pointHoverRadius: 12,
          pointBackgroundColor: '#7a4ebf',
          pointBorderColor: '#fff',
          fill: true,
        }
      ]
    },
    options: {
      responsive: true,
      animation: {
        duration: 2000,
        easing: 'easeInOutQuart',
      },
      plugins: {
        legend: { labels: { color: '#374151', font: { size: 16, weight: 'bold' } } }
      },
      scales: {
        y: { beginAtZero: false, ticks: { color: '#6b7280', font: { size: 14 } } },
        x: { ticks: { color: '#6b7280', font: { size: 14 } } }
      }
    }
  });
};

const getStatusClass = (status) => {
  return {
    'inline-block px-2 py-1 rounded text-xs font-semibold bg-green-100 text-green-700': status === 'completed',
    'inline-block px-2 py-1 rounded text-xs font-semibold bg-yellow-100 text-yellow-700': status === 'pending',
    'inline-block px-2 py-1 rounded text-xs font-semibold bg-red-100 text-red-700': status === 'critical',
    'inline-block px-2 py-1 rounded text-xs font-semibold bg-blue-100 text-blue-700': status === 'in_progress',
  };
};

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('ru-RU');
};

onMounted(() => {
  fetchEquipmentStats();
  fetchMaintenanceRequests();
  fetchWeather();
  fetchSimSensor();
  setTimeout(() => {
    renderEquipmentStatusChart();
    renderSensorTrendChart();
    animateWave();
  }, 500);
});
</script>

<style scoped>
.btn-primary {
  background: linear-gradient(120deg, #0070e0, #7a4ebf);
  color: #fff;
  padding: 0.5rem 1.2rem;
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
.animate-skeleton {
  background: linear-gradient(90deg, #e6f2ff 25%, #f0f4f8 50%, #e6f2ff 75%);
  background-size: 200% 100%;
  animation: skeleton 1.2s ease-in-out infinite;
}
@keyframes skeleton {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
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
.animate-chart-fade {
  animation: chartFadeIn 1.2s cubic-bezier(0.4,0,0.2,1);
}
@keyframes chartFadeIn {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}
</style>
