import { fork, takeLatest, call, put } from 'redux-saga/effects';
import { actions } from './slice';
import { api } from './api';

function* fetchScriptHistoryRecords({ payload: { scriptId } }) {
    yield put(actions.fetchStart());
    try {
        const { data } = yield call(api.fetch, scriptId);
        yield put(actions.fetchSuccess(data));
    } catch (e) {
        yield put(actions.fetchError({ e }));
    }
}

function* watchScriptHistoryFetch() {
    yield takeLatest(actions.fetch.type, fetchScriptHistoryRecords);
}

export default function* scriptRunCardSaga() {
    yield fork(watchScriptHistoryFetch);
}
