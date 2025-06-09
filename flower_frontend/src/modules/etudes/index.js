const module = {
  install (app) {
    app.component(
      "EtudeVoir",
      () => import("./views/EtudeVoir")
    )
  }
}

export default module
