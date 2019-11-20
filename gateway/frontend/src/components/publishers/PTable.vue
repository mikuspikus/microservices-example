<template>
  <div id = "PTable">
    <template v-if="has_data">
      <BTable :fields="fields" :items="data" :bordered="true" responsive="sm">

        <template v-slot:cell(uuid)="{ value, index }">
          <router-link
            :to="{ name: 'publisher', params: {uuid: value} }"
          >
            {{ value }}
          </router-link>
        </template>

        <template v-slot:cell(journals)="{ value, item }">
          <template v-if="value.length">
          <router-link
            v-for="journal in value" :key="journal"
            :to="{ name: 'journal', params: {uuid: journal.uuid} }"
          >
            {{ journal.uuid }}
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
  name: 'PTable',

  props: {
    data: {
      type: Array,
      default () { return [] }
    },

    api: String,

    fields: [
      'uuid',
      'name',
      'editor',
      'address',
      'journals'
    ]
  },

  components: {
    'BTable': BTable
  },

  methods: {
    formatJournals (journals) {
      let result = journals.map((j) => j.uuid).join(', ')

      return result === '' ? 'No data' : result
    }
  },

  computed: {
    has_data () { return this.data.length !== 0 }
  }
}
</script>
