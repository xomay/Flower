const routes = [
  {
    path: "etudes/ajouter",
    name: "etudes-ajouter",
    component: () => import("../views/project/EtudeCreer")
  },
  {
    path: "etudes",
    name: "etudes",
    component: () => import("../views/EtudeVoir")
  },
  {
    path: "etudes/:id/modifier",
    name: "etudes-modifier",
    component: () => import("../views/project/EtudeModifier")
  },
  {
    path: "etudes/:id/voir",
    name: "etudes-details",
    component: () => import("../views/project/EtudeDetail")
  },
  {
    path: "etudes/:id/phases",
    name: "etudes-phases",
    component: () => import("../views/PhaseModifier")
  },
  {
    path: "etudes/:id/convention-etude",
    name: "etudes-convention-etude",
    component: () => import("../views/projectConvention/EtudeConvention")
  },
  {
    path: "etudes/:id/missions",
    name: "etudes-missions",
    component: () => import("../views/MissionCreer")
  },
  {
    path: "etudes/:id/factures/ajouter",
    name: "etudes-factures",
    component: () => import("../views/invoice/InvoiceCreate")
  },
  {
    path: "etudes/:id/factures/modifier/:facture_id",
    name: "etudes-factures-modifier",
    component: () => import("../views/invoice/InvoiceModify")
  },
  {
    path: "etudes/:id/pvr/ajouter",
    name: "etudes-pvr-ajouter",
    component: () => import("../views/PVRCreator")
  },
  {
    path: "etudes/:id/pvr/modifier/:pvr_id",
    name: "etudes-pvr-modifier",
    component: () => import("../views/PVREditor")
  },
  {
    path: "etudes/:id/commentaires/:realisateur_id/ajouter",
    name: "etudes-commentaire-ajouter",
    component: () => import("../views/comments/NewComment")
  },
  // Accès réalisateur
  {
    path: "etudes/acces-rea",
    name: "etudes-acces-rea",
    component: () => import("../views/ReaEtudesVoir")
  },
  {
    path: "etudes/acces-rea/:id/voir",
    name: "etudes-acces-rea-detail",
    component: () => import("../views/project/ReaEtudeDetail")
  }
]

export default routes
