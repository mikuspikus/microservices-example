<template>
  <div id = "publishers">

    <post-form :api="api"></post-form>

    <br/>
    <hr/>
    <br/>

    <PublishersTable
      :data="publishers"
      :api="api"
    >
    </PublishersTable>

  </div>
</template>

<script>
import PPostForm from '@/components/publishers/New.vue'
import PTable from '@/components/publishers/PTable.vue'
import toast from '@/utility/toast'

export default {
  name: 'Publishers',

  components: {
    'PublishersTable': PTable,
    'post-form': PPostForm
  },

  data () {
    return {
      publishers: [],
      api: 'publishers/'
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
          this.publishers = response.data
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
