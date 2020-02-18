import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
Vue.use(Vuex)


export default new Vuex.Store({
    state: {
        count: 0,
        status: '',
        token: localStorage.getItem('token') || '',
        user: {}
    },
    mutations: {
        increment (state) {
            state.count++
        },
        decrement (state) {
            state.count--
        },
        // auth
        auth_request(state){
            state.status = 'loading'
        },
        auth_success(state, token, user){
            state.status = 'success'
            state.token = token
            state.user = user
        },
        auth_error(state){
            state.status = 'error'
        },
        logout(state){
            state.status = ''
            state.token = ''
        },
    },
    actions: {
        login({commit}, credentials){
            return new Promise((resolve, reject) => {
                commit('auth_request')
                axios({
                    url: 'https://atarasov.ru/api/token/',
                    data: credentials,
                    method: 'POST'
                })
                .then(response => {
                    const token = response.data.token
                    localStorage.setItem('token', token)

                    axios
                    .get('https://atarasov.ru/api/users/getuser/', {headers: {Authorization: 'JWT ' + token}})
                    .then(response => {
                        const user = response.data.user
                        commit('auth_success', token, user)
                        resolve(response)

                    })
                    .catch(err => {
                        commit('auth_error')
                        localStorage.removeItem('token')
                        reject(err)
                    })
                })
                .catch(err => {
                    commit('auth_error')
                    localStorage.removeItem('token')
                    reject(err)
                })
            })
        },
        logout({commit}){
            return new Promise((resolve, reject) => {
                commit('logout')
                localStorage.removeItem('token')
                resolve()
            })
        },
        register({commit}, credentials){
            return new Promise((resolve, reject) => {
                commit('auth_request')
                axios({
                    url: 'https://atarasov.ru/api/users/register/',
                    data: credentials,
                    method: 'POST'
                })
                .then(response => {
                    const token = response.data.token
                    localStorage.setItem('token', token)

                    axios
                    .get('https://atarasov.ru/api/users/getuser/', {headers: {Authorization: 'JWT ' + token}})
                    .then(response => {
                        const user = response.data.user
                        commit('auth_success', token, user)
                        resolve(response)

                    })
                    .catch(err => {
                        commit('auth_error')
                        localStorage.removeItem('token')
                        reject(err)
                    })
                })
                .catch(err => {
                    commit('auth_error', err)
                    localStorage.removeItem('token')
                    reject(err)
                })
            })
        },
        createPost({commit}, text_data) {
            const token = localStorage.getItem('token')
            return new Promise((resolve, reject) => {
                axios({
                    url: 'https://atarasov.ru/api/posts/',
                    data: text_data,
                    headers: {
                        'Authorization': 'JWT ' + token,
                    },
                    method: 'POST'
                })
                .then(response => {
                    resolve(response)
                })
                .catch(error => {
                    reject(error)
                })
            })
        }
    },
    getters: {
        isLoggedIn: state => !!state.token,
        authStatus: state => state.status,
    }
})
