import React from 'react';
import { Card, Box, Grid, Divider } from '@mui/material';
import { RegistrationWidget } from 'containers/auth/RegistrationWidget';
import Typography from '@mui/material/Typography';

const RegistrationPage = () => {
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
                    minWidth: 650,
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
                                src="/assets/images/illustrations/welcome.svg"
                                alt=""
                            />
                        </Box>
                    </Grid>
                    <Grid item lg={7} md={7} sm={7} xs={12}>
                        <Box
                            sx={{
                                padding: '2rem',
                                background: 'rgba(0, 0, 0, 0.01) !important',
                                position: 'relative',
                            }}
                        >
                            <RegistrationWidget />
                        </Box>
                        <Divider
                            sx={{ borderColor: 'rgba(255, 255, 255, 0.7)' }}
                        />
                        <Typography
                            sx={{
                                padding: '1rem',
                                color: 'rgba(255, 255, 255, 0.7)'
                            }}
                            variant={'subtitle2'}
                        >
                            Registration in the service is required to track the launch of scripts and autotests, as
                            well as for displaying personalized information.
                        </Typography>
                    </Grid>
                </Grid>
            </Card>
        </Box>
    );
};

export default RegistrationPage;
