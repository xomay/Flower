const routes = [
  {
    path: "membres",
    name: "membres",
    component: () => import("../views/MembresVoir")
  },
  {
    path: "membres/ajouter",
    name: "membres-ajouter",
    component: () => import("../views/MembresCreer")
  },
  {
    path: "membres/:id/voir",
    name: "membres-detail",
    component: () => import("../views/MembresDetail")
  },
  {
    path: "membres/:id/modifier",
    name: "membres-modifier",
    component: () => import("../views/MembresModifier")
  }
]

export default routes
