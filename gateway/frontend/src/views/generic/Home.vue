<template>
  <div id = "home"></div>
</template>

<script>

export default {
  name: 'home',

  components: {
  },

  props: {
    user: {
      default: () => { return {} },
      type: Object
    }
  },
  data () {
    return {
    }
  }
}
</script>
