import { createRouter, createWebHistory } from 'vue-router';

import Home from '../views/Home.vue';
// Import des routes des différents modules
import etudesRoutes from '@/modules/etudes/routes';
import membresRoutes from '@/modules/membres/routes';
import prospectsRoutes from '@/modules/prospects/routes';
import dashboardRoutes from '@/modules/dashboard/routes';
import performancesRoutes from '@/modules/performances/routes';
import realisateursRoutes from '@/modules/realisateurs/routes';
import administrationRoutes from '@/modules/administration/routes';
import tresorerieRoutes from '@/modules/tresorerie/routes';
import error404Routes from '@/modules/error404/routes';

const routes = [
  // Routes d'authentification
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/modules/authentication/views')
  },
  {
    path: '/passwordreset',
    name: 'password-reset',
    component: () => import('@/modules/authentication/views/PasswordReset.vue')
  },
  {
    path: '/passwordreset/confirm/:token',
    name: 'password-reset-confirm',
    component: () => import('@/modules/authentication/views/NewPassword.vue')
  },
  // Route principale avec les enfants
  {
    path: '/',
    name: 'Home',
    component: Home,
    children: [
      ...administrationRoutes,
      ...etudesRoutes,
      ...membresRoutes,
      ...prospectsRoutes,
      ...dashboardRoutes,
      ...performancesRoutes,
      ...realisateursRoutes,
      ...tresorerieRoutes,
      ...error404Routes
    ]
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
