<template>
    <nav class = "navbar navbar-inverse-lg navbar-light navbar-fixed-top" role = "navigation">

        <a class="navbar-brand" href="#">{{ title }}</a>

        <div class = "container-fluid">

          <div class = "navbar-header">
            <button type = "button" class = "navbar-toggle collapsed" data-toggle = "collapse" data-target = ".navbar-collapse">
              <span class = "sr-only">Toggle navigation</span>
              <span class = "icon-bar"></span>
              <span class = "icon-bar"></span>
              <span class = "icon-bar"></span>
            </button>
          </div>

          <div class = "collapse navbar-collapse">

            <ul class = "nav navbar-nav navbar-right">

              <li class = "nav-item active">
                <router-link to="/">Home</router-link>
              </li>

              <template  v-if="is_authorized">
              <!-- <li class = "nav-item active">
                <router-link to="/">Profile</router-link>
              </li> -->

              <li class = "nav-item active">
                <a v-on:click="logout">Logout</a>
              </li>
              </template>

              <template v-else>
              <li class = "nav-item active">
                <router-link to="/login">Sign In</router-link>
              </li>
              <li class = "nav-item active">
                <router-link to="/register">Sign Up</router-link>
              </li>
              </template>

              <li class = "nav-item">
                <span class="navbar-text justify-content-end">
                  {{ greetings }}
                </span>
              </li>

            </ul>
          </div>
        </div>
    </nav>
</template>

<script>
export default {
  name: 'Navbar',

  props: {
    title: {
      type: String,
      default: 'Example of microservice implementation with Django 2, DRF and Vue.js'
    }
  },

  methods: {
    logout () {
      this.$store.dispatch('logout')
        .then(
          () => this.$router.push('/')
        )
        .catch(
          err => console.log(err)
        )
    }
  },

  computed: {
    is_authorized () { return this.$store.getters.isLoggedIn },
    greetings () {
      let user = this.$store.getters.getUser
      return this.is_authorized ? 'Welcome, ' + user.username : 'Welcome'
    }
  }
}
</script>
