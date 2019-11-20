<template>
    
</template>

<template>
  <div id = "journal-form" class = "container">

    <AEditForm
      v-if="has_data"
      v-bind:journal="article"
      v-bind:service="api"
    >
    </AEditForm>

    <h4 v-else>No data</h4>

  </div>

</template>

<script>
import toast from '@/utility/toast'
import AEditForm from '@/components/articles/Edit.vue'

export default {
  name: 'article-view',

  components: {
    'AEditForm': AEditForm
  },

  data () {
    return {
      article: {
        type: Object
      },
      api: '/articles/',
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
    has_data () { return this.article.length !== 0 }
  }
}
</script>
