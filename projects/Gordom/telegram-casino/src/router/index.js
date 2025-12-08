import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/dice', name: 'Dice', component: () => import('../views/games/Dice.vue') },
  { path: '/wheel', name: 'Wheel', component: () => import('../views/games/Wheel.vue') },
  { path: '/mines', name: 'Mines', component: () => import('../views/games/Mines.vue') },
  { path: '/slots', name: 'Slots', component: () => import('../views/games/Slots.vue') },
  { path: '/profile', name: 'Profile', component: () => import('../views/Profile.vue') },
  { path: '/deposit', name: 'Deposit', component: () => import('../views/Deposit.vue') },
  { path: '/withdraw', name: 'Withdraw', component: () => import('../views/Withdraw.vue') },
  { path: '/bonus', name: 'Bonus', component: () => import('../views/Bonus.vue') },
  { path: '/referral', name: 'Referral', component: () => import('../views/Referral.vue') },
  { path: '/history', name: 'History', component: () => import('../views/History.vue') },
  { path: '/leaderboard', name: 'Leaderboard', component: () => import('../views/Leaderboard.vue') },
  { path: '/achievements', name: 'Achievements', component: () => import('../views/Achievements.vue') },
  { path: '/tournaments', name: 'Tournaments', component: () => import('../views/Tournaments.vue') },
  // Букмекерские ставки
  { path: '/sports', name: 'Sports', component: () => import('../views/Sports.vue') },
  { path: '/sports/history', name: 'BetHistory', component: () => import('../views/BetHistory.vue') },
  // Аналитика и AI
  { path: '/analytics', name: 'Analytics', component: () => import('../views/Analytics.vue') },
  { path: '/predictions', name: 'Predictions', component: () => import('../views/Predictions.vue') },
  { path: '/achievements', name: 'Achievements', component: () => import('../views/Achievements.vue') },
  // Админ-панель
  { path: '/admin', name: 'AdminPanel', component: () => import('../views/AdminPanel.vue') },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Save start_param from query for non-Telegram browsers (dev/testing)
router.beforeEach((to) => {
  const ref = to.query?.start_param
  if (ref) {
    localStorage.setItem('ref', String(ref))
  }
})

export default router
