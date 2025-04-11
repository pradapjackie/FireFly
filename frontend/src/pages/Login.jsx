import React from 'react';
import { Card, Box, Grid } from '@mui/material';
import { LoginWidget } from 'containers/auth/LoginWidget';
import { NavLink } from 'react-router-dom';

const LoginPage = () => {
    return (
        <Box
            sx={{
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                minHeight: '100vh !important',
                background: '#1A2038',
            }}
        >
            <Card
                sx={{
                    maxWidth: 800,
                    borderRadius: '12px',
                    margin: '1rem',
                }}
            >
                <Grid container>
                    <Grid item lg={5} md={5} sm={5} xs={12}>
                        <Box
                            sx={{
                                display: 'flex',
                                justifyContent: 'center',
                                alignItems: 'center',
                                height: '100% !important',
                                padding: '2rem',
                            }}
                        >
                            <Box
                                component={'img'}
                                sx={{ width: '200px' }}
                                src="/assets/images/illustrations/dreamer.svg"
                                alt=""
                            />
                        </Box>
                    </Grid>
                    <Grid item lg={7} md={7} sm={7} xs={12}>
                        <Box
                            sx={{
                                padding: '2rem',
                                height: '100% !important',
                                background: 'rgba(0, 0, 0, 0.01) !important',
                                position: 'relative',
                            }}
                        >
                            <LoginWidget />
                            <Box>
                                Don't have an account?
                                <Box
                                    component={NavLink}
                                    to={'/session/signup'}
                                    sx={{ marginLeft: 1, color: 'primary.main' }}
                                >
                                    Register
                                </Box>
                            </Box>
                        </Box>
                    </Grid>
                </Grid>
            </Card>
        </Box>
    );
};

export default LoginPage;
