<template>
  <div id="app">
    <navbar></navbar>
    <div class = "container-fluid">
        <div class = "row">
          <sidebar></sidebar>
          <div class = "col-sm-9 col-md-10 main">
              <router-view/>
          </div>
        </div>
    </div>
  </div>
</template>

<script>

import Sidebar from '@/components/generic/Sidebar.vue'
import Navbar from '@/components/generic/Navbar.vue'

export default {
  name: 'App',
  components: {
    'sidebar': Sidebar,
    'navbar': Navbar
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

@import '@/static/bootstrap/css/bootstrap.min.css';
</style>
