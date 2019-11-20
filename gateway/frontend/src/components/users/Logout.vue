<template>

  <div id = "login">

    <form class="login" @submit.prevent="login">
      <h1>Sign in</h1>

      <label for="username" class="sr-only">Username</label>
      <input id = "username" class = "form-control" required v-model="username" type="login" placeholder="Username"/>

      <br>

      <label for="password" class="sr-only">Password</label>
      <input id = "password" class = "form-control" required v-model="password" type="password" placeholder="Password"/>
      <hr/>
      <button type="submit" class = "btn btn-danger">Login</button>
    </form>

  </div>

</template>

<script>
export default {
  data () {
    return {
      username: '',
      password: '',
      errors: []
    }
  },

  methods: {
    login () {
      let username = this.username
      let password = this.password

      this.$store.dispatch('login', { username, password })
        .then(
          () => this.$router.push('/')
        )
        .catch(
          err => console.log(err)
        )
    }
  }
}
</script>
