const routes = [
  {
    path: "/performance/devco",
    name: "performances-devco",
    component: () => import("../views/PerfDevCo")
  },
  {
    path: "/performance/ticket",
    name: "performances-ticket",
    component: () => import("../views/Ticket")
  },
]

export default routes
