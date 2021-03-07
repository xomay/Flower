import Vue from "vue"
import VueRouter from "vue-router"
import Home from "../views/Home.vue"

//import authenticationRoutes from "@/modules/authentication/routes"
import etudesRoutes from "@/modules/etudes/routes"
import membresRoutes from "@/modules/membres/routes"
import prospectsRoutes from "@/modules/prospects/routes"
import dashboardRoutes from "@/modules/dashboard/routes"
import performancesRoutes from "@/modules/performances/routes"
import realisateursRoutes from "@/modules/realisateurs/routes"
import administrationRoutes from "@/modules/administration/routes"
import tresorerieRoutes from "@/modules/tresorerie/routes"
import error404Routes from "@/modules/error404/routes"

Vue.use(VueRouter)

const routes = [
    // Alors, à cause du système de E404 qui va tout gober, on ne doit mettre les authentificationavant le reste. Désolé :(
    {path: "/login", name: "Login",
      component: () => import("@/modules/authentication/views")},
    {path: "/passwordreset", name: "password-reset",
      component: () => import("@/modules/authentication/views/PasswordReset")},
    {path: "/passwordreset/confirm/:token", name: "password-reset-confirm",
      component: () => import("@/modules/authentication/views/NewPassword")},
    {
      path: "/",
      name: "Home",
      component: Home,
      children: [
        administrationRoutes,
        etudesRoutes,
        membresRoutes,
        prospectsRoutes,
        dashboardRoutes,
        performancesRoutes,
        realisateursRoutes,
        tresorerieRoutes,
        error404Routes
      ].flat()
    }
  ],

  router = new VueRouter({
    routes, mode: "history"
  })
//router.addRoutes(authenticationRoutes)

export default router
