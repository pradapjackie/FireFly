import { fork, takeLatest, call, put, select} from 'redux-saga/effects';
import {actions, testRunTreeStatusSelector} from './slice';
import { api } from './api';

function* fetchTestRunTree({ payload: { testRunId } }) {
  const status = yield select(testRunTreeStatusSelector, testRunId);
  if (status !== 'finished') {
    yield put(actions.fetchStart({testRunId}));
    try {
      const { data } = yield call(api.fetch, testRunId);
      yield put(actions.fetchSuccess({testRunId, data}));
    } catch (e) {
      yield put(actions.fetchError({testRunId, e}));
    }
  }
}

function* runTestRunTreeFetch() {
  yield takeLatest(actions.fetch.type, fetchTestRunTree);
}

export default function* testRunTreeSaga() {
  yield fork(runTestRunTreeFetch);
}
