<template>
  <div id = "Articles">

    <complex-form
      :api="api"
      :instruction="instruction"
    />

    <br/>
    <hr/>
    <br/>

    <post-form/>

    <br/>
    <hr/>
    <hr/>
    <br/>

    <ArticlesTable :data="articles">
    </ArticlesTable>

  </div>
</template>

<script>

import APostForm from '@/components/articles/New.vue'
import AComplexForm from '@/components/articles/ComplexNew.vue'
import ATable from '@/components/articles/ATable.vue'
import toast from '@/utility/toast'

export default {
  name: 'Articles',

  components: {
    'ArticlesTable': ATable,
    'post-form': APostForm,
    'complex-form': AComplexForm
  },

  data () {
    return {
      articles: [],
      api: '/articles/',
      instruction: 'journal/'
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
          toast.error(error.message)

          if (error.response.status === 422) this.$router.push('/422')

          if (error.response.status === 404) this.$router.push('/404')
        })
    }
  }
}
</script>
