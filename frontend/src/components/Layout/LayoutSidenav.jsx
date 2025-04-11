import React from 'react';
import { useTheme } from '@mui/material/styles';

import { Switch, Box, Paper } from '@mui/material';
import { convertHexToRGB } from 'utils/hex-to-rgb';
import Sidenav from '../../containers/sidenav/Sidenav';
import { FireflyLogo } from '../FireflyLogo';

const LayoutSidenav = ({ sidebarMode, setSidebarMode }) => {
    const theme = useTheme();

    const bgRGB = convertHexToRGB(theme.palette.primary.main);
    const bgImgURL = '/assets/images/sidebar/sidebar-bg-dark.jpg';

    const handleSidenavToggle = () => {
        setSidebarMode(sidebarMode === 'compact' ? 'full' : 'compact');
    };

    return (
        <Box
            sx={{
                position: 'fixed',
                top: 0,
                left: 0,
                height: '100vh',
                width: sidebarMode === 'compact' ? 'var(--sidenav-compact-width)' : 'var(--sidenav-width)',
                boxShadow: theme.shadows[8],
                backgroundRepeat: 'no-repeat',
                backgroundPosition: 'top',
                backgroundSize: 'cover',
                zIndex: 111,
                overflow: 'hidden',
                color: 'text.primary',
                transition: 'all 250ms ease-in-out',
                backgroundImage: `linear-gradient(to bottom, rgba(${bgRGB}, 0.96), rgba(${bgRGB}, 0.96)), url(${bgImgURL})`,
                '&:hover': {
                    width: 'var(--sidenav-width)',
                    '& .sidenavHoverShow': {
                        display: 'block',
                    },
                    '& .compactNavItem': {
                        width: '100%',
                        maxWidth: '100%',
                        '& .navBulletText': {
                            display: 'none',
                        },
                    },
                },
            }}
        >
            <Box
                sx={{
                    display: 'flex',
                    flexDirection: 'column',
                    position: 'relative',
                    height: '100% !important',
                }}
            >
                <FireflyLogo sidebarMode={sidebarMode}>
                    <Paper sx={{ display: { xs: 'none', md: 'block' } }}>
                        <Switch
                            onChange={handleSidenavToggle}
                            checked={sidebarMode !== 'full'}
                            color="secondary"
                            size="small"
                        />
                    </Paper>
                </FireflyLogo>
                <Sidenav sidebarMode={sidebarMode} setSidebarMode={setSidebarMode} />
            </Box>
        </Box>
    );
};

export default React.memo(LayoutSidenav);
