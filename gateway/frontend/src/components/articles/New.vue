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
          <label for="title">Article title</label>
          <input id = "title" class="form-control" name = "title" v-model="title">
        </div>

        <div class="form-group">
          <label for = "published">Publishing date</label>
          <input id = "published" class="form-control" name = "published" v-model="published">
        </div>

        <div class="form-group">
          <label for="journal">Journal</label>
          <input id = "journal" class="form-control" name = "journal" v-model="journal">
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
  name: 'APostForm',
  data () {
    return {
      errors: [],
      title: null,
      published: null,
      journal: null,
      authors: [],
      newAuthor: ''
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
      if (!this.title) { this.errors.push('Article title is required') }

      if (!this.journal) { this.errors.push('Journal must not be empty') }

      if (this.authors.length === 0) { this.errors.push('Article must have at least one author') }

      if (!this.published) { this.errors.push('Publishing date must not be empty') }

      if (!this.errors.length) {
        this.submitArticle()
      }
      e.preventDefault()
    },
    submitArticle () {
      this.$http.post('articles/', JSON.stringify(
        {
          'title': this.title,
          'published': this.published,
          'journal': this.journal,
          'authors': this.authors
        }
      )).then(response => {
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
