<template>
  <div id = "ATable">
    <template v-if="has_data">
      <BTable
        :fields="fields"
        :busy="has_data"
        :items="data"
        :bordered="true"
        responsive="sm"
      >
        <template v-slot:cell(uuid)="{ value, index }">
          <router-link
            :to="{ name: 'article', params: {uuid: value} }"
          >
            {{ value }}
          </router-link>
        </template>

        <template v-slot:cell(authors)="{ value, item }">
          <template v-if="value.length">
          <router-link
            v-for="author in value" :key="author"
            :to="{ name: 'users', params: {uuid: author.author_uuid} }"
          >
            {{ author.author_uuid }}
          </router-link>
          </template>
          <b v-else>
            No data
          </b>
        </template>
      </BTable>
    </template>
    <template v-else>
      <span>No data has been provided</span>
    </template>
  </div>
</template>

<script>
import {BTable} from 'bootstrap-vue'

export default {
  name: 'ATable',

  props: {
    data: {
      type: Array,
      default () { return [] }
    },

    fields: [
      { key: 'uuid', label: 'UUID' },
      { key: 'authors', labela: 'Authors' },
      { key: 'title', labela: 'Title' },
      { key: 'added', labela: 'Added at' },
      { key: 'published', labela: 'Published at' },
      { key: 'journal', labela: 'Journal' }
    ]
  },

  components: {
    'BTable': BTable
  },

  methods: {
    formatAuthors (authors) {
      let result = authors.map((j) => j.author_uuid).join(', ')

      return result === '' ? 'No data' : result
    }
  },

  computed: {
    has_data () { return this.data.length !== 0 }
  }
}
</script>
