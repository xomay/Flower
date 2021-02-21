const routes = [
  {
    path: "tresorerie/factures",
    name: "factures-choice-etudes",
    component: () => import("../views/FactureSelectEtude")
  },
  {
    path: "tresorerie/factures/:id/",
    name: "factures-choice-type",
    component: () => import("../views/FactureAboutEtude")
  }
]

export default routes
