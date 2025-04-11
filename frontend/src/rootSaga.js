import { all } from 'redux-saga/effects';
import AuthSaga from "containers/auth/saga"

export default function* rootSaga() {
  yield all([
    AuthSaga()
  ])
}
