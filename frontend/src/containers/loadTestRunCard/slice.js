import { createSlice } from '@reduxjs/toolkit';
import { useInjectReducer, useInjectSaga } from 'redux-injectors';
import saga from './saga';
import { useSelector } from 'react-redux';
import { flatCamelize } from '../../utils/to-camel-case';

const initialLoadTestCard = {
    fetchStatus: 'idle',
    status: 'idle',
    parametersValues: {},
    executionConfigValues: {},

    numberOfTasks: 0,
};

const initialState = {
    loadTests: {},
};

export const loadTestRunCardSlice = createSlice({
    name: 'loadTestRunCard',
    initialState,
    reducers: {
        fetch: () => {},
        fetchStart: (state, { payload: { loadTestId } }) => {
            state.loadTests[loadTestId] = { ...state.loadTests[loadTestId], ...initialLoadTestCard };
            state.loadTests[loadTestId].fetchStatus = 'pending';
        },
        fetchSuccess: (state, { payload: { loadTestId, data } }) => {
            const { params, ...restData } = data;
            state.loadTests[loadTestId] = {
                ...state.loadTests[loadTestId],
                ...flatCamelize(restData),
                params: Object.fromEntries(
                    Object.entries(params).map(([paramName, paramValue]) => [
                        paramName,
                        {
                            ...flatCamelize(paramValue),
                            valid: null,
                        },
                    ]),
                ),
                executionConfigValues: restData.config,
                numberOfTasks: restData.config['concurrency_within_a_single_worker'],
            };
            state.loadTests[loadTestId].fetchStatus = 'success';
        },
        fetchError: (state, { payload: { loadTestId, e } }) => {
            state.loadTests[loadTestId].fetchStatus = 'error';
            console.log('Fetch one load test error', e);
        },

        setLoadTestParamValue: (state, { payload: { loadTestId, paramName, paramValue } }) => {
            state.loadTests[loadTestId].parametersValues[paramName] = paramValue;
            state.loadTests[loadTestId].params[paramName].valid = true;
        },

        markParamAsInvalid: (state, { payload: { loadTestId, paramNames } }) => {
            paramNames.forEach((name) => (state.loadTests[loadTestId].params[name].valid = false));
        },

        setLoadTestExecutionParamValue: (state, { payload: { loadTestId, paramName, paramValue } }) => {
            state.loadTests[loadTestId].executionConfigValues[paramName] = paramValue;
            state.loadTests[loadTestId].numberOfTasks = 0;
        },

        setNumberOfTasks: (state, { payload: { loadTestId, numberOfTasks } }) => {
            state.loadTests[loadTestId].numberOfTasks = numberOfTasks;
        },

        startLoadTest: () => {},
        loadTestStart: () => {},
        loadTestStartSuccess: () => {},
        loadTestStartError: (_, { payload: { e } }) => {
            console.log('Start load test error', e);
        },

        stopLoadTest: () => {},
        loadTestStop: () => {},
        loadTestStopSuccess: () => {},
        loadTestStopError: (_, { payload: { e } }) => {
            console.log('Stop load test error', e);
        },

        changeNumberOfWorkers: () => {},
        changeNumberOfWorkersStart: () => {},
        changeNumberOfWorkersStartSuccess: () => {},
        changeNumberOfWorkersStartError: (_, { payload: { e } }) => {
            console.log('Change number of workers error', e);
        },
    },
});

export const { actions } = loadTestRunCardSlice;

export const useLoadTestRunCardSlice = () => {
    useInjectReducer({
        key: loadTestRunCardSlice.name,
        reducer: loadTestRunCardSlice.reducer,
    });
    useInjectSaga({ key: loadTestRunCardSlice.name, saga: saga });
    return { actions: loadTestRunCardSlice.actions };
};

export function useLoadTestRunCardSelector(loadTestId) {
    return useSelector(
        (state) => (state[loadTestRunCardSlice.name] || initialState).loadTests[loadTestId] || initialLoadTestCard,
    );
}

export function useLoadTestChartConfigSelector(loadTestId) {
    return useSelector(
        (state) =>
            ((state[loadTestRunCardSlice.name] || initialState).loadTests[loadTestId] || initialLoadTestCard).charts,
    );
}
