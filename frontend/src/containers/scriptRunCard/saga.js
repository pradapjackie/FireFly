import { fork, takeLatest, call, put, takeEvery } from 'redux-saga/effects';
import { actions } from './slice';
import {actions as lastExecutionScriptActions} from '../scriptLastExecutionCard/slice'
import { api } from './api';
import { filterOnlyOverwrite } from '../enviroment/utils';

function* fetchScript({ payload: { scriptId } }) {
    yield put(actions.fetchStart({ scriptId }));
    try {
        const { data } = yield call(api.fetch, scriptId);
        yield put(actions.fetchSuccess({ scriptId, data }));
    } catch (e) {
        yield put(actions.fetchError({ scriptId, e }));
    }
}

function* runScript({ payload: { folder, selectedEnv, envData, scriptId, params } }) {
    yield put(actions.scriptStart({}));
    try {
        const filteredEnvData = filterOnlyOverwrite(envData);
        const { data } = yield call(api.runScript, folder, selectedEnv, filteredEnvData, scriptId, params);
        yield put(actions.scriptStartSuccess({ scriptId, data }));
        yield put(lastExecutionScriptActions.startNewScript({scriptId, executionId: data.execution_id}))
    } catch (e) {
        yield put(actions.scriptStartError({ e }));
    }
}

function* watchScriptRunCardFetch() {
    yield takeLatest(actions.fetch.type, fetchScript);
}

function* watchScriptRun() {
    yield takeEvery(actions.runScript.type, runScript);
}

export default function* scriptRunCardSaga() {
    yield fork(watchScriptRunCardFetch);
    yield fork(watchScriptRun);
}
