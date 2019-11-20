<template>
  <div id = "CustomTable">
    <template v-if="has_data">
      <BTable striped hover :items="data" :bordered="true"></BTable>
    </template>

    <template v-else>
      <span>No data has been provided</span>
    </template>
  </div>
</template>

<script>
import {BTable} from 'bootstrap-vue'

export default {
  name: 'CustomTable',

  props: {
    data: Array,
    default () { return [] }
  },

  components: {
    'BTable': BTable
  },

  computed: {
    has_data () { return this.data.length !== 0 }
  }
}
</script>
