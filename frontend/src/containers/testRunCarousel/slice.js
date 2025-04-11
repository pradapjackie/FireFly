import { createSlice } from '@reduxjs/toolkit';
import { camelize } from '../../utils/to-camel-case';
import { useInjectReducer, useInjectSaga } from 'redux-injectors';
import saga from './saga';
import { useSelector } from 'react-redux';

const initialFolderState = {
    status: 'idle',
    ids: [],
    entities: {},
};

const initialState = {};

export const testRunCarouselSlice = createSlice({
    name: 'testRunCarousel',
    initialState,
    reducers: {
        fetch: () => {},
        fetchStart: (state, { payload: { folder } }) => {
            state[folder] = { ...initialFolderState, ...state[folder]};
            state[folder].status = 'pending';
        },
        fetchSuccess: (state, { payload: { folder, data } }) => {
            state[folder].ids = data.ids;
            if (data.runs) {
                for (const [runId, testRun] of Object.entries(data.runs)) {
                    data.runs[runId] = camelize(testRun);
                }
            }
            state[folder].entities = data.runs;
            state[folder].status = 'success';
        },
        fetchError: (state, { payload: { folder, e } }) => {
            state[folder].status = 'error';
            console.log('fetchTestRunError');
            console.log(e);
        },
        addItem: (state, { payload: { data, folder } }) => {
            state[folder].ids.unshift(data.id);
            state[folder].entities[data.id] = camelize(data);
        },
    },
});

export const { actions } = testRunCarouselSlice;

export const useTestRunCarouselSlice = () => {
    useInjectReducer({
        key: testRunCarouselSlice.name,
        reducer: testRunCarouselSlice.reducer,
    });
    useInjectSaga({ key: testRunCarouselSlice.name, saga: saga });
    return { actions: testRunCarouselSlice.actions };
};

export function useTestRunCarouselSliceSelector(folder, selector) {
    return useSelector((state) => selector((state[testRunCarouselSlice.name] || initialState)[folder] || initialFolderState));
}
