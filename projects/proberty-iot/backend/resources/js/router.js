import { createRouter, createWebHistory } from 'vue-router';
import Login from './views/Login.vue';
import Dashboard from './views/Dashboard.vue';
import Equipment from './views/Equipment.vue';
import Sensors from './views/Sensors.vue';
import Maintenance from './views/Maintenance.vue';
import Profile from './views/Profile.vue';

const routes = [
  { path: '/', name: 'Dashboard', component: Dashboard, meta: { requiresAuth: true, roles: ['admin', 'engineer', 'operator'] } },
  { path: '/equipment', name: 'Equipment', component: Equipment, meta: { requiresAuth: true, roles: ['admin', 'engineer'] } },
  { path: '/sensors', name: 'Sensors', component: Sensors, meta: { requiresAuth: true, roles: ['admin', 'engineer'] } },
  { path: '/maintenance', name: 'Maintenance', component: Maintenance, meta: { requiresAuth: true, roles: ['admin', 'engineer', 'operator'] } },
  { path: '/profile', name: 'Profile', component: Profile, meta: { requiresAuth: true, roles: ['admin', 'engineer', 'operator'] } },
  { path: '/login', name: 'Login', component: Login, meta: { guest: true } },
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token');
  const userRole = localStorage.getItem('role');
  if (to.meta.requiresAuth && !token) {
    next('/login');
  } else if (to.meta.guest && token) {
    next('/');
  } else if (to.meta.roles && userRole && !to.meta.roles.includes(userRole)) {
    next('/');
  } else {
    next();
  }
});

export default router;
