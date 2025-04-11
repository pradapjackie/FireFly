import React from 'react';

export const pagesRoutes = [
    {
        path: '/auto/history/:folder/:testRunId',
        component: React.lazy(() => import('pages/RunHistory')),
    },
    {
        path: '/auto/:folder',
        component: React.lazy(() => import('pages/RunAutotest')),
    },
    {
        path: '/script_runner/:folder',
        component: React.lazy(() => import('pages/ScriptRunner')),
    },
    {
        path: '/load_test/:folder',
        component: React.lazy(() => import('pages/LoadTest')),
    },
    {
        path: '/health',
        component: React.lazy(() => import('pages/ComingSoon')),
    },
    {
        path: '/mock',
        component: React.lazy(() => import('pages/ComingSoon')),
    },
    {
        path: '/user-profile',
        component: React.lazy(() => import('pages/ComingSoon')),
    },
    {
        path: '/user-settings',
        component: React.lazy(() => import('pages/ComingSoon')),
    },
];
