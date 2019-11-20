import 'izitoast/dist/css/iziToast.min.css'
import izitoast from 'izitoast'

const toast = {
  error: (message, title = 'Error') => {
    return izitoast.error({
      title: title,
      message: message,
      position: 'bottomCenter'
    })
  },
  success: (message, title = 'Success') => {
    return izitoast.success({
      title: title,
      message: message,
      position: 'bottomCenter'
    })
  }
}

export default toast
