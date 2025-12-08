import './bootstrap';
import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import axios from './axios';
import '../css/app.css';
import ToastContainer from './components/ToastContainer.vue';

const app = createApp(App);
app.component('ToastContainer', ToastContainer);

// Глобальные свойства
app.config.globalProperties.$axios = axios;

// Монтирование приложения
app.use(router)
   .mount('#app');
