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
  },
  {
    path: "administration/uploads",
    name: "uploads-je",
    component: () => import("../views/UploadManagement")
  },
  {
    path: "administration/doctypes",
    name: "doctypes-je",
    component: () => import("../views/DoctypeConfig")
  }
]

export default routes
