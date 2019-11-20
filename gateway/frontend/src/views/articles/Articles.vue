<template>
  <div id = "Articles">

    <post-from></post-from>

    <br/>
    <hr/>
    <br/>

    <ArticlesTable :data="articles">
    </ArticlesTable>

  </div>
</template>

<script>

import APostForm from '@/components/articles/New.vue'
import ATable from '@/components/articles/ATable.vue'
import toast from '@/utility/toast'

export default {
  name: 'Articles',

  components: {
    'ArticlesTable': ATable,
    'post-from': APostForm
  },

  data () {
    return {
      articles: [],
      api: 'articles/'
    }
  },

  created () {
    this.fetchData()
  },

  methods: {
    fetchData () {
      this.$http.get(this.api).then(
        response => {
          console.log(response.data)
          this.articles = response.data
        }).catch(
        error => {
          toast.error(error)

          if (error.response.status === 422) this.$router.push('/422')

          if (error.response.status === 404) this.$router.push('/404')
        })
    }
  }
}
</script>
