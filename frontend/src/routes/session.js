import LoginPage from "pages/Login";
import RegistrationPage from "pages/Registration"
import NotFound from "pages/NotFound";

export const sessionRoutes = [
  {
    path: '/session/signin',
    component: LoginPage,
  },
  {
    path: '/session/signup',
    component: RegistrationPage,
  },
  {
    path: '/session/404',
    component: NotFound,
  },
];
