const routes = [
  {
    path: "/login",
    name: "Login",
    component: () => import("../views")
  },
  {
    path: "/passwordreset",
    name: "password-reset",
    component: () => import("../views/PasswordReset")
  },
  {
    path: "/passwordreset/confirm/:token",
    name: "password-reset-confirm",
    component: () => import("../views/NewPassword")
  },
]

export default routes
