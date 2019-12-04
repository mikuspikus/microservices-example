<template>
  <div id = "ATable">
    <template v-if="has_data">
      <BTable
        :fields="fields"
        :busy="has_data"
        :items="full_data"
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

        <template v-slot:cell(j_publisher)="{ value, index }">
          <router-link
            :to="{ name: 'publisher', params: {uuid: value} }"
          >
            {{ value }}
          </router-link>
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
  name: 'UFullTAble',

  data () {
    return {
      fields: [
        { key: 'uuid', label: 'UUID' },
        { key: 'authors', label: 'Authors' },
        { key: 'title', label: 'Title' },
        { key: 'added', label: 'Added at' },
        { key: 'published', label: 'Published at' },
        { key: 'journal', lable: 'Journal\'s UUID' },

        { key: 'j_name', label: 'Journal\'s name' },
        { key: 'j_foundation', label: 'Journal\'s foundation' },
        { key: 'j_publisher', label: 'Journal\'s publisher' }
      ]
    }
  },

  props: {
    full_data: {
      type: Array,
      default () { return [] }
    }
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
    has_data () { return this.full_data.length !== 0 }
  }
}
</script>
