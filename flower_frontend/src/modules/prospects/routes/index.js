const routes = [
  {
    path: "prospects",
    name: "prospects",
    component: () => import("../views/ProspectsVoir")
  },
  {
    path: "prospects/ajouter",
    name: "prospects-ajouter",
    component: () => import("../views/ProspectsCreer")
  },
  {
    path: "prospects/actionCommerciale/:id/voir",
    name: "actionCommerciale-detail",
    component: () => import("../views/ActionCommercialeDetail")
  },
  {
    path: "prospects/actionCommerciale/:id/modifier",
    name: "actionCommerciale-modifier",
    component: () => import("../views/ActionCommercialeModifier")
  },
  {
    path: "prospects/actionCommerciale/ajouter",
    name: "actionCommerciale-ajouter",
    component: () => import("../views/ActionCommercialeCreer")
  },
  {
    path: "prospects/actionCommerciale/",
    name: "actionCommerciale-voir",
    component: () => import("../views/ActionCommercialeVoir")
  },
  {
    path: "prospects/:id/voir",
    name: "prospects-detail",
    component: () => import("../views/ProspectsDetail")
  },
  {
    path: "prospects/:id/modifier",
    name: "prospects-modifier",
    component: () => import("../views/ProspectsModifier")
  },
  {
    path: "prospects/:id/employes/ajouter",
    name: "employes-ajouter",
    component: () => import("../views/EmployesCreer")
  },
  {
    path: "prospects/:id/employes/:employe_id/voir",
    name: "employes-detail",
    component: () => import("../views/EmployesDetail")
  },
  {
    path: "prospects/:id/employes/:employe_id/modifier",
    name: "employes-modifier",
    component: () => import("../views/EmployesModifier")
  },
  {
    path: "generation/devis",
    name: "generation-devis",
    component: () => import("../views/Devis")
  }
]

export default routes
