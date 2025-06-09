const authentication = {
  install (app) {
    app.component(
      "Authentication",
      () => import("./components/AuthenticationComponent.vue")
    )
  }
}

export default authentication
