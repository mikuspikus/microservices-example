// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import store from './store'

import axios from 'axios'

import Sidebar from '@/components/generic/Sidebar.vue'
import Navbar from '@/components/generic/Navbar.vue'

Vue.prototype.$http = axios
const token = localStorage.getItem('token')
if (token) {
  Vue.prototype.$http.defaults.headers.common['Authorization'] = token
}

Vue.prototype.$http.defaults.baseURL = 'http://localhost:8080/'

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App, Sidebar, Navbar },
  template: '<App/>',
  store: store
})
