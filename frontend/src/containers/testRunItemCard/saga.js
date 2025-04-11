import { fork, takeLatest, call, put, select} from 'redux-saga/effects';
import {actions, useTestRunItemCardStatusSelector} from './slice';
import { api } from './api';

function* fetchTestItemCard({ payload: { testRunId, itemId } }) {
  const status = yield select(useTestRunItemCardStatusSelector, testRunId, itemId);
  if (!["success", "fail"].includes(status)) {
    yield put(actions.fetchStart({testRunId, itemId}));
    try {
      const { data } = yield call(api.fetch, testRunId, itemId);
      yield put(actions.fetchSuccess({testRunId, itemId, data}));
    } catch (e) {
      yield put(actions.fetchError({testRunId, itemId, e}));
    }
  }
}

function* runTestRunItemCardFetch() {
  yield takeLatest(actions.fetch.type, fetchTestItemCard);
}

export default function* testRunItemCardSaga() {
  yield fork(runTestRunItemCardFetch);
}
