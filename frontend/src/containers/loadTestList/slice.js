import { createSlice } from '@reduxjs/toolkit';
import { useInjectReducer, useInjectSaga } from 'redux-injectors';
import { useSelector } from 'react-redux';
import saga from './saga';
import { camelize } from '../../utils/to-camel-case';

const initialFolderState = {
    status: 'idle',
    loadTestList: [],
};

const initialState = {};

export const loadTestListSlice = createSlice({
    name: 'LoadTestList',
    initialState,
    reducers: {
        fetch: () => {},
        fetchStart: (state, { payload: { folder } }) => {
            state[folder] = { ...initialFolderState, ...state[folder] };
            state[folder].status = 'pending';
        },
        fetchSuccess: (state, { payload: { folder, data } }) => {
            state[folder].loadTestList = camelize(data);
            state[folder].status = 'success';
        },
        fetchError: (state, { payload: { folder, e } }) => {
            state[folder].status = 'error';
            console.log('Fetch error', e);
        },
    },
});

export const { actions } = loadTestListSlice;

export const useLoadTestListSlice = () => {
    useInjectReducer({ key: loadTestListSlice.name, reducer: loadTestListSlice.reducer });
    useInjectSaga({ key: loadTestListSlice.name, saga: saga });
    return { actions: loadTestListSlice.actions };
};

export function useLoadTestListSelector(folder, selector) {
    return useSelector((state) =>
        selector((state[loadTestListSlice.name] || initialState)[folder] || initialFolderState),
    );
}
