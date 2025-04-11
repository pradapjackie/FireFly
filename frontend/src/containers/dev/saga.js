import {fork, takeLatest, call, put} from "redux-saga/effects";
import {actions} from './slice';
import {actions as runAutotestActions} from '../runAutotest/slice'
import {actions as scriptRunnerListActions} from '../scriptRunnerList/slice'
import {actions as loadTestListActions} from '../loadTestList/slice'
import {actions as sidenavMenuActions} from '../sidenav/slice'
import {api} from './api'

function* reCollect({payload: {folder, module}}) {
  yield put(actions.reCollectStart({}));
  try {
    if (module === "auto") yield call(api.recollectTests);
    if (module === "script_runner") yield call(api.recollectScripts);
    if (module === "load_test") yield call(api.recollectLoadTests);
    yield put(sidenavMenuActions.startMenuLoad)
    yield put(actions.reCollectSuccess({}));
    if (module === "auto") yield put(runAutotestActions.fetch({folder: folder}))
    if (module === "script_runner") yield put(scriptRunnerListActions.fetch({folder: folder}))
    if (module === "load_test") yield put(loadTestListActions.fetch({folder: folder}))
  } catch (e) {
    yield put(actions.reCollectError({e}));
  }
}
function* runReCollect() {
  yield takeLatest(actions.reCollect.type, reCollect)
}

export default function* devSaga() {
  yield fork(runReCollect)
}
