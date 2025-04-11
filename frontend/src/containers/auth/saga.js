import { call, put, take, fork, cancel, cancelled, takeLatest } from 'redux-saga/effects';
import { saveLocalToken, removeLocalToken, getLocalToken } from 'utils/local-storage';
import { actions } from './slice';
import { api } from './api';
import jwtDecode from 'jwt-decode';

export function* sessionStart(token) {
    const { isTokenValid, error } = yield call(checkToken, token);
    if (!isTokenValid) {
        yield put(actions.sessionError({ error }));
    } else {
        try {
            const response = yield call(api.getMe, token);
            const user = response.data;
            if (user) {
                yield put(actions.sessionStarted({ user }));
                yield put(actions.sessionChecked({}));
            } else {
                yield put(actions.sessionError({ error: 'No user in api response' }));
            }
        } catch (error) {
            yield put(actions.sessionError({ error }));
        }
    }
}

function* checkToken(token) {
    try {
        const decodedToken = jwtDecode(token);
        const currentTime = Date.now() / 1000;
        if (decodedToken.exp < currentTime) {
            yield put(actions.sessionError({ error: 'Token expired' }));
            return { isTokenValid: false, error: 'Token expired' };
        }
    } catch (error) {
        yield put(actions.sessionError({ error }));
        return { isTokenValid: false, error: error };
    }
    return { isTokenValid: true, error: '' };
}

function* closeSession() {
    removeLocalToken();
}

export function* authorize(username, password) {
    try {
        const {
            data: { access_token },
        } = yield call(api.authorize, username, password);
        if (access_token) {
            yield call(saveLocalToken, access_token);
            yield put(actions.authSuccess({}));
            yield call(sessionStart, access_token);
        } else {
            yield put(actions.authError({ error: 'No access_token in API response' }));
        }
    } catch (error) {
        console.log(error);
        yield put(actions.authError({ error }));
    } finally {
        if (yield cancelled()) {
            // ... put special cancellation handling code here
        }
    }
}

function* loginFlow() {
    while (true) {
        const {
            payload: { username, password },
        } = yield take(actions.authStart.type);
        const task = yield fork(authorize, username, password);
        const action = yield take([actions.authError.type, actions.logout.type]);
        if (action.type === actions.logout.type) {
            yield cancel(task);
        }
    }
}

function* sessionFlow() {
    while (true) {
        yield take(actions.startSessionCheck.type);
        const token = getLocalToken();
        let task;
        if (!token) {
            yield put(actions.sessionChecked({}));
            task = yield fork(loginFlow);
        } else {
            task = yield fork(sessionStart, token);
        }
        yield take([actions.logout.type, actions.sessionError.type]);
        yield cancel(task);
        yield call(closeSession);
    }
}

function* SignUp({ payload: { email, password, fullName } }) {
    yield put(actions.signUpStart({}));
    try {
        const {
            data: { access_token },
        } = yield call(api.signUp, email, password, fullName);
        yield fork(sessionStart, access_token);
        yield put(actions.signUpSuccess({}));
    } catch (e) {
        yield put(actions.signUpError({ e }));
    }
}

function* watchAutoTestRun() {
    yield takeLatest(actions.signUp, SignUp);
}

export default function* AuthSaga() {
    yield fork(sessionFlow);
    yield fork(watchAutoTestRun);
}

// ToDo Fix Auth flow
