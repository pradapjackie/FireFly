import { combineReducers } from '@reduxjs/toolkit';

import { reducer as authReducer } from 'containers/auth/slice';
import { reducer as alertReducer } from 'containers/alerts/slice';


export default function  createReducer(injectedReducers = {}) {
  return combineReducers({
    auth: authReducer,
    alert: alertReducer,
    ...injectedReducers,
  });
}
