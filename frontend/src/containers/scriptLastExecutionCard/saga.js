import { fork, takeLatest, takeLeading, call, put, take, cancel, cancelled } from 'redux-saga/effects';
import { actions } from './slice';
import { api } from './api';
import { WebSocketManager} from 'utils/ws-client';

const wsManager = new WebSocketManager();

function* fetchLastScriptHistory({ payload: { scriptId } }) {
    yield put(actions.fetchStart({ scriptId }));
    try {
        const { data } = yield call(api.fetch, scriptId);
        yield put(actions.fetchSuccess({ scriptId, data }));
    } catch (e) {
        yield put(actions.fetchError({ scriptId, e }));
    }
}

function* webSocketsWriteFlow() {
    while (true) {
        const { payload } = yield take(actions.subscribe.type);
        wsManager.wsSend(JSON.stringify({ execution_id: payload }));
    }
}

function* webSocketsReadFlow() {
    const channel = yield call(wsManager.createEventChannel, '/script/ws/history/');
    while (true) {
        try {
            const rawMessage = yield take(channel);
            const message = JSON.parse(rawMessage);
            switch (message.type) {
                case 'log':
                    yield put(actions.updateLog({ scriptId: message.script_id, message: message.message }));
                    break;
                case 'status':
                    yield put(actions.updateStatus({ scriptId: message.script_id, message: message.message }));
                    break;
                case 'result':
                    yield put(actions.updateResult({ scriptId: message.script_id, message: message.message }));
                    break;
                case 'intermediate_result':
                    yield put(
                        actions.updateIntermediateResult({ scriptId: message.script_id, message: message.message }),
                    );
                    break;
                case 'errors':
                    yield put(actions.updateErrors({ scriptId: message.script_id, message: message.message }));
                    break;
                case 'intermediate_errors':
                    yield put(
                        actions.updateIntermediateErrors({ scriptId: message.script_id, message: message.message }),
                    );
                    break;
                case 'env_used':
                    yield put(actions.updateEnvUsed({ scriptId: message.script_id, message: message.message }));
                    break;
                default:
                // console.log(`Unknown message type ${message.type}`);
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

function* watchLastScriptHistoryFetch() {
    yield takeLatest(actions.fetch.type, fetchLastScriptHistory);
}

function* watchInitWs() {
    yield takeLeading(actions.initWS.type, webSocketFlow);
}

export default function* scriptLastExecutionSaga() {
    yield fork(watchLastScriptHistoryFetch);
    yield fork(watchInitWs);
}
