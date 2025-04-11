import { createSlice } from '@reduxjs/toolkit';
import { useInjectReducer, useInjectSaga } from 'redux-injectors';
import saga from './saga';
import { useSelector } from 'react-redux';
import { flatCamelize } from '../../utils/to-camel-case';

const initialState = {
    fetchStatus: 'idle',
};

export const scriptHistorySlice = createSlice({
    name: 'scriptHistory',
    initialState,
    reducers: {
        fetch: () => {},
        fetchStart: (state) => {
            state.fetchStatus = 'pending';
        },
        fetchSuccess: (state, { payload: { name, history } }) => {
            state.scriptName = name;
            state.history = flatCamelize(history);
            state.fetchStatus = 'success';
        },
        fetchError: (state, { payload: { e } }) => {
            state.fetchStatus = 'error';
            console.log('Fetch test run statistic error', e);
        },
    },
});

export const { actions } = scriptHistorySlice;

export const useScriptHistorySlice = () => {
    useInjectReducer({
        key: scriptHistorySlice.name,
        reducer: scriptHistorySlice.reducer,
    });
    useInjectSaga({ key: scriptHistorySlice.name, saga: saga });
    return { actions: scriptHistorySlice.actions };
};

export function useScriptHistorySelector() {
    return useSelector((state) => state[scriptHistorySlice.name] || initialState);
}
