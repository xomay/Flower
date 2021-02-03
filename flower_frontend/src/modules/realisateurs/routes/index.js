const routes = [
  {
    path: "realisateurs",
    name: "realisateurs",
    component: () => import("../views/RealisateursVoir")
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
]

export default routes
