import React, { useEffect, useState } from 'react';
import LoadingButton from '@mui/lab/LoadingButton';
import { Box } from '@mui/material';
import { TextValidator, ValidatorForm } from 'react-material-ui-form-validator';
import { actions, name } from './slice';
import { useDispatch, useSelector } from 'react-redux';
import Typography from '@mui/material/Typography';
import history from '../../history';

export const RegistrationWidget = () => {
    const dispatch = useDispatch();
    const status = useSelector((state) => state[name].signUpStatus);
    const error = useSelector((state) => state[name].signUpError);
    const isAuthorized = useSelector((state) => state[name].isAuthorized);
    const [formData, setFormData] = useState({ fullName: '', email: '', password: '' });
    const handleChange = ({ target: { name, value } }) => setFormData({ ...formData, [name]: value });

    const dispatchSignUp = (formData) => () => {
        dispatch(actions.signUp(formData));
    };

    useEffect(() => {
        if (isAuthorized) {
            history.push(history?.location?.state?.redirectUrl || '/');
        }
    }, [isAuthorized]);

    return (
        <ValidatorForm onSubmit={dispatchSignUp(formData)}>
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
                label="Full Name"
                onChange={handleChange}
                type="text"
                name="fullName"
                value={formData.fullName}
                validators={['required']}
                errorMessages={['this field is required']}
            />
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
                name="email"
                value={formData.email}
                validators={['required', 'isEmail']}
                errorMessages={['this field is required', 'email is not valid']}
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
                value={formData.password}
                validators={['required']}
                errorMessages={['this field is required']}
                autoComplete="off"
            />

            <Box
                sx={{
                    display: 'flex',
                    flexWrap: 'wrap',
                    alignItems: 'center',
                }}
            >
                <Box sx={{ position: 'relative' }}>
                    {status === 'error' && (
                        <Typography
                            sx={{
                                paddingBottom: '1rem',
                                color: 'error.main',
                            }}
                            variant={'body1'}
                        >
                            {error}
                        </Typography>
                    )}
                    <LoadingButton variant="contained" color="primary" loading={status === 'pending'} type="submit">
                        Sign up
                    </LoadingButton>
                </Box>
            </Box>
        </ValidatorForm>
    );
};
