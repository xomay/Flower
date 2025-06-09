import { defineAsyncComponent } from "vue"

const navigation = {
  install (app) {
    app.component(
      "Navigation",
      defineAsyncComponent(() => import("./components/Navigation.vue"))
    )
    app.component(
      "BaseComponent",
      defineAsyncComponent(() => import("./components/Base.vue"))
    )
  }
}

export default navigation
