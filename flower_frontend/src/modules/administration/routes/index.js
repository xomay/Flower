const routes = [
  {
    path: "administration/params",
    name: "parametres-je",
    component: () => import("../views/ParamsJEView")
  },
  {
    path: "administration/postes",
    name: "postes-je",
    component: () => import("../views/PostesEdition")
  }
]

export default routes
