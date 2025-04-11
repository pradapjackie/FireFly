import React from 'react';
import {Redirect} from "react-router-dom";

export const redirectRoute = [
  {
    path: '/',
    exact: true,
    component: () => <Redirect to="/dashboard" />,
  },
];
