import { createSlice } from '@reduxjs/toolkit';
import { useInjectReducer, useInjectSaga } from 'redux-injectors';
import { useSelector } from 'react-redux';
import saga from './saga';
import { camelize } from '../../utils/to-camel-case';

const initialFolderState = {
    status: 'idle',
    scriptList: [],
};

const initialState = {};

export const scriptRunnerListSlice = createSlice({
    name: 'scriptRunnerList',
    initialState,
    reducers: {
        fetch: () => {},
        fetchStart: (state, { payload: { folder } }) => {
            state[folder] = { ...state[folder], ...initialFolderState };
            state[folder].status = 'pending';
        },
        fetchSuccess: (state, { payload: { folder, data } }) => {
            state[folder].scriptList = camelize(data);
            state[folder].status = 'success';
        },
        fetchError: (state, { payload: { folder, e } }) => {
            state[folder].status = 'error';
            console.log('Fetch error', e);
        },
    },
});

export const { actions } = scriptRunnerListSlice;

export const useScriptRunnerListSlice = () => {
    useInjectReducer({ key: scriptRunnerListSlice.name, reducer: scriptRunnerListSlice.reducer });
    useInjectSaga({ key: scriptRunnerListSlice.name, saga: saga });
    return { actions: scriptRunnerListSlice.actions };
};

export function useScriptRunnerListSelector(folder, selector) {
    return useSelector((state) =>
        selector((state[scriptRunnerListSlice.name] || initialState)[folder] || initialFolderState),
    );
}
