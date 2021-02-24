const routes = [
  // Factures :
  {
    path: "tresorerie/factures",
    name: "factures-choice-etudes",
    component: () => import("../views/FactureSelectEtude")
  },
  {
    path: "tresorerie/factures/:id/",
    name: "factures-choice-type",
    component: () => import("../views/FactureAboutEtude")
  },
  // NF :
  {
    path: "tresorerie/nfs/voir/",
    name: "nfs-voir",
    component: () => import("../views/NFsVoir")
  },
  {
    path: "tresorerie/nfs/:id/voir",
    name: "nfs-detail",
    component: () => import("../views/NFsDetail")
  },
  {
    path: "tresorerie/nfs/:id/modifier",
    name: "nfs-modifier",
    component: () => import("../views/NFsModifier")
  }
]

export default routes
