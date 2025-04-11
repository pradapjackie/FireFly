import { createSlice } from '@reduxjs/toolkit';
import { useInjectReducer, useInjectSaga } from 'redux-injectors';
import saga from './saga';
import { useSelector } from 'react-redux';
import { flatCamelize } from '../../utils/to-camel-case';

const initialScriptCard = {
    fetchStatus: 'idle',
    status: 'idle',
    parametersValues: {},
};

const initialState = {
    scripts: {},
};

export const scriptRunCardSlice = createSlice({
    name: 'scriptRunCard',
    initialState,
    reducers: {
        fetch: () => {},
        fetchStart: (state, { payload: { scriptId } }) => {
            state.scripts[scriptId] = { ...state.scripts[scriptId], ...initialScriptCard };
            state.scripts[scriptId].fetchStatus = 'pending';
        },
        fetchSuccess: (state, { payload: { scriptId, data } }) => {
            const { params, ...restData } = data;
            state.scripts[scriptId] = {
                ...state.scripts[scriptId],
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
            };
            state.scripts[scriptId].fetchStatus = 'success';
        },
        fetchError: (state, { payload: { scriptId, e } }) => {
            state.scripts[scriptId].fetchStatus = 'error';
            console.log('Fetch test run statistic error', e);
        },

        setScriptParamValue: (state, { payload: { scriptId, paramName, paramValue } }) => {
            state.scripts[scriptId].parametersValues[paramName] = paramValue;
            state.scripts[scriptId].params[paramName].valid = true;
        },

        markParamAsInvalid: (state, { payload: { scriptId, paramNames } }) => {
            paramNames.forEach(name => state.scripts[scriptId].params[name].valid = false);
        },

        runScript: () => {},
        scriptStart: () => {},
        scriptStartSuccess: () => {},
        scriptStartError: (_, { payload: { e } }) => {
            console.log('Run script error', e);
        },
    },
});

export const { actions } = scriptRunCardSlice;

export const useScriptRunCardSlice = () => {
    useInjectReducer({
        key: scriptRunCardSlice.name,
        reducer: scriptRunCardSlice.reducer,
    });
    useInjectSaga({ key: scriptRunCardSlice.name, saga: saga });
    return { actions: scriptRunCardSlice.actions };
};

export function useScriptRunCardSelector(scriptId) {
    return useSelector(
        (state) => (state[scriptRunCardSlice.name] || initialState).scripts[scriptId] || initialScriptCard,
    );
}
