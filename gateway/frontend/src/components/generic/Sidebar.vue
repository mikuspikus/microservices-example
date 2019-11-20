<template>
    <div class = "col-sm-3 col-md-2 sidebar">
            <ul class = "nav nav-sidebar">
              <li>
                <router-link to = "/users">Users</router-link>
              </li>

              <li>
                <router-link to = "/articles">Articles</router-link>
              </li>

              <li>
                <router-link to = "/journals">Journals</router-link>
              </li>

              <li>
                <router-link to = "/publishers">Publishers</router-link>
              </li>
            </ul>
          </div>
</template>

<script>
export default {
  name: 'Sidebar'
}
</script>
