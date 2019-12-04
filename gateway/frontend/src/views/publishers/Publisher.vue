<template>
  <div id = "publisher-form" class = "container">

    <PEditForm
      v-if="has_data"
      v-bind:publisher="publisher"
      v-bind:service="api">
    </PEditForm>

  </div>

</template>

<script>
import toast from '@/utility/toast'
import PEditForm from '@/components/publishers/Edit.vue'

export default {
  name: 'publisher-view',

  components: {
    'PEditForm': PEditForm
  },

  data () {
    return {
      publisher: {
        type: Object
      },
      api: '/publishers/',
      uuid: this.$route.params.uuid
    }
  },

  beforeCreated () {
    this.fetchData()
  },

  methods: {
    fetchData () {
      this.$http.get(`${this.api}${this.uuid}/`).then(
        response => {
          let data = response.data
          this.publisher = data
        }).catch(
        error => {
          toast.error(error)

          if (error.response.status === 422) this.$router.push('/422')

          if (error.response.status === 404) this.$router.push('/404')
        })
    }
  },

  computed: {
    has_data () { return this.publisher.length !== 0 }
  }
}
</script>
