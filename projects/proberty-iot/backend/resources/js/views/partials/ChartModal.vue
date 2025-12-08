<template>
  <div class="modal-bg" @click.self="$emit('close')">
    <div class="modal">
      <h3>График данных по оборудованию #{{ equipmentId }}</h3>
      <canvas ref="chartEl"></canvas>
      <button @click="$emit('close')">Закрыть</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { Chart, LineController, LineElement, PointElement, LinearScale, Title, CategoryScale } from 'chart.js';
import axios from 'axios';
Chart.register(LineController, LineElement, PointElement, LinearScale, Title, CategoryScale);

const props = defineProps({ equipmentId: Number });
const chartEl = ref(null);
let chartInstance = null;

async function fetchSensorData() {
  // Имитация: получаем 10 случайных точек через внешний API
  const points = [];
  for (let i = 0; i < 10; i++) {
    const { data } = await axios.get('/api/external/simulate-sensor');
    points.push({
      x: new Date(Date.now() - (10 - i) * 60000).toLocaleTimeString(),
      y: data.value,
      label: data.type + ' ' + data.unit
    });
  }
  return points;
}

async function renderChart() {
  const points = await fetchSensorData();
  if (chartInstance) chartInstance.destroy();
  chartInstance = new Chart(chartEl.value, {
    type: 'line',
    data: {
      labels: points.map(p => p.x),
      datasets: [{
        label: points[0]?.label || 'Sensor',
        data: points.map(p => p.y),
        borderColor: '#007bff',
        backgroundColor: 'rgba(0,123,255,0.1)',
        fill: true,
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: true } },
    }
  });
}

onMounted(renderChart);
watch(() => props.equipmentId, renderChart);
</script>

<style scoped>
.modal-bg {
  position: fixed;
  inset: 0;
  background: #0008;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}
.modal {
  background: #fff;
  padding: 2rem;
  border-radius: 8px;
  min-width: 350px;
  box-shadow: 0 2px 12px #0002;
  position: relative;
}
canvas {
  width: 100% !important;
  max-width: 400px;
  margin: 1rem 0;
}
button {
  margin-top: 1rem;
  background: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  padding: 0.5rem 1rem;
  cursor: pointer;
}
</style>
