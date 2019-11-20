<template>
  <div id = "publisher-edit" class = "container">

    <div class = "container">
        <label>Publisher</label>
        <span class="label label-primary">{{ uuid }}</span>
    </div>

    <div class="form-group">
      <label for="journal">Journal</label>
      <input id = "journal" class="form-control" name = "journal" v-model="newJournal">
      <br/>
      <button class="btn btn-primary" name = "add_journal" v-on:click="add_journal">Add journal</button>
    </div>

    <form @submit="checkForm" novalidate="true">
        <div class="row error" v-if="errors.length">
            <b>Correct following errors:</b>
            <ul class="list-group">
                <li class="list-group-item list-group-item-danger" v-for="error in errors" :key="error">{{ error }}</li>
            </ul>
        </div>

        <div class="form-group">
          <label for="name">Publisher's name</label>
          <input id = "name" class="form-control" name = "name" v-model="name">
        </div>

        <div class="form-group">
          <label for = "editor">Publisher's editor</label>
          <input id = "editor" class="form-control" name = "editor" v-model="editor">
        </div>

        <div class="form-group">
          <label for="address">Publisher's address</label>
          <input id = "address" class="form-control" name = "address" v-model="address">
        </div>

        <div class="form-group">
          <label for = "journals">Journals:</label>
          <br/>
          <ul class="list-group" name = "journals" id = "journals">
              <li class="list-group-item list-group-item-primary" v-for="(journal, index) in journals" :key="journal">
                {{ journal.uuid }}
                <button type="button" class="close" aria-label="delete" v-on:click="delete_journal(index)">
                  <span aria-hidden="true">&times;</span>
                </button>
              </li>
          </ul>

          <hr/>
        </div>

        <input class="btn btn-primary" type = "Submit" value = "Edit">
      </form>
  </div>
</template>

<script>
import toast from '@/utility/toast'

export default {
  name: 'PEditForm',

  props: {
    'publisher': Object,
    'service': String
  },

  data () {
    return {
      errors: [],

      uuid: this.publisher.uuid,
      name: this.publisher.name,
      editor: this.publisher.editor,
      address: this.publisher.address,
      journals: this.publisher.journals,

      newJournal: ''
    }
  },

  watch: {
    publisher (newPublisher, oldPublisher) {
      this.uuid = newPublisher.uuid
      this.name = newPublisher.name
      this.editor = newPublisher.editor
      this.address = newPublisher.address
      this.journals = newPublisher.journals
    }
  },

  methods: {
    delete_journal (index) {
      this.journals.splice(index, 1)
    },

    add_journal (event) {
      this.journals.push({uuid: this.newJournal})
    },

    checkForm (event) {
      this.errors = []
      if (!this.name) { this.errors.push('Publisher\'s name must not be empty') }

      if (!this.editor) { this.errors.push('Publisher\'s editor must not be empty') }

      if (!this.address) { this.errors.push('Publisher\'s address must not be empty') }

      if (!this.journals || this.journals.length === 0) { this.errors.push('Publisher\'s journals must not be empty') }

      if (this.errors.length === 0) {
        this.editPublisher()
      } else {
        event.preventDefault()
      }
    },

    editPublisher () {
      this.$http.patch(`${this.service}${this.uuid}`,
        {
          'uuid': this.uuid,
          'name': this.name,
          'editor': this.editor,
          'address': this.address,
          'journals': this.journals
        }
      ).then(response => {
        toast.success('Publisher created')
      })
        .catch(error => {
          toast.error(error.message)
        })
    }
  }
}
</script>
