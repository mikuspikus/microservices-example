<template>
  <div id = "journals">

    <post-form></post-form>

    <br/>
    <hr/>
    <br/>

    <JournalsTable :data="journals">
    </JournalsTable>

  </div>
</template>

<script>
import BTable from '@/components/generic/BTable.vue'
import JPostForm from '@/components/journals/New.vue'
import toast from '@/utility/toast'

export default {
  name: 'Journals',

  components: {
    'JournalsTable': BTable,
    'post-form': JPostForm
  },

  data () {
    return {
      journals: [],
      api: 'journals/'
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
          this.journals = response.data
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
