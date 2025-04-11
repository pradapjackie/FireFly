import { createSlice } from '@reduxjs/toolkit';
import { camelize } from '../../utils/to-camel-case';
import { useInjectReducer, useInjectSaga } from 'redux-injectors';
import saga from './saga';
import { useSelector } from 'react-redux';

const initialStatistic = {
  fetchStatus: 'idle',
  status: 'idle',
};

const initialState = {
  testRuns: {},
};

export const testRunStatisticSlice = createSlice({
  name: 'testRunStatistic',
  initialState,
  reducers: {
    fetch: () => {},
    fetchStart: (state, { payload: { testRunId } }) => {
      state.testRuns[testRunId] = { fetchStatus: 'pending' };
    },
    fetchSuccess: (state, { payload: { testRunId, data } }) => {
      state.testRuns[testRunId] = camelize(data);
      state.testRuns[testRunId]['fetchStatus'] = 'success';
    },
    fetchError: (state, { payload: { testRunId, e } }) => {
      state.testRuns[testRunId] = { fetchStatus: 'error' };
      console.log('Fetch test run statistic error', e);
    },
  },
});

export const { actions } = testRunStatisticSlice;

export const useTestRunStatisticSlice = () => {
  useInjectReducer({
    key: testRunStatisticSlice.name,
    reducer: testRunStatisticSlice.reducer,
  });
  useInjectSaga({ key: testRunStatisticSlice.name, saga: saga });
  return { actions: testRunStatisticSlice.actions };
};

export function useTestRunStatisticSelector(testRunId) {
  return useSelector(
    (state) =>
      (state[testRunStatisticSlice.name] || initialState).testRuns[testRunId] ||
      initialStatistic,
  );
}

export function testRunStatusSelector(state, testRunId) {
  return (state[testRunStatisticSlice.name].testRuns[testRunId] || initialStatistic)
    .status;
}
