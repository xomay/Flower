const navigation = {
  install (Vue) {
    Vue.component(
      "Navigation",
      () => import("./components/Navigation")
    )
    Vue.component(
      "BaseComponent",
      () => import("./components/Base")
    )
  }
}

export default navigation
