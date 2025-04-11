import { fork, takeLatest, call, put, select} from 'redux-saga/effects';
import { actions, testRunStatusSelector } from './slice';
import { api } from './api';

function* fetchTestRunStatistic({ payload: { testRunId } }) {
  const status = yield select(testRunStatusSelector, testRunId);
  if (!["success", "fail"].includes(status)) {
    yield put(actions.fetchStart({testRunId}));
    try {
      const { data } = yield call(api.fetch, testRunId);
      yield put(actions.fetchSuccess({testRunId, data}));
    } catch (e) {
      yield put(actions.fetchError({testRunId, e}));
    }
  }
}

function* runTestRunStatisticFetch() {
  yield takeLatest(actions.fetch.type, fetchTestRunStatistic);
}

export default function* testRunStatisticSaga() {
  yield fork(runTestRunStatisticFetch);
}
