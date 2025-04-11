import {createSlice} from '@reduxjs/toolkit';
import {useInjectReducer, useInjectSaga} from "redux-injectors";
import {useSelector} from "react-redux";
import saga from "./saga";

const initialState = {
  status: 'available'
};

export const devSlice = createSlice({
  name: 'dev',
  initialState,
  reducers: {
    reCollect: () => {
    },
    reCollectStart: (state) => {
      state.status = 'loading'
    },
    reCollectSuccess: (state) => {
      state.status = 'available'
    },
    reCollectError: (state, {payload}) => {
      console.log("Error during local env saving", payload)
      state.status = 'available'
    },
  },
});

export const {actions} = devSlice;

export const useDevSlice = () => {
  useInjectReducer({key: devSlice.name, reducer: devSlice.reducer});
  useInjectSaga({key: devSlice.name, saga: saga});
  return {actions: devSlice.actions};
};


export function useDevSliceSelector(selector) {
  return useSelector((state) => selector(state[devSlice.name] || initialState))
}
