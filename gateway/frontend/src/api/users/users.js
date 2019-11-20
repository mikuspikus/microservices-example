import { HTTP } from './common'

export const User = {
  create (config) {
    return HTTP.post('/users/', config).then(response => {
      return response.data
    })
  },
  delete (user) {
    return HTTP.delete(`/users/${user.id}/`)
  },
  list () {
    return HTTP.get('/users/').then(response => {
      return response.data
    })
  }
}