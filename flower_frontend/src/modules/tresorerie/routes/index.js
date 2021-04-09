const routes = [
  // Vues de trésorerie :
  {
    path: "tresorerie/etudes/",
    name: "treso-choice-etudes",
    component: () => import("../views/TresoSelectEtude")
  },
  {
    path: "tresorerie/etudes/:id/",
    name: "treso-choice-type",
    component: () => import("../views/TresoAboutEtude")
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
  },
  {
    path: "tresorerie/nfs/ajouter",
    name: "nfs-ajouter",
    component: () => import("../views/NFsCreer")
  },
  {
    path: "tresorerie/base-ursaff",
    name: "ursaff-je",
    component: () => import("../views/BaseUrsaffEdition")
  },
  // BV :
  {
    path: "tresorerie/etudes/:id/bvs/ajouter",
    name: "bv-creer",
    component: () => import("../views/BVsCreer")
  }
]

export default routes
