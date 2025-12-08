import { createApp, h } from 'vue'
import Toast from '../components/Toast.vue'

export default {
  install(app) {
    const toastContainer = document.createElement('div')
    document.body.appendChild(toastContainer)

    const toastApp = createApp({
      render() {
        return h(Toast, {
          ref: 'toastRef'
        })
      }
    })

    const toastInstance = toastApp.mount(toastContainer)

    const toast = {
      info(message, title = '', options = {}) {
        toastInstance.addToast({ 
          type: 'info', 
          message, 
          title, 
          ...options 
        })
      },
      success(message, title = '', options = {}) {
        toastInstance.addToast({ 
          type: 'success', 
          message, 
          title, 
          ...options 
        })
      },
      warning(message, title = '', options = {}) {
        toastInstance.addToast({ 
          type: 'warning', 
          message, 
          title, 
          ...options 
        })
      },
      error(message, title = '', options = {}) {
        toastInstance.addToast({ 
          type: 'error', 
          message, 
          title, 
          ...options 
        })
      }
    }

    app.config.globalProperties.$toast = toast
    app.provide('toast', toast)
  }
}
