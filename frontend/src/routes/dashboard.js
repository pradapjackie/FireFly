import React from 'react';

export const dashboardRoutes = [
  {
    path: '/dashboard',
    component: React.lazy(() => import('pages/Dashboard')),
  },
  {
    path: '/alternative',
    component: React.lazy(() => import('pages/Dashboard2')),
  },
];
