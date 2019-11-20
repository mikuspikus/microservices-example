<template>
  <div class = "container">

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
          <label for="address">Publisher's editor</label>
          <input id = "address" class="form-control" name = "address" v-model="address">
        </div>

        <div class="form-group">
          <label for = "journals">Journals:</label>
          <br/>
          <ul class="list-group" name = "journals" id = "journals">
              <li class="list-group-item list-group-item-primary" v-for="(journal, index) in journals" :key="journal">
                {{ journal }}
                <button type="button" class="close" aria-label="delete" v-on:click="delete_journal(index)">
                  <span aria-hidden="true">&times;</span>
                </button>
              </li>
          </ul>

          <hr/>
        </div>

        <input class="btn btn-primary" type = "Submit" value = "Submit">
      </form>
  </div>
</template>

<script>
import toast from '@/utility/toast'

export default {
  name: 'PPostForm',
  data () {
    return {
      errors: [],
      name: null,
      editor: null,
      address: null,
      journals: [],
      newJournal: ''
    }
  },
  methods: {
    delete_journal (index) {
      this.journals.splice(index, 1)
    },
    add_journal (event) {
      this.journals.push(this.newJournal)
    },
    checkForm (e) {
      this.errors = []
      if (!this.name) { this.errors.push('Publisher\'s name must not be empty') }

      if (!this.editor) { this.errors.push('Publisher\'s editor must not be empty') }

      if (!this.address) { this.errors.push('Publisher\'s address must not be empty') }

      if (this.journals.length === 0) { this.errors.push('Publisher\'s journals must not be empty') }

      if (!this.errors.length) {
        this.submitPublisher()
      }
      e.preventDefault()
    },
    submitPublisher () {
      this.$http.post('publishers/',
        {
          'name': this.name,
          'editor': this.editor,
          'address': this.address,
          'journals': this.journals
        }
      ).then(response => {
        toast.success('Publisher created')
        this.$router.push('/publishers/' + response.data.id)
      })
        .catch(error => {
          toast.error(error.message)
        })
    }
  }
}
</script>
