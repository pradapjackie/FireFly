import React from 'react';
import { Alert, Snackbar } from '@mui/material';
import { useDispatch, useSelector } from 'react-redux';
import { actions, name } from './slice';

export default function AppAlert() {
    const dispatch = useDispatch();
    const { severity, text, open } = useSelector((state) => state[name]);

    const handleClose = (_, reason) => {
        if (reason !== 'clickaway') {
            dispatch(actions.closeAlert());
        }
    };

    return (
        <Snackbar open={open} autoHideDuration={12000} onClose={handleClose}>
            <Alert onClose={handleClose} severity={severity || "info"} variant="filled" sx={{ width: '100%' }}>
                {text}
            </Alert>
        </Snackbar>
    );
}
