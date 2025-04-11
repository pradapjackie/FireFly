import { createSlice } from '@reduxjs/toolkit';
import { useInjectReducer, useInjectSaga } from 'redux-injectors';
import saga from './saga';
import { useSelector } from 'react-redux';
import { flatCamelize } from '../../utils/to-camel-case';

const initialState = {
    loadTests: {},
    currentSubscribeId: null,
};

const LastLoadTestHistoryInitial = {
    fetchStatus: 'idle',
    status: 'idle',
    workers: {},
    taskStatusHistory: {},
    charts: {},
};

const CreateNewLoadTestHistory = (executionId, numberOfWorkers) => {
    return {
        fetchStatus: 'success',
        status: 'pending',
        executionId: executionId,
        workers: Object.fromEntries(Array.from({ length: numberOfWorkers }, (_, i) => [i, 'pending'])),
        taskStatusHistory: {},
        charts: {},
    };
};

export const loadTestLastExecutionCardSlice = createSlice({
    name: 'loadTestLastExecutionCard',
    initialState,
    reducers: {
        fetch: () => {},
        fetchStart: (state, { payload: { loadTestId } }) => {
            state.loadTests[loadTestId] = { ...state.loadTests[loadTestId], ...LastLoadTestHistoryInitial };
            state.loadTests[loadTestId].fetchStatus = 'pending';
        },
        fetchSuccess: (state, { payload: { loadTestId, data } }) => {
            state.loadTests[loadTestId] = {
                ...state.loadTests[loadTestId],
                ...flatCamelize(data),
            };
            state.loadTests[loadTestId].fetchStatus = 'success';
        },
        fetchError: (state, { payload: { loadTestId, e } }) => {
            state.loadTests[loadTestId].fetchStatus = 'error';
            console.log('Fetch load test execution card error', e);
        },
        startNewLoadTest: (state, { payload: { loadTestId, executionId, numberOfWorkers } }) => {
            state.loadTests[loadTestId] = CreateNewLoadTestHistory(executionId, numberOfWorkers);
        },

        initWS: () => {},
        closeWS: () => {},
        subscribe: () => {},
        setCurrentSubscribeId: (state, { payload: { executionId } }) => {
            state.currentSubscribeId = executionId;
        },
        updateExecutionCard: (state, { payload: { message } }) => {
            state.loadTests[message.load_test_id] = { ...state.loadTests[message.load_test_id], ...message.update };
        },
        updateWorker: (state, { payload: { message } }) => {
            state.loadTests[message.load_test_id].workers[message.worker_id] = message.status;
        },
        updateTaskHistory: (state, { payload: { message } }) => {
            const taskHistory = state.loadTests[message.load_test_id].taskStatusHistory;
            taskHistory[message.now_string] = message.data;
        },
        updateChartData: (state, { payload: { message } }) => {
            const charts = state.loadTests[message.load_test_id].charts;
            if (!charts.hasOwnProperty(message.chart_name)) {
                charts[message.chart_name] = { [message.data[0]]: message.data.slice(1) };
            } else {
                charts[message.chart_name][message.data[0]] = message.data.slice(1);
            }
        },
    },
});

export const { actions } = loadTestLastExecutionCardSlice;

export const useLoadTestLastExecutionCardSlice = () => {
    useInjectReducer({
        key: loadTestLastExecutionCardSlice.name,
        reducer: loadTestLastExecutionCardSlice.reducer,
    });
    useInjectSaga({ key: loadTestLastExecutionCardSlice.name, saga: saga });
    return { actions: loadTestLastExecutionCardSlice.actions };
};

export function useLoadTestLastExecutionCardSelector(loadTestId) {
    return useSelector(
        (state) =>
            (state[loadTestLastExecutionCardSlice.name] || initialState).loadTests[loadTestId] ||
            LastLoadTestHistoryInitial,
    );
}

export function useCurrentLoadTestSubscribeIdSelector() {
    return useSelector((state) => (state[loadTestLastExecutionCardSlice.name] || initialState).currentSubscribeId);
}

export function useLoadTestLastExecutionStatusSelector(loadTestId) {
    return useSelector(
        (state) =>
            (
                (state[loadTestLastExecutionCardSlice.name] || initialState).loadTests[loadTestId] ||
                LastLoadTestHistoryInitial
            ).status,
    );
}

export function useLoadTestLastExecutionIdSelector(loadTestId) {
    return useSelector(
        (state) =>
            (
                (state[loadTestLastExecutionCardSlice.name] || initialState).loadTests[loadTestId] ||
                LastLoadTestHistoryInitial
            ).executionId,
    );
}
