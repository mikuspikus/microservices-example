<template>
  <div id = "Register">
    <h4>Sign Up</h4>

    <form @submit.prevent="register">
      <label for="username">Username</label>
      <div>
          <input id="username" type="text" v-model="username" required autofocus>
      </div>

      <label for="password">Password</label>
      <div>
          <input id="password" type="password" v-model="password" required>
      </div>

      <label for="password-confirm">Confirm Password</label>
      <div>
          <input id="password-confirm" type="password" v-model="password_confirmation" required>
      </div>

      <div>
          <button type="submit">Register</button>
      </div>
    </form>

  </div>

</template>

<script>
import toast from '@/utility/toast'

export default {
  data () {
    return {
      username: '',
      password: '',
      password_confirmation: ''
    }
  },

  methods: {
    register () {
      if (this.password !== this.password_confirmation) {
        toast.error('Passwords does not match')
      } else {
        let data = {
          username: this.username,
          password: this.password
        }
        this.$store.dispatch('register', data)
          .then(
            () => this.$router.push('/')
          )
          .catch(
            err => {
              toast.error(err)
              console.log(err)
            }
          )
      }
    }
  }
}
</script>
