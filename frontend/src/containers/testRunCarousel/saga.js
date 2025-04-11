import {fork, takeLatest, call, put} from "redux-saga/effects";
import {actions} from './slice';
import {api} from './api'

function* fetchTestRuns({payload: {folder, env}}) {
  yield put(actions.fetchStart({folder: folder}));
  try {
    const {data} = yield call(api.fetch_test_runs, folder, env);
    yield put(actions.fetchSuccess({folder: folder, data: data}));
  } catch (e) {
    yield put(actions.fetchError({folder: folder, e: e}));
  }
}

function* watchTestRunFetch() {
  yield takeLatest(actions.fetch.type, fetchTestRuns)
}


export default function* runAutoTestSaga() {
  yield fork(watchTestRunFetch)
}
