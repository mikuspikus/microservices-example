<template>
  <div class = "container">

    <form @submit="checkJForm" novalidate="true">

      <div class="row error" v-if="jerrors.length">
        <b>Correct following errors:</b>
        <ul class="list-group">
          <li class="list-group-item list-group-item-danger" v-for="error in jerrors" :key="error">{{ error }}</li>
        </ul>
      </div>

      <div class="form-group">
        <label for="name">Journal's name</label>
        <input id = "name" class="form-control" name = "name" v-model="jname">
      </div>

      <div class="form-group">
        <label for = "foundation">Date of journal's foundation</label>
        <input id = "foundation" class="form-control" name = "foundation" v-model="jfoundation">
      </div>

      <input class="btn btn-primary" type = "Submit" value = "Add journal">

    </form>

    <form @submit="checkPForm" novalidate="true">
        <div class="row error" v-if="perrors.length">
            <b>Correct following errors:</b>
            <ul class="list-group">
                <li class="list-group-item list-group-item-danger" v-for="error in perrors" :key="error">{{ error }}</li>
            </ul>
        </div>

        <div class="form-group">
          <label for="name">Publisher's name</label>
          <input id = "name" class="form-control" name = "name" v-model="pname">
        </div>

        <div class="form-group">
          <label for = "editor">Publisher's editor</label>
          <input id = "editor" class="form-control" name = "editor" v-model="peditor">
        </div>

        <div class="form-group">
          <label for="address">Publisher's editor</label>
          <input id = "address" class="form-control" name = "address" v-model="paddress">
        </div>

        <div class="form-group">
          <label for = "journals">Journals:</label>
          <br/>
          <ul class="list-group" name = "journals" id = "journals">
              <li class="list-group-item list-group-item-primary" v-for="(journal, index) in journals" :key="journal">
                <div class="row vdivide">

                  <div class="col-xs-3">Name: {{ journal.name }}</div>
                  <div class="col-xs-2 v-divider">Foundation: {{ journal.foundation}}</div>

                  <button type="button" class="close" aria-label="delete" v-on:click="delete_journal(index)">
                    <span aria-hidden="true">&times;</span>
                  </button>

                </div>
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
  name: 'PComplexForm',

  props: {
    api: {type: String, default: '/publishers/'},
    instruction: {type: String, default: 'journal/'}
  },

  data () {
    return {
      perrors: [],
      pname: null,
      peditor: null,
      paddress: null,
      journals: [],

      jerrors: [],
      jname: null,
      jfoundation: null
    }
  },
  methods: {
    delete_journal (index) {
      this.journals.splice(index, 1)
    },
    add_journal (event) {
      this.journals.push(this.newJournal)
    },
    checkPForm (e) {
      this.perrors = []
      if (!this.name) { this.perrors.push('Publisher\'s name must not be empty') }

      if (!this.editor) { this.perrors.push('Publisher\'s editor must not be empty') }

      if (!this.address) { this.perrors.push('Publisher\'s address must not be empty') }

      if (this.journals.length === 0) { this.errors.push('Publisher\'s journals must not be empty') }

      if (!this.perrors.length) {
        this.submitPublisher()
      }
      e.preventDefault()
    },
    checkJForm (e) {
      this.jerrors = []

      if (!this.jname) { this.jerrors.push('Journal\'s name must not be empty') }
      if (!this.jfoundation) { this.jerrors.push('Journal\'s foundation must not be empty') }

      if (!this.jerrors.length) {
        this.journals.push({'name': this.jname, 'foundation': this.jfoundation})
      }

      e.preventDefault()
    },
    submitPublisher () {
      this.$http.post(`${this.api}${this.instruction}`,
        {
          'publisher': {
            'name': this.name,
            'editor': this.editor,
            'address': this.address
          },
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
