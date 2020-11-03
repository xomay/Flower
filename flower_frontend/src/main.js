import Vue from "vue"
import App from "./App.vue"
import router from "./router"
import store from "./store"

import ElementUI from "element-ui"
import locale from "element-ui/lib/locale/lang/fr"
import "element-ui/lib/theme-chalk/index.css"
import VueCookies from "vue-cookies"

import authentication from "@/modules/authentication"
import navigation from "@/modules/navigation"
import dashboard from "@/modules/dashboard"
import etudes from "@/modules/etudes"
import membres from "@/modules/membres"
import prospects from "@/modules/prospects"

Vue.use(
  ElementUI,
  {locale,
    size: "medium"}
)
Vue.use(VueCookies)
Vue.use(authentication)
Vue.use(navigation)
Vue.use(dashboard)
Vue.use(etudes)
Vue.use(membres)
Vue.use(prospects)

Vue.config.productionTip = false

Vue.prototype.$server_url = "http://localhost:8000"

new Vue({
  router,
  store,
  render: (h) => h(App)
}).$mount("#app")
