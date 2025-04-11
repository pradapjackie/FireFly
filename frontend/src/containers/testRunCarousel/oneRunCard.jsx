import React from 'react';
import { Card, Fab, CircularProgress, Zoom, Box } from '@mui/material';
import { Link } from 'react-router-dom';
import { Done, Close, HourglassEmpty } from '@mui/icons-material';
import { useTestRunCarouselSliceSelector } from './slice';
import { format } from 'date-fns';
import Typography from '@mui/material/Typography';

export const OneRunCard = ({ id, folder }) => {
    const {
        status,
        resultByStatus: { success, pending, fail },
        startTime,
    } = useTestRunCarouselSliceSelector(folder, (state) => state.entities[id]);

    const chipStyles = {
        borderRadius: '4px',
        paddingLeft: '0.5rem',
        paddingRight: '0.5rem',
        paddingTop: '2px',
        paddingBottom: '2px',
        marginRight: '2px',
    };

    const cardIcon = (status) => {
        if (['pending', 'primed', 'running'].includes(status)) {
            return (
                <CircularProgress
                    sx={{
                        marginTop: '1rem',
                        marginBottom: '1rem',
                        marginRight: '1rem',
                        minHeight: '40px',
                        minWidth: '40px',
                    }}
                />
            );
        } else {
            let icon, color;
            switch (status) {
                case 'success':
                    icon = <Done />;
                    color = 'success';
                    break;
                case 'idle':
                    icon = <HourglassEmpty />;
                    color = 'primary';
                    break;
                default:
                    icon = <Close />;
                    color = 'error';
            }

            return (
                <Fab
                    size="small"
                    color={color}
                    sx={{
                        marginTop: '1rem',
                        marginBottom: '1rem',
                        marginRight: '1rem',
                        boxShadow: 'none',
                        color: 'rgba(255, 255, 255, 1)',
                        minHeight: '40px',
                        minWidth: '40px',
                    }}
                >
                    {icon}
                </Fab>
            );
        }
    };

    return (
        <Zoom in timeout={700}>
            <Box>
                <Link to={`/auto/history/${folder}/${id}`}>
                    <Card
                        sx={{
                            display: 'flex',
                            alignItems: 'stretch',
                            paddingLeft: '1rem',
                            paddingRight: '1rem',
                            background: 'background.paper',
                            margin: '0.25rem',
                            gap: '10px',
                            width: 'max-content',
                        }}
                        elevation={12}
                    >
                        {cardIcon(status)}
                        <Box
                            sx={{
                                marginLeft: 0,
                                display: 'flex',
                                flexDirection: 'column',
                                justifyContent: 'space-around',
                                paddingTop: '0.5rem',
                                paddingBottom: '0.5rem',
                            }}
                        >
                            <Box sx={{ display: 'flex' }}>
                                <Box
                                    component={'small'}
                                    sx={{
                                        ...chipStyles,
                                        color: '#08ad6c',
                                        backgroundColor: 'rgba(8, 173, 108,.1)',
                                        borderColor: '#08ad6c',
                                    }}
                                >
                                    {success}
                                </Box>
                                <Box
                                    component={'small'}
                                    sx={{
                                        ...chipStyles,
                                        color: 'rgba(255, 255, 255, 0.7)',
                                        backgroundColor: 'rgba(255, 255, 255, 0.1)',
                                        borderColor: 'rgba(255, 255, 255, 0.7)',
                                    }}
                                >
                                    {pending}
                                </Box>
                                <Box
                                    component={'small'}
                                    sx={{
                                        ...chipStyles,
                                        color: '#ec412c',
                                        backgroundColor: 'rgba(236,65,44,.1)',
                                        borderColor: '#ec412c',
                                    }}
                                >
                                    {fail}
                                </Box>
                            </Box>
                            <Typography>{format(new Date(startTime), 'dd.MM.yyyy HH:mm')}</Typography>
                        </Box>
                    </Card>
                </Link>
            </Box>
        </Zoom>
    );
};
