import React from 'react';
import {Redirect} from 'react-router-dom';
import {dashboardRoutes} from "./dashboard";
import {redirectRoute} from "./redirect";
import {pagesRoutes} from "./pages";

const errorRoute = [{
  component: () => <Redirect to="/session/404"/>,
},];

export const routes = [
  ...dashboardRoutes,
  ...redirectRoute,
  ...pagesRoutes,
  ...errorRoute
];
