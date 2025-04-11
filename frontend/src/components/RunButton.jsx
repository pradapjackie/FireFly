import { Button } from '@mui/material';
import React from 'react';

export const RunButton = ({ text, runCallback, isDisabled, isSuccess = true }) => {
    return (
        <Button
            onClick={runCallback}
            variant="contained"
            disabled={isDisabled}
            sx={[
                !isDisabled && {
                    backgroundColor: isSuccess ? 'rgba(9, 182, 109, 1)' : 'rgba(255, 61, 87, 1)',
                    background: isSuccess ? '#08ad6c' : '#FF3D57',
                    '&:hover': {
                        background: isSuccess ? `rgba(9, 182, 109, 1) !important` : `rgba(255, 61, 87, 1) !important`,
                        backgroundColor: isSuccess
                            ? `rgba(9, 182, 109, 1) !important`
                            : `rgba(255, 61, 87, 1) !important`,
                    },
                },
                {
                    margin: 0,
                    width: '100%',
                    color: 'rgba(0, 0, 0, 0.87)',
                },
            ]}
        >
            {text}
        </Button>
    );
};
