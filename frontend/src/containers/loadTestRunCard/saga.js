import { fork, takeLatest, call, put, takeEvery } from 'redux-saga/effects';
import { actions } from './slice';
import { api } from './api';
import { filterOnlyOverwrite } from '../enviroment/utils';
import { actions as lastExecutionLoadTestActions } from '../loadTestLastExecutionCard/slice';
import { actions as alertsActions } from '../alerts/slice';

function* fetchLoadTest({ payload: { loadTestId } }) {
    yield put(actions.fetchStart({ loadTestId }));
    try {
        const { data } = yield call(api.fetch, loadTestId);
        yield put(actions.fetchSuccess({ loadTestId, data }));
    } catch (e) {
        yield put(actions.fetchError({ loadTestId, e }));
    }
}

function* startLoadTest({ payload: { folder, selectedEnv, envData, loadTestId, params, configValues, numberOfTasks, chartConfig } }) {
    yield put(actions.loadTestStart({}));
    try {
        const filteredEnvData = filterOnlyOverwrite(envData);
        const { data } = yield call(
            api.start,
            folder,
            selectedEnv,
            filteredEnvData,
            loadTestId,
            params,
            configValues,
            numberOfTasks,
            chartConfig
        );
        yield put(actions.loadTestStartSuccess({ loadTestId, data }));
        yield put(
            lastExecutionLoadTestActions.startNewLoadTest({
                loadTestId: loadTestId,
                executionId: data.execution_id,
                numberOfWorkers: numberOfTasks / parseInt(configValues['concurrency_within_a_single_worker']),
            }),
        );
    } catch (e) {
        yield put(actions.loadTestStartError({ e }));
        yield put(alertsActions.newAlert({ severity: "error", text: e?.response?.data?.detail || "Unknown error" }));
    }
}

function* stopLoadTest({ payload: { loadTestId } }) {
    yield put(actions.loadTestStop({}));
    try {
        yield call(api.stop, loadTestId);
        yield put(actions.loadTestStopSuccess());
    } catch (e) {
        yield put(actions.loadTestStopError({ e }));
        yield put(alertsActions.newAlert({ severity: "error", text: e?.response?.data?.detail || "Unknown error" }));
    }
}

function* changeNumberOfWorkers({ payload: { loadTestId, executionId, configValues, numberOfTasks } }) {
    yield put(actions.changeNumberOfWorkersStart({}));
    try {
        yield call(api.changeNumberOfWorkers, loadTestId, executionId, configValues, numberOfTasks);
        yield put(actions.changeNumberOfWorkersStartSuccess());
    } catch (e) {
        yield put(actions.changeNumberOfWorkersStartError({ e }));
        yield put(alertsActions.newAlert({ severity: "error", text: e?.response?.data?.detail || "Unknown error" }));
    }
}

function* watchLoadTestRunCardFetch() {
    yield takeLatest(actions.fetch.type, fetchLoadTest);
}

function* watchLoadTestStart() {
    yield takeEvery(actions.startLoadTest.type, startLoadTest);
}

function* watchLoadTestStop() {
    yield takeEvery(actions.stopLoadTest.type, stopLoadTest);
}

function* watchLoadTestChangeNumberOfWorkers() {
    yield takeEvery(actions.changeNumberOfWorkers.type, changeNumberOfWorkers);
}

export default function* loadTestRunCardSaga() {
    yield fork(watchLoadTestRunCardFetch);
    yield fork(watchLoadTestStart);
    yield fork(watchLoadTestStop);
    yield fork(watchLoadTestChangeNumberOfWorkers);
}
