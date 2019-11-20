import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)
export default new Vuex.Store({
  state: {
    status: '',
    token: localStorage.getItem('token') || '',
    user: {}
  },

  mutations: {
    auth_request (state) {
      state.status = 'loading'
    },

    auth_success (state, payload) {
      state.status = 'success'
      state.token = payload.token
      state.user = payload.user
    },

    auth_error (state) {
      state.status = 'error'
    },

    logout (state) {
      state.status = ''
      state.token = ''
    }
  },

  actions: {
    login ({commit}, UserData) {
      return new Promise((resolve, reject) => {
        commit('auth_request')

        axios({ url: 'http://localhost:8080/auth/', data: UserData, method: 'POST' })
          .then(resp => {
            const token = resp.data.token
            const user = {
              username: resp.data.username,
              id: resp.data.user_id,
              uuid: resp.data.uuid
            }

            localStorage.setItem('token', token)

            axios.defaults.headers.common['Authorization'] = token

            commit('auth_success', {token: token, user: user})
            resolve(resp)
          })
          .catch(err => {
            commit('auth_error')

            localStorage.removeItem('token')

            reject(err)
          })
      })
    },

    register ({commit}, user) {
      return new Promise((resolve, reject) => {
        commit('auth_request')

        axios({ url: 'http://localhost:8080/register', data: user, method: 'POST' })

          .then(resp => {
            const token = resp.data.token
            const user = resp.data.user

            localStorage.setItem('token', token)

            axios.defaults.headers.common['Authorization'] = token

            commit('auth_success', token, user)
            resolve(resp)
          })
          .catch(err => {
            commit('auth_error', err)

            localStorage.removeItem('token')

            reject(err)
          })
      })
    },

    logout ({commit}) {
      return new Promise((resolve, reject) => {
        commit('logout')

        localStorage.removeItem('token')

        delete axios.defaults.headers.common['Authorization']

        resolve()
      })
    }
  },

  getters: {
    isLoggedIn: state => !!state.token,
    authStatus: state => state.status,
    getUser: state => state.user
  }
})
