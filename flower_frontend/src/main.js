import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import { createStore } from 'vuex'
import App from './App.vue'
import routes from './router' // Ensure your routes are exported as an array
import storeOptions from './store' // Ensure your store options are exported

// Please note that ElementUI is not yet compatible with Vue 3
// import ElementUI from 'element-ui'
// import locale from 'element-ui/lib/locale/lang/fr'
// import 'element-ui/lib/theme-chalk/index.css'

import VueCookies from 'vue-cookies'

import authentication from '@/modules/authentication'
import navigation from '@/modules/navigation'
import dashboard from '@/modules/dashboard'
import etudes from '@/modules/etudes'
import membres from '@/modules/membres'
import prospects from '@/modules/prospects'
import router from './router'

const routerInstance = createRouter({
  history: createWebHistory(),
  routes: router.options.routes,
})

const store = createStore(storeOptions)

const app = createApp(App)
app.use(routerInstance)
app.use(store)
// app.use(ElementUI, { locale }) // Commented out until ElementUI is compatible with Vue 3
app.use(VueCookies)
app.mount('#app')