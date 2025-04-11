import React from 'react';
import { Box, Chip } from '@mui/material';

export const StatusChip = ({ status, position = 'left' }) => {
    return (
        <Chip
            sx={[
                {
                    borderRadius: '4px',
                    color: 'rgba(255, 255, 255, 1)',
                    fontSize: '1rem',
                    marginBottom: 0,
                    minWidth: 'fit-content',
                },
                position === 'left' && { marginRight: '1.25rem' },
                position === 'right' && { marginLeft: '1.25rem' },
                status === 'success' || status === "running" && { background: '#08ad6c' },
                status === 'partial_success' && {backgroundColor: 'secondary.main', color: 'white'},
                status === 'fail' && { backgroundColor: 'error.main', color: 'white' },
            ]}
            label={status.toUpperCase().replace('_', ' ')}
            color="primary"
        />
    );
};

export const SmallStatusChip = ({ status }) => {
    return (
        <Box
            component={'small'}
            sx={[
                {
                    borderRadius: '4px',
                    color: 'rgba(255, 255, 255, 1)',
                    paddingLeft: '0.5rem',
                    paddingRight: '0.5rem',
                    paddingTop: '1px',
                    paddingBottom: '1px',
                    textTransform: 'uppercase',
                    fontSize: 'small',
                    letterSpacing: 'normal',
                },
                status === 'success' && { background: '#08ad6c' },
                status === 'fail' && { backgroundColor: 'error.main' },
                status === 'partial_success' && {backgroundColor: 'secondary.main' },
            ]}
        >
            {status.replace('_', ' ')}
        </Box>
    );
};
