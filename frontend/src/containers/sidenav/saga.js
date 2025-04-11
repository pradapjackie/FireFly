import {fork, takeLatest, call, put} from "redux-saga/effects";
import {actions} from "./slice";
import {api} from "./api";

function* fetchSidenavMenu() {
  yield put(actions.MenuLoadStarted());
  try {
    const {data: testsData} = yield call(api.getTestsFolders);
    const {data: scriptData} = yield call(api.getScriptsFolders);
    const {data: loadTestsData} = yield call(api.getLoadTestsFolders);
    yield put(actions.MenuLoadSucceed({tests: testsData, scripts: scriptData, loadTests: loadTestsData}));
  } catch (e) {
    yield put(actions.MenuLoadError({e: e}));
  }
}

function* watchSidenavMenuFetch() {
  yield takeLatest(actions.startMenuLoad.type, fetchSidenavMenu)
}


export default function* sidenavMenuSaga() {
  yield fork(watchSidenavMenuFetch)
}
