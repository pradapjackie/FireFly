import { createSlice } from '@reduxjs/toolkit';
import { useInjectReducer, useInjectSaga } from 'redux-injectors';
import saga from './saga';
import { useSelector } from 'react-redux';
import { camelize } from '../../utils/to-camel-case';

const initialFolderState = {
    status: 'idle',
    stat: {},
    testRuns: [],
};

const initialState = {};

export const autoTestStatisticSlice = createSlice({
    name: 'autoTestStatistic',
    initialState,
    reducers: {
        fetch: () => {},

        fetchStart: (state, { payload: { folder } }) => {
            state[folder] = { ...initialFolderState, ...state[folder]};
            state[folder].status = 'pending';
        },
        fetchSuccess: (state, { payload: { folder, data } }) => {
            data = camelize(data);
            state[folder].stat = data.stat;
            state[folder].testRuns = data.testRuns;
            state[folder].status = 'success';
        },
        fetchError: (state, { payload: { folder, e } }) => {
            state[folder].status = 'error';
            console.log('Fetch error');
            console.log(e);
        },
    },
});

export const { actions } = autoTestStatisticSlice;

export const useAutoTestStatisticSlice = () => {
    useInjectReducer({ key: autoTestStatisticSlice.name, reducer: autoTestStatisticSlice.reducer });
    useInjectSaga({ key: autoTestStatisticSlice.name, saga: saga });
    return { actions: autoTestStatisticSlice.actions };
};

export function useAutoTestStatisticSliceSelector(folder,  selector) {
    return useSelector((state) => selector((state[autoTestStatisticSlice.name] || initialState)[folder] || initialFolderState));
}
