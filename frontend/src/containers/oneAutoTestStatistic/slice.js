import {createSlice} from '@reduxjs/toolkit';
import {useInjectReducer, useInjectSaga} from "redux-injectors";
import saga from "./saga";
import {useSelector} from "react-redux";
import {camelize} from "../../utils/to-camel-case";

const initialState = {
  status: 'idle',
  fullName: '',
  resultByStatus: {},
  statistic: []
};

export const oneAutoTestStatisticSlice = createSlice({
  name: 'oneAutoTestStatistic',
  initialState,
  reducers: {
    fetch: () => {
    },

    fetchStart: (state) => {
      state.status = 'pending'
    },
    fetchSuccess: (state, {payload: {data}}) => {
      data = camelize(data)
      state.fullName = data.fullName
      state.resultByStatus = data.resultByStatus
      state.statistic = data.statistic
      state.status = 'success'
    },
    fetchError: (state, {payload: {e}}) => {
      state.status = 'error'
      console.log('Fetch oneAutoTestStatistic error')
      console.log(e)
    },
  },
});

export const {actions} = oneAutoTestStatisticSlice;

export const useOneAutoTestStatisticSlice = () => {
  useInjectReducer({key: oneAutoTestStatisticSlice.name, reducer: oneAutoTestStatisticSlice.reducer});
  useInjectSaga({key: oneAutoTestStatisticSlice.name, saga: saga});
  return {actions: oneAutoTestStatisticSlice.actions};
};


export function useOneAutoTestStatisticSliceSelector(selector) {
  return useSelector((state) => selector(state[oneAutoTestStatisticSlice.name] || initialState))
}
