import Vue from "vue"
import VueRouter from "vue-router"
import Home from "../views/Home.vue"

import authenticationRoutes from "@/modules/authentication/routes"
import etudesRoutes from "@/modules/etudes/routes"
import membresRoutes from "@/modules/membres/routes"
import prospectsRoutes from "@/modules/prospects/routes"
import dashboardRoutes from "@/modules/dashboard/routes"
import performancesRoutes from "@/modules/performances/routes"
import realisateursRoutes from "@/modules/realisateurs/routes"
import error404Routes from "@/modules/error404/routes"

Vue.use(VueRouter)

const routes = [
    {
      path: "/",
      name: "Home",
      component: Home,
      children: [
        etudesRoutes,
        membresRoutes,
        prospectsRoutes,
        dashboardRoutes,
        performancesRoutes,
        realisateursRoutes,
        error404Routes
      ].flat()
    }
  ],

  router = new VueRouter({
    routes
  })
router.addRoutes(authenticationRoutes)

/*
 * Router.options.routes.find(r => r.path === '/').children.addRoutes(etudesRoutes)
 * router.addRoutes(etudesRoutes)
 */

export default router
