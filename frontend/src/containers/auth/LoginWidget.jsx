import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import LoadingButton from '@mui/lab/LoadingButton';
import { Box } from '@mui/material';
import { TextValidator, ValidatorForm } from 'react-material-ui-form-validator';
import history from '../../history';
import { name, actions } from './slice';

export const LoginWidget = () => {
    const isAuthorized = useSelector((state) => state[name].isAuthorized);
    const authLoading = useSelector((state) => state[name].authLoading);
    const [userInfo, setUserInfo] = useState({ username: '', password: '' });

    const dispatch = useDispatch();
    const dispatchLogin = (userInfo) => () => {
        dispatch(actions.authStart(userInfo));
    };

    useEffect(() => {
        dispatch(actions.startSessionCheck({}));
    }, []);

    useEffect(() => {
        if (isAuthorized) {
            history.push(history?.location?.state?.redirectUrl || '/');
        }
    }, [isAuthorized]);

    const handleChange = ({ target: { name, value } }) => setUserInfo({ ...userInfo, [name]: value });

    return (
        <ValidatorForm onSubmit={dispatchLogin(userInfo)}>
            <TextValidator
                sx={{
                    marginBottom: '1.5rem',
                    width: '100%',
                    '& .MuiInputBase-input': {
                        WebkitBoxShadow: '0 0 0 100px var(--bg-paper) inset !important',
                    },
                }}
                variant="outlined"
                size="small"
                label="Email"
                onChange={handleChange}
                type="email"
                name="username"
                value={userInfo.username}
                validators={['required', 'isEmail']}
                errorMessages={['this field is required', 'email is not valid']}
                focused={true}
            />
            <TextValidator
                sx={{
                    marginBottom: '1rem',
                    width: '100%',
                    '& .MuiInputBase-input': {
                        WebkitBoxShadow: '0 0 0 100px var(--bg-paper) inset !important',
                    },
                }}
                label="Password"
                variant="outlined"
                size="small"
                onChange={handleChange}
                name="password"
                type="password"
                value={userInfo.password}
                validators={['required']}
                errorMessages={['this field is required']}
                autoComplete="off"
                focused={true}
            />

            <Box
                sx={{
                    display: 'flex',
                    flexWrap: 'wrap',
                    alignItems: 'center',
                    marginBottom: '1rem',
                }}
            >
                <Box sx={{ position: 'relative' }}>
                    <LoadingButton variant="contained" color="primary" loading={authLoading} type="submit">
                        Sign in
                    </LoadingButton>
                </Box>
            </Box>
        </ValidatorForm>
    );
};
