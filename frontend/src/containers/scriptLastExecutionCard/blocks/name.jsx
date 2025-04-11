import React from 'react';
import Typography from '@mui/material/Typography';
import { Box } from '@mui/material';
import { StatusChip } from 'components/StatusChip';

export const Name = ({ name, status }) => {
    return (
        <Box sx={{ display: 'flex', borderRadius: '4px' }}>
            <Typography variant="h6" color="textSecondary">
                {name}
            </Typography>
            <StatusChip status={status} position={'right'}/>
        </Box>
    );
};
