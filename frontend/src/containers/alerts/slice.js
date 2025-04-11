import { createSlice } from '@reduxjs/toolkit';

const initialState = {
    severity: '',
    text: '',
    open: false,
};

export const alertSlice = createSlice({
    name: 'alert',
    initialState,
    reducers: {
        newAlert: (state, { payload: { severity, text } }) => {
            state.severity = severity;
            state.text = text;
            state.open = true;
        },
        closeAlert: (state) => {
            state.open = false;
        },
    },
});

export const { name, actions, reducer } = alertSlice;
