import React from 'react';
import Typography from '@mui/material/Typography';

export const Name = ({ name }) => {
    return (
        <Typography variant="h6" color="textSecondary">
            {name}
        </Typography>
    );
};
