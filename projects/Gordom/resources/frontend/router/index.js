import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Index',
    component: () => import('../views/Index.vue'),
    meta: {
      title: 'Treasure Casino - Главная'
    }
  },
  {
    path: '/dice',
    name: 'Dice',
    component: () => import('../views/games/Dice.vue'),
    meta: {
      title: 'Treasure Casino - Dice'
    }
  },
  {
    path: '/mines',
    name: 'Mines',
    component: () => import('../views/games/Mines.vue'),
    meta: {
      title: 'Treasure Casino - Mines'
    }
  },
  {
    path: '/wheel',
    name: 'Wheel',
    component: () => import('../views/games/Wheel.vue'),
    meta: {
      title: 'Treasure Casino - Wheel'
    }
  },
  {
    path: '/slots',
    name: 'Slots',
    component: () => import('../views/games/Slots.vue'),
    meta: {
      title: 'Treasure Casino - Slots'
    }
  },
  {
    path: '/slots/:id',
    name: 'SlotsGame',
    component: () => import('../views/games/SlotGame.vue'),
    meta: {
      title: 'Treasure Casino - Slots'
    }
  },
  {
    path: '/bonus',
    name: 'Bonus',
    component: () => import('../views/Bonus.vue'),
    meta: {
      title: 'Treasure Casino - Бонусы'
    }
  },
  {
    path: '/policy',
    name: 'Policy',
    component: () => import('../views/Policy.vue'),
    meta: {
      title: 'Treasure Casino - Политика конфиденциальности'
    }
  },
  {
    path: '/contacts',
    name: 'Contacts',
    component: () => import('../views/Contacts.vue'),
    meta: {
      title: 'Treasure Casino - Контакты'
    }
  },
  {
    path: '/refferal',
    name: 'Refferal',
    component: () => import('../views/Refferal.vue'),
    meta: {
      title: 'Treasure Casino - Партнерская программа'
    }
  },
  {
    path: '/provably-fair',
    name: 'Fair',
    component: () => import('../views/Fair.vue'),
    meta: {
      title: 'Treasure Casino - Честная игра'
    }
  },
  {
    path: '/tourniers',
    name: 'Tourniers',
    component: () => import('../views/tourniers/Tourniers.vue'),
    meta: {
      title: 'Treasure Casino - Турниры'
    }
  },
  {
    path: '/tourniers/:id',
    name: 'Tournier',
    component: () => import('../views/tourniers/Tournier.vue'),
    meta: {
      title: 'Treasure Casino - Турнир'
    }
  },
  {
    path: '/faq',
    name: 'Faq',
    component: () => import('../views/Faq.vue'),
    meta: {
      title: 'Treasure Casino - Помощь'
    }
  },
  {
    path: '/logout',
    name: 'Logout',
    component: () => import('../views/Logout.vue'),
    meta: {
      title: 'Treasure Casino - Выход'
    }
  },
  {
    path: '/404',
    name: '404',
    component: () => import('../views/errors/404.vue'),
    meta: {
      title: 'Упс! Страница не найдена'
    }
  },
  {
    path: '*',
    redirect: '/404',
  },
]

const router = new VueRouter({
  routes,
  mode: 'history'
})

router.beforeEach((to, from, next) => {
  document.title = to.meta.title
  next()
})

export default router
