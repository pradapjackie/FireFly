import React from 'react';
import { Logo } from 'components/Logo';
import { Box } from '@mui/material';

export const FireflyLogo = ({ sidebarMode, children }) => {
    const isCompact = sidebarMode === 'compact';
    return (
        <Box
            sx={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between !important',
                padding: '20px 18px 20px 29px',
            }}
        >
            <Box
                sx={{
                    display: 'flex',
                    alignItems: 'center',
                }}
            >
                <Logo />
                <Box
                    className="sidenavHoverShow"
                    component="span"
                    sx={[
                        {
                            fontSize: '18px !important',
                            marginLeft: '0.5rem !important',
                            fontWeight: '500 !important',
                        },
                        isCompact && {
                            display: 'none',
                        },
                    ]}
                >
                    FireFly
                </Box>
            </Box>
            <Box className="sidenavHoverShow" sx={[isCompact && { display: 'none' }]}>
                {children || null}
            </Box>
        </Box>
    );
};
