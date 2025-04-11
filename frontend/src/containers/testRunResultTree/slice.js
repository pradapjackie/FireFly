import { createSlice } from '@reduxjs/toolkit';
import { flatCamelize, camelize } from '../../utils/to-camel-case';
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

export const testRunTreeSlice = createSlice({
  name: 'testRunTree',
  initialState,
  reducers: {
    fetch: () => {},
    fetchStart: (state, { payload: { testRunId } }) => {
      state.testRuns[testRunId] = { fetchStatus: 'pending' };
    },
    fetchSuccess: (state, { payload: { testRunId, data } }) => {
      data = flatCamelize(data);
      if (data.groups) {
        for (const [group_name, value] of Object.entries(data.groups)) {
          data.groups[group_name] = camelize(value);
        }
      }
      state.testRuns[testRunId] = data;
      state.testRuns[testRunId]['fetchStatus'] = 'success';
    },
    fetchError: (state, { payload: { testRunId, e } }) => {
      state.testRuns[testRunId] = { fetchStatus: 'error' };
      console.log('Fetch test run tree error', e);
    },
  },
});

export const { actions } = testRunTreeSlice;

export const useTestRunTreeSlice = () => {
  useInjectReducer({
    key: testRunTreeSlice.name,
    reducer: testRunTreeSlice.reducer,
  });
  useInjectSaga({ key: testRunTreeSlice.name, saga: saga });
  return { actions: testRunTreeSlice.actions };
};

export function useTestRunTreeSelector(testRunId, selector) {
  return useSelector((state) =>
    selector(
      (state[testRunTreeSlice.name] || initialState).testRuns[testRunId] ||
        initialStatistic,
    ),
  );
}

export function testRunTreeStatusSelector(state, testRunId) {
  return (state[testRunTreeSlice.name].testRuns[testRunId] || initialStatistic)
    .status;
}
