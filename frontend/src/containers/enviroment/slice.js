import { createSlice } from '@reduxjs/toolkit';
import { useInjectReducer, useInjectSaga } from 'redux-injectors';
import saga from './saga';
import { useSelector } from 'react-redux';
import { createSelector } from 'reselect';

const initialState = {
    status: 'idle',
    selected: '',
    ids: [],
    entities: {
        ids: [],
        entities: {},
    },
};

const envSlice = createSlice({
    name: 'env',
    initialState,
    reducers: {
        fetch: () => {},
        fetchStart: (state) => {
            state.status = 'pending';
        },
        fetchSuccess: (state, { payload: { ids, activeEnv } }) => {
            state.selected = activeEnv || 'trunk';
            state.ids = ids;
            state.ids.forEach((id) => {
                if (!state.entities[id]) {
                    state.entities[id] = { status: 'idle', ids: [], entities: {} };
                }
            });
            state.status = 'success';
        },
        fetchError: (state, { payload }) => {
            state.status = 'error';
            console.log('Fetch error', payload);
        },
        fetchByEnv: () => {},
        fetchByEnvStart: (state, { payload: { env } }) => {
            state.entities[env] = { status: 'pending' };
        },
        fetchByEnvSuccess: (state, { payload: { env, overwrite, data } }) => {
            state.entities[env]['ids'] = data.map((item) => item.param);
            const entitiesMap = {};
            data.forEach(
                (paramObject) =>
                    (entitiesMap[paramObject.param] = {
                        value: paramObject.value,
                        secure: paramObject.secure,
                        overwrite: overwrite[paramObject.param],
                        initial: {
                            value: paramObject.value,
                            secure: paramObject.secure,
                            overwrite: overwrite[paramObject.param],
                        },
                    }),
            );
            state.entities[env].entities = entitiesMap;
            state.entities[env].status = 'success';
        },
        fetchByEnvError: (state, { payload: { e, env } }) => {
            console.log('Fetch error', e);
            state.entities[env].status = 'error';
        },
        saveSelected: () => {},
        setSelected: (state, { payload: { selected } }) => {
            state.selected = selected;
        },
        editNewName: (state, { payload: { env, param, newName } }) => {
            state.entities[env].entities[param].newName = newName;
        },
        editValue: (state, { payload: { env, param, valueName, value } }) => {
            const item = state.entities[env].entities[param];
            item[valueName] = value;
            item.valueChanged = !item.isNew && value !== item.initial[valueName];
        },
        editOverwriteValue: (state, { payload: { env, param, value } }) => {
            const item = state.entities[env].entities[param];
            item.overwrite = value;
            item.overwriteChanged = !item.isNew && value !== item.initial.overwrite;
        },
        addParam: (state, { payload: { env, param } }) => {
            state.entities[env].entities[param] = {
                value: '',
                overwrite: '',
                secure: false,
                isNew: true,
                newName: '',
                initial: {},
            };
            state.entities[env].ids.push(param);
            state.entities[env].status = 'success';
        },
        saveLocalEnv: () => {},
        saveLocalEnvError: (state, action) => {
            console.log('Error during local env saving', action.payload);
        },
        saveGlobalEnv: (state, { payload: { env } }) => {
            state.entities[env].status = 'pending';
        },
        saveGlobalEnvSuccess: (state, { payload: { env } }) => {
            const idsToRemove = [];
            const idsToAdd = [];
            state.entities[env].ids.forEach((id) => {
                const oldItem = state.entities[env].entities[id];
                oldItem.valueChanged = false;
                oldItem.overwriteChanged = false;
                oldItem.value = oldItem.secure ? 'REPLACE_THIS' : oldItem.value;
                oldItem.initial = {
                    value: oldItem.value,
                    secure: oldItem.secure,
                    overwrite: oldItem.overwrite,
                };
                if (state.entities[env].entities[id].isNew) {
                    state.entities[env].entities[oldItem.newName] = oldItem;
                    idsToAdd.push(oldItem.newName);
                    idsToRemove.push(id);
                    delete state.entities[env].entities[oldItem.newName].isNew;
                    delete state.entities[env].entities[oldItem.newName].newName;
                }
                if (state.entities[env].entities[id].toRemove) {
                    idsToRemove.push(id);
                }
                delete state.entities[env].entities[id].toRemove;
                delete state.entities[env].entities[id].overwriteChanged;
            });
            const oldIds = state.entities[env].ids;
            state.entities[env].ids = oldIds.filter((item) => !idsToRemove.includes(item)).concat(idsToAdd);
            state.entities[env].status = 'success';
        },
        saveGlobalEnvError: (state, action) => {
            console.log('Error during global env saving', action.payload);
        },
        markRowToRemove: (state, { payload: { env, param } }) => {
            state.entities[env].entities[param].toRemove = true;
        },
        removeNewRow: (state, { payload: { env, param } }) => {
            state.entities[env].ids = state.entities[env].ids.filter((item) => item !== param);
            delete state.entities[env].entities[param];
        },
        markRowToRestore: (state, { payload: { env, param } }) => {
            state.entities[env].entities[param].toRemove = false;
        },
    },
});

export const { actions } = envSlice;

export const useEnvSlice = () => {
    useInjectReducer({ key: envSlice.name, reducer: envSlice.reducer });
    useInjectSaga({ key: envSlice.name, saga: saga });
    return { actions: envSlice.actions };
};

export function useEnvSliceSelector(selector) {
    return useSelector((state) => selector(state[envSlice.name] || initialState));
}

export function useSelectedEnvName() {
    return useSelector((state) => (state[envSlice.name] || initialState).selected);
}

const selectedEnv = createSelector(
    [(state) => state.selected, (state) => state.entities],
    (selectedEnv, envs) => envs[selectedEnv],
);

export function useSelectedEnv() {
    return useSelector((state) => selectedEnv(state[envSlice.name] || initialState));
}
