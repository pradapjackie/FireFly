import { fork, takeLatest, takeLeading, call, put, take, cancel, cancelled } from 'redux-saga/effects';
import { actions } from './slice';
import { api } from './api';
import {WebSocketManager} from 'utils/ws-client';

const wsManager = new WebSocketManager();

function* fetchLastLoadTestHistory({ payload: { loadTestId } }) {
    yield put(actions.fetchStart({ loadTestId }));
    try {
        const { data } = yield call(api.fetch, loadTestId);
        yield put(actions.fetchSuccess({ loadTestId, data }));
    } catch (e) {
        yield put(actions.fetchError({ loadTestId, e }));
    }
}

function* webSocketsWriteFlow() {
    while (true) {
        const {
            payload: { executionId, loadTestId },
        } = yield take(actions.subscribe.type);
        wsManager.wsSend(JSON.stringify({ execution_id: executionId, load_test_id: loadTestId }));
    }
}

function* webSocketsReadFlow() {
    const channel = yield call(wsManager.createEventChannel, '/load_test/ws/history/');
    while (true) {
        try {
            const rawMessage = yield take(channel);
            const message = JSON.parse(rawMessage);
            switch (message.type) {
                case 'successful_subscribe':
                    yield put(actions.setCurrentSubscribeId({ executionId: message.execution_id }));
                    yield put(actions.fetch({ loadTestId: message.load_test_id }));
                    break;
                case 'execution':
                    yield put(actions.updateExecutionCard({ message: message.data }));
                    break;
                case 'worker':
                    yield put(actions.updateWorker({ message: message.data }));
                    break;
                case 'task':
                    yield put(actions.updateTaskHistory({ message: message.data }));
                    break;
                case 'chart':
                    yield put(actions.updateChartData({ message: message.data }));
                    break;
                default:
                    console.log(`Unknown message type ${message.type}`);
            }
        } finally {
            if (yield cancelled()) {
                channel.close();
            }
        }
    }
}

function* webSocketFlow() {
    const readTask = yield fork(webSocketsReadFlow);
    const writeTask = yield fork(webSocketsWriteFlow);
    yield take(actions.closeWS.type);
    yield cancel(readTask);
    yield cancel(writeTask);
}

function* watchLastLoadTestHistoryFetch() {
    yield takeLatest(actions.fetch.type, fetchLastLoadTestHistory);
}

function* watchInitWs() {
    yield takeLeading(actions.initWS.type, webSocketFlow);
}

export default function* scriptLastExecutionSaga() {
    yield fork(watchLastLoadTestHistoryFetch);
    yield fork(watchInitWs);
}
