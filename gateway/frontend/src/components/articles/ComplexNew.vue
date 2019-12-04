<template>
  <div class = "container">

    <div class="form-group">
    <label for="author">Author</label>
      <input id = "author" class="form-control" name = "author" v-model="newAuthor">
      <br/>
      <button class="btn btn-primary" name = "add_author" v-on:click="add_author">Add author</button>
    </div>

    <form @submit="checkForm" novalidate="true">
        <div class="row error" v-if="errors.length">
            <b>Correct following errors:</b>
            <ul class="list-group">
                <li class="list-group-item list-group-item-danger" v-for="error in errors" :key="error">{{ error }}</li>
            </ul>
        </div>

        <div class="form-group">
          <label for="atitle">Article title</label>
          <input id = "atitle" class="form-control" name = "atitle" v-model="atitle">
        </div>

        <div class="form-group">
          <label for = "apublished">Publishing date</label>
          <input id = "apublished" class="form-control" name = "apublished" v-model="apublished">
        </div>

        <div class="form-group">
          <label for="jname">Journal's name</label>
          <input id = "jname" class="form-control" name = "jname" v-model="jname">
        </div>

        <div class="form-group">
          <label for="jfoundation">Journal's foundation</label>
          <input id = "jfoundation" class="form-control" name = "jfoundation" v-model="jfoundation">
        </div>

        <div class="form-group">
          <label for = "authors">Authors:</label>
          <br/>
          <ul class="list-group" name = "authors" id = "authors">
              <li class="list-group-item list-group-item-primary" v-for="(author, index) in authors" :key="author">
                {{ author }}
                <button type="button" class="close" aria-label="delete" v-on:click="delete_author(index)">
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
  name: 'AComplexForm',

  props: {
    api: {type: String, default: '/articles/'},
    instruction: {type: String, default: 'journals/'}
  },

  data () {
    return {
      errors: [],
      atitle: null,
      apublished: null,
      authors: [],
      newAuthor: '',

      jname: null,
      jfoundation: null
    }
  },
  methods: {
    delete_author (index) {
      this.authors.splice(index, 1)
    },
    add_author (event) {
      this.authors.push(this.newAuthor)
    },
    checkForm (e) {
      this.errors = []
      if (!this.atitle) { this.errors.push('Article title is required') }

      if (!this.jname) { this.errors.push('Journal\'s name must not be empty') }
      if (!this.jfoundation) { this.errors.push('Journal\'s foundation must not be empty') }

      if (this.authors.length === 0) { this.errors.push('Article must have at least one author') }

      if (!this.apublished) { this.errors.push('Publishing date must not be empty') }

      if (!this.errors.length) {
        this.submitArticle()
      }
      e.preventDefault()
    },
    submitArticle () {
      this.$http.post(`${this.api}${this.instruction}`,
        {
          'article': {
            'title': this.title,
            'published': this.published,
            'authors': this.authors
          },
          'journal': {'name': this.jname, 'foundation': this.jfoundation}
        }
      ).then(response => {
        toast.success('Article created')
        this.$router.push('/articles/' + response.data.uuid)
      })
        .catch(error => {
          toast.error(error.message)
        })
    }
  }
}
</script>
