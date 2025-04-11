import React from 'react';
import {useSelector, useDispatch} from 'react-redux';
import {Icon, IconButton, MenuItem, Avatar, useMediaQuery, Hidden, Box, Link} from '@mui/material';
import {CustomMenu} from 'components/CustomMenu';
import {Link as RouterLink} from 'react-router-dom';
import {useTheme} from '@mui/material/styles';
import {actions, name} from 'containers/auth/slice';
import {EnvironmentSelect} from "containers/enviroment/EnvironmentSelect";
import {Recollect} from "containers/dev/Recollect";


const LayoutTopbar = ({sidebarMode, setSidebarMode}) => {
  const {user} = useSelector((state) => state[name]);
  const dispatch = useDispatch();

  const theme = useTheme();
  const isMdScreen = useMediaQuery(theme.breakpoints.down('lg'));

  const handleSidebarToggle = () => {
    let mode;

    if (isMdScreen) {
      mode = sidebarMode === 'close' ? 'mobile' : 'close';
    } else {
      mode = sidebarMode === 'full' ? 'close' : 'full';
    }

    setSidebarMode(mode);
  };

  return (<Box
    sx={{
      top: 0,
      zIndex: 96,
      transition: 'all 0.3s ease',
      background: 'linear-gradient(180deg, rgba(255, 255, 255, 0.95) 44%, rgba(247, 247, 247, 0.4) 50%, rgba(255, 255, 255, 0))',
    }}
  >
    <Box
      sx={{
        backgroundColor: 'primary.main', height: 64, paddingLeft: {
          'xs': '14px', 'sm': '14px', 'md': '16px', 'lg': '18px', 'xl': '18px',
        }, paddingRight: {
          'xs': '14px', 'sm': '14px', 'md': '16px', 'lg': '20px', 'xl': '20px',
        }, boxShadow: theme.shadows[8],
      }}
    >
      <Box
        sx={{
          display: 'flex', justifyContent: 'space-between !important', alignItems: 'center', height: '100% !important'
        }}
      >
        <Box
          sx={{display: 'flex'}}
        >
          <IconButton
            sx={{
              '@media screen and (min-width: 1200px)': {
                display: 'none !important'
              },
            }}
            onClick={handleSidebarToggle}
            size="large"
          >
            <Icon>menu</Icon>
          </IconButton>
          <EnvironmentSelect/>
          {process.env.REACT_APP_TEST_DEV_MODE && <Recollect/>}
        </Box>
        <Box
          sx={{display: 'flex', alignItems: 'center'}}
        >
          <CustomMenu
            menuButton={
              <Box
                sx={{
                  display: 'flex',
                  alignItems: 'center',
                  cursor: 'pointer',
                  borderRadius: '24px',
                  padding: '4px',
                  '& span': {
                    margin: '0 8px',
                  }
                }}
              >
                <Hidden smDown>
                <span>
                  Hi <strong>{user?.full_name}</strong>
                </span>
                </Hidden>
                <Avatar
                  sx={{cursor: 'pointer'}}
                  src="/assets/images/avatar.svg"
                />
              </Box>
            }
          >
            <MenuItem>
              <Link
                component={RouterLink}
                sx={{
                  display: 'flex',
                  alignItems: 'center',
                  minWidth: 185,
                  color: 'unset',
                  textDecoration: 'unset'
                }}
                to='/user-profile'
              >
                <Icon> person </Icon>
                <Box component="span" sx={{paddingLeft: "1rem"}}> Profile </Box>
              </Link>
            </MenuItem>
            <MenuItem>
              <Link
                component={RouterLink}
                sx={{
                  display: 'flex',
                  alignItems: 'center',
                  minWidth: 185,
                  color: 'unset',
                  textDecoration: 'unset'
                }}
                to='/user-settings'
              >
                <Icon> settings </Icon>
                <Box component="span" sx={{paddingLeft: "1rem"}}> Settings </Box>
              </Link>
            </MenuItem>
            <MenuItem
              onClick={() => dispatch(actions.logout({}))}
              sx={{
                display: 'flex',
                alignItems: 'center',
                minWidth: 185,
                color: 'unset',
                textDecoration: 'unset'
              }}
            >
              <Icon> power_settings_new </Icon>
              <Box component="span" sx={{paddingLeft: "1rem"}}> Logout </Box>
            </MenuItem>
          </CustomMenu>
        </Box>
      </Box>
    </Box>
  </Box>
  );
};

export default React.memo(LayoutTopbar);
