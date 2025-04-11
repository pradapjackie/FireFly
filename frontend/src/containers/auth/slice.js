import { createSlice } from '@reduxjs/toolkit';

const initialState = {
    sessionChecked: false,
    isAuthorized: false,
    sessionError: false,
    authLoading: false,
    authError: false,
    user: {},
    signUpStatus: 'idle',
    signUpError: null,
};

export const authSlice = createSlice({
    name: 'auth',
    initialState,
    reducers: {
        startSessionCheck: () => {},
        sessionChecked: (state) => {
            state.sessionChecked = true;
        },
        sessionStarted: (state, action) => {
            state.isAuthorized = true;
            state.user = action.payload.user;
        },
        sessionError: (state, action) => {
            state.isAuthorized = false;
            state.sessionError = action.payload.error;
        },

        authStart: (state) => {
            state.authLoading = true;
            state.authError = false;
        },
        authSuccess: (state) => {
            state.authLoading = false;
        },
        authError: (state, action) => {
            state.authError = action.payload.error;
            state.isAuthorized = false;
            state.authLoading = false;
        },

        logout: (state) => {
            state.user = {};
            state.isAuthorized = false;
            state.authLoading = false;
            state.authError = false;
            state.sessionChecked = true;
        },

        signUp: state => {},

        signUpStart: (state) => {
            state.signUpStatus = 'pending';
        },

        signUpSuccess: (state) => {
          state.signUpStatus = 'success';
        },

        signUpError: (state, { payload: { e } }) => {
          state.signUpError = e.response.data.detail
          state.signUpStatus = 'error';
          console.log('Sign up error', e);
        }
    },
});

export const { name, actions, reducer } = authSlice;
