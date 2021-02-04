const routes = [
  {
    path: "*",
    name: "error404",
    component: () => import("../components/Error404")
  }
]

export default routes