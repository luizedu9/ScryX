import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import Login from './views/Login.vue'
import QuotePrice from './views/QuotePrice.vue'
import History from './views/History.vue'
import Account from './views/Account.vue'
import axiosAuth from '@/api/axios-auth'

Vue.use(Router);

const routes = [
	{
		path: '/',
		component: Home,
	},
	{ 
		path: '/login', 
		component: Login,
	},
	{ 
		path: '/quoteprice', 
		component: QuotePrice,
		meta: { requiresAuth: true }
	},
	{
		path: '/history',
		component: History,
		meta: { requiresAuth: true }
	},
	{
		path: '/account',
		component: Account,
		meta: { requiresAuth: true }
	},
];

const router = new Router({
	routes: routes,
});

router.beforeEach((to, from, next) => {
	let token = localStorage.getItem('token');
	let requireAuth = to.matched.some(record => record.meta.requiresAuth);

	if (!requireAuth) {
		next();
	}

	if (requireAuth && !token) {
		next('/login');
	}

	if (to.path === '/login') {
		if (token) {
			axiosAuth.post('/verify-token').then(() => {
				next('/');
			}).catch(() => {
				next();
			});
		}
		else {
			next();
		}
	}

	if (requireAuth && token) {
		axiosAuth.post('/verify-token').then(() => {
			next();
		}).catch(() => {
			next('/login');
		})
	}
});

export default router;