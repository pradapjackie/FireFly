import { Box } from '@mui/material';
import React from 'react';
import { useTheme } from '@mui/material/styles';
import {convertHexToRGB} from "../../utils/hex-to-rgb";

export const DotLoading = () => {
    const theme = useTheme();

    return (
        <Box
            sx={{
                position: 'relative',
                width: '10px',
                height: '10px',
                borderRadius: '5px',
                backgroundColor: 'primary.main',
                color: 'primary.main',
                '@keyframes dot-flashing': {
                    '0%': {
                        backgroundColor: 'primary.main',
                    },
                    '50%, 100%': {
                        backgroundColor: `rgba(${convertHexToRGB(theme.palette.primary.main)}, 0.2)`,
                    },
                },
                animation: 'dot-flashing 1s infinite linear alternate',
                animationDelay: '0.5s',
                '&:before': {
                    content: '""',
                    display: 'inline-block',
                    position: 'absolute',
                    top: '0',
                    left: '-15px',
                    width: '10px',
                    height: '10px',
                    borderRadius: '5px',
                    backgroundColor: 'primary.main',
                    color: 'primary.main',
                    animation: 'dot-flashing 1s infinite alternate',
                    animationDelay: '0s',
                },
                '&:after': {
                    content: '""',
                    display: 'inline-block',
                    position: 'absolute',
                    top: '0',
                    left: '15px',
                    width: '10px',
                    height: '10px',
                    borderRadius: '5px',
                    backgroundColor: 'primary.main',
                    color: 'primary.main',
                    animation: 'dot-flashing 1s infinite alternate',
                    animationDelay: '1s',
                },
            }}
        />
    );
};
