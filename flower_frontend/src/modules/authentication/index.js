const authentication = {
  install (Vue) {
    Vue.component(
      "Authentication",
      () => import("./components/AuthenticationComponent")
    )
  }
}

export default authentication
