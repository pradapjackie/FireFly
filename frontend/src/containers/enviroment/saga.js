import {fork, takeLatest, call, put} from "redux-saga/effects";
import {actions} from './slice';
import {api} from './api'
import {getActiveEnv, saveActiveEnv, getEnvOverwriteData, saveEnvOverwriteData} from "../../utils/local-storage";


function* fetchEnvList() {
  yield put(actions.fetchStart({}));
  try {
    const {data} = yield call(api.fetch);
    const activeEnv = yield call(getActiveEnv);
    yield put(actions.fetchSuccess({ids: data, activeEnv: activeEnv}));
  } catch (e) {
    yield put(actions.fetchError({e}));
  }
}

function* fetchByEnv({payload: {env}}) {
  yield put(actions.fetchByEnvStart({env: env}));
  try {
    const {data} = yield call(api.fetchByEnv, env);
    const overwriteData = yield call(getEnvOverwriteData, env);
    const overwrite = JSON.parse(overwriteData)
    Object.keys(overwrite).forEach(function(key){ overwrite[key] = overwrite[key].value })
    yield put(actions.fetchByEnvSuccess({env: env, data: data, overwrite: overwrite}));
  } catch (e) {
    yield put(actions.fetchByEnvError({error: e, env: env}));
  }
}

function* saveLocalEnv({payload: {env, overwriteEnv}}) {
  try {
    overwriteEnv = JSON.stringify(overwriteEnv)
    yield call(saveEnvOverwriteData, env, overwriteEnv);
  } catch (e) {
    yield put(actions.saveLocalEnvError({e}));
  }
}

function* saveGlobalEnv({payload: {env, updatedEnv}}) {
  try {
    yield call(api.updateEnv, env, updatedEnv);
    yield put(actions.saveGlobalEnvSuccess({env: env}));
  } catch (e) {
    yield put(actions.saveGlobalEnvError({e}));
  }
}

function* setSelected({payload: {selected}}) {
  yield call(saveActiveEnv, selected);
  yield put(actions.setSelected({selected: selected}));
}

function* runEnvListFetch() {
  yield takeLatest(actions.fetch.type, fetchEnvList)
}

function* runByEnvFetch() {
  yield takeLatest(actions.fetchByEnv.type, fetchByEnv)
}

function* runSaveLocalEnv() {
  yield takeLatest(actions.saveLocalEnv.type, saveLocalEnv)
}

function* runSaveGlobalEnv() {
  yield takeLatest(actions.saveGlobalEnv.type, saveGlobalEnv)
}

function* runEnvSetActiveEnv() {
  yield takeLatest(actions.saveSelected.type, setSelected)
}

export default function* environmentSaga() {
  yield fork(runEnvSetActiveEnv)
  yield fork(runEnvListFetch)
  yield fork(runByEnvFetch)
  yield fork(runSaveLocalEnv)
  yield fork(runSaveGlobalEnv)
}
