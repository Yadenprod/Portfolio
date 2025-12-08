import Vue from 'vue';

export default {
	actions: {
		getUserData(ctx) {
			Utils.apiPostCall('/api/user/')
					.then(resp => {
						ctx.commit('updateUser', resp.data.user);
					})
		}
	},
	mutations: {
		updateUser(state, user) {
			Vue.set(state, 'user', user);
		},
		changeBalance(state, change) {
			Vue.set(state.user, 'balance', parseInt(state.user.balance) + parseInt(change));
		},
		setBalance(state, balance) {
			Vue.set(state.user, 'balance', balance);
		},
	},
	state: {
		user: {}
	},
	getters: {
		hasUserData(state) {
			return Object.keys(state.user).length != 0;
		},
		userData(state) {
			return state.user;
		},
		isLogin(state) {
			return state.user && state.user.login;
		}
	}
}