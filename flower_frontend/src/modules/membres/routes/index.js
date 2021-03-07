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
  },
  // Spécial case
  {
    path: "membres/:id/redirect",
    name: "membres-redirect",
    component: () => import("../views/RedirectToAnother")
  }
]

export default routes
