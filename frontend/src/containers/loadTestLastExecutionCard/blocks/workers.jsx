import React from 'react';
import { Box } from '@mui/material';
import { LoadWorkers } from 'components/Charts/LoadWorkers';
import Typography from '@mui/material/Typography';

export const Workers = ({ workers }) => {
    return (
        <Box sx={{ borderRadius: '4px' }}>
            <Typography sx={{ fontWeight: '700' }} variant={'subtitle1'}>
                Worker status:
            </Typography>
            <LoadWorkers workers={workers} />
        </Box>
    );
};
