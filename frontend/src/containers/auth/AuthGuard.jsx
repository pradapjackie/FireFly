import React, {useEffect} from 'react';
import {useDispatch, useSelector} from 'react-redux'
import {Redirect, useLocation} from 'react-router-dom';
import {actions, name} from './slice';
import {Loading} from "components/Loading/Loading";

const AuthGuard = ({children}) => {
  const isAuthorized = useSelector((state) => state[name].isAuthorized);
  const sessionChecked = useSelector((state) => state[name].sessionChecked);
  const dispatch = useDispatch();
  const {pathname, search} = useLocation();

  useEffect(() => {dispatch(actions.startSessionCheck({}))}, [])

  if (!sessionChecked) return <Loading/>;
  if (isAuthorized) return <>{children}</>;
  return (
    <Redirect
      to={{
        pathname: '/session/signin',
        state: {redirectUrl: `${pathname}${search}`},
      }}
    />
  );
};

export default AuthGuard;
