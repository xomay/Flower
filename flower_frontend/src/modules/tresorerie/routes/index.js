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
    path: "tresorerie/nfs/voir/normales",
    name: "nfs-voir-normales",
    component: () => import("../views/NFsVoir")
  },
  {
    path: "tresorerie/nfs/:id/voir",
    name: "nfs-detail",
    component: () => import("../views/NFsDetail")
  }
]

export default routes
