const routes = [
    //routes pour les etudes en mode simulation
    {
        path: "simulation/etudes/ajouter",
        name: "simulation-etudes-ajouter",
        component: () => import("@/modules/etudes/views/project/EtudeCreer"),
        meta : { type: 'simulation' }
    },
    {
        path: "simulation/etudes/ajoutercc",
        name: "simulation-etudes-ajoutercc",
        component: () => import("@/modules/etudes/views/projectConvention/ConvCadreCreer.vue"),
        meta : { type: 'simulation' }
    },
    {
        path: "simulation/etudes",
        name: "simulation-etudes",
        component: () => import("@/modules/etudes/views/EtudeVoir"),
        meta : { type: 'simulation' }
    },
    //routes pour les membres et réalisateurs en mode simulation
    {
        path: "simulation/membres",
        name: "simulation-membres",
        component: () => import("@/modules/membres/views/AssoVoir.vue"),
        meta : { type: 'simulation' }
    },
    {
        path: "simulation/realisateurs/ajouter",
        name: "simulation-realisateurs-ajouter",
        component: () => import("@/modules/realisateurs/views/RealisateursCreer"),
        meta : { type: 'simulation' }
    },
    //routes pour les prospects en mode simulation
    {
        path: "simulation/prospects",
        name: "simulation-prospects",
        component: () => import("@/modules/prospects/views/ProspectsVoir"),
        meta : { type: 'simulation' }
    },
    {
        path: "simulation/prospects/ajouter",
        name: "simulation-prospects-ajouter",
        component: () => import("@/modules/prospects/views/ProspectsCreer"),
        meta : { type: 'simulation' }
    },
    {
        path: "simulation/prospects/actionCommerciale/ajouter",
        name: "simulation-actionCommerciale-ajouter",
        component: () => import("@/modules/prospects/views/ActionCommercialeCreer"),
        meta : { type: 'simulation' }
    },
    {
        path: "simulation/prospects/actionCommerciale/",
        name: "simulation-actionCommerciale-voir",
        component: () => import("@/modules/prospects/views/ActionCommercialeVoir"),
        meta : { type: 'simulation' }
    },
]

export default routes;