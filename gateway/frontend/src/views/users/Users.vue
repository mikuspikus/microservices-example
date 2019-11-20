<template>
  <div id = "users">

    <UsersTable :data="users">
    </UsersTable>

  </div>
</template>

<script>
import BTable from '@/components/generic/BTable.vue'
import toast from '@/utility/toast'

export default {
  name: 'users',

  components: {
    'UsersTable': BTable
  },

  data () {
    return {
      users: [],
      api: 'users/'
    }
  },

  created () {
    this.fetchData()
  },

  methods: {
    fetchData () {
      this.$http.get(this.api).then(
        response => {
          this.users = response.data
        }).catch(
        error => {
          toast.error(error.message)
          if (error.response.status === 422) this.$router.push('/422')

          if (error.response.status === 404) this.$router.push('/404')
        })
    }
  }
}
</script>
