const routes = [
  {
    path: "realisateurs",
    name: "realisateurs",
    component: () => import("../../membres/views/AssoVoir.vue")
  },
  {
    path: "realisateurs/:id/voir",
    name: "realisateurs-details",
    component: () => import("../views/RealisateursDetail")
  },
  {
    path: "realisateurs/:id/modifier",
    name: "realisateurs-modifier",
    component: () => import("../views/RealisateursModifier")
  },
  {
    path: "realisateurs/ajouter",
    name: "realisateurs-ajouter",
    component: () => import("../views/RealisateursCreer")
  },
]

export default routes
