<template>
  <div id = "journal-form" class = "container">

    <form @submit="checkForm" novalidate="true">
        <div class="row error" v-if="errors.length">
            <b>Correct following errors:</b>
            <ul class="list-group">
                <li class="list-group-item list-group-item-danger" v-for="error in errors" :key="error">{{ error }}</li>
            </ul>
        </div>

        <div class="form-group">
          <label for="name">Journal's name</label>
          <input id = "name" class="form-control" name = "name" v-model="name">
        </div>

        <div class="form-group">
          <label for = "foundation">Date of journal's foundation</label>
          <input id = "foundation" class="form-control" name = "foundation" v-model="foundation">
        </div>

        <div class="form-group">
          <label for="publisher">Journal's publisher</label>
          <input id = "publisher" class="form-control" name = "publisher" v-model="publisher">
        </div>

        <hr/>

        <input class="btn btn-primary" type = "Submit" value = "Submit">
      </form>
  </div>
</template>

<script>
import toast from '@/utility/toast'

export default {
  name: 'JPostForm',
  data () {
    return {
      errors: [],
      name: null,
      foundation: null,
      publisher: null
    }
  },
  methods: {
    checkForm (e) {
      this.errors = []
      if (!this.name) { this.errors.push('Journal\'s name is required') }

      if (!this.foundation) { this.errors.push('Journal\'s foundation must not be empty') }

      if (!this.publisher) { this.errors.push('Journal\'s publisher must not be empty') }

      if (!this.errors.length) {
        this.submitJournal()
      }
      e.preventDefault()
    },
    submitJournal () {
      this.$http.post('journals/',
        {
          'name': this.name,
          'foundation': this.foundation,
          'publisher': this.publisher
        }).then(response => {
        toast.success('Journal created')
        this.$router.push('/journals/' + response.data.uuid)
      })
        .catch(error => {
          toast.error(error)
        })
    }
  }
}
</script>
