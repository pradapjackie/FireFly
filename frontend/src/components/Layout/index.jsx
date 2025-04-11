import React, {useEffect, useState} from 'react';
import {Box, useMediaQuery} from '@mui/material';
import {renderRoutes} from 'react-router-config';
import {useTheme} from '@mui/material/styles';
import SidenavTheme from 'styles/GlobalTheme/SidenavTheme/SidenavTheme';
import {TopbarTheme} from 'styles/GlobalTheme/TopbarTheme';
import LayoutSidenav from './LayoutSidenav';
import LayoutTopbar from './LayoutTopbar';
import {CustomSuspense} from "components/CustomSuspense";
import {routes} from "routes/root";
import AppAlert from "../../containers/alerts";

const Index = () => {
  const [sidebarMode, setSidebarMode] = useState("full");

  const SidenavWidthClasses = {
    full: 'var(--sidenav-width)',
    compact: 'var(--sidenav-compact-width)',
  };

  const sidenavWidth = SidenavWidthClasses[sidebarMode] || '0px';
  const theme = useTheme();
  const isMdScreen = useMediaQuery(theme.breakpoints.down('lg'));

  useEffect(() => {
    setSidebarMode(isMdScreen ? 'close' : 'full')
  }, [isMdScreen]);

  return (
    <Box
      sx={{
        background: `${theme.palette.background.default} !important`
      }}
    >
      {sidebarMode !== 'close' && (
        <SidenavTheme>
          <LayoutSidenav sidebarMode={sidebarMode} setSidebarMode={setSidebarMode}/>
        </SidenavTheme>
      )}

      <Box
        sx={{
          verticalAlign: 'top',
          marginLeft: sidenavWidth,
          transition: 'all 0.3s ease',
          marginRight: 0,
          flexGrow: '1',
          display: 'flex',
          flexDirection: 'column',
          position: 'relative',
          overflow: 'hidden !important',
          height: '100vh'
        }}
      >
        <TopbarTheme>
          <LayoutTopbar sidebarMode={sidebarMode} setSidebarMode={setSidebarMode} fixed/>
        </TopbarTheme>

        <Box
          sx={{
            display: 'flex',
            flexDirection: 'column',
            flexGrow: '1',
            position: 'relative',
            height: '100%',
            overflowX: 'hidden',
            overflowY: 'auto'
          }}
        >
          <Box
            sx={{
              position: 'relative',
              flexGrow: '1'
            }}
          >
            <CustomSuspense>
              <Box sx={{margin: {'xs': '14px', 'sm': '14px', 'md': '16px', 'lg': '30px', 'xl': '30px'}}}>
                {renderRoutes(routes)}
              </Box>
            </CustomSuspense>
          </Box>
        </Box>
      </Box>
      <AppAlert/>
    </Box>
  );
};

export default React.memo(Index);
