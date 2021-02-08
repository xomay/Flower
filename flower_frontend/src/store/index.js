import Vue from "vue"
import Vuex from "vuex"

Vue.use(Vuex)

export default new Vuex.Store({
  currentUser: {
    username: "",
    isAdmin: false
  },
  // Je n'utilise pas les véritables propriétées de Vuex, mais... ça fonctionne ? ^^
  state: {
  },
  mutations: {
  },
  getters: {
  }
})
