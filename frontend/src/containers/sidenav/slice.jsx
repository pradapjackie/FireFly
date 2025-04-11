import { createSlice } from '@reduxjs/toolkit';
import { useInjectReducer, useInjectSaga } from 'redux-injectors';
import { useSelector } from 'react-redux';
import saga from './saga';

const initialState = {
    status: 'idle',
    navigations: [
        {
            name: 'Dashboard',
            path: '/dashboard',
            icon: 'dashboard',
        },
        {
            label: 'Pages',
            type: 'label',
        },

        {
            name: 'Autotest',
            icon: 'account_tree',
            children: [],
        },
        {
            name: 'Script runner',
            icon: 'vertical_split',
            children: [],
        },
        {
            name: 'Load tests',
            icon: 'vertical_split',
            children: [],
        },
        {
            name: 'Healths',
            path: '/health',
            icon: 'favorite',
        },
        {
            name: 'Mock',
            path: '/mock',
            icon: 'developer_mode',
        },
    ],
};

export const menuSlice = createSlice({
    name: 'menu',
    initialState,
    reducers: {
        startMenuLoad: () => {},
        MenuLoadStarted: (state) => {
            state.status = 'loading';
        },
        MenuLoadSucceed: (state, { payload }) => {
            state.status = 'available';
            const testsItems = payload.tests.map(str => ({
                name: str.toUpperCase(),
                path: `/auto/${str}`,
                iconText: str.slice(0, 2).toUpperCase(),
            }));
            const scriptsItems = payload.scripts.map(str => ({
                name: str.toUpperCase(),
                path: `/script_runner/${str}`,
                iconText: str.slice(0, 2).toUpperCase(),
            }));
            const loadTestsItems = payload.loadTests.map(str => ({
                name: str.toUpperCase(),
                path: `/load_test/${str}`,
                iconText: str.slice(0, 2).toUpperCase(),
            }));
            state.navigations = state.navigations.map((item) =>
                item.name === 'Autotest' ? { ...item, children: testsItems } :
                item.name === 'Script runner' ? { ...item, children: scriptsItems } :
                item.name === 'Load tests' ? { ...item, children: loadTestsItems } : item,
            );
        },
        MenuLoadError: (state, { payload }) => {
            console.log('Error during dynamic menu items saving', payload);
            state.status = 'available';
        },
    },
});

export const { actions } = menuSlice;

export const useMenuSlice = () => {
    useInjectReducer({ key: menuSlice.name, reducer: menuSlice.reducer });
    useInjectSaga({ key: menuSlice.name, saga: saga });
    return { actions: menuSlice.actions };
};

export function useMenuSliceSelector(selector) {
    return useSelector((state) => selector(state[menuSlice.name] || initialState));
}
