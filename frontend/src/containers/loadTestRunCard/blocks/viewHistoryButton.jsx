import React from 'react';
import { Button } from '@mui/material';
import RedoIcon from '@mui/icons-material/Redo';

export const ViewHistoryButton = ({ switchToHistory }) => {
    return (
        <Button
            onClick={switchToHistory}
            sx={{
                top: '-15px',
                right: '-25px',
                borderRadius: '0px',
                minWidth: '150px',
            }}
            variant="contained"
            endIcon={<RedoIcon />}
        >
            View history
        </Button>
    );
};
