import React from 'react';
import { Button } from '@mui/material';
import RedoIcon from '@mui/icons-material/Redo';

export const ReturnToScriptButton = ({ switchToScript }) => {
    return (
        <Button
            onClick={switchToScript}
            sx={{
                top: '-15px',
                right: '-25px',
                borderRadius: '0px',
                minWidth: '150px',
            }}
            variant="contained"
            endIcon={<RedoIcon />}
        >
            Return to script
        </Button>
    );
};
