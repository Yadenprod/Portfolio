import Vue from 'vue';
import VueRouter from 'vue-router';
import Vuex from 'vuex';
import VueClipboards from "vue-clipboards";
import Notifications from 'vue-notification'
import User from './store/user';
import Index from './components/pages/IndexPage.vue';
import Case from './components/pages/CasePage.vue';
import Contracts from './components/pages/ContractsPage.vue';
import Upgrade from './components/pages/UpgradePage.vue';
import Battles from './components/pages/BattlesPage.vue';
import Battle from './components/pages/BattlePage.vue';
import Profile from './components/pages/ProfilePage.vue';
import Top from './components/pages/TopPage.vue';
import Livetrade from './components/pages/LivetradePage.vue';
import FAQ from './components/pages/FAQPage.vue';
import Simple from './components/pages/SimplePage.vue';
import Default from './components/pages/DefaultPage.vue';

window.$ = window.jQuery = require('jquery');
window.Utils = require('./utils/utils');
window.axios = require('axios');
window.Centrifuge = require("centrifuge");

Vue.use(VueRouter);
Vue.use(Vuex);
Vue.use(VueClipboards);
Vue.use(Notifications);

Vue.prototype.$eventBus = new Vue();

Vue.prototype.SITE_URL = SITE_URL;
Vue.prototype.SITE_NAME = SITE_NAME;
Vue.prototype.GAME_NAME = GAME_NAME;
Vue.prototype.VK_URL = 'https://vk.com/club198007059';

Vue.prototype.$centrifugeConnected = false;
//let centrifuge = new Centrifuge('ws://127.0.0.1:8888/connection/websocket');
let centrifuge = new Centrifuge('wss://maybedrop.com/centrifugo/connection/websocket');
Vue.prototype.$centrifuge = centrifuge;
centrifuge.on('connect', (ctx) => {
	if (Vue.prototype.$centrifugeConnected != true) {
		Vue.prototype.$centrifugeConnected = true;
		Vue.prototype.$eventBus.$emit('centrifugeConnected');
	}
});
centrifuge.on('disconnect', (ctx) => {
	if (Vue.prototype.$centrifugeConnected != false) {
		Vue.prototype.$centrifugeConnected = false;
		Vue.prototype.$eventBus.$emit('centrifugeDisconnected');
	}
});
centrifuge.connect();

Vue.prototype.clearItemQuality = (itemName) => {
	return itemName.replace(/\(Factory New\)|\(Minimal Wear\)|\(Field-Tested\)|\(Well-Worn\)|\(Battle-Scarred\)/gi, '').trim();
};

Vue.component('header-layout', require('./components/layout/HeaderLayout.vue').default);
Vue.component('footer-layout', require('./components/layout/FooterLayout.vue').default);
Vue.component('page-404', require('./components/pages/404.vue').default);

const router = new VueRouter({
	mode: 'history',
	routes: [
		{path: '/', component: Index},
		{path: '/case/:key/', component: Case},
		{path: '/contracts/', name: 'contracts', component: Contracts, props: true},
		{path: '/upgrade/', component: Upgrade},
		{path: '/battles/', component: Battles},
		{path: '/battle/:id/', component: Battle},
		{path: '/profile/:steamId?/', component: Profile},
		{path: '/top/', component: Top},
		{path: '/livetrade/', component: Livetrade},
		{path: '/faq/', component: FAQ},
		{path: '/deposite/success/', component: Simple, props: {pageData: {title: 'Оплата успешно произведена', pageTitle: 'Оплата успешно произведена', content: 'Оплата успешно произведена'}}},
		{path: '/deposite/fail/', component: Simple, props: {pageData: {title: 'Неудачная попытка оплаты', pageTitle: 'Неудачная попытка оплаты', content: 'Неудачная попытка оплаты'}}},
		{path: '/deposite/waiting/', component: Simple, props: {pageData: {title: 'Ожидание подтверждения', pageTitle: 'Ожидание подтверждения', content: 'Ожидание процесса подтверждения платежа со стороны платежной системы'}}},
		{path: '*', component: Default}
	],
	scrollBehavior(to, from, savedPosition) {
		if (savedPosition) {
			return savedPosition;
		} else {
			return {x: 0, y: 0};
		}
	}
});

const store = new Vuex.Store({
	modules: {
		User
	}
});

const app = new Vue({
	el: '#app',
	router,
	store,
	created: function () {
		this.$store.dispatch('getUserData');
	}
});

export default app;
