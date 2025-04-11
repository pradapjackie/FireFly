import {fork, takeLatest, takeEvery, call, put} from "redux-saga/effects";
import {actions} from './slice';
import {actions as carouselActions} from '../testRunCarousel/slice'
import {api} from './api'
import {filterOnlyOverwrite} from "../enviroment/utils";

function* fetchCollectedTests({payload: {folder}}) {
  yield put(actions.fetchStart({folder: folder}));
  try {
    const {data} = yield call(api.fetch, folder);
    yield put(actions.fetchSuccess({folder: folder, data: data}));
  } catch (e) {
    yield put(actions.fetchError({folder: folder, e: e}));
  }
}

function* runCollectedTests({payload: {folder, testIds, selectedEnv, envData, runConfig}}) {
  yield put(actions.runStart({}));
  try {
    const filteredEnvData = filterOnlyOverwrite(envData)
    const {data} = yield call(api.run, folder, testIds, selectedEnv, filteredEnvData, runConfig);
    yield put(actions.runSuccess({}));
    yield put(carouselActions.addItem({data, folder}));
  } catch (e) {
    yield put(actions.runError({e}));
  }
}

function* fetchDynamicData({payload: {alias, callbackUrl, folder}}) {
  yield put(actions.fetchDynamicDataStart({alias: alias, folder: folder}));
  try {
    const {data} = yield call(api.fetchDynamicData, callbackUrl);
    yield put(actions.fetchDynamicDataSuccess({alias: alias, folder: folder, data: data}));
  } catch (e) {
    yield put(actions.fetchDynamicDataError({alias: alias, folder: folder, error: e}));
  }
}

function* watchAutoTestFetch() {
  yield takeLatest(actions.fetch.type, fetchCollectedTests)
}

function* watchAutoTestRun() {
  yield takeEvery(actions.run.type, runCollectedTests)
}

function* watchAutoTestDynamicDataFetch() {
  yield takeLatest(actions.fetchDynamicData.type, fetchDynamicData)
}

export default function* runAutoTestSaga() {
  yield fork(watchAutoTestFetch)
  yield fork(watchAutoTestRun)
  yield fork(watchAutoTestDynamicDataFetch)
}
