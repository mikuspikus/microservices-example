import Vue from 'vue'
import Router from 'vue-router'
import store from '@/store'

import Home from '@/views/generic/Home.vue'

import Users from '@/views/users/Users.vue'
import Articles from '@/views/articles/Articles.vue'
import Publishers from '@/views/publishers/Publishers.vue'
import Journals from '@/views/journals/Journals.vue'

import Journal from '@/views/journals/Journal.vue'
import Publisher from '@/views/publishers/Publisher.vue'

import Login from '@/components/users/Login.vue'
import Logout from '@/components/users/Logout.vue'
import Register from '@/components/users/Register.vue'

import NotFound from '@/views/generic/NotFound.vue'
import UnprocessableEntity from '@/views/generic/UnprocessableEntity.vue'

Vue.use(Router)

const router = new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    // Users
    {
      path: '/users/',
      name: 'users',
      component: Users,
      meta: {
        requiresAuthorization: true
      }
    },

    {
      path: '/login',
      name: 'login',
      component: Login
    },

    {
      path: '/logout',
      name: 'logout',
      component: Logout
    },

    {
      path: '/register',
      name: 'register',
      component: Register
    },
    // ,
    // {
    //   path: '/users/:id',
    //   name: 'user',
    //   component: User
    // },

    // Articles
    {
      path: '/articles/',
      name: 'articles',
      component: Articles
    },
    // {
    //   path: '/articles/:uuid',
    //   name: 'article',
    //   component: Article,
    //   meta: {
    //    requiresAuthorization: true
    //   }
    // },

    // Journals
    {
      path: '/journals/',
      name: 'journals',
      component: Journals
    },
    {
      path: '/journals/:uuid',
      name: 'journal',
      component: Journal,
      meta: {
        requiresAuthorization: true
      }
    },

    // Publishers
    {
      path: '/publishers/',
      name: 'publishers',
      component: Publishers
    },
    {
      path: '/publishers/:uuid',
      name: 'publisher',
      component: Publisher,
      meta: {
        requiresAuthorization: true
      }
    },

    // Errors
    {
      path: '/422',
      name: 'UnprocessableEntity',
      component: UnprocessableEntity
    },
    {
      path: '/404',
      name: 'NotFound',
      component: NotFound
    }
  ]
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuthorization)) {
    if (store.getters.isLoggedIn) {
      next()
      return
    }
    next('/login')
  } else {
    next()
  }
})

export default router
