import { createSlice } from '@reduxjs/toolkit';
import { useInjectReducer, useInjectSaga } from 'redux-injectors';
import saga from './saga';
import { useSelector } from 'react-redux';
import { flatCamelize } from '../../utils/to-camel-case';

const initialState = {
    scripts: {},
};

const LastScriptHistoryInitial = {
    fetchStatus: 'idle',
    status: 'idle',
    log: {},
};

const CreateNewScriptHistory = (executionId) => {
    return {
        fetchStatus: 'success',
        status: 'pending',
        executionId: executionId,
        log: {},
    };
};

export const scriptLastExecutionCardSlice = createSlice({
    name: 'scriptLastExecutionCard',
    initialState,
    reducers: {
        fetch: () => {},
        fetchStart: (state, { payload: { scriptId } }) => {
            state.scripts[scriptId] = { ...state.scripts[scriptId], ...LastScriptHistoryInitial };
            state.scripts[scriptId].fetchStatus = 'pending';
        },
        fetchSuccess: (state, { payload: { scriptId, data } }) => {
            state.scripts[scriptId] = {
                ...state.scripts[scriptId],
                ...flatCamelize(data),
            };
            state.scripts[scriptId].fetchStatus = 'success';
        },
        fetchError: (state, { payload: { scriptId, e } }) => {
            state.scripts[scriptId].fetchStatus = 'error';
            console.log('Fetch test run statistic error', e);
        },
        startNewScript: (state, { payload: { scriptId, executionId } }) => {
            state.scripts[scriptId] = CreateNewScriptHistory(executionId);
        },

        initWS: () => {},
        closeWS: () => {},
        subscribe: () => {},
        updateLog: (state, { payload: { scriptId, message } }) => {
            state.scripts[scriptId].log[message.index] = message.line;
        },
        updateStatus: (state, { payload: { scriptId, message } }) => {
            state.scripts[scriptId].status = message;
        },
        updateResult: (state, { payload: { scriptId, message } }) => {
            state.scripts[scriptId].result = message;
        },
        updateIntermediateResult: (state, { payload: { scriptId, message } }) => {
            state.scripts[scriptId].result = state.scripts[scriptId].result || { type: 'multi', object: {} };
            let current = state.scripts[scriptId].result.object;
            state.scripts[scriptId].result.object = { ...current, ...message };
        },
        updateErrors: (state, { payload: { scriptId, message } }) => {
            state.scripts[scriptId].errors = message;
        },
        updateIntermediateErrors: (state, { payload: { scriptId, message } }) => {
            state.scripts[scriptId].errors = state.scripts[scriptId].errors || [];
            state.scripts[scriptId].errors.push(...message);
        },
        updateEnvUsed: (state, { payload: { scriptId, message } }) => {
            state.scripts[scriptId].envUsed = message;
        },
    },
});

export const { actions } = scriptLastExecutionCardSlice;

export const useScriptLastExecutionCardSlice = () => {
    useInjectReducer({
        key: scriptLastExecutionCardSlice.name,
        reducer: scriptLastExecutionCardSlice.reducer,
    });
    useInjectSaga({ key: scriptLastExecutionCardSlice.name, saga: saga });
    return { actions: scriptLastExecutionCardSlice.actions };
};

export function useScriptLastExecutionCardSelector(scriptId, selector) {
    return useSelector((state) =>
        selector(
            (state[scriptLastExecutionCardSlice.name] || initialState).scripts[scriptId] || LastScriptHistoryInitial,
        ),
    );
}
