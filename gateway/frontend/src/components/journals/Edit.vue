<template>
  <div id = "journal-form" class = "container">

    <div class = "container">
        <label>journal</label>
        <span class="label label-primary">{{ uuid }}</span>
    </div>

    <form @submit="checkForm" novalidate="true">
        <div class="row error" v-if="errors.length">
            <b>Correct following errors:</b>
            <ul class="list-group">
                <li class="list-group-item list-group-item-danger" v-for="error in errors" :key="error">{{ error }}</li>
            </ul>
        </div>

        <div class="form-group">
          <label for="name">journal's name</label>
          <input id = "name" class="form-control" name = "name" v-model="name">
        </div>

        <div class="form-group">
          <label for = "foundation">Date of journal's foundation</label>
          <input id = "foundation" class="form-control" name = "foundation" v-model="foundation">
        </div>

        <div class="form-group">
          <label for="publisher">journal's publisher</label>
          <input id = "publisher" class="form-control" name = "publisher" v-model="publisher">
        </div>

        <hr/>

        <input class="btn btn-primary" type = "Submit" value = "Edit">
      </form>
  </div>
</template>

<script>
import toast from '@/utility/toast'

export default {
  name: 'JEditForm',

  props: {
    'journal': Object,
    'service': String
  },

  data () {
    return {
      errors: [],

      name: this.journal.name,
      foundation: this.journal.foundation,
      publisher: this.journal.publisher,
      uuid: this.journal.uuid,

      api: this.service
    }
  },

  watch: {
    publisher (newJournal, oldJournal) {
      this.uuid = newJournal.uuid
      this.name = newJournal.name
      this.editor = newJournal.editor
      this.address = newJournal.address
      this.journals = newJournal.journals
    }
  },

  methods: {
    checkForm (e) {
      this.errors = []
      if (!this.name) { this.errors.push('journal\'s name is required') }

      if (!this.foundation) { this.errors.push('journal\'s foundation must not be empty') }

      if (!this.publisher) { this.errors.push('journal\'s publisher must not be empty') }

      if (!this.errors.length) {
        this.editJournal()
      }
      e.preventDefault()
    },

    editJournal () {
      this.$http.patch(`${this.api}${this.uuid}/`,
        {
          'uuid': this.uuid,
          'name': this.name,
          'foundation': this.foundation,
          'publisher': this.publisher
        }
      ).then(response => {
        toast.success('journal edited')
      })
        .catch(error => {
          toast.error(error.response.data.errors)
        })
    }
  },

  computed: {
    has_data () {
      return this.uuid !== undefined
    }
  }
}
</script>
