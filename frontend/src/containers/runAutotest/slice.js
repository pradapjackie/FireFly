import { createSlice } from '@reduxjs/toolkit';
import { camelize, flatCamelize } from '../../utils/to-camel-case';
import { useInjectReducer, useInjectSaga } from 'redux-injectors';
import saga from './saga';
import { useSelector } from 'react-redux';

const initialFolderState = {
    status: 'idle',
    groups: {},
    items: {},
    focusedTest: '',
    runConfig: {},
    dynamicData: {},
};

const initialState = {};

const updateGroupSelectedState = (state, groupId, folder) => {
    let allSelected = true;
    let allDeselected = true;
    const group = state[folder].groups.entities[groupId];

    if (group.groups) {
        for (let nestedGroupID of group.groups) {
            updateGroupSelectedState(state, nestedGroupID, folder);
            const { selected, indeterminate } = state[folder].groups.entities[nestedGroupID];
            allSelected = indeterminate || !selected ? false : allSelected;
            allDeselected = indeterminate || selected ? false : allDeselected;
        }
    }
    if (group.items) {
        for (const testId of group.items) {
            const { selected } = state[folder].items.entities[testId];
            allSelected = !selected ? false : allSelected;
            allDeselected = selected ? false : allDeselected;
        }
    }
    group.indeterminate = !allSelected && !allDeselected;
    group.selected = !group.indeterminate && allSelected;
};

const recursiveGroupUpdate = (state, groupId, value, stateSubFolderName) => {
    const group = state[stateSubFolderName].groups.entities[groupId];
    group.selected = value;
    group.indeterminate = false;
    if (group.groups) {
        for (const id of group.groups) {
            id && recursiveGroupUpdate(state, id, value, stateSubFolderName);
        }
    }
    if (group.items) {
        for (const testId of group.items) {
            const test = state[stateSubFolderName].items.entities[testId];
            test.selected = value;
        }
    }
};

const recalculateSelectedState = (state, stateSubFolderName) => {
    const folderState = state[stateSubFolderName] || initialFolderState
    const { firstLevel } = folderState.groups;
    firstLevel.forEach((groupId) => updateGroupSelectedState(state, groupId, stateSubFolderName));
};

export const runAutotestSlice = createSlice({
    name: 'runAutotest',
    initialState,
    reducers: {
        fetch: () => {},
        run: () => {},
        runStart: () => {},
        runSuccess: () => {},
        runError: () => {},
        fetchStart: (state, { payload: { folder } }) => {
            state[folder] = { ...initialFolderState, ...state[folder]};
            state[folder].status = 'pending';
        },
        fetchSuccess: (state, { payload: { folder, data } }) => {
            state[folder].groups.ids = data.groups.ids;
            state[folder].groups.firstLevel = data.groups.first_level;
            let groupMap = data.groups.groups_map;
            for (const [group_name, value] of Object.entries(groupMap)) {
                value.items = value.auto_tests;
                value.selected = false;
                value.expanded = group_name.split('.').length <= 1;
                value.indeterminate = false;
                delete value.auto_tests;
            }
            state[folder].groups.entities = groupMap;

            state[folder].items.ids = data.items.ids;
            let testMap = data.items.auto_test_map;
            for (const [name, value] of Object.entries(testMap)) {
                const { required_run_config: requiredRunConfig, ...restValues } = value;
                value.selected = false;
                testMap[name] = {
                    ...flatCamelize(restValues),
                    requiredRunConfig: Object.fromEntries(
                        Object.entries(requiredRunConfig).map(([paramName, paramValue]) => [
                            paramName,
                            {
                                ...flatCamelize(paramValue),
                                valid: null,
                            },
                        ]),
                    ),
                };
            }
            state[folder].items.entities = testMap;
            state[folder].status = 'success';
        },
        fetchError: (state, { payload: { folder, e } }) => {
            state[folder].status = 'error';
            console.log('Fetch error', e);
        },
        groupSelected: (state, { payload: { groupId, value, stateSubFolderName } }) => {
            recursiveGroupUpdate(state, groupId, value, stateSubFolderName);
            recalculateSelectedState(state, stateSubFolderName);
        },
        testSelected: (state, { payload: { testId, value, stateSubFolderName } }) => {
            const test = state[stateSubFolderName].items.entities[testId];
            test.selected = value;
            recalculateSelectedState(state, stateSubFolderName);
        },
        testFocused: (state, { payload: { testId, folder } }) => {
            state[folder] = { ...initialFolderState, ...state[folder]};
            state[folder].focusedTest = testId;
        },
        setRunConfig: (state, { payload: { name, value, folder } }) => {
            state[folder].runConfig[name] = value;
        },
        fetchDynamicData: () => {},
        fetchDynamicDataStart: (state, { payload: { alias, folder } }) => {
            state[folder] = { ...initialFolderState, ...state[folder]};
            state[folder].dynamicData[alias] = { status: 'pending' };
        },
        fetchDynamicDataSuccess: (state, { payload: { alias, folder, data } }) => {
            state[folder].dynamicData[alias].data = camelize(data);
            state[folder].dynamicData[alias].status = 'success';
        },
        fetchDynamicDataError: (state, { payload: { alias, folder, error } }) => {
            state[folder].dynamicData[alias].status = 'error';
            console.log('fetchDynamicDataError', error);
        },
    },
});

export const { actions } = runAutotestSlice;

export const useRunAutotestSlice = () => {
    useInjectReducer({ key: runAutotestSlice.name, reducer: runAutotestSlice.reducer });
    useInjectSaga({ key: runAutotestSlice.name, saga: saga });
    return { actions: runAutotestSlice.actions };
};

export function useRunAutotestSliceSelector(folder, selector) {
    return useSelector((state) => selector((state[runAutotestSlice.name] || initialState)[folder] || initialFolderState));
}
