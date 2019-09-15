import Vue from 'vue'
import Vuex from 'vuex'

import { authenticate, register } from '@/api'
import { isValidJwt, EventBus } from '@/utils'

Vue.use(Vuex)

const state = {
    user: {},
    jwt: ''
}

const actions = {
    login(context, userData) {
        context.commit('setUserData', { userData })
        return authenticate(userData)
            .then(response => context.commit('setJwtToken', { jwt: response.data }))
            .catch(error => {
                console.log('Error Authenticating: ', error)
                EventBus.emit('failedAuthentication', error)
            })
    },
    register(context, userData) {
        context.commit('setUserData', { userData })
        return register(userData)
            .then(context.dispatch('login', userData))
            .catch(error => {
                console.log('Error Registering: ', error)
                EventBus.emit('failedRegistering: ', error)
            })
    }
}

const mutations = {
    setUserData(state, payload) {
        console.log('setUserData payload = ', payload)
        state.userData = payload.userData
    },
    setJwtToken(state, payload) {
        console.log('setJwtToken payload = ', payload)
        localStorage.token = payload.jwt.token
        state.jwt = payload.jwt
    }
}

const getters = {
    // reusable data accessors
    isAuthenticated(state) {
        return isValidJwt(state.jwt.token)
    }
}