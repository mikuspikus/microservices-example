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
      <!-- <b-spinner/> -->
      <b>Loading data...</b>
    </template>

  </div>
</template>

<script>
import {BTable, BSpinner} from 'bootstrap-vue'

export default {
  name: 'PTable',

  props: {
    data: {
      type: Array,
      default () { return [] }
    },

    api: String
  },

  data () {
    return {
      fields: [
        { key: 'uuid', label: 'UUID' },
        { key: 'name', label: 'Name' },
        { key: 'editor', label: 'Editor' },
        { key: 'address', label: 'Address' },
        { key: 'journals', label: 'Journals' }
      ]
    }
  },

  components: {
    'BTable': BTable,
    'b-spinner': BSpinner
  },

  computed: {
    has_data () { return this.data.length !== 0 }
  }
}
</script>
