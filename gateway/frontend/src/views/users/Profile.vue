<template>
  <div id = "articles-table" class = "container">

    <full-table
      v-if="is_data_full"
      v-bind:full_data="articles"
    />

    <degrated-table
      v-else-if="is_data_degrated"
      v-bind:degrated_data="articles"
    />

    <template v-else>
      <span>No data has been provided</span>
    </template>

  </div>

</template>

<script>
import toast from '@/utility/toast'
import UFullTable from '@/components/users/UArticlesFullTable.vue'
import UDegratedTable from '@/components/users/UArticlesDegratedTable.vue'

export default {
  name: 'profile-view',

  components: {
    'full-table': UFullTable,
    'degrated-table': UDegratedTable
  },

  data () {
    return {
      articles: {
        type: Array
      },
      api: '/users/',
      instruction: '/articles/',
      id: this.$route.params.id,

      fullDataHeaders: ['j_name', 'j_foundation', 'j_publisher'],
      degratedDataHeaders: ['uuid', 'authors', 'title', 'added', 'published', 'journal']
    }
  },

  created () {
    this.fetchData()
  },

  methods: {
    fetchData () {
      this.$http.get(`${this.api}${this.id}${this.instruction}`).then(
        response => {
          let data = response.data
          this.articles = data
        }).catch(
        error => {
          if (error.response.data.hasOwnProperty('detail')) {
            toast.error(error.response.data.detail)
          } else {
            toast.error(error.response.data)
          }

          if (error.response.status === 422) this.$router.push('/422')

          if (error.response.status === 404) this.$router.push('/404')
        })
    }
  },

  computed: {
    has_data () {
      return this.articles.length
    },

    is_data_full () {
      if (this.has_data) {
        const first = this.articles[0]
        return this.fullDataHeaders.every(header => first.hasOwnProperty(header))
      } else {
        return false
      }
    },

    is_data_degrated () {
      if (this.has_data) {
        const first = this.articles[0]
        return this.degratedDataHeaders.every(header => first.hasOwnProperty(header))
      } else {
        return false
      }
    }
  }
}
</script>
