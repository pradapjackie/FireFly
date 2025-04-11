import {fork, takeLatest, call, put} from "redux-saga/effects";
import {actions} from './slice';
import {api} from './api'


function* fetchCollectedLoadTests({payload: {folder}}) {
  yield put(actions.fetchStart({folder: folder}));
  try {
    const {data} = yield call(api.fetch, folder);
    yield put(actions.fetchSuccess({folder: folder, data: data}));
  } catch (e) {
    yield put(actions.fetchError({folder: folder, e: e}));
  }
}

function* watchLoadTestListFetch() {
  yield takeLatest(actions.fetch.type, fetchCollectedLoadTests)
}


export default function* loadTestListSaga() {
  yield fork(watchLoadTestListFetch)
}
