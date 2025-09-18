const routes = [
  {
    path: "membres",
    name: "membres",
    component: () => import("../views/AssoVoir")
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
  // Redirection entre les membres
  {
    path: "membres/:id/redirect",
    name: "membres-redirect",
    component: () => import("../views/RedirectToAnother")
  },
  // Profil
  {
    path: "profil",
    name: "profil",
    component: () => import("../views/ProfileView")
  }
]

export default routes
