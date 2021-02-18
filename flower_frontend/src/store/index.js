import Vue from "vue"
import Vuex from "vuex"

Vue.use(Vuex)

export default new Vuex.Store({
  currentUser: {// Update dans AuthenticationComponent et App.vue
    username: "",// Get dans Navigation & dashboard
    roles: []
  },
  hasRole (role) {
    console.log(role)
    return this.currentUser.roles.includes(role)
  },
  // Je n'utilise pas les véritables propriétées de Vuex, mais... ça fonctionne ? ^^
  state: {
  },
  mutations: {
  },
  getters: {
    hasRole (r) {
      console.log("ouif")
      return r
    }
  }
})
