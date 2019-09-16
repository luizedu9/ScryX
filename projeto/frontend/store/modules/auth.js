import axios from 'axios'
import router from '@/router'

const state = {
	username: null,
	token: null,
	status: null,
};

const mutations = {
	authUser(state, userData) {
		state.username = userData.username;
		state.token = userData.token;
	},
	clearAuthData(state) {
		state.username = null;
		state.token = null;
	},
	setStatus(state, status) {
		state.status = status;
	}
};

const getters = {
	isAuthenticated(state) {
		return state.token !== null;
	},
	getStatus(state) {
		return state.status;
	},
};

const actions = {
	login: ({commit}, authData) => {
		axios.post('/login', {
			username: authData.username,
			password: authData.password,
		}).then(response => {
			let status = response.data.status;
			if (status == '0') {
				commit('authUser', { username: authData.username, token: response.data.token });
				localStorage.setItem('token', response.data.token);
				localStorage.setItem('username', authData.username);
				router.push("/")
			} 
			else if (status == '2') {
				commit('setStatus', "Usuário ou senha incorretos");
			} else {
				commit('setStatus', "Houve um erro, tente mais tarde");
			}
		}).catch(error => {
			// eslint-disable-next-line
			console.log(error);
			commit('setStatus', "Houve um erro, tente mais tarde");
		})
	},
	cleanStatus({ commit }) {
		commit('setStatus', null);
	},
	autoLogin({commit}) {
		let token = localStorage.getItem('token');
		let username = localStorage.getItem('username');

		if (!token || !username) {
			return;
		}

		commit('authUser', { username: username, token: token });
	},
	logout: ({commit}) => {
		commit('clearAuthData');
		localStorage.removeItem('username');
		localStorage.removeItem('token');
		router.replace('login');
	},
};

export default {
	namespaced: true,
	state,
	mutations,
	getters,
	actions,
}