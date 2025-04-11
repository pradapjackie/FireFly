import { createSlice } from '@reduxjs/toolkit';
import { flatCamelize } from '../../utils/to-camel-case';
import { useInjectReducer, useInjectSaga } from 'redux-injectors';
import saga from './saga';
import { useSelector } from 'react-redux';

const initialItemCard = {
  fetchStatus: 'idle',
  status: 'idle'
};

const initialState = {
  testRuns: {},
};

export const testRunItemCardSlice = createSlice({
  name: 'testRunItemCard',
  initialState,
  reducers: {
    fetch: () => {},
    fetchStart: (state, { payload: { testRunId, itemId } }) => {
      state.testRuns[testRunId] = state.testRuns[testRunId] || {}
      state.testRuns[testRunId][itemId] = { fetchStatus: 'pending' };
    },
    fetchSuccess: (state, { payload: { testRunId, itemId, data } }) => {
      state.testRuns[testRunId][itemId] = flatCamelize(data);
      state.testRuns[testRunId][itemId]['fetchStatus'] = 'success';
    },
    fetchError: (state, { payload: { testRunId, itemId, e } }) => {
      state.testRuns[testRunId][itemId] = { fetchStatus: 'error' };
      console.log('Fetch test run statistic error', e);
    },
  },
});

export const { actions } = testRunItemCardSlice;

export const useTestRunItemCardSlice = () => {
  useInjectReducer({
    key: testRunItemCardSlice.name,
    reducer: testRunItemCardSlice.reducer,
  });
  useInjectSaga({ key: testRunItemCardSlice.name, saga: saga });
  return { actions: testRunItemCardSlice.actions };
};

export function useTestRunItemCardSelector(testRunId, itemId) {
  return useSelector(
    (state) =>
      (state[testRunItemCardSlice.name] || initialState).testRuns[testRunId]?.[itemId] || initialItemCard,
  );
}

export function useTestRunItemCardStatusSelector(state, testRunId, itemId) {
  return ((state[testRunItemCardSlice.name] || initialState).testRuns[testRunId]?.[itemId] || initialItemCard).status;
}
