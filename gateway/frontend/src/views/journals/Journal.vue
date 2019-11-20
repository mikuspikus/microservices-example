<template>
  <div id = "journal-form" class = "container">

    <JEditForm
      v-if="has_data"
      v-bind:journal="journal"
      v-bind:service="api"
    >
    </JEditForm>

    <h4 v-else>No data</h4>

  </div>

</template>

<script>
import toast from '@/utility/toast'
import JEditForm from '@/components/journals/Edit.vue'

export default {
  name: 'journal-view',

  components: {
    'JEditForm': JEditForm
  },

  data () {
    return {
      journal: {
        type: Object
      },
      api: '/journals/',
      uuid: this.$route.params.uuid
    }
  },

  created () {
    this.fetchData()
  },

  methods: {
    fetchData () {
      this.$http.get(`${this.api}${this.uuid}/`).then(
        response => {
          let data = response.data
          this.journal = data
        }).catch(
        error => {
          toast.error(error)

          if (error.response.status === 422) this.$router.push('/422')

          if (error.response.status === 404) this.$router.push('/404')
        })
    }
  },

  computed: {
    has_data () { return this.journal.length !== 0 }
  }
}
</script>
