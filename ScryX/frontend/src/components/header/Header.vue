<template>
	<b-navbar toggleable="lg" style="background-color: #99ccff !important" class="mb-5">
		<b-navbar-toggle target="nav_text_collapse"></b-navbar-toggle>
		<b-navbar-brand>ScryX</b-navbar-brand>
	
		<b-collapse is-nav id="nav_text_collapse">
			<b-navbar-nav>
				<b-nav-text>
					<router-link to="/" class="nav-link">Início</router-link>
				</b-nav-text>
				<b-nav-text v-if="!isAuth">
					<router-link to="/login" class="nav-link">Login</router-link>
				</b-nav-text>
				<b-nav-text v-if="isAuth">
					<router-link to="/quoteprice" class="nav-link">Cotar</router-link>
				</b-nav-text>
				<b-nav-text v-if="isAuth">
					<router-link to="/history" class="nav-link">Histórico</router-link>
				</b-nav-text>
			</b-navbar-nav>
	
			<b-navbar-nav v-if="isAuth" class="ml-auto" >
				<b-nav-item-dropdown text="" right>
					<b-dropdown-item href="#"><router-link to="/account" class="nav-link">Perfil</router-link></b-dropdown-item>
					<b-dropdown-item href="#" @click="onLogout"><router-link to="/" class="nav-link">Sair</router-link></b-dropdown-item>
				</b-nav-item-dropdown>
			</b-navbar-nav>
		</b-collapse>
	</b-navbar>
</template>

<script>
	import { mapGetters } from 'vuex'
	
	export default {
		computed: {
			...mapGetters('auth', {
				isAuth: 'isAuthenticated',
			})
		},
		methods: {
			onLogout() {
				this.$store.dispatch('auth/logout');
			}
		}
	}
</script>
