const module = {
  install (Vue) {
    Vue.component(
      "EtudeVoir",
      () => import("./views/EtudeVoir")
    )
  }
}

export default module
