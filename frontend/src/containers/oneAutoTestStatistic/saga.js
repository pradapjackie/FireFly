import {fork, takeLatest, call, put} from "redux-saga/effects";
import {actions} from './slice';
import {api} from './api'

function* fetchStat(action) {
  const {payload: {test_id}} = action
  yield put(actions.fetchStart({}));
  try {
    const {data} = yield call(api.fetch, test_id);
    yield put(actions.fetchSuccess({data}));
  } catch (e) {
    yield put(actions.fetchError({e}));
  }
}

function* watchStatFetch() {
  yield takeLatest(actions.fetch.type, fetchStat)
}


export default function* runSaga() {
  yield fork(watchStatFetch)
}
